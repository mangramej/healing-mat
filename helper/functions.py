import re
from flask import session, redirect, url_for


def request_validation(form):
    fields = {
        "email": "",
        "password": "",
        "emailErr": "",
        "passwordErr": ""
    }

    # check whether email form has value and if it's a valid email
    if form['email']:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if re.fullmatch(regex, form['email']):
            fields['email'] = form['email']

        else:
            fields["emailErr"] = "Please use a valid email address."

    else:
        fields["emailErr"] = "Email is required."

    # check whether email form has value
    if form['password']:
        fields['password'] = form['password']
    else:
        fields["passwordErr"] = "Password is required."

    return fields


def is_authenticated():
    if session.get('signedin'):
        return True

    return False
