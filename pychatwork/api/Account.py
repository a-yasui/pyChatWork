# coding: utf-8
import pychatwork.api.model.Account

class Account:
	def __init__ (self, chatwork):
		self.chatwork = chatwork

	def retrieve (self):
		return pychatwork.api.model.Account.Account(self.chatwork.get("/me"))
