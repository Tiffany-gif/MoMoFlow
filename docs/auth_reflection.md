# Authentication & Security Reflection

## What we used (for this assignment)
We protected every endpoint with **HTTP Basic Authentication**. The server expects an `Authorization: Basic <base64(username:password)>` header and returns `401 Unauthorized` if missing or incorrect. For a small internal assignment and a simple `http.server` API, this is acceptable.

## Why Basic Auth is weak
- **Base64 is not encryption**: credentials are easily decoded if intercepted.
- **Replay risk**: the same header can be reused by an attacker if traffic is sniffed.
- **Credentials in logs & caches**: proxies or tools may record the header.
- **No key rotation / session control**: static username/password, no expiry.
- **Phishing-prone**: credentials are long-lived and often reused.
- **Transport dependent**: only safe when used strictly over HTTPS.

## Minimum hardening (even with Basic)
- **Always use HTTPS** (TLS) to protect the header.
- **Store secrets in environment variables** (not hard-coded).
- **Rate limiting and lockouts** on repeated failures.
- **Audit logs** for auth attempts and sensitive actions.
- **Input validation** on all POST/PUT payloads; limit body size.

## Better alternatives
- **JWT (Bearer tokens)**: app issues a token after `/login`; tokens expire, can carry claims (role/permissions). Works great with SPAs and mobile apps.
- **OAuth2 / OpenID Connect**: standardized flows, supports third-party identity providers; best for multi-client ecosystems.
- **API keys per client**: simple, rotateable, and revocable (but still use HTTPS).
- **Mutual TLS** for service-to-service trust in internal networks.

**Recommendation:** For production, replace Basic Auth with a small `/login` that returns a short-lived **JWT**, enforce HTTPS, rotate secrets, and add role-based checks (e.g., only Admin can DELETE).
