import os
import re
import json
import requests
import difflib
from typing import TypedDict, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END

# Define tools for the agent
def port_scan(target, ports="1-1024"):
    """Perform a port scan on a target using nmap."""
    try:
        import subprocess
        import re

        # Use subprocess to run nmap directly
        cmd = ['nmap', '-p', ports, '-T4', '--open', target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            return f"Port scan failed: nmap returned error code {result.returncode}. Make sure nmap is installed."

        output = result.stdout

        # Parse the output to extract open ports
        lines = output.split('\n')
        open_ports = []

        for line in lines:
            # Look for lines like "22/tcp open  ssh"
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else 'unknown'
                    open_ports.append(f"Port {port}: open ({service})")

        if open_ports:
            return f"Port scan results for {target}:\n" + "\n".join(open_ports)
        else:
            return f"No open ports found on {target} in range {ports}"

    except subprocess.TimeoutExpired:
        return f"Port scan timed out for {target}"
    except FileNotFoundError:
        return "Port scan failed: nmap not found. Please install nmap."
    except Exception as e:
        return f"Port scan failed: {str(e)}"

def vulnerability_assessment(target):
    """Perform basic vulnerability assessment on a target system."""
    try:
        import subprocess

        # First, do a basic port scan to identify services
        port_cmd = ['nmap', '-p-', '--open', '-T4', target]
        port_result = subprocess.run(port_cmd, capture_output=True, text=True, timeout=120)

        results = [f"Basic Vulnerability Assessment for {target}:"]
        open_ports = []

        if port_result.returncode == 0:
            # Parse open ports
            for line in port_result.stdout.split('\n'):
                if '/tcp' in line and 'open' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        port = parts[0].split('/')[0]
                        service = parts[2] if len(parts) > 2 else 'unknown'
                        open_ports.append((port, service))

                        # Basic vulnerability checks based on service
                        port_num = int(port)
                        if port_num == 21 and 'ftp' in service.lower():
                            results.append("⚠️  WARNING: FTP service detected on port 21 - consider using SFTP (secure)")
                        elif port_num == 23 and 'telnet' in service.lower():
                            results.append("🚨 CRITICAL: Telnet service detected on port 23 - insecure, use SSH")
                        elif port_num == 80 and 'http' in service.lower():
                            results.append("ℹ️  INFO: HTTP detected on port 80 - check for HTTPS support")
                        elif port_num == 445 and 'smb' in service.lower():
                            results.append("⚠️  WARNING: SMB service detected - check for known vulnerabilities")
                        elif port_num == 3389 and 'rdp' in service.lower():
                            results.append("⚠️  WARNING: RDP service detected - ensure NLA is enabled")

        # Check for common misconfigurations
        if open_ports:
            results.append(f"\nOpen ports found: {len(open_ports)}")
            for port, service in open_ports:
                results.append(f"  - Port {port}: {service}")
        else:
            results.append("No open ports detected")

        # Additional checks
        results.append("\nGeneral Recommendations:")
        results.append("• Ensure all services are up-to-date")
        results.append("• Use strong authentication mechanisms")
        results.append("• Implement proper firewall rules")
        results.append("• Regularly scan for vulnerabilities")

        return "\n".join(results)

    except subprocess.TimeoutExpired:
        return f"Vulnerability assessment timed out for {target}"
    except FileNotFoundError:
        return "Vulnerability assessment failed: nmap not found. Please install nmap."
    except Exception as e:
        return f"Vulnerability assessment failed: {str(e)}"

def web_app_security_test(url):
    """Perform basic web application security testing."""
    try:
        response = requests.get(url, timeout=10, verify=False)

        results = []
        results.append(f"Web Application Security Test for {url}")
        results.append(f"Status Code: {response.status_code}")
        results.append(f"Server: {response.headers.get('Server', 'Unknown')}")
        results.append(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")

        # Check for security headers
        security_headers = {
            'X-Frame-Options': 'Missing X-Frame-Options header (Clickjacking vulnerability)',
            'X-Content-Type-Options': 'Missing X-Content-Type-Options header (MIME sniffing vulnerability)',
            'X-XSS-Protection': 'Missing X-XSS-Protection header (XSS vulnerability)',
            'Strict-Transport-Security': 'Missing Strict-Transport-Security header (No HTTPS enforcement)',
            'Content-Security-Policy': 'Missing Content-Security-Policy header (XSS/injection vulnerabilities)'
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
        admin_paths = ['/admin', '/admin.php', '/administrator', '/wp-admin', '/login', '/signin']
        for path in admin_paths:
            try:
                admin_response = requests.get(url.rstrip('/') + path, timeout=5, verify=False)
                if admin_response.status_code == 200:
                    results.append(f"⚠️  Potential admin panel found at {path} (status: {admin_response.status_code})")
            except:
                pass

        # Check for directory listing
        try:
            dir_response = requests.get(url.rstrip('/') + '/', timeout=5, verify=False)
            if 'Index of' in dir_response.text or 'Directory listing' in dir_response.text:
                results.append("⚠️  Directory listing enabled (information disclosure)")
        except:
            pass

        # Check for outdated software versions
        server = response.headers.get('Server', '').lower()
        if 'apache' in server and '2.4' not in server:
            results.append("⚠️  Potentially outdated Apache version")
        elif 'nginx' in server and '1.2' not in server:
            results.append("⚠️  Potentially outdated Nginx version")

        return "\n".join(results)

    except Exception as e:
        return f"Web application security test failed: {str(e)}"

def check_https_hsts(url):
    """Check if HTTPS is enforced and HSTS is enabled."""
    try:
        results = []

        # Check HTTPS redirect
        if not url.startswith('http'):
            url = 'http://' + url

        # Try HTTP first
        try:
            http_response = requests.get(url.replace('https://', 'http://'), timeout=10, allow_redirects=False)
            if http_response.status_code in [301, 302, 303, 307, 308]:
                location = http_response.headers.get('Location', '')
                if location.startswith('https://'):
                    results.append("✅ HTTP redirects to HTTPS")
                else:
                    results.append("⚠️  HTTP redirects but not to HTTPS")
            else:
                results.append("❌ No HTTPS redirect from HTTP")
        except:
            results.append("⚠️  HTTP request failed or timed out")

        # Check HTTPS
        https_url = url.replace('http://', 'https://')
        try:
            https_response = requests.get(https_url, timeout=10, verify=False)
            if https_response.status_code == 200:
                results.append("✅ HTTPS is accessible")

                # Check HSTS
                hsts = https_response.headers.get('Strict-Transport-Security')
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

def analyze_login_form(url):
    """Analyze login form for security best practices."""
    try:
        response = requests.get(url, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        results.append(f"Login Form Analysis for {url}")

        # Find login forms
        forms = soup.find_all('form')
        login_forms = []

        for form in forms:
            inputs = form.find_all('input')
            has_username = any(inp.get('name', '').lower() in ['username', 'user', 'email', 'login'] for inp in inputs)
            has_password = any(inp.get('type', '').lower() == 'password' for inp in inputs)

            if has_username and has_password:
                login_forms.append(form)

        if not login_forms:
            return f"No login forms found on {url}"

        results.append(f"Found {len(login_forms)} potential login form(s)")

        for i, form in enumerate(login_forms):
            results.append(f"\nForm {i+1} Analysis:")

            # Check method
            method = form.get('method', 'get').upper()
            if method == 'POST':
                results.append("✅ Form uses POST method")
            else:
                results.append("❌ Form uses GET method (credentials may be in URL)")

            # Check action
            action = form.get('action', '')
            if action.startswith('https://'):
                results.append("✅ Form action uses HTTPS")
            elif action.startswith('http://'):
                results.append("❌ Form action uses HTTP")
            else:
                results.append("⚠️  Form action is relative (depends on page protocol)")

            # Analyze inputs
            inputs = form.find_all('input')
            username_fields = [inp for inp in inputs if inp.get('name', '').lower() in ['username', 'user', 'email', 'login']]
            password_fields = [inp for inp in inputs if inp.get('type', '').lower() == 'password']

            results.append(f"Username fields: {len(username_fields)}")
            results.append(f"Password fields: {len(password_fields)}")

            # Check for autocomplete
            for inp in inputs:
                if inp.get('autocomplete') == 'off':
                    results.append("⚠️  Autocomplete disabled (may reduce UX)")

            # Check for CSRF tokens
            hidden_inputs = [inp for inp in inputs if inp.get('type') == 'hidden']
            potential_csrf = [inp for inp in hidden_inputs if len(inp.get('value', '')) > 10]
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
        session_cookies = [c for c in all_cookies if 'session' in c.name.lower() or 'auth' in c.name.lower() or 'token' in c.name.lower()]

        if session_cookies:
            results.append(f"\nSession-related cookies found: {len(session_cookies)}")
            for cookie in session_cookies:
                flags = []
                if cookie.secure:
                    flags.append("Secure")
                if cookie.has_nonstandard_attr('HttpOnly'):
                    flags.append("HttpOnly")
                if cookie.has_nonstandard_attr('SameSite'):
                    flags.append(f"SameSite={cookie.get_nonstandard_attr('SameSite')}")

                status = "✅" if 'Secure' in flags and 'HttpOnly' in flags else "⚠️"
                results.append(f"{status} {cookie.name}: {', '.join(flags) if flags else 'No security flags'}")
        else:
            results.append("No obvious session cookies detected")

        # Check for session fixation (basic)
        if len(cookies1) > 0 and len(cookies2) > 0:
            cookie_names1 = set(c.name for c in cookies1)
            cookie_names2 = set(c.name for c in cookies2)
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
        results = []
        results.append(f"Rate Limiting Test for {url}{endpoint}")

        # Send multiple rapid requests
        import time
        responses = []

        for i in range(10):
            try:
                start_time = time.time()
                response = requests.post(url.rstrip('/') + endpoint,
                                       data={'username': f'test{i}', 'password': 'wrong'},
                                       timeout=5, verify=False)
                end_time = time.time()

                responses.append({
                    'attempt': i+1,
                    'status': response.status_code,
                    'time': end_time - start_time
                })

                # Small delay to avoid overwhelming
                time.sleep(0.1)

            except Exception as e:
                responses.append({
                    'attempt': i+1,
                    'error': str(e),
                    'time': 0
                })

        # Analyze responses
        status_codes = [r.get('status', 0) for r in responses if 'status' in r]
        times = [r['time'] for r in responses]

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
        results.append(".2f")
        results.append(".2f")

        if max_time > avg_time * 2:
            results.append("⚠️  Significant timing variations detected")

        return "\n".join(results)

    except Exception as e:
        return f"Rate limiting test failed: {str(e)}"

def check_password_policy(url):
    """Check password policy requirements."""
    try:
        results = []
        results.append(f"Password Policy Check for {url}")

        # This is a basic check - in practice, you'd need to test the actual registration/reset endpoints
        response = requests.get(url, timeout=10, verify=False)

        # Look for client-side password requirements in JavaScript or HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for password strength indicators
        password_scripts = soup.find_all(['script', 'input'], {'type': 'password'})

        if password_scripts:
            results.append("✅ Password input fields found")
        else:
            results.append("❌ No password input fields found")

        # Look for password policy text
        policy_indicators = ['password', 'must contain', 'at least', 'characters', 'uppercase', 'lowercase', 'number', 'special']
        text_content = soup.get_text().lower()

        policy_mentions = [word for word in policy_indicators if word in text_content]
        if policy_mentions:
            results.append(f"ℹ️  Password policy indicators found: {', '.join(policy_mentions)}")
        else:
            results.append("⚠️  No visible password policy requirements")

        # Check for common security features
        security_features = {
            'Password strength meter': 'password-strength' in text_content or 'strength' in text_content,
            'Password visibility toggle': 'show password' in text_content or 'toggle' in text_content,
            'Password generator': 'generate' in text_content and 'password' in text_content
        }

        results.append("\nSecurity Features:")
        for feature, detected in security_features.items():
            status = "✅" if detected else "❌"
            results.append(f"{status} {feature}")

        return "\n".join(results)

    except Exception as e:
        return f"Password policy check failed: {str(e)}"

TOOLS = {
    "security_scan": {
        "description": "Perform a security scan on a target system or application",
        "parameters": ["target"],
        "function": lambda target: f"Security scan completed for {target}. Found 3 medium-risk vulnerabilities: outdated dependencies, missing CORS headers, weak password policy."
    },
    "check_system_status": {
        "description": "Check the status of a system service or application",
        "parameters": ["service_name"],
        "function": lambda service_name: f"Service '{service_name}' is running. CPU: 45%, Memory: 2.3GB, Uptime: 7 days."
    },
    "analyze_logs": {
        "description": "Analyze logs from a specified source for errors or anomalies",
        "parameters": ["log_source"],
        "function": lambda log_source: f"Analyzed logs from {log_source}. Found 12 errors in the last hour, mostly connection timeouts to external API."
    },
    "deploy_config": {
        "description": "Deploy a configuration to a specified environment",
        "parameters": ["environment", "config_name"],
        "function": lambda environment, config_name: f"Configuration '{config_name}' successfully deployed to {environment} environment. Rollback available if needed."
    },
    "port_scan": {
        "description": "Perform a port scan on a target IP or hostname to discover open ports and services",
        "parameters": ["target", "ports"],
        "function": lambda target, ports="1-1024": port_scan(target, ports)
    },
    "vulnerability_assessment": {
        "description": "Perform vulnerability assessment on a target system using nmap scripts",
        "parameters": ["target"],
        "function": vulnerability_assessment
    },
    "web_app_security_test": {
        "description": "Perform basic web application security testing including header checks and common vulnerabilities",
        "parameters": ["url"],
        "function": web_app_security_test
    },
    "check_https_hsts": {
        "description": "Check if HTTPS is enforced and HSTS (HTTP Strict Transport Security) is enabled",
        "parameters": ["url"],
        "function": check_https_hsts
    },
    "analyze_login_form": {
        "description": "Analyze login forms for security best practices including method, HTTPS usage, and CSRF protection",
        "parameters": ["url"],
        "function": analyze_login_form
    },
    "check_session_security": {
        "description": "Check session management security including cookie flags and session handling",
        "parameters": ["url"],
        "function": check_session_security
    },
    "test_rate_limiting": {
        "description": "Test for rate limiting on authentication endpoints to prevent brute force attacks",
        "parameters": ["url", "endpoint"],
        "function": lambda url, endpoint="/login": test_rate_limiting(url, endpoint)
    },
    "check_password_policy": {
        "description": "Check password policy requirements and security features",
        "parameters": ["url"],
        "function": check_password_policy
    }
}

# Agent state
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    tool_calls: list

def create_tool_prompt():
    """Create a prompt describing available tools."""
    tool_descriptions = []
    for name, info in TOOLS.items():
        params = ", ".join(info["parameters"])
        tool_descriptions.append(f"- {name}({params}): {info['description']}")
    
    return f"""You have access to the following tools:

{chr(10).join(tool_descriptions)}

To use a tool, respond with: TOOL_CALL: tool_name(param1, param2, ...)
You can call multiple tools by using multiple TOOL_CALL lines.
After tool results, provide your final answer to the user."""

def parse_tool_calls(text: str) -> list:
    """Parse tool calls from LLM response."""
    tool_calls = []
    pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    for tool_name, params_str in matches:
        if tool_name in TOOLS:
            # Parse parameters
            params = [p.strip().strip('"\'') for p in params_str.split(',') if p.strip()]
            tool_calls.append({"name": tool_name, "params": params})
    
    return tool_calls

def execute_tools(tool_calls: list) -> str:
    """Execute tool calls and return results."""
    results = []
    for call in tool_calls:
        tool_name = call["name"]
        params = call["params"]
        
        if tool_name in TOOLS:
            try:
                result = TOOLS[tool_name]["function"](*params)
                results.append(f"[{tool_name}] {result}")
            except Exception as e:
                results.append(f"[{tool_name}] Error: {str(e)}")
    
    return "\n".join(results) if results else "No tools executed."

class HuggingFaceLLM:
    """Custom LLM wrapper for HuggingFace Router API with chat completions."""
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        model_name = model or os.getenv("HUGGINGFACE_MODEL", "DeepHat/DeepHat-V1-7B")
        
        # Add provider suffix for DeepHat model if not present
        if "DeepHat" in model_name and ":featherless-ai" not in model_name:
            self.model = f"{model_name}:featherless-ai"
        else:
            self.model = model_name
        
        # Use chat completions endpoint for all models
        self.endpoint = "https://router.huggingface.co/v1/chat/completions"
        
        print(f"🤖 Using model: {self.model}")
        print(f"📡 Endpoint: {self.endpoint}")
    
    def invoke(self, prompt: str, max_retries: int = 3) -> str:
        """Call the HuggingFace API using chat completions format with retry logic."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Use chat completions format for all models
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are DeepHat, created by Kindo.ai. You are a helpful assistant that is an expert in Cybersecurity and DevOps."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.7,
            "stream": False
        }
        
        import time
        
        for attempt in range(max_retries):
            try:
                response = requests.post(self.endpoint, json=payload, headers=headers, timeout=60)
                response.raise_for_status()
                
                result = response.json()
                
                # OpenAI-compatible format
                return result["choices"][0]["message"]["content"]
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 503:
                    # Model is loading, wait and retry
                    wait_time = (attempt + 1) * 5  # 5, 10, 15 seconds
                    print(f"⏳ Model loading... Retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    
                    if attempt < max_retries - 1:
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Model still unavailable after {max_retries} attempts")
                        raise Exception("Model is loading. Please try again in a moment.")
                else:
                    print(f"❌ HTTP Error {e.response.status_code}: {str(e)}")
                    if hasattr(e, 'response') and e.response is not None:
                        print(f"Response: {e.response.text}")
                    raise
            
            except requests.exceptions.RequestException as e:
                print(f"❌ Error calling HuggingFace API: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Response: {e.response.text}")
                raise

# Initialize LLM
def create_agent():
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
    
    llm = HuggingFaceLLM(api_key=api_key)
    
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Decide whether to use tools or end."""
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage):
            tool_calls = parse_tool_calls(last_message.content)
            if tool_calls:
                return "tools"
        return "end"
    
    def call_model(state: AgentState):
        """Call the LLM."""
        messages = state["messages"]
        
        # Build prompt with tool information
        if len(messages) == 1 or not any("TOOL_RESULT" in str(m.content) for m in messages):
            tool_prompt = create_tool_prompt()
            system_msg = SystemMessage(content=f"You are DeepHat, created by Kindo.ai. You are a helpful assistant that is an expert in Cybersecurity and DevOps.\n\n{tool_prompt}")
            prompt_messages = [system_msg] + list(messages)
        else:
            prompt_messages = messages
        
        # Convert to string prompt for HuggingFace
        prompt_text = "\n".join([f"{m.type}: {m.content}" for m in prompt_messages])
        response = llm.invoke(prompt_text)
        
        return {"messages": [AIMessage(content=response)]}
    
    def call_tools(state: AgentState):
        """Execute tools and add results to messages."""
        last_message = state["messages"][-1]
        tool_calls = parse_tool_calls(last_message.content)
        
        if tool_calls:
            results = execute_tools(tool_calls)
            return {"messages": [HumanMessage(content=f"TOOL_RESULTS:\n{results}\n\nNow provide your final answer based on these results.")]}
        
        return {"messages": []}
    
    # Build graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)
    
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

# Create agent instance
agent_executor = create_agent()

# Load demo prompts from JSON file
def load_demo_prompts():
    """Load demo prompts from demos.json file."""
    try:
        # Get the directory of the current script and construct path to demos.json
        script_dir = os.path.dirname(os.path.abspath(__file__))
        demos_path = os.path.join(script_dir, 'demos.json')
        with open(demos_path, 'r') as f:
            data = json.load(f)
            demo_prompts = data.get('demo_prompts', {})
            print(f"✅ Loaded {len(demo_prompts)} demo prompts from {demos_path}")
            return demo_prompts
    except FileNotFoundError:
        print("⚠️  demos.json file not found, using empty demo prompts")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing demos.json: {e}")
        return {}

DEMO_PROMPTS = load_demo_prompts()

def clean_response(content: str) -> str:
    """Clean up the response by removing tool call syntax and extra whitespace."""
    if not content:
        return ""
    
    # Remove TOOL_CALL lines
    lines = content.split('\n')
    cleaned_lines = []
    skip_next = False
    
    for line in lines:
        # Skip TOOL_CALL lines
        if re.match(r'^\s*TOOL_CALL:', line, re.IGNORECASE):
            continue
        # Skip TOOL_RESULTS section header
        if re.match(r'^\s*TOOL_RESULTS:', line, re.IGNORECASE):
            skip_next = True
            continue
        # Skip the instruction line after TOOL_RESULTS
        if skip_next and "provide your final answer" in line.lower():
            skip_next = False
            continue
        
        cleaned_lines.append(line)
    
    # Join and clean up extra whitespace
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)  # Max 2 consecutive newlines
    result = result.strip()
    
    return result

def find_best_matching_demo(message: str, threshold: float = 0.8) -> tuple:
    """Find the best matching demo prompt using fuzzy string matching.

    Args:
        message: The user input message
        threshold: Minimum similarity ratio (0.0 to 1.0) to consider a match

    Returns:
        Tuple of (best_match_key, similarity_ratio) or (None, 0.0) if no match
    """
    best_match = None
    best_ratio = 0.0

    # Normalize the input message for better matching
    normalized_message = message.lower().strip()

    for demo_prompt in DEMO_PROMPTS.keys():
        # Calculate similarity ratio using normalized strings
        ratio = difflib.SequenceMatcher(None, normalized_message, demo_prompt.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = demo_prompt

    # Only return match if it exceeds threshold
    if best_ratio >= threshold:
        return best_match, best_ratio
    else:
        return None, 0.0

def run_agent(message: str, history: list = None):
    """Run the agent with a message and optional history."""
    # Check if the message matches any demo prompt using fuzzy matching
    best_match, similarity = find_best_matching_demo(message)
    if best_match:
        demo_data = DEMO_PROMPTS[best_match]
        print(f'✅ DEMO MATCH FOUND (similarity: {similarity:.2f}) - Using default answer, NOT calling LLM')
        print(f'Demo prompt: {best_match[:100]}...')
        print(f'Final answer: {demo_data["final_answer"][:100]}...')
        # Return both the animation steps, diagram data, and final answer - LLM is NEVER called for demo matches
        return {
            "animation_steps": demo_data["animation_steps"],
            "diagram": demo_data.get("diagram"),
            "final_answer": demo_data["final_answer"]
        }

    # No demo match found - proceed with LLM processing
    print('🤖 No demo match found - calling LLM for response')
    messages = []

    # Add history
    if history:
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    # Add current message
    messages.append(HumanMessage(content=message))

    try:
        # Run agent
        result = agent_executor.invoke({"messages": messages, "tool_calls": []})

        # Extract final response
        final_message = result["messages"][-1]
        content = final_message.content if hasattr(final_message, 'content') else str(final_message)

        # Clean up the response
        cleaned_content = clean_response(content)

        print('✅ Agent response:', cleaned_content[:200] + '...' if len(cleaned_content) > 200 else cleaned_content)

        return cleaned_content

    except Exception as e:
        print(f"❌ Error in run_agent: {str(e)}")
        raise
