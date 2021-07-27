"""User Authorizations"""

import pandas as pd
from pandas.core.frame import DataFrame
from wtforms.validators import ValidationError
from passlib.hash import sha256_crypt

def auth_user(username, password):
    """Authorizes Password"""
    user_authorized = False
    username = str(username).lower()
    password = str(password)

    try:
        cols = ['Username', 'Password']
        check = DataFrame(pd.read_csv("app/static/database/users.csv", usecols=cols))

        if username not in check['Username'].values: # throw user if it doesnt exist
            user_authorized = False
        else:
            condition = check['Username'] == username # set query condition
            location = check.loc[condition] # find user on data set
            location = location['Password'].reset_index() # reset index to 0 (only one row)
            stored_pass = str(location['Password'][0]) # get stored password

            # verify user password match
            if sha256_crypt.verify(password, stored_pass) is True:
                user_authorized = True

        if user_authorized is False:
            raise ValidationError()
    except ValidationError:
        print('Incorrect Username or Password')

    return user_authorized
