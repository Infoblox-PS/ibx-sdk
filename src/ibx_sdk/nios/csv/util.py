import csv
import os
from logging import getLogger

from ibx_sdk.nios.csv.enums import ImportActionEnum

LOG = getLogger(__name__)


def extract_columns(item) -> list:
    """Extract column names from a single item."""
    return item.model_dump(
        by_alias=True, exclude_defaults=False, exclude_none=True
    ).keys()


def get_header(*, data: list) -> list:
    """Generate a unique header from the given data."""
    header_columns = []
    for item in data:
        cols = extract_columns(item)
        for col in cols:
            if col not in header_columns:
                header_columns.append(col)

    LOG.debug(header_columns)
    return header_columns


def output_to_file(
    *,
    filename: str,
    data: list,
    import_action: str = None,
    output_dir: str = None,
    file_prefix: str = None,
) -> None:
    """
    Generate a CSV file from the given data.

    Args:
        filename: csv filename or object name
        data: list of objects
        import_action: optional import-action to be added to the header
        output_dir: output to a specific directory
        file_prefix: optional file name prefix

    Returns:
        None
    """
    if filename.endswith(".csv"):
        output_file_name = filename
    else:
        output_file_name = f"{filename}.csv"

    if file_prefix:
        output_file_name = "-".join([file_prefix, output_file_name])

    if output_dir:
        output_file_name = os.path.join(output_dir, output_file_name)

    LOG.info(
        "Writing Infoblox NIOS %s data to CSV file %s",
        filename,
        output_file_name,
    )

    # if there's no data do not write to file
    if len(data) == 0:
        LOG.warning(
            "Skipping %s file, no data to write to file", output_file_name
        )
        return

    header = get_header(data=data)
    if import_action:
        LOG.debug("Adding import-action to header using %s", import_action)
        header.insert(1, "import-action")

    with open(output_file_name, "w") as f:
        mywriter = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        mywriter.writeheader()
        for row in data:
            if import_action is not None:
                row.import_action = ImportActionEnum(import_action)
            mywriter.writerow(
                row.model_dump(
                    by_alias=True, exclude_defaults=False, exclude_none=True
                )
            )
