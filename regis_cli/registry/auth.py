"""Authentication resolution for the Docker Registry."""

from __future__ import annotations

import base64
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def resolve_credentials(
    registry: str,
    cli_auths: list[str] | None = None,
) -> tuple[str | None, str | None]:
    """Resolve credentials for a given registry domain.
    
    Order of precedence:
    1. CLI-provided auth overrides (--auth flag)
    2. Domain-specific env vars (e.g., REGIS_AUTH_REGISTRY_EXAMPLE_COM_USERNAME)
    3. Global env vars (REGIS_USERNAME / REGIS_PASSWORD)
    4. Docker config.json (~/.docker/config.json)
    
    Args:
        registry: The registry hostname to authenticate against.
        cli_auths: A list of string overrides in the form 'registry=user:pass'.
        
    Returns:
        A tuple of (username, password) if found, otherwise (None, None).
    """
    # 1. Check CLI overrides
    if cli_auths:
        for auth_override in cli_auths:
            if "=" in auth_override:
                domain, creds = auth_override.split("=", 1)
                if domain == registry and ":" in creds:
                    user, pwd = creds.split(":", 1)
                    logger.debug("Using CLI override credentials for %s", registry)
                    return user, pwd

    # 2. Check domain-specific environment variables
    env_domain = registry.upper().replace(".", "_").replace(":", "_").replace("-", "_")
    domain_user = os.environ.get(f"REGIS_AUTH_{env_domain}_USERNAME")
    domain_pass = os.environ.get(f"REGIS_AUTH_{env_domain}_PASSWORD")
    if domain_user and domain_pass:
        logger.debug("Using domain-specific env vars for %s", registry)
        return domain_user, domain_pass

    # 3. Check global environment variables
    global_user = os.environ.get("REGIS_USERNAME")
    global_pass = os.environ.get("REGIS_PASSWORD")
    if global_user and global_pass:
        logger.debug("Using global env vars for %s", registry)
        return global_user, global_pass

    # 4. Check Docker config.json
    try:
        docker_config_path = Path.home() / ".docker" / "config.json"
        if docker_config_path.exists():
            with open(docker_config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            auths = config.get("auths", {})
            
            candidates = [
                registry,
                f"https://{registry}",
                f"https://{registry}/v1/",
                f"https://{registry}/v2/",
                "https://index.docker.io/v1/" if registry in ("docker.io", "registry-1.docker.io") else registry,
            ]
            for candidate in candidates:
                if candidate in auths and "auth" in auths[candidate]:
                    auth_b64 = auths[candidate]["auth"]
                    try:
                        auth_str = base64.b64decode(auth_b64).decode("utf-8")
                        if ":" in auth_str:
                            user, pwd = auth_str.split(":", 1)
                            logger.debug("Using Docker config.json credentials for %s", registry)
                            return user, pwd
                    except Exception as e:
                        logger.debug("Failed to decode auth from config.json for %s: %s", candidate, e)
    except Exception as e:
        logger.debug("Failed to read ~/.docker/config.json: %s", e)

    return None, None
