import json
import requests


class MasterAPI:
    """
    API for the following routes:
    /api/create-key
    /api/create-database
    /api/reset-database
    """
    def __init__(self, url):
        """ Constructor requires the user to input the master key """
        self.url = url  # should be url of local host or the live website
        self.master = input('Enter os.environ["MASTER_KEY"]: ')
        self.typical = json.dumps({'master': self.master})

    def create_database(self):
        """ Creates the database """
        r = requests.get(f'{self.url}/api/create-database', data=self.typical)
        return r.status_code, r.text

    def reset_database(self):
        """ Resets the database """
        r = requests.get(f'{self.url}/api/reset-database', data=self.typical)
        return r.status_code, r.text

    def create_key(self):
        """ Creates an API key for updating players and results """
        print('Create a key...')
        payload = json.dumps({
            'master': self.master,
            'username': input('username: '),
            'password': input('password: ')
        })
        r = requests.get(f'{self.url}/api/create-key', data=payload)
        return r.status_code, r.text


class KeyAPI:
    """
    API for the following routes:
    /api/update-players
    /api/update-results
    /api/update
    """
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.typical = json.dumps({
            'username': self.username,
            'password': self.password,
        })

    def update_players(self):
        """ Update players """
        r = requests.get(f'{self.url}/api/update-players', data=self.typical)
        return r.status_code, r.text

    def update_results(self):
        """ Update results """
        r = requests.get(f'{self.url}/api/update-results', data=self.typical)
        return r.status_code, r.text

    def update(self):
        """ Update results and players """
        r = requests.get(f'{self.url}/api/update', data=self.typical)
        return r.status_code, r.text


"""
# EXAMPLE
master = MasterAPI('http://127.0.0.1:5000')
print(master.reset_database())
print(master.create_database())
print(master.create_key())

key = KeyAPI('http://127.0.0.1:5000', 'username', 'password')
print(key.update_players())
"""
