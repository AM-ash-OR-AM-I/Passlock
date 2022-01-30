from kivy.factory import Factory
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.uix.dialog import MDDialog

Dialog = """
<UpdateDialog@MDBoxLayout>
	size_hint_y:None
	height:"120dp"
	orientation:"vertical"
	spacing:"10dp"
	MDTextField:
		hint_text:"Enter new name"
	MDTextField:
		hint_text:"Enter new password"
		
MDScreen:
	
	MDRaisedButton:
		pos_hint:{"center_y":.5,"center_x":.5}
		text:"hi"
		on_release:
			app.open_dialog()
"""


class TestApp(MDApp):
	content_cls = None
	dialog = None

	def build(self):
		return Builder.load_string(Dialog)

	def open_dialog(self):
		if not self.content_cls:
			self.content_cls = Factory.UpdateDialog()
		if not self.dialog:
			self.dialog = MDDialog(title='Update Password', type="custom", radius=[dp(30), dp(30), dp(30), dp(30)],
								   content_cls=self.content_cls)
		self.dialog.open()


TestApp().run()
