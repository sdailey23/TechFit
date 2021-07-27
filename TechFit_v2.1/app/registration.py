"""User Registration"""

import pandas as pd

from csv import writer
from pandas import DataFrame
from passlib.hash import sha256_crypt
from app.users import User

def register_pass(user: User, password):
    """Registers New Passowrd"""

    path = "app/static/database/users.csv"
    new_password = sha256_crypt.hash(str(password))
    username = user.username

    cols = ['Username', 'Password']
    data = DataFrame(pd.read_csv(path, usecols=cols))

    condition = data['Username'] == username # find user
    location = data.loc[condition] # find data location
    data.loc[location.index] = user.username, new_password # reset data at location
    data.to_csv(path, columns=cols, index=False, line_terminator="\n") # overwrite

def register_user(username, password):
    """Registers User to Database(static/database/users.csv)"""

    hash_pass = sha256_crypt.hash(str(password))
    sha256_crypt.verify(password, hash_pass)

    user = [
        str(username).lower(),
        hash_pass
    ]

    try:
        with open('app/static/database/users.csv', 'a', newline='') as csvfile:
            csv_writer = writer(csvfile, lineterminator="\n")
            csv_writer.writerow(user)
    except FileExistsError:
        print('File not found: users.csv')
