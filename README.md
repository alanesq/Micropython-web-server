# Micropython-web-server
None blocking webserver for esp8266/esp32

Enter your wifi details in main.py
  wifi_name = "blank"
  wifi_password = "blank"
and it should work with a standard esp8266 or esp32 python board without any additional addins

The idea of this code is to have a web server running along side running other tasks which tends to be what I require for most new esp projects I build.

Video on the concept: https://www.youtube.com/watch?v=tIgu7q38bUw

--------------------------------

main.py = loads on boot
          attaches to wifi and starts the uasyncio loop
          
webserver.py = serves the web pages

maincode.py = The code which runs along side the web server (i.e. main code of the project)

wifimgr.py =  Used to connect to a wifi network without having to suply credentials in the code
              https://github.com/tayfunulu/WiFiManager
              this can be enabled/disabled by commenting out sections in main.py
              

                                                                    alanesq@disroot.org
