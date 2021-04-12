from enum import Enum
from dataclasses import dataclass


class Headdress(Enum):
    CAP = "CA"
    HAT = "HA"


class Outerwear(Enum):
    PEA_COAT = "PC"
    JACKET = "JA"


@dataclass
class Uniform:
    headdress: Headdress
    outerwear: Outerwear
    milfaculty: str

    @staticmethod
    def from_raw(body) -> "Uniform":
        return Uniform(
            headdress=Headdress(body["headdress"]),
            outerwear=Outerwear(body["outerwear"]),
            milfaculty=body["milfaculty"],
        )
