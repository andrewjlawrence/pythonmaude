# Copyright 2017 Andrew Lawrence


class MaudeException(Exception):
    def __init__(self, msg):
        super.__init__(msg)