#!/usr/bin/env python

"""htc-server"""

import simplejson

from sanic import Sanic
from sanic import response

from common import HTCServerInvalidPayload

app = Sanic()


def validate_server_code(server_code):
    """Validate the server code."""
    raise NotImplementedError


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

    # TODO: validate server code
    # validate_server_code(server_code)

    return response.json({'success': True})


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
