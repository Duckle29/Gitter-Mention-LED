#import RPIO
import json
import gitterest
gitter_token = ""
room_name = "dumle29/api-test"
#room_name = "scanlime/live"
gitter = gitterest.Gitter(gitter_token)
unreadMentions = []

stream = gitter.roomStream(room_name)
for line in stream.iter_lines():
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

        print('ID: {}\nUnread: {}\nMentions: {}\n'.format(postID,unread,mentions))
        for mention in mentions:
            if mention['screenName'] == 'dumle29':
                unreadMentions.append(postID)
                break;
