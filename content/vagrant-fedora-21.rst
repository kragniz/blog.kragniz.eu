Vagrant on fedora 21 and later
##############################
:date: 2015-05-10 22:23
:author: Louis Taylor
:category: fedora
:tags: fedora, vagrant, libvirt
:slug: vagrant-fedora-21

Vagrant is `now packaged
<https://bugzilla.redhat.com/show_bug.cgi?id=1020456>`_ in Fedora 21 and later versions, which is great news.
No more messing around with the horror of rvm!

After installing vagrant and the libvirt plugin with yum::

    $ sudo yum install vagrant vagrant-libvirt

I got some syntax errors from Vagrant::

    $ vagrant up
    /usr/share/vagrant/lib/vagrant/pre-rubygems.rb:19:in `require_relative': /usr/share/vagrant/lib/vagrant/bundler.rb:217: syntax error, unexpected tPOW (SyntaxError)
        def internal_install(plugins, update, **extra)
                                                ^
    /usr/share/vagrant/lib/vagrant/bundler.rb:298: class definition in method body
    /usr/share/vagrant/lib/vagrant/bundler.rb:315: class definition in method body
    /usr/share/vagrant/lib/vagrant/bundler.rb:368: syntax error, unexpected keyword_end, expecting $end
        from /usr/share/vagrant/lib/vagrant/pre-rubygems.rb:19:in `<main>'


This was caused by rvm having an old version of ruby installed, which is what
was installed when I installed vagrant on this machine initially::

    $ ruby --version
    ruby 1.9.3p545 (2014-02-24 revision 45159) [x86_64-linux]

Luckily you can just::

    $ rvm implode

and everything will be happy, where happy is defined by vagrant running and
having the fewest versions of ruby installed.
