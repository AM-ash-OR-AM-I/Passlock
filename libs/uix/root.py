import json

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.app import MDApp


class Root(ScreenManager):

    history = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self._handle_keyboard)
        self.transition = CardTransition(duration=.3)
        # getting screens data from screens.json
        with open("screens.json") as f:
            self.screens_data = json.load(f)

    def set_current(self, screen_name, side="left", _from_goback=False):
        # checks that the screen already added to the screen-manager
        if not self.has_screen(screen_name):
            screen = self.screens_data[screen_name]
            # loads the kv file
            Builder.load_file(screen["kv"])
            # imports the screen class dynamically
            exec(screen["import"])
            # calls the screen class to get the instance of it
            screen_object = eval(screen["object"])
            # automatically sets the screen name using the arg that passed in set_current
            screen_object.name = screen_name
            # finnaly adds the screen to the screen-manager
            self.add_widget(screen_object)

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
