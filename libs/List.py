from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, get_color_from_hex, ColorProperty, ListProperty, \
	DictProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout

KV = '''
<List>
	orientation:'vertical'
	size_hint_y:None
	padding: dp(28),dp(0),dp(10),dp(15)
	size_hint_x:1
	spacing:'6dp'
	height:'90dp' if self.selected else "56dp"
	elevation:0
	radius:'28dp'
	disable: True
	md_bg_color:self.list_color_active if self.selected else app.theme_cls.primary_light[:-1] + [0]
	MDLabel:
		adaptive_height: True
		text:root.primary_text
	MDBoxLayout:
		id: sec_box
		size_hint_y:None
		height:root.selected*dp(30) 
		opacity: root.selected*1
		MDLabel:
			adaptive_height:True
			text:root.secondary_text
			theme_text_color:'Secondary'
		MDIconButton:
			id: copy_button
			disabled: not root.selected
			md_bg_color_disabled:[0,0,0,0]
			icon:'content-copy'
			pos_hint:{'center_y':.5}
		MDIconButton:
			id: update_button
			disabled: not root.selected
			md_bg_color_disabled:[0,0,0,0]
			icon:'pencil-outline'
			pos_hint:{'center_y':.5} 
			# text_color:[.3,.3,.3,1]
		MDIconButton:
			id: delete_button
			disabled: not root.selected
			md_bg_color_disabled:[0,0,0,0]
			icon:'trash-can-outline'
			pos_hint:{'center_y':.5}

'''


class List(RectangularRippleBehavior, RecycleDataViewBehavior, ThemableBehavior, ButtonBehavior, MDBoxLayout):
	# ThemableBehavior, ButtonBehavior, MDBoxLayout or MDCard
	Builder.load_string(KV)
	selected = BooleanProperty(False)
	primary_text = StringProperty('Google')
	_no_ripple_effect = True
	ripple_alpha = .1
	secondary_text = StringProperty("12345678910111213")
	list_color_active = ColorProperty()
	button_actions = DictProperty()

	def on_button_actions(self,*args):
		if len(self.button_actions)==3:
			self.ids.copy_button.on_release = self.button_actions["copy"]
			self.ids.update_button.on_release = self.button_actions["update"]
			self.ids.delete_button.on_release = self.button_actions["delete"]

	def on_release(self):
		if self.selected:
			if self.right - self.last_touch.x >= dp(170):
				self.selected = False
				self.parent.clear_selection()
		else:
			self.parent.select_with_touch(self.index, None)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		# Logger.info(msg="Info: Refreshed")
		return super().refresh_view_attrs(rv, index, data)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		rv.data[index]["selected"] = is_selected

	def on_selected(self, instance, selected):
		if selected:
			self.list_color_active = self.theme_cls.primary_light[:-1] + [0]
			Animation(list_color_active=self.theme_cls.primary_light[:-1] + [.3], d=.1).start(self)
# self.Li


if __name__ == '__main__':
	class CardBehavior(MDApp):
		def on_start(self):
			self.bg_color_dark = get_color_from_hex('262626')
			# self.theme_cls.theme_style='Dark'
			self.fps_monitor_start()

		def build(self):
			return Builder.load_string("""
MDScreen:
	md_bg_color:[.8,.8,.8,1]
	# RecycleView:
	MDBoxLayout:
		pos_hint:{'top':0.8}
		adaptive_height: True
		# size_hint_y:.7
		# height:'100dp'
		orientation:'vertical'
		# OneLineListItem:
		#     text:'Hi'
		List:
		List:
		List:
		List:
		# OneLineListItem:
		#     text:'Hi'
		# OneLineListItem:
		#     text:'Hi'
		# OneLineListItem:
		#     text:'Hi'
		# OneLineListItem:
		#     text:'Hi'
		List:
		# OneLineListItem:
		#     text:'Hi'
		
			
			""")


	CardBehavior().run()
