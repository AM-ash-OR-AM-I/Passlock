import threading
from functools import partial

from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.uix.tab import MDTabsBase
from kivy.factory import Factory
from kivy.properties import ListProperty
from kivy.core.window import Window

from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.material_resources import dp

from libs.screens.classes import Dialog, DialogButton, RoundIconButton, CustomSnackbar, SyncWidget
from libs.utils import auto_password

app = MDApp.get_running_app()


class FindScreen(MDScreen):
    """
    FindScreen inside the HomeScreen.
    """

    rv_data = ListProperty()
    update_dialog = None
    snackbar = None
    snackbar_duration = 2.5
    delete_dialog = None

    def show_all_passwords(self):
        self.ids.find_label.opacity = 0
        if self.rv_data:
            self.rv_data = []
        for name, password in app.passwords.items():
            self.append_item(name, password)

    def append_item(self, name, password):
        self.rv_data.append(
            {
                "class": "List",
                "name": name,
                "password": password,
                "is_deleted": False,
                "button_actions": {
                    "copy": lambda: app.show_toast_copied(password),
                    "update": lambda: self.open_update_dialog(name),
                    "delete": partial(self.delete_item, name),
                },
            }
        )

    def find_password(self, text, from_update = False):
        """
        Gets executed when text is entered in search bar.
        """
        if not text:
            self.rv_data = []
            self.ids.find_label.text = "Type to search"
            self.ids.find_label.opacity = 0.5
        else:
            if not from_update:
                self.ids.box.clear_selection()

            def find_password_thread(text):
                self.find_dictionary = app.encryption_class.find_key(
                    app.passwords, text
                )
                if self.find_dictionary:
                    self.ids.find_label.opacity = 0
                else:
                    self.ids.find_label.opacity = 0.5
                    self.ids.find_label.text = "No results found :("
                self.rv_data = []
                for ((name, password), value) in self.find_dictionary:
                    self.append_item(name, password)

            threading.Thread(
                target=find_password_thread, args=(text,), daemon=True
            ).start()

    def update_password(self) -> None:
        name = self.update_content.ids.name.text
        password = self.update_content.ids.password.text
        def update_thread():
            try:
                if name == self.original_name:
                    app.passwords[name] = password
                    app.encryption_class.update(app.encrypted_keys[name], password)
                else:
                    del app.passwords[self.original_name]
                    app.encryption_class.delete(app.encrypted_keys[self.original_name])
                    app.passwords[name] = password
                    app.encryption_class.add(name, password)
                self.find_password(name,from_update=True)
            except KeyError as e:
                print(f"KeyError, occured while updating password. {e}")

        threading.Thread(target=update_thread, daemon=True).start()
        self.update_dialog.dismiss()
        toast(text=f"{name} is updated")

    def open_update_dialog(self, original_name):
        self.original_name = original_name
        if not self.update_dialog:
            self.update_content = Factory.UpdateContent()
            self.update_dialog = Dialog(
                title="Update",
                type="custom",
                content_cls=self.update_content,
                pos_hint={"center_y": 0.6},
                buttons=[
                    DialogButton(
                        text="Cancel", on_release=lambda x: self.update_dialog.dismiss()
                    ),
                    RoundIconButton(
                        text="Update",
                        icon="update",
                        on_release=lambda x: self.update_password(),
                    ),
                ],
            )
        self.update_content.ids.name.text = original_name
        self.update_content.ids.password.text = app.passwords[original_name]
        self.update_dialog.open()

    def delete_from_storage(self, name, dt):
        """
        Deletes the password from the file permanently.
        """

        def remove_permanently(encrypted_key):
            app.encryption_class.delete(encrypted_key)
            toast("Removed Password from storage")

        if self.delete_permanently:
            del app.passwords[name]
            if name in app.encrypted_keys:
                encrypted_key = app.encrypted_keys[name]
                threading.Thread(
                    target=remove_permanently, args=(encrypted_key,), daemon=True
                ).start()

    def delete_item(self, name):
        self.delete_permanently = True

        def undo_delete(index, item):
            self.delete_permanently = False
            self.rv_data.insert(index, item)
            self.snackbar.dismiss()

        data = self.rv_data
        for index, item in enumerate(data):
            if item["name"] == name:
                self.rv_data.remove(item)
                break

        Clock.schedule_once(lambda x: self.ids.box.clear_selection())
        if self.snackbar is None:
            self.snackbar = CustomSnackbar(
                text=f"{name} is deleted",
                buttons=[
                    DialogButton(
                        text="UNDO",
                        pos_hint={"center_y": 0.5},
                        on_release=lambda x: undo_delete(index, item),
                    )
                ],
            )
        else:
            self.snackbar.text = f"{name} is deleted"

        self.snackbar.duration = self.snackbar_duration
        self.snackbar.open()
        Clock.schedule_once(
            partial(self.delete_from_storage, name), self.snackbar_duration + .1
        )


class Auto(ScrollView, MDTabsBase):
    use_ascii = True
    use_digits = True
    use_special_chars = True
    password_length = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initial_random = auto_password(10, True, True, True)

    def set_length(self, length):
        self.password_length = length
        self.generate_password(True, True, True)

    def generate_password(self, ascii=None, digits=None, special_chars=None) -> None:
        if ascii is not None:
            self.use_ascii = ascii
        if digits is not None:
            self.use_digits = digits
        if special_chars is not None:
            self.use_special_chars = special_chars
        self.ids.password_field.text = auto_password(
            len=self.password_length,
            ascii=self.use_ascii,
            digits=self.use_digits,
            special_chars=self.use_special_chars,
        )


class HomeScreen(MDScreen):
    """
    It contains 2 screens:\n
    * CreateScreen\n
    * FindScreen
    """

    sync_widget = None
    sync_dialog = None
    
    def on_enter(self, *args):
        Window.softinput_mode = "below_target"
    
    def get_sync_widget(self):
        if self.sync_widget is None:
            self.sync_widget = SyncWidget(pos_hint={"center_x":.8,"center_y":.1})
            self.add_widget(self.sync_widget)
        return self.sync_widget

    def open_sync_dialog(self):
        if not self.sync_dialog:
            self.sync_dialog = Dialog(
                title="Sync",
                text="Do you want to backup or restore passwords from cloud?",
                buttons=[
                    RoundIconButton(
                        text="Backup",
                        icon="cloud-upload",
                        on_release=lambda x: self.backup(),
                    ),
                    RoundIconButton(
                        text="Restore",
                        icon="cloud-download",
                        on_release=lambda x: self.restore(),
                    ),
                ],
            )
        self.sync_dialog.open()

    def backup(self):
        self.sync_dialog.dismiss()
        self.sync_widget = self.get_sync_widget()
        app.backup(self.sync_widget)

    def restore(self, user_id = None):
        if self.sync_dialog:
            self.sync_dialog.dismiss()
        self.sync_widget = self.get_sync_widget()
        app.restore(self.sync_widget, user_id)

    def create_password(self, name, password):
        threading.Thread(
            target=app.encryption_class.add,
            args=(name, password),
            daemon=True,
        ).start()
        # Updates passwords dictionary.
        app.passwords[name] = password
        toast("Password Created Successfully.")
