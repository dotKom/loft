import argparse
import json
import logging
from pprint import pprint

from agents import rsync_backup
from helpers import sanity_check


logger = logging.getLogger('loft')


def build_parser():
    parser = argparse.ArgumentParser(description='loft backup agent')
    # parser.add_argument(
    #     '--state', choices=['master', 'slave'],
    #     help='State to run in'
    # )

    parser.add_argument(
        'agent', choices=['rsync', 'rclone'],
        help='What backup agent to use'
    )

    parser.add_argument(
        '--agent-arguments', type=str, default='',
        help='What arguments loft should pass to the backup agent'
             'See agent manual for help', dest='agent_arguments'
    )

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


def main():
    parser = build_parser()
    try:
        with open('loft/config.json', 'r') as config:
            config = json.load(config)
        pprint(config)

    except FileNotFoundError:
        print('nope')
    args = parser.parse_args()
    print(dir(args))

    logging.basicConfig(filename=args.log + 'backup.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s')

    if args.source and args.dest:
        if args.agent == 'rsync':
            if rsync_backup(args.source, args.dest, logger, options=args.agent_arguments):
                logger.info('Backup completed')
            else:
                logger.error('Backup failed')
            sanity_check(args.source, args.dest, logger)
        else:
            logger.info('Not implemented yet')
    else:
        logger.error('Missing arguments')



if __name__ == '__main__':
    main()
