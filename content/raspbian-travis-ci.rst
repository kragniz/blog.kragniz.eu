Raspbian on Travis CI
#####################
:date: 2016-01-22 22:23
:author: Louis Taylor
:category: raspberry-pi
:tags: raspbian, raspberry pi, qemu
:slug: raspbian-on-travis-ci

For abersailbot, I've been working on automation of provisioning images to run
on the main raspberry pi inside the boat. In the past, this has been a
primitive bash script which installs packages and configurations files with a
dubious amount of calls out to apt, cp and sed. Wanting to make this a little
more sophisticated, I started writing a set of ansible playbooks.

For testing other repositories, I normally always use
`<https://travis-ci.org>`_. If you're not familiar, Travis CI offers free CI
resources for open source repositories. The VMs it boots are all Ubuntu on
x86_64, however. In order to test things on raspbian, some hacks would be
needed.

Options I considered:

1. No testing (no tests? What madness!)
2. ARM chroot
3. Raspbian fat Docker container
4. Raspbian image booted under QEMU

After some playing around, the QEMU route seemed like the best option. If you'd
like to do the same, the steps I took are fairly simple:

First off, we need to get a disk image. The images provided from the Raspberry
Pi site need some small modifications to run under QEMU, so we need to mount
and edit it. I'm using the ``2015-11-21-raspbian-jessie-lite.img`` image from
`<https://www.raspberrypi.org/downloads/raspbian/>`_.

This image contains two partitions, a small boot partition (FAT) which contains
a few config files and a kernel, and the main ext4 root partition. The latter
is the partition we're interested in. You can inspect the image with ``fdisk``
to show these::

    ~/g/dewi (master) $ fdisk -l 2015-11-21-raspbian-jessie-lite.img
    Disk 2015-11-21-raspbian-jessie-lite.img: 1.4 GiB, 1458569216 bytes, 2848768 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0xb3c5e39a

    Device                               Boot  Start     End Sectors  Size Id Type
    2015-11-21-raspbian-jessie-lite.img1        8192  131071  122880   60M  c W95 FAT32 (LBA)
    2015-11-21-raspbian-jessie-lite.img2      131072 2848767 2717696  1.3G 83 Linux

Note the start of the partition we're interested in (131072). This is the
offset from the start of the image in terms of number of sectors. The sector
size is 512, so the actual offset in terms of bytes is 131072 × 512 =
67108864.

Armed with this knowledge, we can mount the image and edit files on it
interactively.

First, create a directory to mount the image::

    $ mkdir raspbian-jessie-mount-point

then mount the image::

    $ sudo mount -o loop,offset=67108864 2015-11-21-raspbian-jessie-lite.img \
      raspbian-jessie-mount-point

Now it's time to comment out a bunch of things.

1. Open ``raspbian-jessie-mount-point/etc/ld.so.preload`` in an editor of your
   choice and comment out all lines.
2. Do the same and comment out all lines related to ``mmccblk`` in
   ``raspbian-jessie-mount-point/etc/fstab``

After these edits have been made, unmount the image::

    $ sudo umount raspbian-jessie-mount-point

The modified image can now be saved and backed up somewhere. I took a copy and
compressed it to save on space::

    $ xz 2015-11-21-raspbian-jessie-lite.img

Now we have an image to boot, we need a kernel to run. Sadly, a modified
kernel is required, since QEMU does not support raspberry pi hardware. Luckily
the work of patching and building has already been done by someone else.
https://github.com/polaco1782/raspberry-qemu appears to work well.

Clone that repository and copy ``kernel-qemu``::

    $ git clone git@github.com:polaco1782/raspberry-qemu.git
    $ cp raspberry-qemu/kernel-qemu .

At this point, booting should be possible. To test, first install
``qemu-system-arm``.

If you're on Fedora::

    $ sudo dnf install qemu-system-arm

Or Debian/Ubuntu::

    $ sudo apt install qemu-system-arm

Then run::

    $ qemu-system-arm \
        -kernel kernel-qemu \
        -cpu arm1176 \
        -m 256 \
        -M versatilepb \
        -no-reboot \
        -serial stdio \
        -display none \
        -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" \
        -net user,hostfwd=tcp::10022-:22 \
        -net nic -hda \
        2015-11-21-raspbian-jessie-lite.img

Note the option ``-net user,hostfwd=tcp::10022-:22``. This forwards port 22 on
raspbian to 10022 on the host, allowing us to ssh into the booted VM.

You should see some output similar to::

    pulseaudio: pa_context_connect() failed
    pulseaudio: Reason: Connection refused
    pulseaudio: Failed to initialize PA contextaudio: Could not init `pa' audio driver
    ALSA lib confmisc.c:768:(parse_card) cannot find card '0'
    ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
    ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
    ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
    ALSA lib confmisc.c:1251:(snd_func_refer) error evaluating name
    ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
    ALSA lib conf.c:4727:(snd_config_expand) Evaluate error: No such file or directory
    ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM default
    alsa: Could not initialize DAC
    alsa: Failed to open `default':
    alsa: Reason: No such file or directory
    ALSA lib confmisc.c:768:(parse_card) cannot find card '0'
    ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_card_driver returned error: No such file or directory
    ALSA lib confmisc.c:392:(snd_func_concat) error evaluating strings
    ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_concat returned error: No such file or directory
    ALSA lib confmisc.c:1251:(snd_func_refer) error evaluating name
    ALSA lib conf.c:4248:(_snd_config_evaluate) function snd_func_refer returned error: No such file or directory
    ALSA lib conf.c:4727:(snd_config_expand) Evaluate error: No such file or directory
    ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM default
    alsa: Could not initialize DAC
    alsa: Failed to open `default':
    alsa: Reason: No such file or directory
    audio: Failed to create voice `lm4549.out'
    Uncompressing Linux... done, booting the kernel.

Test if a login works::

    $ ssh localhost -o StrictHostKeyChecking=no -p 10022 -l pi

The password should be the default ``raspberry``, unless you changed it
earlier.

If this all works, you can start writing your ``.travis.yml`` to boot this VM
on Travis CI runs. You should first enable travis commit hooks on your
repository (read the `getting started guide
<https://docs.travis-ci.com/user/getting-started/>`_), then start writing a
configuration file. A simple version of the config file to start off:

.. code-block:: python

    language: generic
    sudo: true
    dist: trusty

    before_install:
        - sudo apt-get update
        - sudo apt-get install qemu-system-arm wget xz-utils sshpass

    install:
        - wget "https://super-secret-location.com/2015-11-21-raspbian-jessie-lite.img.xz"
        - unxz "2015-11-21-raspbian-jessie-lite.img.xz"
        - git clone https://github.com/polaco1782/raspberry-qemu.git

    before_script:
        - qemu-system-arm -kernel raspberry-qemu/kernel-qemu -cpu arm1176 -m 256 -M versatilepb -no-reboot -serial stdio -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" -net user,hostfwd=tcp::10022-:22 -net nic -display none -hda 2015-11-21-raspbian-jessie-lite.img &
        - ./test/wait-for-ssh

    script:
        - sshpass -p raspberry ssh localhost -o StrictHostKeyChecking=no -p 10022 -l pi "cat /etc/os-release"
        # whatever you want to test here

You should note this requires a mirror of the image created in the earlier
steps. Each CI run will have to download and decompress the image. With Travis
Pro, I believe you might be able to do something different and cache it, but I
didn't investigate this.

This runs ``qemu-system-arm`` in the background. In order to wait until the VM
is ready, I made a crude script named ``wait-for-ssh`` to ping the ssh port
until it responded:

.. code-block:: bash

    #!/usr/bin/env bash

    while true; do 
        if nc -z localhost 10022 ; then
            echo "Found something on port 10022!"
            exit
        else
            echo "Nothing found on port 10022, sleeping..."
            sleep 10
        fi
    done

When this is done, you can actually test the stuff you wanted to test in the
first place! In the example ``.travis.yml``, I do a sanity check and cat
``/etc/os-release``, expecting something like::

    PRETTY_NAME="Raspbian GNU/Linux 8 (jessie)"
    NAME="Raspbian GNU/Linux"
    VERSION_ID="8"
    VERSION="8 (jessie)"
    ID=raspbian
    ID_LIKE=debian
    HOME_URL="http://www.raspbian.org/"
    SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
    BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"

Now you have a little Raspbian VM booted on every commit. Run some ansible or
puppet against it and you're done. Happy testing!
