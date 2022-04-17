from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading
from time import time
from kivy.clock import Clock, mainthread
from kivy.factory import Factory
app = MDApp.get_running_app()


class LoginScreen(MDScreen):
    spinner =  None
    def __init__(self, **kw):
        super().__init__(**kw)
        self.spinner = Factory.LoadingSpinner()

    def login_button_pressed(self, email, password):
        @mainthread
        def load_home(*args)
            app.root.load_screen('HomeScreen', set_current = False)
            
        @mainthread
        def dismiss_spinner(*args):
            print("dismissed")
            self.spinner.dismiss()
            if self.load:
                app.root.load_screen('HomeScreen')

        def initialise_encryption():
            i = time()
            from libs.Backend import Encryption
            load_home()
            self.load = True
            try:
                if app.fps: 
                    app.fps_monitor_start()
                app.encryption_class = Encryption(password)
                app.passwords = app.encryption_class.load_decrypted()
                encrypted_pass = app.encryption_class.load_passwords()
                for keys in encrypted_pass:
                    app.encrypted_keys[app.encryption_class.decrypt(keys)] = keys
                # app.root.HomeScreen.ids.create.ids.tab.switch_tab("[b]MANUAL")
            except Exception as e:
                self.load = False
                toast('Invalid password')
                print(e)
            print(f"Time taken to load passwords = {time()-i}")
            dismiss_spinner()

        self.spinner.open()
        threading.Thread(target=initialise_encryption, daemon=True).start()
        
        
