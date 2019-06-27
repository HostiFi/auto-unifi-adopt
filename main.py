import threading
from Queue import Queue
import paramiko
url = ''
which_command = raw_input("Which mode? set-inform, info, or set-default [info]: ")
if which_command == "set-inform":
    url = raw_input("Enter your set-inform URL [http://p01.hostifi.net:8080/inform]: ")
username_ = raw_input("Enter device username [ubnt]: ")
password_ = raw_input("Enter device password [ubnt]: ")
subnet_ = raw_input("Enter subnet [192.168.1.0]: ")

if url != '':
    url = url
else:
    url = "http://p01.hostifi.net:8080/inform"

if which_command != '':
    which_command = which_command
else:
    which_command = 'info'

if username_ != '':
    USERNAME = username_
else:
    USERNAME = 'ubnt'

if password_ != '':
    PASSWORD = password_
else:
    PASSWORD = 'ubnt'

if subnet_ != '':
    SUBNET = subnet_
else:
    SUBNET = '192.168.1.0'

SUBNET = SUBNET[:-1]
PORT = 22
COMMAND = url

hostnames = []
ips = range(1,254)
for i in ips:
    hostnames.append(SUBNET + str(i))

def info(hostname, output_q):
    print "Starting..."
    print hostname
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname, port=PORT, username=USERNAME, password=PASSWORD)

        stdin, stdout, stderr = client.exec_command("mca-cli <<EOF\ninfo\nquit\nEOF")
        print stdout.read()
    except:
        client.close()
    finally:
        client.close()

def set_default(hostname, output_q):
    print "Starting..."
    print hostname
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname, port=PORT, username=USERNAME, password=PASSWORD)

        stdin, stdout, stderr = client.exec_command("mca-cli <<EOF\nset-default\nquit\nEOF")
        print stdout.read()
    except:
        client.close()
    finally:
        client.close()
def set_inform(hostname, output_q):
    print "Starting..."
    print hostname
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname, port=PORT, username=USERNAME, password=PASSWORD)

        stdin, stdout, stderr = client.exec_command("mca-cli <<EOF\nset-inform %s\nquit\nEOF" % (COMMAND))
        print stdout.read()
    except:
        client.close()
    finally:
        client.close()


if __name__ == "__main__":

    output_q = Queue()
    try:
        # Start thread for each router in routers list
        for hostname in hostnames:
            if which_command == "set-inform":
                my_thread = threading.Thread(target=set_inform, args=(hostname, output_q))
            if which_command == "info":
                my_thread = threading.Thread(target=info, args=(hostname, output_q))
            if which_command == "set-default":
                my_thread = threading.Thread(target=set_default, args=(hostname, output_q))
            my_thread.start()

        # Wait for all threads to complete
        main_thread = threading.currentThread()
        for some_thread in threading.enumerate():
            if some_thread != main_thread:
                some_thread.join()

        # Retrieve everything off the queue - k is the router IP, v is output
        # You could also write this to a file, or create a file for each router
    except:
        pass
    while not output_q.empty():
        my_dict = output_q.get()
        for k, val in my_dict.iteritems():
            print k
            print val

wait = raw_input("Press any key to exit...")
