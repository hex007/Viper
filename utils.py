#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(Hex)--(11/26/17 8:00 PM)-------------
# `--(Viper ... utils)-->
import subprocess
import xml.etree.ElementTree as ET
from os import path
from subprocess import PIPE

from system import System


__tag__ = 'utils'


def load_settings():
    """Load settings an convert into a dict for easy lookups
    :rtype: dict
    """
    settings_file = "%s/settings.xml" % path.dirname(path.abspath(__file__))
    if not path.isfile(settings_file):
        return {}

    tree = ET.parse(settings_file)
    root = et_leaf_to_dict(tree.getroot())
    return root


def load_systems(settings):
    """Load valid systems with gamelist.xml files
    :rtype: dict of System
    """
    if not settings:
        return dict()

    directory = settings['gamelists_dir']
    sys_conf = settings['systems_conf']

    system_names = _find_systems(directory)
    trees = _load_systems(directory, system_names)
    systems = _parse_gamelist_trees(trees, sys_conf)
    return systems


def _find_systems(directory):
    """Find a list of valid system names that have gamelists already present.
    :returns ['gbc', 'nes'...]
    :rtype: list of str
    """
    valid_systems = subprocess.Popen(
            "find %s -maxdepth 1 -mindepth 1 -type d -not -empty -printf '%s\n'" % (directory, "%f"),
            shell=True, stdout=PIPE)
    systems = [i for i in valid_systems.communicate()[0].split()
               if path.isfile(path.expanduser("%s/%s/gamelist.xml" % (directory, i)))]
    return systems


def _load_systems(directory, system_names):
    """Load system gamelist xmls to trees.
    :rtype: dict
    """
    systems = dict()
    for system in system_names:
        tree = ET.parse(path.expanduser('%s/%s/gamelist.xml' % (directory, system)))
        root = tree.getroot()
        systems[system] = root
    return systems


def _load_details(loc):
    """Extract fullname and command from systems config"""
    tree = ET.parse(path.expanduser(loc))
    sys_list = {}
    for elem in tree.getroot():
        attrib = {i.tag: i.text for i in elem}
        sys_list[attrib['name']] = {'name': attrib['fullname'], 'command': attrib['command'], 'path': attrib['path']}
    return sys_list


def _parse_gamelist_trees(trees, systems_conf):
    """Convert systems tree to System objects which are delegated
     the responsibility of loading data about their games.
    :rtype: list of system
    """
    systems_list = []
    details = _load_details(systems_conf)
    for root in trees:  # for each system (nes, gb, gbc ...)
        if root in details:
            sys_d = details[root]
            systems_list.append(
                    System(root, trees[root], sys_d['name'], path.expanduser(sys_d['path']), sys_d['command'])
            )
    return systems_list


def et_parent_to_dict(root):
    """Convert xml parent element containing many elements to python dict"""
    return {node.tag: node.getchildren() for node in root}


def et_leaf_to_dict(root):
    """Convert xml leaf element describing a dict to python dict"""
    return {node.tag: node.text for node in root}


def et_leaf_list_to_list(root):
    """Convert xml leaf list to python list of dict"""
    return [node.attrib for node in root]
