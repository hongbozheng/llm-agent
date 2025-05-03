from ...domains.base import Domain
from typing import Type

from ...domains.crypto.domain import Crypto
from ...domains.hft.domain import HFT
from ...domains.real_estate.domain import RealEstate
from ...domains.stock import Stock


DOMAIN_REGISTRY: dict[str, Type[Domain]] = {
    "crypto": Crypto,
    "hft": HFT,
    "real-estate": RealEstate,
    "stock": Stock,
}
