import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
from utils import connect_ldap_server, get_users_for_roles
from ldap3 import SUBTREE, MODIFY_DELETE, MODIFY_ADD
from ldap3.core.exceptions import LDAPException


def get_unique_member_list(search_base):
    """get uniqueMember list from role"""
    search_filter = '(cn=Roles#1)'
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.search(search_base=search_base,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['uniqueMember'])
        results = ldap_conn.entries
        return results
    except LDAPException as e:
        return e


def del_from_roles(dn):
    """delete from list of roles"""
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.modify('cn=Roles#1,ou=Roles,dc=name,dc=com',
                         {'uniqueMember': [(MODIFY_DELETE, [f'{dn}'])]})
        ldap_conn.modify(f'{dn}',
                         {'description': [(MODIFY_ADD, [f'verified roles'])]})

    except LDAPException as e:
        return e


def match_check():
    """match checking"""
    unique_member_list = get_unique_member_list('cn=Roles#1,ou=Roles,dc=name,dc=com')
    ex_user_list = get_users_for_roles(search_base='cn=exEmployees,ou=groups,dc=name,dc=com')
    for user in ex_user_list:
        if any(str(user.uid) in uid for uid in unique_member_list[0].uniqueMember):
            del_from_roles(user.entry_dn)
            print(f"[INFO] User {user.uid} has been removed from list of roles.")
            with open('log.txt', 'a') as file:
                file.writelines(f"User {user.uid} has been removed from list of roles.\n")


if __name__ == "__main__":
    match_check()
