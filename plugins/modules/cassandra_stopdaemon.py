#!/usr/bin/python

# 2019 Rhys Campbell <rhys.james.campbell@googlemail.com>
# https://github.com/rhysmeister
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


DOCUMENTATION = '''
---
module: cassandra_stopdaemon
author: Rhys Campbell (@rhysmeister)
short_description: Stops cassandra daemon.
requirements: [ nodetool ]
description:
    - Stops cassandra daemon.
options:
  host:
    description:
      - The hostname.
    type: str
    default: 127.0.0.1
  port:
    description:
      - The Cassandra TCP port.
    type: int
    default: 7199
  password:
    description:
      - The password to authenticate with.
    type: str
  password_file:
    description:
      - Path to a file containing the password.
    type: str
  username:
    description:
      - The username to authenticate with.
    type: str
  nodetool_path:
    description:
      - The path to nodetool.
    type: str
  debug:
    description:
      - Enable additional debug output.
    type: bool
'''

EXAMPLES = '''
- name: Stops cassandra daemon.
  cassandra_stopdaemon:
'''

RETURN = '''
cassandra_stopdaemon:
  description: The return state of the executed command.
  returned: success
  type: str
'''

from ansible.module_utils.basic import AnsibleModule, load_platform_subclass
import socket
__metaclass__ = type


from ansible_collections.community.cassandra.plugins.module_utils.NodeToolCmdObjects import NodeToolCmd, NodeToolCommandSimple
from ansible_collections.community.cassandra.plugins.module_utils.cassandra_common_options import cassandra_common_argument_spec


def main():
    argument_spec = cassandra_common_argument_spec()
    argument_spec.update(
            uuid=dict(type='str', aliases=['is']),
            poll=dict(type='int', default=1),
            interval=dict(type='int', default=30)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
    )

    cmd = 'stopdaemon'

    n = NodeToolCommandSimple(module, cmd)

    rc = None
    out = ''
    err = ''
    result = {}

    (rc, out, err) = n.run_command()
    out = out.strip()
    if module.debug:
        if out:
            result['stdout'] = out
        if err:
            result['stderr'] = err

    if rc == 0:
        result['changed'] = True
        result['msg'] = "nodetool stopdaemon executed successfully"
        module.exit_json(**result)
    elif rc == 2 and out == "Cassandra has shutdown.":
        # 2.2 behaves a little differently
        result['changed'] = True
        result['msg'] = "nodetool stopdaemon executed successfully"
        module.exit_json(**result)
    else:
        result['rc'] = rc
        result['changed'] = False
        result['msg'] = "nodetool stopdaemon did not execute successfully"
        module.exit_json(**result)


if __name__ == '__main__':
    main()
