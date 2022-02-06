from paramiko import SSHClient, AutoAddPolicy
from os.path import expanduser
import paramiko, re

username = 'user'
password = 'user'
home_dir=expanduser("~")

def ssh_check(host):
    try:
        client.connect(host, username=username, password=password)
        print('{:15} - {}'.format(host, 'Ping'))
    except Exception as err:
        err = re.sub('\[.*?\] ', '', str(err))
        print('{:15} - {}'.format(host, err))
       # print(host+" - "+ err)

client = SSHClient()
client.load_host_keys(home_dir+'/.ssh/known_hosts')
client.load_system_host_keys()
client.set_missing_host_key_policy(AutoAddPolicy())

hosts = ['192.168.2.11', '192.168.2.12', '192.168.2.13', '192.168.2.14', 'node1']

for i in hosts:
    ssh_check(i)
