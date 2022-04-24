from re import I
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from libs.utils import remove_user_data
from kivymd.app import MDApp

app = MDApp.get_running_app()


class SettingsScreen(MDScreen):
    def logout(self):
        app.root.load_screen("SignupScreen", empty_history=True)
        app.root.SignupScreen.on_enter = lambda *args: Clock.schedule_once(
            lambda x: app.animate_signup(app.root.SignupScreen.ids.box), 0
        )
        remove_user_data()
