# -*- coding: utf-8 -*-
#
# Copyright: (c) 2017, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

if sys.version_info < (2, 7):
    pytestmark = pytest.mark.skip("F5 Ansible modules require Python >= 2.7")

from ansible.module_utils.basic import AnsibleModule

try:
    from library.modules.bigiq_regkey_license import ModuleParameters
    from library.modules.bigiq_regkey_license import ApiParameters
    from library.modules.bigiq_regkey_license import ModuleManager
    from library.modules.bigiq_regkey_license import ArgumentSpec
    from test.units.compat import unittest
    from test.units.compat.mock import Mock, patch
    from test.units.modules.utils import set_module_args
except ImportError:
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigiq_regkey_license import ModuleParameters
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigiq_regkey_license import ApiParameters
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigiq_regkey_license import ModuleManager
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigiq_regkey_license import ArgumentSpec
    from ansible_collections.f5networks.f5_modules.tests.unit.compat import unittest
    from ansible_collections.f5networks.f5_modules.tests.unit.compat.mock import Mock, patch
    from ansible_collections.f5networks.f5_modules.tests.unit.modules.utils import set_module_args


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            regkey_pool='foo',
            license_key='XXXX-XXXX-XXXX-XXXX-XXXX',
            accept_eula=True,
            description='this is a description'
        )

        p = ModuleParameters(params=args)
        assert p.regkey_pool == 'foo'
        assert p.license_key == 'XXXX-XXXX-XXXX-XXXX-XXXX'
        assert p.accept_eula is True
        assert p.description == 'this is a description'

    def test_api_parameters(self):
        args = load_fixture('load_regkey_license_key.json')

        p = ApiParameters(params=args)
        assert p.description == 'foo bar baz'


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()
        self.patcher1 = patch('time.sleep')
        self.patcher1.start()

    def tearDown(self):
        self.patcher1.stop()

    def test_create(self, *args):
        set_module_args(dict(
            regkey_pool='foo',
            license_key='XXXX-XXXX-XXXX-XXXX-XXXX',
            accept_eula=True,
            description='this is a description',
            provider=dict(
                server='localhost',
                password='password',
                user='admin'
            )
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(side_effect=[False, True])
        mm.create_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
        assert results['description'] == 'this is a description'
