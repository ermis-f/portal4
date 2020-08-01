"""
    LDAP Operations:
"""
import ldap
from ldap.modlist import addModlist,modifyModlist

from django.conf import settings
import logging
logger = logging.getLogger(__name__)

class LDAPOperations():
    def __init__(self):
        self.connect()

    def connect(self):
        if settings.LDAP_PROTO == 'ldaps':
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.con = ldap.initialize(settings.LDAP_PROTO + '://' + settings.LDAP_HOST + ':' + settings.LDAP_PORT)
        try:
            self.con.simple_bind_s(settings.LDAP_BIND_DN, settings.LDAP_BIND_DN_CREDENTIAL)
        except ldap.SERVER_DOWN:
            raise ldap.SERVER_DOWN('The LDAP library can’t contact the LDAP server. Contact the admin.')

    def check_attribute(self, attribute, value):
        """
        Takes an attribute and value and checks it against the LDAP server for existence/availability.
        This is mainly for checking unique attributes ie uid, mail, uidNumber

        :param attribute:
        :param value
        :return: tuple
        """
        query = "(" + attribute + "=" + value + ")"
        result = self.con.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, query)
        return result

    def add_user(self, modlist):
        """
        example param modlist dict should look like below containing only strings:

        modlist = {
            "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
            "uid": ["jdoe"],
            "sn": ["Doe"],
            "givenName": ["John"],
            "cn": ["John Doe"],
            "displayName": ["John Doe"],
            "mail": ["jdoe@example.com"],
            "homePhone": ["07234232434"],
            "uidNumber": ["1003"], # generate a unique ID
            "gidNumber": [502], # get from settings.LDAP_GID
            "loginShell": ["/bin/bash"],
            "homeDirectory": ["/home/users/jdoe"]
        }

        :param modlist:
        :return: tuple

        """
        dn = 'cn=' + modlist['uid'][0] + ',' + settings.LDAP_BASE_DN

        # convert modlist to bytes form ie b'abc'
        modlist_bytes = {}
        for key in modlist.keys():
            modlist_bytes[key] = [i.encode('utf-8') for i in modlist[key] if i
                                  is not None]

        result = self.con.add_s(dn, addModlist(modlist_bytes))
        mod_list = [(ldap.MOD_ADD, 'member', dn.encode('utf-8'))]
        # mod_list_bytes = {}
        # for key in mod_list.keys():
        #    mod_list_bytes[key] = [i.encode('utf-8') for i in mod_list[key] if i
        #                          is not None]
 
        self.con.modify_s('cn=active,ou=gn,ou=groups,dc=ermis-f,dc=eu',mod_list)
        self.con.modify_s('cn=staff,ou=gn,ou=groups,dc=ermis-f,dc=eu',mod_list)
        self.con.modify_s('cn=active,ou=kb,ou=groups,dc=ermis-f,dc=eu',mod_list)
        self.con.modify_s('cn=staff,ou=kb,ou=groups,dc=ermis-f,dc=eu',mod_list)
        self.con.modify_s('cn=active,ou=cr,ou=groups,dc=ermis-f,dc=eu',mod_list)
        self.con.modify_s('cn=staff,ou=cr,ou=groups,dc=ermis-f,dc=eu',mod_list)
        self.con.modify_s('cn=active,ou=sm,ou=groups,dc=ermis-f,dc=eu',mod_list)
        self.con.modify_s('cn=active,ou=ews,ou=groups,dc=ermis-f,dc=eu',mod_list)
        self.con.modify_s('cn=active,ou=sso,ou=groups,dc=ermis-f,dc=eu',mod_list)

        return result

    def set_password(self, username, password):
        """
        set user password
        :param username:
        :param password:
        :return: ldap result
        """
        dn = "cn=%s,%s" % (username, settings.LDAP_BASE_DN,)
        user_result = self.check_attribute('uid', username)  # get user
        tmp_modlist = dict(user_result)
        old_value = {"userPassword": [tmp_modlist[dn]['userPassword'][0]]}
        new_value = {"userPassword": [password.encode()]}

        modlist = ldap.modlist.modifyModlist(old_value, new_value)
        result = self.con.modify_s(dn, modlist)
        return result


    def edit_profile(self, username, firstName, lastName, organization):
    
        dn = "cn=%s,%s" % (username, settings.LDAP_BASE_DN,)
        user_result = self.check_attribute('uid', username)  # get user
        tmp_modlist = dict(user_result)
        old_value = {"givenName": [tmp_modlist[dn]['givenName'][0]],"sn":[tmp_modlist[dn]['sn'][0]],"description":[tmp_modlist[dn]['description'][0]],"displayName": [tmp_modlist[dn]['displayName'][0]]}
        fullName=firstName+' '+lastName
        new_value = {"givenName": [firstName.encode()],"sn":[lastName.encode()],"description":[organization.encode()],"displayName":[fullName.encode()]}
        modlist = ldap.modlist.modifyModlist(old_value, new_value)
        result = self.con.modify_s(dn, modlist)
        result= None
        return result


    def delete_user(self, username):
        dn = "cn=%s,%s" % (username, settings.LDAP_BASE_DN,)
        response = self.con.delete_s(dn)
        return response
