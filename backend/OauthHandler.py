from google.oauth2 import id_token
from google.auth.transport import requests as greq
import facebook
from RegisterException import *
import requests
import const
import abc
import util
from User import User

class OauthException(Exception):
    def __init__(self, error):
        self._error = error
    def __str__(self):
        return self._error

class OauthFactory():
    @staticmethod
    def getHandler(provider, token):
        try:
            if provider == const.GOOGLE:
                return GoogleOauthHandler(token)
            elif provider == const.FACEBOOK:
                return FacebookOauthHandler(token)
            else:
                raise OauthException('No Oauth Provider: {}'.format(provider))
        except Exception as e:
            raise e

class OauthHandler:
    def __init__(self, provider, token):
        self._provider = provider
        self._token = token
        self._user_info = self.getUserInfo(self._token)

    @abc.abstractmethod
    def getUserInfo(self, token):
        raise NotImplementedError()

    @abc.abstractmethod
    def getUsername(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def getUserPassword(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def getUserEmail(self):
        raise NotImplementedError()

    def createUser(self):
        username = self.getUsername()
        password = self.getUserPassword()
        email = self.getUserEmail()
        user = User(username, password, email)  
        return user

    @property
    def username(self):
        return self.getUsername()

    @property
    def password(self):
        return self.getUserPassword()

    @property
    def email(self):
        return self.getUserEmail()

class FacebookOauthHandler(OauthHandler):

    def __init__(self, token):
        super().__init__(const.FACEBOOK, token)

    def getUserInfo(self, token):
        try:
            graph = facebook.GraphAPI(access_token=token)
            profile = graph.get_object('me')
            args = {'fields' : 'id,name,email'}
            return graph.get_object('me', **args)
        except Exception as e:
            raise OauthException(str(e))
    def getUsername(self):
        return self._user_info['name']

    def getUserPassword(self):
        return util.generatePassword(self._user_info['id']) 

    def getUserEmail(self):
        return self._user_info['email']

class GoogleOauthHandler(OauthHandler):

    def __init__(self, token):
        super().__init__(const.GOOGLE, token)

    def getUserInfo(self, token):
        try:
            id_info = id_token.verify_oauth2_token(
                token,
                greq.Request(),
                const.GOOGLE_APP_CLIENT_ID
            )

            # google account providers
            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            return id_info
        except ValueError as e:
            # Invalid token
            raise OauthException(str(e))

    def getUsername(self):
        return self._user_info['name']

    def getUserPassword(self):
        return util.generatePassword(self._user_info['email'])

    def getUserEmail(self):
        return self._user_info['email']
