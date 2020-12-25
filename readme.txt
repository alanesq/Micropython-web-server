webserver demo
--------------

main.py = loads on boot
          attaches to wifi and starts the uasyncio loop
          
webserver.py = serves the web pages

maincode.py = The code which runs along side the web server (i.e. main code of the project)

wifimgr.py =  Used to connect to a wifi network without having to suply credentials in the code
              https://github.com/tayfunulu/WiFiManager
              this can be enabled/disabled by commenting out sections in main.py
              

                                                                    alanesq@disroot.org
