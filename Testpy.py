from kivy.lang import Builder
from kivymd.app import MDApp
KV="""
MDScreen:
    MDFloatingActionButton:
        pos_hint:{"center_x":.5,"center_y":.5}
"""


class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


TestApp().run()