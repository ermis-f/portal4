
def geoServiceAttribs(user, service):
    attributes = {}
    attributes['email'] = getattr(user, 'email')
    attributes['first_name'] = getattr(user, 'first_name')
    attributes['last_name'] = getattr(user, 'last_name')
    attributes['organization'] = getattr(user, 'organization')
    if "://geoportal.ermis-f.eu" in service:
        attributes['is_active'] = getattr(user, 'gn_is_active')
        attributes['is_staff'] = getattr(user, 'gn_is_staff')
        attributes['is_superuser'] = getattr(user, 'gn_is_superuser')

    if "://kb.ermis-f.eu" in service:
        attributes['is_active'] = getattr(user, 'kb_is_active')
        attributes['is_staff'] = getattr(user, 'kb_is_staff')
        attributes['is_superuser'] = getattr(user, 'kb_is_superuser')
        attributes['kb_editor'] = getattr(user, 'kb_is_editor')


    if "://cr.ermis-f.eu" in service:
        attributes['is_active'] = getattr(user, 'cr_is_active')
        attributes['is_staff'] = getattr(user, 'cr_is_staff')
        attributes['is_superuser'] = getattr(user, 'cr_is_superuser')
        attributes['cr_is_editor'] = getattr(user, 'cr_is_editor')


    if "://sm.ermis-f.eu" in service:
        attributes['is_active'] = getattr(user, 'sm_is_active')
        attributes['is_staff'] = getattr(user, 'sm_is_staff')
        attributes['is_superuser'] = getattr(user, 'sm_is_superuser')

    if "://ews.ermis-f.eu" in service:
        attributes['is_active'] = getattr(user, 'ews_is_active')
        attributes['is_staff'] = getattr(user, 'ews_is_staff')
        attributes['is_superuser'] = getattr(user, 'ews_is_superuser')

    print ('SSO Attribs-->>',getattr(user, 'is_active'),
        '<->',getattr(user, 'is_staff'),
        '<->',getattr(user, 'is_superuser'),
        '<<--CR Attribs-->>',getattr(user, 'cr_is_active'),
        '<->',getattr(user, 'cr_is_staff'),
        '<->',getattr(user, 'cr_is_superuser'),
#        '<<--KB Attribs-->>',getattr(user, 'kb_is_active'),
#        '<->',getattr(user, 'kb_is_staff'),
#        '<->',getattr(user, 'kb_is_superuser'),
#        '<<--Sent to NG-->>',attributes['is_active'],
#        '<->',attributes['is_staff'],
#        '<->',attributes['is_superuser'],
        '<--Service-->',service,
        )
    return attributes
