---
name: vendor-status-poll
description: Poll an SMS campaign's carrier vetting status twice daily and alert on change; temporary monitor
---

<!-- Sanitized for publication: host alias, account and service identifiers, phone numbers,
     dates and the credential-loading step replaced with placeholders. The pattern: the
     credential is used on the server, and only the status crosses back to the agent. -->

Check the Twilio A2P 10DLC campaign vetting status and report it.

Run this over SSH on the server that already holds the credentials. The auth token must never reach the agent's transcript; only the printed status comes back:

```
ssh <PROD_HOST> 'bash -s' <<'REMOTE'
# Load SID and TOK from your secret manager here; never echo them.
MG=<MESSAGING_SERVICE_SID>
echo "=== Campaign status ==="
curl -s "https://messaging.twilio.com/v1/Services/$MG/Compliance/Usa2p" -u "$SID:$TOK" \
 | python3 -c "import sys,json; c=json.load(sys.stdin)['compliance'][0]; print('campaign_status:', c.get('campaign_status')); print('errors:', c.get('errors')); print('rate_limits:', c.get('rate_limits'))"
echo; echo "=== Numbers attached ==="
curl -s "https://messaging.twilio.com/v1/Services/$MG/PhoneNumbers?PageSize=50" -u "$SID:$TOK" \
 | python3 -c "import sys,json; d=json.load(sys.stdin); print('count:', len(d.get('phone_numbers',[])))"
REMOTE
```

Background: the campaign was resubmitted after fixing the opt-in flow (recipient-confirmed opt-in and a public SMS consent page). It is waiting to move from IN_PROGRESS to VERIFIED so a sender number can be attached and the backend switched to SMS.

Report concisely:
- IN_PROGRESS: "still in vetting, no change, no action needed."
- VERIFIED: flag it clearly. Next steps: (1) attach the sender number to the messaging service, (2) run the backend SMS cutover, (3) run a live end-to-end test. Recommend the user ask their assistant to proceed.
- FAILED: flag it, print the errors array verbatim (the rejection reason), and note the message_flow or call-to-action likely needs another revision before resubmitting.
- Always include the attached-numbers count.

This is a temporary monitor. Once the campaign reaches VERIFIED or is abandoned, delete it.
