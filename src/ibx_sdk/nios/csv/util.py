import csv
import os
from logging import getLogger

from ibx_sdk.nios.csv.enums import ImportActionEnum

LOG = getLogger(__name__)


def get_header(*, data: list) -> list:
    header = []
    for a in data:
        for col in a.model_dump(
                by_alias=True, exclude_defaults=False, exclude_none=True
        ).keys():
            if col not in header:
                header.append(col)
    LOG.debug(header)
    return header


def output_to_file(
        *,
        filename: str,
        data: list,
        import_action: str = None,
        output_dir: str = None,
        file_prefix: str = None,
) -> None:
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
        LOG.warning("Skipping %s file, no data to write to file", output_file_name)
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
                row.model_dump(by_alias=True, exclude_defaults=False, exclude_none=True)
            )
