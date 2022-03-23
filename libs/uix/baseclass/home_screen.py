from kivy.core.clipboard import Clipboard
from kivy.factory import Factory
from kivy.properties import ListProperty

from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from functools import partial

from libs.uix.classes import Dialog, DialogButton, RoundIconButton

app = MDApp.get_running_app()


class FindScreen(MDScreen):
    rv_data = ListProperty()
    update_dialog = None

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.set_list()

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

    def delete_item(self, text):
        toast("Item deleted")
        print(text)

    def set_list(self):

        def add_list(n):
            text = f"Password{n}"
            self.rv_data.append(
                {
                    "viewclass": "List",
                    "primary_text": f"{text}",
                    "button_actions": {
                        "copy": lambda: exec(
                            f'Clipboard.copy("{text}"); toast("Item copied")',
                            {"Clipboard": Clipboard, "toast": toast}),
                        "update": lambda: self.open_update_dialog(),
                        "delete": partial(self.delete_item, n)
                    },
                }
            )


        for i in range(20):
            add_list(i)


class HomeScreen(MDScreen):
    pass
