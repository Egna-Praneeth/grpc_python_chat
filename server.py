from concurrent import futures
import os
import sys

import grpc
import time

sys.path.insert(1, './proto')
import chat_pb2 as chat
import chat_pb2_grpc as rpc


class ChatServer(rpc.ChatServerServicer):  # inheriting here from the protobuf rpc file which is generated

    def __init__(self):
        # List with all the chat history
        self.chats = []
        self.usersList = []
        self.fileDir = 'uploadedFiles/'

    # The stream which will be used to send new messages to clients
    def ChatStream(self, username: chat.UserName, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                if n.dest == username.username:
                    # print(username.username + " is a match")
                    yield n

    def SendNote(self, request: chat.Note, context):
        """
        This method is called when a clients sends a Note to the server.

        :param request:
        :param context:
        :return:
        """
        # this is only for the server console
        print("[{}] to [{}] : {}".format(request.name, request.dest, request.message))
        # Add it to the chat history
        
        self.chats.append(request)
        return chat.Empty()  # something needs to be returned required by protobuf language, we just return empty msg

    def JoinServer(self, u: chat.UserName,context):
        self.usersList.append(u.username)
        # Below for loop is to print the list.
        # i = 1
        # for user in self.usersList:
        #     print(str(i) + '. ' + user)
        #     i = i + 1
        print(u.username + ' is online.')
        return chat.Empty()

    def getListOfUsers(self,request_iterator,context):
        users_list_obj = chat.UsersList()
        for user in self.usersList:
            users_list_obj.users.append(user)
        # users_list_obj.users = self.usersList
        return users_list_obj
    
    def FtpUploadFile(self, request_iterator, context):
        '''
        upload file to server which client is streaming
        '''
        
        file = ""
        fileData = bytearray() # temporary variable to store the file
        senderName = ""
        dest = ""
        ITALIC_BEGIN = '\x1B[3m'
        ITALIC_END = '\x1B[0m'
        
        for requestData in  request_iterator:
            if requestData.fileMetadata.fileName and requestData.fileMetadata.fileExtension:
                # if file name is sent, instead of chunk of file, first get the full file name
                file = f'{requestData.fileMetadata.fileName}{requestData.fileMetadata.fileExtension}'
                senderName = requestData.fileMetadata.senderName
                dest = requestData.fileMetadata.dest
                print(f'[{senderName}] to [#SERVER#] : dest:[{dest}],file:{file}',end = '', flush=True)  # server log
                yield chat.StringResponse(message=f'{ITALIC_BEGIN}Uploading:')    # response to client  
                continue
            print('-',end = '', flush=True)    # server log
            yield chat.StringResponse(message='-')    # response to client
            fileData.extend(requestData.chunkOfFile)
        with open(self.fileDir+'/'+file, 'wb') as f:
            # write complete data in one go, could also use 'wb+' when in for loop
            f.write(fileData)
            # include in chats[] metadata of file for download
            messageForDest = f'/file:{file}'    # sending filename to dest client in chat. upto Dest to trigger download
            print(ITALIC_BEGIN+' Uploaded! '+ITALIC_END)    # server log
            self.chats.append(chat.Note(name=senderName, message=messageForDest,dest=dest))
            # print('2:',chat.Note(name=senderName, message=messageForDest,dest=dest)) # debug stmt
            yield chat.StringResponse(message=f'{ITALIC_BEGIN}Success!{ITALIC_END}')
        
    def FtpDownloadFile(self, request, context):
        '''
        download a file from server, given file name/path
        '''
        chunk_size = 1024
        filePath = f'{self.fileDir}/{request.fileName}{request.fileExtension}'
        fileNameExtension = f'{request.fileName}{request.fileExtension}'
        # print(f'file:{filePath}, requested by client:{request.dest} for download')
        ITALIC_BEGIN = '\x1B[3m'
        ITALIC_END = '\x1B[0m'
        if os.path.exists(filePath):
            # print(f'requesting file:{filePath}')
            yield chat.FtpResponse(chunkReply=None, progressReply=ITALIC_BEGIN+f'Downloading({fileNameExtension}):'+ITALIC_END)
            print(f'[#SERVER#] to [{request.dest}] : from:[{request.senderName}],file:{fileNameExtension}',end = '', flush=True)  # server log
            with open(filePath, mode="rb") as f:
                while True:
                    chunkOfFile = f.read(chunk_size)
                    if chunkOfFile:
                        fileResponse = chat.FtpResponse(chunkReply=chunkOfFile, progressReply='-')
                        print('-',end = '', flush=True)    # server log
                        yield fileResponse
                    else:  # The chunk was empty, which means we're at the end of the file
                        yield chat.FtpResponse(chunkReply=None, progressReply=ITALIC_BEGIN+'Success!'+ITALIC_END)
                        print(ITALIC_BEGIN+' Downloaded! '+ITALIC_END)    # server log
                        return


if __name__ == '__main__':
    port = 11912  # a random port for the server to run on
    # the workers is like the amount of threads that can be opened at the same time, when there are 10 clients connected
    # then no more clients able to connect to the server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # create a gRPC server
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)  # register the server to gRPC
    # gRPC basically manages all the threading and server responding logic, which is perfect!
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    # Server starts in background (in another thread) so keep waiting
    # if we don't wait here the main thread will end, which will end all the child threads, and thus the threads
    # from the server won't continue to work and stop the server
    while True:
        time.sleep(64 * 64 * 100)
