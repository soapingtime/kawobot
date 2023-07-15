import os
from glob import glob
from random import choice
from wand.image import Image
from atproto import Client


max_size = 900 * 1024  # 900 KB in bytes

def resize_image(random_image):
    with Image(filename=random_image) as img:
        image_size = os.path.getsize(random_image)
        if image_size > max_size:
            img.compression_quality = 80
            img.save(filename=random_image)


def main():
    client = Client()
    client.login(os.environ['BSKY_HANDLE'], os.environ['BSKY_APP_PASSWORD'])
    random_image = choice(glob(f'images/**/*/*'))
    print(random_image)

    if os.path.getsize(random_image) > max_size:
        resize_image(random_image)

    with open(random_image, 'rb') as f:
        img_data = f.read()

        status = random_image.split("/")[-1].split("_")[0]
        client.send_image(
            text=f'twitter.com/i/status/{status}', image=img_data, image_alt=''
        )


if __name__ == '__main__':
    main()
