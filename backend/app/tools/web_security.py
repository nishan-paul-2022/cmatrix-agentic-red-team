"""General web application security testing tools."""


def web_app_security_test(url):
    """Perform basic web application security testing."""
    try:
        import requests

        response = requests.get(url, timeout=10, verify=False)

        results = []
        results.append(f"Web Application Security Test for {url}")
        results.append(f"Status Code: {response.status_code}")
        results.append(f"Server: {response.headers.get('Server', 'Unknown')}")
        results.append(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")

        # Check for security headers
        security_headers = {
            "X-Frame-Options": "Missing X-Frame-Options header (Clickjacking vulnerability)",
            "X-Content-Type-Options": "Missing X-Content-Type-Options header (MIME sniffing vulnerability)",
            "X-XSS-Protection": "Missing X-XSS-Protection header (XSS vulnerability)",
            "Strict-Transport-Security": "Missing Strict-Transport-Security header (No HTTPS enforcement)",
            "Content-Security-Policy": "Missing Content-Security-Policy header (XSS/injection vulnerabilities)",
        }

        results.append("\nSecurity Headers Check:")
        for header, warning in security_headers.items():
            if header not in response.headers:
                results.append(f"❌ {warning}")
            else:
                results.append(f"✅ {header}: {response.headers[header]}")

        # Check for common vulnerabilities
        results.append("\nCommon Vulnerability Checks:")

        # Check for exposed admin panels
        admin_paths = ["/admin", "/admin.php", "/administrator", "/wp-admin", "/login", "/signin"]
        for path in admin_paths:
            try:
                admin_response = requests.get(url.rstrip("/") + path, timeout=5, verify=False)
                if admin_response.status_code == 200:
                    results.append(
                        f"⚠️  Potential admin panel found at {path} (status: {admin_response.status_code})"
                    )
            except:
                pass

        # Check for directory listing
        try:
            dir_response = requests.get(url.rstrip("/") + "/", timeout=5, verify=False)
            if "Index of" in dir_response.text or "Directory listing" in dir_response.text:
                results.append("⚠️  Directory listing enabled (information disclosure)")
        except:
            pass

        # Check for outdated software versions
        server = response.headers.get("Server", "").lower()
        if "apache" in server and "2.4" not in server:
            results.append("⚠️  Potentially outdated Apache version")
        elif "nginx" in server and "1.2" not in server:
            results.append("⚠️  Potentially outdated Nginx version")

        return "\n".join(results)

    except Exception as e:
        return f"Web application security test failed: {str(e)}"


def check_https_hsts(url):
    """Check if HTTPS is enforced and HSTS is enabled."""
    try:
        import requests

        results = []

        # Check HTTPS redirect
        if not url.startswith("http"):
            url = "http://" + url

        # Try HTTP first
        try:
            http_response = requests.get(
                url.replace("https://", "http://"), timeout=10, allow_redirects=False
            )
            if http_response.status_code in [301, 302, 303, 307, 308]:
                location = http_response.headers.get("Location", "")
                if location.startswith("https://"):
                    results.append("✅ HTTP redirects to HTTPS")
                else:
                    results.append("⚠️  HTTP redirects but not to HTTPS")
            else:
                results.append("❌ No HTTPS redirect from HTTP")
        except:
            results.append("⚠️  HTTP request failed or timed out")

        # Check HTTPS
        https_url = url.replace("http://", "https://")
        try:
            https_response = requests.get(https_url, timeout=10, verify=False)
            if https_response.status_code == 200:
                results.append("✅ HTTPS is accessible")

                # Check HSTS
                hsts = https_response.headers.get("Strict-Transport-Security")
                if hsts:
                    results.append(f"✅ HSTS enabled: {hsts}")
                else:
                    results.append("❌ HSTS not enabled")
            else:
                results.append(f"⚠️  HTTPS returns status {https_response.status_code}")
        except:
            results.append("❌ HTTPS not accessible")

        return "\n".join(results)

    except Exception as e:
        return f"HTTPS/HSTS check failed: {str(e)}"
