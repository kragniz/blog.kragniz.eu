Controlling vagalume last.fm client using python
################################################
:date: 2010-06-01 18:09
:author: Louis Taylor
:category: python
:tags: DBus, open source, programing, python, vagalume
:slug: control-vagalume-from-python

I've recently been playing with the docky python bindings, and started by
writing a helper to interact with `Vagalume <http://vagalume.igalia.com/>`__, a
lightweight last.fm client (I later added it to `a project on launchpad
<https://launchpad.net/vagalume-docky>`__). The vagalume DBus methods and
signals are mostly undocumented, but they can be found lurking around after a
quick look at `some of the source code
<http://gitorious.org/vagalume/vagalume/blobs/master/src/dbus.h>`__.

.. code-block:: python

    import dbus
    import gobject
    from dbus.mainloop.glib import DBusGMainLoop

    class Vagalume(object):
        def __init__(self):
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
            self.bus = dbus.SessionBus()

            self.player = self.bus.get_object('com.igalia.vagalume',
                                              '/com/igalia/vagalume')

            self.bus.add_signal_receiver(self.song_changed,
                                         dbus_interface='com.igalia.vagalume',
                                         signal_name='notify')

        def song_changed(self, *args):
            state = args[0]
            if state == 'stopped':
                #do something when the player is stopped
                self.stopped()
            elif state == 'playing':
                artist = args [1]
                title = args [2]
                album = args [3]
                #do something with the data here...
                self.playing(artist, title, album)

        def stopped(self):
            '''Run when music is stopped'''
            pass

        def playing(self, artist, title, album):
            '''Run when new song is played'''
            pass

    if __name__ == "__main__":
        app = Vagalume()

        # gtk mainloop can be used if you're using this as part of a gtk app
        mainloop = gobject.MainLoop(is_running=True)
        mainloop.run() 

You'll probably notice the method ``song_changed``. This is a method which is
registered with DBus and run each time the ``'notify'`` signal is emitted from
vagalume. This checks whether the notification is due to vagalume starting a
new song or stopping the current one and runs either ``self.stopped`` or
``self.playing``. These two methods by default do nothing, so subclassing
``Vagalume`` to make them do something useful is good:

.. code-block:: python

    class MyFancyVagalume(Vagalume):
        def stopped(self):
            print 'just stopped the beat'

        def playing(self, artist, title, album):
            print 'now playing "%s" by %s' % (title, artist)

To interact with vagalume do something like:

.. code-block:: python

    vagalume = Vagalume()

    # do anything you want with dbus
    vagalume.player.Play()
    vagalume.player.Skip()
    vagalume.player.LoveTrack()
    vagalume.player.BanTrack()
    vagalume.player.Stop()

take a look at the source
(http://gitorious.org/vagalume/vagalume/blobs/master/src/dbus.h) for all of the
functions available
