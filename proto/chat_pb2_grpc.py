# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_pb2 as chat__pb2


class ChatServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ChatStream = channel.unary_stream(
                '/grpc.ChatServer/ChatStream',
                request_serializer=chat__pb2.UserName.SerializeToString,
                response_deserializer=chat__pb2.Note.FromString,
                )
        self.SendNote = channel.unary_unary(
                '/grpc.ChatServer/SendNote',
                request_serializer=chat__pb2.Note.SerializeToString,
                response_deserializer=chat__pb2.Empty.FromString,
                )
        self.JoinServer = channel.unary_unary(
                '/grpc.ChatServer/JoinServer',
                request_serializer=chat__pb2.UserName.SerializeToString,
                response_deserializer=chat__pb2.Empty.FromString,
                )
        self.getListOfUsers = channel.unary_unary(
                '/grpc.ChatServer/getListOfUsers',
                request_serializer=chat__pb2.Empty.SerializeToString,
                response_deserializer=chat__pb2.UsersList.FromString,
                )
        self.getListOfOnlyUsers = channel.unary_unary(
                '/grpc.ChatServer/getListOfOnlyUsers',
                request_serializer=chat__pb2.Empty.SerializeToString,
                response_deserializer=chat__pb2.UsersList.FromString,
                )
        self.CreateGroup = channel.unary_unary(
                '/grpc.ChatServer/CreateGroup',
                request_serializer=chat__pb2.Group.SerializeToString,
                response_deserializer=chat__pb2.Empty.FromString,
                )
        self.FtpUploadFile = channel.stream_stream(
                '/grpc.ChatServer/FtpUploadFile',
                request_serializer=chat__pb2.FtpUploadRequest.SerializeToString,
                response_deserializer=chat__pb2.StringResponse.FromString,
                )
        self.FtpDownloadFile = channel.unary_stream(
                '/grpc.ChatServer/FtpDownloadFile',
                request_serializer=chat__pb2.FileMetadata.SerializeToString,
                response_deserializer=chat__pb2.FtpResponse.FromString,
                )


class ChatServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ChatStream(self, request, context):
        """This bi-directional stream makes it possible to send and receive Notes between 2 persons
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendNote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getListOfUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getListOfOnlyUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FtpUploadFile(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FtpDownloadFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ChatStream': grpc.unary_stream_rpc_method_handler(
                    servicer.ChatStream,
                    request_deserializer=chat__pb2.UserName.FromString,
                    response_serializer=chat__pb2.Note.SerializeToString,
            ),
            'SendNote': grpc.unary_unary_rpc_method_handler(
                    servicer.SendNote,
                    request_deserializer=chat__pb2.Note.FromString,
                    response_serializer=chat__pb2.Empty.SerializeToString,
            ),
            'JoinServer': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinServer,
                    request_deserializer=chat__pb2.UserName.FromString,
                    response_serializer=chat__pb2.Empty.SerializeToString,
            ),
            'getListOfUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.getListOfUsers,
                    request_deserializer=chat__pb2.Empty.FromString,
                    response_serializer=chat__pb2.UsersList.SerializeToString,
            ),
            'getListOfOnlyUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.getListOfOnlyUsers,
                    request_deserializer=chat__pb2.Empty.FromString,
                    response_serializer=chat__pb2.UsersList.SerializeToString,
            ),
            'CreateGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateGroup,
                    request_deserializer=chat__pb2.Group.FromString,
                    response_serializer=chat__pb2.Empty.SerializeToString,
            ),
            'FtpUploadFile': grpc.stream_stream_rpc_method_handler(
                    servicer.FtpUploadFile,
                    request_deserializer=chat__pb2.FtpUploadRequest.FromString,
                    response_serializer=chat__pb2.StringResponse.SerializeToString,
            ),
            'FtpDownloadFile': grpc.unary_stream_rpc_method_handler(
                    servicer.FtpDownloadFile,
                    request_deserializer=chat__pb2.FileMetadata.FromString,
                    response_serializer=chat__pb2.FtpResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grpc.ChatServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ChatStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/grpc.ChatServer/ChatStream',
            chat__pb2.UserName.SerializeToString,
            chat__pb2.Note.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendNote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/SendNote',
            chat__pb2.Note.SerializeToString,
            chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def JoinServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/JoinServer',
            chat__pb2.UserName.SerializeToString,
            chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getListOfUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/getListOfUsers',
            chat__pb2.Empty.SerializeToString,
            chat__pb2.UsersList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getListOfOnlyUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/getListOfOnlyUsers',
            chat__pb2.Empty.SerializeToString,
            chat__pb2.UsersList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/grpc.ChatServer/CreateGroup',
            chat__pb2.Group.SerializeToString,
            chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FtpUploadFile(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/grpc.ChatServer/FtpUploadFile',
            chat__pb2.FtpUploadRequest.SerializeToString,
            chat__pb2.StringResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FtpDownloadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/grpc.ChatServer/FtpDownloadFile',
            chat__pb2.FileMetadata.SerializeToString,
            chat__pb2.FtpResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
