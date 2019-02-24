#!/usr/bin/env python

"""htc-server"""

import simplejson

from sanic import Sanic
from sanic import response
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1beta1 import ArrayUnion

from common import HTCServerInvalidPayload

app = Sanic()
firebase = firebase_admin.initialize_app(credentials.Certificate("hacktheclassroom.firebase.json"), {
    'databaseURL': "https://hacktheclassroom-34a66.firebaseio.com"
})
# User id to room id collection object
u2r = firestore.client().collection("uid_to_rid")
# Level to flag collection object
l2f = firestore.client().collection("level_to_flag")


def validate_user(username, server_code):
    """
    Validate username, if the user exists in the db,
    otherwise create it
    """
    room = list(u2r.where('rid', '==', server_code).get())
    if room:
        u2r.document(room[0].id).collection("users").add({"username": username, "flags": []})


def validate_server_code(server_code):
    if len(server_code) != 6:
        return response.json({'success': False})

    result = list(u2r.where('rid', '==', server_code).get())
    if result:
        # uid = result[0].get('uid')
        return response.json({"success": True})
    else:
        return response.json({'success': False})


def add_flag_to_user(username, server_code, flag):
    """
    Add flag to user, true if success, else false
    """
    room = list(u2r.where('rid', '==', server_code).get())
    if room:
        for user in u2r.document(room[0].id).collection("users").get():
            if user.get("username") == username:
                return bool(u2r.document(room[0].id).collection("users").document(user.id)
                            .update({"flags": ArrayUnion([flag])}))
    return False


def solve_check(username, server_code, level_id, flag):
    """
    Check if the Flag is correct for a given Level ID.
    Add flag to user's collection
    """
    level = list(l2f.where("level_id", "==", level_id).get())
    correct_flag = False
    if level:
        flags = level[0].get("flags")
        if flag in flags:
            correct_flag = add_flag_to_user(username, server_code, flag)
    return response.json({"success": correct_flag})


def score_flags(flags):
    """
    Score flag
    flag format should be flagid.flag
    """
    score = 0
    for flag in flags:
        if len(flag.split(".")) != 2:
            # invalid flag
            continue

        level_id, flag_id = flag.split(".")
        if not level_id or not flag_id:
            # Invalid flag
            continue
        else:
            level = list(l2f.where('level_id', '==', level_id).get())
            if level:
                level = level[0]
                if flag_id in level.get("flags"):
                   score += score + level.get("flags").get(flag_id, 0)
    return score


def score_lookup(username, server_code):
    """Get the score of a player."""
    room = list(u2r.where('rid', '==', server_code).get())
    score = -1
    if room:
        for user in u2r.document(room[0].id).collection("users").get():
            if user.get("username") == username:
                score = score_flags(user.get("flags"))
                break
    return response.json({"score": score})


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
    """
    Attempt to solve a puzzle.
    if the user doesn't exist, create it
    """

    try:
        level_id = request.json['level_id']
        flag = request.json['flag']
        username = request.json['username']
        server_code = request.json['server_code']

    except KeyError:
        raise HTCServerInvalidPayload

    validate_user(username, server_code)
    return solve_check(username, server_code, level_id, flag)


@app.route('/score/<username>', methods=['GET', ])
async def get_score(request, username):
    """Get the score of a player given a username."""
    try:
        server_code = request.json["server_code"]
    except KeyError:
        raise HTCServerInvalidPayload

    return score_lookup(username, server_code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51337)
