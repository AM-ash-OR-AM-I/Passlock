from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading
from kivy.clock import Clock, mainthread
from kivy.factory import Factory
app = MDApp.get_running_app()


class LoginScreen(MDScreen):
    spinner =  None

    def login_button_pressed(self, email, password):
        @mainthread
        def dismiss_spinner(*args):
            print("dismissed")
            self.spinner.dismiss()
            if self.load:
                app.root.load_screen('HomeScreen')

        def initialise_encryption():
            from libs.Backend import Encryption
            self.load = True
            dismiss_spinner()
            try:
                
                
                if app.fps: 
                    app.fps_monitor_start()
                app.encryption_class = Encryption(password)
                app.passwords = app.encryption_class.load_decrypted()
                encrypted_pass = app.encryption_class.load_passwords()
                for keys in encrypted_pass:
                    app.encrypted_keys[app.encryption_class.decrypt(keys)] = keys
                # load_homescreen()
                # app.root.HomeScreen.ids.create.ids.tab.switch_tab("[b]MANUAL")
            except Exception as e:
                self.load = False
                toast('Invalid password')
                print(e)
            
            
            
        if self.spinner is None:
            self.spinner = Factory.LoadingSpinner()

        self.spinner.open()
        threading.Thread(target=initialise_encryption, daemon=True).start()
        
