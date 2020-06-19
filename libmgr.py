from os import path
import urllib.request

xargswin_URL = 'https://github.com/manasmbellani/xargswin/releases/download/initial/xargswin.exe'
xargswin_path = 'lib\\xargswin.exe'

def get_libs():
    print('Checking libraries..')
    if not path.exists(xargswin_path):
        print('downloading XargsWin')
        local_filename, headers = urllib.request.urlretrieve(xargswin_URL, xargswin_path)
