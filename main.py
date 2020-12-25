# ---------------------------------------------------------------------------
#
#                    Demo of web server using uasyncio
#                                                                   25 Dec 20
# ---------------------------------------------------------------------------

print("\n\nWebserver demo")

import uasyncio as asyncio
import network

from maincode import mainloop         # the main loop which runs along side the web server

import webserver                      # the webserver code
server = webserver.Server()           # load the web server class


# ----------------------------------------------
# standard setup 
# ----------------------------------------------


#connect to wifi with specific login details
wifi_name = ""
wifi_password = ""
wlan = network.WLAN(network.STA_IF)    # station
wlan.active(True)
wlan.connect(wifi_name, wifi_password)
while wlan.isconnected() == False:
  pass

"""
# connect to wifi using Wifi_Manager (wifimgr.py)
print ("Using WifiManager to access network - https://github.com/tayfunulu/WiFiManager)
import wifimgr
wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D
"""

print('\n\nConnection successful')
print(wlan.ifconfig())
ap_if = network.WLAN(network.AP_IF)     # access point
ap_if.active(False)                     # turn access point off

# NTP time
# see: https://mpython.readthedocs.io/en/master/library/micropython/ntptime.html
print("Getting NTP time")
import ntptime, time
ntptime.host = "uk.pool.ntp.org"
try:
    ntptime.settime()   
except OSError:
    print("Error: unable to get NTP time")
print("Local time ：%s" %str(time.localtime()))

# esp specific - see: https://docs.micropython.org/en/latest/esp8266/quickref.html
#                     https://docs.micropython.org/en/latest/esp32/quickref.html
import esp
esp.osdebug(None)       # turn off vendor O/S debugging messages
#esp.osdebug(0)          # redirect vendor O/S debugging messages to UART(0)

# standard garbage collection to free up memory
import gc
gc.collect()
    

# ----------------------------------------------
# Main code running along side the web server
# ----------------------------------------------

async def maincode():
    global led                                 # ensure the led variable used is the global one
    while 1:                                   # loop forever
        print("LED status = {}".format(led.value()))
        print("Local time:", time.localtime()[3], time.localtime()[4], time.localtime()[5])
        
        
        # < your code here >
        
        
        
        # if lose wifi connection, reboot
        #if not wifi.isconnected():
        #    machine.reset()
            
        await asyncio.sleep_ms(4000)           # yield point (wait 4 seconds)
    


# ----------------------------------------------
# Set up the asyncio tasks
# ----------------------------------------------
# asyncio tutorial: https://www.youtube.com/watch?v=BI0asZuqFXM

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(server.run(loop))          # run the web server (in webserver.py)
    try:
        loop.run_until_complete(mainloop())     # run the main project code (in maincode.py)
    except KeyboardInterrupt:
        print('Main code interrupted')  
    finally:
        print("Closing")
        server.close()
        loop.close()
    

# ---------------------------------------------------------------------------
#end
