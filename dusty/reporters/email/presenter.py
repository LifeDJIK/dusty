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
    EMail presenter
"""

from .models import EMailJiraTicket, EMailError


class EMailPresenter:
    """ EMail presenter """

    def __init__(self, context, config):
        self.context = context
        self.config = config

    @property
    def subject(self):
        """ Returns mail subject """
        return self.config.get(
            "subject",
            "{} {} {} {} {} scanning {} results".format(
                self.context.get_meta("project_name", "UNKNOWN"),
                self.context.get_meta("project_description", "Unnamed"),
                self.context.get_meta("environment_name", "unknown"),
                self.context.get_meta("testing_type", "UNKN"),
                self.context.get_meta("scan_type", "unknown"),
                self.context.get_meta("build_id", "#0"),
            )
        )

    @property
    def body(self):
        """ Returns mail body """
        return self.config.get("body", "Please see the results attached.")

    @property
    def attachments(self):
        """ Returns mail attachments """
        result = list()
        # Attach HTML report (if any)
        report_file = \
            self.context.performers["reporting"].get_module_meta("html", "report_file", None)
        if report_file:
            result.append(report_file)
        return result

    @property
    def errors(self):
        """ Returns project errors """
        result = list()
        for item in self.context.errors:
            result.append(EMailError(
                tool=item.tool,
                title=item.error
            ))
        result.sort(key=lambda item: (item.tool, item.title))
        return result

    @property
    def new_jira_tickets(self):
        """ Returns created Jira tickets """
        result = list()
        tickets = self.context.performers["reporting"].get_module_meta("jira", "new_tickets", None)
        if tickets:
            for _ in tickets:
                result.append(EMailJiraTicket(
                    jira_id="", jira_url="", priority="", status="",
                    open_date="", description="", assignee=""
                ))
        result.sort(key=lambda item: item.jira_id)
        return result

    @property
    def existing_jira_tickets(self):
        """ Returns existing Jira tickets """
        result = list()
        tickets = \
            self.context.performers["reporting"].get_module_meta("jira", "existing_tickets", None)
        if tickets:
            for _ in tickets:
                result.append(EMailJiraTicket(
                    jira_id="", jira_url="", priority="", status="",
                    open_date="", description="", assignee=""
                ))
        result.sort(key=lambda item: item.jira_id)
        return result