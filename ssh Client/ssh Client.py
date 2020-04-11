import paramiko
# from Module.MyData import MyData

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect('pc.lan', username='gns3', password='gns3')

stdin, stdout, stderr = client.exec_command('ls -l')
a = stdout.readlines()
# md = MyData(a)
# print(md.column(-2, stop=-1).to_str())
# print([1, 2, 3, 4][-2:-1])

stdin, stdout, stderr = client.exec_command('netstat -npt4')
for i in stdout.readlines():
    print(i[:-2])

client.close()

# md[-1]
