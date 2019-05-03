#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,R0902

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
    Reporter: scan time metadata
"""

import time

from dusty.tools import log
from dusty.models.module import DependentModuleModel
from dusty.models.reporter import ReporterModel


class Reporter(DependentModuleModel, ReporterModel):
    """ Add time metadata to scanners """

    def __init__(self, context):
        """ Initialize reporter instance """
        self.context = context
        self.config = \
            self.context.config["reporters"][__name__.split(".")[-2]]
        self.errors = list()
        self.meta = dict()

    def report(self):
        """ Report """

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
        log.debug("Testing started")
        self.set_meta("testing_start_time", time.time())

    def on_finish(self):
        """ Called when testing ends """
        self.set_meta("testing_finish_time", time.time())
        log.info(
            "Testing finished (%d seconds)",
            int(self.get_meta("testing_finish_time") - self.get_meta("testing_start_time"))
        )

    def on_scanner_start(self, scanner):
        """ Called when scanner starts """
        log.debug("Started scanning with %s", scanner)
        self.context.scanners[scanner].set_meta("scanner_start_time", time.time())

    def on_scanner_finish(self, scanner):
        """ Called when scanner ends """
        self.context.scanners[scanner].set_meta("scanner_finish_time", time.time())
        log.info(
            "Finished scanning with %s (%d seconds, %d results, %d errors)",
            scanner,
            int(
                self.context.scanners[scanner].get_meta("scanner_finish_time") -
                self.context.scanners[scanner].get_meta("scanner_start_time")
            ),
            len(self.context.scanners[scanner].get_results()),
            len(self.context.scanners[scanner].get_errors())
        )

    @staticmethod
    def fill_config(data_obj):
        """ Make sample config """

    @staticmethod
    def validate_config(config):
        """ Validate config """

    @staticmethod
    def depends_on():
        """ Return required depencies """
        return []

    @staticmethod
    def run_after():
        """ Return optional depencies """
        return []

    @staticmethod
    def get_name():
        """ Reporter name """
        return "TimeMeta"

    @staticmethod
    def get_description():
        """ Reporter description """
        return "Time metadata reporter"
