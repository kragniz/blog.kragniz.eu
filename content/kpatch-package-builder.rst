kpatch-package-builder 0.1.0
############################
:date: 2015-06-29 22:23
:author: Louis Taylor
:category: kpatch
:tags: kernel, centos, gsoc, kpatch
:slug: kpatch-package-builder

As part of a larger project to improve the kernel livepatching tooling and
capabilities of CentOS, I've been writing ``kpatch-package-builder``, a tool to
generate RPM packages containing a kernel module to patch the running kernel.

The motivation for writing this is to automate creating distributable packages
containing an individual kernel patch. This package can then be installed and
managed using standard package management tools, like dnf and yum.

This first version is pretty simple. You create a patch against the source of the
kernel you want to modify, then run ``kpatch-package-builder`` with the patch
name as the last argument. The output can either be a built .rpm file, or the
raw spec.

By default, without any arguments, ``kpatch-package-builder`` outputs a .spec
file, which can be used to build the RPM. (something about how the spec
works...)

The ``-b`` option will... (something about binary packages)


Creating a package from a patch file:

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


something about where it's going...
