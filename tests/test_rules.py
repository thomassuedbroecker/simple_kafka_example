from banking_ai.models import BankingTransaction
from banking_ai.rules import inspect_transaction_rules


def make_transaction(**overrides) -> BankingTransaction:
    data = {
        "transaction_id": "txn-test",
        "account_id": "acc-test",
        "amount": 100.0,
        "currency": "EUR",
        "merchant": "Local Shop",
        "country": "DE",
        "timestamp": "2026-06-10T10:15:00Z",
        "transaction_type": "card_payment",
    }
    data.update(overrides)
    return BankingTransaction.model_validate(data)


def rule_ids(transaction: BankingTransaction) -> list[str]:
    return [finding.rule_id for finding in inspect_transaction_rules(transaction)]


def test_normal_transaction_has_no_findings() -> None:
    assert inspect_transaction_rules(make_transaction()) == []


def test_large_amount_is_suspicious() -> None:
    assert "amount_greater_than_1000" in rule_ids(make_transaction(amount=1000.01))


def test_foreign_country_is_suspicious() -> None:
    assert "foreign_country" in rule_ids(make_transaction(country="US"))


def test_large_cash_withdrawal_is_suspicious() -> None:
    assert "large_cash_withdrawal" in rule_ids(
        make_transaction(transaction_type="cash_withdrawal", amount=600)
    )


def test_suspicious_merchant_keyword_is_suspicious() -> None:
    assert "suspicious_merchant_keyword" in rule_ids(
        make_transaction(merchant="Unknown Crypto Casino")
    )


def test_findings_carry_a_severity() -> None:
    findings = inspect_transaction_rules(
        make_transaction(merchant="Crypto Casino", amount=2000, country="US")
    )

    severities = {finding.rule_id: finding.severity for finding in findings}
    assert severities["suspicious_merchant_keyword"] == "high"
    assert severities["amount_greater_than_1000"] == "medium"
    assert severities["foreign_country"] == "low"
    assert all(finding.severity in {"low", "medium", "high"} for finding in findings)
