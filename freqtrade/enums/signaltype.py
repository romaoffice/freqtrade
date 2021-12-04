from enum import Enum


class SignalType(Enum):
    """
    Enum to distinguish between buy and sell signals
    """
    BUY = "entry"
    SELL = "exit"


class SignalTagType(Enum):
    """
    Enum for signal columns
    """
    BUY_TAG = "buy_tag"
    EXIT_TAG = "exit_tag"
