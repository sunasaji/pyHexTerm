# pyHexTerm
Simple Hex Serial Terminal for pySerial.

# usage
pyhexterm &lt;portname&gt;,&lt;baudrate&gt; [-ip <input_prompt>] [-op <output_prompt>] [-cn <chunk_num>]  
example: pyhexterm COM1,115200

If you need to use other pyserial options (parity,timeout,xonxoff,etc), please add these options to serial.Serial() in this script.
