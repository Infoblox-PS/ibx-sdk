#!/usr/bin/env python3
import logging

from infoblox_pslib.logger.ibx_logger import IbxLogger

log = IbxLogger(
    filename='myfile.log',
    filemode='w'
)


def main():
    log.set_level('DEBUG', 'ALL')
    log.info('running %s', __file__)

    log.debug('log DEBUG message to console')
    log.info('log INFO message to console')
    log.warning('log WARNING message to console')
    log.error('log ERROR message to console')
    log.error('log CRITICAL message to console')
    try:
        raise Exception('my sample exception')
    except Exception as err:
        log.exception('log EXCEPTION message to console - %s', err)


if __name__ == '__main__':
    main()
