# coding: utf-8

import json
import logging

class Model (object):
    def __init__(self, data):
        self._data = data

        for k, v in data.items():
            self.__dict__[k] = self._instantiate_field(k, v)
    
    def _instantiate_field (self, k, v):
        return v
