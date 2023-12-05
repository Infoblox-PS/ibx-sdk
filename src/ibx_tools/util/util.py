"""
utility function(s) used by any of our classes and other modules
"""
import csv
import io
import logging
import os
import pprint
import subprocess
from urllib.parse import urlparse


def named_checkconf(
        chroot_path: str,
        conf_path: str) -> None:
    """
    perform named-checkconf and re-write a canonicalized copy of the named.conf file

    :param chroot_path: base path or directory to process
    :param conf_path: named.conf file path within the jail
    """
    logging.info('parsing %s conf file', conf_path)

    if not os.path.exists(f'{chroot_path}/{conf_path}'):
        logging.error('%s does not exist', f'{chroot_path}/{conf_path}')
        raise FileNotFoundError
    command = f'sudo named-checkconf -p -t {chroot_path} {conf_path} > name.conf'
    logging.debug(command)
    res = subprocess.run([
        'sudo',
        'named-checkconf',
        '-p',
        '-t',
        chroot_path,
        conf_path
    ], capture_output=True, text=True, check=True)
    if res.stdout:
        with open('named.conf', 'w', encoding='utf8') as file:
            file.write(res.stdout)
    if res.stderr:
        logging.error(res.stderr)


def named_compilezone(
        zone_name: str,
        zone_file: str,
        output_file: str,
        input_format: str = 'text') -> list:
    """
    perform named-compilezone to canonicalize and rewrite the zone file

    :param zone_name: the string value of the zone being processed
    :param zone_file: the string value of the zone file to read/process
    :param output_file: the string value of the canonicalized zone file
    :param input_format: specify current zone format text or raw (default=text)

    :returns: list of lines which produce errors causing the zone to fail
    """
    if input_format not in ['raw', 'text']:
        raise ValueError('specify one of "text" or "raw" value')
    command = f'named-compilezone -k ignore -i none -f {input_format} -o {output_file} ' \
              f'{zone_name} {zone_file}'
    logging.debug(command)
    try:
        subprocess.run([
            'named-compilezone',
            '-k',
            'ignore',
            '-f',
            input_format,
            '-o',
            output_file,
            zone_name,
            zone_file
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as err:
        if int(err.returncode) > 0 and "not loaded due to errors." in err.stdout:
            logging.error('err_code: %s', err.returncode)
            for line in err.stdout.split('\n'):
                if line:
                    logging.error(line)
            return _parse_named_checkzone_log(err.stdout)

        for line in err.stdout.split('\n'):
            if line:
                logging.debug(line)
            return []
    return []


rewrite_zone_file = named_compilezone


def remove_lines_from_file(file_path: str, lines_to_remove: list, output_path: str = None) -> None:
    """
    remove the supplied list of lines from a file

    :param file_path: fully qualified path to file name
    :param lines_to_remove: list of line numbers to remove
    :param output_path: specify path to new file if desire otherwise, same file is modified

    :returns: None
    """
    if not output_path:
        output_path = file_path
    logging.warning('file: %s lines to remove: %s', file_path, lines_to_remove)
    with open(file_path, 'r', encoding='utf8') as fin:
        lines = fin.readlines()
        ptr = 1
        with open(output_path, 'w', encoding='utf8') as fout:
            for line in lines:
                if ptr not in lines_to_remove:
                    fout.write(line)
                else:
                    logging.warning('file: %s - removing line: %s', output_path, line.strip())
                ptr += 1
            logging.info('file %s rewritten', output_path)


def _parse_named_checkzone_log(error_output: str) -> list:
    """
    post-process the error output from named-checkzone and return offending lines

    :param error_output: err.stdout from running named-checkzone on rewriting a zone

    :return: list of the offending line numbers
    """
    line_numbers = []
    error_conditions = [
        'dns_rdata_fromtext',
        'dns_master_load',
    ]
    for line in error_output.split('\n'):
        parts = line.split(':')
        if any(error_condition in line for error_condition in error_conditions):
            line_numbers.append(int(parts[2]))
        if (
                'NS record ' in line and
                ' appears to be an address' in line
        ):
            line_numbers.append(int(parts[1]))
    return line_numbers


def get_csv_header(csvfile: io.TextIOWrapper) -> list:
    """
    fetch CSV header from file using sniffer

    :param csvfile: csv file object
    :return: list of columns in the csv file
    """
    csvfile.seek(0)
    sample = csvfile.read(1024)
    dialect = csv.Sniffer().sniff(sample)
    cols = []
    if csv.Sniffer().has_header(sample):
        csvfile.seek(0)
        myreader = csv.reader(csvfile, dialect)
        cols = next(myreader)
    return cols


def csv_filtered_header(row: dict, col_filter: list = None) -> dict:
    """
    fetches csv required fields for header w/ any other(s) in filter list

    @param row: csv header row with fieldnames
    @param col_filter: list of other columns to filter on
    @return header_object: dictionary of column and index in the header row
    """
    header_object = {}
    items = list(row.keys())
    for col in row:
        if 'header-' in col:
            idx = items.index(col)
            header_object[col] = idx
        elif col.endswith("*"):
            idx = items.index(col)
            header_object[col] = idx
        elif col_filter and col in col_filter:
            idx = items.index(col)
            header_object[col] = idx
    logging.debug(header_object)
    return header_object


def get_csv_from_url(url) -> str:
    """
    return csv file name from download_url

    This method is used to extract the csv file name from the download url

    @param url: Infoblox download url for CSV export
    @return filename: string value of the csv file name
    """
    logging.debug('parsing url: %s', url)
    try:
        obj = urlparse(url)
    except Exception as err:
        logging.error(err)
        raise
    logging.debug(pprint.pformat(obj))
    parts = obj.path.split('/')
    filename = str(parts[-1]).lower()
    logging.debug('parsed filename %s', filename)

    return filename


def ibx_csv_file_split(filename: str, output_path: str = '.'):
    """
    perform CSV file split on globally exported CSV

    @param filename: source CSV file to split by CSV object type(s)
    @param output_path: output path for writing CSV files
    """
    if not os.path.exists(output_path):
        logging.warning(
            'output path %s does not exist, creating...', output_path
        )
        try:
            os.makedirs(output_path, exist_ok=True)
        except Exception as err:
            logging.error(err)
            raise

    # build the struct using the csv object type as the key
    csv_objects = {}
    with open(filename, 'r', encoding='utf8') as handle:
        myreader = csv.reader(handle)
        for row in myreader:
            if row[0].lower().startswith('header-'):
                obj_type = row[0].lower().replace('header-', '')
                csv_output_file = f'{obj_type}.csv'
                csv_output_file_path = os.path.join(
                    output_path, csv_output_file
                )
                csv_objects[obj_type] = {}
                csv_objects[obj_type]['filename'] = csv_output_file
                csv_objects[obj_type]['filepath'] = csv_output_file_path
                csv_objects[obj_type]['data'] = [row]
            else:
                obj_type = row[0].lower()
                csv_objects[obj_type]['data'].append(row)

    # output the struct
    for obj_type, obj_data in csv_objects.items():
        num_of_objects = len(obj_data['data'])
        if num_of_objects == 1:
            logging.warning(
                'skipping creating output file %s, no %s objects',
                obj_data['filename'], obj_type
            )
        else:
            logging.info(
                'creating output file %s with %s %s objects',
                obj_data['filename'], num_of_objects, obj_type
            )
            with open(obj_data['filepath'], 'w', encoding='utf8') as fh_out:
                mywriter = csv.writer(fh_out)
                for row in obj_data['data']:
                    mywriter.writerow(row)
                fh_out.close()


def _get_include_data(chroot: str, include_file: str):
    data = ''
    full_path = f'{chroot}{include_file}'
    if not os.path.exists(full_path):
        logging.error('%s include file does not exist!', full_path)
        return data
    with open(full_path, 'r', encoding='utf8') as file:
        for line in file:
            if 'include ' in line:
                logging.warning('nested include file found in %s', include_file)
                _, _inc_file, _ = line.split('"', 2)
                content = _get_include_data(chroot, _inc_file)
                if content:
                    data += content
            else:
                data += line
        return data


def generate_from_includes(chroot: str, filepath: str) -> str:
    """
    generate a config file from include(s)

    :param chroot: string value of the chroot path
    :param filepath: string value of the path to the initial conf file to process

    :return: string contents of the config file
    """
    if filepath.startswith('/'):
        filepath = filepath.lstrip('/')
    logging.info('processing file %s', f'{chroot}{filepath}')
    data = ''
    if os.path.exists(os.path.join(chroot, filepath)):
        with open(os.path.join(chroot, filepath), 'r', encoding='utf8') as file:
            for line in file:
                if line.startswith('include '):
                    logging.debug(line.strip())
                    _, include_file, _ = line.split('"', 2)
                    logging.info('processing include file %s', include_file)
                    contents = _get_include_data(chroot, include_file)
                    if contents:
                        data += contents
                else:
                    data += line
    else:
        logging.error('file %s does not exist!', os.path.join(chroot, filepath))
    return data
