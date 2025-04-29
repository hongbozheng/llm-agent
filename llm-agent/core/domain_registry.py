from ..domains.crypto.domain import CryptoDomain
from ..domains.real_estate.domain import RealEstateDomain

DOMAIN_REGISTRY = {
    "crypto": CryptoDomain,
    "real_estate": RealEstateDomain,
}
