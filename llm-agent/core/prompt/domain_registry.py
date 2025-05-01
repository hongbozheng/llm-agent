from ...domains.crypto.domain import Crypto
from ...domains.hft.domain import HFT
from ...domains.real_estate.domain import RealEstate

DOMAIN_REGISTRY = {
    "crypto": Crypto,
    "hft": HFT,
    "real-estate": RealEstate,
}

SUPPORTED_DOMAINS = list(DOMAIN_REGISTRY.keys())
