# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import time
from queue import Queue
from threading import Thread

from ovos_bus_client.client import MessageBusClient
from ovos_bus_client import Message
from ovos_utils.log import LOG
from ovos_utils.signal import check_for_signal


class EnclosureWriter(Thread):
    """
    Writes data to Serial port.
        # . Enqueues all commands received from Mycroft enclosures
           implementation
        # . Process them on the received order by writing on the Serial port

    E.g. Displaying a text on Mycroft's Mouth
        # . ``EnclosureMouth`` sends a text command
        # . ``EnclosureWriter`` captures and enqueue the command
        # . ``EnclosureWriter`` removes the next command from the queue
        # . ``EnclosureWriter`` writes the command to Serial port

    Note: A command has to end with a line break
    """

    def __init__(self, serial, bus, size=16):
        super(EnclosureWriter, self).__init__(target=self.flush)
        self.alive = True
        self.daemon = True
        self.serial = serial
        self.bus = bus
        self.commands = Queue(size)
        self.val = 0
        self.val0 = 0
        self.val1 = 1
        self.valx = 0
        self.valy = 0
        self.current_pos=[0,20]
        self.signs=[b'\x01', b'\x01']
        self.eye_alphas=[1.0,1.0]
        self.last_col = 'G'
        self.av = 'N'
        
        self.base_colours = {}
        self.base_colours['R'] = [255,0,0]
        self.base_colours['G'] = [0,255,0]
        self.base_colours['B'] = [0,0,255]
        self.base_colours['Y'] = [200,200,0]
        self.base_colours['P'] = [200,0,200]
        self.base_colours['C'] = [0,200,200]
        self.base_colours['W'] = [200,200,200]
        self.base_colours['N'] = [0,0,0]
        self.current_col = self.base_colours[self.last_col]
        
        
        self.start()

    def movement(self, x,y, point=False):
        if point: 
            self.current_pos[0]=x
            self.current_pos[1]=y
        else:
            self.current_pos[0]=self.current_pos[0]+x
            self.current_pos[1]=self.current_pos[1]+y

        if self.current_pos[0]<0:
            self.signs[0]=b'\x01'
        else:
            self.signs[0]=b'\xFF'

        if self.current_pos[1]>0:
            self.signs[1]=b'\x01'
        else:
            self.signs[1]=b'\xFF'

        LOG.info("Movement:" + str(self.current_pos[0]) +" "+ str(self.current_pos[1]) + " " + str(x) + " " +str(y))
        LOG.info("sign x/y:" + str(self.signs[0]) +" " + str(self.signs[1]))
    
    def hsv2rgb(h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    def flush(self):
        while self.alive:
            try:
                cmd = self.commands.get() + '\n'
                #self.serial.write(cmd.encode())
                line = cmd
                print (line)
                sys.stdout.flush()
                if line=='GREEN\n':
                    #self.values = bytearray(['E','G', 1, 0])
                    self.serial.write('E'.encode())
                    self.serial.write('G'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.last_col='G'
                    self.current_col = self.base_colours[self.last_col]
                if line=='YELLOW\n':
                    #self.values = bytearray(['E','Y', 1, 0])
                    self.serial.write('E'.encode())
                    self.serial.write('Y'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.last_col='Y'
                    self.current_col = self.base_colours[self.last_col]
                if line=='RED\n':
                    #self.values = bytearray(['E','R', 1, 0])
                    self.serial.write('E'.encode())
                    self.serial.write('R'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.last_col='R'
                    self.current_col = self.base_colours[self.last_col]
                if line=='BLUE\n':
                    #self.values = bytearray(['E','B', 1, 0])
                    self.serial.write('E'.encode())
                    self.serial.write('B'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.last_col='B'
                    self.current_col = self.base_colours[self.last_col]
                if line=='CIAN\n':
                    #self.values = bytearray(['E','C', 1, 0])
                    self.serial.write('E'.encode())
                    self.serial.write('C'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.last_col='C'
                    self.current_col = self.base_colours[self.last_col]
                if line=='PINK\n':
                    #self.values = bytearray(['E','P', 1, 0])
                    self.serial.write('E'.encode())
                    self.serial.write('P'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.last_col='P'
                    self.current_col = self.base_colours[self.last_col]
                if line=='WHITE\n':
                    #self.values = bytearray(['E','W', 1, 0])
                    self.serial.write('E'.encode())
                    self.serial.write('W'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.last_col='W'
                    self.current_col = self.base_colours[self.last_col]
                if line=='NONE\n':
                    #self.values = bytearray(['E','N', 1, 0])
                    self.serial.write('E'.encode())
                    self.serial.write('N'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                    self.last_col='N'
                    self.current_col = self.base_colours[self.last_col]
                if line=='OPEN\n':
                    #self.values = bytearray(['T',1])
                    self.serial.write('T'.encode())
                    self.val=1
                    self.serial.write(self.val.to_bytes(1, 'little'))
                if line=='CLOSE\n':
                    #self.values = bytearray(['T',0])
                    self.serial.write('T'.encode())
                    self.val=0
                    self.serial.write(self.val.to_bytes(1, 'little'))
                if line=='HOME\n':
                    #self.values = bytearray(['M',1,0,1,0,0,0])
                    self.av = 'N'
                    self.serial.write('M'.encode())
                    self.val1=1
                    self.val0=0
                    self.current_pos[0]=0
                    self.current_pos[1]=20
                    self.signs[0]=b'\xFF'
                    self.signs[1]=b'\x01'
                    self.serial.write(self.val1.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val1.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                if line=='AVL\n':
                    #self.values = bytearray(['M',1,0,1,0,0,0])
                    if(self.av == 'N'):
                        self.serial.write('M'.encode())
                        self.val1=1
                        self.val0=0
                        self.movement(30,30)
                        self.valx=abs(self.current_pos[0])
                        self.valy=abs(self.current_pos[1])
                        self.serial.write(self.signs[0])
                        self.serial.write(self.valx.to_bytes(1, 'little'))
                        self.serial.write(self.signs[1])
                        self.serial.write(self.valy.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))
                        self.av = 'L'
                    elif(self.av == 'R'):
                        #then should reverse the R and do L 
                        self.serial.write('M'.encode())
                        self.val1=1
                        self.val0=0
                        self.movement(30,-30)
                        self.valx=abs(self.current_pos[0])
                        self.valy=abs(self.current_pos[1])
                        self.serial.write(self.signs[0])
                        self.serial.write(self.valx.to_bytes(1, 'little'))
                        self.serial.write(self.signs[1])
                        self.serial.write(self.valy.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))  
                        self.val1=1
                        self.val0=0
                        self.movement(30,30)
                        self.valx=abs(self.current_pos[0])
                        self.valy=abs(self.current_pos[1])
                        self.serial.write(self.signs[0])
                        self.serial.write(self.valx.to_bytes(1, 'little'))
                        self.serial.write(self.signs[1])
                        self.serial.write(self.valy.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))  
                        self.av = 'L'
                        
                if line=='AVR\n':
                    #self.values = bytearray(['M',1,0,1,0,0,0])
                    LOG.info("AVR current av = "+self.av)
                    if(self.av == 'N'):
                        self.serial.write('M'.encode())
                        self.val1=1
                        self.val0=0
                        self.movement(-30,30)
                        self.valx=abs(self.current_pos[0])
                        self.valy=abs(self.current_pos[1])
                        self.serial.write(self.signs[0])
                        self.serial.write(self.valx.to_bytes(1, 'little'))
                        self.serial.write(self.signs[1])
                        self.serial.write(self.valy.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))
                        self.av = 'R'
                    elif(self.av == 'L'):
                        #then should reverse the L and do R
                        self.serial.write('M'.encode())
                        self.val1=1
                        self.val0=0
                        self.movement(-30,-30)
                        self.valx=abs(self.current_pos[0])
                        self.valy=abs(self.current_pos[1])
                        self.serial.write(self.signs[0])
                        self.serial.write(self.valx.to_bytes(1, 'little'))
                        self.serial.write(self.signs[1])
                        self.serial.write(self.valy.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))  
                        self.val1=1
                        self.val0=0
                        self.movement(-30,30)
                        self.valx=abs(self.current_pos[0])
                        self.valy=abs(self.current_pos[1])
                        self.serial.write(self.signs[0])
                        self.serial.write(self.valx.to_bytes(1, 'little'))
                        self.serial.write(self.signs[1])
                        self.serial.write(self.valy.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))
                        self.serial.write(self.val0.to_bytes(1, 'little'))  
                        self.av = 'R'

                if line=='SHAKE\n':
                    #self.values = bytearray(['M',1,0,1,0,0,0])
                    self.serial.write('M'.encode())
                    self.val1=1
                    self.val0=0
                    self.movement(20,0)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    LOG.info("Shake:" +" "+ str(self.current_pos[0]) +" "+ str(self.current_pos[1]) +" "+ str(self.valx) +" "+ str(self.valy) +" "+ str(self.signs[0]) +" "+ str(self.signs[1]))
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    time.sleep(0.2)
                    self.serial.write('M'.encode())
                    self.movement(-40,0)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    time.sleep(0.2)
                    self.serial.write('M'.encode())
                    self.movement(40,0)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    time.sleep(0.2)
                    self.serial.write('M'.encode())
                    self.movement(-40,0)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    time.sleep(0.2)
                    self.serial.write('M'.encode())
                    self.movement(20,0)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                if line=='NOD\n':
                    #self.values = bytearray(['M',1,0,1,0,0,0])
                    self.serial.write('M'.encode())
                    self.val1=1
                    self.val0=0
                    self.movement(0,30)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    time.sleep(0.3)
                    self.serial.write('M'.encode())
                    self.valx=1
                    self.movement(0,-30)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    time.sleep(0.3)
                    self.serial.write('M'.encode())
                    self.valx=1
                    self.movement(0,30)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    time.sleep(0.3)
                    self.serial.write('M'.encode())
                    self.movement(0,-30)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                if line.find('HSV') != -1:
                    mylist = line.split(":")
                    self.current_col = self.hsv2rgb((float)(mylist[1]), (float)(mylist[2]), (float)(mylist[3]))
                    self.serial.write('C'.encode())
                    self.serial.write(((int)(self.current_col[0])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[1])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[2])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[0])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[1])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[2])).to_bytes(1, 'little'))
                if line.find('COL') != -1:
                    mylist = line.split(":")
                    self.current_col[0]=(int)(mylist[1]) #r
                    self.current_col[1]=(int)(mylist[2]) #g
                    self.current_col[2]=(int)(mylist[3]) #b
                    self.serial.write('C'.encode())
                    self.serial.write(((int)(self.current_col[0])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[1])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[2])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[0])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[1])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[2])).to_bytes(1, 'little'))
                if line.find('SQUINT') != -1:
                    mylist = line.split(":")
                    eye=(str)(mylist[1]) #EYE L/R
                    delta=(int)(mylist[2]) #Change in brighness
                    if eye=='L':                    
                       LOG.info("L has been selected")
                       self.eye_alphas[0]=delta/100
                    else:
                       LOG.info("R has been selected")
                       self.eye_alphas[1]=delta/100
                    self.serial.write('C'.encode())
                    self.serial.write(((int)(self.current_col[0]*self.eye_alphas[0])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[1]*self.eye_alphas[0])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[2]*self.eye_alphas[0])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[0]*self.eye_alphas[1])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[1]*self.eye_alphas[1])).to_bytes(1, 'little'))
                    self.serial.write(((int)(self.current_col[2]*self.eye_alphas[1])).to_bytes(1, 'little'))
                if line.find('MOVE') != -1:
                    self.av = 'N' #Should cancel any aversion I guess
                    mylist = line.split(":")
                    #self.valx=abs((int)(mylist[2])) #the abs seems to kill it...
                    #self.valy=abs((int)(mylist[3]))
                    #self.current_pos[0] = self.valx
                    #self.current_pos[1] = self.valy
                    #if mylist[1]=='1':
                    #    self.signs[0]=b'\x01'
                    #else:
                    #    self.signs[0]=b'\xFF'
                    #if mylist[3]=='1':
                    #    self.signs[1]=b'\x01'
                    #else:
                    #    self.signs[1]=b'\xFF'

                    #Do we still need the signs for this? I'm not sure any more 
                    cx = int(mylist[2])
                    cy = int(mylist[4])
                    LOG.info(f'Moving to {cx} {cy}')
                    self.serial.write('M'.encode())
                    self.val1=1
                    self.val0=0
                    self.movement(cx, cy, True)
                    self.valx=abs(self.current_pos[0])
                    self.valy=abs(self.current_pos[1])
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))

                    # self.serial.write('M'.encode())
                    # self.val1=1
                    # self.val0=0
                    # self.movement(30,30)
                    # self.valx=abs(self.current_pos[0])
                    # self.valy=abs(self.current_pos[1])
                    # self.serial.write(self.signs[0])
                    # self.serial.write(self.valx.to_bytes(1, 'little'))
                    # self.serial.write(self.signs[1])
                    # self.serial.write(self.valy.to_bytes(1, 'little'))
                    # self.serial.write(self.val0.to_bytes(1, 'little'))
                    # self.serial.write(self.val0.to_bytes(1, 'little'))

                    
                    #LOG.info("Current position "+" "+ str(self.current_pos))
                    #self.serial.write('M'.encode())
                    #self.val1=1
                    #self.val0=0
                    #self.serial.write(self.signs[0])
                    #self.serial.write(self.valx.to_bytes(1, 'little'))
                    #self.serial.write(self.signs[1])
                    #self.serial.write(self.valy.to_bytes(1, 'little'))
                    #self.serial.write(self.val0.to_bytes(1, 'little'))
                    #self.serial.write(self.val0.to_bytes(1, 'little'))

                if  line=='\x1b[D\n':
                    self.current_pos[0]=self.current_pos[0]-1

                    if self.current_pos[0]<0:
                        self.signs[0]=b'\x01'
                    else:
                        self.signs[0]=b'\xFF'
                    if self.current_pos[1]>0:
                        self.signs[1]=b'\x01'
                    else:
                        self.signs[1]=b'\xFF'
                    self.serial.write('M'.encode())
                    self.val1=1
                    self.val0=0
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    LOG.info("Current position " +" "+ str(self.current_pos))
                if  line=='\x1b[C\n':
                    self.current_pos[0]=self.current_pos[0]+1


                    self.valx= abs(self.current_pos[0])
                    self.valy= abs(self.current_pos[1])

                    if self.current_pos[0]<0:
                        self.signs[0]=b'\x01'
                    else:
                        self.signs[0]=b'\xFF'
                    if self.current_pos[1]>0:
                        self.signs[1]=b'\x01'
                    else:
                        self.signs[1]=b'\xFF'
                    self.serial.write('M'.encode())
                    self.val1=1
                    self.val0=0
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    LOG.info("Current position "+" "+ str(self.current_pos) +" "+ str(self.valy))
                if  line=='\x1b[A\n':
                    self.current_pos[1]=self.current_pos[1]+1

                    self.valx= abs(self.current_pos[0])
                    self.valy= abs(self.current_pos[1])

                    if self.current_pos[0]<0:
                        self.signs[0]=b'\x01'
                    else:
                        self.signs[0]=b'\xFF'
                    if self.current_pos[1]>0:
                        self.signs[1]=b'\x01'
                    else:
                        self.signs[1]=b'\xFF'
                    self.serial.write('M'.encode())
                    self.val1=1
                    self.val0=0
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    LOG.info("Current position " +" "+ str(self.current_pos))

                if  line=='\x1b[B\n':
                    self.current_pos[1]=self.current_pos[1]-1

                    self.valx= abs(self.current_pos[0])
                    self.valy= abs(self.current_pos[1])

                    if self.current_pos[0]<0:
                        self.signs[0]=b'\x01'
                    else:
                        self.signs[0]=b'\xFF'
                    if self.current_pos[1]>0:
                        self.signs[1]=b'\x01'
                    else:
                        self.signs[1]=b'\xFF'
                    self.serial.write('M'.encode())
                    self.val1=1
                    self.val0=0
                    self.serial.write(self.signs[0])
                    self.serial.write(self.valx.to_bytes(1, 'little'))
                    self.serial.write(self.signs[1])
                    self.serial.write(self.valy.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    self.serial.write(self.val0.to_bytes(1, 'little'))
                    LOG.info("Current position  "+ str(self.current_pos))
                # Taking this from the tama_2019 tama.py file

                self.commands.task_done()
            except Exception as e:
                LOG.error("Writing error: {0}".format(e))
                print(
                    type(e).__name__,          # TypeError
                    __file__,                  # /tmp/example.py
                    e.__traceback__.tb_lineno  # 2
                )

    def write(self, command):
        self.commands.put(str(command))
        

    def stop(self):
        self.alive = False




class EnclosureReader(Thread):
    """
    Reads data from Serial port.

    Listens to all commands sent by Arduino that must be be performed on
    Mycroft Core.

    E.g. Mycroft Stop Feature
        # . Arduino sends a Stop command after a button press on a Mycroft unit
        # . ``EnclosureReader`` captures the Stop command
        # . Notify all Mycroft Core processes (e.g. skills) to be stopped

    Note: A command is identified by a line break
    """

    def __init__(self, serial, bus):
        super(EnclosureReader, self).__init__(target=self.read)
        self.alive = True
        self.daemon = True
        self.serial = serial
        self.bus = bus
        self.start()

        # Notifications from mycroft-core
        self.bus.on("mycroft.stop.handled", self.on_stop_handled)

    def read(self):
        while self.alive:
            try:
                data = self.serial.readline()[:-2]
                if data:
                    try:
                        data_str = data.decode()
                    except UnicodeError as e:
                        data_str = data.decode('utf-8', errors='replace')
                        LOG.warning('Invalid characters in response from '
                                    ' enclosure: {}'.format(repr(e)))
                    self.process(data_str)
            except Exception as e:
                LOG.error("Reading error: {0}".format(e))

    def on_stop_handled(self, event):
        # A skill performed a stop
        check_for_signal('buttonPress')

    def process(self, data):
        # TODO: Look into removing this emit altogether.
        # We need to check if any other serial bus messages
        # are handled by other parts of the code
        if "mycroft.stop" not in data:
            self.bus.emit(Message(data))

        if "Command: system.version" in data:
            # This happens in response to the "system.version" message
            # sent during the construction of Enclosure()
            self.bus.emit(Message("enclosure.started"))

        if "mycroft.stop" in data:
            self.bus.emit(Message("mycroft.stop"))

        if "volume.up" in data:
            self.bus.emit(Message("mycroft.volume.increase",
                                  {'play_sound': True}))

        if "volume.down" in data:
            self.bus.emit(Message("mycroft.volume.decrease",
                                  {'play_sound': True}))

        if "unit.shutdown" in data:
            # Eyes to soft gray on shutdown
            self.bus.emit(Message("enclosure.eyes.color",
                                  {'r': 70, 'g': 65, 'b': 69}))
            self.bus.emit(
                Message("enclosure.eyes.timedspin",
                        {'length': 12000}))
            self.bus.emit(Message("enclosure.mouth.reset"))
            time.sleep(0.5)  # give the system time to pass the message
            self.bus.emit(Message("system.shutdown"))

        if "unit.reboot" in data:
            # Eyes to soft gray on reboot
            self.bus.emit(Message("enclosure.eyes.color",
                                  {'r': 70, 'g': 65, 'b': 69}))
            self.bus.emit(Message("enclosure.eyes.spin"))
            self.bus.emit(Message("enclosure.mouth.reset"))
            time.sleep(0.5)  # give the system time to pass the message
            self.bus.emit(Message("system.reboot"))

        if "unit.setwifi" in data:
            self.bus.emit(Message("system.wifi.setup"))
        if "unit.factory-reset" in data:
            self.bus.emit(Message("system.factory.reset"))  # not in mycroft-core!
        if "unit.enable-ssh" in data:
            # This is handled by the wifi client
            self.bus.emit(Message("system.ssh.enable"))
        if "unit.disable-ssh" in data:
            # This is handled by the wifi client
            self.bus.emit(Message("system.ssh.disable"))

    def stop(self):
        self.alive = False
