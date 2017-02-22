import subprocess


def rsync_backup(source, dest, logger, options='avr'):

    cmd = 'rsync'

    _cmd = [cmd, '-' + options, source, dest]
    job = subprocess.run(_cmd, shell=False, stdout=subprocess.PIPE)

    if job.returncode == 0:
        logger.info(job.stdout.decode("utf-8"))
        return True
    else:
        return False