from kivy import platform
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty, BooleanProperty, NumericProperty, ListProperty, \
	get_color_from_hex
from kivy.uix.textinput import TextInput

from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout

if platform == 'android':
	from AndroidAPI import fix_back_button, keyboard_height

Builder.load_string('''

# kv_start
<CardTextField>
    height: '60dp'
    size_hint_y:None
    size_hint_x:.8
    radius: dp(30)
    set_elevation: 0
    label_name:'Hi there'
    md_bg_color: [1,1,1,1] if app.theme_cls.theme_style=='Light' else app.dark_color
    label_size:'15sp'
    hint_text:''
    adaptive_height:True
    spacing:'20dp'
    orientation:'vertical'
    start_anim: app.dark_mode
    
    MDLabel:
        text:root.label_name
        markup:True
        adaptive_height:True
        y:card.y+card.height+dp(10)
        x:card.x+dp(30)
        size_hint_x:0.8
        font_size:root.label_size
        font_name:'RobotoMedium'
    MDCard:
        id: card
        height: root.height
        size_hint_y: None
        radius: root.radius
        elevation: root.set_elevation
        md_bg_color:root.md_bg_color
        canvas:
            Color:
                rgba: root.border_color
            Line:
                width:root.thickness
                rounded_rectangle:
                    (self.x,self.y,self.width,self.height,self.radius[0])
    MDBoxLayout:
        id: card_box
        padding:(dp(20),0,0,0)if root.icon_left_action is None else (0,0,0,0)
        spacing:'5dp'
        TextInput:
            id: textfield
            size_hint_y:None
            hint_text:root.hint_text
            height: card.height
            background_color:[0,0,0,0]
            font_size:root.text_font_size
            padding:[0,(self.height-self.font_size)/2,0,dp(0)] if not root.icon_left_action\
             else [0,(self.height-self.font_size)/2,0,dp(6)]
            foreground_color: app.theme_cls.primary_dark if app.theme_cls.theme_style=='Light'\
             else app.theme_cls.primary_light
            hint_text_color: root.hint_text_color if root.hint_text_color is not None else [.5,.5,.5,.8]
            cursor_color: app.theme_cls.primary_color
            multiline: root.multiline
            text: root.text
            on_text:
                root.text = self.text
            on_focus:
                root.focus = self.focus
            y: card.y
            center_x: card.center_x
# kv_end
''')


class CardTextField(MDRelativeLayout, ThemableBehavior):
	inactive_color = ColorProperty([.5, .5, .5, .1])
	border_color = ColorProperty([.5, .5, .5, .1])
	active_color = [0, .7, 1, .7]
	focus = BooleanProperty(False)
	text_font_size = StringProperty('17sp')
	hint_text_color = ColorProperty(None)
	text = StringProperty('')
	thickness = NumericProperty(dp(1) if platform == 'android' else dp(1.4))
	hint_text = StringProperty('')
	label_size = StringProperty('20dp')
	label_name = StringProperty('')
	icon_left_action = ListProperty(None)
	multiline = BooleanProperty(False)
	icon_color = ColorProperty([.5, .5, .5, 1])
	icon_right_action = ListProperty(None)
	icon_font_size = NumericProperty()
	win = True if platform == 'win' else False
	start_anim = BooleanProperty(False)

	app = None
	c = 0

	def on_start_anim(self, instance, mode):
		self.anim = Animation(md_bg_color=get_color_from_hex(colors["Dark" if mode else "Light"]["CardsDialogs"]), d=.3)
		self.anim.start(instance)

	def on_icon_left_action(self, instance, icon_list: 'List containing icon name and function'):
		box = self.ids.card_box
		rm = 0
		for inst in box.children:
			if isinstance(inst, TextInput):
				rm = 1
			else:
				if rm:
					box.remove_widget(inst)
		# self.ids.card_box.remove_widget()
		if len(icon_list) and type(icon_list[0]) != list:
			if len(icon_list) == 1:
				self.icon_left = MDIconButton(icon=self.icon_left_action[0], theme_text_color='Custom',
											  text_color=self.icon_color, user_font_size=self.icon_font_size,
											  pos_hint={'center_y': .5})

			else:
				self.icon_left = MDIconButton(icon=self.icon_left_action[0], theme_text_color='Custom',
											  text_color=self.icon_color, user_font_size=self.icon_font_size,
											  pos_hint={'center_y': .5}, on_release=self.icon_left_action[1])
			self.ids.card_box.add_widget(self.icon_left, index=1)
		elif type(icon_list[0]) == list:
			for icons in icon_list:
				if len(icons) == 1:
					self.icon_left = MDIconButton(icon=icons[0], theme_text_color='Custom',
												  text_color=self.icon_color, user_font_size=self.icon_font_size,
												  pos_hint={'center_y': .5})

				else:
					self.icon_left = MDIconButton(icon=icons[0], theme_text_color='Custom',
												  text_color=self.icon_color, user_font_size=self.icon_font_size,
												  pos_hint={'center_y': .5}, on_release=icons[1])
				self.ids.card_box.add_widget(self.icon_left, index=1)

	def on_icon_right_action(self, instance, icon_list):
		if len(icon_list) and type(icon_list[0]) != list:
			if len(icon_list) == 1:
				self.icon_right = MDIconButton(icon=self.icon_right_action[0], theme_text_color='Custom',
											   text_color=self.icon_color, user_font_size=self.icon_font_size,
											   pos_hint={'center_y': .5})

			else:
				self.icon_right = MDIconButton(icon=self.icon_right_action[0], theme_text_color='Custom',
											   text_color=self.icon_color, user_font_size=self.icon_font_size,
											   pos_hint={'center_y': .5}, on_release=self.icon_right_action[1])
			self.ids.card_box.add_widget(self.icon_right)
		elif type(icon_list[0]) == list:
			for icons in icon_list:
				if len(icons) == 1:
					self.icon_right = MDIconButton(icon=icons[0], theme_text_color='Custom',
												   text_color=self.icon_color, user_font_size=self.icon_font_size,
												   pos_hint={'center_y': .5})

				else:
					self.icon_right = MDIconButton(icon=icons[0], theme_text_color='Custom',
												   text_color=self.icon_color, user_font_size=self.icon_font_size,
												   pos_hint={'center_y': .5}, on_release=icons[1])
				self.ids.card_box.add_widget(self.icon_right)

	def on_icon_color(self, instance, color):
		if self.icon_left_action is not None:
			self.icon_left.text_color = color
		if self.icon_right_action is not None:
			self.icon_right.text_color = color

	def on_inactive_color(self, *args):
		self.border_color = self.inactive_color

	def on_text(self, instance, text):
		"""Use this to do what you want"""

	def on_focus(self, instance, focus):
		print('event:<on_focus> is_called')
		if self.app is None:
			self.app = MDApp.get_running_app()
		if platform == "android":
			if not focus:
				fix_back_button()

			def call(*args):
				if focus:
					if (height:=keyboard_height())>0:
						self.app.key_height = height
				else:
					self.app.key_height = 0
			Clock.schedule_once(call, .2)


		if focus:
			self.border_color = self.active_color
		else:
			self.border_color = self.inactive_color


if __name__ == '__main__':
	class TestCard(MDApp):
		def build(self):
			Window.size = (500, 900)
			return Builder.load_string('''
#:import window kivy.core.window.Window
#:set height window.height
#:set width window.width
#: set rad 250
#: set lbl_size '15sp'
#: set icon_size 60
#: set card_height '70dp'
#: set card_font_size '15sp'
#: import platform kivy.platform
#: import CardTextField CustomCard.CardTextField
#: import ListProperty kivy.properties.ListProperty
<FloatingButton@MDFloatingActionButton+FakeCircularElevationBehavior>

<LoginScreen@MDScreen>:
    canvas:
		Color:
			rgba:1,0.2,0,0.7
		Ellipse:
			size:rad,rad
			pos:0-rad/2,height-rad+20
			angle_start:0
			angle_end:180
		Color:
			rgba:1,0.8,0.65,0.7
		Ellipse:
			pos:0,height-rad/2
			size:rad,rad
			angle_start:90
			angle_end:270

	MDBoxLayout:
		adaptive_height:True
		orientation:'vertical'
		pos_hint:{'top':0.95}
		spacing:'50dp'
		MDLabel:
		    adaptive_height:True
            text:"LOGIN\\nTO [color=FF4400][u]PA[/u]SS"
            markup:True
            font_name:'RobotoMedium'
            halign:'center'
            font_size:'48dp'
            pos_hint:{'top':1}
        MDBoxLayout:
            adaptive_height:True
            spacing:'60dp'
            orientation:'vertical'
            CardTextField:
                hint_text:'username@mail.com'
                label_name:'Email Address'
                size_hint_x:.7
				pos_hint:{'center_x':.5}
				height:'80dp'
                icon_left_action:['account']
                icon_right_action:['chevron-down']
            CardTextField:
                hint_text:'Enter password'
                size_hint_x:.7
                label_name:'Password'
				pos_hint:{'center_x':.5}
				height:'80dp'
                icon_right_action:['eye-off-outline']
        MDTextButton:
            text:'Forgot Password?'
            font_name:'RobotoMedium'
            pos_hint:{'center_x':.5}
            theme_text_color:'Secondary'

		FloatingButton:
			elevation:10
			icon:'lock'
			user_font_size:100
			md_bg_color:[.25,.25,.25,1]
			theme_text_color:'Custom'
            text_color:[.9,0.4,0,1]
			pos_hint:{'center_x':.5}
	MDTextButton:
		text:'I\\'m a new user. [color=FF4400]Sign up!'
		markup:True
		pos_hint:{'center_y':.07,'center_x':.5}
		font_name:'RobotoMedium'
		halign:'center'
		font_size:lbl_size
LoginScreen:
            ''')


	TestCard().run()
