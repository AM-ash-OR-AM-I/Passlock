from kivy.core.clipboard import Clipboard
from kivy.properties import ListProperty

from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

app = MDApp.get_running_app()


class FindScreen(MDScreen):
    rv_data = ListProperty()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.set_list()

    def set_list(self):
        def add_list(n):
            text_to_copy = "Demo text"
            self.rv_data.append(
                {
                    "viewclass": "List",
                    "primary_text": f"Google{n}",
                    "button_actions": {
                        "copy": lambda: exec(
                            f'Clipboard.copy("{text_to_copy}"); toast("Item copied")',
                            {"Clipboard": Clipboard, "toast": toast}),
                        "update": lambda: exec("MDApp.get_running_app().open_update_dialog()"),
                        "delete": lambda: toast("Item deleted")
                    },
                }
            )

        for i in range(20):
            add_list(i)


class HomeScreen(MDScreen):
    pass
