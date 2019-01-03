#!/usr/bin/env python

import api_client.base as base
from api_client.templates import fas as template

cli = base.ApiClientBase()
render = lambda opt, **message: cli.render(getattr(template, opt), **message)

msg = {
    "id": "83231a53-5e62-4fc9-b4ae-3b55804545ea",
    "sn": "FG800D3916801596",
    "cluster_members":
        "['FG800D3916801596', 'FGVM8V0000159780', 'FGVMULTM18000178']"
}

print(render('DELETE_USER', **msg))
