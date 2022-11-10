import sys
# sys.path.append("/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
from sys import argv
from ldap3 import MODIFY_ADD, MODIFY_DELETE
from ldap3.core.exceptions import LDAPException
from utils import connect_ldap_server, get_user_mail

sys.tracebacklimit = 0
try:
    _, dn, mailing, = argv


    def add_user_to_mailing(dn, mailing):
        """add the user's email to the mailing list'"""
        ldap_conn = connect_ldap_server()
        try:
            add_mailinig = ldap_conn.modify(mailing,
                                            {'rfc822MailMember': [(MODIFY_ADD, [f'{get_user_mail(dn)}'])]})
            if add_mailinig:
                ldap_conn.modify(f'{dn}',
                                 {'description': [(MODIFY_DELETE, [f'[SYS] deleted from mailing list'])]})
            else:
                raise Exception(
                    "[SYS] The mail has not been added in mailing list. Check the user DN and mailing list DN. For "
                    "example: python3 add_mailing.py \"uid=uniqueUid,ou=group,ou=group,dc=rightandabove,dc=com,"
                    "dc=domains\" \"cn=cnMailingList,ou=Mailing Lists,dc=rightandabove,dc=com,dc=domains\" "
                    "or such entry already exists")
        except LDAPException as e:
            return e
except:
    raise Exception(
        "[SYS] The mail has not been added in mailing list. Check the user DN and mailing list DN. For "
        "example: python3 add_mailing.py \"uid=uniqueUid,ou=group,ou=group,dc=rightandabove,dc=com,"
        "dc=domains\" \"cn=cnMailingList,ou=Mailing Lists,dc=rightandabove,dc=com,dc=domains\"")
if __name__ == '__main__':
    add_user_to_mailing(dn, mailing)
