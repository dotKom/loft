import subprocess

def du(path):
    du = subprocess.run(["du", "-sb", path], stdout=subprocess.PIPE)
    # Decode binary string, split return and fetch first entry
    # in array which is the size in bytes
    size = du.stdout.decode().split()[0]


def sanity_checks(config, logger):
    pass