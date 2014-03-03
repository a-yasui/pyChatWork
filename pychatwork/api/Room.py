# coding: utf-8
import pychatwork.api.model.Room
import pychatwork.api.model.Message
from . import errors


class Room:
	def __init__ (self, chatwork, room=None):
		self.chatwork = chatwork
		self.room = None

		if isinstance(room, pychatwork.api.model.Room.Room):
			self.room = room

	def list (self):
		return [ pychatwork.api.model.Room.Room( data ) for data in self.chatwork.get("/rooms") ]

	def message (self, room, body):
		if getattr(room, 'room_id', None) == None:
			raise errors.ArgumentUnknownTypeError(-1, "Unknown type Room")

		message = pychatwork.api.model.Message.Message(
					self.chatwork.post(
						'/rooms/{0}/messages'.format(room.room_id), { "body": body } ))

		return pychatwork.api.model.Message.Message(
				self.chatwork.get('/rooms/{0}/messages/{1}'.format(
					room.room_id, message.message_id)))
