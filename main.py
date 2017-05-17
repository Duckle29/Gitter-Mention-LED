#!/usr/bin/python3
import RPIO
import json
import gitterest
import threading
from time import sleep

LED = 17
RPIO.setup(LED, RPIO.OUT, initial=RPIO.LOW)

username = 'dumle29'
gitter_token = ""
room_name = "scanlime/live"
gitter = gitterest.Gitter(gitter_token)
unreadMention = "0"
exit = False

output_on = False

class chatEater (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('Starting chatEater thread')
        global unreadMention
        stream = gitter.roomStream(room_name) # Open the stream
        for line in stream.iter_lines():
            if exit:
                break
            # Wait for lines and filter out keep-alive new lines
            if line and not line.isspace():
                decoded_line = line.decode('utf-8')
                parsed_json = json.loads(decoded_line)
                postID = parsed_json['id']
                unread = parsed_json['unread']
                if len(parsed_json['mentions']) > 0:
                    mentions = parsed_json['mentions']
                else:
                    mentions = []

                print("postID: {}\n unread: {}\nmentions: {}\n".format(postID, unread, mentions))

                for mention in mentions:
                    if mention['screenName'] == username:
                        unreadMention = postID
                        break
        print('Exiting chatEater thread')

class unreadChecker (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('Starting unreadChecker thread')
        global output_on
        global unreadMention
        while not exit:
            while unreadMention != "0":
                if not output_on:
                    output_on = True
                    RPIO.output(LED, True)
                # Check the stored message
                response = gitter.getMessage(room_name, unreadMention)
                unread = response['unread']
                if not unread:
                    unreadMention = "0"
                else:
                    sleep(10)

            if output_on:
                output_on = False
                RPIO.output(LED, False)
            sleep(1)
        print('Exiting unreadChecker thread')

# Create the threads
chatEaterThread = chatEater()
unreadCheckerThread = unreadChecker()

# Start the threads
chatEaterThread.start()
unreadCheckerThread.start()
chatEaterThread.join()
unreadCheckerThread.join()
