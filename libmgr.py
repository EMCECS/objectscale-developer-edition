import os
from os import path
import urllib.request
import subprocess

xargswin_URL = 'https://github.com/manasmbellani/xargswin/releases/download/initial/xargswin.exe'
xargswin_path = 'lib\\xargswin.exe'

pip_url = 'https://bootstrap.pypa.io/get-pip.py'


class libmgr():
    certs_found = False

    def get_libs(self):
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

        print('Checking for psutil.')
        # noinspection PyBroadException
        try:
            subprocess.check_output(['pip3', 'show', 'psutil'], stderr=subprocess.DEVNULL,
                                                           shell=True)
            print('Psutil installed.')
        except:
            print('Psutil not found, installing...')
            os.system('pip3 install psutil')

        print('Checking for OpenSSL.')
        # noinspection PyBroadException
        try:
            subprocess.check_output(['pip3', 'show', 'pyOpenSSL'], stderr=subprocess.DEVNULL,
                                                           shell=True)
            print('OpenSSL installed.')
        except:
            print('OpenSSL not found, installing...')
            os.system('pip3 install pyOpenSSL')



