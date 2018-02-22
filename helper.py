#!/usr/bin/env python3
import os


def bool_env(env, default=False):
    """docstring for bool_env"""
    e = os.getenv(env)
    if e:
        return e.upper() == 'TRUE'
    else:
        return default
