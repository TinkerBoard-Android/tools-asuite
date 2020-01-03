#!/usr/bin/env python3
#
# Copyright 2020 - The Android Open Source Project
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
"""The iml/xml templates of AIDEgen."""

# Content of iml file.
FILE_IML = """<?xml version="1.0" encoding="UTF-8"?>
<module type="JAVA_MODULE" version="4">
@FACETS@
    <component name="NewModuleRootManager" inherit-compiler-output="true">
        <exclude-output />
@SOURCES@
@SRCJAR@
        <orderEntry type="sourceFolder" forTests="false" />
@MODULE_DEPENDENCIES@
        <orderEntry type="inheritedJdk" />
    </component>
</module>
"""

# The template content of modules.xml.
XML_MODULES = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="ProjectModuleManager">
        <modules>
@MODULES@
@ENABLE_DEBUGGER_MODULE@
        </modules>
    </component>
</project>
"""

# The template content of vcs.xml.
XML_VCS = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="VcsDirectoryMappings">
@VCS@
    </component>
</project>
"""

# The template content of misc.xml
XML_MISC = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="ConfigCheckProjectState">
        <option name="disabledCheckers">
            <list>
                <option value="com.google.devtools.intellig.configcheck.JavacHeapChecker"/>
                <option value="com.google.devtools.intellig.configcheck.VcsMappingsChecker"/>
            </list>
        </option>
    </component>
    <component name="ContinuousBuildConfigurationComponent">
        <builds>
            <build intervalToCheckBuild="1" buildKey="" buildLabel=""
                   enabled="false" tapBuild="false"/>
        </builds>
    </component>
    <component name="DependencyValidationManager">
        <option name="SKIP_IMPORT_STATEMENTS" value="false"/>
    </component>
    <component name="EntryPointsManager">
        <entry_points version="2.0"/>
    </component>
    <component name="JavadocGenerationManager">
        <option name="HEAP_SIZE"/>
        <option name="LOCALE"/>
        <option name="OPEN_IN_BROWSER" value="true"/>
        <option name="OPTION_DEPRECATED_LIST" value="true"/>
        <option name="OPTION_DOCUMENT_TAG_AUTHOR" value="false"/>
        <option name="OPTION_DOCUMENT_TAG_DEPRECATED" value="true"/>
        <option name="OPTION_DOCUMENT_TAG_USE" value="false"/>
        <option name="OPTION_DOCUMENT_TAG_VERSION" value="false"/>
        <option name="OPTION_HIERARCHY" value="true"/>
        <option name="OPTION_INDEX" value="true"/>
        <option name="OPTION_NAVIGATOR" value="true"/>
        <option name="OPTION_SCOPE" value="protected"/>
        <option name="OPTION_SEPARATE_INDEX" value="true"/>
        <option name="OTHER_OPTIONS" value=""/>
        <option name="OUTPUT_DIRECTORY"/>
    </component>
    <component name="Mach LOCAL_PREFIX stripper" stripping="true"/>
    <component name="ProjectResources">
        <default-html-doctype>http://www.w3.org/1999/xhtml
        </default-html-doctype>
    </component>
    <component name="ProjectRootManager" version="2" languageLevel="JDK_1_8"
               assert-keyword="true" project-jdk-name="JDK18"
               project-jdk-type="JavaSDK"/>
    <component name="WebServicesPlugin" addRequiredLibraries="true"/>
</project>

"""

# The template content of compiler.xml
XML_COMPILER = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="CompilerConfiguration">
        <option name="DEFAULT_COMPILER" value="Javac"/>
        <resourceExtensions/>
        <wildcardResourcePatterns>
            <entry name="?*.dtd"/>
            <entry name="?*.ftl"/>
            <entry name="?*.gif"/>
            <entry name="?*.html"/>
            <entry name="?*.jpeg"/>
            <entry name="?*.jpg"/>
            <entry name="?*.png"/>
            <entry name="?*.properties"/>
            <entry name="?*.tld"/>
            <entry name="?*.xml"/>
        </wildcardResourcePatterns>
        <annotationProcessing enabled="false" useClasspath="true"/>
    </component>
    <component name="JavacSettings">
        <option name="MAXIMUM_HEAP_SIZE" value="1024"/>
    </component>
</project>
"""

# The template content of codeStyleConfig.xml
XML_CODE_STYLE_CONFIG = """<component name="ProjectCodeStyleConfiguration">
  <state>
    <option name="USE_PER_PROJECT_SETTINGS" value="true" />
  </state>
</component>
"""

# The template content of Apache_2.xml
XML_APACHE_2 = """<component name="CopyrightManager">
    <copyright>
        <option name="notice"
                value="Copyright (C) &amp;#36;today.year The Android Open Source Project&#10;&#10;Licensed under the Apache License, Version 2.0 (the &quot;License&quot;);&#10;you may not use this file except in compliance with the License.&#10;You may obtain a copy of the License at&#10;&#10;     http://www.apache.org/licenses/LICENSE-2.0&#10;&#10;Unless required by applicable law or agreed to in writing, software&#10;distributed under the License is distributed on an &quot;AS IS&quot; BASIS,&#10;WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.&#10;See the License for the specific language governing permissions and&#10;limitations under the License."/>
        <option name="keyword" value="Copyright"/>
        <option name="allowReplaceKeyword" value=""/>
        <option name="myName" value="Apache 2"/>
        <option name="myLocal" value="true"/>
    </copyright>
</component>
"""

# The template content of profiles_settings.xml
XML_PROFILES_SETTINGS = """<component name="CopyrightManager">
    <settings default="">
        <module2copyright>
            <element module="Project Files" copyright="Apache 2"/>
        </module2copyright>
    </settings>
</component>
"""

# The configuration of JDK on Linux.
LINUX_JDK_XML = """    <jdk version="2">
      <name value="JDK18" />
      <type value="JavaSDK" />
      <version value="java version &quot;1.8.0_152&quot;" />
      <homePath value="{JDKpath}" />
      <roots>
        <annotationsPath>
          <root type="composite">
            <root url="jar://$APPLICATION_HOME_DIR$/lib/jdkAnnotations.jar!/" type="simple" />
          </root>
        </annotationsPath>
        <classPath>
          <root type="composite">
            <root url="jar://{JDKpath}/jre/lib/charsets.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/cldrdata.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/dnsns.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/jaccess.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/localedata.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/nashorn.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/sunec.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/sunjce_provider.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/sunpkcs11.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/zipfs.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/jce.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/jsse.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/management-agent.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/resources.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/rt.jar!/" type="simple" />
          </root>
        </classPath>
        <javadocPath>
          <root type="composite" />
        </javadocPath>
        <sourcePath>
          <root type="composite">
            <root url="jar://{JDKpath}/src.zip!/" type="simple" />
          </root>
        </sourcePath>
      </roots>
      <additional />
    </jdk>
"""

# The configuration of JDK on Mac.
MAC_JDK_XML = """    <jdk version="2">
      <name value="JDK18" />
      <type value="JavaSDK" />
      <version value="java version &quot;1.8.0_152&quot;" />
      <homePath value="{JDKpath}" />
      <roots>
        <annotationsPath>
          <root type="composite">
            <root url="jar://$APPLICATION_HOME_DIR$/lib/jdkAnnotations.jar!/" type="simple" />
          </root>
        </annotationsPath>
        <classPath>
          <root type="composite">
            <root url="jar://{JDKpath}/jre/lib/charsets.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/cldrdata.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/dnsns.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/jaccess.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/localedata.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/nashorn.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/sunec.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/sunjce_provider.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/sunpkcs11.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/ext/zipfs.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/jce.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/jsse.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/management-agent.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/resources.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/rt.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/management-agent.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/resources.jar!/" type="simple" />
            <root url="jar://{JDKpath}/jre/lib/rt.jar!/" type="simple" />
            <root url="jar://{JDKpath}/lib/dt.jar!/" type="simple" />
            <root url="jar://{JDKpath}/lib/jconsole.jar!/" type="simple" />
            <root url="jar://{JDKpath}/lib/sa-jdi.jar!/" type="simple" />
            <root url="jar://{JDKpath}/lib/tools.jar!/" type="simple" />
          </root>
        </classPath>
        <javadocPath>
          <root type="composite" />
        </javadocPath>
        <sourcePath>
          <root type="composite">
            <root url="jar://{JDKpath}/src.zip!/" type="simple" />
          </root>
        </sourcePath>
      </roots>
      <additional />
    </jdk>
"""

# The file's header of CLion project file.
CMAKELISTS_HEADER = """# THIS FILE WAS AUTOMATICALLY GENERATED!
# ANY MODIFICATION WILL BE OVERWRITTEN!

# To improve project view in Clion    :
# Tools > CMake > Change Project Root

cmake_minimum_required(VERSION @MINVERSION@)
project(@PROJNAME@)
set(ANDROID_ROOT @ANDROIDROOT@)

"""
