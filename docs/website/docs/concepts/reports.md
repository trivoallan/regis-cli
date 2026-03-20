---
tags:
  - reports
---

# Reports

One of the core missions of `regis-cli` is to bridge the gap between automated tools and human review through **Visual Excellence**.

## The Reporting Engine

`regis-cli` uses a powerful rendering engine based on **Jinja2** templates. This allows for:

- **Dynamic Content**: Injecting analysis results directly into interactive HTML.
- **Modular Layouts**: Reusing components like "Vulnerability Tables" or "Score Gauges" across different report types.
- **Multi-format Support**: While HTML is the flagship format, the engine can also produce Markdown for pull request comments or JSON for further processing.

## Philosophy: Visual Excellence

We believe that security reports should be easy to read and aesthetically pleasing. A well-designed report:

1. **Reduces Cognitive Load**: Highlighting the most important issues first.
2. **Encourages Adoption**: Teams are more likely to use tools that provide clear, professional feedback.
3. **Facilitates Decision Making**: Using color coding and clear typography to distinguish between risks.

## Customization

Users can provide their own Jinja2 templates or CSS overrides to match their company's branding or specific reporting requirements.

```bash
regis analyze --template ./my-custom-report.html.j2
```

> [!TIP]
> Check our [Usage Guide](../usage/configuration.md) to learn how to set default themes for your project.
