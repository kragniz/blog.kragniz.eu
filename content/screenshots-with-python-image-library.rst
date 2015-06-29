Grabbing screenshots as a Python Image Library ``Image`` type
#############################################################
:date: 2010-05-26 18:09
:author: Louis Taylor
:category: python
:tags: programing, python, python image library
:slug: screenshots-with-python-image-library

A couple of days ago I needed to take screenshots of my linux desktop's screen and 
manipulate these captured images using Python Image Library (PIL). I wrote a
small python class to do the work of taking the screenshot and returning a PIL
``Image`` object for use in the rest of the system I was writing.

The code ended up being simpler than I expected, mostly because `GDK
<http://en.wikipedia.org/wiki/GDK>`__, the library used as an intermediary
between GTK and the low-level window manager and display server commands, does
all the heavy lifting.

Method
------

I wanted to take many screenshots during a run of the program I was writing, so
allocated a persistent ``gtk.gdk.Pixbuf`` object to store the captured image
in. This object has a handy ``get_from_drawable`` method. Of course, the X11
root window is a drawable, so by using ``gtk.gdk.get_default_root_window()`` we
can copy each pixel into our buffer.

Once the ``Pixbuf`` is full, an ``Image`` needs to be created from it, since
that was the original aim. Luckily, there's ``Image.frombuffer`` to do all the
hard work when combined with ``Pixbuf.get_pixels()``.

Full code:

.. code-block:: python

    import Image, gtk

    class Screenshotter(object):
        def __init__(self):
            self.img_width = gtk.gdk.screen_width()
            self.img_height = gtk.gdk.screen_height()

            self.screengrab = gtk.gdk.Pixbuf(
                gtk.gdk.COLORSPACE_RGB,
                False,
                8,
                self.img_width,
                self.img_height
            )

        def take(self):
            self.screengrab.get_from_drawable(
                gtk.gdk.get_default_root_window(),
                gtk.gdk.colormap_get_system(),
                0, 0, 0, 0,
                self.img_width,
                self.img_height
            )

            final_screengrab = Image.frombuffer(
                "RGB",
                (self.img_width, self.img_height),
                self.screengrab.get_pixels(),
                "raw",
                "RGB",
                self.screengrab.get_rowstride(),
                1
            )

            return final_screengrab

    if __name__ == '__main__':
        screenshot = Screenshotter()
        image = screenshot.take()

