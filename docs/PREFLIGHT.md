# PREFLIGHT.md — Go/No-Go Verification

> **Purpose:** Two critical verifications the human owner must confirm before production deployment.
> **Status:** Update the status fields below as each item is verified.

---

## 1. Azure Commercial Availability for Syria

**Question:** Can Azure services be commercially used to serve users in Syria without violating sanctions or terms of service?

**Owner:** _______________________

**Status:** ⬜ NOT VERIFIED

### Verification Steps

1. Review Microsoft's sanctions compliance documentation for Syria
2. Confirm Azure services can be deployed to regions that serve Syrian users
3. Verify no restrictions on providing SaaS applications to end users in Syria
4. Consult legal counsel if needed

### Notes

- Syria is under various international sanctions (US, EU, UN)
- Some Azure services may have restrictions in certain regions
- Email and communication services need particular attention
- Payment processing (if ever added) would be severely restricted

---

## 2. Email/WhatsApp Verification Deliverability

**Question:** Can email and WhatsApp verification messages be reliably delivered to Syrian users?

**Owner:** _______________________

**Status:** ⬜ NOT VERIFIED

### Verification Steps

1. **Email Deliverability:**
   - Test email delivery from Azure Communication Services (or SendGrid) to Syrian email providers
   - Verify SPF/DKIM/DMARC configuration
   - Check if any Syrian ISPs block foreign email services
   - Test with major Syrian email providers (gmail.com, outlook.com, local providers)

2. **WhatsApp Deliverability:**
   - Confirm WhatsApp Business API access is available for Syrian phone numbers (+963)
   - Test verification message delivery
   - Note: SMS is intentionally NOT used (unreliable in Syria)

3. **Alternative Verification:**
   - Consider backup verification methods if primary methods fail
   - Document fallback procedures

### Notes

- SMS is intentionally excluded from this project (unreliable infrastructure in Syria)
- WhatsApp may be more reliable than email for some users
- Consider user experience if verification delays occur
- Test with real Syrian phone numbers if possible

---

## Sign-off

Once both items are verified, update the status fields above to ✅ VERIFIED and add:

**Verified by:** _______________________

**Date:** _______________________

**Notes:** _______________________

---

*This document is required before production deployment per BUILD_PROMPT.md Phase 9.4.*
