import os.path
import subprocess


def rsync_backup(config=None, source="", dest="", logger=None, options='avr'):
    cmd = 'rsync'

    if config:
        source = config.source
        # If no remote host backup will be local
        if config.dest_host:
            dest = config.dest_host + ':' + config.dest_location
        else:
            dest = config.dest_location
        options = config.options

    _cmd = [cmd, '-' + options, source, dest]
    logger.debug('Starting rsync subprocess')
    job = subprocess.run(_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if job.returncode == 0:
        logger.debug(job.stdout.decode("utf-8"))
        return True
    else:
        logger.error("Something failed: ")
        logger.debug(job.stdout.decode("utf-8"))
        return False


def rclone_backup(config=None, source="", dest="", logger=None, options='--transfers 10'):
    paths = ['/usr/sbin/rclone', '/usr/bin/rclone', '/snap/bin/rclone']
    for path in paths:
        if os.path.isfile(path):
            cmd = path
            logger.debug('Using the %s executabale' % cmd)
            break
        # If last entry in paths is not found it is time to fail
        elif path == paths[-1]:
            logger.error('Cannot find rclone executable')
            return False

    if config:
        source = config.source
        dest = config.remote_name + ':' + config.remote_location
        options = config.options
        _cmd = [cmd, 'sync', source, dest]
        # Inserting options into command array
        _cmd[2:2] = options.split()
    else:
        logger.error("Config file required at this point")
        return False

    job = subprocess.run(_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if job.returncode == 0:
        logger.debug(job.stdout.decode("utf-8"))
        return True
    else:
        logger.error("Something failed: ")
        logger.debug(job.stdout.decode("utf-8"))
        return False


def agent_picker(agent):
    return agent_declaration.get(agent, rsync_backup) # rsync_backup is default fallback

# Add agents to dictionary so it is exported to the main program
agent_declaration = {
        "rsync": rsync_backup,
        "rclone": rclone_backup
    }
