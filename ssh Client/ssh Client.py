import paramiko
from Module.MyData import MyData
#
# class ssh:
#     def __init__(self):
#         self.client = paramiko.SSHClient()
#         self.client.load_host_keys()
#         self.client.connect('localhost')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect('127.0.0.1', key_filename='/home/zyy/.ssh/openSSH_private_key')
stdin, stdout, stderr = client.exec_command('ls -l')

# print(dir(stdout))

a = stdout.readlines()
md = MyData(a)
# print('error: ', stderr.readlines())
print(md.column(-2, stop=-1).to_str())
# print([1, 2, 3, 4][-2:-1])
client.close()

# md[-1]
