from llm_agent.domains.base import Domain
from typing import Type

# from llm_agent.domains.crypto.domain import Crypto
# from llm_agent.domains.hft.domain import HFT
# from llm_agent.domains.real_estate.domain import RealEstate
from llm_agent.domains.stock import Stock


DOMAIN_REGISTRY: dict[str, Type[Domain]] = {
    # "crypto": Crypto,
    # "hft": HFT,
    # "real-estate": RealEstate,
    "stock": Stock,
}
