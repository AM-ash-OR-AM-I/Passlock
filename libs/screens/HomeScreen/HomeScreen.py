import string
import random

from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.factory import Factory
from kivy.properties import ListProperty

from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from functools import partial

from libs import Backend
from libs.screens.classes import Dialog, DialogButton, RoundIconButton, CustomSnackbar

app = MDApp.get_running_app()


class FindScreen(MDScreen):
    """
    FindScreen inside the HomeScreen.
    TODO: While backing up passwords encrypt the email address.
    """

    rv_data = ListProperty()
    update_dialog = None
    snackbar = None
    snackbar_duration = 2.5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        '''Replace demo passwords with the dictionary containing passwords.'''

        self.demo_passwords = {}
        for i in range(20):
            key = "".join(random.sample(string.ascii_letters, 8))
            self.demo_passwords[f"Hello{key}{i}hi"]=f"Password{i}"

        self.add_passwords()
        self.delete_dialog = None

    def add_passwords(self):
        """
        Used to add password lists to the RecycleView.
        """

        for name, password in self.demo_passwords.items():
            self.append_item(name, password)

    def append_item(self, name, password):
        self.rv_data.append(
            {
                "class": "List",
                "name": name,
                "password": password,
                "is_deleted": False,
                "button_actions": {
                    "copy": lambda: exec(
                        f'Clipboard.copy("{name}"); toast("Item copied")',
                        {"Clipboard": Clipboard, "toast": toast}),
                    "update": lambda: self.open_update_dialog(),
                    "delete": partial(self.delete_item, name),
                }
            }
        )

    def find_password(self, text):
        """
        Gets executed when text is entered in search bar.
        """
        self.find_dictionary = Backend.find_key(self.demo_passwords, text)
        print(self.find_dictionary)

        self.rv_data = []
        for name, password in self.find_dictionary:
            self.append_item(name, password)

    def open_update_dialog(self):
        if not self.update_dialog:
            update_content = Factory.UpdateContent()
            self.update_dialog = Dialog(
                title="Update", type="custom", content_cls=update_content, pos_hint={"center_y": .6},
                buttons=[
                    DialogButton(text="Cancel", on_release=lambda x: self.update_dialog.dismiss()),
                    RoundIconButton(text="Update", icon="update")
                ]
            )
        self.update_dialog.open()
    
    def delete_from_storage(self, name, dt):
        """
        Deletes the password from the file permanently.
        """

        if self.delete_permanently:
            print("delete_permanently")

    def delete_item(self, name):
        self.delete_permanently = True

        def undo_delete(index, item):
            self.delete_permanently = False
            self.rv_data.insert(index, item)
            self.snackbar.dismiss()

        data = self.rv_data
        for index, item in enumerate(data):
            if item["name"]==name:
                self.rv_data.remove(item)
                break

        Clock.schedule_once(lambda x: self.ids.box.clear_selection())
        self.snackbar = CustomSnackbar(
            text=f"{name} is deleted",
            buttons=[
                DialogButton(
                    text="UNDO", pos_hint={"center_y": .5},
                    on_release=lambda x: undo_delete(index, item)
                )
            ]
        )
        self.snackbar.duration = self.snackbar_duration
        self.snackbar.open()
        Clock.schedule_once(partial(self.delete_from_storage, name), self.snackbar_duration)


class HomeScreen(MDScreen):
    """
    It contains 2 screens:\n
    * CreateScreen\n
    * FindScreen
    """
