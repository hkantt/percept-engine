
from .states import *


class Clock:

    time = 0
    dt = 0.016
    dt_sq = dt * dt
    _last_time = 0

    @classmethod
    def process(cls):
        cls.time = time.time()
        cls.dt = cls.time - cls._last_time
        cls.dt_sq = cls.dt * cls.dt
        cls._last_time = cls.time


class Core:

    ctx = None
    oal_ctx = None
    render_targets = {}
    imgui_io = None

    states = {}
    active_s = None
    queued_s = None

    w, h = 0, 0
    hw, hh = 0, 0 
    qw, qh = 0, 0

    @classmethod
    def init(cls, width: int, height: int, title: str):
        cls.w, cls.h = width, height
        cls.hw, cls.hh = math.ceil(cls.w) // 2, math.ceil(cls.h) // 2
        cls.qw, cls.qh = math.ceil(cls.w) // 4, math.ceil(cls.h) // 4
        
        percept.set_window_size(width, height)
        percept.set_window_title(title)
        
        percept.init()
        percept.set_events_callback(cls.events)
        percept.set_process_callback(cls.process)
        percept.set_render_callback(cls.render)
        percept.set_render_ui_callback(cls.render_ui)

        cls.oal_ctx = percept.oal.Context()

        cls.ctx = mgl.create_context()

        cls.imgui_io = imgui.get_io()

        Data.init(cls)
        Audio.init(cls)

    @classmethod
    def add_render_target(cls, label: str, width: int, height: int, channels: int=4, filter_flags: tuple=(mgl.NEAREST, mgl.NEAREST)):
        cls.render_targets[label] = [cls.ctx.texture((width, height), channels), None]
        cls.render_targets[label][0].filter = filter_flags
        cls.render_targets[label][1] = cls.ctx.framebuffer(color_attachments=[cls.render_targets[label][0]])

    @classmethod
    def delete_render_target(cls, label: str):
        if label in cls.render_targets.keys():
            cls.render_targets[label][0].release()
            cls.render_targets[label][1].release()
            del cls.render_targets[label]

    @classmethod
    def set_render_target(cls, label: str):
        cls.render_targets[label][1].use()

    @classmethod
    def reset_render_target(cls):
        cls.ctx.screen.use()

    @classmethod
    def get_render_target_tex(cls, label: str):
        return cls.render_targets[label][0].glo

    @classmethod
    def add_state(cls, state: State):
        for s in cls.states.values():
            if isinstance(s, state):
                print("State already added")
                return
        new_state = state()
        cls.states[new_state.id] = new_state

    @classmethod
    def remove_state(cls, state_id: any):
        if state_id in cls.states.keys():
            if cls.active_s:
                if cls.active_s.id == state_id:
                    cls.active_s.exit()
                    cls.active_s = None
            del cls.states[state_id]

    @classmethod
    def activate_state(cls, state_id):
        cls.queued_s = cls.states[state_id]

    @classmethod
    def run(cls):
        percept.run()

    @classmethod
    def events(cls):
        if cls.queued_s:
            if cls.active_s:
                cls.active_s.exit()
            cls.active_s = cls.queued_s
            cls.active_s.enter()
            cls.queued_s = None

        if cls.active_s:
            cls.active_s.events()

    @classmethod
    def process(cls):
        Clock.process()
        Audio.process()

        cls.w, cls.h = percept.get_window_size()
        cls.hw, cls.hh = math.ceil(cls.w) // 2, math.ceil(cls.h) // 2
        cls.qw, cls.qh = math.ceil(cls.w) // 4, math.ceil(cls.h) // 4
        
        if cls.active_s:
            cls.active_s.process()

    @classmethod
    def render(cls):
        cls.ctx.clear(0.0, 0.0, 0.0, 1.0)
        if cls.active_s:
            cls.active_s.render()

    @classmethod
    def render_ui(cls):
        if cls.active_s:
            cls.active_s.render_ui()