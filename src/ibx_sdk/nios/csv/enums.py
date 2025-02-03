from enum import Enum


class CreatorEnum(str, Enum):
    SYSTEM = "SYSTEM"
    STATIC = "STATIC"
    DYNAMIC = "DYNAMIC"


class TargetRecordTypeEnum(str, Enum):
    A = "A"
    AAAA = "AAAA"
    MX = "MX"
    NAPTR = "NAPTR"
    PTR = "PTR"
    SPF = "SPF"
    SRV = "SRV"
    TXT = "TXT"


class ZoneFormatTypeEnum(str, Enum):
    FORWARD = "FORWARD"
    IPV4 = "IPV4"
    IPV6 = "IPV6"


class FailoverServerTypeEnum(str, Enum):
    GRID = "GRID"
    EXTERNAL = "EXTERNAL"


class ProtocolTypeEnum(str, Enum):
    IPV4 = "IPV4"
    IPV6 = "IPV6"


class FingerprintTypeEnum(str, Enum):
    STANDARD = "Standard"
    CUSTOM = "Custom"


class HostAddressMatchEnum(str, Enum):
    MAC_ADDRESS = "MAC_ADDRESS"
    CLIENT_IDENTIFIER = "CLIENT_IDENTIFIER"
    RESERVED = "RESERVED"


class MatchOptionEnum(str, Enum):
    MAC_ADDRESS = "MAC_ADDRESS"
    CLIENT_ID = "CLIENT_ID"
    CIRCUIT_ID = "CIRCUIT_ID"
    REMOTE_ID = "REMOTE_ID"


class IPv6AddressTypeEnum(str, Enum):
    ADDRESS = "ADDRESS"
    PREFIX = "PREFIX"
    BOTH = "BOTH"


class LeasePerClientSettingsEnum(str, Enum):
    ONE_LEASE_PER_CLIENT = "ONE_LEASE_PER_CLIENT"
    RELEASE_MATCHING_ID = "RELEASE_MATCHING_ID"
    NEVER_RELEASE = "NEVER_RELEASE"


class ServerAssociationTypeEnum(str, Enum):
    NONE = "NONE"
    MEMBER = "MEMBER"
    FAILOVER = "FAILOVER"


class ImportActionEnum(str, Enum):
    INSERT = "I"
    MERGE = "M"
    OVERRIDE = "O"
    DELETE = "D"
    INSERT_MERGE = "IM"
    INSERT_OVERRIDE = "IO"


class DhcpTypeEnum(str, Enum):
    T_ARRAY_DOMAIN = "T_ARRAY_DOMAIN"
    T_ARRAY_INT8 = "T_ARRAY_INT8"
    T_ARRAY_INT16 = "T_ARRAY_INT16"
    T_ARRAY_INT32 = "T_ARRAY_INT32"
    T_ARRAY_IP_ADDRESS = "T_ARRAY_IP_ADDRESS"
    T_ARRAY_IP_ADDRESS_PAIR = "T_ARRAY_IP_ADDRESS_PAIR"
    T_ARRAY_UINT8 = "T_ARRAY_UINT8"
    T_ARRAY_UINT16 = "T_ARRAY_UINT16"
    T_ARRAY_UINT32 = "T_ARRAY_UINT32"
    T_DOMAIN = "T_DOMAIN"
    T_FLAG = "T_FLAG"
    T_FLAG_IP_ADDRESS = "T_FLAG_IP_ADDRESS"
    T_FLAG_TEXT = "T_FLAG_TEXT"
    T_INT8 = "T_INT8"
    T_INT16 = "T_INT16"
    T_INT32 = "T_INT32"
    T_IP_ADDRESS = "T_IP_ADDRESS"
    T_STRING = "T_STRING"
    T_TEXT = "T_TEXT"
    T_UINT8 = "T_UINT8"
    T_UINT16 = "T_UINT16"
    T_UINT32 = "T_UINT32"
    T_UINT8_1_2_4_8 = "T_UINT8_1_2_4_8"
