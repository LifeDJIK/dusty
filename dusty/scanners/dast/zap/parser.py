#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,E0401,W0702,W0703,R0902

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
    OWASP ZAP JSON parser
"""

import json

from dusty.tools import log
from dusty.models.finding import DastFinding

from . import constants


def parse_results(data, scanner):
    """ Parse results """
    log.debug("Parsing results")
    zap_json = json.loads(data)
    for site in zap_json["site"]:
        for alert in site["alerts"]:
            description = list()
            if "desc" in alert:
                description.append(alert["desc"])
            if "solution" in alert:
                description.append(f'Solution:\n {alert["solution"]}')
            if "reference" in alert:
                description.append(f'Reference:\n {alert["reference"]}')
            if "otherinfo" in alert:
                description.append(f'Other information:\n {alert["otherinfo"]}')
            description = "\n".join(description)
            # Make finding object
            finding = DastFinding(
                title=alert["name"],
                description=description
            )
            finding.set_meta("tool", "ZAP")
            finding.set_meta("severity", constants.ZAP_SEVERITIES[alert["riskcode"]])
            finding.set_meta("confidence", constants.ZAP_CONFIDENCES[alert["confidence"]])
            scanner.results.append(finding)