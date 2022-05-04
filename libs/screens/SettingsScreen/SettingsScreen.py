from re import L
import webbrowser

from kivy.core.clipboard import Clipboard
from kivy.factory import Factory
from kivy.clock import Clock
from kivymd .toast import toast
from kivymd.uix.screen import MDScreen
from libs.utils import remove_user_data
from kivymd.app import MDApp
from libs.modules.dialogs import AKAlertDialog

app = MDApp.get_running_app()


class SettingsScreen(MDScreen):
    content = None
    YOUTUBE_VIDEO_LINK = ""
    GITHUB_REPO_LINK = "https://github.com/AM-ash-OR-AM-I/Passlock"

    def logout(self):
        app.root.load_screen("SignupScreen", empty_history=True)
        app.root.SignupScreen.on_enter = lambda *args: Clock.schedule_once(
            lambda x: app.animate_signup(app.root.SignupScreen.ids.box), 0
        )
        remove_user_data()

    def change_colors(self):
        app.primary_palette = "DeepOrange" if app.theme_cls.primary_palette == "Blue" else "Blue"
        app.set_theme_style() # Update theme style
    
    def open_about(self):
        if self.content is None:
            self.content = Factory.AboutClass()
            self.about_dialog = AKAlertDialog(header_icon='heart-circle')
            self.about_dialog.size_portrait = ['300dp', '380dp']
            self.about_dialog.content_cls = self.content
        self.about_dialog.bg_color = app.primary_accent
        self.about_dialog.open()

    def open_web(self, github=False, youtube=False, email=False):
        if github:
            webbrowser.open(self.GITHUB_REPO_LINK)
            toast('Star my repository if you like it :)')
        elif youtube:
            webbrowser.open(self.YOUTUBE_VIDEO_LINK)
        elif email:
            webbrowser.open('https://mail.google.com/mail/u/0/#inbox?compose=new')
            Clipboard.copy('ashutoshmaha2909@gmail.com')
            toast('Email address Copied, Paste Email address to send email.')
    
    def open_youtube_demo(self):
        if self.YOUTUBE_VIDEO_LINK:
            webbrowser.open(self.YOUTUBE_VIDEO_LINK)
