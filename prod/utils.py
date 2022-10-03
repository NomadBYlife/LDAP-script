from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPExceptionError

from config import server_ip, user_dn, password


def connect_ldap_server():
    try:
        server_uri = server_ip
        server = Server(server_uri, get_info=ALL)
        connection = Connection(server,
                                user=user_dn,
                                password=password)

        connection.bind()
        return connection
    except LDAPExceptionError as e:
        print(e)


def get_users_for_mailing(search_base):
    search_filter = '(&(uid=*)(!(description=verified email)))'
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.search(search_base=search_base,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['uid', 'mail', 'description'])
        results = ldap_conn.entries
        print(results)
        if len(results) == 0:
            raise ValueError('incorrect dn')
        return results
    except LDAPException as e:
        return e


def get_users_for_roles(search_base):
    search_filter = '(&(uid=*)(!(description=verified roles)))'
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.search(search_base=search_base,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['uid', 'mail', 'description'])
        results = ldap_conn.entries
        print(results)
        if len(results) == 0:
            raise ValueError('incorrect dn')
        return results
    except LDAPException as e:
        return e


def get_user_for_add(search_base):
    search_filter = '(uid=*)'
    ldap_conn = connect_ldap_server()
    try:
        ldap_conn.search(search_base=search_base,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         attributes=['uid', 'mail', 'description'])
        results = ldap_conn.entries
        print(results)
        if len(results) == 0:
            raise ValueError('incorrect dn')
        return results
    except LDAPException as e:
        return e


