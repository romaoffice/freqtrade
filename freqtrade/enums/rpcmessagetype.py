from enum import Enum


class RPCMessageType(Enum):
    STATUS = 'status'
    WARNING = 'warning'
    STARTUP = 'startup'
    BUY = 'entry'
    BUY_FILL = 'entry_fill'
    BUY_CANCEL = 'entry_cancel'
    SELL = 'exit'
    SELL_FILL = 'exit_fill'
    SELL_CANCEL = 'exit_cancel'
    PROTECTION_TRIGGER = 'protection_trigger'
    PROTECTION_TRIGGER_GLOBAL = 'protection_trigger_global'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
