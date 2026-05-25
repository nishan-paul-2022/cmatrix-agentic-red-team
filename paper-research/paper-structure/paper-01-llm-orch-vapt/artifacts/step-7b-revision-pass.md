# Step 7b: Revision Pass Summary

This document summarizes the technical and textual revisions implemented to address the "Major Revision" requirements identified in the Hostile Peer Review (Step 7a).

## 1. Methodological Enhancements

### A. Formalizing State Serialization
*   **Change**: Updated Section IV.B (Methodology) to explicitly describe the **JSON-B serialization** of LangGraph thread states.
*   **Detail**: Clarified that the persistence layer stores not just the message history, but the internal thought buffers and intermediate tool outputs, ensuring that fallback models resume from the exact node where the failure occurred.

### B. Objective Complexity Weighting
*   **Change**: Updated Section IV.C (Methodology) to clarify the derivation of $w_i$.
*   **Detail**: Established the use of a **Security Reasoning Ontology** mapped to MITRE ATT&CK techniques, removing the reliance on manual/subjective expert weighting.

## 2. Theoretical Extensions

### A. Gray Failure Discussion
*   **Change**: Added Subsection VI.A (Performance Degradation and Gray Failures).
*   **Detail**: Addressed the limitation of the current APF engine regarding latency spikes and hallucinations, proposing **In-Context Verification (ICV)** loops as a future mitigation.

### B. Router Failure Modes
*   **Change**: Added Subsection VI.B (Failure Modes of the Dynamic Router).
*   **Detail**: Analyzed scenarios where the DCAT signal might under-estimate complexity and formalized the **Reactive Escalation** policy (elevating to Reasoning-tier after three failed attempts).

## 3. Formatting Refinements
*   **Equation Scaling**: Split Equation 1 (Complexity) and refactored Equation 2 (Optimization) to ensure perfect single-column alignment.
*   **Layout Consistency**: Reverted all full-width `figure*` and `table*` environments to standard `figure` and `table` column-width formats for IEEE compliance.
