# Copyright 2024 mkdocs-rosidl contributors
# Copyright 2020 Open Source Robotics Foundation, Inc.
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

"""Utility functions for ROS2 interface documentation generation."""

import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from rosidl_parser.definition import (
    AbstractGenericString, AbstractString, Array, BasicType, BoundedSequence,
    BoundedString, NamespacedType, UnboundedSequence
)
from rosidl_runtime_py import get_interface_path

# Magic field name that should be skipped in documentation
SKIP_FIELD_NAME = 'structure_needs_at_least_one_member'


def resource_name(resource):
    """
    Return the resource name.

    :param resource: resource name of the interface
    :type resource: str
    :returns: a tuple with the 3 parts of the resource name 
              (e.g., std_msgs/msg/Bool -> ('std_msgs', 'msg', 'Bool'))
    :rtype: tuple
    """
    if '/' not in resource:
        return '', '', resource
    values = resource.split('/')
    if len(values) != 3:
        raise ValueError('Resource name "{}" is malformed'.format(resource))
    return tuple(values)


def get_templates_dir():
    """
    Return template directory.

    :returns: the directory of the template directory
    :rtype: str
    """
    return os.path.join(os.path.dirname(__file__), 'templates')


def load_jinja_env():
    """
    Load Jinja2 environment with templates.

    :returns: Jinja2 environment
    :rtype: jinja2.Environment
    """
    template_dir = get_templates_dir()
    return Environment(loader=FileSystemLoader(template_dir), autoescape=True)


def get_field_type_and_link(field):
    """
    Get the field type and link from a rosidl_parser.definition.Member.

    :param field: field to get the type and link if it's a NamespacedType
    :type field: rosidl_parser.definition.Member
    :returns: a string with field type and the relative link to the NamespacedType
    :rtype: tuple of (str, str)
    """
    link = ''
    if isinstance(field.type.value_type, AbstractGenericString):
        type_field = 'string'
    elif isinstance(field.type.value_type, NamespacedType):
        type_field = '/'.join(field.type.value_type.namespaced_name())
        link = type_field + '.html'
    else:
        type_field = field.type.value_type.typename
    return type_field, link


def read_constants(imported_interface, compact):
    """
    Set constants in the compact structure.

    :param imported_interface: interface to read all the constants
    :type imported_interface: rosidl_parser.definition.Message
    :param compact: dictionary with the compact definition
    :type compact: dict
    :returns: dictionary with the compact definition
    :rtype: dict
    """
    constants = imported_interface.constants
    for constant in constants:
        compact['constant_names'].append(constant.name + '=' + str(constant.value))
        if isinstance(constant.type, BasicType):
            compact['constant_types'].append(constant.type.typename)
        elif isinstance(constant.type, AbstractGenericString):
            compact['constant_types'].append('string')
    return compact


def read_default(field):
    """
    Read the default value otherwise return an empty string.

    :param field: field to get the default value if exists
    :type field: rosidl_parser.definition.Member
    :returns: default value string or empty string
    :rtype: str
    """
    if field.has_annotations('default'):
        return '=' + str(field.get_annotation_values('default')[0]['value'])
    else:
        return ''


def generate_compact_definition(imported_interface, indent=0):
    """
    Create the compact definition dictionary.

    :param imported_interface: class with all the data about the interface
    :type imported_interface: rosidl_parser.definition.Message
    :param indent: number of indentations to add to the generated text
    :type indent: int
    :returns: dictionary with the compact definition
    :rtype: dict
    """
    compact = {
        'constant_types': [],
        'constant_names': [],
        'relative_paths': [],
        'field_types': [],
        'field_names': [],
        'field_default_values': []
    }

    compact = read_constants(imported_interface, compact)

    for field in imported_interface.structure.members:
        compact['field_default_values'].append(read_default(field))

        type_field = ''
        array_definition_str = ''
        link = ''
        if isinstance(field.type, BasicType):
            type_field = field.type.typename
        elif isinstance(field.type, Array):
            type_field, link = get_field_type_and_link(field)
            if field.type.has_maximum_size():
                array_definition_str = '[' + str(field.type.size) + ']'
            else:
                array_definition_str = '[]'
        elif isinstance(field.type, AbstractGenericString):
            type_field = 'string'
            if isinstance(field.type, BoundedString):
                type_field = 'string[<=' + str(field.type.maximum_size) + ']'
        elif isinstance(field.type, NamespacedType):
            type_field = '/'.join(field.type.namespaced_name())
            link = type_field + '.html'
        elif isinstance(field.type, UnboundedSequence):
            array_definition_str = '[]'
            type_field, link = get_field_type_and_link(field)
        elif isinstance(field.type, BoundedSequence):
            array_definition_str = '[<=' + str(field.type.maximum_size) + ']'
            type_field, link = get_field_type_and_link(field)
        elif isinstance(field.type.value_type, Array):
            if field.type.value_type.has_maximum_size():
                array_definition_str = '[' + str(field.type.value_type.size) + ']'
            else:
                array_definition_str = '[]'
        elif isinstance(field.type.value_type, AbstractString):
            type_field = 'string'
            if isinstance(field.type, BoundedString):
                type_field = 'string[<=' + str(field.type.maximum_size) + ']'
        elif isinstance(field.type.value_type, NamespacedType):
            type_field = '/'.join(field.type.value_type.namespaced_name())
            link = type_field + '.html'
        else:
            type_field = str(field.type.value_type.typename)
        
        if field.name != SKIP_FIELD_NAME:
            compact['relative_paths'].append(link)
            compact['field_types'].append(type_field + array_definition_str)
            compact['field_names'].append(field.name)
    
    return compact


def copy_dict_with_suffix(destination, source, suffix):
    """
    Copy a dictionary and add a suffix to each key.

    :param destination: dictionary to set the value with the new key
    :type destination: dict
    :param source: dictionary to copy
    :type source: dict
    :param suffix: suffix to add to keys
    :type suffix: str
    """
    for key, value in source.items():
        destination['{}_{}'.format(key, suffix)] = value
