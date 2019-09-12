#!/usr/bin/env python3
#
# Copyright 2018 - The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Unittest constants.

Unittest constants get their own file since they're used purely for testing and
should not be combined with constants_defaults as part of normal aidegen
operation.
"""

import os

from aidegen.lib import common_util

# The data below is only for test usage.
TEST_DATA_PATH = os.path.join(common_util.get_aidegen_root_dir(), "test_data")
IDEA_SH_FIND = [
    '/opt/intellij-ce-2018.1/bin/idea.sh', '/opt/intellij-ce-2017.2/bin/idea.sh'
]  # script path data

SH_GODEN_SAMPLE = '/opt/intellij-ce-2018.1/bin/idea.sh'

IDEA_SH_FIND_NONE = ''  # Neither IntelliJ CE nor UE script exists.
TEST_PATH = 'path'
TEST_MODULE = 'test'
ANDROID_SOURCE_DICT = {
    'test_data/project/level11/level21': True,
    'test_data/project/level11/level22/level31': False,
    'test_data/project/level12/level22': False,
}
JAR_DEP_LIST = ['test1.jar', 'test2.jar']
ANDROID_PROJECT_PATH = os.path.join(TEST_DATA_PATH, 'android_project')
MODULE_PATH = 'packages/apps/test'
MODULE_INFO = {
    'path': [MODULE_PATH],
    'srcs': [
        'packages/apps/test/src/main/java/com/android/java.java',
        'packages/apps/test/tests/com/android/test.java',
        'packages/apps/test/tests/test.srcjar'
    ],
    'dependencies': [],
    'installed': []
}
