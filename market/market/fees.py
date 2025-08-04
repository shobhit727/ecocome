# market/fees.py
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
