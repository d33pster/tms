#!/usr/bin/env python3

# import modules
from time import sleep
from os import system, getcwd, chdir, remove, mkdir
from os.path import join, exists, expanduser
from os import name as n
from shutil import rmtree
from platform import system as getsys

# get directory info 
currentDirectory = getcwd()
mainDirectory = join(currentDirectory, 'main')
if not getsys() == 'Windows':
    # get dir info
    home = expanduser('~')
    local_bin = join(home, '.local-bin')
    # check for .local-bin in Linux and macOS
    if not exists(local_bin):
        mkdir(local_bin)
        system('echo \"export $')

#change dir
chdir(mainDirectory)

# clear screen
system('cls') if 'nt' in n else system("clear")

# check for pyinstaller
print('Checking for Pyinstaller...', end='')
sleep(1)
print('\n')
system('pip install pyinstaller')
sleep(2)

# Install tms-simple...
print('\nInstalling tms-simple ... ', end='')
sleep(1)
print('\n')
system('pyinstaller --onefile tms-simple.py --windowed -i pp-app.ico')
rmtree(join(mainDirectory,'build'))
remove(join(mainDirectory, 'tms-simple.spec'))
