# Copyright 2017 Andrew Lawrence

from ast import Module
from exceptions import MaudeException
import termparser


class Context:
    def __init__(self):
        self._modules = set()
        self._termparser = None

    def add_module(self, module: Module):
        self._modules.add(module)
        self._termparser = termparser.generateTermParsers(self._modules)


    def get_termparser(self):
        return self._termparser


