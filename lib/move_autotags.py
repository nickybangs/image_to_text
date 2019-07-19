from fastai.core import Path
from file_maintenance import *
import config

mp = Path('/Users/nicholasbangs/Notebooks/personal/greek_reader_master')
config.master_path = mp

config.letter_dest = mp/'lgi_data'/'new_lgi_data'
move_autotags()
