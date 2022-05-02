from typing import Dict
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading
from time import time
from kivy.properties import BooleanProperty
from kivy.factory import Factory

from libs.firebase import Firebase
from libs.screens.classes import SyncWidget

app = MDApp.get_running_app()


class SignupScreen(MDScreen):
    loading_view = None
    show_signup = BooleanProperty(True)
    encryption = None

    def on_show_signup(self, *args):
        """Animation to be shown when clicking on login or signup"""

        print("switch_signup")
        box = self.ids.box
        box.pos_hint = {"top": 0.8}
        box.opacity = 0
        app.animate_signup(box)

    def save_uid_password(self, uid):
        """
        Saves user_id and a file that has been encrypted with master password.
        This makes sure that even when user hasn't created any passwords,
        app can still verify the password.
        """

        with open("data/user_id.txt", "w") as f:
            f.write(uid)
        with open("data/encrypted_file.txt", "w") as f:
            f.write(app.encryption_class.encrypt("Test"))

    def dismiss_loading(self, *args):
        app.root.load_screen("HomeScreen")
        self.loading_view.dismiss()

    def signup(self, email, password):
        def signup_success(req, result):
            user_id = result["localId"]
            toast("Signup successful")
            app.encryption_class = self.encryption(self.password)
            self.dismiss_loading()
            threading.Thread(target=self.save_uid_password, args=(user_id,)).start()

        def signup_failure(req, result):
            print(result["error"]["message"])
            toast(result["error"]["message"])
            self.loading_view.dismiss()

        self.firebase.signup_success = lambda req, result: signup_success(req, result)
        self.firebase.signup_failure = lambda req, result: signup_failure(req, result)
        self.firebase.signup(email, password)
        app.root.load_screen("HomeScreen", set_current=False)

    def login(self, email, password):
        def login_success(req, result):
            user_id = result["localId"]
            toast("Login successful")
            self.dismiss_loading()
            app.encryption_class = self.encryption(self.password)
            app.root.HomeScreen.restore(user_id = user_id)
            threading.Thread(target=self.save_uid_password, args=(user_id,)).start()

        def login_failure(req, result):
            print(result["error"]["message"])
            toast(result["error"]["message"])
            self.loading_view.dismiss()

        self.firebase.login_success = lambda req, result: login_success(req, result)
        self.firebase.login_failure = lambda req, result: login_failure(req, result)
        self.firebase.login(email, password)
        app.root.load_screen("HomeScreen", set_current=False)

    def restore(self, user_id):
        """
        Restore user's passwords from Database.
        """

        def restore_success(req, result):
            from libs.utils import write_passwords

            if result:
                write_passwords(result)
                app.passwords = app.encryption_class.load_decrypted()
                toast("Restored successfully")
            else:
                toast("No passwords to restore")
            

        def restore_failure(req, result):
            print(result)
            toast("Restore failed")
            

        self.firebase.restore_success = lambda req, result: restore_success(req, result)
        self.firebase.restore_failure = lambda req, result: restore_failure(req, result)
        self.firebase.restore(user_id)

    def button_pressed(self, email, password):
        def import_encryption():
            from libs.encryption import Encryption
            self.encryption = Encryption
            if not self.show_signup:
                self.login(email, password)

        self.email = email
        self.password = password
        self.firebase = Firebase()

        if self.loading_view is None:
            self.loading_view = Factory.LoadingScreen()
            self.loading_view.text = (
                "Signing up..." if self.show_signup else "Logging in..."
            )
        self.loading_view.open()
        self.loading_view.on_open = lambda *args: import_encryption()
        if self.show_signup:
            self.signup(email, password)
