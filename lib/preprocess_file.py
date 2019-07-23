from fastai.core import Path
from fastai.vision import load_learner, defaults
import torch as torch
import os
import yaml

from file_maintenance import *
from image_graph import *
from image_handling import *
from pred_handler import *
import config

pic_name = 'GK_RDR_PG3_2'

mp = Path('../')
config.master_path = mp

defaults.device = torch.device('cpu')
model_path = mp/'models'
model_name = 'rn_34.pkl'
config.model = load_learner(model_path,model_name)
config.letter_dest = mp/'all_data'/'lgi_data'/'pg3_data'
os.system('mkdir -p {}'.format(config.letter_dest))
config.temp_path = config.letter_dest
get_letter_dict()

gr_path = mp/'greek_pages'/'page_graphs'
im_path = mp/'greek_pages'/'page_images'
gr_name = pic_name + '.txt'
im_name = pic_name + '.jpeg'

config.img_arr = get_image_array(im_path/im_name)
config.rows, config.cols = config.img_arr.shape
G = get_graph(gr_path, gr_name, im_path/im_name)
config.components = get_components(G)

preprocess()

with open(config.temp_path/'all_components.yaml', 'w') as f:
	yaml.dump(config.components, f)

with open(config.temp_path/'new_components.yaml', 'w') as f:
	yaml.dump(config.new_components, f)
