
from pydantic import BaseModel, Field, ConfigDict

from ibx_sdk.nios.csv.enums import ImportActionEnum


class NamedACL(BaseModel):
    model_config = ConfigDict(extra="allow")

    namedacl: str = Field(
        "namedacl",
        frozen=True,
        serialization_alias="header-namedacl",
        description="CSV header for namedacl object",
    )
    import_action: ImportActionEnum | None = Field(
        default=None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Name of ACL")
    new_name: str | None = Field(
        None, serialization_alias="_new_name", description="New ACL name"
    )
    comment: str | None = Field(None, description="Optional comment field")
    network_view: str | None = Field(None, description="Network view name")


class NamedACLItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    namedaclitem: str = Field(
        "namedaclitem",
        frozen=True,
        serialization_alias="header-namedaclitem",
        description="CSV header for namedaclitem object",
    )
    import_action: ImportActionEnum | None = Field(
        default=None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    parent: str = Field(..., description="Parent ACL name")
    address: str = Field(
        ...,
        description="IP address or network example 192.168.1.0/24/Allow|Deny",
    )
    new_address: str | None = Field(
        default=None,
        serialization_alias="_new_address",
        description="New address to overwrite address",
    )
    tsig_key: str | None = Field(
        default=None,
        description="TSIG key as name/key/algorithm/use_2x_tsig_key"
    )
    new_tsig_key: str | None = Field(
        default=None,
        serialization_alias="_new_tsig_key",
        description="New TSIG key"
    )
    defined_acl: str | None = Field(
        default=None,
        description="Pre-defined ACL name to nest"
    )
    new_named_acl: str | None = Field(
        default=None,
        serialization_alias="_new_named_acl",
        description="New Defined ACL name",
    )
    # comment: str | None = Field(None, description="Optional comment field")
