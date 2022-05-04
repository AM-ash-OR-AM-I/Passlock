from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import os.path
from time import time
from kivy.factory import Factory
from libs.screens.classes import SyncWidget
from libs.utils import *

app = MDApp.get_running_app()


class LoginScreen(MDScreen):
    loading_view = None
    sync_widget = None
    logged_in = False
    password = None

    def get_sync_widget(self):
        if self.sync_widget is None:
            self.sync_widget = SyncWidget(pos_hint={"center_x":.8,"center_y":.1})
            self.add_widget(self.sync_widget)
        return self.sync_widget

    def on_enter(self,*args):
        if app.auto_sync and not is_backup_failure():
            self.sync_widget = self.get_sync_widget()
            app.restore(self.sync_widget, decrypt = False)

    def login_button_pressed(self, password):
        
        def dismiss_spinner(*args):
            app.root.load_screen("HomeScreen")
            self.loading_view.dismiss()

        def initialise_encryption():
            i = time()
            from libs.encryption import Encryption

            try:
                if app.fps:
                    app.fps_monitor_start()
                app.encryption_class = Encryption(password)
                if os.path.exists("data/passwords"):
                    app.passwords = app.encryption_class.load_decrypted()
                else:
                    if os.path.exists("data/encrypted_file.txt"):
                        with open("data/encrypted_file.txt", "r") as f:
                            app.encryption_class.decrypt(f.read())
                    else:
                        print("'encrypted_file' not found, can't check password.")

                dismiss_spinner()
                if not self.password:
                    self.password = password
                # app.root.HomeScreen.ids.create.ids.tab.switch_tab("[b]MANUAL")
            except UnicodeDecodeError:
                self.loading_view.dismiss()
                toast("Invalid password")
            # print(app.encrypted_keys)
            print(f"Time taken to load passwords = {time()-i}")
        if not self.password:
            if self.loading_view is None:
                self.loading_view = Factory.LoadingScreen()
            self.loading_view.open()
            self.loading_view.on_open = lambda *args: initialise_encryption()
        else:
            if self.password == password:
                app.root.load_screen("HomeScreen")
            else:
                toast("Invalid password")