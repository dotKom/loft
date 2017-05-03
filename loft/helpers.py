import subprocess


def du(path):
    du = subprocess.run(["du", "-sb", path], stdout=subprocess.PIPE)
    # Decode binary string, split return and fetch first entry
    # in array which is the size in bytes
    size = du.stdout.decode().split()[0]
    return size


def du_remote(host, path):
    du = subprocess.run(["ssh", host, "du", "-sb", path], stdout=subprocess.PIPE)
    size = du.stdout.decode().split()[0]
    return size


def du_check(job):
    source_size = du(job.source)
    dest_size = du_remote(job.dest_host, job.dest_location) if job.dest_host else du(job.dest_location)
    if source_size == dest_size:
        return True
    else:
        return "Sizes are not correct %s vs %s" % (source_size, dest_size)


def sanity_checks(job, logger):
    if job.agent == 'rsync':
        if du_check(job):
            logger.info("correct size")
        else:
            logger.info("brrrt")
