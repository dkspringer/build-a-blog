import re

from models import User


def user_exists(username, email):
    if User.query.filter_by(user_name=username).count() > 0:
        return True
    if User.query.filter_by(email_address=email).count() > 0:
        return True
    return False

def passwords_match(password, verify):
    return password == verify

def is_valid_username(username):
    return (5 <= len(username) <= 32) and (' ' not in username)

def is_valid_password(password):
    return(8 <= len(password) <= 64) and (' ' not in password)

def is_valid_email(email):
    if re.match(pattern, email):
        return True
    return False


# Defines pattern for valid email address (done once, when module imported)
special = "!#$%&'*+\-\/=?^_`{|}~" # special characters allowed
alpha = "a-zA-Z"
num = "0-9"
chars = alpha+num+special # permitted characters
dotted = '[{0}](\.?[{1}]+)*'.format(chars, chars)
domain = '\.[a-zA-Z]{2,3}' # i.e. '.com' or '.edu'
pattern_string = '^{0}@{1}{2}$'.format(dotted, dotted, domain)
pattern = re.compile(pattern_string)