#!/usr/bin/env python

"""htc-server"""

import simplejson

from sanic import Sanic
from sanic import response
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common import HTCServerInvalidPayload

app = Sanic()
firebase = firebase_admin.initialize_app(credentials.Certificate("hacktheclassroom.firebase.json"), {
    'databaseURL': "https://hacktheclassroom-34a66.firebaseio.com"
})
# User id to room id collection object
u2r = firestore.client().collection("uid_to_rid")


def validate_server_code(server_code):
    if len(server_code) != 6:
        return response.json({'success': False})

    result = list(u2r.where('rid', "==", server_code).get())
    if result:
        # uid = result[0].get('uid')
        return response.json({"success": True})
    else:
        return response.json({'success': False})


def solve_check(level_id, flag):
    """Check if the Flag is correct for a given Level ID."""
    raise NotImplementedError


def score_lookup(username):
    """Get the score of a player."""
    raise NotImplementedError


@app.route('/validate', methods=['GET', ])
async def validate(request):
    """Validate server code."""
    try:
        server_code = request.json['server_code']
    except KeyError:
        raise HTCServerInvalidPayload

    return validate_server_code(server_code)


@app.route('/solve', methods=['GET', ])
async def solve(request):
    """Attempt to solve a puzzle."""

    try:
        level_id = request.json['level_id']
        flag = request.json['flag']
    except KeyError:
        raise HTCServerInvalidPayload

    # TODO: check Level ID and Flag here :)
    # solve_check(level_id, flag)

    return response.json({'success': True})


@app.route('/score/<username>', methods=['GET', ])
async def get_score(request, username):
    """Get the score of a player given a username."""

    # TODO: get player score
    # score_lookup(username)

    return response.json({'score': 100})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51337)
