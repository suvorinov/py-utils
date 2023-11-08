# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg <olegsuvorinov@me.com>
# @Date:   2019-07-08 16:51:27
# @Last Modified by:   Oleg Suvorinov
# @Last Modified time: 2021-08-23 18:47:26

import logging
import functools
import sys
import os
import importlib
import binascii
import time
import json
from random import choice, randint
import string
from threading import Thread
from importlib.util import spec_from_file_location, module_from_spec
from werkzeug.http import HTTP_STATUS_CODES
from flask import request, session, abort
import phonenumbers

_format = '[%(asctime)s] %(levelname)s:%(name)s: %(message)s'
logging.basicConfig(format=_format, level=logging.INFO)
logger = logging.getLogger('Helpers')


def chunk(sequence, chunk_size):
    # Делим массив на части
    res = []
    for item in sequence:
        res.append(item)
        if len(res) >= chunk_size:
            yield res
            res = []
    if res:
        yield res  # yield the last, incomplete, portion


def str_to_class(module_name, class_name, *args, **kwargs):
    """Return a class instance from a string reference"""
    class_ = None
    try:
        module_ = importlib.import_module(module_name)
        try:
            class_ = getattr(module_, class_name)(*args, **kwargs)
        except AttributeError:
            _msg = "класс {0} не определен".format(class_name)
            logger.error(_msg)
    except ImportError:
        _msg = "модуль {0} не определен".format(module_name)
        logger.error(_msg)
    return class_ or None


def plugin_name(name_options):
    if name_options is None:
        return None
    _pn = name_options.strip().split("|")[0]
    if _pn:
        return _pn
    return None


def plugin_options(name_options):

    def _int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def _float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    if name_options is None:
        return None
    _op = name_options.strip().split("|")[1:]
    _ops = {}
    for item in _op:
        _s = item.split('=')
        _v = _s[1]
        if _int(_s[1]):
            _v = int(_s[1])
        if _float(_s[1]):
            _v = float(_s[1])
        if _s[1] == '0':
            _v = False
        elif _s[1] == '1':
            _v = True
        _ops[_s[0]] = _v
    return _ops


def http_error_code(code):
    return "{0} {1}".format(code, HTTP_STATUS_CODES[code])


def mkpassword(length=16: ):
    pwd = []
    charsets = [
        'abcdefghijklmnopqrstuvwxyz',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '0123456789',
        '^!%&/()=?{[]}+~#-_.:,;<>|\\'
    ]
    charset = choice(charsets)
    while len(pwd) < length:
        pwd.append(choice(charset))
        charset = choice(list(set(charsets) - set([charset])))
    return "".join(pwd)


def is_finex_csrf_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            token = session.pop('_finex_csrf_token', None)
            if not token:
                abort(403)

            if request.data:
                data = request.get_json() or {}
                if 'finex_csrf_token' not in data:
                    abort(403)
                token_from_req = data["finex_csrf_token"]

            if request.form:
                if not request.form.get('finex_csrf_token'):
                    abort(403)
                token_from_req = request.form.get('finex_csrf_token')

            if token != token_from_req:
                abort(403)

        return func(*args, **kwargs)
    return wrapper


def generate_finex_csrf_token():
    if '_finex_csrf_token' not in session:
        session['_finex_csrf_token'] = mkpassword(24)
    return session['_finex_csrf_token']


# Чтение json файла
def read_json_file(file_name):
    data = None

    try:
        with open(file_name, 'r', encoding='utf8') as inputfile:
            data = json.load(inputfile)
    except Exception:
        logger.error("%s" % sys.exc_info()[1])
        return None
    return data


def read_json(directory_name, file_name):
    data = None
    file = os.path.join(directory_name, file_name)
    try:
        with open(file, 'r', encoding='utf8') as inputfile:
            data = json.load(inputfile)
    except Exception:
        logger.error("%s" % sys.exc_info()[1])
        return None
    return data


# Запись json файла
def write_json_file(file_name, data):
    try:
        with open(file_name, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile,
                      sort_keys=False, separators=(',', ': '),
                      indent=4, ensure_ascii=False)
    except Exception:
        return False
    return True


def write_json(data, directory_name, file_name):
    file = os.path.join(directory_name, file_name)
    try:
        with open(file, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile,
                      sort_keys=False, separators=(',', ': '),
                      indent=4, ensure_ascii=False)
    except Exception:
        return False
    return True


"""Вспомогательные методы для работы с
системой плагинов
"""


def check_plugin_directory(location):
    """Check if plugin directory exists."""
    exists = os.path.exists(os.path.join(os.getcwd(), 'app', location))
    return exists


def load_plugin(location, plugin, methods):
    if not plugin:
        return None

    if not check_plugin_directory(location):
        return None

    path = os.path.join(os.getcwd(), 'app', location, plugin + ".py")
    spec = spec_from_file_location(plugin, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    if not methods:
        return None
    for item in methods:
        if not hasattr(module, item):
            logger.error(
                "для {0} неопределен метод {1}".format(plugin, item)
            )
            return None
    return module


def uniqueid():
    random_string = ''
    random_str_seq = (
        "0123456789"
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    uuid_format = [8, 4, 4, 4, 12]
    for n in uuid_format:
        for i in range(0, n):
            random_string += str(
                random_str_seq[randint(0, len(random_str_seq) - 1)])
        if n != 12:
            random_string += '-'
    return random_string


def gen_random_object_id():
    timestamp = '{0:x}'.format(int(time.time()))
    rest = binascii.b2a_hex(os.urandom(8)).decode('ascii')
    return timestamp + rest


def password_generator(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(choice(chars) for i in range(size))


def is_valid_phone_number(phone):
    if phone:
        phone = phone.strip()
        try:
            phone = phonenumbers.parse(phone, 'RU')
        except Exception:
            return False
        if phonenumbers.is_possible_number(phone) and \
           phonenumbers.is_valid_number(phone):
            return True
    return False


def a_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
        return func(*args, **kwargs)
    return wrapper
