
from entities import *


class Demo(State):

    # Demonstration of basic features of the engine

    def __init__(self):
        super().__init__("Demo")

    def enter(self):
        Core.imgui_io.font_global_scale = 2

        self.chk = False
        self.f1 = 0.0
        self.i1 = 0
        self.color = imgui.Vec4(1.0, 0.0, 0.0, 1.0)
        self.items = ['A', 'B', 'C']
        self.selected = 0
        self.radio_items = ['P', 'Q', 'R']
        self.radio_select = 0
        self.text = ""
        self.script = ""
        self.df1 = 0
        self.col = [0, 0, 0, 0]       

        Core.add_render_target("render", 512, 512, 4)

    def render(self):
        Core.set_render_target("render")
        Core.ctx.clear(self.color.x, self.color.y, self.color.z, self.color.w)
        Core.reset_render_target()

    def render_ui(self):
        imgui.begin("Window")

        imgui.text("Hello, World!")
        imgui.same_line()
        imgui.button("Button")

        self.chk = imgui.checkbox("Checkbox", self.chk)[1]
        self.f1 = imgui.slider_float("Float", self.f1, -1.0, 1.0, "%.2f")[1]
        self.i1 = imgui.slider_int("Int", self.i1, -10, 10)[1]
        self.color = imgui.color_edit3("Color", self.color)[1]

        for i, label in enumerate(self.radio_items):
            changed, result = imgui.radio_button(label, self.radio_select, i)
            if changed:
                self.radio_select = result
            imgui.same_line()

        imgui.spacing()

        self.selected = imgui.combo("Combo", self.selected, self.items)[1]
        c, self.text = imgui.input_text("Text", self.text)
        c, self.script = imgui.input_text_multiline("Script", self.script, imgui.Vec2(400, 200))
        c, self.df1 = imgui.drag_float("Drag Float", self.df1, speed=0.01, min = 0.0, max=1.0)
        c, self.col = imgui.drag_int4("Col", self.col, min=0, max=255)
        
        imgui.end()

        imgui.push_style_var_vec2(imgui.StyleVar.WindowPadding, imgui.Vec2(0, 0))
        imgui.begin("Render")
        w, h = imgui.get_available_region()

        # Note: Image is being remapped while rendering here to prevent inversion
        imgui.image(Core.get_render_target_tex("render"), w, h, imgui.Vec2(0, 1), imgui.Vec2(1, 0))
        
        imgui.end()
        imgui.pop_style_var()

Core.add_state(Demo)