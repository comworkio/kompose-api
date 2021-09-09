import json

from flask import request
from subprocess import check_output

def get_script_output (cmd):
    try:
        return check_output(cmd, shell=True, text=True)
    except:
        return check_output(cmd, shell=True, universal_newlines=True)

def is_forbidden (var):
    forbidden_chars = ["'" , "\"", "&", ";", "|", "\\"]
    return any(char in var for char in forbidden_chars)

def is_not_empty (var):
    if (isinstance(var, bool)):
        return var
    elif (isinstance(var, int)):
        return False
    empty_chars = ["", "null", "nil", "false", "none"]
    return var is not None and not any(c == var.lower() for c in empty_chars)

def is_empty (var):
    return not is_not_empty(var)

def is_empty_request_field (name):
    body = request.get_json(force=True)
    return not name in body or is_empty(body[name])

def get_available_versions(var):
    return json.loads(get_script_output("/versions.sh {}".format(var)))

def get_kompose_available_versions():
    return get_available_versions("KOMPOSE_VERSION")

def konvert (filename, version, provider, namespace, apply):
    return get_script_output("/konvert.sh {} {} {} {} {}".format(filename, version, provider, namespace, apply))
