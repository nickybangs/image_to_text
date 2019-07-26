import numpy as np
import os
import re
import config

# GLOBAL VARIABLES
# letter_dict
# letter_dest
# components
# new_components


def get_all_images(d):
	return list(filter(lambda x: '.jpg' in x.name, d.ls()))


def get_formatted_images(d, custom_pat=None):
	if custom_pat:
		pat = custom_pat
	else:
		if isinstance(d, list):
			if len(d) == 0:
				return []
			pat = '{}_[0-9]+\.jpg'.format(d[0].parent.name)
			return list(filter(lambda x: re.search(pat, x.name), d))
		else:
			pat = '{}_[0-9]+\.jpg'.format(d.name)
			return list(filter(lambda x: re.search(pat, x.name), d.ls()))


def get_max_im_id(imgs):
	if isinstance(imgs, list) and len(imgs) == 0:
		return -1
	imgs = get_formatted_images(imgs)
	return max(map(int, map(lambda x: x.name.split('_')[-1].replace('.jpg',''), imgs)))


def get_present_ids(imgs):
	if isinstance(imgs, list):
		img_list = imgs
	else:
		img_list = imgs.ls()

	matches = get_formatted_images(imgs)
	max_id = max(get_max_im_id(matches), len(img_list))
	present = np.zeros(max_id+1)

	for f in matches:
		int_id = int(f.name.split('_')[-1].replace('.jpg',''))
		present[int_id] = img_list.index(f) + 1

	return present


def update_letter_names(dirs):
	for d in filter(lambda x: x.is_dir(), dirs):
		dir_ims = get_all_images(d)
		present = get_present_ids(dir_ims)
		available_ids = np.argwhere(present==0).flatten()
		present_ids = list(filter(lambda x: x!= 0, present))
		d_ims = list(filter(lambda x: dir_ims.index(x) + 1 not in present_ids, dir_ims))
		for f in d_ims:
			ind = available_ids[0]
			available_ids = np.delete(available_ids, 0)
			present[ind] = 1
			new_imname = '{}_{}.jpg'.format(d.name, ind)
			os.system('mv {0} {1}'.format(f, d/new_imname))


def get_letter_dict():
	letter_dest = config.letter_dest
	letter_dict = dict()
	for ltr in filter(lambda x: x.is_dir(), letter_dest.ls()):
		present = get_present_ids(ltr)
		letter_dict[ltr.name] = (len(present), np.argwhere(present==0).flatten())
	config.letter_dict = letter_dict


def get_next_ind(ltr):
	letter_dict = config.letter_dict
	if ltr not in letter_dict.keys():
		letter_dict[ltr] = (0, [])
		ind = 0
	else:
		intind = letter_dict[ltr][0]
		avail = letter_dict[ltr][1]
		if len(avail) > 0:
			ind = avail[0]
			avail = np.delete(avail, 0)
			letter_dict[ltr] = (intind, avail)
		else:
			ind = intind
			letter_dict[ltr] = (intind + 1, avail)
	config.letter_dict = letter_dict
	return ind


def get_mistags():
	letter_dest = config.letter_dest
	components = config.components
	new_components = config.new_components
	mistag_pth = letter_dest/'auto_tags'/'mistags'

	for f in get_all_images(mistag_pth):
		com = int(f.name.split('_')[2])
		new_components[com] = components[com]

	if len(get_all_images(mistag_pth)) == 0:
		os.system('rm -r {}'.format(mistag_pth))

	config.new_components = new_components


def move_autotags():
	letter_dest = config.letter_dest
	get_letter_dict()
	autotag_pth = letter_dest/'auto_tags'
	for d in filter(lambda x: x.is_dir(), autotag_pth.ls()):
		for f in d.ls():
			if '.jpg' in f.name:
				os.system('mkdir -p {0}'.format(letter_dest/d.name))
				new_fname = '{}_{}.jpg'.format(d.name, get_next_ind(d.name))
				os.system('mv {0} {1}'.format(f, letter_dest/d.name/new_fname))
