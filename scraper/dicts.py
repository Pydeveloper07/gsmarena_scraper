import typing


class NetworkData(typing.TypedDict):
    network: str


class LaunchData(typing.TypedDict):
    announced: str
    status: str


class BodyData(typing.TypedDict):
    dimensions: str
    weight: float
    sim: str


class DisplayData(typing.TypedDict):
    type: str
    size: str
    resolution: str


class PlatformData(typing.TypedDict):
    os: str
    chipset: str
    cpu: str


class MemoryData(typing.TypedDict):
    card_slot: str
    internal: str
