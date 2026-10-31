# Example interactions

These are illustrative outputs, not recorded benchmark results.

## Guardian: useful reuse

Request: “Review the resend endpoint. It must respect notification preferences.”

Response: “Confirmed: `resend` calls the email transport directly, so users who disabled email still receive it. The existing `dispatch` function checks that preference. Could we use it here and add an opt-out test?”

## Detective: missing evidence

Request: “Notifications timed out. Was the database down?”

Response: “The request log confirms a timeout, but it does not show which dependency stalled. The database and enrichment call are both possible causes. Could you share the failed request's trace or timings for those two calls?”

## Guardian: no meaningful issue

Response: “No meaningful issues found in the inspected path. The implementation reuses the preference-aware dispatcher, and the focused opt-out test passed. I could not check the external delivery provider.”

Use a statement about passed tests only when that test actually ran. Keep limitations specific to the task.
