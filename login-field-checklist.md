  ------------------------------------------------------------------------
  Question                   How to check
  -------------------------- ---------------------------------------------
  Is the login page served   Open page in browser and confirm URL starts
  over HTTPS only (no HTTP)? with https://. Try http:// and observe
                             redirect behavior. Check Network tab for
                             mixed-content warnings.

  Is HSTS enabled for the    Inspect response headers in DevTools →
  domain?                    Network for Strict-Transport-Security or use
                             an HSTS checker.

  Are credentials ever sent  Observe requests in DevTools/Proxy and check
  in URL/query strings?      request line and query string for credential
                             parameters.

  Is the login request sent  Inspect the HTTP method of the login request
  as POST (not GET)?         in DevTools/Network or proxy.

  Is the Content-Type        Check the request header Content-Type and the
  appropriate (form/json)    request body format in the proxy.
  and consistent?            

  Is there server-side input Submit unusual inputs (long strings, special
  validation for             chars) and observe server responses for
  username/password?         validation or errors.

  Are client-side            Disable JavaScript or modify the form in
  validations present only   DevTools then submit to verify server
  as UX (not relied on)?     enforces constraints.

  Does the app accept        Send very long username/password values and
  extremely long or binary   watch for 500 errors, stack traces, or other
  inputs without error?      failures.

  Are error messages generic Trigger failed logins and inspect response
  (no internal info or stack bodies and UI for debug info, file paths, or
  traces)?                   stack traces.

  Do responses differ        Try existing-user + wrong-password vs
  between valid vs invalid   non-existent-user and compare response
  usernames                  bodies, status codes, and timing.
  (timing/message)?          

  Can you enumerate accounts Use differences observed above (messages or
  from error messages or     timing) to determine if enumeration is
  behavior?                  possible.

  Is there rate-limiting or  Perform multiple failed login attempts and
  progressive delay on       watch for increased latency, HTTP 429, or
  failed attempts?           lockout responses.

  Are CAPTCHAs or lockouts   Repeat failed attempts and observe when
  applied after repeated     CAPTCHA appears or when IP/account is
  failures?                  blocked.

  Are cookies set with       After login, inspect cookies in DevTools →
  Secure, HttpOnly, and      Application → Cookies and check flags.
  appropriate SameSite?      

  Does the session token     Capture session token before and after login
  rotate after login and     or privilege change and verify the token
  after privilege changes?   value changes.

  Is session invalidated on  Log out and attempt reuse of old
  logout and after password  cookie/token; after password reset, confirm
  reset?                     old tokens no longer work.

  Is MFA/2FA enforced or     Check account settings for MFA enrollment and
  available for users with   perform a login that should trigger 2FA to
  elevated access?           observe the extra step.

  Can MFA be bypassed by     Inspect MFA request/response flow in proxy
  parameter tampering or     for client-side parameters that could be
  code reuse?                modified (do not brute-force codes).

  Are password complexity    Attempt to set weak passwords via
  rules enforced             change/reset endpoints with JS disabled and
  server-side?               see if server rejects them.

  Does password reset use    Request password reset and inspect token
  single-use, short-lived    characteristics (length, reuse behavior,
  tokens?                    expiry info).

  Does password reset reveal Submit password reset for existing vs
  account existence?         non-existing emails and compare responses and
                             timing.

  Are security               Review recovery flow for weak fallback
  questions/recovery options mechanisms or exposure of answers/hints.
  implemented securely?      

  Are SSO/OAuth redirect     Inspect auth request/redirect parameters and
  URIs strictly whitelisted  test redirect_uri handling in a controlled
  and validated?             environment.

  Are tokens from IdP        Capture IdP tokens and inspect claims (aud,
  validated for audience,    exp, scope) or review token-validation on app
  scope, and expiry?         side.

  Are there open-redirects   Controlled test: alter redirect parameters
  in the auth or callback    and observe if app redirects to arbitrary
  parameters?                domains.

  Are login-related          Check for anti-CSRF tokens in forms or
  endpoints protected        confirm SameSite cookie settings; attempt
  against CSRF where         state-changing requests without token.
  applicable?                

  Is X-Frame-Options / CSP   Inspect response headers for X-Frame-Options
  frame-ancestors set to     or CSP frame-ancestors directives.
  prevent clickjacking?      

  Are error messages and     Review response bodies/headers for secrets,
  client responses free of   internal IPs, DB IDs, or debug info.
  sensitive data?            

  Does the app implement     Attempt password change/reset with
  breached-password checks   known-breached or reused passwords and
  or block reused passwords? observe server response.

  Are API/mobile auth        Identify API endpoints via Network tab and
  endpoints subject to the   test them separately for validation,
  same checks as web form?   rate-limiting, and error handling.

  Are logs recording         If you have access, inspect logs for
  failed/successful logins   timestamp, IP, user-agent; otherwise request
  with IP and user-agent?    log policy from devs/ops.

  Do logs avoid storing      Search server logs (if accessible) for
  plaintext passwords or     password strings; otherwise request logging
  sensitive tokens?          policies and evidence.

  Are alerts triggered for   Simulate suspicious patterns safely and
  suspicious login patterns  verify detection/alerts in monitoring or ask
  (mass failures)?           ops for examples.

  Is CSP, XSS protections,   Inspect response headers for
  and secure headers applied Content-Security-Policy and other security
  on the login page?         headers.

  Is any secret (key/token)  View served JS files in DevTools → Sources
  embedded in client-side    and search for hard-coded keys or tokens.
  JavaScript?                

  Is input reflected         Submit data with special characters and
  anywhere (error messages,  inspect pages/HTML responses for reflected
  profile) without encoding? content lacking encoding.

  Are account lockouts       Trigger lockout in test account and attempt
  recoverable only through   recovery; document required verification
  secure channels?           steps and weaknesses.

  Is there protection        Review rate-limiting behavior and check for
  against credential         device fingerprinting or anomaly detection
  stuffing (rate-limits,     that blocks stuffing.
  device fingerprint)?       

  Are OAuth scopes limited   Inspect issued tokens for expiry and scope
  and tokens short-lived?    claims or review OAuth client configuration.

  Is there a documented      Request internal procedure documentation and
  admin/privileged-account   confirm recovery requires strong controls and
  recovery process with      audit trail.
  audit?                     
  ------------------------------------------------------------------------
