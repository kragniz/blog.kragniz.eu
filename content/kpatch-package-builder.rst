kpatch-package-builder 0.1.0
############################
:date: 2015-06-29 22:23
:author: Louis Taylor
:category: kpatch
:tags: kernel, centos, gsoc, kpatch
:slug: kpatch-package-builder

As part of `Google Summer of Code
<https://developers.google.com/open-source/gsoc/>`_, I've been working with the
CentOS project to create a delivery and build system to provide easy and
automatic delivery of patches to a running linux kernel. CentOS 7 currently has
support for live patching a running kernel (via the kpatch kernel module and
the surrounding userland tools), but crafting a patch and applying it is a
currently a very manual process. The overall aim of the project is to make
applying kernel fixes an easy and automatic process, which will make it easier
to keep a CentOS installation more secure by without having to schedule
downtime.

As the first part of this project, I've been writing
``kpatch-package-builder``, a tool which generates RPM packages containing a
kernel module which patchs the currently running kernel.  These distributable
packages contain a single kernel patch, so standard package management tools,
such as dnf and yum can install and manage them.

This first version is pretty simple. You create a patch against the source of the
kernel you want to modify, then run ``kpatch-package-builder`` with the patch
name as the last argument. The output can either be a built .rpm file, or the
raw spec.

By default ``kpatch-package-builder`` outputs an RPM .spec file, which can be
used to build the RPM. This is a very simple spec, which just specifies the
name of the package, description, and other common package metadata. The name
of the package currently is based off the patch filename with a prefix of
``kpatch-module-``, which allows these packages to be simply distinguished.
Future versions will have a series of virtual dependencies to prevent patch
collisions, but that's something for a future post.

When given the ``-b`` or ``--build-rpm`` option, ``kpatch-package-builder``
will invoke rpmbuild and build the package in place. The makes the kernel patch
to distributable package a single step.

As an example, creating a package from a patch file:

.. code:: bash

    [vagrant@localhost ~]$ kpatch-package-builder -b livepatch-test.patch 
    kpatch-package-builder: generating spec file...
    kpatch-package-builder: building RPM...
    kpatch-package-builder: writing spec file to /tmp/kpatch_3I6mHJ.spec...
    kpatch-package-builder: writing kpatch-module-livepatch-test-1-1.x86_64.rpm...

The default metadata associated with that generated package:

.. code:: bash

    [vagrant@localhost ~]$ rpm -qip kpatch-module-livepatch-test-1-1.x86_64.rpm 
    Name        : kpatch-module-livepatch-test
    Version     : 1
    Release     : 1
    Architecture: x86_64
    Install Date: (not installed)
    Group       : System Environment/Kernel
    Size        : 281661
    License     : GPLv2
    Signature   : (none)
    Source RPM  : kpatch-module-livepatch-test-1-1.src.rpm
    Build Date  : Wed 24 Jun 2015 15:26:46 EDT
    Build Host  : localhost
    Relocations : (not relocatable)
    Summary     : kpatch livepatch module
    Description :
    Package generated from livepatch-test.patch by kpatch-package-builder

The contents of the package:

.. code:: bash

    [vagrant@localhost ~]$ rpm -qlp kpatch-module-livepatch-test-1-1.x86_64.rpm 
    /var/lib/kpatch/3.10.0-229.el7.x86_64/kpatch-livepatch-test.ko

The current options available:

.. code:: bash

    [vagrant@localhost ~]$ kpatch-package-builder -h
    usage: kpatch-package-builder [-h] [-v] [-o FILE | -b] [-k VERSION] [-a ARCH]
                                  [--set-release NUM] [--set-version NUM] [-d]
                                  PATCH

    Build an RPM package or an RPM spec file to install and manage a kpatch
    livepatch module.

    positional arguments:
      PATCH                 patch file from which to build the livepatch module

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -o FILE, --output FILE
                            name of output spec file
      -b, --build-rpm       build an RPM package
      -k VERSION, --kernel VERSION
                            target kernel version to build the livepatch module
                            against. Defaults to the currently running version
      -a ARCH, --arch ARCH  architecture to compile the patch against
      --set-release NUM     package release version
      --set-version NUM     package version number
      -d, --debug           print debug information

    Usage examples:

    Build an RPM package for a given patch:

        $ kpatch-package-builder --build-rpm module.patch

    Generate a spec file to later build into an RPM:

        $ kpatch-package-builder --output module.spec module.patch


If you want to test this or use it yourself, the code lives at https://github.com/centos-livepatching/kpatch-package-builder.

Future work
-----------

Next up is the rest of the tooling to make building and distributing a series
of patches across a set of kernel versions easy. This will be working on top of
the basic kpatch-package-builder functionality to allow building many versions
of packages for particular kernels.
