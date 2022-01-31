# working only with python2

from paramiko import SSHClient, AutoAddPolicy
from os.path import expanduser
import re, sys, ipaddress, paramiko

command='/sbin/ip r'
user_name='user'
password=''
hosts=[]
host_file='hosts'

# check for argument (with password)
try:
    password=sys.argv[1]
except:
    print("Missing password")
    sys.exit(1)

# get path to home directory
home_dir=expanduser("~")

# open file with hosts IPs and read all line
fl=open(host_file, 'r')
lines=fl.readlines()
fl.close()

# check every line, if starts with '#' skip it, othwerwise add to list 'hosts'
for line in lines:
    if re.match('^#', str(line)):
       pass
    else:
        ip=line.rstrip('\n')
        # validate if it's IP address
        try:
            ipaddress.ip_address(unicode(ip))
            hosts.append(ip)
        except ValueError:
            print('- - -')
            print(ip+'- not valid IP')

# use of paramiko module
# creat object of SSHClient class and load ssh keys
client = SSHClient()
# load existing keys from home directory
client.load_host_keys(home_dir+'/.ssh/known_hosts')
client.load_system_host_keys()
print(home_dir+'/.ssh/known_hosts')
# auto add keys if missing
client.set_missing_host_key_policy(AutoAddPolicy())

# initiate connection and run command
for host_ip in hosts:
    print('- - -')
    try:
        # connect client
        client.connect(host_ip, username=user_name, password=password, timeout=10)
        # get hostname
        stdin, stdout, stderr = client.exec_command('hostname')
        print(stdout.read().rstrip('\n')+' - '+host_ip)
        # run command and save output to variables
        stdin, stdout, stderr = client.exec_command(command)
        stdout=stdout.read()
        stderr=stderr.read()
        # if there is standard output print it, otherwise printout error output
        if(stdout != ''):
            print(stdout)
        elif(stderr != ''):
            print(stderr)
        else:
            print("No output")
        # close connection
        client.close()
    except paramiko.ssh_exception.AuthenticationException:
        print(host_ip+" - Authentication error")
    except:
        print(host_ip+" - Couldn't connect")
print('- - -')
