#!/usr/bin/env python3
# pyhexterm: Simple Hex Serial Terminal for pySerial.
# - usage: pyhexterm <portname>,<baudrate> [-ip <input_prompt>] [-op <output_prompt>] [-cn <chunk_num>]
# - example: pyhexterm COM1,115200
# - If you need to use other pyserial options (parity,timeout,xonxoff,etc), add these options to serial.Serial() in this script.
# SPDX-License-Identifier: BSD-3-Clause
# (C) 2022 Suna.S
import serial
import re
import sys
import argparse

ap = argparse.ArgumentParser(description='Serial Terminal for Hex data')
ap.add_argument('serial_args', help='args for serial.Serial(), separaded by commas. For example: COM1,115200')
ap.add_argument('-ip','--in_prompt', required=False, help='Prompt for input, defaults to "<< "', default="<< ")
ap.add_argument('-op','--out_prompt', required=False, help='Prompt for output, defaults to ">> "', default=">> ")
ap.add_argument('-cn','--chunk_num', required=False, help='Separate outputs by spaces for each CHUNK_NUM characters, defaults to 2.', default=2)

args = ap.parse_args()
serial_args_list=args.serial_args.split(",")
port = serial.Serial(*serial_args_list,parity=serial.PARITY_NONE)
cn=int(args.chunk_num)

print("Enter HEX strings and press Enter to send. Spaces are ignored. Press Ctrl-C to exit.\n"+args.in_prompt,end="")
string=""
while True:
    try:
        c = sys.stdin.read(1)
    #If c is Ctrl-C, then exit
    except KeyboardInterrupt:
        exit()
    #If c is EOF or Ctrl-D, then exit
    if(not len(c) or ord(c)==4):
        exit()
    if(c=='\n'):
        #Remove spaces
        string=re.sub("\s*","",string)
        #Split string by 2 characters
        string_list=re.split('(..)',string)[1::2]
        #Convert hex byte list to bytearray
        string_bytes=bytearray.fromhex(" ".join(string_list))
        port.write(list(string_bytes))
        string=""
        print(args.out_prompt,end="")
        while (port.in_waiting > 0):
            r=port.read().hex()
            string+=r
        #Separate string by spaces for each cn characters
        i=0
        j=cn
        out=""
        for _ in range(-(-len(string)//cn)): #Roundup to integer
            out+=string[i:j]+" "
            i+=cn
            j+=cn
        print(out[:-1]+"\n"+args.in_prompt,end="")
        string=""
    else:
        string+=c
