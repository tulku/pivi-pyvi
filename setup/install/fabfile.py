# This script assumes that the Rpi is already running raspbian.
from fabric.operations import sudo, run, put, reboot
from fabric.api import task, cd, env, settings

DEBS_MAIN = 'git python-serial python-pip lighttpd supervisor fabric'

PIP_MODS = ['flup', 'web.py']

GIT_ROOT = 'git@bitbucket.org:less-is-more/'

# Sudo password
env.password = 'raspberry'


@task
def from_tulku():
    """
    Uses tulku's fork for deployment. This is used to test updates
    before merging into trimaker repos.
    """
    global GIT_ROOT
    GIT_ROOT = 'git@bitbucket.org:tulku/'


@task
def install():
    """
    Install all needed software to run the Trimaker printer.
    It assumes that the filesystem is already expanded.
    """
    # Copies the deployment ssh key
    copy_sshid()
    # Install deb packages in main
    debian_main()
    # Install packages from pip
    pip_all()
    # Clone and install pimaker software
    install_pivi()
    # Reboot rpi
    reboot(wait=60*5)


def copy_sshid():
    put('keys/*', '/home/pi/.ssh/')
    run('chmod og-r /home/pi/.ssh/id_rsa')


def copy_configs():
    sudo('shopt -s dotglob; cp -R /home/pi/src/configs/* /')


def install_pivi():
    git_get('pivi-code', 'src')
    sudo('cd /home/pi/src/pyvi/; python setup.py install')
    sudo('cd /home/pi/src/webserver/; chown -R www-data:www-data *')
    sudo('update-rc.d lighttpd defaults')
    # Install custom configuration
    copy_configs()

# Apt methods
def debian_main():
    debian_install(DEBS_MAIN)


def debian_install(pkgs):
    sudo('apt-get -q update')
    sudo('apt-get install --no-upgrade -qy %s' % pkgs)


# Pip methods
def pip_all():
    """ Installs all the required pip packages."""
    for pkg in PIP_MODS:
        pip(pkg)


def pip(pkg):
    sudo('pip install -q %s' % pkg)


# Git methods
def git_get(name, dest=None):
    """
    Clones or updates a hg repo in pi home folder.
    """
    if dest is None:
        dest = name
    url = GIT_ROOT + name
    code_dir = '/home/pi/' + dest
    # On the first run it will clone and then fetch.
    # the fetch step is not needed right after cloning
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run('git clone %s %s' % (url, code_dir))
    with cd(code_dir):
        run('git pull origin master')
