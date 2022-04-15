from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading

app = MDApp.get_running_app()

class LoginScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        def load_backend():
            from libs.Backend import Encryption
            self.encryption = Encryption
        threading.Thread(target=load_backend).start()

    def login_button_pressed(self, email, password):
        def initialise_encryption():
            try:
                if app.fps: 
                    app.fps_monitor_start()
                app.encryption_class = self.encryption(password)
                app.passwords = app.encryption_class.load_decrypted()
                encrypted_pass = app.encryption_class.load_passwords()
                app.root.load_screen('HomeScreen')
                app.root.HomeScreen.ids.create.ids.tab.switch_tab("[b]MANUAL")
                for keys in encrypted_pass:
                    app.encrypted_keys[app.encryption_class.decrypt(keys)] = keys
            except UnicodeDecodeError:
                toast('Invalid password')
        
        threading.Thread(target=initialise_encryption, daemon=True).start()
        
