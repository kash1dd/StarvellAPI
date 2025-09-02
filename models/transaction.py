from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from StarvellAPI.common.enums import TransactionDirections, TransactionTypes, TransactionStatuses

class BaseConfig(BaseModel):
    class Config:
        validate_by_name = True

class PayOut(BaseConfig):
    payout_id: str = Field(alias="id")
    status: str
    amount: str
    address: str
    net_amount: int = Field(alias="netAmount")
    process_at: Optional[datetime] = Field(alias="processAt")
    completed_at: Optional[datetime] = Field(alias="completedAt")
    external_tx_id: str = Field(alias="externalTxId")
    external_error: Optional[str] = Field(alias="externalError")
    requestedAmount: int

class PayOutSystemIcon(BaseConfig):
    icon_id: str = Field(alias="id")
    file_extension: str = Field(alias="extension")

class PayOutSystem(BaseConfig):
    system_id: int = Field(alias="id")
    name: str
    icon: PayOutSystemIcon

class TransactionInfo(BaseConfig):
    transaction_id: str = Field(alias="id")
    direction: TransactionDirections
    type: TransactionTypes
    status: TransactionStatuses
    amount: int
    user_id: int = Field(alias="userId")
    order_id: Optional[str] = Field(alias="orderId")
    topup_id: Optional[str] = Field(alias="topupId")
    payout_id: Optional[str] = Field(alias="payoutId")
    funds_release_at: Optional[datetime] = Field(alias="fundsReleaseAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    topup: Optional[dict]
    payout: Optional[PayOut]
    payout_payment_system: Optional[PayOutSystem] = Field(alias="payoutPaymentSystem")
    topup_payment_system: Optional[dict] = Field(alias="topupPaymentSystem")