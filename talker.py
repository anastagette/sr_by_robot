#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import pyaudio
from vosk import Model, KaldiRecognizer
import rospy
from std_msgs.msg import String

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

model = Model("model")
rec = KaldiRecognizer(model, 16000)

dictionary = {'вперёд': 'forward', 'назад': 'backwards', 'налево': 'left', 'направо': 'right',
              'влево': 'left', 'вправо': 'right', 'стоп': 'stop', 'разверн': 'turn around', 'иди': 'go', 'стой': 'stop'}

def talker():
    result = str()
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            for word in dictionary:
                if word in result:
                    result = dictionary[word]
                    rospy.loginfo(result)
                    pub.publish(result)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        res = rec.FinalResult()
    except KeyBoardInterrupt:
        res = rec.FinalResult()