
from .config import *


class Data:

    core = None
    textures = {}
    audio_buffers = {}
    fonts = {}
    imgui_fonts = {}
    imgui_font_configs = {}

    @classmethod
    def init(cls, core):
        cls.core = core
        cls.imgui_fonts["--default--"] = cls.core.imgui_io.fonts.add_font_default()

    @classmethod
    def load_audio(cls, label: str, filename: str):
        if label not in cls.audio_buffers.keys():
            cls.audio_buffers[label] = cls.core.oal_ctx.create_buffer()
            cls.core.oal_ctx.load_audio(cls.audio_buffers[label], str(AUDIO_DIR.joinpath(filename)))

    @classmethod
    def delete_audio(cls, label: str):
        if label in cls.audio_buffers.keys():
            cls.core.oal_ctx.delete_buffer(cls.audio_buffers[label])
            del cls.audio_buffers[label]

    @classmethod
    def load_imgui_font(cls, label: str, filename: str, size: int):
        cls.imgui_font_configs[label] = imgui.FontConfig()
        cls.imgui_font_configs[label].name = label
        cls.imgui_font_configs[label].oversample_h = 2
        cls.imgui_font_configs[label].oversample_v = 2
        cls.imgui_fonts[label] = cls.core.io.fonts.add_font_from_file_ttf(str(TEX_DIR.joinpath(filename)), size, cls.imgui_font_configs[label])