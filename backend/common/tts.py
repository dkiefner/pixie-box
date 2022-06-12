#!/usr/bin/env python

import pyttsx3


class TTS:
    @staticmethod
    def say(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
