# Module 02 — The Dual-Graph World Model (ASG + APG)

---

## 🎯 One-Line Summary

CMatrix maintains two living graphs: one that records **what the target is**, and one that records **what can be done to it**. They are kept strictly separate — always.

---

## 🗺️ A Map Analogy to Get Started

Think about how a detective works a crime scene versus how they build a case.

At the scene, they collect **facts**: "There's a broken window on the east side. The alarm was disabled at 11:43 PM. This person's fingerprint is on the safe." These are confirmed observations. The detective writes them down as facts — not guesses.

Later, in their notebook, they build a **theory**: "The suspect entered via the broken window, disabled the alarm using a code they obtained from an employee, and opened the safe. This leads to the conclusion: inside job, accomplice with alarm access."

The facts and the theory are *different kinds of knowledge*. If you mix them up — writing guesses in the evidence log, or treating unconfirmed theories as proven facts — you corrupt both. You end up with a case that doesn't hold up.

CMatrix works exactly this way:
- **ASG** = the evidence log (confirmed discovered facts)
- **APG** = the detective's theory notebook (inferred attack reasoning)

They are never mixed. This is the most important design principle in CMatrix.

---

## 🕸️ Graph 1: The Attack Surface Graph (ASG)

**The ASG answers: "What does the target look like?"**

Every time CMatrix discovers something about the target — a live server, an open port, a technology, a vulnerability — it is written into the ASG as a node. The relationships between these discoveries are recorded as edges (connections between nodes).

The ASG is not a list. It's a **connected knowledge graph** — a living model of the target environment that grows richer as the assessment progresses.

### ASG Node Types — What Gets Stored

Think of each node type as a category of real-world thing that can be discovered:

| Node | What It Represents | Real Example |
|------|--------------------|-------------|
| **Domain** | A web domain or subdomain | `shopvault.io`, `api.shopvault.io` |
| **Host** | A live server with an IP address | `192.168.1.10` (OS: Ubuntu 22.04) |
| **Port** | An open network port on a host | Port 443 (HTTPS), Port 8080 (HTTP) |
| **Service** | The software running on a port | Nginx 1.18.0, Apache 2.4.51 |
| **Technology** | Framework, CMS, library detected | WordPress 5.9.3, Django 4.1 |
| **Endpoint** | A specific URL or API route | `/api/v1/orders`, `/admin/login` |
| **Parameter** | An input field or query param | `user_id=?`, `?q=search` |
| **Vulnerability** | A weakness or CVE — enriched with live intelligence | CVE-2022-21661, SQL error exposure |
| **Evidence** | Proof artifact — screenshot, output | `admin-panel-screenshot.png` |

### ASG Edge Types — How Things Connect

Edges make the ASG a *graph* rather than just a list. They express real-world relationships:

| Edge | What It Means | Example |
|------|---------------|---------|
| `has_host` | A domain resolves to a host | `shopvault.io` → `192.168.1.10` |
| `has_port` | A host has a port open | `192.168.1.10` → Port 443 |
| `runs` | A port runs a service | Port 443 → Nginx 1.18.0 |
| `uses` | A host uses a technology | Host → WordPress 5.9.3 |
| `has_endpoint` | A service has a URL path | Service → `/api/v1/orders` |
| `has_parameter` | An endpoint has an input | `/api/v1/orders` → `user_id=?` |
| `affected_by` | A host/endpoint has a vulnerability | WordPress host → CVE-2022-21661 |
| `validated_by` | A vulnerability has proof | CVE-2022-21661 → screenshot.png |

### The Golden Rule of the ASG

> **The ASG contains only confirmed discovered facts. It never contains hypotheses.**

If something wasn't directly observed or confirmed, it does not go in the ASG. No guesses. No "probably has this." Only facts. This is what makes the ASG trustworthy as a source of truth for all subsequent reasoning.

---

## 🛣️ Graph 2: The Attack Path Graph (APG)

**The APG answers: "What can be done to the target?"**

While the ASG records *what was found*, the APG records *what can be done with those findings*. It is the reasoning layer — the collection of hypothesized, in-progress, and validated attack plans.

The APG is built entirely by the **Commander Agent** through active reasoning over ASG state. It is never automatically derived. It requires intelligence: "Given these vulnerabilities I've found, which ones can chain together into a meaningful attack that achieves real impact?"

### APG Node Types

| Node | What It Represents |
|------|-------------------|
| **AttackChain** | A complete, ordered sequence of exploitation steps from an entry point to a final impact |
| **ChainStep** | A single step within a chain — a specific action on a specific ASG node |
| **Impact** | The business or technical consequence achieved at the end of a chain |

### APG Edge Types

| Edge | What It Means |
|------|---------------|
| `starts_at` | An AttackChain begins at a specific ASG Vulnerability or Endpoint node |
| `next_step` | One ChainStep leads to the next ChainStep |
| `achieves` | The final ChainStep achieves an Impact |
| `supported_by` | A ChainStep is backed by an ASG Evidence node (proof!) |

### Each AttackChain Carries Three Properties

Every AttackChain has metadata that allows the Commander to prioritize and track it:

1. **risk_score** — How dangerous is this chain? Derived from the vulnerability's severity (CVSS), how easy it is to exploit (exploitability), and the classification of the impact (data breach, RCE, etc.).

2. **validation_status** — Where is this chain in its lifecycle? Four possible states:
   - `HYPOTHESIZED` — The Commander thinks this chain is possible. Not yet tested.
   - `PARTIALLY_VALIDATED` — Some steps have been confirmed. Not complete yet.
   - `VALIDATED` — Every step confirmed with evidence. Impact demonstrated. Done.
   - `RULED_OUT` — A step failed after retries. This chain is not exploitable as hypothesized.

3. **priority** — The Commander ranks all active chains by risk score. The highest-priority chain gets validated first. This ranking updates every time a chain's status changes.

### The Golden Rule of the APG

> **The APG contains only inferred attack reasoning. It never contains raw scan data.**

Scan results, tool outputs, raw findings — these belong in the ASG. The APG is strictly a reasoning layer. Mixing them would corrupt the clarity that makes both graphs valuable.

---

## ⚖️ The Separation Principle — Why This Matters So Much

Here's a subtle but critical point: why are these two graphs kept **strictly separate** instead of just being one big combined graph?

Because **facts and hypotheses are different kinds of knowledge**, and conflating them causes real problems.

Consider what happens if you mix them in a typical system:
- You scan a target and find WordPress 5.9.3 with CVE-2022-21661.
- You also "think" there might be an SQL injection attack path.
- You store both in the same place.

Now your system tries to re-plan. It looks at its knowledge store and sees both "WordPress 5.9.3 discovered" (fact) and "SQL injection path possible" (hypothesis) as equivalent entries. It can't distinguish which to trust. It may plan exploits based on unconfirmed hypotheses, or worse, treat a failed hypothesis as evidence about the target's nature.

CMatrix's separation principle eliminates this entire class of errors:

- **Discovery agents write only to the ASG** — they discover facts. They never reason about attack chains.
- **The Commander writes only to the APG** — it reasons about attack chains. It never runs tools.
- **Each layer is authoritative for exactly one type of knowledge.**

This creates a clean information architecture where every piece of knowledge has a home, a purpose, and clear ownership.

---

## 🔗 How the Two Graphs Work Together

The graphs are separate but interdependent:

1. **ASG feeds APG reasoning.** When the Commander reads a new Vulnerability node in the ASG, it reasons: "What attack chain could start here?" It creates a new AttackChain in the APG rooted at that ASG node.

2. **APG chain status drives re-planning.** When a chain is validated or ruled out, the Commander re-reads the APG priority list and decides what to do next.

3. **APG evidence links back to ASG.** When an AttackChain is validated, each ChainStep is connected to an ASG Evidence node via `supported_by` edges. This makes every claimed attack traceable back to concrete proof.

Think of it as a dialogue between two layers of intelligence: the ASG constantly grows with new facts, and the APG constantly evolves as the Commander turns those facts into attack understanding.

---

## 🔬 A Tiny Concrete Example

Let's trace one discovery through both graphs:

> The Recon Agent runs Nmap on `shopvault.io` and finds port 8080 running an HTTP service.

**ASG update:** A new Port node (`8080`) and Service node (`HTTP, unencrypted`) are written to the ASG. They are linked to the Host node for `shopvault.io` via `has_port` and `runs` edges.

> WhatWeb identifies WordPress 5.9.3 running on the main domain.

**ASG update:** A Technology node (`WordPress 5.9.3`) is written. The Research Agent finds CVE-2022-21661 (CVSS 8.8, public PoC exists). A Vulnerability node is written with all enriched attributes. An `affected_by` edge connects the Host to the Vulnerability.

> The Commander reads the new Vulnerability node from the ASG. It reasons: "CVE-2022-21661 on WordPress → SQL injection → possible database dump → customer PII exposure."

**APG update:** The Commander creates a new AttackChain in the APG:
- Chain-01, risk_score 8.8, status `HYPOTHESIZED`
- ChainStep 1: Exploit WP_Query via SQLMap
- ChainStep 2: Extract admin credentials
- ChainStep 3: Authenticate → deploy shell → achieve RCE
- Impact: Full server access, customer data exposure

> The Validation Agent runs SQLMap and Metasploit. All steps succeed.

**APG update:** Chain-01 status advances to `VALIDATED`. Each ChainStep's `supported_by` edge is linked to the Evidence nodes (screenshots) in the ASG.

In under four steps, the dual-graph model captured a complete, evidence-backed, end-to-end attack chain.

---

## ✅ What You Should Remember From This Module

| Concept | Plain English |
|---------|---------------|
| ASG | Living graph of everything *discovered* about the target — facts only |
| APG | Living graph of all *attack plans* inferred by the Commander — reasoning only |
| Separation principle | Facts and hypotheses are different kinds of knowledge — mixing them causes errors |
| How they connect | ASG facts trigger APG chain creation; APG chains link back to ASG evidence |
| Termination | Mission ends when ASG has no unexplored nodes AND all APG chains are in terminal states |

---

*Next: Module 03 — The Agent Architecture (Who Does What)*
