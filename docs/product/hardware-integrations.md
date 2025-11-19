# Hardware Integrations

## Device Matrix
| Device             | Protocol / SDK        | Key Events Captured               | Notes |
|--------------------|-----------------------|-----------------------------------|-------|
| Barcode scanner    | USB-HID, OPOS         | Scan success/fail, latency        | Support hands-free + pistol grip modes. |
| Receipt printer    | ESC/POS over USB/LAN  | Print job start/end, paper status | Auto-fallback to email if printer offline > 30s. |
| Cash drawer        | Printer kick or IoT   | Open/close events, dwell time     | Drawer auto-lock after 30 seconds idle. |
| Payment terminal   | Semi-integrated API   | Device ready, EMV outcome, tip    | Supports multi-lane via terminal IDs. |
| Customer display   | WebSocket             | Cart updates, prompts, loyalty    | Mirrors marketing messages during idle. |
| Scale              | RS-232/USB            | Gross/net weight, tare applied    | Self-calibrates daily with manager PIN. |

## Integration Principles
1. **Idempotent messaging:** every device event carries register + device ID so backend can dedupe.
2. **Health heartbeats:** devices publish health every 30 seconds; register blocks tender types if heartbeats lapse.
3. **Driver sandboxing:** hardware drivers run in containerized service to isolate crashes from the POS UI.
4. **Version pinning:** firmware versions recorded per terminal; upgrades scheduled after store close windows.
5. **Security:** payment terminals never share PAN data; register receives tokens only, aligning with PCI scope reduction.

## State Management
- Maintain state machine per device: `ready → active → error → recovering → ready`.
- When a device enters `error`, show inline banner, log telemetry, and route to fallback (e.g., email receipt or manual entry).
- Offline register caches device events locally (SQLite) with retry + exponential backoff once connectivity resumes.

## Deployment & Testing
- Provide simulated device harness for QA with canned events and fault injection (paper jam, disconnect, tamper).
- Store kit checklist includes QR code linking device to register asset record.
- Certification matrix covers: power fail recovery, USB reconnect, firmware upgrade rollback, and locale-specific printers.
