#!/usr/bin/env python3
from paramiko import SSHClient, AutoAddPolicy
import optparse

def argements():
    parser = optparse.OptionParser()
    parser.add_option('-u','--username', help='dest file', dest='username')
    parser.add_option('-p','--password', help='password', dest='password')
    parser.add_option('-s', '--server', help='server ip addr', dest='server')

    return parser.parse_args()

(options,args) = argements()
client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())

try:

    client.connect(options.server, username=options.username, password=options.password)
    
    stdin, stdout, stderr = client.exec_command('ls')
    while True:
        command = input('> ')
        stdin, stdout, stderr = client.exec_command(command)

        stdin.write('<?php echo "Hello!"; sleep(2); ?>')
        stdin.channel.shutdown_write()

        # Print output of command. Will wait for command to finish.
        print(stdout.read().decode("utf8")) 
        

        # Get return code from command (0 is default for success)
        if stdout.channel.recv_exit_status() != 0:

            print('Error')
except KeyboardInterrupt:


    # Optionally, send data via STDIN, and shutdown when done

    # Because they are file objects, they need to be closed
    stdin.close()
    stdout.close()
    stderr.close()

    # Close the client itself
    client.close()
