import typing


class NameData(typing.Dict):
    name: str


class NetworkData(typing.Dict):
    network_technology: str


class LaunchData(typing.Dict):
    announced: str
    status: str


class BodyData(typing.Dict):
    dimensions: str
    weight: float
    build: str
    sim: str


class DisplayData(typing.Dict):
    type: str
    size: str
    resolution: str
    protection: str


class PlatformData(typing.Dict):
    os: str
    chipset: typing.List[str]
    cpu: typing.List[str]
    gpu: typing.List[str]


class MemoryData(typing.Dict):
    card_slot: str
    internal_memory: str


class MainCameraData(typing.Dict):
    mc_type: str
    mc_details: typing.List[str]
    mc_features: str
    mc_video: str


class SelfieCameraData(typing.Dict):
    sc_type: str
    sc_details: typing.List[str]
    sc_features: str
    sc_video: str


class SoundData(typing.Dict):
    loudspeaker: str
    jack: str


class CommsData(typing.Dict):
    wlan: str
    bluetooth: str
    gps: str
    nfc: str
    radio: str
    usb: str


class FeaturesData(typing.Dict):
    sensors: str
    features_other: typing.List[str]


class BatteryData(typing.Dict):
    battery_type: str
    charging: typing.List[str]
    stand_by: str
    music_play: str


class MiscData(typing.Dict):
    colors: str
    models: str
    price: str


class ImageData(typing.Dict):
    image_url: str
