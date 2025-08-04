# ==============================================
# Trading Fee Calculator
# ==============================================
# Handles all fee-related calculations:
# - Calculates trading fees based on trade value
# - Uses TRADING_FEE_PERCENT from settings
# - Splits fees between buyer and seller
# - Currently uses same fee for both parties
#
# Fee Structure:
# - Base fee: TRADING_FEE_PERCENT of trade value
# - Buyer pays: base fee
# - Seller pays: base fee
# ==============================================

from typing import Dict
from ..config import settings


def calculate_trading_fees(trade_value: float) -> Dict[str, float]:
    """
    Calculate trading fees for a transaction
    Returns: {'buyer_fee': fee, 'seller_fee': fee}
    """
    fee_percent = settings.TRADING_FEE_PERCENT
    fee_amount = trade_value * fee_percent / 100

    # Both buyer and seller pay the same fee in this model
    # Could be modified to have different fee structures
    return {"buyer_fee": fee_amount, "seller_fee": fee_amount}
