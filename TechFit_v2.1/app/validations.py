"""Holds Input Validation Functions"""

import pandas as pd
from wtforms.validators import ValidationError

# COMMON VALIDATORS

def val_upper(data: str):
    """Validates Upper Case Exist"""
    return any(i.isupper() for i in data)

def val_lower(data: str):
    """Validates Upper Case Exist"""
    return any(i.islower() for i in data)

def val_digit(data: str):
    """Validates Digit Exist"""
    return any(i.isdigit() for i in data)

def val_char(data: str):
    """Validates Digit Exist"""
    return any(i.isalnum() for i in data)

# ENTRY SPECIFIC VALIDATORS

# Users

def validate_username(form, field):
    """"Validates Username Input"""
    username = str(field.data)

    # username exist?
    if validate_not_onfile(username) is True:
        # length correct?
        if len(username) >= 5:
            # num included?
            if val_digit(username) is False:
                raise ValidationError('Username must contain at least 1 letter & number.')
        else:
            raise ValidationError('Username Must be at least 6 characters long.')
    else:
        raise ValidationError('Username Already Exist')

def validate_not_onfile(username: str):
    """Validates Username Doesnt Exist"""
    user_avaliable = False

    try:
        cols = ['Username']
        check = pd.read_csv("app/static/database/users.csv", usecols=cols)
        # throw user if it already exist
        if username not in check['Username'].values:
            user_avaliable = True
        else:
            raise ValidationError()
    except ValidationError:
        user_avaliable = False

    return user_avaliable

# Passwords

def validate_password(form, field):
    """"Validates Password Inputs"""
    password = str(field.data)

    # length correct?
    if len(password) >= 12:
        # contains at least 1 upper case, 1 lower case, 1 number & 1 special character?
        if val_upper(password) is False\
                or val_lower(password) is False\
                or val_digit(password) is False\
                or val_char(password) is False:
            raise ValidationError(
                'Password Must contain: 1 lower letter, 1 upper letter, 1 number & 1 char')
    else:
        raise ValidationError('Password Must be at least 12 characters long.')


def validate_not_common(form, field):
    """Checks Against Common Passwords"""
    password = str(field.data)
    common = False

    common_passwords = open("app/static/extras/common_pass.txt", 'r')
    Lines = common_passwords.readlines()

    # check lines to see if password exist
    for line in Lines:
        if password in line:
            common = True
            raise ValidationError('Password too "common." Please select another')

    return common
