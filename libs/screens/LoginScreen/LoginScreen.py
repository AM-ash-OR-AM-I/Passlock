from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading
from time import time
from kivy.clock import mainthread
from kivy.factory import Factory
app = MDApp.get_running_app()


class LoginScreen(MDScreen):
    loading_view =  None
    def __init__(self, **kw):
        super().__init__(**kw)
        self.loading_view = Factory.LoadingScreen()

    def login_button_pressed(self, password):
        @mainthread
        def load_home(*args):
            app.root.load_screen('HomeScreen', set_current = False)

        @mainthread
        def dismiss_spinner(*args):
            self.loading_view.dismiss()
            if self.load:
                app.root.load_screen('HomeScreen')

        def initialise_encryption():
            i = time()
            from libs.Backend import Encryption
            load_home()
            try:
                self.load = True
                if app.fps: 
                    app.fps_monitor_start()
                app.encryption_class = Encryption(password)
                app.passwords = app.encryption_class.load_decrypted()
                dismiss_spinner()
                encrypted_pass = app.encryption_class.load_passwords()
                for keys in encrypted_pass:
                    app.encrypted_keys[app.encryption_class.decrypt(keys)] = keys
                # app.root.HomeScreen.ids.create.ids.tab.switch_tab("[b]MANUAL")
            except UnicodeDecodeError:
                self.load = False
                dismiss_spinner()
                toast('Invalid password')
            print(f"Time taken to load passwords = {time()-i}")
            

        self.loading_view.open()
        initialise_encryption()
        
        
