import logging
from datetime import datetime, timezone

from regis_cli.playbook.engine import _WIDGET_ENV, _resolve_path, _resolve_template

logging.basicConfig(level=logging.DEBUG)

report = {
    "request": {
        "registry": "registry-1.docker.io",
        "repository": "library/alpine",
        "tag": "latest",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "user": "tristan"
        }
    }
}

val_path = "{{ request.metadata.user | default('Unknown') }}"

print("Testing _resolve_path with report...")
try:
    res = _resolve_path(val_path, report, nested_context=report)
    print("Result:", res)
except Exception as e:
    print("Exception:", e)

print("\nTesting missing metadata...")
report_missing = {
    "request": {
        "registry": "registry-1.docker.io",
        "repository": "library/alpine",
        "tag": "latest",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        # metadata missing or empty
    }
}
try:
    res = _resolve_path(val_path, report_missing, nested_context=report_missing)
    print("Result missing metadata:", res)
except Exception as e:
    print("Exception:", e)

print("Done.")
