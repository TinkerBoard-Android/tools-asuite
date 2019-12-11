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


"""Unittests for ide_util."""

import os
import shutil
import subprocess
import tempfile
import unittest

from unittest import mock

from aidegen import aidegen_main
from aidegen import unittest_constants
from aidegen.lib import android_dev_os
from aidegen.lib import config
from aidegen.lib import errors
from aidegen.lib import ide_common_util
from aidegen.lib import ide_util
from aidegen.lib import project_config
from aidegen.lib import sdk_config


# pylint: disable=too-many-public-methods
# pylint: disable=protected-access
# pylint: disable-msg=too-many-arguments
class IdeUtilUnittests(unittest.TestCase):
    """Unit tests for ide_util.py."""

    _TEST_PRJ_PATH1 = ''
    _TEST_PRJ_PATH2 = ''
    _TEST_PRJ_PATH3 = ''
    _TEST_PRJ_PATH4 = ''
    _MODULE_XML_SAMPLE = ''
    _TEST_DIR = None

    def setUp(self):
        """Prepare the testdata related path."""
        IdeUtilUnittests._TEST_PRJ_PATH1 = os.path.join(
            unittest_constants.TEST_DATA_PATH, 'android_facet.iml')
        IdeUtilUnittests._TEST_PRJ_PATH2 = os.path.join(
            unittest_constants.TEST_DATA_PATH, 'project/test.java')
        IdeUtilUnittests._TEST_PRJ_PATH3 = unittest_constants.TEST_DATA_PATH
        IdeUtilUnittests._TEST_PRJ_PATH4 = os.path.join(
            unittest_constants.TEST_DATA_PATH, '.idea')
        IdeUtilUnittests._MODULE_XML_SAMPLE = os.path.join(
            unittest_constants.TEST_DATA_PATH, 'modules.xml')
        IdeUtilUnittests._TEST_DIR = tempfile.mkdtemp()

    def tearDown(self):
        """Clear the testdata related path."""
        IdeUtilUnittests._TEST_PRJ_PATH1 = ''
        IdeUtilUnittests._TEST_PRJ_PATH2 = ''
        IdeUtilUnittests._TEST_PRJ_PATH3 = ''
        IdeUtilUnittests._TEST_PRJ_PATH4 = ''
        shutil.rmtree(IdeUtilUnittests._TEST_DIR)

    @unittest.skip('Skip to use real command to launch IDEA.')
    def test_run_intellij_sh_in_linux(self):
        """Follow the target behavior, with sh to show UI, else raise err."""
        sh_path = ide_util.IdeLinuxIntelliJ()._get_script_from_system()
        if sh_path:
            ide_util_obj = ide_util.IdeUtil()
            ide_util_obj.config_ide(IdeUtilUnittests._TEST_PRJ_PATH1)
            ide_util_obj.launch_ide()
        else:
            self.assertRaises(subprocess.CalledProcessError)

    @mock.patch.object(ide_util, '_get_linux_ide')
    @mock.patch.object(ide_util, '_get_mac_ide')
    def test_get_ide(self, mock_mac, mock_linux):
        """Test if _get_ide calls the correct respective functions."""
        ide_util._get_ide(None, 'j', False, is_mac=True)
        self.assertTrue(mock_mac.called)
        ide_util._get_ide(None, 'j', False, is_mac=False)
        self.assertTrue(mock_linux.called)

    @mock.patch.object(ide_util.IdeEclipse, '_get_script_from_system')
    @mock.patch.object(ide_util.IdeIntelliJ, '_get_preferred_version')
    def test_get_mac_and_linux_ide(self, mock_preference, mock_path):
        """Test if _get_mac_ide and _get_linux_ide return correct IDE class."""
        mock_preference.return_value = None
        mock_path.return_value = 'path'
        self.assertIsInstance(ide_util._get_mac_ide(), ide_util.IdeMacIntelliJ)
        self.assertIsInstance(ide_util._get_mac_ide(None, 's'),
                              ide_util.IdeMacStudio)
        self.assertIsInstance(ide_util._get_mac_ide(None, 'e'),
                              ide_util.IdeMacEclipse)
        self.assertIsInstance(ide_util._get_linux_ide(),
                              ide_util.IdeLinuxIntelliJ)
        self.assertIsInstance(
            ide_util._get_linux_ide(None, 's'), ide_util.IdeLinuxStudio)
        self.assertIsInstance(
            ide_util._get_linux_ide(None, 'e'), ide_util.IdeLinuxEclipse)

    @mock.patch.object(ide_util.IdeIntelliJ, '_set_installed_path')
    @mock.patch.object(ide_common_util, 'get_script_from_input_path')
    @mock.patch.object(ide_util.IdeIntelliJ, '_get_script_from_system')
    def test_init_ideintellij(self, mock_sys, mock_input, mock_set):
        """Test IdeIntelliJ's __init__ method."""
        ide_util.IdeLinuxIntelliJ()
        self.assertTrue(mock_sys.called)
        ide_util.IdeMacIntelliJ()
        self.assertTrue(mock_sys.called)
        ide_util.IdeLinuxIntelliJ('some_path')
        self.assertTrue(mock_input.called)
        self.assertTrue(mock_set.called)
        ide_util.IdeMacIntelliJ('some_path')
        self.assertTrue(mock_input.called)
        self.assertTrue(mock_set.called)

    @mock.patch.object(ide_util.IdeIntelliJ, '_get_preferred_version')
    @mock.patch.object(sdk_config.SDKConfig, '_android_sdk_exists')
    @mock.patch.object(sdk_config.SDKConfig, '_target_jdk_exists')
    @mock.patch.object(ide_util.IdeIntelliJ, '_get_config_root_paths')
    @mock.patch.object(ide_util.IdeBase, 'apply_optional_config')
    def test_config_ide(self, mock_config, mock_paths, mock_jdk, mock_sdk,
                        mock_preference):
        """Test IDEA, IdeUtil.config_ide won't call base none implement api."""
        # Mock SDkConfig flow to not to generate real jdk config file.
        mock_preference.return_value = None
        mock_jdk.return_value = True
        mock_sdk.return_value = True
        module_path = os.path.join(self._TEST_DIR, 'test')
        idea_path = os.path.join(module_path, '.idea')
        os.makedirs(idea_path)
        shutil.copy(IdeUtilUnittests._MODULE_XML_SAMPLE, idea_path)
        util_obj = ide_util.IdeUtil()
        util_obj.config_ide(module_path)
        self.assertFalse(mock_config.called)
        self.assertFalse(mock_paths.called)

    @mock.patch.object(ide_common_util, 'get_script_from_input_path')
    @mock.patch.object(ide_common_util, 'get_script_from_internal_path')
    def test_get_linux_config_1(self, mock_path, mock_path_2):
        """Test to get unique config path for linux IDEA case."""
        if (not android_dev_os.AndroidDevOS.MAC ==
                android_dev_os.AndroidDevOS.get_os_type()):
            mock_path.return_value = '/opt/intellij-ce-2018.3/bin/idea.sh'
            mock_path_2.return_value = '/opt/intellij-ce-2018.3/bin/idea.sh'
            ide_obj = ide_util.IdeLinuxIntelliJ('default_path')
            self.assertEqual(1, len(ide_obj._get_config_root_paths()))
        else:
            self.assertTrue((android_dev_os.AndroidDevOS.MAC ==
                             android_dev_os.AndroidDevOS.get_os_type()))

    @mock.patch('glob.glob')
    @mock.patch.object(ide_common_util, 'get_script_from_input_path')
    @mock.patch.object(ide_common_util, 'get_script_from_internal_path')
    def test_get_linux_config_2(self, mock_path, mock_path_2, mock_filter):
        """Test to get unique config path for linux IDEA case."""
        if (not android_dev_os.AndroidDevOS.MAC ==
                android_dev_os.AndroidDevOS.get_os_type()):
            mock_path.return_value = '/opt/intelliJ-ce-2018.3/bin/idea.sh'
            mock_path_2.return_value = '/opt/intelliJ-ce-2018.3/bin/idea.sh'
            ide_obj = ide_util.IdeLinuxIntelliJ()
            mock_filter.called = False
            ide_obj._get_config_root_paths()
            self.assertFalse(mock_filter.called)
        else:
            self.assertTrue((android_dev_os.AndroidDevOS.MAC ==
                             android_dev_os.AndroidDevOS.get_os_type()))

    def test_get_mac_config_root_paths(self):
        """Return None if there's no install path."""
        if (android_dev_os.AndroidDevOS.MAC ==
                android_dev_os.AndroidDevOS.get_os_type()):
            mac_ide = ide_util.IdeMacIntelliJ()
            mac_ide._installed_path = None
            self.assertIsNone(mac_ide._get_config_root_paths())
        else:
            self.assertFalse((android_dev_os.AndroidDevOS.MAC ==
                              android_dev_os.AndroidDevOS.get_os_type()))

    @mock.patch('glob.glob')
    @mock.patch.object(ide_common_util, 'get_script_from_input_path')
    @mock.patch.object(ide_common_util, 'get_script_from_internal_path')
    def test_get_linux_config_root(self, mock_path_1, mock_path_2, mock_filter):
        """Test to go filter logic for self download case."""
        mock_path_1.return_value = '/usr/tester/IDEA/IC2018.3.3/bin'
        mock_path_2.return_value = '/usr/tester/IDEA/IC2018.3.3/bin'
        ide_obj = ide_util.IdeLinuxIntelliJ()
        mock_filter.reset()
        ide_obj._get_config_root_paths()
        self.assertTrue(mock_filter.called)

    @mock.patch.object(sdk_config.SDKConfig, '__init__')
    @mock.patch.object(ide_util.IdeIntelliJ, '_get_config_root_paths')
    def test_apply_optional_config(self, mock_path, mock_conf):
        """Test basic logic of _apply_optional_config."""
        with mock.patch.object(ide_util, 'IdeIntelliJ') as obj:
            obj._installed_path = None
            obj.apply_optional_config()
            self.assertFalse(mock_path.called)

            obj.reset()
            obj._installed_path = 'default_path'
            mock_path.return_value = ['path1', 'path2']
            obj._IDE_JDK_TABLE_PATH = '/JDK_path'

            obj.apply_optional_config()
            self.assertTrue(mock_conf.called_with('path1/JDK_path'))
            self.assertTrue(mock_conf.called_with('path2/JDK_path'))

    @mock.patch('os.path.realpath')
    @mock.patch('os.path.isfile')
    def test_merge_symbolic_version(self, mock_isfile, mock_realpath):
        """Test _merge_symbolic_version and _get_real_path."""
        symbolic_path = ide_util.IdeIntelliJ._SYMBOLIC_VERSIONS[0]
        original_path = 'intellij-ce-2019.1/bin/idea.sh'
        mock_isfile.return_value = True
        mock_realpath.return_value = original_path
        ide_obj = ide_util.IdeLinuxIntelliJ('default_path')
        merged_version = ide_obj._merge_symbolic_version(
            [symbolic_path, original_path])
        self.assertEqual(
            merged_version[0], symbolic_path + ' -> ' + original_path)
        self.assertEqual(
            ide_obj._get_real_path(merged_version[0]), symbolic_path)

    @mock.patch('os.path.isfile')
    def test_get_application_path(self, mock_isfile):
        """Test _get_application_path."""
        ide_obj = ide_util.IdeLinuxIntelliJ('default_path')
        mock_isfile.return_value = True
        test_path = None
        self.assertEqual(None, ide_obj._get_application_path(test_path))

        test_path = 'a/b/c/d-e/f-gh/foo'
        self.assertEqual(None, ide_obj._get_application_path(test_path))

        test_path = 'a/b/c/d/intellij/foo'
        self.assertEqual(None, ide_obj._get_application_path(test_path))

        test_path = 'a/b/c/d/intellij-efg/foo'
        self.assertEqual(None, ide_obj._get_application_path(test_path))

        test_path = 'a/b/c/d/intellij-efg-hi/foo'
        self.assertEqual(None, ide_obj._get_application_path(test_path))

        test_path = 'a/b/c/d/intellij-ce-303/foo'
        self.assertEqual('.IdeaIC303', ide_obj._get_application_path(test_path))

        test_path = 'a/b/c/d/intellij-ue-303/foo'
        self.assertEqual('.IntelliJIdea303', ide_obj._get_application_path(
            test_path))

    def test_get_ide_util_instance_with_no_launch(self):
        """Test _get_ide_util_instance with no launch IDE."""
        args = aidegen_main._parse_args(['tradefed', '-n'])
        project_config.ProjectConfig(args)
        self.assertEqual(ide_util.get_ide_util_instance(args), None)

    @mock.patch.object(ide_util.IdeIntelliJ, '_get_preferred_version')
    def test_get_ide_util_instance_with_success(self, mock_preference):
        """Test _get_ide_util_instance with success."""
        args = aidegen_main._parse_args(['tradefed'])
        project_config.ProjectConfig(args)
        mock_preference.return_value = '1'
        self.assertIsInstance(
            ide_util.get_ide_util_instance(), ide_util.IdeUtil)

    @mock.patch.object(ide_util.IdeIntelliJ, '_get_preferred_version')
    @mock.patch.object(ide_util.IdeUtil, 'is_ide_installed')
    def test_get_ide_util_instance_with_failure(
            self, mock_installed, mock_preference):
        """Test _get_ide_util_instance with failure."""
        args = aidegen_main._parse_args(['tradefed'])
        project_config.ProjectConfig(args)
        mock_installed.return_value = False
        mock_preference.return_value = '1'
        with self.assertRaises(errors.IDENotExistError):
            ide_util.get_ide_util_instance()

    @mock.patch.object(ide_common_util, 'get_script_from_dir_path')
    @mock.patch.object(ide_common_util, '_run_ide_sh')
    @mock.patch('logging.info')
    def test_ide_base(self, mock_log, mock_run_ide, mock_run_path):
        """Test ide_base class."""
        # Test raise NotImplementedError.
        ide_base = ide_util.IdeBase()
        with self.assertRaises(NotImplementedError):
            ide_base._get_config_root_paths()

        # Test ide_name.
        ide_base._ide_name = 'a'
        self.assertEqual(ide_base.ide_name, 'a')

        # Test _get_ide_cmd.
        ide_base._installed_path = '/a/b'
        ide_base.project_abspath = '/x/y'
        expected_result = 'nohup /a/b /x/y 2>/dev/null >&2 &'
        self.assertEqual(ide_base._get_ide_cmd(), expected_result)

        # Test launch_ide.
        mock_run_ide.return_value = True
        ide_base.launch_ide()
        self.assertTrue(mock_log.called)

        # Test _get_ide_from_environment_paths.
        mock_run_path.return_value = '/a/b/idea.sh'
        ide_base._bin_file_name = 'idea.sh'
        expected_path = '/a/b/idea.sh'
        ide_path = ide_base._get_ide_from_environment_paths()
        self.assertEqual(ide_path, expected_path)

    def test_ide_intellij(self):
        """Test IdeIntelliJ class."""
        # Test raise NotImplementedError.
        ide_intellij = ide_util.IdeIntelliJ()
        with self.assertRaises(NotImplementedError):
            ide_intellij._get_config_root_paths()

    @mock.patch.object(ide_common_util, 'ask_preference')
    @mock.patch.object(config.AidegenConfig, 'deprecated_intellij_version')
    @mock.patch.object(ide_util.IdeIntelliJ, '_get_all_versions')
    def test_intellij_get_preferred_version(self,
                                            mock_all_versions,
                                            mock_deprecated_version,
                                            mock_ask_preference):
        """Test _get_preferred_version for IdeIntelliJ class."""
        ide_intellij = ide_util.IdeIntelliJ()

        # No IntelliJ version is installed.
        mock_all_versions.return_value = ['/a/b', '/a/c']
        mock_deprecated_version.return_value = True
        version = ide_intellij._get_preferred_version()
        self.assertEqual(version, None)

        # Load default preferred version.
        mock_all_versions.return_value = ['/a/b', '/a/c']
        mock_deprecated_version.return_value = False
        ide_intellij._config_reset = False
        expected_result = '/a/b'
        with mock.patch.object(config.AidegenConfig, 'preferred_version',
                               '/a/b'):
            version = ide_intellij._get_preferred_version()
            self.assertEqual(version, expected_result)

        # Asking user the preferred version.
        mock_all_versions.return_value = ['/a/b', '/a/c']
        mock_deprecated_version.return_value = False
        ide_intellij._config_reset = True
        mock_ask_preference.return_value = '/a/b'
        version = ide_intellij._get_preferred_version()
        expected_result = '/a/b'
        self.assertEqual(version, expected_result)

        mock_all_versions.return_value = ['/a/b', '/a/c']
        mock_ask_preference.return_value = None
        expected_result = '/a/b'
        with mock.patch.object(config.AidegenConfig, 'preferred_version',
                               '/a/b'):
            version = ide_intellij._get_preferred_version()
            self.assertEqual(version, expected_result)

        # The all_versions list has only one version.
        mock_all_versions.return_value = ['/a/b']
        mock_deprecated_version.return_value = False
        version = ide_intellij._get_preferred_version()
        self.assertEqual(version, '/a/b')

    @mock.patch.object(config.IdeaProperties, 'set_max_file_size')
    @mock.patch.object(sdk_config.SDKConfig, 'gen_enable_debugger_module')
    @mock.patch.object(sdk_config.SDKConfig, 'config_jdk_file')
    @mock.patch.object(ide_util.IdeStudio, '_get_config_root_paths')
    def test_android_studio_class(self, mock_get_config_paths, mock_config_file,
                                  mock_gen_debugger, mock_set_size):
        """Test IdeStudio."""
        mock_get_config_paths.return_value = ['path1', 'path2']
        mock_config_file.return_value = True
        mock_gen_debugger.return_value = True
        mock_set_size.return_value = True

        obj = ide_util.IdeStudio()
        obj._installed_path = False
        obj.apply_optional_config()
        self.assertEqual(obj.config_folders, [])

        obj._installed_path = '/'
        obj.apply_optional_config()
        expected_paths = ['path1', 'path2']
        self.assertEqual(obj.config_folders, expected_paths)

        mock_get_config_paths.return_value = []
        self.assertIsNone(obj.apply_optional_config())

    def test_studio_get_config_root_paths(self):
        """Test the method _get_config_root_paths of IdeStudio."""
        obj = ide_util.IdeStudio()
        with self.assertRaises(NotImplementedError):
            obj._get_config_root_paths()

    @mock.patch('os.getenv')
    def test_linux_android_studio_class(self, mock_get_home):
        """Test the method _get_config_root_paths of IdeLinuxStudio."""
        mock_get_home.return_value = self._TEST_DIR
        studio_config_dir1 = os.path.join(self._TEST_DIR, '.AndroidStudio3.0')
        studio_config_dir2 = os.path.join(self._TEST_DIR, '.AndroidStudio3.1')
        os.makedirs(studio_config_dir1)
        os.makedirs(studio_config_dir2)
        expected_result = [studio_config_dir1, studio_config_dir2]

        obj = ide_util.IdeLinuxStudio()
        config_paths = obj._get_config_root_paths()
        self.assertEqual(sorted(config_paths), sorted(expected_result))

    @mock.patch('os.getenv')
    def test_mac_android_studio_class(self, mock_get_home):
        """Test the method _get_config_root_paths of IdeMacStudio."""
        mock_get_home.return_value = self._TEST_DIR
        studio_config_dir1 = os.path.join(self._TEST_DIR, 'Library',
                                          'Preferences', 'AndroidStudio3.0')
        studio_config_dir2 = os.path.join(self._TEST_DIR, 'Library',
                                          'Preferences', 'AndroidStudio3.1')
        os.makedirs(studio_config_dir1)
        os.makedirs(studio_config_dir2)
        expected_result = [studio_config_dir1, studio_config_dir2]

        obj = ide_util.IdeMacStudio()
        config_paths = obj._get_config_root_paths()
        self.assertEqual(sorted(config_paths), sorted(expected_result))

    @mock.patch('os.access')
    @mock.patch('glob.glob')
    def test_eclipse_get_script_from_system(self, mock_glob, mock_file_access):
        """Test IdeEclipse _get_script_from_system method."""
        eclipse = ide_util.IdeEclipse()

        # Test no binary path in _get_script_from_system.
        eclipse._bin_paths = []
        expacted_result = None
        test_result = eclipse._get_script_from_system()
        self.assertEqual(test_result, expacted_result)

        # Test get the matched binary from _get_script_from_system.
        mock_glob.return_value = ['/a/b/eclipse']
        mock_file_access.return_value = True
        eclipse._bin_paths = ['/a/b/eclipse']
        expacted_result = '/a/b/eclipse'
        test_result = eclipse._get_script_from_system()
        self.assertEqual(test_result, expacted_result)

        # Test no matched binary from _get_script_from_system.
        mock_glob.return_value = []
        eclipse._bin_paths = ['/a/b/eclipse']
        expacted_result = None
        test_result = eclipse._get_script_from_system()
        self.assertEqual(test_result, expacted_result)

        # Test the matched binary cannot be executed.
        mock_glob.return_value = ['/a/b/eclipse']
        mock_file_access.return_value = False
        eclipse._bin_paths = ['/a/b/eclipse']
        expacted_result = None
        test_result = eclipse._get_script_from_system()
        self.assertEqual(test_result, expacted_result)

    @mock.patch('builtins.input')
    @mock.patch('os.path.exists')
    def test_eclipse_get_ide_cmd(self, mock_exists, mock_input):
        """Test IdeEclipse _get_ide_cmd method."""
        # Test open the IDE with the default Eclipse workspace.
        eclipse = ide_util.IdeEclipse()
        eclipse.cmd = ['eclipse']
        mock_exists.return_value = True
        expacted_result = ('eclipse -data '
                           '~/Documents/AIDEGen_Eclipse_workspace '
                           '2>/dev/null >&2 &')
        test_result = eclipse._get_ide_cmd()
        self.assertEqual(test_result, expacted_result)

        # Test running command without the default workspace.
        eclipse.cmd = ['eclipse']
        mock_exists.return_value = False
        mock_input.return_value = 'n'
        expacted_result = 'eclipse 2>/dev/null >&2 &'
        test_result = eclipse._get_ide_cmd()
        self.assertEqual(test_result, expacted_result)

    @mock.patch.object(ide_util.IdeUtil, 'is_ide_installed')
    @mock.patch.object(project_config.ProjectConfig, 'get_instance')
    def test_get_ide_util_instance(self, mock_config, mock_ide_installed):
        """Test get_ide_util_instance."""
        # Test is_launch_ide conditions.
        mock_instance = mock_config.return_value
        mock_instance.is_launch_ide = False
        ide_util.get_ide_util_instance()
        self.assertFalse(mock_ide_installed.called)
        mock_instance.is_launch_ide = True
        ide_util.get_ide_util_instance()
        self.assertTrue(mock_ide_installed.called)

        # Test ide is not installed.
        mock_ide_installed.return_value = False
        with self.assertRaises(errors.IDENotExistError):
            ide_util.get_ide_util_instance()


if __name__ == '__main__':
    unittest.main()
