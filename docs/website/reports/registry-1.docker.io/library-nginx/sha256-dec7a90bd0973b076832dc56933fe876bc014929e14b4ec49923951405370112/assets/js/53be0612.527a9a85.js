"use strict";
(globalThis.webpackChunk_regis_cli_report_viewer =
  globalThis.webpackChunk_regis_cli_report_viewer || []).push([
  [3375],
  {
    8819(e, r, s) {
      (s.r(r),
        s.d(r, {
          assets: () => m,
          contentTitle: () => h,
          default: () => g,
          frontMatter: () => p,
          metadata: () => l,
          toc: () => x,
        }));
      const l = JSON.parse(
        '{"id":"rules","title":"Rules","description":"","source":"@site/docs/rules.mdx","sourceDirName":".","slug":"/rules","permalink":"/rules","draft":false,"unlisted":false,"tags":[],"version":"current","frontMatter":{"title":"Rules"},"sidebar":"defaultSidebar","previous":{"title":"Overview","permalink":"/"},"next":{"title":"Playbook","permalink":"/playbook"}}',
      );
      var t = s(6730),
        a = s(6451),
        i = s(162),
        n = s(1450),
        o = s(1664);
      function d({ passed: e, status: r }) {
        return "incomplete" === r
          ? (0, t.jsx)("span", {
              title: "Incomplete",
              children: "\u26a0\ufe0f",
            })
          : e
            ? (0, t.jsx)("span", { title: "Passed", children: "\u2705" })
            : (0, t.jsx)("span", { title: "Failed", children: "\u274c" });
      }
      function c({ rules: e, summary: r }) {
        const [s, l] = (0, i.useState)("all"),
          a = "all" === s ? e : e.filter((e) => e.tags?.includes(s)),
          n = r?.by_tag ?? {};
        return (0, t.jsxs)("div", {
          children: [
            Object.keys(n).length > 0 &&
              (0, t.jsx)("div", {
                style: {
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                  gap: "0.75rem",
                  marginBottom: "1.5rem",
                },
                children: Object.entries(n)
                  .sort(([e], [r]) => e.localeCompare(r))
                  .map(([e, r]) =>
                    (0, t.jsxs)(
                      "button",
                      {
                        type: "button",
                        onClick: () => l(s === e ? "all" : e),
                        style: {
                          cursor: "pointer",
                          padding: "0.75rem",
                          textAlign: "center",
                          background: "var(--ifm-card-background-color)",
                          border:
                            s === e
                              ? "2px solid var(--ifm-color-primary)"
                              : "1px solid var(--ifm-color-emphasis-200)",
                          borderRadius: "8px",
                          transform: s === e ? "scale(1.03)" : "scale(1)",
                          transition: "all 0.2s ease",
                        },
                        children: [
                          (0, t.jsx)("small", {
                            style: {
                              textTransform: "uppercase",
                              fontWeight: 700,
                              letterSpacing: "0.05em",
                              opacity: 0.8,
                            },
                            children: e,
                          }),
                          (0, t.jsx)("br", {}),
                          (0, t.jsxs)("span", {
                            style: { fontSize: "1.5rem", fontWeight: 700 },
                            children: [r.score, "%"],
                          }),
                          (0, t.jsx)("br", {}),
                          (0, t.jsxs)("small", {
                            style: { opacity: 0.6 },
                            children: [
                              r.passed_rules.length,
                              " / ",
                              r.rules.length,
                              " passed",
                            ],
                          }),
                        ],
                      },
                      e,
                    ),
                  ),
              }),
            (0, t.jsxs)("div", {
              style: {
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "0.75rem",
              },
              children: [
                (0, t.jsx)("h4", {
                  style: { margin: 0 },
                  children: "Detailed Results",
                }),
                (0, t.jsxs)("select", {
                  value: s,
                  onChange: (e) => l(e.target.value),
                  style: {
                    padding: "0.3rem 0.5rem",
                    borderRadius: "4px",
                    border: "1px solid var(--ifm-color-emphasis-300)",
                    background: "var(--ifm-background-color)",
                    color: "var(--ifm-font-color-base)",
                  },
                  children: [
                    (0, t.jsx)("option", {
                      value: "all",
                      children: "All Tags",
                    }),
                    Object.keys(n)
                      .sort()
                      .map((e) =>
                        (0, t.jsx)("option", { value: e, children: e }, e),
                      ),
                  ],
                }),
              ],
            }),
            (0, t.jsx)("div", {
              style: { overflowX: "auto" },
              children: (0, t.jsxs)("table", {
                children: [
                  (0, t.jsx)("thead", {
                    children: (0, t.jsxs)("tr", {
                      children: [
                        (0, t.jsx)("th", { children: "Status" }),
                        (0, t.jsx)("th", { children: "Level" }),
                        (0, t.jsx)("th", { children: "Rule" }),
                        (0, t.jsx)("th", { children: "Tags" }),
                      ],
                    }),
                  }),
                  (0, t.jsx)("tbody", {
                    children: a.map((e, r) =>
                      (0, t.jsxs)(
                        "tr",
                        {
                          children: [
                            (0, t.jsx)("td", {
                              style: { textAlign: "center" },
                              children: (0, t.jsx)(d, {
                                passed: e.passed,
                                status: e.status,
                              }),
                            }),
                            (0, t.jsx)("td", {
                              children: (0, t.jsx)(o.M, {
                                label: e.level,
                                variant: (0, o.Z)(e.level),
                              }),
                            }),
                            (0, t.jsxs)("td", {
                              children: [
                                (0, t.jsx)("strong", {
                                  children: e.description ?? e.title ?? e.slug,
                                }),
                                e.message &&
                                  (0, t.jsx)("div", {
                                    style: {
                                      fontSize: "0.85rem",
                                      opacity: 0.8,
                                      marginTop: "0.2rem",
                                    },
                                    children: e.message,
                                  }),
                                e.analyzers &&
                                  e.analyzers.length > 0 &&
                                  (0, t.jsx)("div", {
                                    style: { marginTop: "0.3rem" },
                                    children: e.analyzers.map((e) =>
                                      (0, t.jsx)(
                                        o.M,
                                        { label: e, variant: "outline" },
                                        e,
                                      ),
                                    ),
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
                                children: e.tags?.map((e) =>
                                  (0, t.jsx)(o.M, { label: e }, e),
                                ),
                              }),
                            }),
                          ],
                        },
                        e.slug ?? r,
                      ),
                    ),
                  }),
                ],
              }),
            }),
          ],
        });
      }
      function u() {
        const { report: e, loading: r, error: s } = (0, n.e)();
        if (r)
          return (0, t.jsx)("p", { children: "Loading report data\u2026" });
        if (s)
          return (0, t.jsxs)("div", {
            className: "alert alert--danger",
            children: ["Error: ", s],
          });
        if (!e)
          return (0, t.jsx)("p", { children: "No report data available." });
        const l = e.rules ?? e.playbook?.rules ?? [],
          a = e.rules_summary ?? e.playbook?.rules_summary;
        return 0 === l.length
          ? (0, t.jsx)("div", {
              className: "alert alert--info",
              children: "No rules were evaluated in this report.",
            })
          : (0, t.jsx)(c, { rules: l, summary: a });
      }
      const p = { title: "Rules" },
        h = "Rules Evaluation",
        m = {},
        x = [];
      function j(e) {
        const r = {
          h1: "h1",
          header: "header",
          ...(0, a.R)(),
          ...e.components,
        };
        return (0, t.jsxs)(t.Fragment, {
          children: [
            (0, t.jsx)(r.header, {
              children: (0, t.jsx)(r.h1, {
                id: "rules-evaluation",
                children: "Rules Evaluation",
              }),
            }),
            "\n",
            (0, t.jsx)(u, {}),
          ],
        });
      }
      function g(e = {}) {
        const { wrapper: r } = { ...(0, a.R)(), ...e.components };
        return r
          ? (0, t.jsx)(r, { ...e, children: (0, t.jsx)(j, { ...e }) })
          : j(e);
      }
    },
  },
]);
