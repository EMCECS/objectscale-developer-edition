import os
from os import path
import subprocess
import re
import importlib
import shutil


class cert_utility:
    certs_expected = 4
    powershell = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
    certs_folder = '\\certs'
    working_folder = os.path.dirname(os.path.realpath(__file__))[:-8]
    cert_query_regex = 'Subject.*CN=.*(emc|EMC)'
    thumbprint_query_regex = 'Thumbprint.*: [\d|A-F|a-f]{40}'

    def __init__(self, regex):
        self.certs_folder = self.working_folder + '\\certs'
        self.cert_query_regex = regex
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
            print(
                'No certificates found during automatic pull, you must get the following certificates, and place them in the certs folder.')
            print('EMC Root CA')
            print('EMC SSL CA')
            print('EMC SSL Decryption Authority')
            print('EMC SSL Decryption Authority v2')
            print('One may find these certificates by running certmgr.msc, found under'
                  'Trusted Root Certification Authorities/Certificates, and '
                  'Intermediate Certification Authorities/Certificates.')
            return

        print(str(len(cert_dict.keys())) + ' unique certificates found.')
        print('Exporting certificates, this may take a minute.')
        # For every key, export it to the certs folder.
        for key in cert_dict.keys():
            cerfile = path.join(self.certs_folder, key.replace(' ', '_') + '.cer')
            pemfile = path.join(self.certs_folder, key.replace(' ', '_') + '.pem')

            # If neither the cer file nor the pem file exists OR the force flag is specified.
            if not (path.exists(cerfile) or path.exists(pemfile)) or force:
                try:
                    # Export the certificate.
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
                               '\"' + self.certs_folder + '\\' + key.replace(' ', '_') + '.cer\"',
                               '-Type',
                               'cer']
                    result = subprocess.check_output(command, shell=True)
                except:
                    continue
            elif not force:
                print(key.replace(' ', '_') + '.cer already exists, skipping.')

    def convert_certs(self):
        openSSL = importlib.import_module('OpenSSL')

        file_type_in = openSSL.crypto.FILETYPE_ASN1
        file_type_out = openSSL.crypto.FILETYPE_PEM

        files = os.listdir(self.certs_folder)
        cerfiles = []
        for file in files:
            if file.find('.cer') > -1 or file.find('crt') > -1:
                cerfiles.append(file)
        for cerfile in cerfiles:
            pemfile = cerfile[:-4] + '.pem'
            cer = openSSL.crypto.load_certificate(file_type_in, open(self.certs_folder + '\\' + cerfile, 'rb').read())
            pem_file = open(self.certs_folder + '\\' + pemfile, 'wt')
            pem_file.write(openSSL.crypto.dump_certificate(file_type_out, cer).decode('utf-8'))

        print('Successfully converted '+str(len(cerfiles))+' certificates to PEM format.')

    def move_certs_to_minikube(self):
        minikube_cert_path = path.join(os.getenv('HOMEPATH'), '.minikube', 'files', 'etc', 'ssl', 'certs')
        # Creates the certs folder if it does not exist.
        if not path.exists(minikube_cert_path):
            os.makedirs(minikube_cert_path)

        # Find all pem files in the certs folder.
        files = os.listdir(self.certs_folder)
        pemfiles = []
        for file in files:
            if file.find('.pem') > -1:
                pemfiles.append(file)
        for pemfile in pemfiles:
            shutil.copy2(path.join(self.certs_folder, pemfile), path.join(minikube_cert_path, pemfile))

        print('Copied '+str(len(pemfiles))+' cert files to minikube config folder.')

