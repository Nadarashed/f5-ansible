# -*- coding: utf-8 -*-
#
# Copyright: (c) 2019, F5 Networks Inc.
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
    from library.modules.bigip_monitor_mysql import ApiParameters
    from library.modules.bigip_monitor_mysql import ModuleParameters
    from library.modules.bigip_monitor_mysql import ModuleManager
    from library.modules.bigip_monitor_mysql import ArgumentSpec
    from test.units.compat import unittest
    from test.units.compat.mock import Mock, patch
    from test.units.modules.utils import set_module_args
except ImportError:
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_monitor_mysql import ApiParameters
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_monitor_mysql import ModuleParameters
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_monitor_mysql import ModuleManager
    from ansible_collections.f5networks.f5_modules.plugins.modules.bigip_monitor_mysql import ArgumentSpec
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
            parent='/Common/mysql',
            interval=5,
            timeout=120,
            time_until_up=20,
            target_username='foobar',
            send='SELECT * from v$instance1',
            database='instance1',
            recv='OPEN',
            recv_column='1',
            recv_row='1',
            count=10,
            manual_resume=True,
            debug=True
        )
        p = ModuleParameters(params=args)
        assert p.parent == '/Common/mysql'
        assert p.interval == 5
        assert p.timeout == 120
        assert p.time_until_up == 20
        assert p.target_username == 'foobar'
        assert p.send == 'SELECT * from v$instance1'
        assert p.recv == 'OPEN'
        assert p.count == 10
        assert p.recv_column == '1'
        assert p.recv_row == '1'
        assert p.manual_resume == 'enabled'
        assert p.debug == 'yes'

    def test_api_parameters(self):
        args = load_fixture('load_bigip_monitor_mysql.json')
        p = ApiParameters(params=args)
        assert p.parent == '/Common/mysql'
        assert p.ip == '1.1.1.1'
        assert p.port == '30025'
        assert p.time_until_up == 0
        assert p.up_interval == 0
        assert p.manual_resume == 'disabled'
        assert p.target_username == 'some_user'
        assert p.timeout == 60
        assert p.count == 0
        assert p.send == 'this is send string'
        assert p.recv == 'this is recv string'
        assert p.recv_column == '1'
        assert p.recv_row == '2'


class TestManager(unittest.TestCase):
    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create(self, *args):
        set_module_args(dict(
            name='mysqdb',
            parent='/Common/mysql',
            interval=10,
            timeout=30,
            time_until_up=5,
            target_username='foobar',
            send='SELECT * from v$instance1',
            database='instance1',
            recv='OPEN',
            recv_column='1',
            recv_row='1',
            count=10,
            manual_resume=True,
            debug=True,
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

        # Override methods in the specific type of manager
        mm = ModuleManager(module=module)
        mm.exists = Mock(side_effect=[False, True])
        mm.create_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
