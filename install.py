# This is the main installation script, meant to be run
# by the developer on any OS to install
import platform
import libmgr
import os
import shutil
import auxillary.arg_cache
import importlib

# TODO: These requirements should be verified.
requirement_cpu_count = 4
requirement_ram_mb = 16384
requirement_ram_mb_free = 10000
requirement_disk_space_mb = 100000


class colorText:
    def __init__(self):
        init = True

    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


# A function designed to check the requirements of the host system.
# This function is agnostic to all OSes and needs to be able to run
# on all supported OSes.
# All of these should be warning messages, except checking disk space.
def check_system_requirements(psutil):
    cpu_count = os.cpu_count()
    ram_mb = psutil.virtual_memory().total / 1000000
    ram_mb_free = psutil.virtual_memory().available / 1000000
    disk_free_space_mb = shutil.disk_usage(os.getcwd())[2] / 1000000

    if cpu_count < requirement_cpu_count:
        print(
            colorText.bold + 'WARNING: Found ' +
            str(cpu_count) + ' logical CPU cores, we recommend at least ' +
            str(requirement_cpu_count) + ' cores.\n'
                                         'Objectscale performance may suffer.' + colorText.reset)
    if ram_mb < requirement_ram_mb:
        print(
            colorText.bold + 'WARNING: Found ' +
            str(ram_mb) + 'MB of RAM, we recommend at least ' +
            str(requirement_ram_mb) + 'MB of RAM.\n'
                                      'Objectscale performance will suffer.' + colorText.reset)
    if ram_mb_free < requirement_ram_mb_free:
        print(
            colorText.bold + 'WARNING: Found ' +
            str(ram_mb_free) + 'MB of free RAM, we recommend at least ' +
            str(requirement_ram_mb_free) + 'MB of free RAM.\n'
                                           'Objectscale performance may suffer.' + colorText.reset)
    if disk_free_space_mb < requirement_disk_space_mb:
        print(
            colorText.bold + 'WARNING: Found ' +
            str(disk_free_space_mb) + 'MB of free Disk Space, we recommend at least ' +
            str(requirement_disk_space_mb) + 'MB of free space.\n'
                                             'Objectscale performance may suffer.' + colorText.reset)
    if disk_free_space_mb * 2 < requirement_disk_space_mb:
        print(
            colorText.bold + 'Error: Disk space much too low to support a development environment. Please allocate '
                             'more free space on your disk (>' + str(requirement_disk_space_mb / 2) + ' total), and then run again.' + colorText.reset)
        exit(112)


def main():
    #Preamble. Things that have nothing to do with installation.
    print(colorText.reset)
    print('Hello, Developer.')
    args = auxillary.arg_cache.parse_cache()
    args = args.parser.parse_args()

    # This section of code is used to fetch and check all prerequisites for this installation process
    # With the exception of Minikube, Docker, Helm, and of course, Objectscale.
    print('-----Libraries & Prerequisites-----')
    manager = libmgr.libmgr()
    manager.get_libs()
    psutil = importlib.import_module('psutil')
    check_system_requirements(psutil)
    print('----- END Libraries & Prerequisites -----')
    if args.versions_query:
        query.list_versions()
        return
    version_query = importlib.import_module('auxillary.version_query')
    query = version_query.version_manager(args.token)
    query.fetch_versions()
    if args.version is not None:
        query.select_version(args.version)

    # Discern the current operating system and run the proper install script for it.
    # The install scripts are imported on the fly to reduce software conflicts.
    os_var = platform.system().casefold()
    try:
        if os_var.find('linux') > -1:
            tux_installer = importlib.import_module('linux.install_linux')
            tux_installer.install_tux(args)
        elif os_var.find('windows') > -1:
            windows_installer = importlib.import_module('windows.install_windows')
            windows_installer.install_win(args, manager.certs_found)
        elif os_var.find('darwin') > -1:
            print('Installation on MacOS is currently unsupported.')
            #mac_installer = importlib.import_module('macos.install_macos')
            #mac_installer.install_mac()
        else:
            print("Error: Unsupported OS: " + os_var)
    except:
        # If for whatever reason we get an exception,
        # Make sure that the color is reset.
        print(colorText.reset)


if __name__ == "__main__":
    main()
else:
    print('Not run in main context.')
