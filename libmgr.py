import os
from os import path
import urllib.request
import subprocess
import platform

xargswin_URL = 'https://github.com/manasmbellani/xargswin/releases/download/initial/xargswin.exe'
xargswin_path = 'lib\\xargswin.exe'

pip_url = 'https://bootstrap.pypa.io/get-pip.py'


def find_pip(python_path: str) -> str:
    if path.exists(path.join(python_path.replace('python.exe', ''), 'Scripts', 'pip3.exe')):
        return path.join(python_path.replace('python.exe', ''), 'Scripts', 'pip3.exe')
    else:
        return ''


def find_python() -> str:
    if not platform.system().casefold().find('windows') > -1:
        return ''
    else:
        path_x64 = 'C:\\Program Files\\'
        path_x86 = 'C:\\Program Files (x86)\\'
        list_path_x64 = os.listdir(path_x64)
        list_path_x86 = os.listdir(path_x86)
        found_python_path = ''
        for folder in list_path_x64:
            if folder.casefold().find('python') > -1 and path.isdir(path.join(path_x64, folder)):
                found_python_path = path.join(path_x64, folder)
                break
            else:
                continue

        if found_python_path == '':
            for folder in list_path_x86:
                if folder.casefold().find('python') > -1 and path.isdir(path.join(path_x86, folder)):
                    found_python_path = path.join(path_x86, folder)
                    break
                else:
                    continue

    if path.exists(path.join(found_python_path, 'python.exe')):
        return path.join(found_python_path, 'python.exe')
    else:
        return ''


class libmgr():
    certs_found = False
    use_python_path = False
    python_path = ''
    use_pip_path = False
    pip_path = ''

    def get_libs(self):
        print('Checking libraries..')
        if not path.exists('lib'):
            os.mkdir('lib')
        if not path.exists(xargswin_path):
            print('Downloading XargsWin...')
            local_filename, headers = urllib.request.urlretrieve(xargswin_URL, xargswin_path)

        self.get_pip()
        self.get_psutil()
        self.get_openssl()


    def get_pip(self):
        print('Checking pip installation.')
        # noinspection PyBroadException
        try:
            pip_install_check = subprocess.check_output(['pip3', '--version'], stderr=subprocess.DEVNULL, shell=True)
            print('pip installation confirmed.')
        except:
            print('Pip not found in PATH.')
            print('Installing pip now.')
            local_filename, headers = urllib.request.urlretrieve(pip_url, 'pip.py')
            try:
                pip_install_result = subprocess.check_output('python pip.py', stderr=subprocess.DEVNULL, shell=True)
                os.remove('pip.py')
            except:
                if not platform.system().casefold().find('windows') > -1:
                    print('Python not installed properly, please reinstall python, or make sure that the \'python\' command is valid')
                    exit(4)
                print('Python is not in system PATH, attempting to predict a direct path...')
                self.use_python_path = True
                self.python_path = find_python()
                if not self.python_path == '':
                    print('Python found successfully!')
                else:
                    print(
                        'Python not found, despite our best efforts. Make sure you are running with Python 3.0.0 or greater.')
                    exit(2)

                try:
                    print('Installing pip.')
                    pip_install_result = subprocess.check_output('"' + self.python_path + '" pip.py', stderr=subprocess.DEVNULL, shell=True)
                except:
                    print('Error occurred while attempting to install pip. exiting')
                    exit(3)
                finally:
                    print('Pip appears to be already installed. Finding installation path..')
                    self.pip_path = find_pip( self.python_path )
                    if not self.pip_path == '':
                        self.use_pip_path = True
                        print('Pip installation found, but not in PATH. Found at: \r\n'+self.pip_path)
                        print('Important: Be sure to add Pip and Python to your PATH environment variable.')


    def get_psutil(self):
        print('Checking for psutil.')
        pip_command = self.pip_path if self.use_pip_path else 'pip3'
        # noinspection PyBroadException
        try:
            subprocess.check_output([pip_command, 'show', 'psutil'], stderr=subprocess.DEVNULL,
                                    shell=True)
            print('Psutil installed.')
        except:
            print('Psutil not found, installing...')
            subprocess.check_output([pip_command, 'install', 'psutil'],
                                    shell=True)


    def get_openssl(self):
        print('Checking for OpenSSL.')
        # noinspection PyBroadException
        try:
            subprocess.check_output(['pip3', 'show', 'pyOpenSSL'], stderr=subprocess.DEVNULL,
                                    shell=True)
            print('OpenSSL installed.')
        except:
            print('OpenSSL not found, installing...')
            os.system('pip3 install pyOpenSSL')
