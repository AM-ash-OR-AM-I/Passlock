from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading
from kivy.clock import mainthread
from kivy.factory import Factory
app = MDApp.get_running_app()


class LoginScreen(MDScreen):
    spinner =  None
    @mainthread
    def dismiss_spinner(self):
        self.spinner.dismiss()
    
    @mainthread
    def load_homescreen(self):
        app.root.load_screen('HomeScreen')

    def login_button_pressed(self, email, password):
        def initialise_encryption():
            from libs.Backend import Encryption
            try:
                if app.fps: 
                    app.fps_monitor_start()
                app.encryption_class = Encryption(password)
                app.passwords = app.encryption_class.load_decrypted()
                encrypted_pass = app.encryption_class.load_passwords()
                for keys in encrypted_pass:
                    app.encrypted_keys[app.encryption_class.decrypt(keys)] = keys
                self.load_homescreen()
                # app.root.HomeScreen.ids.create.ids.tab.switch_tab("[b]MANUAL")
            except UnicodeDecodeError:
                toast('Invalid password')
            self.dismiss_spinner()
            
            
        if self.spinner is None:
            self.spinner = Factory.LoadingSpinner()

        self.spinner.open()
        threading.Thread(target=initialise_encryption, daemon=True).start()
        
