from unittest.mock import Mock, patch

import pytest

from app.services.rag.cve_graph import CVEGraphTraversal


@pytest.mark.asyncio
async def test_build_graph_single_node():
    """Test building a graph with a single CVE node."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "vulnerabilities": [
            {
                "cve": {
                    "id": "CVE-2021-44228",
                    "descriptions": [{"value": "Log4j vulnerability"}],
                    "metrics": {
                        "cvssMetricV31": [
                            {"cvssData": {"baseScore": 10.0, "baseSeverity": "CRITICAL"}}
                        ]
                    },
                    "references": [],
                }
            }
        ]
    }

    with patch("requests.get", return_value=mock_response):
        service = CVEGraphTraversal()
        graph_data = await service.build_graph("CVE-2021-44228", max_depth=1)

        assert len(graph_data["nodes"]) == 1
        assert graph_data["nodes"][0]["id"] == "CVE-2021-44228"
        assert graph_data["nodes"][0]["score"] == 10.0
        assert graph_data["nodes"][0]["severity"] == "CRITICAL"


@pytest.mark.asyncio
async def test_build_graph_with_relations():
    """Test building a graph where one CVE references another."""

    def side_effect(url, params, **kwargs):
        cve_id = params["cveId"]
        mock_resp = Mock()
        mock_resp.status_code = 200

        if cve_id == "CVE-2021-44228":
            mock_resp.json.return_value = {
                "vulnerabilities": [
                    {
                        "cve": {
                            "id": "CVE-2021-44228",
                            "descriptions": [{"value": "Log4j"}],
                            "metrics": {},
                            "references": [
                                {"url": "https://nvd.nist.gov/vuln/detail/CVE-2021-1234"}
                            ],
                        }
                    }
                ]
            }
        elif cve_id == "CVE-2021-1234":
            mock_resp.json.return_value = {
                "vulnerabilities": [
                    {
                        "cve": {
                            "id": "CVE-2021-1234",
                            "descriptions": [{"value": "Related vuln"}],
                            "metrics": {},
                            "references": [],
                        }
                    }
                ]
            }
        else:
            mock_resp.json.return_value = {"vulnerabilities": []}

        return mock_resp

    with patch("requests.get", side_effect=side_effect):
        service = CVEGraphTraversal()
        graph_data = await service.build_graph("CVE-2021-44228", max_depth=2)

        # Handle NetworkX version differences if any
        if "edges" in graph_data:
            graph_data["links"] = graph_data["edges"]

        assert len(graph_data["nodes"]) == 2
        assert len(graph_data["links"]) == 1

        # NetworkX node_link_data structure puts source/target as IDs
        link = graph_data["links"][0]

        assert link["source"] == "CVE-2021-44228"
        assert link["target"] == "CVE-2021-1234"
        assert link["relation"] == "referenced_in_url"


@pytest.mark.asyncio
async def test_max_depth_limit():
    """Test that traversal respects the max_depth parameter."""

    # Chain: A -> B -> C. Max depth 1 should only get A -> B.
    def side_effect(url, params, **kwargs):
        cve_id = params["cveId"]
        mock_resp = Mock()
        mock_resp.status_code = 200

        if cve_id == "CVE-2021-0001":
            mock_resp.json.return_value = {
                "vulnerabilities": [
                    {
                        "cve": {
                            "id": "CVE-2021-0001",
                            "descriptions": [{"value": "A"}],
                            "references": [{"url": "http://site.com/CVE-2021-0002"}],
                        }
                    }
                ]
            }
        elif cve_id == "CVE-2021-0002":
            mock_resp.json.return_value = {
                "vulnerabilities": [
                    {
                        "cve": {
                            "id": "CVE-2021-0002",
                            "descriptions": [{"value": "B"}],
                            "references": [{"url": "http://site.com/CVE-2021-0003"}],
                        }
                    }
                ]
            }
        elif cve_id == "CVE-2021-0003":
            mock_resp.json.return_value = {
                "vulnerabilities": [
                    {
                        "cve": {
                            "id": "CVE-2021-0003",
                            "descriptions": [{"value": "C"}],
                            "references": [],
                        }
                    }
                ]
            }
        else:
            mock_resp.json.return_value = {"vulnerabilities": []}

        return mock_resp

    with patch("requests.get", side_effect=side_effect):
        service = CVEGraphTraversal()
        # Depth 1: Start (0) -> Child (1). Should stop there.
        graph_data = await service.build_graph("CVE-2021-0001", max_depth=1)

        node_ids = [n["id"] for n in graph_data["nodes"]]

        assert "CVE-2021-0001" in node_ids
        assert "CVE-2021-0002" in node_ids
        assert "CVE-2021-0003" not in node_ids
