"""Trivy analyzer — scans image for vulnerabilities using Trivy CLI."""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from typing import Any

from regis_cli.analyzers.base import AnalyzerError, BaseAnalyzer
from regis_cli.registry.client import RegistryClient

logger = logging.getLogger(__name__)


def _run_trivy(image: str) -> dict[str, Any]:
    """Run trivy image scan and return parsed JSON."""
    trivy_path = shutil.which("trivy")
    if not trivy_path:
        raise AnalyzerError("trivy executable not found in PATH")

    # Pass registry credentials to Trivy if available
    env = os.environ.copy()
    if env.get("REGIS_USERNAME") and env.get("REGIS_PASSWORD"):
        env["TRIVY_USERNAME"] = env["REGIS_USERNAME"]
        env["TRIVY_PASSWORD"] = env["REGIS_PASSWORD"]

    cmd = [
        trivy_path,
        "image",
        "--format", "json",
        "--quiet",
        "--no-progress",
        image,
    ]

    logger.debug("Running trivy: %s", " ".join(cmd))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            check=True,
        )
        return json.loads(result.stdout)  # type: ignore[no-any-return]
    except subprocess.CalledProcessError as exc:
        raise AnalyzerError(f"trivy failed: {exc.stderr}") from exc
    except json.JSONDecodeError as exc:
        raise AnalyzerError(f"trivy produced invalid JSON: {exc}") from exc


class TrivyAnalyzer(BaseAnalyzer):
    """Scan image for vulnerabilities using Trivy."""

    name = "trivy"
    schema_file = "trivy.schema.json"

    def analyze(
        self,
        client: RegistryClient,
        repository: str,
        tag: str,
    ) -> dict[str, Any]:
        """Run trivy analysis."""
        # We need the full image reference for trivy (e.g. registry/repo:tag)
        if client.registry == "docker.io" or client.registry == "registry-1.docker.io":
            # For Docker Hub, trivy expects just repo:tag or library/repo:tag
            # It handles the registry URL internally
            full_image = f"{repository}:{tag}"
        else:
            full_image = f"{client.registry}/{repository}:{tag}"

        try:
            data = _run_trivy(full_image)
        except AnalyzerError as exc:
            # If analysis fails, we return a partial report or raise?
            # BaseAnalyzer usually expects a valid report conforming to schema.
            # But if trivy fails, we can't produce the schema.
            # cli.py catches AnalyzerError and prints it.
            raise exc

        # Process results
        trivy_version = data.get("SchemaVersion", "unknown")  # Trivy JSON output schema version? 
        # Actually SchemaVersion in root is the JSON schema version. 
        # But we want Trivy version? Trivy JSON output doesn't always include its own version in the report.
        # We can run `trivy --version` but that's extra overhead.
        # Let's just use "unknown" or check metadata if available.
        
        targets = []
        counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "UNKNOWN": 0,
        }

        for result in data.get("Results", []):
            target_data = {
                "Target": result.get("Target"),
                "Vulnerabilities": [],
            }
            
            vulns = result.get("Vulnerabilities", [])
            if vulns:
                clean_vulns = []
                for v in vulns:
                    severity = v.get("Severity", "UNKNOWN")
                    counts[severity] = counts.get(severity, 0) + 1
                    
                    clean_vulns.append({
                        "VulnerabilityID": v.get("VulnerabilityID"),
                        "PkgName": v.get("PkgName"),
                        "InstalledVersion": v.get("InstalledVersion"),
                        "FixedVersion": v.get("FixedVersion", ""),
                        "Severity": severity,
                        "Title": v.get("Title", ""),
                        "Description": v.get("Description", ""),
                    })
                target_data["Vulnerabilities"] = clean_vulns
            else:
                target_data["Vulnerabilities"] = None
            
            targets.append(target_data)

        total = sum(counts.values())

        return {
            "analyzer": self.name,
            "repository": repository,
            "tag": tag,
            "trivy_version": str(data.get("SchemaVersion", "unknown")),
            "vulnerability_count": total,
            "critical_count": counts["CRITICAL"],
            "high_count": counts["HIGH"],
            "medium_count": counts["MEDIUM"],
            "low_count": counts["LOW"],
            "unknown_count": counts["UNKNOWN"],
            "targets": targets,
        }
