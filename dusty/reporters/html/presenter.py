#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,R0903

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
    HTML report presenter
"""


class HTMLPresenter:
    """ HTML presenter """

    def __init__(self, context):
        self.context = context

    @property
    def project_name(self):
        """ Returns project name """
        return self.context.config["general"]["settings"]["project_name"]

    @property
    def project_meta(self):
        """ Returns project meta """
        return list()

    @property
    def project_alerts(self):
        """ Returns project alerts """
        return list()

    @property
    def project_findings(self):
        """ Returns project findings """
        return list()

    @property
    def project_information_findings(self):
        """ Returns project information findings """
        return list()

    @property
    def project_errors(self):
        """ Returns project errors """
        return list()
