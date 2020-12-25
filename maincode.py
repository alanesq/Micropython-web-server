# ---------------------------------------------------------------------------
#
#               Main code running along side the web server 
#                                                                     25dec20
# ---------------------------------------------------------------------------

from webserver import led                      # import the global led gpio variable
import time
import uasyncio as asyncio
import ntptime, time


async def mainloop():
    
    #settings
    ntp_refresh = 20                           # period to refresh NTP time (in seconds)
    
    global led                                 # ensure variable used is the global one (LED gpio pin)
    ntp_timer = time.ticks_ms()                # timer for periodic NTP time refresh
    while 1:                                   # loop forever
        
        #sample code  
        print("LED status = {}".format(led.value()))
        print("Local time is ", '%02d' % (time.localtime()[3]), ":", '%02d' % (time.localtime()[4]), ":", '%02d' % (time.localtime()[5]), sep="")
    
        
        # < your code here >
    
    
    
    
        
        # refresh time from ntp server periodically
        # note: this can stop everything for a few seconds
        if time.ticks_diff(time.ticks_ms(), ntp_timer) > (ntp_refresh * 1000):
            ntp_timer = time.ticks_ms()        # reset timer
            try:
                ntptime.settime()              # get time from NTP server
            except: 
                print("Error: problem refreshing NTP time")
            else:
                print("NTP time refreshed ok")
        
        ## if lose wifi connection, reboot
        #if not wifi.isconnected():
        #    machine.reset()
            
        await asyncio.sleep_ms(4000)           # yield point (wait 4 seconds)


# ---------------------------------------------------------------------------
#end
