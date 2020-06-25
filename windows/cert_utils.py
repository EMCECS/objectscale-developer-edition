import os
from os import path
import subprocess
import re
import argparse


class cert_utility:
    certs_expected = 4
    powershell = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
    certs_folder = '\\certs'
    working_folder = os.path.dirname(os.path.realpath(__file__))[:-8]
    cert_query_regex = 'Subject.*CN=.*(emc|EMC)'
    thumbprint_query_regex = 'Thumbprint.*: [\d|A-F|a-f]{40}'

    def __init__(self):
        self.certs_folder = self.working_folder+'\\certs'
        return

    def make_certs_folder(self):
        if not path.exists(self.certs_folder):
            print('No folder named "certs" found, creating...')
            os.mkdir(self.certs_folder)

    def count_certs(self) -> [int, int]:
        cer_count = 0
        pem_count = 0
        for file in os.listdir(self.certs_folder):
            if path.isfile(path.join(self.certs_folder, file)) and file.find('.pem') > -1:
                pem_count += 1
            if path.isfile(path.join(self.certs_folder, file)) and (file.find('.cer') > -1 or file.find('.crt') > -1):
                cer_count += 1
        return pem_count, cer_count

    def pull_certs(self, force):
        # Get all certificates installed on the PC and split them by entry.
        result = subprocess.check_output(self.powershell + ' Get-ChildItem Cert:\\ -Recurse', shell=True)
        result = result.decode(encoding='ascii')
        split = result.split("\r\n\r\n")

        print('Searching registry...')
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
                cert_dict[name] = fingerprint

        if len(cert_dict.keys()) < 1:
            print('No certificates found during automatic pull, you must get the following certificates, and place them in the certs folder.')
            print('EMC Root CA')
            print('EMC SSL CA')
            print('EMC SSL Decryption Authority')
            print('EMC SSL Decryption Authority v2')
            print('One may find these certificates by running certmgr.msc, found under'
                  'Trusted Root Certification Authorities/Certificates, and '
                  'Intermediate Certification Authorities/Certificates')
            return

        print(str(len(cert_dict.keys())) + ' unique certificates found.')
        print('Exporting certificates, this may take a minute.')
        # For every key, export it to the certs folder.
        for key in cert_dict.keys():
            if force or not path.exists(path.join(self.certs_folder, key.replace(' ','_')+'.cer')):
                try:
                    command = [self.powershell,
                           '$cert',
                           '=',
                           'Get-ChildItem',
                           '-Path',
                           'cert:\\CurrentUser\\*\\' + cert_dict[key],
                           ';',
                           'Export-Certificate',
                           '-Cert',
                           '$cert[0]',
                           '-FilePath',
                           '\"' + self.certs_folder + '\\' + key.replace(' ','_') + '.cer\"',
                           '-Type',
                           'cer']
                    result = subprocess.check_output(command, shell=True)
                except:
                    continue
            elif not force:
                print(key.replace(' ', '_') + '.cer already exists, skipping.')

