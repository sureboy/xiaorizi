

from PIL import Image
def make_thumb(path, size = 480):
    pixbuf = Image.open(path)
    width, height = pixbuf.size

     
    delta = 30
    width = 20
    pixbuf.thumbnail((size, width), Image.ANTIALIAS)

    return pixbuf


make_thumb("pic2.jpg").save("d:/pic2.jpg")

