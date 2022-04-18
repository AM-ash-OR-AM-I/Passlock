from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading
from time import time
from kivy.clock import mainthread
from kivy.properties import BooleanProperty
from kivy.factory import Factory
from kivy.network.urlrequest import UrlRequest
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

    def signup(self, email, password):
        def dismiss_loading(*args):
            if self.load:
                app.root.load_screen('HomeScreen')
            self.loading_view.dismiss()

        def initialise_encryption():
            i = time()
            from libs.Backend import Encryption
            try:
                self.load = True
                if app.fps: 
                    app.fps_monitor_start()
                app.encryption_class = Encryption(password)
                app.passwords = app.encryption_class.load_decrypted()
                dismiss_loading()
                encrypted_pass = app.encryption_class.load_passwords()
                for keys in encrypted_pass:
                    app.encrypted_keys[app.encryption_class.decrypt(keys)] = keys
                # app.root.HomeScreen.ids.create.ids.tab.switch_tab("[b]MANUAL")
            except UnicodeDecodeError:
                self.load = False
                dismiss_loading()
                toast('Invalid password')
            threading.Thread(target = save_email_password, args=(email,)).start()
            print(f"Time taken to load passwords = {time()-i}")

        def save_email_password(email):
            with open("data/email.txt","w")as f:
                f.write(email)
            with open("data/encrypted_file.txt","w")as f:
                f.write(app.encryption_class.encrypt("Test"))

        if self.loading_view is None:
            self.loading_view = Factory.LoadingScreen()
            self.loading_view.text = "Signing up..."
        self.loading_view.open()
        self.loading_view.on_open = lambda *args: initialise_encryption()
    