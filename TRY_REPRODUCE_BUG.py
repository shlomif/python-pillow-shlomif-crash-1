from Tkinter import Tk
import os.path
from PIL import Image, ImageOps, ImageTk
import sys

if Image:
    class PIL_Image(ImageTk.PhotoImage):
        def __init__(self, file=None, image=None, pil_image_orig=None):
            if file:
                image = Image.open(file).convert('RGBA')
            ImageTk.PhotoImage.__init__(self, image)
            self._pil_image = image
            if pil_image_orig:
                self._pil_image_orig = pil_image_orig
            else:
                self._pil_image_orig = image
        def subsample(self, r):
            im = self._pil_image
            w, h = im.size
            w, h = int(float(w)/r), int(float(h)/r)
            im = im.resize((w, h))
            im = PIL_Image(image=im)
            return im
        def resize(self, xf, yf):
            w, h = self._pil_image_orig.size
            w0, h0 = int(w*xf), int(h*yf)
            im = self._pil_image_orig.resize((w0,h0), Image.ANTIALIAS)
            return PIL_Image(image=im, pil_image_orig=self._pil_image_orig)

def loadImage(file=None, data=None, dither=None, alpha=None):
    kw = {}
    if data is None:
        assert file is not None
        kw["file"] = file
    else:
        #assert data is not None
        kw["data"] = data
    if Image:
        # use PIL
        if file:
            im = PIL_Image(file)
            return im
        # fromstring(mode, size, data, decoder_name='raw', *args)
        else:
            return Tkinter.PhotoImage(data=data)
    return Tkinter.PhotoImage(**kw)

IMAGE_EXTENSIONS = (".png", ".gif", ".jpg", ".ppm", ".bmp")

class Foo:
    def __init__(self):
        # self.dir = '/usr/share/PySolFC/images/toolbar/bluecurve/small'
        self.dir = '.'

    def _loadImage(self, name):
        file = os.path.join(self.dir, name)
        image = None
        for ext in IMAGE_EXTENSIONS:
            file = os.path.join(self.dir, name+ext)
            if os.path.isfile(file):
                image = loadImage(file=file)
                break
        return image

    def _setButtonImage(self, button, name):
        image = self._loadImage(name)
        setattr(self, name + "_image", image)
        if Image:
            dis_image = self._createDisabledButtonImage(image)
            if dis_image:
                setattr(self, name + "_disabled_image", dis_image)
                button.config(image=(image, 'disabled', dis_image))
        else:
            button.config(image=image)

    def _createDisabledButtonImage(self, tkim):
        # grayscale and light-up image
        if not tkim:
            return None
        im = tkim._pil_image
        dis_im = ImageOps.grayscale(im)
        ##color = '#ffffff'
        ##factor = 0.6
        color = '#dedede'
        factor = 0.7
        sh = Image.new(dis_im.mode, dis_im.size, color)
        tmp = Image.blend(dis_im, sh, factor)
        dis_im = Image.composite(tmp, im, im)
        dis_tkim = ImageTk.PhotoImage(image=dis_im)
        return dis_tkim

root = Tk()

f = Foo()
f._setButtonImage({}, 'new')
sys.exit(0);

