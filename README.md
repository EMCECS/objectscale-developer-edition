# Objectscale-Developer-Edition

### WARNING:
Running this tool may render previous portions of your cluster inoperable! Please only use this utility on a clean installation. If you use minikube, runing `minikube delete` can ensure this is the case.

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

### Quick Command Line Guide
#### Formatting   
Flags are formatted in a subject-verb way, where the first part of a flag represents a subject, and the second part represents an action that can be performed on the subject. If a subject is not provided, the program attempts to execute the verb on all possible subjects.  

#### Special Flags   
There are some flags which don't follow subject-verb grammar, those flags are listed here.   
 * Ram allocation            : --RAM
 * CPU core count allocation : --CPU
 * Storage allocation        : --DISK

#### Subjects  
The following are *Component* subjects, and are valid with component verbs:
 * Minikube      : denoted by 'm'
 * Helm          : denoted by 'h'
 * Objectscale   : denoted by 'o'
 * Docker(Linux) : denoted by 'd'
The following are *Output* subjects, and are valid with output verbs:
 * Certificates (Windows) : denoted by 'pc'
 * Endpoint Credentials   : denoted by 'ec'
The following are *Certificate* subjects, and are valid with the certificate verbs:
 * Certificates (Windows) : denoted by 'pc'  

#### Verbs
Component verbs:
 * Clean          : denoted by 'c'  : Clears all active configuration of the current component. This is a destructive process, so use with caution.
 * Install        : denoted by 'i'  : Uninstalls and reinstalls the specified component. Attempts to keep all active configurations.
Certificate verbs:
 * No Convert     : denoted by 'nc' : Pulled certificates are not to be converted. 
 * Force          : denoted by 'f'  : The certificate operations are to be forced if unsucessful
 * Regex          : denoted by 'r'  : Only certificates which match a certain regex should be pulled
Output verbs: 
 * Output enabled : denoted by 'o'  : Enables the output of the selected subject
 * Output to file : denoted by 'f'  : Outputs to a file, as opposed to default command line
 * Output only    : denoted by 'oo' : Disables all installation features, and only produces the selected output(s). This will cause all other non-output flags to be ignored.



### Complete Command Line Syntax:

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
 * ```-pcr```: Certificate pull regex. Defaults to 'Subject.\*CN=.\*(emc|EMC)'. To select a certificate with a certain phrase in the Common Name, it's recommended to use the following regex: 'Subject.\*CN=.\*([Search Query]).\*,', replacing [Search Query] with said phrase. Should be used alongside ```-pc``` or ```-pcf```, otherwise certificates will not be pulled.

### Regex Guide:
Regex is a powerful tool that can be used generally to select text, and in this context, is used to select which certificates are pulled from the store. One can find a quick-guide on how to use regex [here](https://cheatography.com/davechild/cheat-sheets/regular-expressions/pdf/).
The following is an entry which can be used as an example to test regexes on:

    Subject      : CN=Dell Enterprise Root CA, O=Dell Inc.   
    Issuer       : CN=Dell Enterprise Root CA, O=Dell Inc.  
    Thumbprint   : 0D00D5DEFD97CE5CC879358A3164BBF3EE6B25B3  
    FriendlyName :   
    NotBefore    : 11/19/2004 5:17:46 PM  
    NotAfter     : 11/19/2028 5:17:46 PM  
    Extensions   : {System.Security.Cryptography.Oid, System.Security.Cryptography.Oid, System.Security.Cryptography.Oid,  
               System.Security.Cryptography.Oid}

A regex can match any part of these entries in order to be pulled into a file. In the case of the default regex 'Subject.\*CN=.\*(emc|EMC)' searches for 'Subject' followed by 'CN=' followed by either 'emc' or 'EMC'. Regexes are case sensitive, and while 'Subject.\*CN=.\*(emc|EMC)' may match some certificates, 'subject.\*CN=.\*(emc|EMC)' will not match any certificates. While any part of the regex can match to give a certificates, all certificates are named according to their common name.
