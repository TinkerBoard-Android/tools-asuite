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

"""It is an AIDEGen sub task : launch IDE task!

Takes a project file path as input, after passing the needed check(file
existence, IDE type, etc.), launch the project in related IDE.

    Typical usage example:

    launch_ide(file_path)
    launch_intellij(file_path)
"""

import logging
import os
import subprocess

# We use type command to determine whether the user has installed intelliJ
# IDEA, and the reason is that, in linux, the launch script is created by IDEA
# with specific path naming rule when installed, i.e. /opt/intellij-*/bin/
# idea.sh.

_CHECK_INTELLIJ_CMD = ['type', '/opt/intellij-*/bin/idea.sh']

# In this version, if community edition(CE) exists, AIDEGen prefers IntelliJ
# community edition(CE) over ultimate edition(UE).
# TODO(albaltai): prompt user to select a preferred IDE version from all
#                 installed versions.
_LS_CE_CMD = "ls /opt/intellij-ce-2*/bin/idea.sh | sort -r; exit 0"
_LS_UE_CMD = "ls /opt/intellij-ue-2*/bin/idea.sh | sort -r; exit 0"

# To confirm target is IDEA by project file extension
_IML_EXTENSION = ".iml"

#  To confirm target is IDEA by MUST exist folder
_IDEA_FOLDER = ".idea"


def launch_ide(file_path):
    """Launches the relative IDE by opening the passed project file.

    Args:
        file_path: The full path of the IDE project file.
    """
    assert file_path, 'Empty file path is not allowed.'
    logging.info('Project file path: %s.', file_path)
    if (os.path.isfile(file_path) and _is_intellij_project(file_path)):
        launch_intellij(file_path)
    else:
        logging.error('No IntelliJ IDEA exists.')


def launch_intellij(file_path):
    """Launches IntelliJ IDE by opening the validated project file.

    Args:
        file_path: The target IDE project file.
    """
    assert file_path, 'Empty file path is not allowed.'
    logging.info('Project file path: %s.', file_path)
    if (os.path.isfile(file_path) and _is_intellij_project(file_path)):
        # TODO(albaltai@): Remove below IDEA check after main flow did the same
        #                  check before calling launch_intellij
        if check_intellij():
            _run_intellij_sh(file_path)


def check_intellij():
    """Checks if the IntelliJ is already installed. No exception will be
       raised if IntelliJ is not installed.

    Returns:
        True if IntelliJ is installed already, otherwise False.
    """
    logging.debug('Check if IDEA exists by command: %s.',
                  _CHECK_INTELLIJ_CMD)
    try:
        subprocess.check_call(_CHECK_INTELLIJ_CMD, stderr=subprocess.STDOUT)
        logging.info('An IntelliJ IDEA exists.')
        return True
    except subprocess.CalledProcessError as err:
        logging.error('No IntelliJ IDEA: %s.', err.output)
        return False


def _is_intellij_project(file_path):
    """Checks if the path passed in is an IntelliJ project file.

    Args:
       file_path: The project file's full path.

    Returns:
        True if file_path is an IntelliJ project, otherwise False.
    """
    _, ext = os.path.splitext(os.path.basename(file_path))
    if ext and _IML_EXTENSION == ext.lower():
        path = os.path.dirname(file_path)
        logging.debug('Extracted path is: %s.', path)
        check_folder = os.path.join(path, _IDEA_FOLDER)
        return os.path.isdir(check_folder)  # There must exist a .idea folder
    return False


def _get_intellij_sh():
    """Locates the IntelliJ IDEA launch script path by below rule.

    1. If the community edition(CE) exists, use the newest CE version as
       target.
    2. If there's no CE version, launch the newest UE version if available.

    Returns:
        The sh full path, or None if neither IntelliJ version is installed.
    """
    try:
        ls_output = subprocess.check_output(
            _LS_CE_CMD, stderr=subprocess.STDOUT, shell=True)  # for newest CE
        return ls_output.splitlines()[0]
    except subprocess.CalledProcessError:
        try:
            ls_output = subprocess.check_output(
                _LS_UE_CMD, stderr=subprocess.STDOUT, shell=True)  # newest UE
            return ls_output.splitlines()[0]
        except subprocess.CalledProcessError:
            return None


def _run_intellij_sh(file_path):
    """Run launch script idea.sh with file_path as argument.

    Args:
        file_path: The path of IntelliJ IDEA project file.
    """
    sh_path = _get_intellij_sh()
    if not sh_path:
        logging.error('No suitable IntelliJ IDEA installed.')
        return

    logging.debug('Script path: %s, file path: %s.', sh_path, file_path)
    run_sh_cmd = [sh_path, file_path]
    try:
        logging.info('Run sh to launch IntelliJ IDEA project.')
        subprocess.check_call(run_sh_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        logging.error(
            'Launch file, %s failed with error: %s.', file_path, err)
