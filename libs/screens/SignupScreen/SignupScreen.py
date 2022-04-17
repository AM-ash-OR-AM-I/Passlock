from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
import threading
from time import time
from kivy.clock import mainthread
from kivy.factory import Factory
from kivy.network.urlrequest import UrlRequest
app = MDApp.get_running_app()


class SignupScreen(MDScreen):
    def signup(self, email, password):
        ...