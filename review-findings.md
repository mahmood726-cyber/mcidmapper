# MCIDMapper Code Review Findings

**Date:** 2026-04-03
**Reviewer:** Code Audit (Claude)
**File:** mcid-mapper.html (1,682 lines)

## P0 (Critical — must fix before ship)

### P0-1: Missing Content-Security-Policy meta tag
**Location:** `<head>` section (line 2-5)
**Issue:** No CSP header present. Other tools in the portfolio (SoFTable, KMDigitizer)
include inline CSP. Without CSP, the app is more vulnerable to XSS if user-controlled
data were to be rendered unsafely. While `escapeHtml()` is used consistently, defense
in depth requires CSP.
**Fix:** Add `<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data: blob:; font-src 'self';">`.

### P0-2: Missing skip-to-content link for accessibility
**Location:** After `<body>` tag (line 377)
**Issue:** No skip navigation link for keyboard/screen-reader users. WCAG 2.1 AA
requires a mechanism to bypass blocks of repeated content (Success Criterion 2.4.1).
**Fix:** Add skip-to-content anchor before the header.

## P1 (Important — fix before submission)

### P1-1: Log of zero/negative not guarded in ratio classification
**Location:** `classify()` and `computeProbBeyondMCID()` (~line 695-767)
**Issue:** Validation at line 1396 guards `eff <= 0 || lo <= 0 || hi <= 0 || mcid <= 0`
for ratio measures, returning early with an alert. However, if called programmatically
via `window.__MCID_MAPPER__.classify()` with bad values, `Math.log(0)` = `-Infinity`
would propagate silently.
**Recommendation:** Add guard at function level, not just at UI validation.

### P1-2: Sensitivity analysis assumes baseMCID > 0 but allows baseMCID = 0
**Location:** `renderSensitivity()` (~line 1131)
**Issue:** `if (baseMCID === 0) baseMCID = 0.1;` -- This silently changes the analysis
base without user notification, which could be confusing.
**Recommendation:** Show a toast or note in the sensitivity table when MCID was zero-corrected.

## P2 (Minor — nice to have)

### P2-1: `csvSafe()` is properly implemented
**Location:** Line 533-540
**Status:** Correctly prepends `'` for `=+@\t\r` (not `-`). No issue.

### P2-2: `escapeHtml()` uses DOM-based approach
**Location:** Line 526-530
**Status:** Uses `document.createElement('div')` + `textContent` which handles all
characters safely. No issue.

### P2-3: Blob URL revocation present in `downloadBlob()`
**Location:** Line 1530-1539
**Status:** Correctly revokes. No issue.

### P2-4: Tab keyboard navigation present but uses `classList` not `aria-selected`
**Location:** Line 1575-1602
**Issue:** The MCIDMapper tabs use both `classList.add('active')` and `aria-selected`
which is good. Arrow key navigation is implemented. No issue.

## Summary

| Severity | Count | Fixed |
|----------|-------|-------|
| P0       | 2     | Yes   |
| P1       | 2     | No    |
| P2       | 0     | --    |
| **Total**| **4** |       |
