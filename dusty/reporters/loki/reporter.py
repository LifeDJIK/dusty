#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,R0902,E0401

#   Copyright 2019 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    Reporter: loki logging support
"""

import logging
from queue import Queue

import logging_loki

from dusty.tools import log
from dusty.models.module import DependentModuleModel
from dusty.models.reporter import ReporterModel


class Reporter(DependentModuleModel, ReporterModel):
    """ Log to Grafana Loki instance """

    def __init__(self, context):
        """ Initialize reporter instance """
        self.context = context
        self.config = \
            self.context.config["reporters"][__name__.split(".")[-2]]
        self.errors = list()
        self.meta = dict()
        self._enable_loki_logging()

    def _enable_loki_logging(self):
        loki_username = self.config.get("username", None)
        loki_password = self.config.get("password", None)
        auth = None
        if loki_username and loki_password:
            auth = (loki_username, loki_password)
        if self.config.get("async", False):
            mode = "async"
            handler = logging_loki.LokiQueueHandler(
                Queue(-1),
                url=self.config.get("url"),
                tags={"project": self.context.config["general"]["settings"]["project_name"]},
                auth=auth,
            )
        else:
            mode = "sync"
            handler = logging_loki.LokiHandler(
                url=self.config.get("url"),
                tags={"project": self.context.config["general"]["settings"]["project_name"]},
                auth=auth,
            )
        logging.getLogger("").addHandler(handler)
        log.info("Enabled Loki logging in %s mode", mode)

    def report(self):
        """ Report """

    def flush(self):
        """ Flush results """
        for handler in logging.getLogger("").handlers:
            handler.flush()

    def get_errors(self):
        """ Get errors """
        return self.errors

    def get_meta(self, name, default=None):
        """ Get meta value """
        if name in self.meta:
            return self.meta[name]
        return default

    def set_meta(self, name, value):
        """ Set meta value """
        self.meta[name] = value

    def on_start(self):
        """ Called when testing starts """

    def on_finish(self):
        """ Called when testing ends """

    def on_scanner_start(self, scanner):
        """ Called when scanner starts """

    def on_scanner_finish(self, scanner):
        """ Called when scanner ends """

    @staticmethod
    def fill_config(data_obj):
        """ Make sample config """
        data_obj.insert(
            len(data_obj), "url", "http://loki.example.com:3100/api/prom/push",
            comment="Loki instance URL"
        )
        data_obj.insert(
            len(data_obj), "username", "some_user",
            comment="(optional) Loki username"
        )
        data_obj.insert(
            len(data_obj), "password", "some_password",
            comment="(optional) Loki password"
        )
        data_obj.insert(
            len(data_obj), "async", True,
            comment="(optional) Use async logging"
        )

    @staticmethod
    def validate_config(config):
        """ Validate config """
        if "url" not in config:
            log.error("No Loki URL defined in config")
            raise ValueError("No Loki URL defined in config")

    @staticmethod
    def depends_on():
        """ Return required depencies """
        return []

    @staticmethod
    def run_after():
        """ Return optional depencies """
        return ["emails"]

    @staticmethod
    def get_name():
        """ Reporter name """
        return "Loki"

    @staticmethod
    def get_description():
        """ Reporter description """
        return "Grafana Loki reporter"