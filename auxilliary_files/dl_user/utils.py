# Utility functions

from django.core.mail import send_mail


def send_reset_password_email(email, from_email, full_name, reset_link, app_name, username):
    """
    Send password reset email
    :param email:
    :param from_email:
    :param full_name: 
    :param reset_link: 
    :param app_name: 
    :param username
    :return: 
    """
    tpl = """

Γεια σου {full_name},

Έχετε ζητήσει την αλλαγή του προσωπικού σας κωδικού. Μπορείτε να το κάνετε στον παρακάτω σύνδεσμο:

{reset_link}

Αν δεν έχετε αιτηθεί αλλαγή κωδικού, παρακαλώ αγνοείστε αυτό το mail.

Ο κωδικός σας δεν θα αλλάξει μέχρι να χρησιμοποιήσετε τον σύνδεσμο και να δημιουργήσετε νέο κωδικό.

Το όνομα χρήστη σας είναι {username}

-------------------------------------------------------------------------------------------

Hello {full_name},

Someone has requested a link to change your password. You can do this through the link below:

{reset_link}

If you didn't request this, please ignore this email.

Your password won't change until you access the link above and create a new one.

Your username is {username} 



-- {app_name}
"""
    subject = '[' + app_name + '] Password reset instructions'
    msg_map = { 'full_name': full_name, 'reset_link': reset_link, 'app_name': app_name, 'username': username }
    message = tpl.format_map(msg_map)

    send_mail(subject, message, from_email, [email])


def send_newly_registered_email(email, from_email, full_name, activate_link, app_name, username):
    """
    Send notification for new registrations with activation link
    :param email: 
    :param from_email: 
    :param full_name: 
    :param activate_link: 
    :param app_name: 
    :param username
    :return: 
    """
    tpl = """

Καλώς ήλθες {full_name}!

Το πρώτο βήμα είναι να επιβεβαιώσετε το email σας. Κάντε κλικ στον παρακάτω σύνδεσμο ή επικολλήστε τον στον φυλλομετρητή σας:

{activate_link}

Το όνομα χρήστη σας είναι {username}

-----------------------------------------------------------------------------------------------

Welcome {full_name}!

The first step is to verify your email address. Please click the link or paste the URL into your web browser:

{activate_link}

Your username is {username}



-- {app_name}
"""
    subject = 'Welcome to ' + app_name + '!'
    msg_map = { 'full_name': full_name, 'activate_link': activate_link, 'app_name': app_name, 'username': username }
    message = tpl.format_map(msg_map)

    send_mail(subject, message, from_email, [email])
