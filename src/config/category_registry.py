from enum import Enum
from typing import List


class StrategyCategory(str, Enum):
    HIGH_FREQ_TRADING = "high_frequency_trading"
    LONG_TERM_STOCKS = "long_term_stock_investing"
    CRYPTO = "cryptocurrency_trading"
    REAL_ESTATE = "real_estate_investment"
    STARTUP = "startup_idea_generation"
    PASSIVE = "passive_income"
    ECOMMERCE = "dropshipping_and_ecommerce"
    CONTENT = "content_creation_and_monetization"
    FREELANCE = "freelancing_and_consulting"
    SIDE_HUSTLE = "side_hustles"
    NFT_DOMAINS = "domain_flipping_and_nft"
    ANGEL = "angel_investing"
    RETIREMENT = "retirement_planning"
    OPTIONS = "options_trading"
    FOREX = "forex_trading"
    BONDS = "bond_investing"
    COMMODITIES = "commodities_trading"
    QUANT = "quant_strategies"
    REITS = "REITs_and_property_funds"
    AI = "AI_product_monetization"
    DATA = "data_asset_monetization"
    ARBITRAGE = "automated_arbitrage"
    AFFILIATE = "affiliate_marketing"
    BUY_BUSINESS = "buying_websites_or_SaaS"
    ENGINEERING = "financial_engineering"

def get_all_categories() -> List[str]:
    return [c.value for c in StrategyCategory]
