"use strict";
(globalThis.webpackChunk_regis_cli_report_viewer =
  globalThis.webpackChunk_regis_cli_report_viewer || []).push([
  [7994],
  {
    7557(e, s, r) {
      (r.r(s),
        r.d(s, {
          assets: () => H,
          contentTitle: () => V,
          default: () => E,
          frontMatter: () => U,
          metadata: () => a,
          toc: () => K,
        }));
      const a = JSON.parse(
        '{"id":"playbook","title":"Playbook","description":"","source":"@site/docs/playbook.mdx","sourceDirName":".","slug":"/playbook","permalink":"/playbook","draft":false,"unlisted":false,"tags":[],"version":"current","frontMatter":{"title":"Playbook"},"sidebar":"defaultSidebar","previous":{"title":"Rules","permalink":"/rules"}}',
      );
      var t = r(6730),
        l = r(6451),
        i = (r(162), r(1450));
      function n({ value: e }) {
        return !0 === e
          ? (0, t.jsx)("span", { children: "\u2705" })
          : !1 === e
            ? (0, t.jsx)("span", { children: "\u274c" })
            : null == e
              ? (0, t.jsx)("span", { style: { opacity: 0.5 }, children: "N/A" })
              : (0, t.jsx)("span", { children: String(e) });
      }
      function d({ widgets: e }) {
        return (0, t.jsx)("div", {
          style: {
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(min(100%, 250px), 1fr))",
            gap: "0.75rem",
            marginBottom: "1.5rem",
          },
          children: e.map((e, s) => {
            const r = (0, t.jsxs)("div", {
              style: {
                padding: "1rem",
                background: "var(--ifm-card-background-color)",
                borderRadius: "8px",
                border: "1px solid var(--ifm-color-emphasis-200)",
                textAlign: e.options?.align ?? "left",
                height: "100%",
              },
              children: [
                e.options?.title &&
                  (0, t.jsx)("h6", {
                    style: {
                      marginBottom: "0.5rem",
                      color: "var(--ifm-color-primary)",
                      fontSize: "0.85rem",
                    },
                    children: String(e.options.title),
                  }),
                e.icon &&
                  (0, t.jsx)("span", {
                    style: { fontSize: "1.5rem" },
                    children: e.icon,
                  }),
                (0, t.jsx)("strong", {
                  style: {
                    fontSize: "0.8rem",
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                    opacity: 0.8,
                    display: "block",
                  },
                  children: e.label,
                }),
                (0, t.jsx)("span", {
                  style: {
                    fontSize: "1.8rem",
                    fontWeight: 700,
                    lineHeight: 1,
                    display: "block",
                    marginTop: "0.25rem",
                  },
                  children: (0, t.jsx)(n, { value: e.resolved_value }),
                }),
                e.resolved_subvalue &&
                  (0, t.jsx)("small", {
                    style: { opacity: 0.7, fontSize: "0.85rem" },
                    children: e.resolved_subvalue,
                  }),
              ],
            });
            return e.resolved_url
              ? (0, t.jsx)(
                  "a",
                  {
                    href: e.resolved_url,
                    style: { textDecoration: "none", color: "inherit" },
                    target: "_blank",
                    rel: "noopener noreferrer",
                    children: r,
                  },
                  s,
                )
              : (0, t.jsx)("div", { children: r }, s);
          }),
        });
      }
      const c = {
        bronze: "\ud83e\udd49",
        silver: "\ud83e\udd48",
        gold: "\ud83e\udd47",
        none: "\u2b55",
      };
      function o({ levels: e }) {
        return (0, t.jsx)("div", {
          style: {
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))",
            gap: "0.75rem",
            marginBottom: "1.5rem",
          },
          children: Object.entries(e).map(([e, s]) =>
            (0, t.jsxs)(
              "div",
              {
                style: {
                  textAlign: "center",
                  padding: "0.75rem",
                  background: "var(--ifm-card-background-color)",
                  borderRadius: "8px",
                  border: "1px solid var(--ifm-color-emphasis-200)",
                },
                children: [
                  (0, t.jsxs)("strong", {
                    style: {
                      fontSize: "0.75rem",
                      textTransform: "uppercase",
                      letterSpacing: "0.05em",
                      opacity: 0.8,
                    },
                    children: [c[e] ?? "", " ", e],
                  }),
                  (0, t.jsx)("br", {}),
                  (0, t.jsxs)("span", {
                    style: {
                      fontSize: "1.6rem",
                      fontWeight: 700,
                      lineHeight: 1.2,
                    },
                    children: [
                      s.passed,
                      (0, t.jsxs)("small", {
                        style: { fontSize: "0.9rem", opacity: 0.5 },
                        children: ["/", s.total],
                      }),
                    ],
                  }),
                  (0, t.jsxs)("div", {
                    style: {
                      fontSize: "0.75rem",
                      marginTop: "0.2rem",
                      opacity: 0.6,
                    },
                    children: [s.percentage, "% pass"],
                  }),
                ],
              },
              e,
            ),
          ),
        });
      }
      var h = r(1664);
      function m({ scorecards: e, showLevels: s = !0 }) {
        return (0, t.jsx)("div", {
          style: { overflowX: "auto" },
          children: (0, t.jsxs)("table", {
            children: [
              (0, t.jsx)("thead", {
                children: (0, t.jsxs)("tr", {
                  children: [
                    (0, t.jsx)("th", { children: "Status" }),
                    s && (0, t.jsx)("th", { children: "Level" }),
                    (0, t.jsx)("th", { children: "Scorecard" }),
                    (0, t.jsx)("th", { children: "Analyzers" }),
                  ],
                }),
              }),
              (0, t.jsx)("tbody", {
                children: e.map((e, r) =>
                  (0, t.jsxs)(
                    "tr",
                    {
                      children: [
                        (0, t.jsx)("td", {
                          style: { textAlign: "center" },
                          children: e.passed
                            ? (0, t.jsx)("span", {
                                title: "Passed",
                                children: "\u2705",
                              })
                            : (0, t.jsx)("span", {
                                title: "Failed",
                                children: "\u274c",
                              }),
                        }),
                        s &&
                          (0, t.jsx)("td", {
                            children: (0, t.jsx)(h.M, {
                              label: e.level ?? "info",
                              variant: (0, h.Z)(e.level ?? "info"),
                            }),
                          }),
                        (0, t.jsxs)("td", {
                          children: [
                            (0, t.jsx)("strong", { children: e.title }),
                            e.tags &&
                              e.tags.length > 0 &&
                              (0, t.jsx)("div", {
                                style: {
                                  marginTop: "0.2rem",
                                  display: "flex",
                                  gap: "0.25rem",
                                  flexWrap: "wrap",
                                },
                                children: e.tags.map((e) =>
                                  (0, t.jsx)(h.M, { label: e }, e),
                                ),
                              }),
                            e.details &&
                              (0, t.jsx)("div", {
                                style: {
                                  fontSize: "0.8rem",
                                  opacity: 0.7,
                                  marginTop: "0.3rem",
                                },
                                children: e.details,
                              }),
                          ],
                        }),
                        (0, t.jsx)("td", {
                          children: (0, t.jsx)("div", {
                            style: {
                              display: "flex",
                              gap: "0.25rem",
                              flexWrap: "wrap",
                            },
                            children: e.analyzers?.map((e) =>
                              (0, t.jsx)(
                                h.M,
                                { label: e, variant: "outline" },
                                e,
                              ),
                            ),
                          }),
                        }),
                      ],
                    },
                    r,
                  ),
                ),
              }),
            ],
          }),
        });
      }
      var x = r(4390);
      const p = {
        CRITICAL: "#dc2626",
        HIGH: "#ea580c",
        MEDIUM: "#d97706",
        LOW: "#2563eb",
        UNKNOWN: "#6b7280",
      };
      function j({ data: e }) {
        const s = e.vulnerability_count || 1,
          r = [
            { label: "Critical", count: e.critical_count, color: p.CRITICAL },
            { label: "High", count: e.high_count, color: p.HIGH },
            { label: "Medium", count: e.medium_count, color: p.MEDIUM },
            { label: "Low", count: e.low_count, color: p.LOW },
            { label: "Unknown", count: e.unknown_count, color: p.UNKNOWN },
          ].filter((e) => e.count > 0);
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsx)("div", {
              style: {
                display: "flex",
                height: "12px",
                borderRadius: "6px",
                overflow: "hidden",
                marginBottom: "0.5rem",
                background: "var(--ifm-color-emphasis-200)",
              },
              children: r.map((e) =>
                (0, t.jsx)(
                  "div",
                  {
                    style: {
                      width: (e.count / s) * 100 + "%",
                      background: e.color,
                      minWidth: e.count > 0 ? "4px" : 0,
                    },
                    title: `${e.label}: ${e.count}`,
                  },
                  e.label,
                ),
              ),
            }),
            (0, t.jsx)("div", {
              style: {
                display: "flex",
                gap: "1rem",
                flexWrap: "wrap",
                fontSize: "0.8rem",
              },
              children: r.map((e) =>
                (0, t.jsxs)(
                  "span",
                  {
                    style: {
                      display: "flex",
                      alignItems: "center",
                      gap: "4px",
                    },
                    children: [
                      (0, t.jsx)("span", {
                        style: {
                          width: "10px",
                          height: "10px",
                          borderRadius: "2px",
                          background: e.color,
                          display: "inline-block",
                        },
                      }),
                      e.label,
                      ": ",
                      (0, t.jsx)("strong", { children: e.count }),
                    ],
                  },
                  e.label,
                ),
              ),
            }),
          ],
        });
      }
      function u({ data: e }) {
        const s =
          e.targets?.flatMap(
            (e) =>
              e.Vulnerabilities?.map((s) => ({ ...s, target: e.Target })) ?? [],
          ) ?? [];
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsxs)("div", {
              style: {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                gap: "0.75rem",
                marginBottom: "1.5rem",
              },
              children: [
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Total",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.vulnerability_count,
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Fixable",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.fixed_count,
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Secrets",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.secrets_count,
                    }),
                  ],
                }),
              ],
            }),
            (0, t.jsx)(j, { data: e }),
            s.length > 0 &&
              (0, t.jsxs)("table", {
                style: { marginTop: "1rem" },
                children: [
                  (0, t.jsx)("thead", {
                    children: (0, t.jsxs)("tr", {
                      children: [
                        (0, t.jsx)("th", { children: "ID" }),
                        (0, t.jsx)("th", { children: "Severity" }),
                        (0, t.jsx)("th", { children: "Package" }),
                        (0, t.jsx)("th", { children: "Installed" }),
                        (0, t.jsx)("th", { children: "Fixed" }),
                        (0, t.jsx)("th", { children: "Title" }),
                      ],
                    }),
                  }),
                  (0, t.jsx)("tbody", {
                    children: s.map((e, s) =>
                      (0, t.jsxs)(
                        "tr",
                        {
                          children: [
                            (0, t.jsx)("td", {
                              children: (0, t.jsx)("a", {
                                href: `https://nvd.nist.gov/vuln/detail/${e.VulnerabilityID}`,
                                target: "_blank",
                                rel: "noopener noreferrer",
                                style: {
                                  fontFamily: "monospace",
                                  fontSize: "0.85rem",
                                },
                                children: e.VulnerabilityID,
                              }),
                            }),
                            (0, t.jsx)("td", {
                              children: (0, t.jsx)("span", {
                                style: {
                                  padding: "2px 8px",
                                  borderRadius: "4px",
                                  fontSize: "0.75rem",
                                  fontWeight: 700,
                                  color: "#fff",
                                  background: p[e.Severity] ?? "#6b7280",
                                },
                                children: e.Severity,
                              }),
                            }),
                            (0, t.jsx)("td", {
                              style: {
                                fontFamily: "monospace",
                                fontSize: "0.85rem",
                              },
                              children: e.PkgName,
                            }),
                            (0, t.jsx)("td", {
                              style: {
                                fontFamily: "monospace",
                                fontSize: "0.85rem",
                              },
                              children: e.InstalledVersion,
                            }),
                            (0, t.jsx)("td", {
                              style: {
                                fontFamily: "monospace",
                                fontSize: "0.85rem",
                              },
                              children: e.FixedVersion ?? "\u2014",
                            }),
                            (0, t.jsx)("td", {
                              style: { fontSize: "0.85rem" },
                              children: e.Title ?? "",
                            }),
                          ],
                        },
                        s,
                      ),
                    ),
                  }),
                ],
              }),
            0 === s.length &&
              0 === e.vulnerability_count &&
              (0, t.jsx)("div", {
                className: "alert alert--success",
                style: { marginTop: "1rem" },
                children: "\u2705 No vulnerabilities detected.",
              }),
          ],
        });
      }
      function v({ days: e }) {
        let s = "#22c55e",
          r = "Fresh";
        return (
          e > 180
            ? ((s = "#dc2626"), (r = "Stale"))
            : e > 90
              ? ((s = "#d97706"), (r = "Aging"))
              : e > 30 && ((s = "#2563eb"), (r = "OK")),
          (0, t.jsx)("span", {
            style: {
              padding: "3px 10px",
              borderRadius: "12px",
              fontSize: "0.75rem",
              fontWeight: 700,
              color: "#fff",
              background: s,
            },
            children: r,
          })
        );
      }
      function g({ data: e }) {
        return (0, t.jsxs)("div", {
          style: {
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
            gap: "0.75rem",
          },
          children: [
            (0, t.jsxs)("div", {
              className: "stat-card",
              children: [
                (0, t.jsx)("div", {
                  className: "stat-card__label",
                  children: "Image Age",
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card__value",
                  children: [
                    e.age_days ?? "?",
                    " ",
                    (0, t.jsx)("span", {
                      style: { fontSize: "0.7em", opacity: 0.6 },
                      children: "days",
                    }),
                  ],
                }),
                void 0 !== e.age_days &&
                  (0, t.jsx)("div", {
                    style: { marginTop: "0.25rem" },
                    children: (0, t.jsx)(v, { days: e.age_days }),
                  }),
              ],
            }),
            (0, t.jsxs)("div", {
              className: "stat-card",
              children: [
                (0, t.jsx)("div", {
                  className: "stat-card__label",
                  children: "Is Latest",
                }),
                (0, t.jsx)("div", {
                  className: "stat-card__value",
                  children: e.is_latest ? "\u2705 Yes" : "\u274c No",
                }),
              ],
            }),
            (0, t.jsxs)("div", {
              className: "stat-card",
              children: [
                (0, t.jsx)("div", {
                  className: "stat-card__label",
                  children: "Behind Latest",
                }),
                (0, t.jsx)("div", {
                  className: "stat-card__value",
                  children:
                    null != e.behind_latest_days
                      ? `${e.behind_latest_days} days`
                      : "N/A",
                }),
              ],
            }),
            (0, t.jsxs)("div", {
              className: "stat-card",
              children: [
                (0, t.jsx)("div", {
                  className: "stat-card__label",
                  children: "Created",
                }),
                (0, t.jsx)("div", {
                  className: "stat-card__value",
                  style: { fontSize: "0.85rem" },
                  children: e.tag_created
                    ? new Date(e.tag_created).toLocaleDateString()
                    : "N/A",
                }),
              ],
            }),
          ],
        });
      }
      function y({ data: e }) {
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsxs)("div", {
              style: {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                gap: "0.75rem",
                marginBottom: "1rem",
              },
              children: [
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Compressed Size",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.total_compressed_human,
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Layers",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.layer_count,
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Multi-arch",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.multi_arch ? "\u2705 Yes" : "No",
                    }),
                  ],
                }),
              ],
            }),
            e.platforms &&
              e.platforms.length > 0 &&
              (0, t.jsxs)("div", {
                children: [
                  (0, t.jsx)("h5", { children: "Platform Breakdown" }),
                  (0, t.jsxs)("table", {
                    children: [
                      (0, t.jsx)("thead", {
                        children: (0, t.jsxs)("tr", {
                          children: [
                            (0, t.jsx)("th", { children: "Platform" }),
                            (0, t.jsx)("th", { children: "Size" }),
                            (0, t.jsx)("th", { children: "Layers" }),
                          ],
                        }),
                      }),
                      (0, t.jsx)("tbody", {
                        children: e.platforms.map((e, s) =>
                          (0, t.jsxs)(
                            "tr",
                            {
                              children: [
                                (0, t.jsx)("td", {
                                  children: (0, t.jsx)("code", {
                                    children: e.platform,
                                  }),
                                }),
                                (0, t.jsx)("td", {
                                  children: e.compressed_human,
                                }),
                                (0, t.jsx)("td", { children: e.layer_count }),
                              ],
                            },
                            s,
                          ),
                        ),
                      }),
                    ],
                  }),
                ],
              }),
          ],
        });
      }
      const f = {
        error: "#dc2626",
        warning: "#d97706",
        info: "#2563eb",
        style: "#6b7280",
      };
      function _({ data: e }) {
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsxs)("div", {
              style: {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                gap: "0.75rem",
                marginBottom: "1rem",
              },
              children: [
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Status",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.passed
                        ? "\u2705 Passed"
                        : "\u26a0\ufe0f Issues",
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Issues",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.issues_count,
                    }),
                  ],
                }),
                e.issues_by_level &&
                  Object.entries(e.issues_by_level)
                    .filter(([, e]) => e > 0)
                    .map(([e, s]) =>
                      (0, t.jsxs)(
                        "div",
                        {
                          className: "stat-card",
                          children: [
                            (0, t.jsx)("div", {
                              className: "stat-card__label",
                              children: e,
                            }),
                            (0, t.jsx)("div", {
                              className: "stat-card__value",
                              style: { color: f[e] ?? "inherit" },
                              children: s,
                            }),
                          ],
                        },
                        e,
                      ),
                    ),
              ],
            }),
            e.issues &&
              e.issues.length > 0 &&
              (0, t.jsxs)("table", {
                children: [
                  (0, t.jsx)("thead", {
                    children: (0, t.jsxs)("tr", {
                      children: [
                        (0, t.jsx)("th", { children: "Code" }),
                        (0, t.jsx)("th", { children: "Level" }),
                        (0, t.jsx)("th", { children: "Line" }),
                        (0, t.jsx)("th", { children: "Message" }),
                      ],
                    }),
                  }),
                  (0, t.jsx)("tbody", {
                    children: e.issues.map((e, s) =>
                      (0, t.jsxs)(
                        "tr",
                        {
                          children: [
                            (0, t.jsx)("td", {
                              children: (0, t.jsx)("a", {
                                href: `https://github.com/hadolint/hadolint/wiki/${e.code}`,
                                target: "_blank",
                                rel: "noopener noreferrer",
                                style: { fontFamily: "monospace" },
                                children: e.code,
                              }),
                            }),
                            (0, t.jsx)("td", {
                              children: (0, t.jsx)("span", {
                                style: {
                                  padding: "2px 8px",
                                  borderRadius: "4px",
                                  fontSize: "0.75rem",
                                  fontWeight: 700,
                                  color: "#fff",
                                  background: f[e.level] ?? "#6b7280",
                                },
                                children: e.level,
                              }),
                            }),
                            (0, t.jsx)("td", {
                              style: { fontFamily: "monospace" },
                              children: e.line ?? "\u2014",
                            }),
                            (0, t.jsx)("td", {
                              style: { fontSize: "0.85rem" },
                              children: e.message,
                            }),
                          ],
                        },
                        s,
                      ),
                    ),
                  }),
                ],
              }),
          ],
        });
      }
      function b(e) {
        return void 0 === e
          ? "N/A"
          : e >= 1e6
            ? (e / 1e6).toFixed(1) + "M"
            : e >= 1e3
              ? (e / 1e3).toFixed(1) + "K"
              : e.toString();
      }
      function N({ data: e }) {
        return e.available
          ? (0, t.jsxs)("div", {
              children: [
                (0, t.jsxs)("div", {
                  style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                    gap: "0.75rem",
                    marginBottom: "1rem",
                  },
                  children: [
                    (0, t.jsxs)("div", {
                      className: "stat-card",
                      children: [
                        (0, t.jsx)("div", {
                          className: "stat-card__label",
                          children: "Pulls",
                        }),
                        (0, t.jsx)("div", {
                          className: "stat-card__value",
                          children: b(e.pull_count),
                        }),
                      ],
                    }),
                    (0, t.jsxs)("div", {
                      className: "stat-card",
                      children: [
                        (0, t.jsx)("div", {
                          className: "stat-card__label",
                          children: "Stars",
                        }),
                        (0, t.jsx)("div", {
                          className: "stat-card__value",
                          children: b(e.star_count),
                        }),
                      ],
                    }),
                  ],
                }),
                e.description &&
                  (0, t.jsxs)("div", {
                    style: {
                      marginTop: "1rem",
                      fontSize: "0.9rem",
                      color: "var(--ifm-color-emphasis-700)",
                    },
                    children: [
                      (0, t.jsx)("strong", { children: "Description:" }),
                      " ",
                      e.description,
                    ],
                  }),
                (0, t.jsxs)("div", {
                  style: {
                    marginTop: "0.5rem",
                    fontSize: "0.8rem",
                    opacity: 0.6,
                  },
                  children: [
                    e.last_updated &&
                      `Last Updated: ${new Date(e.last_updated).toLocaleDateString()}`,
                    e.date_registered &&
                      ` | Registered: ${new Date(e.date_registered).toLocaleDateString()}`,
                  ],
                }),
              ],
            })
          : (0, t.jsx)("div", {
              className: "alert alert--info",
              children:
                "Popularity metrics not available for this registry/repository.",
            });
      }
      function S({ data: e }) {
        if (!e.product_found)
          return (0, t.jsxs)("div", {
            className: "alert alert--warning",
            children: [
              "Product ",
              (0, t.jsx)("strong", { children: e.product }),
              " not found in endoflife.date database.",
            ],
          });
        const s = e.is_eol,
          r = s ? "#dc2626" : !1 === s ? "#22c55e" : "#6b7280",
          a = s ? "End of Life" : !1 === s ? "Supported" : "Unknown Status";
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsxs)("div", {
              style: {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                gap: "0.75rem",
                marginBottom: "1rem",
              },
              children: [
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Product",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      style: { textTransform: "capitalize" },
                      children: e.product,
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Cycle",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.matched_cycle || "N/A",
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Status",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      style: {
                        color: r,
                        fontSize: "1.2rem",
                        paddingTop: "0.5rem",
                      },
                      children: a,
                    }),
                  ],
                }),
              ],
            }),
            (0, t.jsxs)("div", {
              className: "alert alert--secondary",
              children: [
                "This product has ",
                (0, t.jsx)("strong", { children: e.active_cycles_count }),
                " active cycles and ",
                (0, t.jsx)("strong", { children: e.eol_cycles_count }),
                " cycles that have reached end-of-life.",
              ],
            }),
          ],
        });
      }
      const k = {
          success: "\u2705",
          failure: "\u274c",
          warning: "\u26a0\ufe0f",
        },
        z = {
          success: "alert--success",
          failure: "alert--danger",
          warning: "alert--warning",
        };
      function T({ data: e }) {
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsxs)("div", {
              style: {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                gap: "0.75rem",
                marginBottom: "1.5rem",
              },
              children: [
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "SLSA Provenance",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.has_provenance
                        ? "\u2705 Found"
                        : "\u274c Missing",
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Cosign Signature",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.has_cosign_signature
                        ? "\u2705 Signed"
                        : "\u274c No",
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Source Tracked",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.source_tracked ? "\u2705 Yes" : "\u274c No",
                    }),
                  ],
                }),
              ],
            }),
            e.indicators &&
              e.indicators.length > 0 &&
              (0, t.jsx)("div", {
                style: {
                  display: "flex",
                  flexDirection: "column",
                  gap: "0.5rem",
                },
                children: e.indicators.map((e, s) =>
                  (0, t.jsxs)(
                    "div",
                    {
                      className: `alert ${z[e.status]}`,
                      style: { padding: "0.5rem 1rem" },
                      children: [
                        (0, t.jsxs)("strong", {
                          children: [k[e.status], " ", e.name],
                        }),
                        ": ",
                        e.message,
                      ],
                    },
                    s,
                  ),
                ),
              }),
          ],
        });
      }
      function w(e) {
        return e >= 8 ? "#22c55e" : e >= 5 ? "#d97706" : "#dc2626";
      }
      function C({ data: e }) {
        return e.scorecard_available
          ? (0, t.jsxs)("div", {
              children: [
                (0, t.jsxs)("div", {
                  style: {
                    display: "flex",
                    alignItems: "center",
                    gap: "2rem",
                    marginBottom: "1.5rem",
                  },
                  children: [
                    (0, t.jsx)("div", {
                      className: "score-circle",
                      style: {
                        background: w(e.score ?? 0),
                        width: "100px",
                        height: "100px",
                        fontSize: "2rem",
                      },
                      children: e.score?.toFixed(1) ?? "N/A",
                    }),
                    (0, t.jsxs)("div", {
                      children: [
                        (0, t.jsx)("h3", {
                          style: { margin: 0 },
                          children: "OpenSSF Scorecard",
                        }),
                        (0, t.jsxs)("p", {
                          style: { opacity: 0.6, margin: 0 },
                          children: [
                            "Source:",
                            " ",
                            (0, t.jsx)("a", {
                              href: e.source_repo,
                              target: "_blank",
                              rel: "noopener noreferrer",
                              children: e.source_repo,
                            }),
                          ],
                        }),
                      ],
                    }),
                  ],
                }),
                e.checks &&
                  e.checks.length > 0 &&
                  (0, t.jsxs)("table", {
                    children: [
                      (0, t.jsx)("thead", {
                        children: (0, t.jsxs)("tr", {
                          children: [
                            (0, t.jsx)("th", { children: "Check" }),
                            (0, t.jsx)("th", { children: "Score" }),
                            (0, t.jsx)("th", { children: "Reason" }),
                          ],
                        }),
                      }),
                      (0, t.jsx)("tbody", {
                        children: [...e.checks]
                          .sort((e, s) => e.score - s.score)
                          .map((e, s) =>
                            (0, t.jsxs)(
                              "tr",
                              {
                                children: [
                                  (0, t.jsx)("td", {
                                    style: { fontWeight: 600 },
                                    children: e.name,
                                  }),
                                  (0, t.jsx)("td", {
                                    children: (0, t.jsx)("span", {
                                      style: {
                                        color: w(e.score),
                                        fontWeight: 700,
                                        fontSize: "1.1rem",
                                      },
                                      children:
                                        -1 === e.score ? "N/A" : e.score,
                                    }),
                                  }),
                                  (0, t.jsx)("td", {
                                    style: { fontSize: "0.85rem" },
                                    children: e.reason,
                                  }),
                                ],
                              },
                              s,
                            ),
                          ),
                      }),
                    ],
                  }),
              ],
            })
          : (0, t.jsx)("div", {
              className: "alert alert--info",
              children:
                "OpenSSF Scorecard results not available for this repository.",
            });
      }
      function A({ data: e }) {
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsxs)("div", {
              style: {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                gap: "0.75rem",
                marginBottom: "1.5rem",
              },
              children: [
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Total Tags",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.total_tags,
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "SemVer Compliance",
                    }),
                    (0, t.jsxs)("div", {
                      className: "stat-card__value",
                      children: [
                        e.semver_compliant_percentage?.toFixed(1),
                        "%",
                      ],
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Dominant Pattern",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      style: {
                        fontSize: "1rem",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                      },
                      children: (0, t.jsx)("code", {
                        children: e.dominant_pattern || "N/A",
                      }),
                    }),
                  ],
                }),
              ],
            }),
            (0, t.jsxs)("div", {
              style: {
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "2rem",
              },
              children: [
                e.patterns &&
                  (0, t.jsxs)("div", {
                    children: [
                      (0, t.jsx)("h5", { children: "Tag Patterns" }),
                      (0, t.jsx)("ul", {
                        style: { fontSize: "0.9rem" },
                        children: e.patterns.map((e) =>
                          (0, t.jsxs)(
                            "li",
                            {
                              children: [
                                (0, t.jsx)("code", { children: e.pattern }),
                                ": ",
                                (0, t.jsx)("strong", { children: e.count }),
                                " ",
                                (0, t.jsxs)("span", {
                                  style: { opacity: 0.5 },
                                  children: [
                                    "(",
                                    e.percentage.toFixed(1),
                                    "%)",
                                  ],
                                }),
                              ],
                            },
                            e.pattern,
                          ),
                        ),
                      }),
                    ],
                  }),
                e.variants &&
                  e.variants.length > 0 &&
                  (0, t.jsxs)("div", {
                    children: [
                      (0, t.jsx)("h5", { children: "Detected Variants" }),
                      (0, t.jsx)("div", {
                        style: {
                          display: "flex",
                          flexWrap: "wrap",
                          gap: "0.4rem",
                        },
                        children: e.variants.map((e) =>
                          (0, t.jsx)(
                            "span",
                            {
                              style: {
                                padding: "2px 8px",
                                background: "var(--ifm-color-emphasis-200)",
                                borderRadius: "4px",
                                fontSize: "0.8rem",
                              },
                              children: e,
                            },
                            e,
                          ),
                        ),
                      }),
                    ],
                  }),
              ],
            }),
          ],
        });
      }
      function L({ data: e }) {
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsx)("div", {
              style: {
                display: "flex",
                flexWrap: "wrap",
                gap: "1rem",
                marginBottom: "1.5rem",
              },
              children: e.platforms.map((e, s) =>
                (0, t.jsxs)(
                  "div",
                  {
                    className: "stat-card",
                    style: { flex: "1 1 300px", textAlign: "left" },
                    children: [
                      (0, t.jsxs)("div", {
                        className: "stat-card__label",
                        children: [
                          "Platform: ",
                          e.os,
                          "/",
                          e.architecture,
                          " ",
                          e.variant ? `(${e.variant})` : "",
                        ],
                      }),
                      (0, t.jsxs)("div", {
                        style: {
                          display: "grid",
                          gridTemplateColumns: "1fr 1fr",
                          gap: "0.5rem",
                          marginTop: "0.5rem",
                          fontSize: "0.9rem",
                        },
                        children: [
                          (0, t.jsxs)("div", {
                            children: [
                              (0, t.jsx)("strong", { children: "User:" }),
                              " ",
                              (0, t.jsx)("code", {
                                children: e.user || "root (default)",
                              }),
                            ],
                          }),
                          (0, t.jsxs)("div", {
                            children: [
                              (0, t.jsx)("strong", { children: "Layers:" }),
                              " ",
                              e.layers_count,
                            ],
                          }),
                          (0, t.jsxs)("div", {
                            children: [
                              (0, t.jsx)("strong", { children: "Size:" }),
                              " ",
                              (e.size / 1024 / 1024).toFixed(1),
                              " MB",
                            ],
                          }),
                        ],
                      }),
                      e.exposed_ports &&
                        e.exposed_ports.length > 0 &&
                        (0, t.jsxs)("div", {
                          style: { marginTop: "0.5rem", fontSize: "0.85rem" },
                          children: [
                            (0, t.jsx)("strong", {
                              children: "Exposed Ports:",
                            }),
                            (0, t.jsx)("div", {
                              style: {
                                display: "flex",
                                gap: "0.4rem",
                                flexWrap: "wrap",
                                marginTop: "0.2rem",
                              },
                              children: e.exposed_ports.map((e) =>
                                (0, t.jsx)(
                                  "span",
                                  {
                                    style: {
                                      padding: "1px 6px",
                                      background:
                                        "var(--ifm-color-primary-lightest)",
                                      color: "var(--ifm-color-primary-darkest)",
                                      borderRadius: "4px",
                                      fontSize: "0.75rem",
                                    },
                                    children: e,
                                  },
                                  e,
                                ),
                              ),
                            }),
                          ],
                        }),
                      e.labels &&
                        Object.keys(e.labels).length > 0 &&
                        (0, t.jsxs)("details", {
                          style: { marginTop: "0.5rem", fontSize: "0.8rem" },
                          children: [
                            (0, t.jsxs)("summary", {
                              style: { cursor: "pointer", opacity: 0.7 },
                              children: [
                                "Labels (",
                                Object.keys(e.labels).length,
                                ")",
                              ],
                            }),
                            (0, t.jsx)("div", {
                              style: {
                                padding: "0.5rem",
                                background: "var(--ifm-color-emphasis-100)",
                                borderRadius: "4px",
                                marginTop: "0.2rem",
                                maxHeight: "150px",
                                overflowY: "auto",
                              },
                              children: Object.entries(e.labels).map(([e, s]) =>
                                (0, t.jsxs)(
                                  "div",
                                  {
                                    style: {
                                      marginBottom: "2px",
                                      wordBreak: "break-all",
                                    },
                                    children: [
                                      (0, t.jsxs)("strong", {
                                        style: { opacity: 0.8 },
                                        children: [e, ":"],
                                      }),
                                      " ",
                                      s,
                                    ],
                                  },
                                  e,
                                ),
                              ),
                            }),
                          ],
                        }),
                      (0, t.jsxs)("div", {
                        style: {
                          marginTop: "0.5rem",
                          fontSize: "0.75rem",
                          opacity: 0.5,
                          wordBreak: "break-all",
                        },
                        children: [
                          "Digest: ",
                          (0, t.jsx)("code", { children: e.digest }),
                        ],
                      }),
                    ],
                  },
                  s,
                ),
              ),
            }),
            e.tags &&
              e.tags.length > 0 &&
              (0, t.jsxs)("details", {
                children: [
                  (0, t.jsxs)("summary", {
                    style: { cursor: "pointer", fontWeight: 600 },
                    children: ["Available Tags (", e.tags.length, ")"],
                  }),
                  (0, t.jsxs)("div", {
                    style: {
                      display: "flex",
                      flexWrap: "wrap",
                      gap: "0.4rem",
                      padding: "1rem 0",
                    },
                    children: [
                      e.tags.slice(0, 50).map((e) =>
                        (0, t.jsx)(
                          "span",
                          {
                            style: {
                              padding: "2px 8px",
                              background: "var(--ifm-color-emphasis-200)",
                              borderRadius: "4px",
                              fontSize: "0.8rem",
                            },
                            children: e,
                          },
                          e,
                        ),
                      ),
                      e.tags.length > 50 &&
                        (0, t.jsxs)("span", {
                          style: { opacity: 0.5 },
                          children: ["... and ", e.tags.length - 50, " more"],
                        }),
                    ],
                  }),
                ],
              }),
          ],
        });
      }
      function F({ data: e }) {
        return e.has_sbom
          ? (0, t.jsxs)("div", {
              children: [
                (0, t.jsxs)("div", {
                  style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                    gap: "0.75rem",
                    marginBottom: "1.5rem",
                  },
                  children: [
                    (0, t.jsxs)("div", {
                      className: "stat-card",
                      children: [
                        (0, t.jsx)("div", {
                          className: "stat-card__label",
                          children: "Total Components",
                        }),
                        (0, t.jsx)("div", {
                          className: "stat-card__value",
                          children: e.total_components,
                        }),
                      ],
                    }),
                    (0, t.jsxs)("div", {
                      className: "stat-card",
                      children: [
                        (0, t.jsx)("div", {
                          className: "stat-card__label",
                          children: "Unique Licenses",
                        }),
                        (0, t.jsx)("div", {
                          className: "stat-card__value",
                          children: e.licenses.length,
                        }),
                      ],
                    }),
                    (0, t.jsxs)("div", {
                      className: "stat-card",
                      children: [
                        (0, t.jsx)("div", {
                          className: "stat-card__label",
                          children: "Format",
                        }),
                        (0, t.jsxs)("div", {
                          className: "stat-card__value",
                          style: { fontSize: "1.2rem", paddingTop: "0.5rem" },
                          children: [e.sbom_format, " ", e.sbom_version],
                        }),
                      ],
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  style: {
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "2rem",
                    marginBottom: "1.5rem",
                  },
                  children: [
                    e.component_types &&
                      (0, t.jsxs)("div", {
                        children: [
                          (0, t.jsx)("h5", { children: "Component Types" }),
                          (0, t.jsx)("ul", {
                            style: { fontSize: "0.9rem" },
                            children: Object.entries(e.component_types).map(
                              ([e, s]) =>
                                (0, t.jsxs)(
                                  "li",
                                  {
                                    children: [
                                      (0, t.jsx)("strong", { children: e }),
                                      ": ",
                                      s,
                                    ],
                                  },
                                  e,
                                ),
                            ),
                          }),
                        ],
                      }),
                    e.licenses &&
                      e.licenses.length > 0 &&
                      (0, t.jsxs)("div", {
                        children: [
                          (0, t.jsx)("h5", { children: "Top Licenses" }),
                          (0, t.jsxs)("div", {
                            style: {
                              display: "flex",
                              flexWrap: "wrap",
                              gap: "0.4rem",
                            },
                            children: [
                              e.licenses.slice(0, 15).map((e) =>
                                (0, t.jsx)(
                                  "span",
                                  {
                                    style: {
                                      padding: "2px 8px",
                                      background:
                                        "var(--ifm-color-emphasis-200)",
                                      borderRadius: "4px",
                                      fontSize: "0.8rem",
                                    },
                                    children: e,
                                  },
                                  e,
                                ),
                              ),
                              e.licenses.length > 15 &&
                                (0, t.jsx)("span", {
                                  style: { opacity: 0.5 },
                                  children: "...",
                                }),
                            ],
                          }),
                        ],
                      }),
                  ],
                }),
                (0, t.jsxs)("details", {
                  children: [
                    (0, t.jsx)("summary", {
                      style: { cursor: "pointer", fontWeight: 600 },
                      children: "Component List (Top 100)",
                    }),
                    (0, t.jsxs)("table", {
                      style: { marginTop: "1rem" },
                      children: [
                        (0, t.jsx)("thead", {
                          children: (0, t.jsxs)("tr", {
                            children: [
                              (0, t.jsx)("th", { children: "Name" }),
                              (0, t.jsx)("th", { children: "Version" }),
                              (0, t.jsx)("th", { children: "Type" }),
                              (0, t.jsx)("th", { children: "Licenses" }),
                            ],
                          }),
                        }),
                        (0, t.jsx)("tbody", {
                          children: e.components.slice(0, 100).map((e, s) =>
                            (0, t.jsxs)(
                              "tr",
                              {
                                children: [
                                  (0, t.jsx)("td", {
                                    style: {
                                      fontWeight: 600,
                                      fontSize: "0.85rem",
                                    },
                                    children: e.name,
                                  }),
                                  (0, t.jsx)("td", {
                                    style: {
                                      fontFamily: "monospace",
                                      fontSize: "0.85rem",
                                    },
                                    children: e.version,
                                  }),
                                  (0, t.jsx)("td", {
                                    children: (0, t.jsx)("span", {
                                      style: {
                                        fontSize: "0.75rem",
                                        opacity: 0.7,
                                        textTransform: "uppercase",
                                      },
                                      children: e.type,
                                    }),
                                  }),
                                  (0, t.jsx)("td", {
                                    style: { fontSize: "0.8rem" },
                                    children: e.licenses.join(", "),
                                  }),
                                ],
                              },
                              s,
                            ),
                          ),
                        }),
                      ],
                    }),
                  ],
                }),
              ],
            })
          : (0, t.jsx)("div", {
              className: "alert alert--warning",
              children: "No SBOM could be generated for this image.",
            });
      }
      const P = {
        FATAL: "#dc2626",
        WARN: "#d97706",
        INFO: "#2563eb",
        SKIP: "#6b7280",
        PASS: "#22c55e",
      };
      function W({ data: e }) {
        return (0, t.jsxs)("div", {
          children: [
            (0, t.jsxs)("div", {
              style: {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                gap: "0.75rem",
                marginBottom: "1rem",
              },
              children: [
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Status",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.passed
                        ? "\u2705 Passed"
                        : "\u26a0\ufe0f Issues",
                    }),
                  ],
                }),
                (0, t.jsxs)("div", {
                  className: "stat-card",
                  children: [
                    (0, t.jsx)("div", {
                      className: "stat-card__label",
                      children: "Issues",
                    }),
                    (0, t.jsx)("div", {
                      className: "stat-card__value",
                      children: e.issues_count,
                    }),
                  ],
                }),
                e.issues_by_level &&
                  Object.entries(e.issues_by_level)
                    .filter(([e, s]) => s > 0 && "PASS" !== e && "SKIP" !== e)
                    .map(([e, s]) =>
                      (0, t.jsxs)(
                        "div",
                        {
                          className: "stat-card",
                          children: [
                            (0, t.jsx)("div", {
                              className: "stat-card__label",
                              children: e,
                            }),
                            (0, t.jsx)("div", {
                              className: "stat-card__value",
                              style: { color: P[e] ?? "inherit" },
                              children: s,
                            }),
                          ],
                        },
                        e,
                      ),
                    ),
              ],
            }),
            e.issues &&
              e.issues.length > 0 &&
              (0, t.jsxs)("table", {
                children: [
                  (0, t.jsx)("thead", {
                    children: (0, t.jsxs)("tr", {
                      children: [
                        (0, t.jsx)("th", { children: "Code" }),
                        (0, t.jsx)("th", { children: "Level" }),
                        (0, t.jsx)("th", { children: "Description" }),
                      ],
                    }),
                  }),
                  (0, t.jsx)("tbody", {
                    children: e.issues
                      .filter((e) => "PASS" !== e.level && "SKIP" !== e.level)
                      .map((e, s) =>
                        (0, t.jsxs)(
                          "tr",
                          {
                            children: [
                              (0, t.jsx)("td", {
                                style: {
                                  fontFamily: "monospace",
                                  fontSize: "0.85rem",
                                  fontWeight: 600,
                                },
                                children: e.code,
                              }),
                              (0, t.jsx)("td", {
                                children: (0, t.jsx)("span", {
                                  style: {
                                    padding: "2px 8px",
                                    borderRadius: "4px",
                                    fontSize: "0.75rem",
                                    fontWeight: 700,
                                    color: "#fff",
                                    background: P[e.level] ?? "#6b7280",
                                  },
                                  children: e.level,
                                }),
                              }),
                              (0, t.jsxs)("td", {
                                children: [
                                  (0, t.jsx)("div", {
                                    style: {
                                      fontSize: "0.85rem",
                                      fontWeight: 600,
                                    },
                                    children: e.title,
                                  }),
                                  e.alerts &&
                                    e.alerts.length > 0 &&
                                    (0, t.jsx)("ul", {
                                      style: {
                                        fontSize: "0.8rem",
                                        marginTop: "0.4rem",
                                        opacity: 0.8,
                                      },
                                      children: e.alerts.map((e, s) =>
                                        (0, t.jsx)("li", { children: e }, s),
                                      ),
                                    }),
                                ],
                              }),
                            ],
                          },
                          s,
                        ),
                      ),
                  }),
                ],
              }),
          ],
        });
      }
      function B(e, s) {
        switch (e) {
          case "trivy":
            return (0, t.jsx)(u, { data: s });
          case "freshness":
            return (0, t.jsx)(g, { data: s });
          case "size":
            return (0, t.jsx)(y, { data: s });
          case "hadolint":
            return (0, t.jsx)(_, { data: s });
          case "popularity":
            return (0, t.jsx)(N, { data: s });
          case "endoflife":
            return (0, t.jsx)(S, { data: s });
          case "provenance":
            return (0, t.jsx)(T, { data: s });
          case "scorecarddev":
            return (0, t.jsx)(C, { data: s });
          case "versioning":
            return (0, t.jsx)(A, { data: s });
          case "skopeo":
            return (0, t.jsx)(L, { data: s });
          case "sbom":
            return (0, t.jsx)(F, { data: s });
          case "dockle":
            return (0, t.jsx)(W, { data: s });
          default:
            return (0, t.jsx)(x.A, {
              language: "json",
              title: `${e} (raw)`,
              children: JSON.stringify(s, null, 2),
            });
        }
      }
      function I({ name: e, data: s }) {
        return (0, t.jsxs)("div", {
          style: { marginBottom: "1.5rem" },
          children: [
            (0, t.jsx)("h4", {
              style: { textTransform: "capitalize" },
              children: e.replace(/_/g, " "),
            }),
            B(e, s),
          ],
        });
      }
      var R = r(5317);
      function D({ analyzerName: e, error: s }) {
        return (0, t.jsx)(R.A, {
          type: "danger",
          title: `${e} \u2014 ${s.type ?? "error"}`,
          children: (0, t.jsx)("p", {
            children: s.message ?? "An unknown error occurred.",
          }),
        });
      }
      function O() {
        const { report: e } = (0, i.e)();
        if (!e?.request)
          return (0, t.jsx)("p", {
            children: "No request metadata available.",
          });
        const s = e.request,
          r = [
            { label: "Registry", value: s.registry },
            { label: "Repository", value: s.repository },
            { label: "Tag", value: s.tag },
            { label: "Digest", value: s.digest },
            {
              label: "Timestamp",
              value: s.timestamp
                ? new Date(s.timestamp).toLocaleString()
                : "N/A",
            },
            {
              label: "Platform Override",
              value: s.platform || "Not specified",
            },
          ];
        return (0, t.jsxs)("table", {
          children: [
            (0, t.jsx)("thead", {
              children: (0, t.jsxs)("tr", {
                children: [
                  (0, t.jsx)("th", {
                    style: { width: "200px" },
                    children: "Parameter",
                  }),
                  (0, t.jsx)("th", { children: "Value" }),
                ],
              }),
            }),
            (0, t.jsx)("tbody", {
              children: r.map((e, s) =>
                (0, t.jsxs)(
                  "tr",
                  {
                    children: [
                      (0, t.jsx)("td", {
                        style: { fontWeight: 600 },
                        children: e.label,
                      }),
                      (0, t.jsx)("td", {
                        style: {
                          fontFamily:
                            e.value && e.value.length > 20
                              ? "monospace"
                              : "inherit",
                          fontSize: "0.9rem",
                        },
                        children: e.value || "\u2014",
                      }),
                    ],
                  },
                  s,
                ),
              ),
            }),
          ],
        });
      }
      function M({ block: e, section: s, results: r }) {
        switch (e) {
          case "widgets":
            if (!s.widgets) return null;
            const e = new Set(),
              a = s.widgets.filter((s) => {
                const r =
                  ((a = s.template) &&
                    a.startsWith("analyzers/") &&
                    a.split("/")[1]) ||
                  null;
                var a;
                return r ? (e.add(r), !1) : "request/table.html" !== s.template;
              }),
              l = s.widgets.some((e) => "request/table.html" === e.template);
            return (0, t.jsxs)(t.Fragment, {
              children: [
                a.length > 0 && (0, t.jsx)(d, { widgets: a }),
                l && (0, t.jsx)(O, {}),
                Array.from(e).map((e) => {
                  const s = r[e];
                  if (!s) return null;
                  const a = s;
                  return a.error
                    ? (0, t.jsx)(D, { analyzerName: e, error: a.error }, e)
                    : (0, t.jsx)(I, { name: e, data: a }, e);
                }),
              ],
            });
          case "levels":
            return s.levels_summary
              ? (0, t.jsx)(o, { levels: s.levels_summary })
              : null;
          case "tags":
            return s.tags_summary
              ? (0, t.jsx)(o, { levels: s.tags_summary })
              : null;
          case "scorecards":
            return s.scorecards
              ? (0, t.jsx)(m, {
                  scorecards: s.scorecards,
                  showLevels: !!s.levels_summary,
                })
              : null;
          case "analyzers":
            return (0, t.jsx)(t.Fragment, {
              children: s.display?.analyzers?.map((e) => {
                const s = r[e];
                if (!s) return null;
                const a = s;
                if (a.error) {
                  const s = a.error;
                  return (0, t.jsx)(D, { analyzerName: e, error: s }, e);
                }
                return (0, t.jsx)(I, { name: e, data: a }, e);
              }),
            });
          default:
            return null;
        }
      }
      function $() {
        const { report: e, loading: s, error: r } = (0, i.e)();
        if (s)
          return (0, t.jsx)("p", { children: "Loading report data\u2026" });
        if (r)
          return (0, t.jsxs)("div", {
            className: "alert alert--danger",
            children: ["Error: ", r],
          });
        if (!e)
          return (0, t.jsx)("p", { children: "No report data available." });
        const a = e.playbooks ?? [];
        if (0 === a.length)
          return (0, t.jsx)("div", {
            className: "alert alert--info",
            children: "No playbooks were evaluated in this report.",
          });
        const l = e.results ?? {};
        return (0, t.jsx)("div", {
          children: a.map((e, s) =>
            (0, t.jsx)(
              "div",
              {
                children: e.pages?.map((s, r) =>
                  (0, t.jsxs)(
                    "div",
                    {
                      children: [
                        (e.pages?.length ?? 0) > 1 &&
                          (0, t.jsx)("h3", {
                            style: { color: "var(--ifm-color-primary)" },
                            children: s.title,
                          }),
                        s.sections?.map((e, s) =>
                          (0, t.jsxs)(
                            "div",
                            {
                              style: { marginBottom: "2rem" },
                              children: [
                                (0, t.jsx)("h4", { children: e.name }),
                                e.hint &&
                                  (0, t.jsx)("p", {
                                    style: {
                                      opacity: 0.7,
                                      fontStyle: "italic",
                                    },
                                    children: e.hint,
                                  }),
                                e.render_order?.map((s, r) =>
                                  (0, t.jsx)(
                                    M,
                                    { block: s, section: e, results: l },
                                    r,
                                  ),
                                ),
                              ],
                            },
                            s,
                          ),
                        ),
                      ],
                    },
                    r,
                  ),
                ),
              },
              s,
            ),
          ),
        });
      }
      const U = { title: "Playbook" },
        V = "Playbook Results",
        H = {},
        K = [];
      function q(e) {
        const s = {
          h1: "h1",
          header: "header",
          ...(0, l.R)(),
          ...e.components,
        };
        return (0, t.jsxs)(t.Fragment, {
          children: [
            (0, t.jsx)(s.header, {
              children: (0, t.jsx)(s.h1, {
                id: "playbook-results",
                children: "Playbook Results",
              }),
            }),
            "\n",
            (0, t.jsx)($, {}),
          ],
        });
      }
      function E(e = {}) {
        const { wrapper: s } = { ...(0, l.R)(), ...e.components };
        return s
          ? (0, t.jsx)(s, { ...e, children: (0, t.jsx)(q, { ...e }) })
          : q(e);
      }
    },
  },
]);
