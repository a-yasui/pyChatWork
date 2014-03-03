# coding: utf-8

class ChatWorkError(Exception):
    def __init__(self, message, status, error_info):
        Exception.__init__(self, message)
        self.status = status
        self.error_info = error_info

class ArgumentUnknownTypeError (ChatWorkError):
	pass

class InvalidRequestError (ChatWorkError):
	pass

class AuthenticationError (ChatWorkError):
	pass


