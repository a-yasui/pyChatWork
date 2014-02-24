# coding: utf-8

from . import Model

class Account (Model):
    def __init__(self, data):
        Model.__init__(self, data)
