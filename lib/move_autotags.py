from fastai.core import Path
from file_maintenance import *
import config

mp = Path('/Users/nicholasbangs/Notebooks/personal/greek_reader_master')
config.master_path = mp

config.letter_dest = mp/'herodotus'/'new_split'
move_autotags()
