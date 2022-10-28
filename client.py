import threading

import grpc

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

address = 'localhost'
port = 11912


class Client:

    def __init__(self, u: str):
        # the frame to put ui components on
        # self.window = window
        self.username = u
        self.end_user = None
        self.active_users = {}
        # create a gRPC channel + stubrpc.ChatServerStub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        
        self.join_chatspace()
        print("You are connected to the chat server")
        self.menu()

    def menu(self):
        print('''Hi, this is the menu page. The available options are: 
1. Chat 
2. Exit
Please enter your choice (number):''')
        option = int(input())
        if option == 2: 
            quit()
        elif option == 1:
            self.chat()
        else:
            print("Please select a valid option")
            self.menu()
    
    def chat(self):
        print("You can enter '/back' to return to menu")
        self.get_users_list()
        self.end_user = input("Please enter the name of the user to chat with: ")
        if self.end_user == '/back':
            self.end_user = None
            self.menu()
            return 
        if self.end_user not in self.active_users:
            print("Please enter the correct username:")
            chat()
            return

        if len(self.active_users[self.end_user]) > 0:
            for msg in self.active_users[self.end_user]:
                print("{}: {}".format(msg.name, msg.message))
        
        while True:
            message = input("{}(Me): ".format(self.username))
            if message == "/back":
                self.end_user = None
                self.menu()
                return 
            if message != '':
                note = chat.Note()  # create protobug message (called Note)
                note.name = self.username  # set the username
                note.message = message  # set the actual message of the note
                note.dest = self.end_user
                # print("S[{}] {}".format(n.name, n.message))  # debugging statement
                
                self.conn.SendNote(note)  # send the Note to the server

    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        userName = chat.UserName();
        userName.username = self.username
        for note in self.conn.ChatStream(userName):  # this line will wait for new messages from the server!
            # print("R[{}] {}".format(note.name, note.message))  # debugging statement
            if note.name == self.end_user:
                LINE_CLEAR = '\x1b[2K' 
                print('\r', end=LINE_CLEAR)
                print("{}: {}\n{}(Me): ".format(note.name, note.message,self.username), end = '')
            else:
                if note.dest in self.active_users:
                    self.active_users[note.name].append(note)
                else:
                    self.active_users[note.name] = []
                    self.active_users[note.name].append(note)

            # self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))  # add the message to the UI

    def join_chatspace(self):
        userName = chat.UserName();
        userName.username = self.username
        self.conn.JoinServer(userName)
        print("Joined the userspace")
    
    def get_users_list(self):
        i = 1
        users_list = self.conn.getListOfUsers(chat.Empty())
        print("Below is the list of active users: ")
        for user in users_list.users:
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

if __name__ == '__main__':
    #root = Tk()  # I just used a very simple Tk window for the chat UI, this can be replaced by anything
    #frame = Frame(root, width=300, height=300)
    #frame.pack()
    #root.withdraw()
    username = None
    while username is None:
        # retrieve a username so we can distinguish all the different clients
        #username = simpledialog.askstring("Username", "What's your username?", parent=root)
        username = input("Please enter your username: ")
    # root.deiconify()  # don't remember why this was needed anymore...
    # c = Client(username, frame)  # this starts a client and thus a thread which keeps connection to server open
    c = Client(username)