from django import forms
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
#from django.contrib.auth.models import User
#Note: It's not recommended to import the User directly as it won't work in projects where the AUTH_USER_MODEL setting has been changed to a different user model. Use the get_user_model method instead:
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import ugettext, ugettext_lazy as _

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset

from captcha.fields import ReCaptchaField
from django_countries.fields import CountryField

from .models import Institution
from .ldap import LDAPOperations
from urllib import request

class UserRegisterForm(forms.Form):
    title_choices = (('Mr.', 'Mr'), ('Ms', 'Ms',), ('Mrs.', 'Mrs.',), ('Dr.', 'Dr.',), ('Prof.', 'Prof.',),)
    # optional schema fields during registration
    if "Personal Data" in settings.LDAP_USER_DATA:
        gender = forms.TypedChoiceField(
                                        choices=((0, "Male"), (1, "Female"),),
                                        coerce=lambda x: bool(int(x)),
                                        widget=forms.RadioSelect,
                                        initial='0',
                                        required=True)
        title = forms.ChoiceField(required=True, choices=title_choices)
        designation = forms.CharField(max_length=200)
        department = forms.CharField(required=True, max_length=255)
        phone = forms.CharField(required=True, max_length=200)
    if "Organization" in settings.LDAP_USER_DATA:
        organization = forms.ModelChoiceField(required=False,
                                              queryset=Institution.objects.all(),
                                              empty_label=_('Select your Organization'),
                                              label=_('Organization'),
                                              to_field_name='name')
    if "Address" in settings.LDAP_USER_DATA:
        address = forms.CharField(max_length=1000, widget=forms.Textarea())
        country = CountryField().formfield()
    # mandatory schema fields during registration
    first_name = forms.CharField(required=True, max_length=255, label=_('First Name'))
    last_name = forms.CharField(required=True, max_length=255, label=_('Last Name'))
    username = forms.CharField(required=True,
                               min_length=3,
                               max_length=30,
                               validators=[UnicodeUsernameValidator()])
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6,label=_('Password'))
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=6, label=_('Confirm Password'))
    #terms = forms.CharField(required=False,disabled=True,widget=forms.Textarea(attrs={"rows":5, "cols":20}),label='',initial=_('Terms'))
    accept = forms.BooleanField(required=True, label=_("I have read and accept the <a href='/static/policy.pdf' target=new>privacy policy</a>"))
    # hide captcha field during unit tests
    if not settings.TESTING:
        captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.ldap_ops = LDAPOperations()
        self.helper = FormHelper()
        self.helper.form_id = 'id-user-data-form'
        self.helper.form_method = 'post'
        # self.helper.form_action = 'register'
        self.helper.add_input(Submit('submit', _('Submit'), css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
                                    Fieldset('Basic Data',
                                             Field('first_name',
                                                   css_class="some-class"),
                                             Div('last_name', title="Your last name"),
                                             'email'),
                                    Fieldset('Login Details',
                                             'username', 'password', 'password1'),
                                    )
        if "Personal Data" in settings.LDAP_USER_DATA:
            self.helper.layout.append(
                                      Fieldset('Personal Data',
                                               'gender', 'title', 'designation', 'department', 'phone'))
        if "Organization" in settings.LDAP_USER_DATA:
            self.helper.layout.append(
                                      Fieldset('Organization', 'organization'))
        if "Address" in settings.LDAP_USER_DATA:
            self.helper.layout.append(
                                      Fieldset('Address', 'address', 'country'))
        self.helper.layout.append(Fieldset('Policy','accept'))
        if settings.RECAPTCHA_PUBLIC_KEY and settings.RECAPTCHA_PRIVATE_KEY is not None:
            self.helper.layout.append(
                                      Fieldset('Spam control', 'captcha'))

    def clean_username(self):
        username = self.cleaned_data['username']

        # check username existence in local storage DB
        query_set = User.objects.filter(username=username)

        # check username existence in LDAP
        result = self.ldap_ops.check_attribute('uid', username)
        if result or query_set:
            raise forms.ValidationError("Username " + username + " is not available (in use)",
                                        code='username_exists_ldap')

        return username

    def clean_email(self):
        mail = self.cleaned_data['email']

        # check for email existence in local storage DB
        query_set = User.objects.filter(email=mail)

        # check email existence in LDAP
        result = self.ldap_ops.check_attribute('mail', mail)
        if result or query_set:
            raise forms.ValidationError("Email " + mail + " is not available (in use)",
                                        code='email_exists_ldap')

        return mail

    def clean(self):

        # Check for password matching
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')

        if password != password1:
            self._errors["password"] = self.error_class([_("Passwords do not match")])

        return self.cleaned_data


class PasswordResetForm(forms.Form):
    # hide captcha field during unit tests
    if not settings.TESTING:
        captcha = ReCaptchaField()
    email = forms.EmailField(
        required=True,
        label=_('Enter your email'),
        help_text=_('An email will be sent at the registered account that will contain a link for reseting your password.')
    )

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.ldap_ops = LDAPOperations()
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-reset-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit'), css_class='btn-warning'))
        #self.helper.form_class = 'form-horizontal'
        #self.helper.label_class = 'col-md-4'
        #self.helper.field_class = 'col-md-8'
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Field('email')
        )
        if settings.RECAPTCHA_PUBLIC_KEY and settings.RECAPTCHA_PRIVATE_KEY is not None:
            self.helper.layout.append(
                Field('captcha')
            )

    def clean_email(self):
        mail = self.cleaned_data['email']
        # check for email existence in local storage DB
        query_set = User.objects.filter(email=mail, is_active=True)

        # check email existence in LDAP
        result = self.ldap_ops.check_attribute('mail', mail)
        if not result and not query_set:
            raise forms.ValidationError(_("This email address is not associated with a user account."),
                                        code='email_exists_ldap')
        return mail


class PasswordResetEditForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label=_('New Password'))
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=6, label=_('Confirm new Password'))

    def __init__(self, *args, **kwargs):
        super(PasswordResetEditForm, self).__init__(*args, **kwargs)
        self.ldap_ops = LDAPOperations()
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-reset-edit-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit'), css_class='btn-warning'))
        #self.helper.form_class = 'form-horizontal'
        #self.helper.label_class = 'col-md-4'
        #self.helper.field_class = 'col-md-8'
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Fieldset('Please enter your new password',
                     Field('password'),
                     Field('password1')
                     )
        )

    def clean(self):
        # Check for password matching

        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')

        if password != password1:
            self._errors["password"] = self.error_class([_("Passwords don't match")])

        return self.cleaned_data

class ProfileEditForm(forms.Form):
        #if "Organization" in settings.LDAP_USER_DATA:
        #    organization = forms.ModelChoiceField(required=False,
        #                                      queryset=Institution.objects.all(),
        #                                  empty_label=_('Select your Organization'),
        #                                      label=_('Organization'),
        #                                      to_field_name='name')
        #first_name = forms.CharField(required=True, max_length=255, label=_('First Name'))
        #last_name = forms.CharField(required=True, max_length=255, label=_('Last Name'))
        #username = forms.CharField(required=True,
        #                       help_text = _("You can not edit your username"),
        #                       disabled=True)
        #email = forms.EmailField(required=True, initial='fd',
        #                       help_text = _("You can not edit your email. If you want to use another email you can create a new account"), 
        #                       disabled=True)
        #user = None
        #referer = forms.CharField(label="ref")

        def __init__(self, *args, **kwargs):
            user = kwargs.pop("user")
            #referer= kwargs.pop("rerefer")
            
            super(ProfileEditForm, self).__init__(*args, **kwargs)
            #self.fields['referer']= forms.CharField(initial=referer)
            self.fields['first_name'] =  forms.CharField(required=True,
                                         max_length=255, 
                                         initial=user.first_name,
                                         label=_('First Name'))
            self.fields['last_name'] =  forms.CharField(required=True,
                                         max_length=255,
                                         initial=user.last_name,
                                         label=_('Last Name'))
            self.fields['username'] = forms.CharField(required=True,
                                         help_text = _("You can not edit your username."),
                                         disabled = True,
                                         initial=user.username)
            self.fields['email'] =  forms.CharField(required=True,
                                         disabled=True,
                                         initial=user.email,
                                         help_text = _("You can not edit your email. If you want to use another email you should create a new account"))
            if "Organization" in settings.LDAP_USER_DATA:
                self.fields['organization'] = forms.ModelChoiceField(required=False,
                                              queryset=Institution.objects.all(),
                                              initial = user.organization,
                                              empty_label=_('Select your Organization'),
                                              label=_('Organization'),
                                              to_field_name='name')


            self.ldap_ops = LDAPOperations()
            self.helper = FormHelper()
            self.helper.form_id = 'id-user-edit-form'
            self.helper.form_method = 'post'
            # self.helper.form_action = 'register'
            self.helper.add_input(Submit('submit', _('Submit'), css_class='btn-success'))
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-md-2'
            self.helper.field_class = 'col-md-8'
            self.helper.error_text_inline = False
            self.helper.layout = Layout(
                                    Fieldset('Basic Data',
                                             Field('first_name',
                                                   css_class="some-class"),
                                             Div('last_name', title="Your last name"),
                                             'email'),
                                    Fieldset('Login Details',
                                             'username'),
                                    )
            if "Organization" in settings.LDAP_USER_DATA:
                self.helper.layout.append(
                                      Fieldset('Organization', 'organization'))

        def clean(self):
            return self.cleaned_data

