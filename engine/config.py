
import os
import sys
import math
import time
import random
import pathlib

CWD = pathlib.Path().cwd()
DATA_DIR = CWD.joinpath("data")
SHADER_DIR = CWD.joinpath("shaders")
TEX_DIR = DATA_DIR.joinpath("textures")
AUDIO_DIR = DATA_DIR.joinpath("audio")

os.environ["ALSOFT_CONF"] = str(CWD.joinpath("alsoft.ini"))

import engine.percept as percept
import engine.percept.imgui as imgui

import moderngl as mgl

def load_shader(filename: str):
    data = None
    with open(SHADER_DIR.joinpath(filename), 'r') as f:
        data = f.read()
    return data