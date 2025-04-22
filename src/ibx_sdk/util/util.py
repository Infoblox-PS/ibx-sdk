"""
Copyright 2023 Infoblox

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import csv
import io
import logging
import os
import pprint
import subprocess
from urllib.parse import urlparse


def named_checkconf(chroot_path: str, conf_path: str) -> None:
    """
    perform named-checkconf and re-write a canonicalized copy of the named.conf file

    Args:
        chroot_path (str): Description of the first argument `chroot_path`.
        conf_path (str): Description of the second argument `conf_path`.

    Returns:
        None

    Example:
        Here you can provide an example of how to use your function.
        >>> named_checkconf("/path/to/chroot", "/path/to/conf")
    """

    logging.info("parsing %s conf file", conf_path)

    if not os.path.exists(f"{chroot_path}/{conf_path}"):
        logging.error("%s does not exist", f"{chroot_path}/{conf_path}")
        raise FileNotFoundError
    command = (
        f"sudo named-checkconf -p -t {chroot_path} {conf_path} > name.conf"
    )
    logging.debug(command)
    res = subprocess.run(
        ["sudo", "named-checkconf", "-p", "-t", chroot_path, conf_path],
        capture_output=True,
        text=True,
        check=True,
    )
    if res.stdout:
        with open("named.conf", "w", encoding="utf8") as file:
            file.write(res.stdout)
    if res.stderr:
        logging.error(res.stderr)


def named_compilezone(
    zone_name: str, zone_file: str, output_file: str, input_format: str = "text"
) -> list:
    """
    The function named_compilezone performs the named-compilezone command to canonicalize and
    rewrite a specified DNS zone file, checking for errors in the file during the process.

    Args:
        zone_name (str): The name of the DNS zone being processed.
        zone_file (str): The path to the file containing the DNS zone information to be
                         read/processed.
        output_file (str): The path where the canonicalized zone file will be written to.
        input_format (str, optional): The format in which the zone information is currently
                                      presented in the zone file.
                                      This should be either 'text' or 'raw'. Defaults to 'text'.

    Returns:
        list: A list of strings, each string being a line from the output of the named-compilezone
            command that indicates an error which prevented the DNS zone from being loaded.
            If there are no such errors, an empty list is returned.

    Raises:
        ValueError: If `input_format` is neither 'text' or 'raw'

    Usage:
        Call this function to check for, log, and return errors in a DNS zone file as it is being
        processed:
        >>> errors = named_compilezone('my_zone', '/path/to/my_zone_file', '/path/to/output_file')
        >>> if errors:
        ...     print('Errors found during zone processing.')
        ...     for error in errors:
        ...         print(error)
    """

    if input_format not in ["raw", "text"]:
        raise ValueError('specify one of "text" or "raw" value')
    command = (
        f"named-compilezone -k ignore -i none -f {input_format} -o {output_file} "
        f"{zone_name} {zone_file}"
    )
    logging.debug(command)
    try:
        subprocess.run(
            [
                "named-compilezone",
                "-i", "none",
                "-k", "ignore",
                "-m", "ignore",
                "-n", "ignore",
                "-r", "ignore",
                "-s", "full",
                "-f", input_format,
                "-o", output_file,
                zone_name,
                zone_file,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as err:
        if (
            int(err.returncode) > 0
            and "not loaded due to errors." in err.stdout
        ):
            logging.error("err_code: %s", err.returncode)
            for line in err.stdout.split("\n"):
                if line:
                    logging.error(line)
            return _parse_named_checkzone_log(err.stdout)

        for line in err.stdout.split("\n"):
            if line:
                logging.debug(line)
            return []
    return []


rewrite_zone_file = named_compilezone


def remove_lines_from_file(
    file_path: str, lines_to_remove: list, output_path: str = None
) -> None:
    """
    The function remove_lines_from_file removes specific lines from a file.

    Args:
        file_path (str): The fully qualified path to the file from which lines are to be removed.
        lines_to_remove (list): A list of integers, with each integer being a line
                                number (1-indexed) of the line to be removed from the file.
        output_path (str, optional): Path to the output file. If provided, the function will
                                     write result to this file.
                                     If not provided, the function will overwrite the original
                                     file. Defaults to None.

    Returns:
        None

    Logging:
        This function logs warning messages for each line that it removes from the file.
        It also logs an info message once the file has been successfully rewritten.

    Usage:
        Use this function to remove specific lines from a file:
        >>> remove_lines_from_file('/path/to/my_file', [2, 3])
        This will remove the 2nd and 3rd lines from the file located at /path/to/my_file.

        To write the result to a different file, specify the output_path argument:
        >>> remove_lines_from_file('/path/to/my_file', [2, 3], '/path/to/output_file')
        This will remove the 2nd and 3rd lines from the file located at /path/to/my_file
        and write the result to a file located at /path/to/output_file.
    """

    if not output_path:
        output_path = file_path
    logging.warning("file: %s lines to remove: %s", file_path, lines_to_remove)
    with open(file_path, "r", encoding="utf8") as fin:
        lines = fin.readlines()
        ptr = 1
        with open(output_path, "w", encoding="utf8") as fout:
            for line in lines:
                if ptr not in lines_to_remove:
                    fout.write(line)
                else:
                    logging.warning(
                        "file: %s - removing line: %s",
                        output_path,
                        line.strip(),
                    )
                ptr += 1
            logging.info("file %s rewritten", output_path)


def _parse_named_checkzone_log(error_output: str) -> list:
    """
    post-process the error output from named-checkzone and return offending lines

    :param error_output: err.stdout from running named-checkzone on rewriting a zone

    :return: list of the offending line numbers
    """
    line_numbers = []
    error_conditions = [
        "dns_rdata_fromtext",
        "dns_master_load",
    ]
    for line in error_output.split("\n"):
        parts = line.split(":")
        if any(error_condition in line for error_condition in error_conditions):
            line_numbers.append(int(parts[2]))
        if "NS record " in line and " appears to be an address" in line:
            line_numbers.append(int(parts[1]))
    return line_numbers


def get_csv_header(csvfile: io.TextIOWrapper) -> list:
    """
        The function get_csv_header retrieves the header from a CSV file.

        Args:
            csvfile (io.TextIOWrapper): A file object for the CSV file from which to retrieve the
            header.

        Returns:
            list: A list of strings where each string is a column name from the CSV file's header row.
                If the CSV file has no header row, an empty list is returned.

        Usage:
            Use this function to get the header from a CSV file:
            >>> with open('/path/to/my_file.csv', 'r') as csv_file:
            ...     # noinspection PyTypeChecker
    header = get_csv_header(csv_file)
            ...     print(header)
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
        if "header-" in col:
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


def extract_filename_from_url(url) -> str:
    """
    The function extract_filename_from_url retrieves the name of the CSV file from a given URL.

    Args:
        url (str): An Infoblox download URL for CSV export.

    Returns:
        str: The name of the file that would be downloaded from the specified URL.

    Raises:
        Exception: An exception is raised if the URL cannot be parsed.

    Logging:
        This function logs debug messages as it parses the URL, and an error message if an exception
        was raised while parsing.

    Usage:
        Use this function to retrieve the name of a file from an Infoblox download URL:
        >>> file_name = extract_filename_from_url('https://my-infoblox-instance/export.csv')
    """

    logging.debug("parsing url: %s", url)
    try:
        obj = urlparse(url)
    except Exception as err:
        logging.error(err)
        raise
    logging.debug(pprint.pformat(obj))
    parts = obj.path.split("/")
    filename = str(parts[-1]).lower()
    logging.debug("parsed filename %s", filename)

    return filename


def ibx_csv_file_split(filename: str, output_path: str = "."):
    """
    The function ibx_csv_file_split splits a globally exported CSV file into separate CSV files
    based on the CSV object type(s).

    Args:
        filename (str): The name of the source CSV file to be split.
        output_path (str, optional): The directory where the output CSV files will be written.
            If the directory does not exist, it will be created. Defaults to the current directory.

    Raises:
        Exception: An exception is raised if the output directory cannot be created.

    Logging:
        This function logs warning messages when a CSV object type has no associated objects in
        the source CSV.
        It also logs informational messages when it creates output CSV files.

    Usage:
        Use this function to split a `Infoblox` exported CSV file into separate CSV files for
        each CSV object type:
        >>> ibx_csv_file_split('/path/to/my_exported_csv_file', '/path/to/output_directory')
    """

    if not os.path.exists(output_path):
        logging.warning(
            "output path %s does not exist, creating...", output_path
        )
        try:
            os.makedirs(output_path, exist_ok=True)
        except Exception as err:
            logging.error(err)
            raise

    # build the struct using the csv object type as the key
    csv_objects = {}
    with open(filename, "r", encoding="utf8") as handle:
        myreader = csv.reader(handle)
        for row in myreader:
            if row[0].lower().startswith("header-"):
                obj_type = row[0].lower().replace("header-", "")
                csv_output_file = f"{obj_type}.csv"
                csv_output_file_path = os.path.join(
                    output_path, csv_output_file
                )
                csv_objects[obj_type] = {}
                csv_objects[obj_type]["filename"] = csv_output_file
                csv_objects[obj_type]["filepath"] = csv_output_file_path
                csv_objects[obj_type]["data"] = [row]
            else:
                obj_type = row[0].lower()
                csv_objects[obj_type]["data"].append(row)

    # output the struct
    for obj_type, obj_data in csv_objects.items():
        num_of_objects = len(obj_data["data"])
        if num_of_objects == 1:
            logging.warning(
                "skipping creating output file %s, no %s objects",
                obj_data["filename"],
                obj_type,
            )
        else:
            logging.info(
                "creating output file %s with %s %s objects",
                obj_data["filename"],
                num_of_objects,
                obj_type,
            )
            with open(obj_data["filepath"], "w", encoding="utf8") as fh_out:
                mywriter = csv.writer(fh_out)
                for row in obj_data["data"]:
                    mywriter.writerow(row)
                fh_out.close()


def _get_include_data(chroot: str, include_file: str):
    data = ""
    full_path = f"{chroot}{include_file}"
    if not os.path.exists(full_path):
        logging.error("%s include file does not exist!", full_path)
        return data
    with open(full_path, "r", encoding="utf8") as file:
        for line in file:
            if "include " in line:
                logging.warning("nested include file found in %s", include_file)
                _, _inc_file, _ = line.split('"', 2)
                content = _get_include_data(chroot, _inc_file)
                if content:
                    data += content
            else:
                data += line
        return data


def generate_from_includes(chroot: str, filepath: str) -> str:
    """
    The function generate_from_includes generates a configuration file from include(s) directives
    found in another configuration file.

    Args:
        chroot (str): The path to the chroot environment where the config file to process exists.
        filepath (str): Path to the initial config file to process. The path is relative to
                        chroot if
                            it starts with '/'.

    Returns:
        str: A single string containing the full contents of the config file. This includes data
        from
            the initial config file and all files included with include directives. If the file
            specified
            in the filepath parameter does not exist, an empty string is returned.

    Logging:
        This function logs informational messages indicating the files it's processing and any
        'include'
        directives it encounters. An error message is logged if it attempts to process a file
        that doesn't exist.

    Usage:
        Use this function to generate a full config file from one that includes other files with
        include directives:
        >>> full_config = generate_from_includes('/path/to/chroot', '/path/to/my_config')
    """

    if filepath.startswith("/"):
        filepath = filepath.lstrip("/")
    logging.info("processing file %s", f"{chroot}{filepath}")
    data = ""
    if os.path.exists(os.path.join(chroot, filepath)):
        with open(os.path.join(chroot, filepath), "r", encoding="utf8") as file:
            for line in file:
                if line.startswith("include "):
                    logging.debug(line.strip())
                    _, include_file, _ = line.split('"', 2)
                    logging.info("processing include file %s", include_file)
                    contents = _get_include_data(chroot, include_file)
                    if contents:
                        data += contents
                else:
                    data += line
    else:
        logging.error("file %s does not exist!", os.path.join(chroot, filepath))
    return data
