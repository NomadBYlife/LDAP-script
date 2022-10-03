import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
import argparse
from ldap3 import MODIFY_ADD
from ldap3.core.exceptions import LDAPException

from utils import connect_ldap_server, get_user_for_add


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('dn', nargs='?')
    return parser


def add_to_mailing_list(dn):
    """add to mailing list"""
    users_list = get_user_for_add(dn)
    ldap_conn = connect_ldap_server()
    for mail_address in users_list[0].mail:
        try:
            ldap_conn.modify('cn=mailing2@rav,ou=Mailing Lists,dc=name,dc=com',
                             {'rfc822MailMember': [(MODIFY_ADD, [f'{mail_address}'])]})
            print(f"[INFO] {mail_address} has been added to mailing list")
            with open('log.txt', 'a') as file:
                file.writelines(f"{dn} has been added to mailing list.\n")
        except LDAPException as e:
            return e


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    if namespace.dn:
        add_to_mailing_list(str(namespace.dn))
    else:
        print(
            "[ERROR]User's DN is necessary. For example: python3 add_mail.py "
            "uid=someuid,cn=exEmployees,ou=groups,dc=domain,dc=com")
