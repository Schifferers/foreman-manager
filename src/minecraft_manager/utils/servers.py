__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""


from flask import current_app
import subprocess, shlex
import json


def query_server_status(server:dict) -> dict:
    current_app.logger.debug("server: %s", server)

    env = {}
    args = shlex.split(server.get('actions', {}).get('status', {}).get('script', ""))
    current_app.logger.debug("args: %s", args)
    cwd = server['path']
    current_app.logger.debug("cwd: %s", cwd)

    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         shell=False, cwd=cwd, env=env)
    out,err = p.communicate()
    status_info = json.loads(out)
    current_app.logger.debug("status_info: %s", status_info)
    rc = p.wait()
    current_app.logger.debug("rc: %d", rc)

    info = server.get('info', {
        'version': "--",
        'pid': "--",
        'status': "--",
        'hostname': "localhost",
        'port': "25565"
    })
    info.update(status_info)
    server['info'] = info

    return server
