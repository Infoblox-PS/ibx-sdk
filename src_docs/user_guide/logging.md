# Logging

The logging module `ibx_logger.py` was written to simplify logging operations by reducing
configuration down to a handful of variables.

| Name         | Type | Description                                                                                                                                 | Default |
|--------------|------|---------------------------------------------------------------------------------------------------------------------------------------------|---------|
| console_log  | bool | If True, create and display a colored console logger                                                                                        | None    |
| logfile_name | str  | Specify the name of a file to log to                                                                                                        |         |
| logfile_mode | str  | Specify the mode for the log file. 'a' for append mode or 'w' for write mode.                                                               | 'w'     |
| level        | str  | Specifies the logging level or verbosity. This accepts the following string values 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'          | 'INFO'  |
| num_logs     | int  | Specify the number of logs to retain when using a rotating log file handler instead of standard log file handler.                           | None    |
| max_size     | int  | Specify the maximum size for the log file (in bytes) if you want to use a rotating log file handler instead of a standard log file handler. | None    |

The logger is configured when using the `init_logger` method, and it creates any one of these
logging handlers depending on which parameters to you pass to the method:

- console logger
- standard log file handler
- rotating log file handler

## Console Logger

The Console Logger in the `ibx_logger` is basically a `StreamHandler` which emits logged
messages to *sys.stderr*. It has been enhanced using the `coloredlogs` Python module to output
logs in color.

### Console-Only Logging

To configure the logger to display console logging for viewing runtime logged events on the
console, simply import and run `init_console_logger`.

```python
from ibx_tools.logger.ibx_logger import init_console_logger

log = init_console_logger(level='INFO')
log.info('This is an informational log message')
```

### Console & File Logging

Configure the console logger with either a standard file or rotating file log handler by passing
the `console_log` to the `init_logger` function.

```python
from ibx_tools.logger.ibx_logger import init_logger

log = init_logger(
    logfile_name='mylog.log',
    logfile_mode='w',
    level='INFO',
    console_log=True
)
```

## Standard File Logger

The standard file logger is configured any time `init_logger` is executed and is controlled by
these three variables:

1. logfile_name (required)
2. logfile_mode (default = 'w')
3. level (default = 'INFO')

The simplest way to get started with the `ibx_logger` is to run as follows:

```python
from ibx_tools.logger.ibx_logger import init_logger

log = init_logger(logfile_name='mylog.log')
```

The logger will write messages to a file named 'mylog.log' in **write** mode at level **INFO**.

!!! tip

    When `logfile_mode` is set to 'w' or write mode, the log file set by `logfile_name` is 
    overwritten every time the program calls the logger. If you wish to preserve prior messages each
    time the program/script is executed, simply change `logfile_mode` to 'a' or append mode. The 
    logger will open the logfile and append its messages to the end of the file.

It is possible to set the logging level two (2) ways:

- as part of the initial call to `init_logger`
- update the current logger by setting `set_log_level`

```python
from ibx_tools.logger.ibx_logger import init_logger, set_log_level

log = init_logger(
    logfile_name='mylog.log',
    logfile_mode='w',
    level='INFO'
)

log.info('logger level is currently INFO')
set_log_level(level='DEBUG')
log.info('logger level is now currently set at DEBUG')
```

In the code above, the level is initially set to 'INFO', but later changed to 'DEBUG'. The
ability to do this is handy when crafting CLI scripts. Often times in a CLI script, you want to
provide the user an optional way of increasing the verbosity of logging with a `--debug` option.
This can call the `set_log_level` method to increase logging levels potentially exposing lower
level logging output messages that might be in the code.

## Rotating File Logger

The _ibx_logger.py_ will create a `RotatingFileHandler` which supports rotation of disk log
files any time the user supplies `num_logs` and `max_size` to the `init_logger` method. If these
arguments are not passed to the function, it will only use a `FileHandler` instance.

If you are coding an application for which you expect a significant number of logged messages,
and you need to retain message data over a long period of time, configure the `ibx_logger` as
follows:

```python
from ibx_tools.logger.ibx_logger import init_logger

log = init_logger(
    logfile_name='mylog.log',
    logfile_mode='a',
    num_logs=4,
    max_size=102400000
)
```

This would save up to 4 files in 100mb increments. The logger would write to *mylog.log* until
it got to the `max_size`. The logger closes the file, and a new file is opened for writing. This
repeats until `num_logs`. Once `num_logs` is reached, files become overwritten. The filenames that
would result are:

```shell
mylog.log
mylog.log.1
mylog.log.2
mylog.log.3
mylog.log.4
```
