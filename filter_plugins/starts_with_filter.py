# -*- coding: utf-8 -*-

import unittest
import re
import unicodedata
import textwrap
import json

import ansible.vars.manager


def _string_sanity_check(string):
    if string is None:
        return ''
    if not isinstance(string, basestring):
        return str(string)
    return string

def _starts_with_str(haystack, needle):
    sanitzed_haystack = _string_sanity_check(haystack)
    sanitzed_needle = _string_sanity_check(needle)
    return sanitzed_haystack.startswith(sanitzed_needle)

def _remove(haystack, needle):
    sanitzed_haystack = _string_sanity_check(haystack)
    sanitzed_needle = _string_sanity_check(needle)
    return sanitzed_haystack[len(sanitzed_needle):]

''' Checks whether the string begins with the needle at position (default: 0). '''
def starts_with(entries, needle, remove=False):
    if isinstance(entries, ansible.vars.hostvars.HostVarsVars):
        res = dict()
        for key in iter(entries):
            if _starts_with_str(key, needle):
                dictkey = key
                if remove:
                    dictkey = _remove(key, needle)
                res[dictkey] = entries.__getitem__(key)
        return res
    elif isinstance(entries, dict):
        res = dict()
        for key, value in iter(entries.items()):
            if _starts_with_str(key, needle):
                if remove:
                    key = _remove(key, needle)
                res[key] = value
        return res
    else:
        ret = []
        for entry in entries:
            if _starts_with_str(entry, needle):
                if remove:
                    entry = _remove(entry, needle)
                ret.append(entry)
        return ret


def starts_with_to_str(entries, needle, remove=False):
    return '"' + json.dumps(starts_with(entries, needle, remove)) + '"'

# ---


class FilterModule(object):

    def filters(self):
        return {
            'starts_with': starts_with,
            'starts_with_to_str': starts_with_to_str
        }

# ---
