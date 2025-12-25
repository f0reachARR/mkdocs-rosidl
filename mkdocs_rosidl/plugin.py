# Copyright 2024 mkdocs-rosidl contributors
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

"""MkDocs plugin for ROS2 interface documentation generation."""

import os
import shutil
import time
from pathlib import Path

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from rosidl_runtime_py import get_action_interfaces, get_message_interfaces, get_service_interfaces

from mkdocs_rosidl import action_utils, msg_utils, srv_utils, utils


class RosidlPlugin(BasePlugin):
    """MkDocs plugin for generating ROS2 interface documentation."""

    config_scheme = (
        ('packages', config_options.Type(list, default=[])),
        ('output_dir', config_options.Type(str, default='interfaces')),
    )

    def on_pre_build(self, config):
        """
        Generate interface documentation before the build.

        :param config: MkDocs configuration
        """
        packages_select = self.config.get('packages', [])
        output_dir = self.config.get('output_dir', 'interfaces')
        
        # Get the docs directory from MkDocs config
        docs_dir = config['docs_dir']
        interface_dir = os.path.join(docs_dir, output_dir)
        
        # Create output directory
        os.makedirs(interface_dir, exist_ok=True)
        
        try:
            # Get all interfaces
            messages = get_message_interfaces(packages_select)
            services = get_service_interfaces(packages_select)
            actions = get_action_interfaces(packages_select)
        except LookupError as e:
            print(f'Error getting interfaces: {e}')
            return
        
        timestamp = time.gmtime()
        
        # Generate documentation for each package
        self._generate_interfaces_index(messages, services, actions, interface_dir, timestamp)
        
        # Generate interface documentation
        self._generate_interfaces(messages, interface_dir, 'msg', timestamp)
        self._generate_interfaces(services, interface_dir, 'srv', timestamp)
        self._generate_interfaces(actions, interface_dir, 'action', timestamp)
        
        # Copy CSS files
        self._copy_css_style(interface_dir)

    def _generate_interfaces_index(self, messages, services, actions, output_dir, timestamp):
        """
        Generate index for packages.

        :param messages: Message package name as key and list of message names as value
        :param services: Service package name as key and list of service names as value
        :param actions: Action package name as key and list of action names as value
        :param output_dir: path to the directory to save the index
        :param timestamp: timestamp to include in the index site
        """
        interface_packages = messages.keys() | services.keys() | actions.keys()
        
        env = utils.load_jinja_env()
        template = env.get_template('index.html.jinja2')
        
        for package_name in interface_packages:
            msg_list = messages.get(package_name, [])
            srv_list = services.get(package_name, [])
            action_list = actions.get(package_name, [])
            
            package_directory = os.path.join(output_dir, package_name)
            os.makedirs(package_directory, exist_ok=True)
            
            # Generate package index
            context = {
                'package': package_name,
                'timestamp': time.strftime("%b %d %Y %H:%M:%S", timestamp),
                'msg_list': msg_list,
                'srv_list': srv_list,
                'action_list': action_list,
                'msg_relative_paths': [f'{package_name}/{msg}.html' for msg in msg_list],
                'srv_relative_paths': [f'{package_name}/{srv}.html' for srv in srv_list],
                'action_relative_paths': [f'{package_name}/{action}.html' for action in action_list],
            }
            
            output_file = os.path.join(package_directory, 'index.md')
            with open(output_file, 'w') as f:
                f.write(template.render(context))

    def _generate_interfaces(self, interfaces, output_dir, interface_type, timestamp):
        """
        Generate documentation for each interface.

        :param interfaces: dictionary with the interface package name associated with all interfaces
        :param output_dir: path to the directory to save the generated documentation
        :param interface_type: type of the interface: msg, action or srv
        :param timestamp: timestamp to include in the documentation
        """
        env = utils.load_jinja_env()
        
        # Select the appropriate template and function
        if interface_type == 'msg':
            template = env.get_template('msg.html.jinja2')
            ext = 'msg'
            type_name = 'Message'
            generate_func = msg_utils.generate_msg_text_from_spec
        elif interface_type == 'srv':
            template = env.get_template('srv.html.jinja2')
            ext = 'srv'
            type_name = 'Service'
            generate_func = srv_utils.generate_msg_text_from_spec
        elif interface_type == 'action':
            template = env.get_template('action.html.jinja2')
            ext = 'action'
            type_name = 'Action'
            generate_func = action_utils.generate_msg_text_from_spec
        else:
            return
        
        for package_name, interface_names in interfaces.items():
            package_directory = os.path.join(output_dir, package_name)
            os.makedirs(package_directory, exist_ok=True)
            
            for interface_name in interface_names:
                # Get the interface file path
                from rosidl_runtime_py import get_interface_path
                interface = f'{package_name}/{interface_type}/{interface_name}'
                
                try:
                    file_path = get_interface_path(interface)
                    with open(file_path, 'r', encoding='utf-8') as h:
                        raw_text = h.read().rstrip()
                except Exception as e:
                    print(f'Error reading interface {interface}: {e}')
                    continue
                
                # Generate compact definition
                try:
                    compact_definition = generate_func(package_name, interface_name)
                except Exception as e:
                    print(f'Error generating compact definition for {interface}: {e}')
                    continue
                
                # Prepare context
                context = {
                    'interface_name': interface_name,
                    'interface_package': package_name,
                    'timestamp': time.strftime("%b %d %Y %H:%M:%S", timestamp),
                    'raw_text': raw_text,
                    'ext': ext,
                    'type': type_name,
                    **compact_definition
                }
                
                # Write output file
                output_file = os.path.join(package_directory, f'{interface_name}.md')
                with open(output_file, 'w') as f:
                    f.write(template.render(context))

    def _copy_css_style(self, folder_name):
        """
        Copy the CSS style files to the folder.

        :param folder_name: name of the folder where the style CSS files will be copied
        """
        template_dir = utils.get_templates_dir()
        for style in ['styles.css', 'msg-styles.css']:
            src = os.path.join(template_dir, style)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(folder_name, style))
