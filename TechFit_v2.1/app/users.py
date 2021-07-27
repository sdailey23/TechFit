"""User Class"""

class User:
    """Contains User Name for 'Authorized' Pages"""
    username = 'unregistered'
    authorized = False
    updated = [False, '']

    def set_user(self, name: str):
        """Sets Username"""
        self.username = name

    def get_user(self):
        """Gets Username"""
        return self.username

    def authorize(self, auth: bool):
        """Sets Authorized Status"""
        self.authorized = auth

    def is_authorized(self):
        """Returns Authorization Status"""
        return self.authorized == True

    def update(self, message: str):
        self.updated = [True, message]

    def clear_update(self):
        self.updated = [False, '']

    def get_update(self):
        return self.updated[1]

    def is_updated(self):
        return self.updated[0] == True
