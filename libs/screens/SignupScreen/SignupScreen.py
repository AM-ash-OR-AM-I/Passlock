from typing import Dict
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading
from time import time
from kivy.properties import BooleanProperty
from kivy.factory import Factory

from libs.firebase import Firebase
app = MDApp.get_running_app()


class SignupScreen(MDScreen):
    loading_view = None
    show_signup = BooleanProperty(True)
    offline_only = BooleanProperty(False)

    def on_show_signup(self, *args):
        """Animation to be shown when clicking on login or signup"""

        print("switch_signup")
        box = self.ids.box
        box.pos_hint = {"top": 0.8}
        box.opacity = 0
        app.animate_login(box)
    
    def save_email_password(self, email):
        """
        Saves email and a file that has been encrypted with master password.
        This makes sure that even when user hasn't created any passwords,
        app can still verify the password.
        """

        with open("data/email.txt","w")as f:
            f.write(email)
        with open("data/encrypted_file.txt","w")as f:
            f.write(app.encryption_class.encrypt("Test"))
    
    def dismiss_loading(self, *args):
        app.root.load_screen('HomeScreen')
        self.loading_view.dismiss()
    
    def signup_failure(self, req, result):
        print(result["error"]["message"])
        toast(result["error"]["message"])
        self.loading_view.dismiss()
    
    def signup_success(self, req, result):
        toast("Signup successful")
        app.encryption_class = self.encryption(self.password)
        self.dismiss_loading()
        threading.Thread(target = self.save_email_password, args=(self.email,)).start()
        
    def signup(self, email, password):
        def import_encryption():
            from libs.Backend import Encryption
            self.encryption = Encryption
        
        self.email = email
        self.password = password
        firebse = Firebase()
        firebse.signup_success = lambda req, result: self.signup_success(req, result)
        firebse.signup_failure = lambda req, result: self.signup_failure(req, result)
        firebse.signup(email, password)
        if self.loading_view is None:
            self.loading_view = Factory.LoadingScreen()
            self.loading_view.text = "Signing up..."
        self.loading_view.open()
        self.loading_view.on_open = lambda *args: import_encryption()
    
    def login_success(self, req, result):
        toast("Login successful")
        app.encryption_class = self.encryption(self.password)
        #TODO: Restore backed up user passwords
        self.dismiss_loading()
        threading.Thread(target = self.save_email_password, args=(self.email,)).start()
    
    def login(self, email, password):
        def import_encryption():
            from libs.Backend import Encryption
            self.encryption = Encryption
        
        self.email = email
        self.password = password
        firebse = Firebase()
        firebse.login_success = lambda req, result: self.login_success(req, result)
        firebse.login_failure = lambda req, result: self.login_failure(req, result)
        firebse.login(email, password)
        if self.loading_view is None:
            self.loading_view = Factory.LoadingScreen()
            self.loading_view.text = "Logging in..."
        self.loading_view.open()
        self.loading_view.on_open = lambda *args: import_encryption()
    