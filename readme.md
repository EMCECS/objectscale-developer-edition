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