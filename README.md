soma-pi
=======

A frontend for soma-pi, a SomaFM Pi Jukebox. This will provide a web-frontend that can be used to select a stream. You'll need to hook up your Pi to some speakers. The design is responsive, and should look nice on your phone/tablet as well as your desktop computer.

Installation:

* `sudo apt-get install mpd mpc python-mpd python-setuptools`
* `sudo easy_install pip`
* `pip install django`
* `git://github.com/fredley/soma-pi.git`
* `cd soma-pi`
* `./manage.py syncdb`
* `./manage.py init_soma`
* `./manage.py runserver 0.0.0.0:80` - You may want to run this in a screen
