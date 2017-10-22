#!/usr/bin/env python
# coding: utf-8

import sys
import urllib
from urllib.request import urlopen
from PIL import Image
from skimage import io
import cv2


def get_camera_image(url):
    try:
        with urlopen(url) as stream:
            data = b''
            img = None
            i = None
            done = False
            while not done:
                data += stream.read(1024)
                start = data.find(b'\xff\xd8')
                end = data.find(b'\xff\xd9')
                if start != -1 and end != -1:
                    jpg = data[start:end + 2]
                    data = data[end + 2:]
                    i = cv2.imdecode(np.fromstring(
                        jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    i2 = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(i2)
                    done = True
            return img
    except urllib.error.HTTPError as HTTPError:
        print("HTTPError; Wait and try again.")
        return None
    except urllib.error.URLError as URLError:
        print("URLError; Check url.")
        return None

if __name__ == "__main__":
    image = get_camera_image(sys.argv[1])
    image.save(sys.argv[2])
