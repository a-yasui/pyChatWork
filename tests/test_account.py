# coding: utf-8
from pychatwork import pyChatWork
from httmock import HTTMock

import tests.helper as helper

class TestAccount:

    def test_retrieve(self):
        with HTTMock(helper.mock_api('/me', 'account/retrieve.txt')):
            account = pyChatWork('test_key').account.retrieve()

        assert account.chatwork_id == 'tarochatworkid'
        assert account.mail == 'taro@example.com'
        assert account.avatar_image_url == 'https://example.com/abc.png'

