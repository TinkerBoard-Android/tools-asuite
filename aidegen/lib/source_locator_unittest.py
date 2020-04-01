#!/usr/bin/env python3
#
# Copyright 2018, The Android Open Source Project
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

"""Unittests for module_data."""

import os
import unittest
from unittest import mock

from aidegen import unittest_constants

from aidegen.lib import module_info
from aidegen.lib import source_locator


# pylint: disable=too-many-arguments
# pylint: disable=protected-access
# pylint: disable=invalid-name
class ModuleDataUnittests(unittest.TestCase):
    """Unit tests for module_data.py"""

    @mock.patch('aidegen.lib.common_util.get_android_root_dir')
    def test_collect_srcs_paths(self, mock_android_root_dir):
        """Test _collect_srcs_paths create the source path list."""
        result_source = set(['packages/apps/test/src/main/java'])
        result_test = set(['packages/apps/test/tests'])
        mock_android_root_dir.return_value = unittest_constants.TEST_DATA_PATH
        module_data = source_locator.ModuleData(
            unittest_constants.TEST_MODULE, unittest_constants.MODULE_INFO, 0)
        module_data._collect_srcs_paths()
        self.assertEqual(module_data.src_dirs, result_source)
        self.assertEqual(module_data.test_dirs, result_test)

    def test_get_package_name(self):
        """test get the package name from a java file."""
        result_package_name = 'com.android'
        test_java = os.path.join(unittest_constants.TEST_DATA_PATH,
                                 unittest_constants.MODULE_PATH,
                                 'src/main/java/com/android/java.java')
        package_name = source_locator.ModuleData._get_package_name(test_java)
        self.assertEqual(package_name, result_package_name)

        # Test on java file with no package name.
        result_package_name = None
        test_java = os.path.join(unittest_constants.TEST_DATA_PATH,
                                 unittest_constants.MODULE_PATH,
                                 'src/main/java/com/android/no_package.java')
        package_name = source_locator.ModuleData._get_package_name(test_java)
        self.assertEqual(package_name, result_package_name)

    @mock.patch('aidegen.lib.common_util.get_android_root_dir')
    def test_get_source_folder(self, mock_android_root_dir):
        """Test _get_source_folder process."""
        # Test for getting the source path by parse package name from a java.
        test_java = 'packages/apps/test/src/main/java/com/android/java.java'
        result_source = 'packages/apps/test/src/main/java'
        mock_android_root_dir.return_value = unittest_constants.TEST_DATA_PATH
        module_data = source_locator.ModuleData(
            unittest_constants.TEST_MODULE, unittest_constants.MODULE_INFO, 0)
        src_path = module_data._get_source_folder(test_java)
        self.assertEqual(src_path, result_source)

        # Return path is None if the java file doesn't exist.
        test_java = 'file_not_exist.java'
        src_path = module_data._get_source_folder(test_java)
        self.assertEqual(src_path, None)

        # Return path is None on the java file without package name.
        test_java = ('packages/apps/test/src/main/java/com/android/'
                     'no_package.java')
        src_path = module_data._get_source_folder(test_java)
        self.assertEqual(src_path, None)

    def test_get_r_dir(self):
        """Test get_r_dir."""
        module_data = source_locator.ModuleData(
            unittest_constants.TEST_MODULE, unittest_constants.MODULE_INFO, 0)
        # Test for aapt2.srcjar
        test_aapt2_srcjar = 'a/aapt2.srcjar'
        expect_result = 'a/aapt2'
        r_dir = module_data._get_r_dir(test_aapt2_srcjar)
        self.assertEqual(r_dir, expect_result)

        # Test for R.srcjar
        test_r_jar = 'b/android/R.srcjar'
        expect_result = 'b/aapt2/R'
        r_dir = module_data._get_r_dir(test_r_jar)
        self.assertEqual(r_dir, expect_result)

        # Test the R.srcjar is not under the android folder.
        test_wrong_r_jar = 'b/test/R.srcjar'
        expect_result = None
        r_dir = module_data._get_r_dir(test_wrong_r_jar)
        self.assertEqual(r_dir, expect_result)

        # Test for the target file is not aapt2.srcjar or R.srcjar
        test_unknown_target = 'c/proto.srcjar'
        expect_result = None
        r_dir = module_data._get_r_dir(test_unknown_target)
        self.assertEqual(r_dir, expect_result)

    @mock.patch('os.path.exists')
    @mock.patch('aidegen.lib.common_util.get_android_root_dir')
    def test_collect_r_src_path(self, mock_android_root_dir, mock_exists):
        """Test collect_r_src_path."""
        mock_exists.return_value = True
        # Test on target srcjar exists in srcjars.
        test_module = dict(unittest_constants.MODULE_INFO)
        test_module['srcs'] = []
        mock_android_root_dir.return_value = unittest_constants.TEST_DATA_PATH
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                test_module, 0)
        # Test the module is not APPS.
        module_data._collect_r_srcs_paths()
        expect_result = set()
        self.assertEqual(module_data.r_java_paths, expect_result)

        # Test the module is not a target module.
        test_module['depth'] = 1
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                test_module, 1)
        module_data._collect_r_srcs_paths()
        expect_result = set()
        self.assertEqual(module_data.r_java_paths, expect_result)

        # Test the srcjar target doesn't exist.
        test_module['class'] = ['APPS']
        test_module['srcjars'] = []
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                test_module, 0)
        module_data._collect_r_srcs_paths()
        expect_result = set()
        self.assertEqual(module_data.r_java_paths, expect_result)

        # Test the srcjar target exists.
        test_module['srcjars'] = [('out/soong/.intermediates/packages/apps/'
                                   'test_aapt2/aapt2.srcjar')]
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                test_module, 0)
        module_data._collect_r_srcs_paths()
        expect_result = {
            'out/soong/.intermediates/packages/apps/test_aapt2/aapt2'
        }
        self.assertEqual(module_data.r_java_paths, expect_result)
        mock_exists.return_value = False
        module_data._collect_r_srcs_paths()
        expect_result = {('out/soong/.intermediates/packages/apps/test_aapt2/'
                          'aapt2.srcjar')}
        self.assertEqual(module_data.build_targets, expect_result)


    def test_parse_source_path(self):
        """Test _parse_source_path."""
        # The package name of e.java is c.d.
        test_java = 'a/b/c/d/e.java'
        package_name = 'c.d'
        expect_result = 'a/b'
        src_path = source_locator.ModuleData._parse_source_path(
            test_java, package_name)
        self.assertEqual(src_path, expect_result)

        # The package name of e.java is c.d.
        test_java = 'a/b/c.d/e.java'
        package_name = 'c.d'
        expect_result = 'a/b'
        src_path = source_locator.ModuleData._parse_source_path(
            test_java, package_name)
        self.assertEqual(src_path, expect_result)

        # The package name of e.java is x.y.
        test_java = 'a/b/c/d/e.java'
        package_name = 'x.y'
        expect_result = 'a/b/c/d'
        src_path = source_locator.ModuleData._parse_source_path(
            test_java, package_name)
        self.assertEqual(src_path, expect_result)

        # The package name of f.java is c.d.
        test_java = 'a/b/c.d/e/c/d/f.java'
        package_name = 'c.d'
        expect_result = 'a/b/c.d/e'
        src_path = source_locator.ModuleData._parse_source_path(
            test_java, package_name)
        self.assertEqual(src_path, expect_result)

        # The package name of f.java is c.d.e.
        test_java = 'a/b/c.d/e/c.d/e/f.java'
        package_name = 'c.d.e'
        expect_result = 'a/b/c.d/e'
        src_path = source_locator.ModuleData._parse_source_path(
            test_java, package_name)
        self.assertEqual(src_path, expect_result)

    @mock.patch('aidegen.lib.common_util.get_android_root_dir')
    def test_append_jar_file(self, mock_android_root_dir):
        """Test _append_jar_file process."""
        # Append an existing jar file path to module_data.jar_files.
        test_jar_file = os.path.join(unittest_constants.MODULE_PATH, 'test.jar')
        result_jar_list = set([test_jar_file])
        mock_android_root_dir.return_value = unittest_constants.TEST_DATA_PATH
        module_data = source_locator.ModuleData(
            unittest_constants.TEST_MODULE, unittest_constants.MODULE_INFO, 0)
        module_data._append_jar_file(test_jar_file)
        self.assertEqual(module_data.jar_files, result_jar_list)

        # Skip if the jar file doesn't exist.
        test_jar_file = os.path.join(unittest_constants.MODULE_PATH,
                                     'jar_not_exist.jar')
        module_data.jar_files = set()
        module_data._append_jar_file(test_jar_file)
        self.assertEqual(module_data.jar_files, set())

        # Skip if it's not a jar file.
        test_jar_file = os.path.join(unittest_constants.MODULE_PATH,
                                     'test.java')
        module_data.jar_files = set()
        module_data._append_jar_file(test_jar_file)
        self.assertEqual(module_data.jar_files, set())

    @mock.patch('aidegen.lib.common_util.get_android_root_dir')
    def test_append_jar_from_installed(self, mock_android_root_dir):
        """Test _append_jar_from_installed handling."""
        # Test appends the first jar file of 'installed'.
        mod_info = dict(unittest_constants.MODULE_INFO)
        mod_info['installed'] = [
            os.path.join(unittest_constants.MODULE_PATH, 'test.aar'),
            os.path.join(unittest_constants.MODULE_PATH, 'test.jar'),
            os.path.join(unittest_constants.MODULE_PATH,
                         'tests/test_second.jar')
        ]
        result_jar_list = set(
            [os.path.join(unittest_constants.MODULE_PATH, 'test.jar')])
        mock_android_root_dir.return_value = unittest_constants.TEST_DATA_PATH
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                mod_info, 0)
        module_data._append_jar_from_installed()
        self.assertEqual(module_data.jar_files, result_jar_list)

        # Test on the jar file path matches the path prefix.
        module_data.jar_files = set()
        result_jar_list = set([
            os.path.join(unittest_constants.MODULE_PATH,
                         'tests/test_second.jar')
        ])
        module_data._append_jar_from_installed(
            os.path.join(unittest_constants.MODULE_PATH, 'tests/'))
        self.assertEqual(module_data.jar_files, result_jar_list)

    @mock.patch('aidegen.lib.common_util.get_android_root_dir')
    def test_set_jars_jarfile(self, mock_android_root_dir):
        """Test _set_jars_jarfile handling."""
        # Combine the module path with jar file name in 'jars' and then append
        # it to module_data.jar_files.
        mod_info = dict(unittest_constants.MODULE_INFO)
        mod_info['jars'] = [
            'test.jar',
            'src/test.jar',  # This jar file doesn't exist.
            'tests/test_second.jar'
        ]
        result_jar_list = set([
            os.path.join(unittest_constants.MODULE_PATH, 'test.jar'),
            os.path.join(unittest_constants.MODULE_PATH,
                         'tests/test_second.jar')
        ])
        result_missing_jars = set()
        mock_android_root_dir.return_value = unittest_constants.TEST_DATA_PATH
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                mod_info, 0)
        module_data._set_jars_jarfile()
        self.assertEqual(module_data.jar_files, result_jar_list)
        self.assertEqual(module_data.missing_jars, result_missing_jars)

    @mock.patch('aidegen.lib.common_util.get_android_root_dir')
    def test_locate_sources_path(self, mock_android_root_dir):
        """Test locate_sources_path handling."""
        # Test collect source path.
        mod_info = dict(unittest_constants.MODULE_INFO)
        result_src_list = set(['packages/apps/test/src/main/java'])
        result_test_list = set(['packages/apps/test/tests'])
        result_jar_list = set()
        result_r_path = set()
        mock_android_root_dir.return_value = unittest_constants.TEST_DATA_PATH
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                mod_info, 0)
        module_data.locate_sources_path()
        self.assertEqual(module_data.src_dirs, result_src_list)
        self.assertEqual(module_data.test_dirs, result_test_list)
        self.assertEqual(module_data.jar_files, result_jar_list)
        self.assertEqual(module_data.r_java_paths, result_r_path)

        # Test find jar files.
        jar_file = ('out/soong/.intermediates/packages/apps/test/test/'
                    'android_common/test.jar')
        mod_info['jarjar_rules'] = ['jarjar-rules.txt']
        mod_info['installed'] = [jar_file]
        result_jar_list = set([jar_file])
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                mod_info, 0)
        module_data.locate_sources_path()
        self.assertEqual(module_data.jar_files, result_jar_list)

    @mock.patch('aidegen.lib.common_util.get_android_root_dir')
    def test_collect_jar_by_depth_value(self, mock_android_root_dir):
        """Test parameter --depth handling."""
        # Test find jar by module's depth greater than the --depth value from
        # command line.
        depth_by_source = 2
        mod_info = dict(unittest_constants.MODULE_INFO)
        mod_info['depth'] = 3
        mod_info['installed'] = [
            ('out/soong/.intermediates/packages/apps/test/test/android_common/'
             'test.jar')
        ]
        result_src_list = set()
        result_jar_list = set(
            [('out/soong/.intermediates/packages/apps/test/test/'
              'android_common/test.jar')])
        mock_android_root_dir.return_value = unittest_constants.TEST_DATA_PATH
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                mod_info, depth_by_source)
        module_data.locate_sources_path()
        self.assertEqual(module_data.src_dirs, result_src_list)
        self.assertEqual(module_data.jar_files, result_jar_list)

        # Test find source folder when module's depth equal to the --depth value
        # from command line.
        depth_by_source = 2
        mod_info = dict(unittest_constants.MODULE_INFO)
        mod_info['depth'] = 2
        result_src_list = set(['packages/apps/test/src/main/java'])
        result_test_list = set(['packages/apps/test/tests'])
        result_jar_list = set()
        result_r_path = set()
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                mod_info, depth_by_source)
        module_data.locate_sources_path()
        self.assertEqual(module_data.src_dirs, result_src_list)
        self.assertEqual(module_data.test_dirs, result_test_list)
        self.assertEqual(module_data.jar_files, result_jar_list)
        self.assertEqual(module_data.r_java_paths, result_r_path)

        # Test find source folder when module's depth smaller than the --depth
        # value from command line.
        depth_by_source = 3
        mod_info = dict(unittest_constants.MODULE_INFO)
        mod_info['depth'] = 2
        result_src_list = set(['packages/apps/test/src/main/java'])
        result_test_list = set(['packages/apps/test/tests'])
        result_jar_list = set()
        result_r_path = set()
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                mod_info, depth_by_source)
        module_data.locate_sources_path()
        self.assertEqual(module_data.src_dirs, result_src_list)
        self.assertEqual(module_data.test_dirs, result_test_list)
        self.assertEqual(module_data.jar_files, result_jar_list)
        self.assertEqual(module_data.r_java_paths, result_r_path)

    def test_collect_srcjar_path(self):
        """Test collect srcjar path."""
        srcjar_path = 'a/b/aapt2.srcjar'
        test_module = dict(unittest_constants.MODULE_INFO)
        test_module['srcjars'] = [srcjar_path]
        expacted_result = set(['%s!/' % srcjar_path])
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                test_module, 0)
        module_data._collect_srcjar_path('R.java')
        self.assertEqual(module_data.srcjar_paths, set())
        module_data._collect_srcjar_path(srcjar_path)
        self.assertEqual(module_data.srcjar_paths, expacted_result)

    def test_collect_all_srcjar_path(self):
        """Test collect all srcjar paths as source root folders."""
        test_module = dict(unittest_constants.MODULE_INFO)
        test_module['srcjars'] = [
            'a/b/aidl0.srcjar',
            'a/b/aidl1.srcjar'
        ]
        expacted_result = set([
            'a/b/aidl0.srcjar!/',
            'a/b/aidl1.srcjar!/'
        ])
        module_data = source_locator.ModuleData(unittest_constants.TEST_MODULE,
                                                test_module, 0)
        module_data._collect_all_srcjar_paths()
        self.assertEqual(module_data.srcjar_paths, expacted_result)

    def test_collect_missing_jars(self):
        """Test _collect_missing_jars."""
        mod_name = 'test'
        mod_info = {'name': 'test'}
        test_path = 'a/b/c'
        mod_data = source_locator.EclipseModuleData(mod_name, mod_info,
                                                    test_path)
        mod_data.missing_jars = set('a')
        mod_data.referenced_by_jar = False
        mod_data._collect_missing_jars()
        self.assertEqual(mod_data.build_targets, set())
        mod_data.referenced_by_jar = True
        mod_data._collect_missing_jars()
        self.assertEqual(mod_data.build_targets, {'a'})


class EclipseModuleDataUnittests(unittest.TestCase):
    """Unit tests for the EclipseModuleData in module_data.py"""

    @mock.patch.object(module_info.AidegenModuleInfo,
                       'is_project_path_relative_module')
    @mock.patch.object(source_locator.ModuleData, '__init__')
    def test___init__(self, mock_base_init, mock_method):
        """Test the implement of __init__()."""
        mod_name = 'test'
        mod_info = {'name': 'test'}
        test_path = 'a/b/c'
        source_locator.EclipseModuleData(mod_name, mod_info, test_path)
        self.assertTrue(mock_base_init.called)
        self.assertTrue(mock_method.called)

    @mock.patch.object(source_locator.ModuleData, '_collect_missing_jars')
    @mock.patch.object(source_locator.ModuleData, '_collect_classes_jars')
    @mock.patch.object(source_locator.EclipseModuleData, '_locate_jar_path')
    @mock.patch.object(source_locator.EclipseModuleData,
                       '_locate_project_source_path')
    def test_locate_sources_path(self, mock_src, mock_jar, mock_class_jar,
                                 mock_missing_jar):
        """Test locate_sources_path."""
        mod_name = 'test'
        mod_info = {'name': 'test'}
        test_path = 'a/b/c'
        mod_data = source_locator.EclipseModuleData(mod_name, mod_info,
                                                    test_path)
        mod_data.is_project = True
        mod_data.locate_sources_path()
        self.assertTrue(mock_src.called)
        self.assertTrue(mock_class_jar.called)
        self.assertTrue(mock_missing_jar.called)

        mock_src.reset()
        mock_jar.reset()
        mod_data.is_project = False
        mod_data.locate_sources_path()
        self.assertTrue(mock_jar.called)

    @mock.patch.object(source_locator.ModuleData, '_collect_srcs_paths')
    @mock.patch.object(source_locator.ModuleData, '_collect_r_srcs_paths')
    def test_locate_project_source_path(self, mock_src, mock_r):
        """Test _locate_project_source_path."""
        mod_name = 'test'
        mod_info = {'name': 'test'}
        test_path = 'a/b/c'
        mod_data = source_locator.EclipseModuleData(mod_name, mod_info,
                                                    test_path)
        mod_data._locate_project_source_path()
        self.assertTrue(mock_src.called)
        self.assertTrue(mock_r.called)

    @mock.patch.object(source_locator.ModuleData, '_append_classes_jar')
    @mock.patch.object(source_locator.ModuleData, '_check_key')
    @mock.patch.object(source_locator.ModuleData, '_set_jars_jarfile')
    @mock.patch.object(source_locator.ModuleData, '_check_jars_exist')
    @mock.patch.object(source_locator.ModuleData, '_append_jar_from_installed')
    @mock.patch.object(source_locator.ModuleData, '_check_jarjar_rules_exist')
    def test_locate_jar_path(self, mock_jarjar, mock_append_jar, mock_check_jar,
                             mock_set_jar, mock_check_key, mock_append_class):
        """Test _locate_jar_path."""
        mod_name = 'test'
        mod_info = {'name': 'test', 'path': 'x/y'}
        test_path = 'a/b/c'
        mod_data = source_locator.EclipseModuleData(mod_name, mod_info,
                                                    test_path)
        mock_jarjar.return_value = False
        mock_check_jar.return_value = False
        mock_check_key.return_value = False
        mod_data._locate_jar_path()
        self.assertTrue(mock_append_jar.called)
        self.assertFalse(mock_set_jar.called)
        self.assertFalse(mock_append_class.called)

        mock_append_jar.reset_mock()
        mock_jarjar.return_value = False
        mock_check_jar.return_value = False
        mock_check_key.return_value = True
        mod_data._locate_jar_path()
        self.assertFalse(mock_append_jar.called)
        self.assertFalse(mock_set_jar.called)
        self.assertTrue(mock_append_class.called)

        mock_check_key.reset_mock()
        mock_append_class.reset_mock()
        mock_append_jar.reset_mock()
        mock_jarjar.return_value = False
        mock_check_jar.return_value = True
        mod_data._locate_jar_path()
        self.assertFalse(mock_append_jar.called)
        self.assertTrue(mock_set_jar.called)
        self.assertFalse(mock_check_key.called)
        self.assertFalse(mock_append_class.called)

        mock_append_jar.reset_mock()
        mock_set_jar.reset_mock()
        mock_check_jar.reset_mock()
        mock_check_key.reset_mock()
        mock_append_class.reset_mock()

        mock_jarjar.return_value = True
        mod_data._locate_jar_path()
        self.assertTrue(mock_append_jar.called)
        self.assertFalse(mock_check_jar.called)
        self.assertFalse(mock_set_jar.called)
        self.assertFalse(mock_check_key.called)
        self.assertFalse(mock_append_class.called)

    def test_add_to_source_or_test_dirs(self):
        """Test _add_to_source_or_test_dirs."""
        mod_name = 'test'
        mod_info = {'name': 'test'}
        test_path = 'a/b/c'
        mod_data = source_locator.EclipseModuleData(mod_name, mod_info,
                                                    test_path)
        mod_data._add_to_source_or_test_dirs('libcore/ojluni/src/lambda/java')
        self.assertEqual(mod_data.src_dirs, set())
        mod_data._add_to_source_or_test_dirs('a')
        self.assertEqual(mod_data.src_dirs, {'a'})


if __name__ == '__main__':
    unittest.main()
