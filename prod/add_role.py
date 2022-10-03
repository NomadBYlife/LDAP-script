import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
import argparse
from ldap3 import MODIFY_ADD
from ldap3.core.exceptions import LDAPException
from utils import connect_ldap_server, get_users_for_mailing


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('dn', nargs='?')
    return parser


def add_to_roles(dn):
    """add to list of roles"""
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.modify('cn=Roles#1,ou=Roles,dc=name,dc=com',
                         {'uniqueMember': [(MODIFY_ADD, [f'{dn}'])]})
        print(f"[INFO] {dn} has been added to list of roles")
        with open('log.txt', 'a') as file:
            file.writelines(f"{dn} has been added to list of roles.\n")

    except LDAPException as e:
        return e


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    if namespace.dn:
        add_to_roles(str(namespace.dn))
    else:
        print(
            "[ERROR]User's DN is necessary. For example: python3 add_mail.py "
            "uid=someuid,cn=exEmployees,ou=groups,dc=domain,dc=com")
