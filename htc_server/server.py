#!/usr/bin/env python

"""htc-server"""

import json

from sanic import Sanic
from sanic import response

app = Sanic()


@app.route('/<foo>')
async def lookup(request, foo):
    data = {'foo': foo}
    return response.text(data)


#@app.route("/", methods=['POST',])
#async def post_handler(request):
#    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51337)
