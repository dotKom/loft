import argparse
from dotmap import DotMap
import json
import logging
import os
from pprint import pprint

from agents import agent_picker, rsync_backup
from helpers import sanity_check

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
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
    try:
        with open(os.path.join(__location__, 'config.json'), 'r') as config_file:
            config_file = json.load(config_file)
        # Because we want a "dotable" config traversing
        config = DotMap(config_file)

    except FileNotFoundError:
        # TODO: Build config from args
        # parser = build_parser()
        # args = parser.parse_args()
        print('Args comming soon')
        exit(1)

    logging.basicConfig(filename=config.log_destination + 'backup.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s')
    logger.info('Backup commencing')
    for key, job in config.jobs.items():
        agent = agent_picker(job.agent)
        if agent(config=job, logger=logger):
            logger.info('Backup job %s completed' % key)
        else:
            logger.error('Backup job %s failed' % key)

if __name__ == '__main__':
    main()
