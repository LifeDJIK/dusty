#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,R0903,R0902

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
    Context helper
"""

from dusty.tools import log
from dusty.tools.dict import LastUpdatedOrderedDict


class RunContext:
    """ Holds invocation context """

    def __init__(self, args):
        """ Initialize context instance """
        log.debug("Initializing context")
        self.args = args
        self.config = dict()
        self.suite = ""
        self.results = list()
        self.errors = dict()  # scanner -> errors
        self.scanners = LastUpdatedOrderedDict()  # scanner -> instance
        self.processing = LastUpdatedOrderedDict()  # processor -> instance
        self.reporters = LastUpdatedOrderedDict()  # reporter -> instance
        self.performers = dict()  # performer -> instance
