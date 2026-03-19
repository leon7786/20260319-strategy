# AUDIT WARNING

## Status: FAILED / NEEDS REBUILD

The current monthly NASDAQ strategy line in `Openclaw_A6` is under audit failure.

### Confirmed issue
`BOND_ANNUAL` was hard-coded and then converted into monthly out-of-market returns using the current row's year. That is a forward-looking leak, because the full-year bond outcome is not knowable during that year.

### Consequence
All reported performance that depends on this bond-side logic should be treated as **invalid for production / invalid for honest reporting** until rebuilt with non-forward-looking data.

### Minimum remediation
- Remove `BOND_ANNUAL`
- Replace defensive side with replayable real data, or fall back to `cash`
- Recompute performance and drawdown under honest execution assumptions
