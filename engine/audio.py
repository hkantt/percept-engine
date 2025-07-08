
from .data import *


class Audio:

    sources = []
    playing = {}
    _check_counter = 0

    @classmethod
    def init(cls, core):
        cls.core = core
        for i in range(24):
            cls.sources.append(cls.core.oal_ctx.create_source())

    @classmethod
    def play(cls, label: str, loop: bool = False):
        if cls.sources:
            if label in cls.playing.keys():
                cls.stop(label)
            if loop:
                cls.core.oal_ctx.set_looping(cls.sources[0], True)
            else:
                cls.core.oal_ctx.set_looping(cls.sources[0], False)
            cls.core.oal_ctx.play(cls.sources[0], Data.audio_buffers[label])
            cls.playing[label] = cls.sources.pop(0)

    @classmethod
    def pause(cls, label: str):
        if label in cls.playing.keys():
            cls.core.oal_ctx.pause(cls.playing[label])

    @classmethod
    def resume(cls, label: str):
        if label in cls.playing.keys():
            cls.core.oal_ctx.resume(cls.playing[label])
    
    @classmethod
    def rewind(cls, label: str):
        if label in cls.playing.keys():
            cls.core.oal_ctx.rewind(cls.playing[label])

    @classmethod
    def stop(cls, label: str):
        if label in cls.playing.keys():
            cls.core.oal_ctx.stop(cls.playing[label])
            cls.sources.append(cls.playing[label])
            del cls.playing[label]

    @classmethod
    def is_playing(cls, label: str):
        return label in cls.playing.keys()

    @classmethod
    def is_paused(cls, label: str):
        if label in cls.playing.keys():
            return cls.core.oal_ctx.is_paused(cls.playing[label])

    @classmethod
    def is_stopped(cls, label: str):
        if label in cls.playing.keys():
            return cls.core.oal_ctx.is_stopped(cls.playing[label])

    @classmethod
    def is_initial(cls, label: str):
        if label in cls.playing.keys():
            return cls.core.oal_ctx.is_initial(cls.playing[label])

    @classmethod
    def set_offset(cls, label: str, seconds: float):
        if label in cls.playing.keys():
            cls.core.oal_ctx.set_offset(cls.playing[label], seconds)

    @classmethod
    def get_offset(cls, label: str):
        if label in cls.playing.keys():
            cls.core.oal_ctx.get_offset(cls.playing[label])

    @classmethod
    def process(cls):
        if cls._check_counter >= 60:
            delete_label = ""
            for label, source in cls.playing.items():
                if not cls.core.oal_ctx.is_playing(source):
                    cls.sources.append(source)
                    delete_label = label
            if delete_label:
                del cls.playing[delete_label]
            cls._check_counter = 0
        cls._check_counter += 1