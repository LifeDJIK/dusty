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

from dusty.models.finding import DastFinding
from dusty.constants import SEVERITIES

from .models import HTMLReportMeta, HTMLReportAlert, HTMLReportFinding, HTMLReportError


class HTMLPresenter:
    """ HTML presenter """

    def __init__(self, context):
        self.context = context

    @staticmethod
    def _item_to_finding(item):
        if isinstance(item, DastFinding):
            return HTMLReportFinding(
                tool=item.get_meta("tool", ""),
                title=item.title,
                severity=item.get_meta("severity", SEVERITIES[-1]),
                description=item.description
            )
        raise ValueError("Unsupported item type")

    @property
    def project_name(self):
        """ Returns project name """
        return self.context.config["general"]["settings"]["project_name"]

    @property
    def project_meta(self):
        """ Returns project meta """
        result = list()
        result.append(HTMLReportMeta(
            name="Project name",
            value=self.context.config["general"]["settings"]["project_name"]
        ))
        testing_time = self.context.performers["reporting"].get_module_meta(
            "time_meta", "testing_run_time", "N/A"
        )
        result.append(HTMLReportMeta(
            name="Testing time",
            value=f"{testing_time} seconds"
        ))
        return result

    @property
    def project_alerts(self):
        """ Returns project alerts """
        result = list()
        result.append(HTMLReportAlert(
            type_="warning",
            text="This report is from proof-of-concept version of Dusty 2.0"
        ))
        return result

    @property
    def project_findings(self):
        """ Returns project findings """
        result = list()
        for item in self.context.results:
            if item.get_meta("information_finding", False) or \
                    item.get_meta("false_positive_finding", False):
                continue
            result.append(self._item_to_finding(item))
        result.sort(key=lambda item: (SEVERITIES.index(item.severity), item.tool, item.title))
        return result

    @property
    def project_information_findings(self):
        """ Returns project information findings """
        result = list()
        for item in self.context.results:
            if item.get_meta("information_finding", False) and \
                    not item.get_meta("false_positive_finding", False):
                result.append(self._item_to_finding(item))
        result.sort(key=lambda item: (SEVERITIES.index(item.severity), item.tool, item.title))
        return result

    @property
    def project_false_positive_findings(self):
        """ Returns project false positive findings """
        result = list()
        for item in self.context.results:
            if item.get_meta("false_positive_finding", False):
                result.append(self._item_to_finding(item))
        result.sort(key=lambda item: (SEVERITIES.index(item.severity), item.tool, item.title))
        return result

    @property
    def project_errors(self):
        """ Returns project errors """
        result = list()
        for item in self.context.errors:
            result.append(HTMLReportError(
                tool=item.tool,
                title=item.error,
                description=item.details
            ))
        result.sort(key=lambda item: (item.tool, item.title))
        return result
