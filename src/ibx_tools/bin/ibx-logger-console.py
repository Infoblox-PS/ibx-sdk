#!/usr/bin/env python3
import logging

from infoblox_pslib.logger.ibx_logger import IbxLogger

log = IbxLogger()


def main():
    log.info('logging an info message to null handler - no output')
    log.add_console_handler()
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
