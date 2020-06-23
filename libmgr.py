import os
from os import path
import urllib.request
import subprocess

xargswin_URL = 'https://github.com/manasmbellani/xargswin/releases/download/initial/xargswin.exe'
xargswin_path = 'lib\\xargswin.exe'

pip_url = 'https://bootstrap.pypa.io/get-pip.py'


def get_libs():
    print('Checking libraries..')
    if not path.exists('lib'):
        os.mkdir('lib')
    if not path.exists(xargswin_path):
        print('Downloading XargsWin...')
        local_filename, headers = urllib.request.urlretrieve(xargswin_URL, xargswin_path)

    print('Checking pip installation.')
    # noinspection PyBroadException
    try:
        pip_install_check = subprocess.check_output(['pip3', '--version'], shell=True)
        print('pip installation confirmed.')
    except:
        print('pip not found...')
        print('Installing pip now.')
        local_filename, headers = urllib.request.urlretrieve(pip_url, 'pip.py')
        os.system('python pip.py')
        os.remove('pip.py')

    print('Checking for psutil')
    psutil_install_check = ''
    # noinspection PyBroadException
    try:
        psutil_install_check = subprocess.check_output(['pip3', 'show', 'psutil'], stderr=subprocess.DEVNULL,
                                                       shell=True)
        print('Psutil installed.')
    except:
        print('Psutil not found, installing...')
        os.system('pip3 install psutil')

    print('Checking for certs')
    if not path.exists('certs'):
        print('No certificates exist in certs folder.')
        print('Please put the proper certificates in PEM format into \'certs\'')
    elif len(os.listdir('certs')) == 0:
        print('No certificates exist in certs folder.')
        print('Please put the proper certificates in PEM format into \'certs\'')
    else:
        i = 0
        for file in os.listdir('certs'):
            if file.find('.pem') > -1:
                i += 1
        print('Found '+str(i)+' certs.')

