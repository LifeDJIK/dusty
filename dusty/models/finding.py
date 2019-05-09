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
    Finding models
"""

from dusty.models.meta import MetaModel


class DastFinding(MetaModel):
    """ DAST Finding """

    def __init__(self, title, description):
        super().__init__()
        self.title = title
        self.description = description


class SastFinding(MetaModel):
    """ SAST Finding """
