from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPExceptionError
from config import server_ip, user_dn, password


def connect_ldap_server():
    """Connect to the LDAP server"""
    try:
        server_uri = server_ip
        server = Server(server_uri, get_info=ALL)
        connection = Connection(server,
                                user=user_dn,
                                password=password)

        connection.bind()
        return connection
    except LDAPExceptionError as e:
        return (e)


def get_groups_of_EX(search_base):
    """get all EX-* groups"""
    search_filter = '(ou=Ex*)'
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.search(search_base=search_base,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['uid', 'mail', 'description'])
        results = ldap_conn.entries
        result = []
        for res in results:
            result.append(res.entry_dn)
        return result
    except LDAPException as e:
        return e


def get_ex_users_for_mailing(search_base):
    """Get email all of exUsers without mark about removal from mailing lists"""
    search_filter = '(&(uid=*)(!(description=[SYS] deleted from mailing list)))'
    ldap_conn = connect_ldap_server()
    mail_list = []
    for dn in search_base:
        try:
            ldap_conn.search(search_base=dn,
                             search_filter=search_filter,
                             search_scope=SUBTREE,
                             attributes=['uid', 'mail', 'description'])
            result = ldap_conn.entries
            for res in result:
                mail_list.append(res.mail)
        except LDAPException as e:
            return e
    return mail_list


def get_users_for_roles(search_base):
    """Get DN all of exUsers without mark about removal from roles"""
    search_filter = '(&(uid=*)(!(description=[SYS] deleted from roles list)))'
    ldap_conn = connect_ldap_server()
    dn_list = []
    for dn in search_base:
        try:
            ldap_conn.search(search_base=dn,
                             search_filter=search_filter,
                             search_scope=SUBTREE,
                             attributes=['uid', 'mail', 'description'])
            result = ldap_conn.entries
            for res in result:
                dn_list.append(res.entry_dn)
        except LDAPException as e:
            return e
    return dn_list


def get_user_mail(dn):
    """taking the email of a unique user"""
    search_filter = '(uid=*)'
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.search(search_base=dn,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['uid', 'mail', 'description'])
        result = ldap_conn.entries[0].mail

        return result
    except LDAPException as e:
        return e


def get_dn_of_mailing_lists():
    """get all dn from the mailing lists"""
    search_filter = '(objectClass=nisMailAlias)'
    ldap_conn = connect_ldap_server()

    try:
        ldap_conn.search(search_base="ou=Mailing Lists,dc=rightandabove,dc=com,dc=domains",
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['rfc822MailMember'])
        data = []
        mails = []
        dn = []
        general_list = ldap_conn.entries
        for group in general_list:
            dn.append(group.entry_dn)
            data.append(group.rfc822MailMember)
        for row in data:
            if type(row.value) == str:
                mails.append(row.value)
            if type(row.value) == list:
                for a in row.value:
                    mails.append(a)
        mails = list(set(mails))
        return mails, dn
    except LDAPException as e:
        return e


def get_unique_member_list():
    """get currently uniqueMember list from roles"""
    search_filter = '(objectClass=groupOfUniqueNames)'
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.search(search_base='ou=Roles,dc=rightandabove,dc=com,dc=domains',
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['uniqueMember'])
        data = ldap_conn.entries
        uniq_members = []
        roles_dn = []
        for i in data:
            roles_dn.append(i.entry_dn)
            for q in i.uniqueMember:
                uniq_members.append(q)
        uniq_members = list(set(uniq_members))
        return uniq_members, roles_dn
    except LDAPException as e:
        return e
