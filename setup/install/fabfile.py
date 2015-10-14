# This script assumes that the Rpi is already running raspbian.
from string import Template
from fabric.operations import sudo, run, put, reboot
from fabric.api import task, env, settings

DEBS_MAIN = 'git python-serial python-pip lighttpd supervisor fabric python-webpy'
GIT_ROOT = 'https://github.com/LESSIoT/'

# Sudo password
env.password = 'raspberry'

PIVI_ID = "0"
VIRTUAL = "False"
SERVER_IP = "52.11.72.101"


@task
def repo(username='tulku'):
    """
    Uses tulku's fork for deployment. This is used to test updates
    before merging into trimaker repos.
    """
    global GIT_ROOT
    GIT_ROOT = 'https://github.com/{}/'.format(username)
    print GIT_ROOT


@task
def install(pivi_id=PIVI_ID, virtual=VIRTUAL, server_ip=SERVER_IP):
    """
    Install all needed software to run the Trimaker printer.
    It assumes that the filesystem is already expanded.
    """
    # Install deb packages in main
    debian_main()
    # Clone and install pivi software
    install_pivi()
    # Install custom configuration
    replace_config(pivi_id, virtual, server_ip)
    copy_configs()


@task
def reboot_pi():
    """
    Reboots the target host.
    """
    reboot(wait=5)


def copy_configs():
    sudo('shopt -s dotglob; cp -R /home/pi/src/configs/* /')


def replace_config(pivi_id, virtual, server_ip):
    kw = {'PIVI_ID': pivi_id, 'VIRTUAL': virtual,
          'SERVER_IP': server_ip}
    f = open('pivi.cfg.in', 'r')
    template = Template(f.read())
    replaced = template.safe_substitute(kw)
    out = open('pivi.cfg', 'w')
    out.writelines(replaced)
    out.close()
    put('pivi.cfg', '/home/pi/src/configs/etc/pivi.cfg')


def install_pivi():
    git_get('pivi-pyvi', 'src')
    sudo('cd /home/pi/src/pyvi/; python setup.py install')
    sudo('cd /home/pi/src/webserver/; chown -R www-data:www-data *')
    sudo('update-rc.d lighttpd defaults')


# Apt methods
def debian_main():
    debian_install(DEBS_MAIN)


def debian_install(pkgs):
    sudo('apt-get -q update')
    sudo('apt-get install --no-upgrade -qy %s' % pkgs)


# Git methods
def git_get(name, dest=None):
    """
    Clones or updates a hg repo in pi home folder.
    """
    if dest is None:
        dest = name
    url = GIT_ROOT + name + '.git'
    code_dir = '/home/pi/' + dest
    # On the first run it will clone and then fetch.
    # the fetch step is not needed right after cloning
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            pass
        else:
            sudo("rm -rf %s" % code_dir)
    run('git clone %s %s' % (url, code_dir))
