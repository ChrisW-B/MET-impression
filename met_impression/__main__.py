import requests
import random
from inky.inky_uc8159 import Inky
from PIL import Image
import hitherdither
import time

inky = Inky()
saturation = 0.5
thresholds = [64, 64, 64]
gutter_size = 5

departments = ['9', '11', '21']
objects_query = 'https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds' + \
    '|'.join(departments)

object_query = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/'

palette = hitherdither.palette.Palette(
    inky._palette_blend(saturation, dtype='uint24'))


def image_fits(img):
    if not img:
        return False
    width, height = img.size
    if width < height:
        return False
    if width < Inky.WIDTH or height < Inky.HEIGHT:
        return False
    return width / height > 1.25 and width / height < 1.4


def query_object(object_id):
    query_url = object_query + str(object_id)
    object_request = requests.get(url=query_url)
    object_data = object_request.json()
    return object_data


def get_random_art():
    art_list_request = requests.get(url=objects_query)
    object_data = art_list_request.json()
    object_ids = object_data['objectIDs']

    random_entry = random.choice(object_ids)
    selected_object = query_object(random_entry)
    im = None
    while (not image_fits(im)):
        random_entry = random.choice(object_ids)
        selected_object = query_object(random_entry)
        if not selected_object['primaryImage']:
            continue
        im = Image.open(requests.get(
            selected_object['primaryImage'], stream=True).raw).convert("RGB")
        time.sleep(1)
    print(selected_object['objectURL'])
    print(selected_object['department'])
    print(selected_object['title'])
    return im


def draw_art(art):
    bg = Image.new("RGBA", (inky.WIDTH, inky.HEIGHT), (255, 255, 255, 255))
    bg_w, bg_h = bg.size

    art.thumbnail((inky.WIDTH, inky.HEIGHT), Image.Resampling.LANCZOS)
    art_dithered = hitherdither.ordered.bayer.bayer_dithering(
        art, palette, thresholds, order=2)
    art_w, art_h = art_dithered.size

    offset = ((bg_w - art_w) // 2, (bg_h - art_h) // 2)
    bg.paste(art_dithered, offset)

    inky.set_image(bg)
    inky.show()


def main():
    art = get_random_art()
    draw_art(art)


if __name__ == '__main__':
    main()
