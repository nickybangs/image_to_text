from fastai.core import Path
from fastai.vision import load_learner, defaults
import torch as torch
import os
from PIL import Image as pil_im
from PIL import ImageEnhance
import yaml

from file_maintenance import *
from image_graph import *
from image_handling import *
from pred_handler import *
import config

pic_name = 'LAT_RDR_PG2'

mp = Path('../')
config.master_path = mp

defaults.device = torch.device('cpu')
model_path = mp/'models'
model_name = 'latin_model.pkl'
config.model = load_learner(model_path,model_name)
page_dir = mp/'all_data'/'lgi_data'/'latin'/'pg2'
config.letter_dest = page_dir/'pg2_data'
yaml_path = config.letter_dest/'pg2_yaml'
os.system('mkdir -p {}'.format(config.letter_dest))
os.system('mkdir -p {}'.format(yaml_path))
config.temp_path = page_dir
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

with open(yaml_path/'all_components.yaml', 'w') as f:
	yaml.dump(config.components, f)

with open(yaml_path/'new_components.yaml', 'w') as f:
	yaml.dump(config.new_components, f)
