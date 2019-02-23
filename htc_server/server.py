#!/usr/bin/env python

"""htc-server"""

import simplejson

from sanic import Sanic
from sanic import response

from common import HTCServerInvalidPayload

app = Sanic()


@app.route('/solve', methods=['POST'])
async def solve(request):
    try:
        level_id = request.json['level_id']
        flag = request.json['flag']
    except KeyError:
        raise HTCServerInvalidPayload

    # check Level ID and Flag here :)

    return response.json({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51337)
