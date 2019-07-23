import config
from file_maintenance import *
from pred_handler import *

def get_letter():
	textbox = config.textbox
	letter_options = config.letter_options
	if textbox.value == '':
		if letter_options.value == '':
			return
		ltr = letter_options.value
	else:
	    ltr = textbox.value
	return ltr


def update_letter_mapping(ltr):
	letter_mappings = config.letter_mappings
	output = config.output
	if ltr not in letter_mappings.keys():
	    if len(ltr.split(':')) > 1:
	        letter_mappings[ltr.split(':')[0].strip()] = ltr.split(':')[1].strip()
	        ltr = ltr.split(':')[0].strip()
	        return ltr
	    else:
	        with output:
	        	print('no key, update field')
	        return -1
	else:
		return ltr


def add_letter_image(ltr):
	letter_dest = config.letter_dest
	letter_dict = config.letter_dict
	temp_path = config.temp_path
	letter_dir = letter_dest/ltr
	os.system('mkdir -p {0}'.format(letter_dir))
	letter_imname = '{}_{}.jpg'.format(ltr, get_next_ind(ltr))
	while letter_dir/letter_imname in letter_dir.ls():
		letter_imname = 'r_' + str(np.random.randint(0,1000)) + letter_imname
	letter_path = letter_dir/letter_imname
	os.system('mv {0} {1}'.format(temp_path/'temp_letter.jpg', letter_path))


def update_letter(b):
	output = config.output
	letter_dict = config.letter_dict
	image = config.image
	textbox = config.textbox
	letter_mappings = config.letter_mappings
	output.clear_output()
	ltr = get_letter() 
	ltr = update_letter_mapping(ltr)
	if ltr == -1:
		return
	ltr = letter_mappings[ltr]

	add_letter_image(ltr)
	image.value = get_next_im()
	textbox.value = ''
	with output:
		print(ltr, letter_dict[ltr])


def skip(b):
	output = config.output
	image = config.image
	output.clear_output()
	image.value = get_next_im()

	
def get_context(b):
	itr = config.itr
	components = config.components  
	cols = config.cols
	rows = config.rows
	temp_path = config.temp_path
	image = config.image
	output = config.output
	output.clear_output()
	lb, ub, lbr, ubr = get_bounds(itr)
	imgarr = config.img_arr.copy()
	draw_box(lb, ub, lbr, ubr, imgarr)
	lb, ub, lbr, ubr = get_bounds(itr,context=1)
	imwrite(temp_path/'temp_letter_context.jpg', imgarr[lbr:ubr,lb:ub])
	image.value = open(temp_path/'temp_letter_context.jpg', 'rb').read()



def reset_context(b):
	output = config.output
	image = config.image
	temp_path = config.temp_path
	output.clear_output()
	image.value = open(temp_path/'temp_letter.jpg', "rb").read()



def get_next_im():
	itr = config.itr
	imgarr = config.img_arr.copy()
	components = config.components
	letter_options = config.letter_options
	output = config.output
	temp_path = config.temp_path
	itr += 1
	lb, ub, lbr, ubr = get_bounds(itr)
	imwrite(temp_path/'temp_letter.jpg', imgarr[lbr:ubr,lb:ub])
	img = open(temp_path/'temp_letter.jpg', "rb").read()
	preds = get_top_preds(temp_path/'temp_letter.jpg')
	letter_options.options =[l[0] for l in preds]
	letter_options.value = letter_options.options[0]
	config.itr = itr
	with output:
		print(preds)
	return img
