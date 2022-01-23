from kivy import platform
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty, NumericProperty, get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, CardTransition, NoTransition

from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen

if platform != 'android':
	Window.size = (450, 900)
else:
	from JavaAPI import statusbar

KV = '''
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer
#: import Window kivy.core.window.Window
HotReloadViewer:
	path: app.path_to_live_ui
	errors: True
	errors_text_color: 0.5, 0.5, 0.5, 1
	errors_background_color: app.theme_cls.bg_dark
'''


class RoundButton(MDFillRoundFlatButton):
	padding = [0, dp(20), 0, dp(20)]
	_radius = dp(20), dp(20)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class TestCard(MDApp):
	dark_mode = BooleanProperty(False)
	screen_history = []
	LIVE_UI = 0
	fps = False
	path_to_live_ui = 'HomeScreenDesign.kv'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bg_color_dark = get_color_from_hex('262626')


	def build(self):
		Builder.load_file('LoginScreenDesign.kv')
		Builder.load_file('BottomNavigation.kv')
		if not self.LIVE_UI:
			# Builder.load_file('LoginScreenDesign.kv')
			Builder.load_file('HomeScreenDesign1.kv')
			Builder.load_file('Settings.kv')
		self.theme_cls.primary_palette = 'DeepOrange'
		# self.dark_mode = True
		self.sm = ScreenManager(transition=CardTransition())
		self.LoginScreen = LoginScreen(name='LoginScreen')
		self.HomeScreen = HomeScreen(name='HomeScreen')
		self.SettingScreen = SettingScreen(name='SettingScreen')
		self.FindScreen = FindScreen(name='FindScreen')
		self.sm.add_widget(self.LoginScreen)
		self.sm.add_widget(self.HomeScreen)
		self.sm.add_widget(self.SettingScreen)
		self.sm.add_widget(self.FindScreen)
		Window.bind(on_keyboard=self.go_back)
		return Builder.load_string(KV) if self.LIVE_UI else self.sm

	def back_button(self, home_screen=False, *args):
		if not home_screen:
			self.screen_history.pop()
		else:
			self.screen_history = ['HomeScreen']
		self.sm.transition.mode = 'pop'
		self.sm.transition.direction = 'right'
		self.sm.current = self.screen_history[-1]

	def go_back(self, instance, key, *args):
		if key in (27, 1001):
			if self.screen_history:
				self.screen_history.pop()
				if self.screen_history != []:
					self.sm.transition.mode = 'pop'
					self.sm.transition.direction = 'right'
					self.sm.current = self.screen_history[-1]

				else:
					self.exit_dialog = MDDialog(title='Exit', text='Do you want to exit?',
												buttons=[MDRaisedButton(text='YES', on_release=lambda x: self.stop()),
														 MDFlatButton(text='NO',
																	  on_release=lambda x: self.exit_dialog.dismiss())])
					self.exit_dialog.open()
					self.screen_history = ['HomeScreen']
			else:
				self.stop()
		return True

	def animation_behavior(self, instance):
		instance.opacity = 0
		instance.pos_hint = {'top': 1}
		# Animation(opacity=1, t='linear', d=.2).start(instance)
		Animation(opacity=1, d=.25, t='in_quad').start(instance)

	def change_screen(self, screen_name, *args):
		self.sm.transition.mode = 'push'
		self.sm.transition.direction = 'left'
		self.sm.current = screen_name
		self.screen_history.append(screen_name)
		print(f'{self.screen_history = }')

	def on_dark_mode(self, instance, mode):
		print(mode)
		# if self.start_call:
		#     self.set_mode()
		# else:
		self.anim = Animation(md_bg_color=self.theme_cls.opposite_bg_normal, duration=.3)
		color = get_color_from_hex(colors[self.theme_cls.primary_palette]["500"])
		Animation(md_bg_color=self.bg_color_dark if self.dark_mode else color, duration=.3).start(
			self.HomeScreen.ids.toolbar)
		Animation(background_color=self.bg_color_dark if self.dark_mode else color,
				  duration=.3).start(self.HomeScreen.ids.tab)

		self.anim.start(self.HomeScreen)
		# radius = 1.3 * max(Window.size)
		# self.HomeScreen.ids.circle_mode.opacity = 1
		# self.anim = Animation(rad=radius, duration=.6, t='in_quad')
		# self.anim.start(self.HomeScreen.ids.circle_mode)
		self.anim.on_complete = self.set_mode

	def set_mode(self, *args):
		print("mode set")
		if self.dark_mode:
			self.theme_cls.theme_style = 'Dark'
			self.theme_cls.primary_hue = '300'
			if platform == 'android':
				statusbar(status_color=colors["Dark"]["CardsDialogs"])
		else:
			self.theme_cls.theme_style = 'Light'
			self.theme_cls.primary_hue = '500'
			if platform == 'android':
				statusbar(status_color='ff7a4f')
		self.HomeScreen.ids.circle_mode.rad = 0.1

	def toggle_mode(self, *args):
		self.dark_mode = not self.dark_mode

	def activate_find(self, *args):
		self.sm.transition=NoTransition()
		self.sm.current='FindScreen'

	def on_start(self):
		# self.HomeScreen.ids.bottom_nav.ids.item.ids.create.active=True
		if platform == 'android':
			statusbar(status_color=colors["Dark"]["CardsDialogs"] if self.dark_mode else 'ff7a4f')

	# def on_stop(self):
	#     self.root.ids.box.export_to_png("gradient.png")


# class IconButton(MDIcon, ButtonBehavior, CircularRippleBehavior): pass


class RoundButton(MDFillRoundFlatButton):
	padding = [0, dp(20), 0, dp(20)]
	_radius = '20dp'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class LoginScreen(MDScreen): pass


class HomeScreen(MDScreen): pass


class FindScreen(MDScreen): pass


class LabelIcon(MDBoxLayout, ThemableBehavior):
	active = BooleanProperty(False)
	text_color = ColorProperty([1, 1, 1, 1])
	scale = NumericProperty(1)
	opac = BooleanProperty(False)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.text_color = self.theme_cls.primary_color if self.active else [.7, .7, .7, 1]
		self.primary_color = MDApp.get_running_app().theme_cls.primary_color

	def on_active(self, instance, active):
		# print(app.root.children)
		for instances in self.parent.children:
			# print(instances, instance)
			if instances != instance:
				instances.text_color = [.7, .7, .7, 1]
				instances.scale = 1
				instances.opac = 0
			else:
				instances.text_color = self.theme_cls.primary_color
				instances.opac = 1
				self.animate = Animation(scale=1.3, d=.15, t='linear')
				self.animate.start(instances)


# class Tab(MDBoxLayout, MDTabsBase):pass
class RoundedList(TwoLineListItem):
	active = BooleanProperty(False)

	def on_release(self):
		self.active = not self.active

	def on_active(self, instance, active):
		if self.active:
			self.secondary_text = 'Password'
			Animation(height=dp(80), d=.1).start(self)
		else:
			self.secondary_text = ''
			Animation(height=dp(50), d=.1).start(self)


class SettingScreen(MDScreen): pass


TestCard().run()
