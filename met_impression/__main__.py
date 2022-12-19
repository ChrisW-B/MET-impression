import requests
import random
from inky.inky_uc8159 import Inky
from PIL import Image, ImageDraw
import hitherdither
import time

inky = Inky()
saturation = 0.5
thresholds = [64, 64, 64]
gutter_size = 5

departments = ['9', '12', '21']
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
    return width/height > 1.25 and width/height < 1.5


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
   return im


def draw_art(art):
    bg = Image.new("RGBA", (inky.WIDTH, inky.HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(bg)

    art.thumbnail((inky.HEIGHT, inky.HEIGHT), Image.ANTIALIAS)
    art_dithered = hitherdither.ordered.bayer.bayer_dithering(art, palette, thresholds, order=2)
    bg.paste(art_dithered, (0, 0))

    inky.set_image(bg)
    inky.show()


def main():
    art = get_random_art()
    draw_art(art)

if __name__ == '__main__':
    main()
