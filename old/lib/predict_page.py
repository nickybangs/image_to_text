from fastai.core import Path
from fastai.vision import load_learner, defaults, ImageList,DatasetType
import torch as torch
import os
import yaml

pic_name = 'GK_RDR_PG3_2'

mp = Path('/Users/nicholasbangs/Notebooks/personal/greek_reader_master')
im_path = mp/'lgi_data'/'gk_letter_imgs'/'ω'

defaults.device = torch.device('cpu')
model_path = mp/'models'
model_name = 'rn_34.pkl'
model = load_learner(model_path, model_name, test=ImageList.from_folder(im_path))
preds,y = model.get_preds(ds_type=DatasetType.Test)
classes = model.data.classes
zipped = list([zip(classes, p) for p in preds])
sorted_preds = [sorted(z, key=lambda x: x[1], reverse=True)[0] for z in zipped]
print(sorted_preds)
