from pexpect import pxssh
import getpass
try:                                                            
    s = pxssh.pxssh()
    hostname = "10.65.6.78" #raw_input('hostname: ')
    username = "comp-proj-13"#raw_input('username: ')
    password = "987"#getpass.getpass('password: ')
    s.login (hostname, username, password)
    s.sendline ('uptime')   # run a command
    s.prompt()             # match the prompt
    print s.before          # print everything before the prompt.
    s.sendline ('echo %s | sudo -S mkdir a1' % (password))
    s.prompt()
    print s.before
    s.sendline ('df')
    s.prompt()
    print s.before
    s.logout()
except pxssh.ExceptionPxssh, e:
    print "pxssh failed on login."
    print str(e)
