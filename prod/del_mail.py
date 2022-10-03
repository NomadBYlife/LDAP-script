import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")

from utils import connect_ldap_server, get_users_for_mailing
from ldap3 import SUBTREE, MODIFY_DELETE, MODIFY_ADD
from ldap3.core.exceptions import LDAPException


def get_mailing_list(search_base):
    """get mailing list"""
    search_filter = '(objectClass=nisMailAlias)'
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.search(search_base=search_base,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['rfc822MailMember'])

        results = ldap_conn.entries
        return results
    except LDAPException as e:
        return e


def del_from_mailing_list(mail_address, user_dn):
    """delete from mailing list"""
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.modify('cn=mailing2@rav,ou=Mailing Lists,dc=name,dc=com',
                         {'rfc822MailMember': [(MODIFY_DELETE, [f'{mail_address}'])]})
        ldap_conn.modify(f'{user_dn}',
                         {'description': [(MODIFY_ADD, [f'verified email'])]})
    except LDAPException as e:
        return e


def match_check():
    """match checking"""
    mailing_list = get_mailing_list(search_base='cn=mailing2@rav,ou=Mailing Lists,dc=name,dc=com')
    ex_user_list = get_users_for_mailing(search_base='cn=exEmployees,ou=groups,dc=name,dc=com')
    mailing_list_str = set(map(str.lower, mailing_list[0].rfc822MailMember))
    for user in ex_user_list:
        if len(user.mail) > 1:
            for mail in user.mail:
                if str(mail).lower() in mailing_list_str:
                    del_from_mailing_list(mail, user.entry_dn)
                    print(f"[INFO] {user.uid}'s mail({mail}) has been removed from mailing list.")
                    with open('log.txt', 'a') as file:
                        file.writelines(f"{user.uid}'s mail({user.mail}) has been removed from mailing list.\n")
        else:
            if str(user.mail).lower() in mailing_list_str:
                del_from_mailing_list(user.mail, user.entry_dn)
                print(f"[INFO] {user.uid}'s mail({user.mail}) has been removed from mailing list.")
                with open('log.txt', 'a') as file:
                    file.writelines(f"{user.uid}'s mail({user.mail}) has been removed from mailing list.\n")


if __name__ == "__main__":
    match_check()
