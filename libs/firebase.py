from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
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

    AUTH_KEY = "VHwmUVXGQpfiNlgn4WCXgxDtc0ivne4N4DjXLCg1"  # Check in the setting/service accounts of project

    DATABASE_URL = "https://password-manager-aea5d-default-rtdb.firebaseio.com"

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

    def backup():
        """
        Used to backup the user's passwords.
        """

    def restore_success(self, req, result):
        """
        Override this method to handle the result of the successful restore request.
        """
        Logger.warn("Firebase: Restore success not implemented")

    def restore_failure(self, req, result):
        """
        Override this method to handle the result of the failure in restore request.
        """
        Logger.warn("Firebase: Restore failure not implemented")

    def restore(self, email = None):
        """
        Used to restore the user's passwords.
        """
        if email is None:
            with open("data/email.txt", "r") as f:
                email = f.read()
        email = email.replace(".", "-")
        UrlRequest(
            f"{self.DATABASE_URL}{email}/passwords.json?auth={self.AUTH_KEY}",
            on_success=self.restore_success,
            on_failure=self.restore_failure,
            on_error=self.restore_failure
        )