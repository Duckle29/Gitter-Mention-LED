"""
Most of this code is copied from gitterpy and adapted for python 3 support and
our needs.
Original Copyright (c) 2015 - Gray Cat Labs, Alex Hiam <alex@graycat.io>
"""

import requests
import json
import urllib
import logging


class Gitter:
    rest_api_url = "https://api.gitter.im/v1/"
    stream_api_url = "https://stream.gitter.im/v1/"

    def __init__(self, api_token):
        # Same headers are used for all requests:
        self.headers = {
            "Content-Type" : "application/json; charset=utf-8",
            "Accept" : "application/json",
            "Authorization" : "Bearer {}".format(api_token)
        }

        # Find the user ID, which is used in some API requests (also tests the
        # given auth token):
        user_info = self.getUser()
        self.user_id = user_info[0].get("id")
        if not self.user_id:
            raise ValueError("Wrong token?")

    def getUser(self):
        """ Returns the info for the user.
        """
        return self._get("user")

    def getRooms(self):
        """ Returns a list of rooms the user is a part of.
        """
        return self._get("user/{}/rooms".format(self.user_id))

    def getChannels(self):
        """ Returns a list of channels nested under the user.
        """
        return self._get("user/{}/rooms".format(self.user_id))

    def getRepos(self):
        """ Returns a list of the user's repos and their associated rooms if
        available.
        """
        return self._get("user/{}/repos".format(self.user_id))

    def joinRoom(self, room_name):
        """ Joins the given room. Returns server response if successful, None
        otherwise.
        """
        return self._post("rooms", uri=room_name)

    def leaveRoom(self, room_name):
        """ Leaves the given room. Returns server response if successful, None
        otherwise.
        """
        room_id = self.roomIdFromName(room_name)
        uri = "rooms/{}/users/{}".format(room_id, self.user_id)
        return self._delete(uri)

    def sendMessage(self, room_name, message):
        """ Sends the given message in the given room. Returns server response
        if successful, None otherwise.
        """
        room_id = self.roomIdFromName(room_name)
        return self._post("rooms/{}/chatMessages".format(room_id), text=message)

    def roomStream(self, room_name):
        """ Returns a requests.request object with stream=True, which can be
        iterated over to get live messages in the given room.
        See: http://docs.python-requests.org/en/master/user/advanced/#streaming-requests
        """
        room_id = self.roomIdFromName(room_name)
        return self._stream("rooms/{}/chatMessages".format(room_id))

    def getMessage(self, room_name, message_id):
        """ Returns the requested message in the given room if successful,
        None otherwise
        """
        room_id = self.roomIdFromName(room_name)
        return self._get("rooms/{}/chatMessages/{}".format(room_id, message_id))

    def roomIdFromName(self, room_name):
        info = self._get("rooms")
        for room in info:
            if room.get("name") == room_name:
                return room.get("id")
        return None

    def _stream(self, path):
        """ Makes a GET request to the given path, returning the response
        if successful and None otherwise.
        """
        if path[0] == "/":
            path = path[1:]
        url = urllib.parse.urljoin(self.stream_api_url, path)
        return requests.get(url, headers=self.headers, stream=True)

    def _do_rest_request(self, requests_method, path, json_data=None):
        """
        Does a request to the rest API with the given function. You can pass
        e.g. `requests.get` as the `requests_method` parameter.
        """
        if path[0] == "/":
            path = path[1:]
        url = urllib.parse.urljoin(self.rest_api_url, path)
        r = requests_method(url, headers=self.headers, json=json_data)

        try:
            response = json.loads(r.content.decode())
        except ValueError:
            logging.exception('Something went wrong while querying ' + path)
            return None
        return response

    def _get(self, path):
        """ Makes a GET request to the given path, returning the response
        if successful and None otherwise.
        """
        return self._do_rest_request(requests.get, path)

    def _post(self, path, **json_data):
        """ Makes a POST request to the given path with the given data,
        returning the response if successful and None otherwise.
        """
        return self._do_rest_request(requests.post, path, json_data=json_data)

    def _delete(self, path):
        """ Makes a DELETE request to the given path, returning the
        response if successful and None otherwise.
        """
        return self._do_rest_request(requests.delete, path)
