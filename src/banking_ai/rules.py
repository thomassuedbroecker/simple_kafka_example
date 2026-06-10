"""Deterministic transaction inspection rules.

These rules are intentionally simple. They teach why a predictable first pass
is useful before asking an LLM to explain the result in plain language.
"""

from banking_ai.models import BankingTransaction, RuleFinding

TRUSTED_COUNTRIES = {"DE", "NL", "FR", "AT"}
SUSPICIOUS_MERCHANT_WORDS = ("crypto", "casino", "unknown")


def inspect_transaction_rules(transaction: BankingTransaction) -> list[RuleFinding]:
    findings: list[RuleFinding] = []

    if transaction.amount > 1000:
        findings.append(
            RuleFinding(
                rule_id="amount_greater_than_1000",
                reason="The transaction amount is greater than 1000.",
                relevant_fields=["amount"],
            )
        )

    if transaction.country not in TRUSTED_COUNTRIES:
        findings.append(
            RuleFinding(
                rule_id="foreign_country",
                reason="The transaction country is outside the simple trusted country list.",
                relevant_fields=["country"],
            )
        )

    if (
        transaction.transaction_type == "cash_withdrawal"
        and transaction.amount > 500
    ):
        findings.append(
            RuleFinding(
                rule_id="large_cash_withdrawal",
                reason="Cash withdrawals above 500 should be reviewed.",
                relevant_fields=["transaction_type", "amount"],
            )
        )

    merchant_lower = transaction.merchant.lower()
    matched_words = [
        word for word in SUSPICIOUS_MERCHANT_WORDS if word in merchant_lower
    ]
    if matched_words:
        findings.append(
            RuleFinding(
                rule_id="suspicious_merchant_keyword",
                reason=(
                    "The merchant name contains a simple suspicious keyword: "
                    + ", ".join(matched_words)
                ),
                relevant_fields=["merchant"],
            )
        )

    return findings
