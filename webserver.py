# ---------------------------------------------------------------------------
#
#            Demo of web server using uasyncio - main webserer code
#                                                                   25 Dec 20
# ---------------------------------------------------------------------------

import usocket as socket
import uasyncio as asyncio
import uselect as select
#import ujson


# ----------------------------------------------
# st up gpio pin 2, the onboard led on esp8266
# ----------------------------------------------

from machine import Pin
led = Pin(2, Pin.OUT)
led.value(1)


# ----------------------------------------------
# server class
# ----------------------------------------------

class Server:
    
    # ----------------------------------------------
    # set up the socket server (web server)
    # ----------------------------------------------
    # see: https://docs.micropython.org/en/latest/library/usocket.html

    async def run(self, loop, port=80):
        addr = socket.getaddrinfo('0.0.0.0', port, 0, socket.SOCK_STREAM)[0][-1]
        s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # server socket
        s_sock.settimeout(4)                                        # blocking timeout
        s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_sock.bind(addr)
        s_sock.listen(5)
        self.socks = [s_sock]                      # List of current sockets for .close()
        print('Awaiting connection on port', port)
        poller = select.poll()
        poller.register(s_sock, select.POLLIN)
        client_id = 1                              # For user feedback
        while True:
            res = poller.poll(1)                   # 1ms block
            if res:                                # Only s_sock is polled
                c_sock, _ = s_sock.accept()        # get client socket
                loop.create_task(self.run_client(c_sock, client_id))
                client_id += 1
            await asyncio.sleep_ms(200)            # yield point (delay 200ms)
            

    # ----------------------------------------------
    # Deal with a new web page client connection
    # ----------------------------------------------

    async def run_client(self, sock, cid):
        print('Client {} connected.'.format(cid))
        request = ""
        try:
            request = sock.recv(1024)                              # receive request from client (max 1024 bytes)
        except OSError:
            print("ERROR: No reply received")
        request = str(request)
        #print(request)
        if request.find('/test') == 6: 
            self.testpage(sock, request)                       # test web page requested
        else:
            self.rootpage(sock, request)                       # root web page requested
        print('Client {} disconnected.'.format(cid))
        sock.close()
        

    # ----------------------------------------------
    # close sockets
    # ----------------------------------------------

    def close(self):
        print('Closing {} sockets.'.format(len(self.socks)))
        for sock in self.socks:
            sock.close()
            

    # ----------------------------------------------
    # test web page requested
    # ----------------------------------------------

    def testpage(self, sock, request):
        print("Test page requested")
        html = """
            <html>
            <head>
                <title>ESP Web Server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="icon" href="data:,">
            </head>
            <body>
                <h1>Test page</h1>
            </body>
            </html>"""
        try:
            sock.send(html)  
        except OSError:
            print("ERROR: sending reply to client (test)")
        

    # ----------------------------------------------
    # root web page requested
    # ----------------------------------------------

    def rootpage(self, sock, request):
        global led       # ensure the led variable used is the global one
        print("Root page requested")
        gpio_state = "OFF"
        if request.find('/?led=on') == 6:
            gpio_state = "ON"
            print('LED TURNED ON')
            led.value(0)
        if request.find('/?led=off') == 6:
            print('LED TURNED OFF')
            led.value(1)
        html = """
            <html>
            <head>
                <title>ESP Web Server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="icon" href="data:,">
                <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
                    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
                    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
                    .button2{background-color: #4286f4;}
                </style>
            </head>
            <body>
                <h1>ESP Web Server</h1>
                <p>GPIO state: <strong>""" + gpio_state + """</strong></p>
                <p><a href="/?led=on"><button class="button">ON</button></a></p>
                <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
            </body>
            </html>"""
        try:
            sock.send(html)  
        except OSError:
            print("ERROR: sending reply to client (root)")
        
        
# ---------------------------------------------------------------------------
#end
