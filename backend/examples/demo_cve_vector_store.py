"""Demo script for CVE Vector Store.

This script demonstrates the capabilities of the CVE Vector Store:
1. Initialization and setup
2. Adding sample CVEs
3. Semantic search
4. Hybrid search (semantic + filters)
5. CVSS score filtering
6. Severity filtering
7. Exploit filtering
8. Statistics and performance

Usage:
    python examples/demo_cve_vector_store.py
"""

import sys
import os
import asyncio
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from app.services.rag.cve_vector_store import (
    CVEVectorStore,
    CVEMetadata,
    CVSSScore,
    get_cve_vector_store
)


def create_sample_cves():
    """Create sample CVEs for demonstration."""
    return [
        CVEMetadata(
            cve_id="CVE-2021-44228",
            description="Apache Log4j2 2.0-beta9 through 2.15.0 (excluding security releases 2.12.2, 2.12.3, and 2.3.1) JNDI features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP and other JNDI related endpoints. An attacker who can control log messages or log message parameters can execute arbitrary code loaded from LDAP servers when message lookup substitution is enabled.",
            published_date="2021-12-10T10:15:09.000",
            last_modified_date="2023-11-07T04:22:02.000",
            cvss_v3_1=CVSSScore(
                version="v3.1",
                base_score=10.0,
                severity="CRITICAL",
                vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                exploitability_score=3.9,
                impact_score=6.0
            ),
            cwe_ids=["CWE-502", "CWE-400"],
            cpe_uris=[
                "cpe:2.3:a:apache:log4j:2.0:*:*:*:*:*:*:*",
                "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*"
            ],
            exploit_available=True,
            exploit_maturity="FUNCTIONAL",
            references=[
                "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
                "https://www.exploit-db.com/exploits/50592",
                "https://logging.apache.org/log4j/2.x/security.html"
            ],
            patch_available=True,
            patch_references=["https://logging.apache.org/log4j/2.x/security.html"],
            vendor="apache",
            product="log4j"
        ),
        CVEMetadata(
            cve_id="CVE-2021-45046",
            description="It was found that the fix to address CVE-2021-44228 in Apache Log4j 2.15.0 was incomplete in certain non-default configurations. This could allow attackers with control over Thread Context Map (MDC) input data when the logging configuration uses a non-default Pattern Layout with either a Context Lookup or a Thread Context Map pattern to craft malicious input data using a JNDI Lookup pattern resulting in an information leak and remote code execution in some environments.",
            published_date="2021-12-14T20:15:12.000",
            last_modified_date="2023-11-07T04:22:02.000",
            cvss_v3_1=CVSSScore(
                version="v3.1",
                base_score=9.0,
                severity="CRITICAL",
                vector_string="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H",
                exploitability_score=2.2,
                impact_score=6.0
            ),
            cwe_ids=["CWE-917"],
            cpe_uris=["cpe:2.3:a:apache:log4j:2.15.0:*:*:*:*:*:*:*"],
            exploit_available=True,
            exploit_maturity="POC",
            references=[
                "https://nvd.nist.gov/vuln/detail/CVE-2021-45046",
                "https://logging.apache.org/log4j/2.x/security.html"
            ],
            patch_available=True,
            patch_references=["https://logging.apache.org/log4j/2.x/security.html"],
            vendor="apache",
            product="log4j"
        ),
        CVEMetadata(
            cve_id="CVE-2022-22965",
            description="A Spring MVC or Spring WebFlux application running on JDK 9+ may be vulnerable to remote code execution (RCE) via data binding. The specific exploit requires the application to run on Tomcat as a WAR deployment. If the application is deployed as a Spring Boot executable jar, i.e. the default, it is not vulnerable to the exploit. However, the nature of the vulnerability is more general, and there may be other ways to exploit it.",
            published_date="2022-04-01T23:15:13.000",
            last_modified_date="2023-11-07T03:45:32.000",
            cvss_v3_1=CVSSScore(
                version="v3.1",
                base_score=9.8,
                severity="CRITICAL",
                vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                exploitability_score=3.9,
                impact_score=5.9
            ),
            cwe_ids=["CWE-94"],
            cpe_uris=["cpe:2.3:a:vmware:spring_framework:5.3.0:*:*:*:*:*:*:*"],
            exploit_available=True,
            exploit_maturity="FUNCTIONAL",
            references=[
                "https://nvd.nist.gov/vuln/detail/CVE-2022-22965",
                "https://spring.io/blog/2022/03/31/spring-framework-rce-early-announcement"
            ],
            patch_available=True,
            patch_references=["https://spring.io/blog/2022/03/31/spring-framework-rce-early-announcement"],
            vendor="vmware",
            product="spring_framework"
        ),
        CVEMetadata(
            cve_id="CVE-2023-12345",
            description="Example SQL injection vulnerability in a web application allows remote attackers to execute arbitrary SQL commands via the 'id' parameter.",
            published_date="2023-06-15T10:00:00.000",
            last_modified_date="2023-06-20T10:00:00.000",
            cvss_v3_1=CVSSScore(
                version="v3.1",
                base_score=7.5,
                severity="HIGH",
                vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
                exploitability_score=3.9,
                impact_score=3.6
            ),
            cwe_ids=["CWE-89"],
            cpe_uris=["cpe:2.3:a:example:webapp:1.0:*:*:*:*:*:*:*"],
            exploit_available=False,
            references=["https://example.com/security/CVE-2023-12345"],
            patch_available=True,
            patch_references=["https://example.com/security/CVE-2023-12345"],
            vendor="example",
            product="webapp"
        ),
        CVEMetadata(
            cve_id="CVE-2023-67890",
            description="Example cross-site scripting (XSS) vulnerability in a web application allows remote attackers to inject arbitrary web script or HTML via the 'search' parameter.",
            published_date="2023-08-01T10:00:00.000",
            last_modified_date="2023-08-05T10:00:00.000",
            cvss_v3_1=CVSSScore(
                version="v3.1",
                base_score=6.1,
                severity="MEDIUM",
                vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
                exploitability_score=2.8,
                impact_score=2.7
            ),
            cwe_ids=["CWE-79"],
            cpe_uris=["cpe:2.3:a:example:webapp:1.0:*:*:*:*:*:*:*"],
            exploit_available=False,
            references=["https://example.com/security/CVE-2023-67890"],
            patch_available=False,
            vendor="example",
            product="webapp"
        )
    ]


async def demo_initialization():
    """Demo 1: Initialize CVE Vector Store."""
    print("\n" + "="*80)
    print("DEMO 1: CVE Vector Store Initialization")
    print("="*80)
    
    store = get_cve_vector_store()
    success = await store.initialize()
    
    if success:
        print("✅ CVE Vector Store initialized successfully")
        stats = await store.get_stats()
        print(f"📊 Collection: {stats.get('collection_name', 'N/A')}")
        print(f"📊 Embedding Dimension: {stats.get('embedding_dimension', 'N/A')}")
        print(f"📊 Total CVEs: {stats.get('total_cves', 0)}")
    else:
        print("❌ Failed to initialize CVE Vector Store")
        print("⚠️  Make sure Qdrant is running (docker compose up qdrant)")
        return False
    
    return True


async def demo_add_cves():
    """Demo 2: Add sample CVEs."""
    print("\n" + "="*80)
    print("DEMO 2: Adding Sample CVEs")
    print("="*80)
    
    store = get_cve_vector_store()
    sample_cves = create_sample_cves()
    
    print(f"Adding {len(sample_cves)} sample CVEs...")
    successful, failed = await store.add_cves_batch(sample_cves)
    
    print(f"✅ Successfully added: {successful}")
    print(f"❌ Failed: {failed}")
    
    # Show stats
    stats = await store.get_stats()
    print(f"📊 Total CVEs in store: {stats.get('total_cves', 0)}")


async def demo_semantic_search():
    """Demo 3: Semantic search."""
    print("\n" + "="*80)
    print("DEMO 3: Semantic Search")
    print("="*80)
    
    store = get_cve_vector_store()
    
    queries = [
        "Apache Log4j remote code execution",
        "Spring Framework RCE vulnerability",
        "SQL injection in web application"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: \"{query}\"")
        print("-" * 80)
        
        response = await store.search(query=query, limit=3)
        
        print(f"⏱️  Search time: {response.search_time_ms:.2f}ms")
        print(f"📊 Results found: {response.total_found}")
        
        for i, result in enumerate(response.results, 1):
            print(f"\n  #{i} {result.cve_id} (Score: {result.score:.3f})")
            print(f"     CVSS: {store._get_highest_cvss_score(result.metadata):.1f} ({result.metadata.cvss_v3_1.severity if result.metadata.cvss_v3_1 else 'N/A'})")
            print(f"     {result.description[:150]}...")


async def demo_cvss_filtering():
    """Demo 4: CVSS score filtering."""
    print("\n" + "="*80)
    print("DEMO 4: CVSS Score Filtering")
    print("="*80)
    
    store = get_cve_vector_store()
    
    print("\n🔍 Searching for CRITICAL vulnerabilities (CVSS >= 9.0)")
    print("-" * 80)
    
    response = await store.search(
        query="vulnerability",
        min_cvss_score=9.0,
        limit=5
    )
    
    print(f"⏱️  Search time: {response.search_time_ms:.2f}ms")
    print(f"📊 Results found: {response.total_found}")
    
    for i, result in enumerate(response.results, 1):
        cvss = store._get_highest_cvss_score(result.metadata)
        print(f"\n  #{i} {result.cve_id}")
        print(f"     CVSS: {cvss:.1f} ({result.metadata.cvss_v3_1.severity if result.metadata.cvss_v3_1 else 'N/A'})")
        print(f"     {result.description[:100]}...")


async def demo_severity_filtering():
    """Demo 5: Severity filtering."""
    print("\n" + "="*80)
    print("DEMO 5: Severity Filtering")
    print("="*80)
    
    store = get_cve_vector_store()
    
    severities = ["CRITICAL", "HIGH", "MEDIUM"]
    
    for severity in severities:
        print(f"\n🔍 Searching for {severity} severity vulnerabilities")
        print("-" * 80)
        
        response = await store.search(
            query="vulnerability",
            severity=severity,
            limit=3
        )
        
        print(f"📊 Found {response.total_found} results")
        
        for i, result in enumerate(response.results, 1):
            print(f"  • {result.cve_id} - {result.metadata.cvss_v3_1.severity if result.metadata.cvss_v3_1 else 'N/A'}")


async def demo_exploit_filtering():
    """Demo 6: Exploit availability filtering."""
    print("\n" + "="*80)
    print("DEMO 6: Exploit Availability Filtering")
    print("="*80)
    
    store = get_cve_vector_store()
    
    print("\n🔍 Searching for vulnerabilities with public exploits")
    print("-" * 80)
    
    response = await store.search(
        query="remote code execution",
        exploit_available=True,
        limit=5
    )
    
    print(f"⏱️  Search time: {response.search_time_ms:.2f}ms")
    print(f"📊 Results found: {response.total_found}")
    
    for i, result in enumerate(response.results, 1):
        print(f"\n  #{i} {result.cve_id}")
        print(f"     Exploit Available: {'✅ Yes' if result.metadata.exploit_available else '❌ No'}")
        print(f"     Exploit Maturity: {result.metadata.exploit_maturity or 'N/A'}")
        print(f"     CVSS: {store._get_highest_cvss_score(result.metadata):.1f}")


async def demo_hybrid_search():
    """Demo 7: Hybrid search (semantic + multiple filters)."""
    print("\n" + "="*80)
    print("DEMO 7: Hybrid Search (Semantic + Multiple Filters)")
    print("="*80)
    
    store = get_cve_vector_store()
    
    print("\n🔍 Query: 'remote code execution'")
    print("📋 Filters:")
    print("   • CVSS >= 9.0")
    print("   • Severity: CRITICAL")
    print("   • Exploit Available: Yes")
    print("   • Published after: 2021-01-01")
    print("-" * 80)
    
    response = await store.search(
        query="remote code execution",
        min_cvss_score=9.0,
        severity="CRITICAL",
        exploit_available=True,
        published_after="2021-01-01",
        limit=5
    )
    
    print(f"⏱️  Search time: {response.search_time_ms:.2f}ms")
    print(f"📊 Results found: {response.total_found}")
    
    for i, result in enumerate(response.results, 1):
        print(f"\n  #{i} {result.cve_id} (Score: {result.score:.3f})")
        print(f"     CVSS: {store._get_highest_cvss_score(result.metadata):.1f} ({result.metadata.cvss_v3_1.severity if result.metadata.cvss_v3_1 else 'N/A'})")
        print(f"     Published: {result.metadata.published_date[:10]}")
        print(f"     Exploit: {'✅ Yes' if result.metadata.exploit_available else '❌ No'}")
        print(f"     {result.description[:100]}...")


async def demo_get_by_id():
    """Demo 8: Retrieve CVE by ID."""
    print("\n" + "="*80)
    print("DEMO 8: Retrieve CVE by ID")
    print("="*80)
    
    store = get_cve_vector_store()
    
    cve_id = "CVE-2021-44228"
    print(f"\n🔍 Retrieving {cve_id}...")
    print("-" * 80)
    
    cve = await store.get_cve_by_id(cve_id)
    
    if cve:
        print(f"✅ Found: {cve.cve_id}")
        print(f"📝 Description: {cve.description[:200]}...")
        print(f"📊 CVSS: {store._get_highest_cvss_score(cve):.1f} ({cve.cvss_v3_1.severity if cve.cvss_v3_1 else 'N/A'})")
        print(f"📅 Published: {cve.published_date[:10]}")
        print(f"🔗 References: {len(cve.references)}")
        print(f"🛡️  Patch Available: {'✅ Yes' if cve.patch_available else '❌ No'}")
        print(f"💥 Exploit Available: {'✅ Yes' if cve.exploit_available else '❌ No'}")
    else:
        print(f"❌ CVE not found")


async def demo_statistics():
    """Demo 9: Vector store statistics."""
    print("\n" + "="*80)
    print("DEMO 9: Vector Store Statistics")
    print("="*80)
    
    store = get_cve_vector_store()
    stats = await store.get_stats()
    
    print("\n📊 CVE Vector Store Statistics:")
    print("-" * 80)
    print(f"  Collection Name: {stats.get('collection_name', 'N/A')}")
    print(f"  Total CVEs: {stats.get('total_cves', 0):,}")
    print(f"  Vectors Count: {stats.get('vectors_count', 0):,}")
    print(f"  Indexed Vectors: {stats.get('indexed_vectors_count', 0):,}")
    print(f"  Embedding Dimension: {stats.get('embedding_dimension', 'N/A')}")
    print(f"  Status: {stats.get('status', 'N/A')}")


async def main():
    """Run all demos."""
    print("\n" + "="*80)
    print("CVE VECTOR STORE - COMPREHENSIVE DEMO")
    print("="*80)
    print("\nThis demo showcases the CVE Vector Store capabilities:")
    print("  1. Initialization and setup")
    print("  2. Adding sample CVEs")
    print("  3. Semantic search")
    print("  4. CVSS score filtering")
    print("  5. Severity filtering")
    print("  6. Exploit availability filtering")
    print("  7. Hybrid search (semantic + filters)")
    print("  8. Retrieve CVE by ID")
    print("  9. Statistics")
    
    # Run demos
    if not await demo_initialization():
        return
    
    await demo_add_cves()
    await demo_semantic_search()
    await demo_cvss_filtering()
    await demo_severity_filtering()
    await demo_exploit_filtering()
    await demo_hybrid_search()
    await demo_get_by_id()
    await demo_statistics()
    
    print("\n" + "="*80)
    print("🎉 DEMO COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("  • Run NVD sync: python scripts/sync_nvd.py --test")
    print("  • Integrate with VulnIntelAgent")
    print("  • Set up daily incremental sync")
    print("  • Monitor performance and optimize")


if __name__ == '__main__':
    asyncio.run(main())
