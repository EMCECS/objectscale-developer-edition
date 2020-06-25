import os
from os import path
from os.path import isfile, join
import subprocess
import re


class cert_utility:
    certs_expected = 4
    powershell = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
    certs_folder = os.getcwd() + '\\certs'
    cert_query_regex = 'Subject.*CN=.*(emc|EMC)'
    thumbprint_query_regex = 'Thumbprint.*: [\d|A-F|a-f]{40}'

    def __init__(self):
        return

    def make_certs_folder(self):
        if not path.exists(os.getcwd() + '\\certs'):
            print('No folder named "certs" found, creating...')
            os.mkdir(os.getcwd() + '\\certs')

    def count_certs(self) -> [int, int]:
        cer_count = 0
        pem_count = 0
        for file in os.listdir(self.certs_folder):
            if path.isfile(path.join(self.certs_folder, file)) and file.find('.pem') > -1:
                pem_count += 1
            if path.isfile(path.join(self.certs_folder, file)) and (file.find('.cer') > -1 or file.find('.crt') > -1):
                cer_count += 1
        return pem_count, cer_count

    def pull_certs(self):
        # Get all certificates installed on the PC and split them by entry.
        result = subprocess.check_output(self.powershell + ' Get-ChildItem Cert:\\ -Recurse', shell=True)
        result = result.decode(encoding='ascii')
        split = result.split("\r\n\r\n")

        # Start a dictionary of the certificates that we want and count them.
        i = 0
        cert_dict = {}
        for item in split:
            i += 1
            if not re.search(self.cert_query_regex, item, re.IGNORECASE) is None:
                lines = item.split("\r\n")
                name = ''
                fingerprint = ''
                for line in lines:
                    if not re.search(self.thumbprint_query_regex, line, re.IGNORECASE) is None:
                        fingerprint = line[-40:]
                    if not re.search(self.cert_query_regex, line, re.IGNORECASE) is None:
                        start = line.find('CN=') + 3
                        end = line.find(',')
                        name = line[start:end]
                        print(name)
                cert_dict[name] = fingerprint

        if len(cert_dict.keys()) < 1:
            print(
                'No certificates found during automatic pull, you must get the following certificates, and place them in the certs folder.')
            print('EMC Root CA')
            print('EMC SSL CA')
            print('EMC SSL Decryption Authority')
            print('EMC SSL Decryption Authority v2')
            print('One may find these certificates by running certmgr.msc, found under'
                  'Trusted Root Certification Authorities/Certificates, and '
                  'Intermediate Certification Authorities/Certificates')
            return

        # For every key, export it to a folder.
        for key in cert_dict.keys():

            try:
                result = subprocess.check_output(
                    self.powershell + ' $cert = Get-ChildItem -Path cert:\\CurrentUser\\*\\' + cert_dict[key]
                    + ';Export-Certificate -Cert $cert[0] -FilePath \"' + self.certs_folder + key.replace(' ',
                                                                                                          '_') + '.cer\" -Type cer',
                    shell=True)
                result = result.decode(encoding='ascii')
            except:
                print(result)
                continue

        print(str(len(cert_dict.keys())) + ' unique certificates found.')
