from ast import Return
import os
import sys
import threading

import grpc

sys.path.insert(1, './proto')
import chat_pb2 as chat
import chat_pb2_grpc as rpc

address = 'localhost'
# address ='54.235.29.223'
port = 11912


class Client:

    def __init__(self):
        # the frame to put ui components on
        # self.window = window
        self.username = None
        self.end_user = None
        self.active_users = {}
        # create a gRPC channel + stubrpc.ChatServerStub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        # create new listening thread for when new message streams come in
        
        
        self.pre_menu()
        #below functions means the user is active. 
        self.join_chatspace()
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        print("You are connected to the chat server")
        self.menu()


    def pre_menu(self):
        while True:
            print("Hi, welcome to the chatspace!!!!")
            choice = input('''Do you want to\n1.Register\n2.LogIn\n3.Quit\n Indicate via entering the number:''')
            choice = int(choice)
            if choice == 1:
                self.register()
                break
            elif choice == 2:
                self.logIn()
                break
            elif choice == 3:
                print("Quitting")
                quit()
                break
            else:
                print("Please select a valid option")
        return

    def register(self):
        print("REGISTER: Please choose an username and a password: ")
        username_selected = input("username:")
        password_selected = input("password:")
        # check uniqueness of username
        user = chat.UserName()
        user.username = username_selected
        resp = self.conn.CheckUniqueUser(user)
        if not resp.response:
            print("Username already taken, please choose another one:")
            self.register()
            return 
        # register user
        new_user = chat.UsernamePassword()
        new_user.username = username_selected
        new_user.password = password_selected
        resp = self.conn.Register(new_user)
        print("Successfully registered, you can logIn now")
        self.logIn()
    
    def logIn(self):
        #Take input
        print("LOGIN PAGE: Please enter you username and password: ")
        username_selected = input("username:")
        password_selected = input("password:")
        user_details = chat.UsernamePassword()
        user_details.username = username_selected
        user_details.password = password_selected
        resp = self.conn.CheckUserExists(user_details)
        #checkUserExists()
        #if yes. joinserver call, if no. Say details wrong, please reenter
        if resp.response :
            print("logging in....")
            self.username = user_details.username
        else:
            print("Details entered are incorrect. Please check your username and password")
            self.pre_menu()

    def menu(self):
        print('''Hi, this is the menu page. The available options are: \n1. Chat \n2. Create New Group \n3. Exit\nPlease enter your choice (number):''')
        option = int(input())
        if option == 3: 
            quit()
        elif option == 2:
            self.createNewGroup()
        elif option == 1:
            self.chat()
        else:
            print("Please select a valid option")
            self.menu()
    
    def chat(self):
        print("You can enter '/back' to return to menu")
        self.get_users_list()
        self.end_user = input("Please enter the name of the user/group to chat with: ")
        if self.end_user == '/back':
            self.end_user = None
            self.menu()
            return 
        if self.end_user not in self.active_users:
            print("Please enter the correct username:")
            self.chat()
            return

        if len(self.active_users[self.end_user]) > 0:
            for msg in self.active_users[self.end_user]:
                print("{}: {}".format(msg.name, msg.message))
                if msg.message.startswith("/file:"): # TODO CHECK IF THIS SNIPPET IS PLACED CORRECTLY
                    # print('dwnldng file')
                    self.handleDownloadFile(msg) # TODO make it async? thread/pool, but it might hamper other printed msgs
            
                # print('Am I here 0:',msg,msg.message.startswith("/file:"))
                # if(msg.message.startswith("/file:")):
                #     print('AM I HERE?')
                #     self.handleDownloadFile(msg) # TODO make it async? thread/pool, but it might hamper other printed msgs
            
            self.active_users[self.end_user] = []
        
        while True:
            message = input("{}(Me): ".format(self.username))
            if message == "/back":
                self.end_user = None
                self.menu()
                return 
            if message.startswith("/file:"):
                # print('Uploading section:') #   debug stmt
                responses = self.conn.FtpUploadFile(self.readIterfile(message))
                for response in responses:
                    # print(response.message)
                    print(response.message,end = '', flush=True) #   status responses to client 
                print('\n')
                continue
            if message != '':
                note = chat.Note()  # create protobuf message (called Note)
                note.name = self.username  # set the username
                note.message = message  # set the actual message of the note
                note.dest = self.end_user
                # print("S[{}] {}".format(n.name, n.message))  # debugging statement
                
                self.conn.SendNote(note)  # send the Note to the server

    def createNewGroup(self):
        group = chat.Group()
        userlist = self.get_users_list(print_options=False)
        
        print("Below is the list of active users: ")

        for i,j in enumerate(userlist):
            print(f'{i+1}. {j}')
        
        print('Please enter a space separated list of usernames you want to include in\nthe group - ')
        # group.users = ' '.split(input().strip())
        user_input = input()
        user_input = user_input.strip().split()
        user_input = [i for i in user_input if i in userlist]
        print('Please enter the group name - ')
        group.GroupName = input()
        group.username = self.username

        for i in user_input:
            group.users.append(i)

        if self.username not in group.users:
            group.users.append(self.username)

        self.conn.CreateGroup(group)

        print(f'Created Group with Group name - {group.GroupName} and users')
        for i,j in enumerate(group.users):
            print(f'{i+1}. {j}')

        self.menu()


    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        userName = chat.UserName()
        userName.username = self.username
        dest_var = ''
        for note in self.conn.ChatStream(userName):  # this line will wait for new messages from the server!
            # print("R[{}] {}".format(note.name, note.message))  # debugging statement
            # print('here2',note.message.startswith("/file:"))
            if note.dest != self.username:
            # if group message
                dest_var = note.dest
            else:
            # not group message
                dest_var = note.name

            if dest_var == self.end_user:
                LINE_CLEAR = '\x1b[2K' 
                print('\r', end=LINE_CLEAR)
                print("{}: {}\n{}(Me): ".format(note.name, note.message,self.username), end = '')   # TODO can check flush=True, if req!
                if note.message.startswith("/file:"): # TODO CHECK IF THIS SNIPPET IS PLACED CORRECTLY
                    # print('dwnldng file')
                    self.handleDownloadFile(note) # TODO make it async? thread/pool, but it might hamper other printed msgs
            
            else:
                if dest_var in self.active_users:
                    self.active_users[dest_var].append(note)
                else:
                    self.active_users[dest_var] = []
                    self.active_users[dest_var].append(note)

            # self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))  # add the message to the UI

    def join_chatspace(self):
        userName = chat.UserName()
        userName.username = self.username
        self.conn.JoinServer(userName)
        print("Joined the userspace")
    
    def get_users_list(self, print_options=True):
        i = 1
        users_list = []
        
        if print_options:
            users_list = self.conn.getListOfUsers(chat.Empty())
            print("Below is the list of active users: ")
            for user in users_list.users:
                if user == self.username:
                    continue
                if user in self.active_users:
                    # If the user's messages are unread. 1. ram [3] (this 3 indicates unread messages)
                    if len(self.active_users[user]) > 0:
                        print(str(i) + ". " + user + " [{}]".format(len(self.active_users[user])))
                    else : # len of list is 0
                        print(str(i) + ". " + user)
                else:
                    self.active_users[user] = []        
                    print(str(i) + ". " + user)
                i = i + 1
        else:
            users_list = self.conn.getListOfOnlyUsers(chat.Empty())
        return users_list.users
            
    def readIterfile(self, fileString, chunkSize=1024):
        filePath = fileString[6:]
        fileArr = filePath.rsplit("/",1) # read after "/file:"
        split_data = os.path.splitext(fileArr[-1])
        fileName = split_data[0]
        fileExtension = split_data[1]
        # print(f'fileName={fileName},fileExtension={fileExtension}, {self.username},{self.end_user}')
        # metadata = chat.FileMetadata(fileName=fileName)
        metadata = chat.FileMetadata(senderName=self.username,dest=self.end_user,fileName=fileName, fileExtension=fileExtension)
        # print(f'metadata:{metadata}')
        # first send off the file name(with extension) of the file we are reading iteratively, to upload
        
        yield chat.FtpUploadRequest(fileMetadata=metadata)
        # res = chat.FtpUploadRequest(fileMetadata=metadata)
        # print(f'res:{res}')
        # yield res
        f = None
        try:
            f = open(filePath, mode="rb")
        except FileNotFoundError:
            print(f'Unable to find/open file:{filePath}')
            return
        
        # with open(filePath, mode="rb") as f:
        # print('file opened')
        while True:
            chunkOfFile = f.read(chunkSize)
            # print('a')
            if chunkOfFile:
                # now return the file data in chunks
                # print('b')
                entry_request = chat.FtpUploadRequest(chunkOfFile=chunkOfFile)
                # print(f'yielding {entry_request}')
                yield entry_request
            else:  # The chunk was empty, which means we're at the end of the file
                f.close()
                return

    def handleDownloadFile(self, note):
        # this should be non blocking/async?
        
        # TODO : PRINT STATEMENTS and STREAM STATUS
        # TODO : NOT A GOOD WAY TO USE CHAT MESSAGE TEXT TO INITIATE DOWNLOAD, CAN'T SEND ANYTHING OTHER THAN EXACT "/file:..."

        split_data = os.path.splitext(note.message[6:])  # read after "/file:"
        fileName = split_data[0]
        fileExtension = split_data[1]
        filePath = f'clientFiles/{fileName}{fileExtension}'    # TODO destination path
        # print(f'handleDownload:{filePath}')
        
        f=None
        try:
            f = open(filePath, mode="ab")
        except FileNotFoundError:
            print(f'Unable to find/open/create file:{filePath}')
            return
        for entry_response in self.conn.FtpDownloadFile(chat.FileMetadata(senderName=note.name, dest=note.dest, fileName=fileName, fileExtension=fileExtension)):
            # print(chat.FileMetadata(senderName=note.name, dest=note.dest, fileName=fileName, fileExtension=fileExtension))
            print(entry_response.progressReply,end='',flush=True)  # client log
            # with open(filePath, mode="ab") as f:
                # print(entry_response.chunkReply)
                # print('-', end='',flush=True)
            f.write(entry_response.chunkReply)
        # print()
        print("\n{}(Me): ".format(self.username), end = '', flush=True)
        f.close()

if __name__ == '__main__':
    c = Client()