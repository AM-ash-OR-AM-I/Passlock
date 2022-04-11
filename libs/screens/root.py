from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.app import MDApp
from kivy.logger import Logger
import os

class Root(ScreenManager):

    history = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self._handle_keyboard)
        self.transition = CardTransition(duration=.3)


    def set_current(self, screen_name, side="left", _from_goback=False):
        # checks that the screen already added to the screen-manager
        if not self.has_screen(screen_name):
            # loads the kv file
            Builder.load_file(f"libs/screens/{screen_name}/{screen_name}.kv")
            # imports the screen class dynamically
            exec(f"from libs.screens.{screen_name}.{screen_name} import {screen_name}")
            # calls the screen class to get the instance of it
            self.screen_object = eval(f"{screen_name}()")
            # automatically sets the screen name using the arg that passed in set_current
            self.screen_object.name = screen_name
            # saves screen instance object to access later.
            exec(f"self.{screen_name} = self.screen_object")
            # finnaly adds the screen to the screen-manager
            self.add_widget(self.screen_object)

        # saves screen information to history
        # if you not want a screen to go back
        # use like below
        # if not from_goback and screen_name not in ["auth", ...]

        if not _from_goback:
            self.transition.mode = 'push'
            self.transition.direction = 'left'
            self.history.append(screen_name)

        # sets transition direction
        # sets to the current screen
        self.current = screen_name

    def _handle_keyboard(self, instance, key, *args):
        if key == 27:
            if self.current=="HomeScreen" and self.current_screen.ids.tab_manager.current == 'FindScreen':
                self.current_screen.ids.tab_manager.current = "CreateScreen"
            elif self.current=="HomeScreen":
                MDApp.get_running_app().open_exit_dialog()
            else:
                self.goback()
            return True

    def goback(self):
        if len(self.history) > 1:
            self.history.pop()
            prev_screen = self.history[-1]
            self.transition.mode = 'pop'
            self.transition.direction = 'right'
            self.set_current(prev_screen, _from_goback=True)
