__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
minecraft.py
- Minecraft server controller
"""


from flask import current_app
import yaml, json
import os
import logging
from minecraft_manager import constants
from minecraft_manager.utils.users import validate_action
import subprocess, shlex, threading


def load_servers(app:object):
    with open(os.environ[constants.SERVERS_FILE]) as s:
        data = yaml.load(s, Loader=yaml.FullLoader)
        app.logger.debug("data: %s", data)

        app.config[constants.SERVERS] = data['servers']


def _task(server:dict, action:dict, user:str):
    print(f"server: {server}, action: {action}, user: {user}")

    env = {}
    args = shlex.split(action['script'])
    print(f"args: {args}")
    cwd = server['path']
    print(f"cwd: {cwd}")

    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         shell=False, cwd=cwd, env=env)
    out,err = p.communicate()
    rc = p.wait()
    print(f"rc: {rc}")
    # TODO


def execute_action(data:dict, server:dict, user:str) -> str:
    current_app.logger.debug("data: %s, server: %s, user: %s", data, server, user)

    action = validate_action(server, data['action'], user)

    thread = threading.Thread(target=_task,
                              kwargs={
                                'server': server,
                                'action': action,
                                'user': user
                              })
    thread.start()

    return "1" # TODO
