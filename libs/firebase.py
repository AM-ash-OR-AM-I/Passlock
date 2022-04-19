from kivy.network.urlrequest import UrlRequest
import json


class Firebase:
    SIGNUP_URL = (
        "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key="
    )
    LOGIN_URL = (
        "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key="
    )
    DELETE_URL = (
        "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key="
    )

    WEB_API_KEY = "AIzaSyCmgWZzNrBiKoc1NdrQ3p4rpYE23zm9YIA"

    def signup_success(self, req, result):
        """
        Implement this method to handle the result of the successful signup request.
        Similarly to handle successful login, `login_success` method should be implemented.
        """
    
    def signup_failure(self, req, result):
        """
        Implement this method to handle the result of the signup failure request.
        Similarly to handle login failure, `login_failure` method should be implemented.
        """

    def signup(self, name, password):
        url = self.SIGNUP_URL + self.WEB_API_KEY
        data = json.dumps(
            {"email": name, "password": password, "returnSecureToken": True}
        )
        UrlRequest(
            url,
            req_body=data,
            on_success=self.signup_success,
            on_failure=self.signup_failure,
        )

    def login(self, name, password):

        url = self.LOGIN_URL + self.WEB_API_KEY
        data = json.dumps(
            {"email": name, "password": password, "returnSecureToken": True}
        )
        UrlRequest(
            url,
            req_body=data,
            on_success=self.login_success,
            on_failure=self.login_failure,
        )

