# coding: utf-8
from pychatwork import pyChatWork
from httmock import HTTMock

import tests.helper as helper

class TestRoom:

	def test_rooms(self):
		with HTTMock(helper.mock_api('/rooms', 'room/list.txt')):
			rooms = pyChatWork('test_key').room.list()
		assert len(rooms) == 2
		assert rooms[0].room_id == 123
		assert rooms[1].room_id == 124

	def test_message_post (self):
		chatwork = pyChatWork('test_key')
		with HTTMock(helper.mock_api('/rooms', 'room/list.txt')):
			rooms = chatwork.room.list()
		assert len(rooms) == 2
		assert rooms[0].room_id == 123
		assert rooms[1].room_id == 124

		with HTTMock(helper.mock_api('/rooms', 'room/message_post.txt')):
			msg = chatwork.room.message(rooms[0], "Test")
		assert msg.message_id == 1234
