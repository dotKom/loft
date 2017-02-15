import argparse
import logging
import subprocess

cmd = ['rsync', '-avr']

config = {
    'source': {
        'host': '',
        'path': '/home/hernil/cloud/'},
    'destination': {
        'host': 'odin:',
        'path': '/mnt/storage/hernil/testing/'}
}

logger = logging.getLogger('loft')
log_path = ""


def build_parser():
    parser = argparse.ArgumentParser(description='loft backup agent')
    # parser.add_argument(
    #     '--state', choices=['master', 'slave'],
    #     help='State to run in'
    # )

    parser.add_argument(
        '-s', '--source', type=str, default='',
        help='Backup source', dest='source'
    )

    parser.add_argument(
        '-d', '--destination', type=str, default='',
        help='Backup destination', dest='dest'
    )

    parser.add_argument(
        '-l', '--log-destination', type=str, default='/var/log/loft/',
        help='Log file destination', dest='log'
    )

    return parser


def rsync_backup(source, dest):
    source = config['source']
    dest = config['destination']
    _cmd = [cmd[0], cmd[1], source['host'] + source['path'], dest['host'] + dest['path']]
    job = subprocess.run(_cmd, shell=False, stdout=subprocess.PIPE)

    if job.returncode == 0:
        logger.info(job.stdout.decode("utf-8"))
        return True
    else:
        return False


def main():
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(filename=args.log + 'backup.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s')

    if args.source and args.dest:
        if rsync_backup(args.source, args.dest):
            logger.info('Backup completed')
        else:
            logger.info('error')
    else:
        logger.error('Missing arguments')


if __name__ == '__main__':
    main()