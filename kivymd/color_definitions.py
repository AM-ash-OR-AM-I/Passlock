from kivy.properties import get_color_from_hex

'''
Method to create light colors...

dict={}
    col = get_color_from_hex('FF004C')
    col1=get_color_from_hex('296DFF')
    col2=get_color_from_hex('A200FF')
    col3 = get_color_from_hex('FF5722')
    col[3],col1[3],col[3],col3[3] = 0.2,0.3,0.3,0.3
    dict['Pink'],dict['Blue'],dict['DeepPurple'],dict['DeepOrange']=col,col1,col2,col3
    
'''

dark_colors={'Pink': [0.6313725490196078, 0.00784313725490196, 0.19215686274509805, 1.0], 'DeepPurple': [0.3607843137254902, 0.0, 0.5686274509803921, 1.0], 'Blue': [0.10980392156862745, 0.27058823529411763, 0.6196078431372549, 1.0], 'DeepOrange': [0.6784313725490196, 0.23921568627450981, 0.10196078431372549, 1.0]}
custom_light_color={'Red': [0.9568627450980393, 0.2627450980392157, 0.21176470588235294, 0.25], 'Pink': [1.0, 0.0, 0.2980392156862745, 0.25], 'Purple': [0.611764705882353, 0.15294117647058825, 0.6901960784313725, 0.25], 'DeepPurple': [0.6352941176470588, 0.0, 1.0, 0.25], 'Indigo': [0.24705882352941178, 0.3176470588235294, 0.7098039215686275, 0.25], 'Blue': [0.1607843137254902, 0.42745098039215684, 1.0, 0.25], 'LightBlue': [0.011764705882352941, 0.6627450980392157, 0.9568627450980393, 0.25], 'Cyan': [0.0, 0.9215686274509803, 0.8901960784313725, 0.25], 'Teal': [0.0, 0.5882352941176471, 0.5333333333333333, 0.25], 'Green': [0.2980392156862745, 0.6862745098039216, 0.3137254901960784, 0.25], 'LightGreen': [0.5450980392156862, 0.7647058823529411, 0.2901960784313726, 0.25], 'Lime': [0.803921568627451, 0.8627450980392157, 0.2235294117647059, 0.25], 'Yellow': [1.0, 0.9215686274509803, 0.23137254901960785, 0.25], 'Amber': [1.0, 0.7568627450980392, 0.027450980392156862, 0.25], 'Orange': [1.0, 0.596078431372549, 0.0, 0.25], 'DeepOrange': [1.0, 0.3411764705882353, 0.13333333333333333, 0.25], 'Brown': [0.4745098039215686, 0.3333333333333333, 0.2823529411764706, 0.25], 'Gray': [0.6196078431372549, 0.6196078431372549, 0.6196078431372549, 0.25], 'BlueGray': [0.3764705882352941, 0.49019607843137253, 0.5450980392156862, 0.25]}
colors = {
    "Red": {
        "50": "FFEBEE",
        "100": "FFCDD2",
        "200": "EF9A9A",
        "300": "E57373",
        "400": "EF5350",
        "500": "F44336",
        "600": "E53935",
        "700": "D32F2F",
        "800": "C62828",
        "900": "B71C1C",
        "A100": "FF8A80",
        "A200": "FF5252",
        "A400": "FF1744",
        "A700": "D50000",
    },
    "Pink": {
        "50": "FCE4EC",
        "100": "F8BBD0",
        "200": "F48FB1",
        "300": "F06292",
        "400": "EC407A",
        "500": "E91E63",
        "600": "D81B60",
        "700": "C2185B",
        "800": "AD1457",
        "900": "880E4F",
        "A100": "FF80AB",
        "A200": "FF4081",
        "A400": "F50057",
        "A700": "C51162",
    },
    "Purple": {
        "50": "F3E5F5",
        "100": "E1BEE7",
        "200": "b0a1ff",
        "300": "A594FF",
        "400": "b0a1ff",
        "500": "5433FE",
        "600": "4E34D8",
        "700": "4E34D8",
        "800": "4E34D8",
        "900": "4A148C",
        "A100": "EA80FC",
        "A200": "E040FB",
        "A400": "D500F9",
        "A700": "AA00FF",
    },
    "DeepPurple": {
        "50": "EDE7F6",
        "100": "D1C4E9",
        "200": "B39DDB",
        "300": "9575CD",
        "400": "7E57C2",
        "500": "6200EA",
        "600": "5E35B1",
        "700": "512DA8",
        "800": "4527A0",
        "900": "311B92",
        "A100": "B388FF",
        "A200": "7C4DFF",
        "A400": "651FFF",
        "A700": "6200EA",
    },
    "Indigo": {
        "50": "E8EAF6",
        "100": "C5CAE9",
        "200": "9FA8DA",
        "300": "7986CB",
        "400": "5C6BC0",
        "500": "3F51B5",
        "600": "3949AB",
        "700": "303F9F",
        "800": "283593",
        "900": "1A237E",
        "A100": "8C9EFF",
        "A200": "536DFE",
        "A400": "3D5AFE",
        "A700": "304FFE",
    },
    "Blue": {
        "50": "E3F2FD",
        "100": "BBDEFB",
        "200": "90CAF9",
        "300": "64B5F6",
        "400": "42A5F5",
        "500": "2962FF",
        "600": "1E88E5",
        "700": "1976D2",
        "800": "1565C0",
        "900": "0D47A1",
        "A100": "82B1FF",
        "A200": "448AFF",
        "A400": "2979FF",
        "A700": "2962FF",
    },
    "LightBlue": {
        "50": "E1F5FE",
        "100": "B3E5FC",
        "200": "81D4FA",
        "300": "4FC3F7",
        "400": "29B6F6",
        "500": "03A9F4",
        "600": "039BE5",
        "700": "0288D1",
        "800": "0277BD",
        "900": "01579B",
        "A100": "80D8FF",
        "A200": "40C4FF",
        "A400": "00B0FF",
        "A700": "0091EA",
    },
    "Cyan": {
        "50": "E0F7FA",
        "100": "B2EBF2",
        "200": "80DEEA",
        "300": "4DD0E1",
        "400": "26C6DA",
        "500": "00D8D4",
        "600": "00ACC1",
        "700": "0097A7",
        "800": "00838F",
        "900": "006064",
        "A100": "84FFFF",
        "A200": "18FFFF",
        "A400": "00E5FF",
        "A700": "00B8D4",
    },
    "Teal": {
        "50": "E0F2F1",
        "100": "B2DFDB",
        "200": "80CBC4",
        "300": "4DB6AC",
        "400": "26A69A",
        "500": "00BFA5",
        "600": "00897B",
        "700": "00796B",
        "800": "00695C",
        "900": "004D40",
        "A100": "A7FFEB",
        "A200": "64FFDA",
        "A400": "1DE9B6",
        "A700": "00BFA5",
    },
    "Green": {
        "50": "E8F5E9",
        "100": "C8E6C9",
        "200": "A5D6A7",
        "300": "81C784",
        "400": "66BB6A",
        "500": "00C853",
        "600": "43A047",
        "700": "388E3C",
        "800": "2E7D32",
        "900": "1B5E20",
        "A100": "B9F6CA",
        "A200": "69F0AE",
        "A400": "00E676",
        "A700": "00C853",
    },
    "LightGreen": {
        "50": "F1F8E9",
        "100": "DCEDC8",
        "200": "C5E1A5",
        "300": "AED581",
        "400": "9CCC65",
        "500": "8BC34A",
        "600": "7CB342",
        "700": "689F38",
        "800": "558B2F",
        "900": "33691E",
        "A100": "CCFF90",
        "A200": "B2FF59",
        "A400": "76FF03",
        "A700": "64DD17",
    },
    "Lime": {
        "50": "F9FBE7",
        "100": "F0F4C3",
        "200": "E6EE9C",
        "300": "DCE775",
        "400": "D4E157",
        "500": "CDDC39",
        "600": "C0CA33",
        "700": "AFB42B",
        "800": "9E9D24",
        "900": "827717",
        "A100": "F4FF81",
        "A200": "EEFF41",
        "A400": "C6FF00",
        "A700": "AEEA00",
    },
    "Yellow": {
        "50": "FFFDE7",
        "100": "FFF9C4",
        "200": "FFF59D",
        "300": "FFF176",
        "400": "FFEE58",
        "500": "FFEB3B",
        "600": "FDD835",
        "700": "FBC02D",
        "800": "F9A825",
        "900": "F57F17",
        "A100": "FFFF8D",
        "A200": "FFFF00",
        "A400": "FFEA00",
        "A700": "FFD600",
    },
    "Amber": {
        "50": "FFF8E1",
        "100": "FFECB3",
        "200": "FFE082",
        "300": "FFD54F",
        "400": "FFCA28",
        "500": "FFC107",
        "600": "FFB300",
        "700": "FFA000",
        "800": "FF8F00",
        "900": "FF6F00",
        "A100": "FFE57F",
        "A200": "FFD740",
        "A400": "FFC400",
        "A700": "FFAB00",
    },
    "Orange": {
        "50": "FFF3E0",
        "100": "FFE0B2",
        "200": "FFCC80",
        "300": "FFB74D",
        "400": "FFA726",
        "500": "FF9800",
        "600": "FB8C00",
        "700": "F57C00",
        "800": "EF6C00",
        "900": "E65100",
        "A100": "FFD180",
        "A200": "FFAB40",
        "A400": "FF9100",
        "A700": "FF6D00",
    },
    "DeepOrange": {
        "50": "FBE9E7",
        "100": "FFCCBC",
        "200": "FFAB91",
        "300": "ff8d69",
        "400": "FF7043",
        "500": "ff7a4f",
        "600": "F4511E",
        "700": "E64A19",
        "800": "D84315",
        "900": "BF360C",
        "A100": "FF9E80",
        "A200": "FF6E40",
        "A400": "FF3D00",
        "A700": "DD2C00",
    },
    "Brown": {
        "50": "EFEBE9",
        "100": "D7CCC8",
        "200": "BCAAA4",
        "300": "A1887F",
        "400": "8D6E63",
        "500": "795548",
        "600": "6D4C41",
        "700": "5D4037",
        "800": "4E342E",
        "900": "3E2723",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "Gray": {
        "50": "FAFAFA",
        "100": "F5F5F5",
        "200": "EEEEEE",
        "300": "E0E0E0",
        "400": "BDBDBD",
        "500": "9E9E9E",
        "600": "757575",
        "700": "616161",
        "800": "424242",
        "900": "212121",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "BlueGray": {
        "50": "ECEFF1",
        "100": "CFD8DC",
        "200": "B0BEC5",
        "300": "90A4AE",
        "400": "78909C",
        "500": "607D8B",
        "600": "546E7A",
        "700": "455A64",
        "800": "37474F",
        "900": "263238",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "FFFFFF",
        "Background": "FAFAFA",
        "CardsDialogs": "FFFFFF",
        "FlatButtonDown": "cccccc",
    },
    "Dark": {
        "StatusBar": "000000",
        "AppBar": "262626",
        "Background": "161616",
        "CardsDialogs": "262626",
        "FlatButtonDown": "999999",
    },
}
"""Color palette. Taken from `2014 Material Design color palettes
<https://material.io/design/color/the-color-system.html>`_.

To demonstrate the shades of the palette, you can run the following code:

.. code-block:: python

    from kivy.lang import Builder
    from kivy.uix.boxlayout import BoxLayout
    from kivy.utils import get_color_from_hex
    from kivy.properties import ListProperty, StringProperty

    from kivymd.color_definitions import colors
    from kivymd.uix.tab import MDTabsBase

    demo = '''
    <Root@BoxLayout>
        orientation: 'vertical'

        MDToolbar:
            title: app.title

        MDTabs:
            id: android_tabs
            on_tab_switch: app.on_tab_switch(*args)
            size_hint_y: None
            height: "48dp"
            tab_indicator_anim: False

        ScrollView:

            MDList:
                id: box


    <ItemColor>:
        size_hint_y: None
        height: "42dp"

        canvas:
            Color:
                rgba: root.color
            Rectangle:
                size: self.size
                pos: self.pos

        MDLabel:
            text: root.text
            halign: "center"


    <Tab>:
    '''

    from kivy.factory import Factory
    from kivymd.app import MDApp


    class Tab(BoxLayout, MDTabsBase):
        pass


    class ItemColor(BoxLayout):
        text = StringProperty()
        color = ListProperty()


    class Palette(MDApp):
        title = "Colors definitions"

        def build(self):
            Builder.load_string(demo)
            self.screen = Factory.Root()

            for name_tab in colors.keys():
                tab = Tab(text=name_tab)
                self.screen.ids.android_tabs.add_widget(tab)
            return self.screen

        def on_tab_switch(self, instance_tabs, instance_tab, instance_tabs_label, tab_text):
            self.screen.ids.box.clear_widgets()
            for value_color in colors[tab_text]:
                self.screen.ids.box.add_widget(
                    ItemColor(
                        color=get_color_from_hex(colors[tab_text][value_color]),
                        text=value_color,
                    )
                )

        def on_start(self):
            self.on_tab_switch(
                None,
                None,
                None,
                self.screen.ids.android_tabs.ids.layout.children[-1].text,
            )


    Palette().run()

.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/palette.gif
    :align: center
"""

palette = [
    "Red",
    "Pink",
    "Purple",
    "DeepPurple",
    "Indigo",
    "Blue",
    "LightBlue",
    "Cyan",
    "Teal",
    "Green",
    "LightGreen",
    "Lime",
    "Yellow",
    "Amber",
    "Orange",
    "DeepOrange",
    "Brown",
    "Gray",
    "BlueGray",
]
"""Valid values for color palette selecting."""

hue = [
    "50",
    "100",
    "200",
    "300",
    "400",
    "500",
    "600",
    "700",
    "800",
    "900",
    "A100",
    "A200",
    "A400",
    "A700",
]
"""Valid values for color hue selecting."""


light_colors = {
    "Red": ["50", "100", "200", "300", "A100"],
    "Pink": ["50", "100", "200", "A100"],
    "Purple": ["50", "100", "200", "A100"],
    "DeepPurple": ["50", "100", "200", "A100"],
    "Indigo": ["50", "100", "200", "A100"],
    "Blue": ["50", "100", "200", "300", "400", "A100"],
    "LightBlue": [
        "50",
        "100",
        "200",
        "300",
        "400",
        "500",
        "A100",
        "A200",
        "A400",
    ],
    "Cyan": [
        "50",
        "100",
        "200",
        "300",
        "400",
        "500",
        "600",
        "A100",
        "A200",
        "A400",
        "A700",
    ],
    "Teal": ["50", "100", "200", "300", "400", "A100", "A200", "A400", "A700"],
    "Green": [
        "50",
        "100",
        "200",
        "300",
        "400",
        "500",
        "A100",
        "A200",
        "A400",
        "A700",
    ],
    "LightGreen": [
        "50",
        "100",
        "200",
        "300",
        "400",
        "500",
        "600",
        "A100",
        "A200",
        "A400",
        "A700",
    ],
    "Lime": [
        "50",
        "100",
        "200",
        "300",
        "400",
        "500",
        "600",
        "700",
        "800",
        "A100",
        "A200",
        "A400",
        "A700",
    ],
    "Yellow": [
        "50",
        "100",
        "200",
        "300",
        "400",
        "500",
        "600",
        "700",
        "800",
        "900",
        "A100",
        "A200",
        "A400",
        "A700",
    ],
    "Amber": [
        "50",
        "100",
        "200",
        "300",
        "400",
        "500",
        "600",
        "700",
        "800",
        "900",
        "A100",
        "A200",
        "A400",
        "A700",
    ],
    "Orange": [
        "50",
        "100",
        "200",
        "300",
        "400",
        "500",
        "600",
        "700",
        "A100",
        "A200",
        "A400",
        "A700",
    ],
    "DeepOrange": ["50", "100", "200", "300", "400", "A100", "A200"],
    "Brown": ["50", "100", "200"],
    "Gray": ["50", "100", "200", "300", "400", "500"],
    "BlueGray": ["50", "100", "200", "300"],
    "Dark": [],
    "Light": ["White", "MainBackground", "DialogBackground"],
}
"""Which colors are light. Other are dark."""

text_colors = {
    "Red": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "FFFFFF",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "Pink": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "FFFFFF",
        "400": "FFFFFF",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "Purple": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "FFFFFF",
        "400": "FFFFFF",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "DeepPurple": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "FFFFFF",
        "400": "FFFFFF",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "Indigo": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "FFFFFF",
        "400": "FFFFFF",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "Blue": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "LightBlue": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "FFFFFF",
    },
    "Cyan": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "000000",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "Teal": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "Green": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "LightGreen": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "000000",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "Lime": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "000000",
        "700": "000000",
        "800": "000000",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "Yellow": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "000000",
        "700": "000000",
        "800": "000000",
        "900": "000000",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "Amber": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "000000",
        "700": "000000",
        "800": "000000",
        "900": "000000",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "Orange": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "000000",
        "700": "000000",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "000000",
        "A400": "000000",
        "A700": "000000",
    },
    "DeepOrange": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "000000",
        "A200": "000000",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "Brown": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "FFFFFF",
        "400": "FFFFFF",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "FFFFFF",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "Gray": {
        "50": "FFFFFF",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "000000",
        "500": "000000",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "FFFFFF",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
    "BlueGray": {
        "50": "000000",
        "100": "000000",
        "200": "000000",
        "300": "000000",
        "400": "FFFFFF",
        "500": "FFFFFF",
        "600": "FFFFFF",
        "700": "FFFFFF",
        "800": "FFFFFF",
        "900": "FFFFFF",
        "A100": "FFFFFF",
        "A200": "FFFFFF",
        "A400": "FFFFFF",
        "A700": "FFFFFF",
    },
}
"""Text colors generated from :data:`~light_colors`. "000000" for light and
"FFFFFF" for dark.

How to generate text_colors dict

.. code-block:: python

   text_colors = {}
   for p in palette:
       text_colors[p] = {}
       for h in hue:
           if h in light_colors[p]:
               text_colors[p][h] = "000000"
           else:
               text_colors[p][h] = "FFFFFF"
"""

theme_colors = [
    "Primary",
    "Secondary",
    "Background",
    "Surface",
    "Error",
    "On_Primary",
    "On_Secondary",
    "On_Background",
    "On_Surface",
    "On_Error",
]
"""Valid theme colors."""

