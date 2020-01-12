import Path
import PIL

from imaging import preprocess

def main():
    imname = input('image name: ')
    image = PIL.Image.open(imname)
    image = preprocess(image)
    lines = split_lines(image)
    parsed = [[] * len(lines)]
    for i,line in enumerate(lines):
        parsed[i] = parse_line(line)

    with open(f"~/im_to_text_output/{imname.split('.')[0]}_text.txt") as f:
        f.write(text_from_parse(parsed))

    print('Done processing')
