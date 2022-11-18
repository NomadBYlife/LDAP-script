import logging
import sys
# sys.path.append("/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
from utils import connect_ldap_server, get_groups_of_EX, get_ex_users_for_mailing, get_users_for_roles, \
    get_dn_of_mailing_lists, get_unique_member_list
from ldap3 import MODIFY_DELETE, MODIFY_ADD
sys.tracebacklimit = 0
logger = logging.getLogger('main.main_check')

def del_from_mailing_list(mail_address):
    """delete from mailing list"""
    ldap_conn = connect_ldap_server()
    try:
        _, dns = get_dn_of_mailing_lists()
        for dn in dns:
            result = ldap_conn.modify(dn, {'rfc822MailMember': [(MODIFY_DELETE, [f'{mail_address}'])]})
            if result:
                ldap_conn.modify(f'{mail_address.entry.entry_dn}',
                             {'description': [(MODIFY_ADD, [f'[SYS] deleted from mailing: {dn} '])]})
                logger.info(f"{mail_address.entry.entry_dn} deleted from mailing: {dn}")
    except Exception as e:
        logger.error(e)


def del_from_roles(user_dn, dn_roles):
    """delete from role"""
    ldap_conn = connect_ldap_server()
    for dn in dn_roles:
        try:
            result = ldap_conn.modify(dn,
                             {'uniqueMember': [(MODIFY_DELETE, [f'{(user_dn)}'])]})
            if result:
                ldap_conn.modify(f'{user_dn}',
                             {'description': [(MODIFY_ADD, [f'[SYS] deleted from role: {dn}'])]})
                logger.info(f"{user_dn} deleted from: {dn}")

        except Exception as e:
            logger.error(e)


def main_check():
    """match checking"""
    logger.info('The check has begun')
    mailing_list, _ = get_dn_of_mailing_lists()
    users_groups = get_groups_of_EX(search_base='ou=Users,dc=rightandabove,dc=com,dc=domains')
    ex_user_list_mailing = get_ex_users_for_mailing(users_groups)
    for i in ex_user_list_mailing:
        if i in mailing_list:
            del_from_mailing_list(i)
    ex_user_list_roles = get_users_for_roles(users_groups)
    uniq_members_roles, dn_roles = get_unique_member_list()
    for dn in ex_user_list_roles:
        if dn in uniq_members_roles:
            del_from_roles(dn, dn_roles)
    logger.info('The check has finished')

if __name__ == "__main__":
    main_check()
