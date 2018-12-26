#!/usr/bin/env python

import api_client.base as base


cli = base.ApiClientBase()

msg = {
    'realm': 'default',
    'sn': 'FG800D3916801596',
    'cluster_members':
        "['FG800D3916801596', 'FGVM8V0000159780', 'FGVMULTM18000178']"
}

res = cli.render('DELETE_USER', **msg)
