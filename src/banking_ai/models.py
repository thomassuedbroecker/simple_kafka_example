"""Typed models used by producer, consumer, rules, and graph."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BankingTransaction(BaseModel):
    transaction_id: str = Field(min_length=1)
    account_id: str = Field(min_length=1)
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    merchant: str = Field(min_length=1)
    country: str = Field(min_length=2, max_length=2)
    timestamp: datetime
    transaction_type: str = Field(min_length=1)


class RuleFinding(BaseModel):
    rule_id: str
    reason: str
    relevant_fields: list[str]
    suspicious: bool = True


class InspectionResult(BaseModel):
    transaction_id: str
    status: Literal["NORMAL", "SUSPICIOUS"]
    findings: list[RuleFinding]
    ai_explanation: str
    reviewer_check: str


class AgentState(BaseModel):
    """The data that moves through the LangGraph workflow."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    transaction: BankingTransaction
    findings: list[RuleFinding] = Field(default_factory=list)
    suspicious: bool = False
    ai_explanation: str = ""
    final_result: InspectionResult | None = None
