# API & Compliance Requirements

## Overview
Backend services must expose consistent APIs that allow the register and reporting stack to remain loosely coupled while staying compliant with PCI DSS and GDPR. Each domain below specifies required endpoints, payloads, and regulatory considerations.

## Payments API
- **Endpoints**
  - `POST /payments/authorize`: accepts `amount`, `currency`, `tender_type`, `tokenized_pan`, `capture_mode`, `device_id`, `metadata (cashier_id, register_id)`.
  - `POST /payments/capture`: `authorization_id`, `amount`, `tip_amount`, `receipt_ref`.
  - `POST /payments/void` & `POST /payments/refund`: include `reason_code`, `original_transaction_id`.
  - `GET /payments/{id}`: returns status, EMV data, risk scores.
- **Events**
  - Publish `payment.authorized`, `payment.captured`, `payment.failed`, `payment.refund_initiated` with ISO-8601 timestamps.
- **Compliance**
  - Tokenization service must be PCI DSS level 1; registers only handle tokens and truncated PAN.
  - Store PCI scope diagram in runbook and ensure quarterly ASV scans.

## Tax API
- **Endpoints**
  - `POST /tax/quote`: request body includes line items (`sku`, `tax_code`, `price`, `quantity`), `ship_to`, `ship_from`, `customer_exemption_id`.
  - `POST /tax/commit`: commit the quote once sale completed; returns journal IDs.
  - `POST /tax/adjust`: handle returns/exchanges referencing original commit ID.
- **Data Contracts**
  - All responses carry jurisdiction breakdown (state, county, city, special tax), effective rates, and rounding mode.
  - Support destination-based and origin-based taxation plus tax holidays.
- **Compliance**
  - Store exemption certificates for 7 years with retrieval API for auditors.

## Accounting API
- **Endpoints**
  - `POST /journal`: create accounting entries with `transaction_id`, `ledger`, `debit`, `credit`, `currency`, `posting_date`, `department`.
  - `POST /payouts`: represent daily deposits per tender type with bank settlement metadata.
  - `GET /settlements/{date}`: reconciliation view of expected vs. actual deposits.
- **Data Considerations**
  - Journal entries must be immutable; corrections executed via reversing entry reference.
  - Support multi-entity (legal) and multi-currency posting with FX rates snapshot.

## Regulatory Constraints
### PCI DSS
- Isolate cardholder data environment (CDE) to payment microservice + terminals.
- Enforce TLS 1.2+, disable weak ciphers, rotate certificates annually.
- Mask PAN except last 4 digits in logs; purge raw PAN/token data after 18 months unless legal hold.
- Implement role-based access; only payment ops team can view sensitive logs.

### GDPR
- Provide customer consent tracking for digital receipts and loyalty enrollment.
- `DELETE /customers/{id}` must cascade to marketing preferences while retaining anonymized sales data.
- Data minimization: register only caches 30 days of customer data offline.
- Record processing activities (RoPA) describing POS data flows; accessible to Data Protection Officer.

## Non-Functional Requirements
- APIs must support 400 TPS per region with P99 < 300ms for auth/quote endpoints.
- Provide sandbox environments with sample data for integration testing.
- Publish OpenAPI specs and SDKs (TypeScript, Kotlin) to speed client integration.
- All endpoints require OAuth 2.0 client credentials with scoped tokens; audit log tracks token issuance and usage.
