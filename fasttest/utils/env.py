#!/usr/bin/env python3

import os

class Env:
    @staticmethod
    def get_env(var_name: str, default=None):
        try:
            return os.environ[var_name]
        except KeyError:
            if default is not None:
                return default
            else:
                error_msg = f'The environment variable {var_name} is not set.'
                raise KeyError(error_msg)