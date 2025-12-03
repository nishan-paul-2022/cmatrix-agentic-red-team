"""Authentication and session security testing tools."""


def analyze_login_form(url):
    """Analyze login form for security best practices."""
    try:
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        results.append(f"Login Form Analysis for {url}")

        # Find login forms
        forms = soup.find_all("form")
        login_forms = []

        for form in forms:
            inputs = form.find_all("input")
            has_username = any(
                inp.get("name", "").lower() in ["username", "user", "email", "login"]
                for inp in inputs
            )
            has_password = any(inp.get("type", "").lower() == "password" for inp in inputs)

            if has_username and has_password:
                login_forms.append(form)

        if not login_forms:
            return f"No login forms found on {url}"

        results.append(f"Found {len(login_forms)} potential login form(s)")

        for i, form in enumerate(login_forms):
            results.append(f"\nForm {i+1} Analysis:")

            # Check method
            method = form.get("method", "get").upper()
            if method == "POST":
                results.append("✅ Form uses POST method")
            else:
                results.append("❌ Form uses GET method (credentials may be in URL)")

            # Check action
            action = form.get("action", "")
            if action.startswith("https://"):
                results.append("✅ Form action uses HTTPS")
            elif action.startswith("http://"):
                results.append("❌ Form action uses HTTP")
            else:
                results.append("⚠️  Form action is relative (depends on page protocol)")

            # Analyze inputs
            inputs = form.find_all("input")
            username_fields = [
                inp
                for inp in inputs
                if inp.get("name", "").lower() in ["username", "user", "email", "login"]
            ]
            password_fields = [inp for inp in inputs if inp.get("type", "").lower() == "password"]

            results.append(f"Username fields: {len(username_fields)}")
            results.append(f"Password fields: {len(password_fields)}")

            # Check for autocomplete
            for inp in inputs:
                if inp.get("autocomplete") == "off":
                    results.append("⚠️  Autocomplete disabled (may reduce UX)")

            # Check for CSRF tokens
            hidden_inputs = [inp for inp in inputs if inp.get("type") == "hidden"]
            potential_csrf = [inp for inp in hidden_inputs if len(inp.get("value", "")) > 10]
            if potential_csrf:
                results.append("✅ Potential CSRF protection detected")
            else:
                results.append("⚠️  No CSRF protection detected")

        return "\n".join(results)

    except Exception as e:
        return f"Login form analysis failed: {str(e)}"


def check_session_security(url):
    """Check session management security."""
    try:
        import requests

        results = []
        results.append(f"Session Security Check for {url}")

        # Make initial request to get cookies
        response1 = requests.get(url, timeout=10, verify=False)
        cookies1 = response1.cookies

        # Make second request
        response2 = requests.get(url, timeout=10, verify=False, cookies=cookies1)
        cookies2 = response2.cookies

        results.append(f"Initial request cookies: {len(cookies1)}")
        results.append(f"Second request cookies: {len(cookies2)}")

        # Check cookie security flags
        all_cookies = list(cookies1) + list(cookies2)
        session_cookies = [
            c
            for c in all_cookies
            if "session" in c.name.lower() or "auth" in c.name.lower() or "token" in c.name.lower()
        ]

        if session_cookies:
            results.append(f"\nSession-related cookies found: {len(session_cookies)}")
            for cookie in session_cookies:
                flags = []
                if cookie.secure:
                    flags.append("Secure")
                if cookie.has_nonstandard_attr("HttpOnly"):
                    flags.append("HttpOnly")
                if cookie.has_nonstandard_attr("SameSite"):
                    flags.append(f"SameSite={cookie.get_nonstandard_attr('SameSite')}")

                status = "✅" if "Secure" in flags and "HttpOnly" in flags else "⚠️"
                results.append(
                    f"{status} {cookie.name}: {', '.join(flags) if flags else 'No security flags'}"
                )
        else:
            results.append("No obvious session cookies detected")

        # Check for session fixation (basic)
        if len(cookies1) > 0 and len(cookies2) > 0:
            cookie_names1 = {c.name for c in cookies1}
            cookie_names2 = {c.name for c in cookies2}
            if cookie_names1 == cookie_names2:
                results.append("⚠️  Same cookies returned in both requests")
            else:
                results.append("ℹ️  Cookie set may vary between requests")

        return "\n".join(results)

    except Exception as e:
        return f"Session security check failed: {str(e)}"


def test_rate_limiting(url, endpoint="/login"):
    """Test for rate limiting on authentication endpoints."""
    try:
        import time

        import requests

        results = []
        results.append(f"Rate Limiting Test for {url}{endpoint}")

        # Send multiple rapid requests
        responses = []

        for i in range(10):
            try:
                start_time = time.time()
                response = requests.post(
                    url.rstrip("/") + endpoint,
                    data={"username": f"test{i}", "password": "wrong"},
                    timeout=5,
                    verify=False,
                )
                end_time = time.time()

                responses.append(
                    {
                        "attempt": i + 1,
                        "status": response.status_code,
                        "time": end_time - start_time,
                    }
                )

                # Small delay to avoid overwhelming
                time.sleep(0.1)

            except Exception as e:
                responses.append({"attempt": i + 1, "error": str(e), "time": 0})

        # Analyze responses
        status_codes = [r.get("status", 0) for r in responses if "status" in r]
        times = [r["time"] for r in responses]

        results.append(f"Total requests: {len(responses)}")
        results.append(f"Status codes: {status_codes}")

        # Check for rate limiting indicators
        if 429 in status_codes:
            results.append("✅ Rate limiting detected (HTTP 429)")
        elif len(set(status_codes)) > 1:
            results.append("⚠️  Mixed status codes - possible rate limiting")
        else:
            results.append("❌ No rate limiting detected")

        # Check for timing patterns
        avg_time = sum(times) / len(times) if times else 0
        max_time = max(times) if times else 0
        results.append(f"Average response time: {avg_time:.2f}s")
        results.append(f"Max response time: {max_time:.2f}s")

        if max_time > avg_time * 2:
            results.append("⚠️  Significant timing variations detected")

        return "\n".join(results)

    except Exception as e:
        return f"Rate limiting test failed: {str(e)}"


def check_password_policy(url):
    """Check password policy requirements."""
    try:
        import requests
        from bs4 import BeautifulSoup

        results = []
        results.append(f"Password Policy Check for {url}")

        # This is a basic check - in practice, you'd need to test the actual registration/reset endpoints
        response = requests.get(url, timeout=10, verify=False)

        # Look for client-side password requirements in JavaScript or HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Check for password strength indicators
        password_scripts = soup.find_all(["script", "input"], {"type": "password"})

        if password_scripts:
            results.append("✅ Password input fields found")
        else:
            results.append("❌ No password input fields found")

        # Look for password policy text
        policy_indicators = [
            "password",
            "must contain",
            "at least",
            "characters",
            "uppercase",
            "lowercase",
            "number",
            "special",
        ]
        text_content = soup.get_text().lower()

        policy_mentions = [word for word in policy_indicators if word in text_content]
        if policy_mentions:
            results.append(f"ℹ️  Password policy indicators found: {', '.join(policy_mentions)}")
        else:
            results.append("⚠️  No visible password policy requirements")

        # Check for common security features
        security_features = {
            "Password strength meter": "password-strength" in text_content
            or "strength" in text_content,
            "Password visibility toggle": "show password" in text_content
            or "toggle" in text_content,
            "Password generator": "generate" in text_content and "password" in text_content,
        }

        results.append("\nSecurity Features:")
        for feature, detected in security_features.items():
            status = "✅" if detected else "❌"
            results.append(f"{status} {feature}")

        return "\n".join(results)

    except Exception as e:
        return f"Password policy check failed: {str(e)}"
