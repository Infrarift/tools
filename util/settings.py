# -*- coding: utf-8 -*-

"""
cluster-node | settings | 10/05/18
Meant to be used as a super-class, to load in attributes from the environment.
"""

import json
import os

from dotenv import load_dotenv

from tools.util.logger import Logger

__author__ = "Jakrin Juangbhanich"
__copyright__ = "Copyright 2018, GenVis Pty Ltd."
__email__ = "juangbhanich.k@gmail.com"
__version__ = "0.0.0"


class Settings:

    DOT_ENV_LOADED: bool = False

    def __init__(self):
        pass

    @staticmethod
    def _load_dotenv():
        """ Load the default .env file if it hasn't already been loaded."""
        if Settings.DOT_ENV_LOADED:
            return
        load_dotenv(dotenv_path=".env")

    def load(self):
        """ Look for the matching attributes in the .env and set them here. """

        self._load_dotenv()
        Logger.log_special("Load Settings for {}".format(self.__class__.__name__), with_gap=True)

        for attribute in self.__dict__:
            if not hasattr(self, attribute):
                continue

            if attribute not in os.environ:
                Logger.log_field_red("{} (Default)".format(attribute), getattr(self, attribute))
                continue

            env_val = os.environ[attribute]
            attr_type = type(getattr(self, attribute))

            if attr_type is int:
                setattr(self, attribute, int(env_val))

            elif attr_type is float:
                setattr(self, attribute, float(env_val))

            elif attr_type is bool:
                setting_value = env_val == "True"
                setattr(self, attribute, setting_value)

            elif attr_type.__name__ == "NoneType":
                setattr(self, attribute, env_val)

            elif attr_type is list:
                setattr(self, attribute, json.loads(env_val))

            elif attr_type is str:
                setattr(self, attribute, env_val)

            else:
                raise Exception(
                    "Could not set attribute on settings object, the attribute {} has an unsupported type {}"
                    .format(attribute, attr_type.__name__))

            Logger.log_field(attribute, getattr(self, attribute))

