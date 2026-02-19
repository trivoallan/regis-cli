"""HTML report renderer for regis-cli."""

from __future__ import annotations

import html
import json
from typing import Any


def _score_color(score: float | int | None, max_score: float = 10) -> str:
    """Return a CSS color for a numeric score."""
    if score is None:
        return "#6b7280"
    ratio = score / max_score
    if ratio >= 0.7:
        return "#22c55e"
    if ratio >= 0.4:
        return "#f59e0b"
    return "#ef4444"


def _badge(label: str, value: str, color: str = "#6366f1") -> str:
    """Render a small badge."""
    return (
        f'<span style="display:inline-flex;align-items:center;gap:4px;'
        f'background:{color}22;color:{color};border:1px solid {color}44;'
        f'border-radius:6px;padding:2px 8px;font-size:0.8rem;font-weight:600;">'
        f'{html.escape(label)}: {html.escape(str(value))}</span>'
    )


def _bool_icon(val: bool | None) -> str:
    if val is True:
        return "✅"
    if val is False:
        return "❌"
    return "➖"


def _section(title: str, content: str, icon: str = "📦") -> str:
    return (
        f'<details open><summary style="cursor:pointer;font-size:1.15rem;'
        f'font-weight:700;padding:12px 0;border-bottom:1px solid #333;'
        f'margin-bottom:12px;">{icon} {html.escape(title)}</summary>'
        f'<div style="padding:0 0 16px 0;">{content}</div></details>'
    )


def _table(headers: list[str], rows: list[list[str]]) -> str:
    ths = "".join(
        f'<th style="text-align:left;padding:8px 12px;border-bottom:2px solid #444;'
        f'font-size:0.85rem;text-transform:uppercase;letter-spacing:0.05em;'
        f'color:#94a3b8;">{html.escape(h)}</th>'
        for h in headers
    )
    trs = ""
    for row in rows:
        tds = "".join(
            f'<td style="padding:8px 12px;border-bottom:1px solid #2a2a2a;'
            f'font-size:0.9rem;">{cell}</td>'
            for cell in row
        )
        trs += f"<tr>{tds}</tr>"
    return (
        f'<table style="width:100%;border-collapse:collapse;margin:8px 0;">'
        f"<thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>"
    )


def _score_bar(score: float | int, max_score: float = 10) -> str:
    pct = max(0, min(100, score / max_score * 100))
    color = _score_color(score, max_score)
    return (
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<div style="flex:1;height:8px;background:#1e1e2e;border-radius:4px;overflow:hidden;">'
        f'<div style="width:{pct:.0f}%;height:100%;background:{color};border-radius:4px;'
        f'transition:width 0.3s;"></div></div>'
        f'<span style="font-weight:700;color:{color};min-width:36px;text-align:right;">'
        f'{score}</span></div>'
    )


# ---------------------------------------------------------------------------
# Per-analyzer renderers
# ---------------------------------------------------------------------------

def _render_tags(data: dict[str, Any]) -> str:
    tags = data.get("tags", [])
    sample = tags[:30]
    badges = " ".join(_badge("tag", t, "#6366f1") for t in sample)
    extra = f"<p style='color:#94a3b8;margin-top:8px;'>… and {len(tags) - 30} more</p>" if len(tags) > 30 else ""
    return _section(
        f"Tags ({data.get('total_tags', len(tags))})",
        f"<div style='display:flex;flex-wrap:wrap;gap:6px;'>{badges}</div>{extra}",
        "🏷️",
    )


def _render_image(data: dict[str, Any]) -> str:
    platforms = data.get("platforms", [])
    if not platforms:
        return _section("Image", "<p>No platform data available.</p>", "🖼️")
    rows = []
    for p in platforms:
        rows.append([
            html.escape(str(p.get("architecture", ""))),
            html.escape(str(p.get("os", ""))),
            html.escape(str(p.get("variant", "-"))),
            str(p.get("layers", "-")),
            html.escape(str(p.get("created", "-"))),
        ])
    return _section("Image", _table(["Arch", "OS", "Variant", "Layers", "Created"], rows), "🖼️")


def _render_versioning(data: dict[str, Any]) -> str:
    patterns = data.get("patterns", [])
    rows = [[
        html.escape(p["pattern"]),
        str(p["count"]),
        f'{p["percentage"]}%',
        ", ".join(p.get("examples", [])[:5]),
    ] for p in patterns]
    badges_html = (
        _badge("Dominant", data.get("dominant_pattern", "?"), "#8b5cf6") + " " +
        _badge("SemVer", f'{data.get("semver_compliant_percentage", 0)}%', "#22c55e")
    )
    return _section(
        "Versioning",
        f"<div style='margin-bottom:12px;'>{badges_html}</div>"
        + _table(["Pattern", "Count", "%", "Examples"], rows),
        "🔢",
    )


def _render_scorecard(data: dict[str, Any]) -> str:
    if not data.get("scorecard_available"):
        return _section("Scorecard", "<p style='color:#94a3b8;'>Scorecard data not available.</p>", "🛡️")
    score = data.get("score", 0)
    checks = data.get("checks", [])
    rows = []
    for c in checks:
        s = c.get("score", -1)
        bar = _score_bar(s) if s >= 0 else '<span style="color:#6b7280;">N/A</span>'
        rows.append([html.escape(c["name"]), bar, html.escape(c.get("reason", "")[:80])])
    repo_html = f'<a href="{html.escape(data.get("source_repo", ""))}" style="color:#818cf8;">{html.escape(data.get("source_repo", ""))}</a>' if data.get("source_repo") else ""
    return _section(
        "OpenSSF Scorecard",
        f"<div style='margin-bottom:16px;'>"
        f"<div style='font-size:2.5rem;font-weight:800;color:{_score_color(score)};'>{score}/10</div>"
        f"<div style='margin-top:4px;'>{repo_html}</div></div>"
        + _table(["Check", "Score", "Reason"], rows),
        "🛡️",
    )


def _render_endoflife(data: dict[str, Any]) -> str:
    if not data.get("product_found"):
        return _section("End-of-Life", "<p style='color:#94a3b8;'>Product not found on endoflife.date.</p>", "📅")
    matched = data.get("matched_cycle")
    is_eol = data.get("is_eol")
    status = _badge("EOL", "Yes", "#ef4444") if is_eol else _badge("Supported", "Yes", "#22c55e") if is_eol is False else _badge("Unknown", "—", "#6b7280")
    info = ""
    if matched:
        info = _table(
            ["Cycle", "Release", "EOL", "Latest", "LTS"],
            [[
                html.escape(str(matched.get("cycle", ""))),
                html.escape(str(matched.get("release_date", ""))),
                html.escape(str(matched.get("eol", ""))),
                html.escape(str(matched.get("latest", ""))),
                _bool_icon(matched.get("lts")),
            ]]
        )
    counts = (
        f"<div style='margin-top:8px;display:flex;gap:8px;'>"
        f"{_badge('Active cycles', str(data.get('active_cycles_count', '?')), '#22c55e')}"
        f"{_badge('EOL cycles', str(data.get('eol_cycles_count', '?')), '#ef4444')}</div>"
    )
    return _section("End-of-Life", f"{status}{info}{counts}", "📅")


def _render_popularity(data: dict[str, Any]) -> str:
    if not data.get("available"):
        return _section("Popularity", "<p style='color:#94a3b8;'>Docker Hub data not available.</p>", "⭐")
    pulls = data.get("pull_count", 0)
    stars = data.get("star_count", 0)
    pulls_fmt = f"{pulls:,}"
    return _section(
        "Popularity",
        f"<div style='display:flex;gap:24px;flex-wrap:wrap;'>"
        f"<div style='text-align:center;'><div style='font-size:2rem;font-weight:800;color:#818cf8;'>{pulls_fmt}</div>"
        f"<div style='color:#94a3b8;font-size:0.85rem;'>Downloads</div></div>"
        f"<div style='text-align:center;'><div style='font-size:2rem;font-weight:800;color:#f59e0b;'>⭐ {stars:,}</div>"
        f"<div style='color:#94a3b8;font-size:0.85rem;'>Stars</div></div>"
        f"<div style='text-align:center;'><div style='font-size:2rem;font-weight:800;color:#22c55e;'>"
        f"{_bool_icon(data.get('is_official'))}</div>"
        f"<div style='color:#94a3b8;font-size:0.85rem;'>Official</div></div></div>"
        f"<div style='margin-top:12px;color:#94a3b8;font-size:0.85rem;'>"
        f"Last updated: {html.escape(str(data.get('last_updated', '?')))}</div>",
        "⭐",
    )


def _render_size(data: dict[str, Any]) -> str:
    total = data.get("total_compressed_human", "?")
    layers = data.get("layers", [])
    platforms = data.get("platforms")
    content = (
        f"<div style='font-size:2rem;font-weight:800;color:#818cf8;margin-bottom:12px;'>"
        f"{html.escape(str(total))}</div>"
        f"<div style='color:#94a3b8;font-size:0.85rem;margin-bottom:12px;'>"
        f"{data.get('layer_count', 0)} layer(s)"
        f"{' · multi-arch' if data.get('multi_arch') else ''}</div>"
    )
    if layers:
        rows = [[str(l["index"]), html.escape(l["size_human"])] for l in layers]
        content += _table(["Layer", "Size"], rows)
    if platforms:
        rows = [[html.escape(p["platform"]), html.escape(p["compressed_human"]), str(p["layer_count"])] for p in platforms]
        content += _table(["Platform", "Size", "Layers"], rows)
    return _section("Size", content, "📦")


def _render_license(data: dict[str, Any]) -> str:
    spdx = data.get("spdx_id")
    if not spdx:
        return _section("License", "<p style='color:#94a3b8;'>License not detected.</p>", "📜")
    url = data.get("license_url", "")
    link = f'<a href="{html.escape(url)}" style="color:#818cf8;">{html.escape(url)}</a>' if url else ""
    return _section(
        "License",
        f"{_badge('SPDX', spdx, '#22c55e')}"
        f"<div style='margin-top:8px;'>{link}</div>"
        f"<div style='margin-top:4px;color:#94a3b8;font-size:0.85rem;'>Source: {html.escape(str(data.get('detection_source', '?')))}</div>",
        "📜",
    )


def _render_freshness(data: dict[str, Any]) -> str:
    age = data.get("age_days")
    behind = data.get("behind_latest_days")
    is_latest = data.get("is_latest")
    color = "#22c55e" if (age is not None and age < 90) else "#f59e0b" if (age is not None and age < 365) else "#ef4444"
    age_str = f"{age} days" if age is not None else "unknown"
    return _section(
        "Freshness",
        f"<div style='display:flex;gap:24px;flex-wrap:wrap;'>"
        f"<div><div style='font-size:2rem;font-weight:800;color:{color};'>{age_str}</div>"
        f"<div style='color:#94a3b8;font-size:0.85rem;'>Image age</div></div>"
        f"<div><div style='font-size:2rem;font-weight:800;color:#818cf8;'>"
        f"{behind if behind is not None else '?'} days</div>"
        f"<div style='color:#94a3b8;font-size:0.85rem;'>Behind latest</div></div>"
        f"<div><div style='font-size:2rem;font-weight:800;'>{_bool_icon(is_latest)}</div>"
        f"<div style='color:#94a3b8;font-size:0.85rem;'>Is latest</div></div></div>",
        "🕐",
    )

def _render_trivy(data: dict[str, Any]) -> str:
    count = data.get("vulnerability_count", 0)
    targets = data.get("targets", [])
    trivy_version = data.get("trivy_version", "?")

    color = "#22c55e" if count == 0 else "#f59e0b" if count < 10 else "#ef4444"
    
    header = (
        f"<div style='margin-bottom:12px;display:flex;align-items:center;justify-content:space-between;'>"
        f"<div style='font-size:2rem;font-weight:800;color:{color};'>"
        f"{count} vulnerabilit{'y' if count == 1 else 'ies'}</div>"
        f"<div style='color:#94a3b8;font-size:0.85rem;'>Trivy v{html.escape(trivy_version)}</div></div>"
    )

    counts_html = (
        f"<div style='display:flex;gap:8px;margin-bottom:16px;'>"
        f"{_badge('Critical', str(data.get('critical_count', 0)), '#ef4444')}"
        f"{_badge('High', str(data.get('high_count', 0)), '#f97316')}"
        f"{_badge('Medium', str(data.get('medium_count', 0)), '#f59e0b')}"
        f"{_badge('Low', str(data.get('low_count', 0)), '#6366f1')}"
        f"{_badge('Unknown', str(data.get('unknown_count', 0)), '#6b7280')}</div>"
    )

    content = header + counts_html

    for target in targets:
        vulns = target.get("Vulnerabilities", [])
        if not vulns:
            continue
            
        target_name = html.escape(target.get("Target", "Unknown Target"))
        content += f"<h4 style='font-size:1rem;margin:12px 0 8px 0;color:#c084fc;'>{target_name}</h4>"
        
        rows = []
        for v in vulns[:10]:
            sev = html.escape(v.get("Severity", "UNKNOWN"))
            sev_color = "#ef4444" if sev == "CRITICAL" else "#f97316" if sev == "HIGH" else "#f59e0b" if sev == "MEDIUM" else "#6366f1" if sev == "LOW" else "#6b7280"
            rows.append([
                html.escape(v.get("VulnerabilityID", "")),
                html.escape(v.get("PkgName", "")),
                html.escape(v.get("InstalledVersion", "")),
                html.escape(v.get("FixedVersion", "")),
                f"<span style='color:{sev_color};font-weight:600;'>{sev}</span>",
            ])
        content += _table(["ID", "Package", "Installed", "Fixed", "Severity"], rows)
        if len(vulns) > 10:
             content += f"<p style='color:#94a3b8;margin-top:8px;'>… and {len(vulns) - 10} more in this target</p>"

    return _section("Trivy Scan", content, "🛡️")




def _render_provenance(data: dict[str, Any]) -> str:
    has = data.get("has_provenance")
    indicators = data.get("indicators", [])
    status_html = (
        f"{_badge('Provenance', 'Yes', '#22c55e')} "
        f"{_badge('Cosign', _bool_icon(data.get('has_cosign_signature')), '#818cf8')} "
        f"{_badge('Source tracked', _bool_icon(data.get('source_tracked')), '#818cf8')}"
    )
    rows = [[html.escape(i["type"]), html.escape(i["key"]), html.escape(i["value"][:80])] for i in indicators]
    table_html = _table(["Type", "Key", "Value"], rows) if rows else ""
    return _section("Provenance", f"{status_html}{table_html}", "🔏")


def _render_deps(data: dict[str, Any]) -> str:
    deps = data.get("dependencies", [])
    if not deps:
        return _section("Dependencies", "<p style='color:#94a3b8;'>No base image detected.</p>", "🔗")
    has_eol = data.get("has_eol_dependency")
    status = _badge("EOL dependency", "Yes", "#ef4444") if has_eol else _badge("All supported", "✓", "#22c55e")
    rows = []
    for d in deps:
        eol = d.get("eol_check", {})
        rows.append([
            html.escape(str(d.get("image", ""))),
            html.escape(str(d.get("tag", "") or "—")),
            html.escape(str(eol.get("product", ""))),
            _bool_icon(not eol.get("is_eol")) if eol.get("is_eol") is not None else "➖",
        ])
    return _section("Dependencies", f"{status}{_table(['Image', 'Tag', 'Product', 'Supported'], rows)}", "🔗")


_RENDERERS: dict[str, Any] = {
    "tags": _render_tags,
    "image": _render_image,
    "versioning": _render_versioning,
    "scorecard": _render_scorecard,
    "endoflife": _render_endoflife,
    "popularity": _render_popularity,
    "size": _render_size,
    "license": _render_license,
    "freshness": _render_freshness,
    "trivy": _render_trivy,

    "provenance": _render_provenance,
    "deps": _render_deps,
}

_LEVEL_STYLES = {
    "gold": ("🥇", "#f59e0b"),
    "silver": ("🥈", "#94a3b8"),
    "bronze": ("🥉", "#cd7f32"),
    "none": ("—", "#6b7280"),
}


def _render_scorecard_result(sc: dict[str, Any]) -> str:
    """Render the scorecard evaluation result."""
    level = sc.get("level", "none")
    icon, color = _LEVEL_STYLES.get(level, ("—", "#6b7280"))
    score_pct = sc.get("score", 0)
    passed = sc.get("passed_rules", 0)
    total = sc.get("total_rules", 0)

    # Level badge and progress bar.
    header = (
        f'<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;">'
        f'<div style="font-size:3rem;">{icon}</div>'
        f'<div>'
        f'<div style="font-size:1.5rem;font-weight:800;color:{color};'
        f'text-transform:uppercase;letter-spacing:0.1em;">{html.escape(level)}</div>'
        f'<div style="color:#94a3b8;font-size:0.85rem;">{passed}/{total} rules passed · {score_pct}%</div>'
        f'</div></div>'
        + _score_bar(score_pct, 100)
    )

    # Per-rule rows.
    rules = sc.get("rules", [])
    rows = []
    for r in rules:
        status = '✅' if r["passed"] else '❌'
        lvl = r.get("level", "")
        lvl_icon = _LEVEL_STYLES.get(lvl, ("", "#6b7280"))[0]
        rows.append([
            status,
            f'{lvl_icon} {html.escape(lvl)}',
            html.escape(r.get("title", r.get("name", ""))),
        ])

    return (
        f'<div style="background:linear-gradient(135deg,#1a1a2e,#16213e);'
        f'border-radius:12px;padding:20px;margin-bottom:20px;'
        f'border:1px solid {color}44;">'
        f'<h2 style="font-size:1.2rem;font-weight:700;margin-bottom:16px;">'
        f'📊 {html.escape(sc.get("scorecard_name", "Scorecard"))}</h2>'
        f'{header}'
        f'<div style="margin-top:16px;">{_table(["Status", "Level", "Rule"], rows)}</div>'
        f'</div>'
    )


def render_html(report: dict[str, Any]) -> str:
    """Render a full report dict as a standalone HTML page."""
    request = report.get("request", {})
    results = report.get("results", {})

    repo = html.escape(str(request.get("repository", "?")))
    tag = html.escape(str(request.get("tag", "?")))
    registry = html.escape(str(request.get("registry", "?")))
    timestamp = html.escape(str(request.get("timestamp", "?")))

    # Render scorecard result if present.
    scorecard_html = ""
    sc_data = report.get("scorecard")
    if sc_data:
        scorecard_html = _render_scorecard_result(sc_data)

    # Render each analyzer section.
    sections = ""
    for name in sorted(results):
        renderer = _RENDERERS.get(name)
        if renderer:
            sections += renderer(results[name])
        else:
            sections += _section(
                name,
                f'<pre style="background:#1e1e2e;padding:12px;border-radius:8px;overflow-x:auto;font-size:0.85rem;">'
                f'{html.escape(json.dumps(results[name], indent=2))}</pre>',
                "📋",
            )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>regis-cli Report — {repo}:{tag}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family:'Inter',system-ui,-apple-system,sans-serif;
    background:#0f0f1a;
    color:#e2e8f0;
    padding:24px;
    line-height:1.6;
  }}
  a {{ color:#818cf8; text-decoration:none; }}
  a:hover {{ text-decoration:underline; }}
  .container {{
    max-width:960px;
    margin:0 auto;
  }}
  .header {{
    background:linear-gradient(135deg,#1e1b4b,#312e81);
    border-radius:16px;
    padding:32px;
    margin-bottom:24px;
    border:1px solid #3730a3;
    box-shadow:0 4px 24px rgba(99,102,241,0.15);
  }}
  .header h1 {{
    font-size:1.8rem;
    font-weight:800;
    background:linear-gradient(90deg,#818cf8,#c084fc);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
  }}
  .header .meta {{
    margin-top:8px;
    color:#94a3b8;
    font-size:0.85rem;
  }}
  .card {{
    background:#16162a;
    border-radius:12px;
    padding:20px;
    margin-bottom:16px;
    border:1px solid #1e1e3a;
  }}
  details > summary::marker {{ color:#6366f1; }}
  table {{ font-variant-numeric:tabular-nums; }}
  pre {{ white-space:pre-wrap; word-break:break-word; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>{repo}:{tag}</h1>
    <div class="meta">
      Registry: {registry} · Generated: {timestamp}
    </div>
  </div>
  <div class="card">
    {scorecard_html}
    {sections}
  </div>
  <div style="text-align:center;color:#475569;font-size:0.8rem;padding:16px;">
    Generated by <strong>regis-cli</strong>
  </div>
</div>
</body>
</html>"""
