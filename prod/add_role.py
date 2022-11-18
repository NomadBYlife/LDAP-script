import logging
import sys
# sys.path.append("/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
from sys import argv
from ldap3 import MODIFY_ADD, MODIFY_DELETE
from utils import connect_ldap_server

sys.tracebacklimit = 0
logger = logging.getLogger('main.add_role')
try:
    _, dn, role, = argv


    def add_user_to_role(dn, role):
        """add the user's dn to the role'"""

        ldap_conn = connect_ldap_server()
        try:
            add_roles = ldap_conn.modify(role,
                                         {'uniqueMember': [(MODIFY_ADD, [f'{dn}'])]})
            if add_roles:
                ldap_conn.modify(f'{dn}',
                                 {'description': [(MODIFY_DELETE, [f'[SYS] deleted from role: {role}'])]})
                logger.info(f"{dn} added to {role}")

            else:
                raise ValueError(
                    "[SYS] The role has not been added. Check the user DN and role DN. For example: python3 "
                    "add_role.py \"uid=uniqueUid,ou=group,ou=group,dc=rightandabove,dc=com,"
                    "dc=domains\" \"cn=cnRole,ou=role,dc=rightandabove,dc=com,dc=domains\" "
                    "or such entry already exists")
        except ValueError as e:
            return e
except:
    raise ValueError(
        "[SYS] The role has not been added. Check the user DN and role DN. For example: python3 "
        "add_role.py \"uid=uniqueUid,ou=group,ou=group,dc=rightandabove,dc=com,"
        "dc=domains\" \"cn=cnRole,ou=role,dc=rightandabove,dc=com,dc=domains\"")
if __name__ == '__main__':
    add_user_to_role(dn, role)
