# SECURITY.md — Security Controls & Checklist

## OWASP Compliance

This application follows **OWASP Mobile Top 10** and **OWASP API Security Top 10** guidelines.

---

## 1. Authentication & Authorization

### Authentication
- [x] Email OR WhatsApp verification (phone mandatory)
- [x] JWT tokens with expiration
- [x] Brute-force protection on login
- [x] Non-enumerable error messages
- [x] No SMS OTP (unreliable in Syria)

### Authorization
- [x] Object-level authorization on every endpoint
- [x] Multi-tenant isolation (seller cannot access other sellers' data)
- [x] Role-based access control (consumer/seller/admin)
- [x] BOLA prevention testing

---

## 2. Data Protection

### At Rest
- [x] Database encryption (Azure PostgreSQL TDE)
- [x] Blob storage encryption (Azure-managed keys)
- [x] PII encryption in database
- [x] Secrets in Azure Key Vault only

### In Transit
- [x] TLS everywhere
- [x] Certificate pinning in mobile app
- [x] No secrets in client bundles

---

## 3. Input Validation & Sanitization

### API
- [x] Pydantic validation on all inputs
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] XSS sanitization on all free text
- [x] Rate limiting on all endpoints

### File Uploads
- [x] Content-type validation by magic bytes
- [x] File size limits
- [x] EXIF/GPS metadata stripping
- [x] Malware scanning (hook)
- [x] Image resize/normalization

---

## 4. Mobile Security

- [x] Certificate pinning
- [x] Root/jailbreak detection
- [x] Code obfuscation in release builds
- [x] No API keys in mobile binary
- [x] Secure storage for tokens

---

## 5. API Security

### Rate Limiting
- [x] Global rate limiting
- [x] Per-endpoint rate limiting
- [x] Brute-force protection on auth endpoints

### Error Handling
- [x] Structured error responses
- [x] No stack traces in responses
- [x] No enumeration of existing users

---

## 6. Infrastructure Security

- [x] Azure Key Vault for secrets
- [x] Managed Identity for service access
- [x] Network isolation (VNet)
- [x] WAF rules (Front Door)
- [x] DDoS protection

---

## 7. Monitoring & Logging

- [x] Application Insights integration
- [x] Audit logging for admin actions
- [x] No secrets in logs
- [x] No full PII in logs

---

## 8. Food Safety Enforcement

- [x] `use_by` items past date rejected at listing creation
- [x] `best_before` items past date may be listed
- [x] Auto-delist on expiry date
- [x] Auto-delist when quantity reaches 0

---

## 9. Anti-Fraud

- [x] Device fingerprint collection
- [x] Price history retention
- [x] Manual admin review for fraud
- [x] No automated bans

---

## 10. Compliance

### Privacy
- [x] Privacy policy documenting:
  - Device IP storage
  - Device ID storage
  - Phone number storage
  - Photo storage
  - Location data
  - EXIF handling

### Legal
- [x] Terms of Service
- [x] Liability disclaimer
- [x] Food safety rules in ToS

---

## Security Checklist for Each Task

Before completing any task, verify:

1. [ ] No secrets in code
2. [ ] No API keys in client bundles
3. [ ] Object-level authorization enforced
4. [ ] Input validation complete
5. [ ] Rate limiting configured
6. [ ] Error messages don't leak info
7. [ ] File uploads validated
8. [ ] EXIF stripped from images
9. [ ] Logs don't contain PII/secrets
10. [ ] Tests pass

---

*See BUILD_PROMPT.md Section 12 for complete security requirements.*
