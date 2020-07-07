# Objectscale-Developer-Edition

A tool for automatically setting up and managing a development environment for EMCECS Objectscale for Windows, Linux, and MacOS.

#### Before you set up your development environment:

 * Create a Github developer access token.
 * Install Python 3.
 * Make sure you have an active internet connection.
 * Read the command-line syntax.

### Quickstart Guide:
Note: this will clean your current installation of Minikube and Helm if they are already installed.

 1. Download the zip of this Git
 2. Extract to a folder of choice
 3. Run ```python install.py -t [Github access token] --clean```

If you would like to keep previous configurations for Minikube and Helm:

  ```python install.py -t [Github access token]```

### Command Line Syntax:

 * ```-t```, ```--token```: Your github access token. To create a new token, go to Settings -> Developer settings -> Personal access tokens -> Generate new token. Access at minimum needs 'repo' and 'read:packages' permissions.
 * ```-c```, ```--clean```: Perform a clean installation wherein all dependancies are cleaned, uninstalled, and re-installed. Using this flag with other cleaning and installation flags is redundant.
 * ```-mi```: Perform a clean installation of Minikube, keeping all local files. Used to update Minikube.
 * ```-mc```: Perform a cleaning of Minikube, removing all local files, and recreating the Objectscale configuration. **Will delete all Minikube configurations, use with caution.**
 * ```-hi```: Perform a clean installation of Helm, keeping all local files. Used to update Helm.
 * ```-hc```: Perform a cleaning of Helm, removing all local files, and recreating the Objectscale configuration. **Will delete all Helm configurations, use with caution.**
 * ```-oi```: Perform a clean installation of objectscale on your minikube cluster. Used to update the helm charts. (WIP)
 * ```-oc```: For now, this is the same as OI, but remains an option, as in future releases, this will reset the configuration without uninstalling objectscale (WIP)
 * ```-pc```: Pull Certificates. This is a **windows only** command that can pull the self-signed SSL certificates which will be needed on both minikube and ubuntu systems in order to fetch the docker containers. If this flag is not specified, SSL certificates will need to be added manually to the /certs folder, either in .cer or .pem format.
 * ```-pcf```: Force Pull Certificates. This is another **windows only** command that will pull certificate files, even if they already exist in the file system. Using this can slow down your install time significantly. Note that certificates will be converted from cer to pem on every run, even if the pcf flag is not specified, and a pem file already exists.
 * ```-pcnc```: Pull Certificates No Convert. Another **windows only** command which will prevent the certificates in the certs folder from being converted to PEM format, instead leaving them in the windows naitive .cer format. This is used to pull certificates for a linux based system. this flag itself will **not** cause the installer to pull certificates, and is usually used with the -pc or the -pcf flags. (WIP)
 * ```-pcr```: Certificate pull regex. Defaults to 'Subject.\*CN=.\*(emc|EMC)'. To select a certificate with a certain phrase in the Common Name, it's recommended to use the following regex: 'Subject.\*CN=.\*(<Search Query>).\*,', replacing <Search Query> with said phrase. Should be used alongside ```-pc``` or ```-pcf```, otherwise certificates will not be pulled.