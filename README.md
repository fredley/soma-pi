#soma-pi

A frontend for a [SomaFM](http://somafm.com/) Pi Jukebox. Soma-pi will provide a web-frontend that can be used to select a station. It'll work with any internet radio stream, but comes with SomaFM streams out of the box. You'll need to hook up your Pi to some speakers. The design is responsive, and should look nice on your phone/tablet as well as your desktop computer.

![Screenshot](http://i.imgur.com/iuM1yir.png)

###Setup/Installation:

* Not covered in this guide: Setting up ssh/wireless/sound card. These topics are covered in this [lifehacker guide](http://lifehacker.com/5978594/turn-a-raspberry-pi-into-an-airplay-receiver-for-streaming-music-in-your-living-room).
* Assuming you've got the Pi set up as you want, you'll need to install the required tools:  
`sudo apt-get install mpd mpc python-mpd python-setuptools screen`
* Test that `mpc` is working by entering the command `sudo mpc`. You should see output like  
*volume: 80%   repeat: off   random: off   single: off   consume: off*  
There are [futher instructions for setting up/testing mpc](http://www.gmpa.it/it9xxs/?p=727) if you want them.
* Next you'll need to use `easy_install` to install Django:  
`sudo easy_install django`
* Now clone this repository:  
`git clone git://github.com/fredley/soma-pi.git`  
`cd soma-pi`
* Now set up the Django app with the following commands. This will create the database:  
`./manage.py syncdb`  
During this step you will be asked for a superuser name and password. You can use these to access the admin should you want to.
* [optional] This will pre-populate the database with all of the SomaFM stations :  
`./manage.py init_soma`
* You're now ready to roll! Start up a screen by typing `screen`. Running the server in the screen means that it will keep running after `ssh` is disconnected. You need to use `sudo` for this command if you want to use port 80 (recommended).  
`sudo ./manage.py runserver 0.0.0.0:80` 
* You should now be able to access soma-pi from your web browser, point it at the IP of your Pi. You can go to `http://192.168.pi.ip/admin` and log in with your credentials to access the admin.
* Setting up a better web server is left as an excercise for the enthusiast. I can personally recommend [gunicorn](http://gunicorn.org/).
* **Bonus Pebble Round** If you have [Glance for Pebble](http://www.finebyte.co.uk/?page_id=9) you can configure [Tasker](http://tasker.dinglisch.net/) to operate Soma-Pi with your watch buttons. Simply set up tasks according to [Christopher Stein's guide](https://plus.google.com/u/0/109925457418000128828/posts/WKjzY7rktKz), using the `HTTP GET` action and entering the URL to be (for example) `192.168.pi.ip/random` or `192.168.pi.ip/stop` conditional on `%key`. Congratulations, you have now glimpsed geekvana.
