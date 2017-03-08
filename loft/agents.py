import subprocess


def rsync_backup(config=False, source="", dest="", logger="", options='avr'):
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
    job = subprocess.run(_cmd, shell=False, stdout=subprocess.PIPE)

    if job.returncode == 0:
        logger.info(job.stdout.decode("utf-8"))
        return True
    else:
        return False


def agent_picker(agent):
    # Add agents to dictionary so it is exported to the main program
    return {
        "rsync": rsync_backup
    }.get(agent, rsync_backup) # rsync_backup is default fallback
