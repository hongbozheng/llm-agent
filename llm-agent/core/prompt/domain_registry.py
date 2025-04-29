from ...domains.crypto.domain import Crypto
from ...domains.real_estate.domain import RealEstate

DOMAIN_REGISTRY = {
    "crypto": Crypto,
    "real_estate": RealEstate,
}

SUPPORTED_DOMAINS = list(DOMAIN_REGISTRY.keys())
