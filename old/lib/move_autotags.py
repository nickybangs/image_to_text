from fastai.core import Path
from file_maintenance import *
import config

mp = Path('../')
config.master_path = mp
config.letter_dest = mp/'all_data'/'lgi_data'/'latin'/'pg2'/'pg2_data'
move_autotags()
