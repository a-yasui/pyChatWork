# coding: utf-8

from . import Model

class Message (Model):
    def __init__(self, data):
        Model.__init__(self, data)
