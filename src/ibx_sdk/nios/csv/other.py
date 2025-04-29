from typing import Optional

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
    import_action: Optional[ImportActionEnum] = Field(
        serialization_alias="import-action",
        default=None,
        description="CSV custom import action",
    )
    name: str = Field(..., description="Name of ACL")
    new_name: Optional[str] = Field(
        None, serialization_alias="_new_name", description="New ACL name"
    )
    comment: Optional[str] = Field(None, description="Optional comment field")
    network_view: Optional[str] = Field(None, description="Network view name")


class NamedACLItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    namedaclitem: str = Field(
        "namedaclitem",
        frozen=True,
        serialization_alias="header-namedaclitem",
        description="CSV header for namedaclitem object",
    )
    import_action: Optional[ImportActionEnum] = Field(
        serialization_alias="import-action",
        default=None,
        description="CSV custom import action",
    )
    parent: str = Field(..., description="Parent ACL name")
    address: str = Field(
        ...,
        description="IP address or network example 192.168.1.0/24/Allow|Deny",
    )
    new_address: Optional[str] = Field(
        None,
        serialization_alias="_new_address",
        description="New address to overwrite address",
    )
    tsig_key: Optional[str] = Field(
        None, description="TSIG key as name/key/algorithm/use_2x_tsig_key"
    )
    new_tsig_key: Optional[str] = Field(
        None, serialization_alias="_new_tsig_key", description="New TSIG key"
    )
    defined_acl: Optional[str] = Field(
        None, description="Pre-defined ACL name to nest"
    )
    new_named_acl: Optional[str] = Field(
        None,
        serialization_alias="_new_named_acl",
        description="New Defined ACL name",
    )
    # comment: Optional[str] = Field(None, description="Optional comment field")
