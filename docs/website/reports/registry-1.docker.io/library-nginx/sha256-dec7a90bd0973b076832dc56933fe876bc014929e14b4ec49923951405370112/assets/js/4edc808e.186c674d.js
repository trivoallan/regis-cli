"use strict";
(globalThis.webpackChunk_regis_cli_report_viewer =
  globalThis.webpackChunk_regis_cli_report_viewer || []).push([
  [308],
  {
    3230(e, r, s) {
      (s.r(r),
        s.d(r, {
          assets: () => p,
          contentTitle: () => g,
          default: () => u,
          frontMatter: () => m,
          metadata: () => a,
          toc: () => x,
        }));
      const a = JSON.parse(
        '{"id":"index","title":"index","description":"","source":"@site/docs/index.mdx","sourceDirName":".","slug":"/","permalink":"/","draft":false,"unlisted":false,"tags":[],"version":"current","frontMatter":{"slug":"/","hide_title":true},"sidebar":"defaultSidebar","next":{"title":"Rules","permalink":"/rules"}}',
      );
      var i = s(6730),
        t = s(6451),
        l = (s(162), s(1450));
      const n = {
        gold: {
          icon: "\ud83e\udd47",
          gradient: "linear-gradient(135deg, #f9a825, #ff8f00)",
        },
        silver: {
          icon: "\ud83e\udd48",
          gradient: "linear-gradient(135deg, #90a4ae, #607d8b)",
        },
        bronze: {
          icon: "\ud83e\udd49",
          gradient: "linear-gradient(135deg, #a1887f, #795548)",
        },
        none: {
          icon: "\u2b55",
          gradient: "linear-gradient(135deg, #757575, #424242)",
        },
      };
      function d({ tier: e }) {
        const r = n[e?.toLowerCase()] ?? n.none;
        return (0, i.jsxs)("span", {
          style: {
            display: "inline-flex",
            alignItems: "center",
            gap: "0.4rem",
            background: r.gradient,
            color: "#fff",
            padding: "0.3rem 0.8rem",
            borderRadius: "6px",
            fontSize: "0.9rem",
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.05em",
            boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
          },
          children: [
            (0, i.jsx)("span", {
              style: { fontSize: "1.1rem" },
              children: r.icon,
            }),
            e,
            " Tier",
          ],
        });
      }
      var c = s(1664);
      function o() {
        const { report: e, loading: r, error: s } = (0, l.e)();
        if (r)
          return (0, i.jsx)("p", { children: "Loading report data\u2026" });
        if (s)
          return (0, i.jsxs)("div", {
            className: "alert alert--danger",
            children: ["Error: ", s],
          });
        if (!e)
          return (0, i.jsx)("p", { children: "No report data available." });
        const a = e.request ?? {},
          t = e.playbook ?? (e.playbooks ? e.playbooks[0] : void 0),
          n = t?.score ?? e.rules_summary?.score,
          o = e.tier ?? t?.tier,
          m = a.analyzers ?? [];
        let g = "score-circle--low";
        return (
          void 0 !== n &&
            (n >= 80
              ? (g = "score-circle--high")
              : n >= 50 && (g = "score-circle--medium")),
          (0, i.jsxs)("div", {
            children: [
              (0, i.jsxs)("h1", {
                children: [a.registry, "/", a.repository, ":", a.tag],
              }),
              (0, i.jsxs)("div", {
                style: {
                  display: "flex",
                  alignItems: "center",
                  gap: "1rem",
                  flexWrap: "wrap",
                  marginBottom: "1rem",
                },
                children: [
                  o && (0, i.jsx)(d, { tier: o }),
                  e.badges?.map((e, r) =>
                    (0, i.jsx)(
                      c.M,
                      { label: e.label, variant: (0, c.Z)(e.class) },
                      r,
                    ),
                  ),
                ],
              }),
              void 0 !== n &&
                (0, i.jsxs)("div", {
                  style: {
                    display: "flex",
                    alignItems: "center",
                    gap: "1.5rem",
                    marginBottom: "1.5rem",
                  },
                  children: [
                    (0, i.jsxs)("div", {
                      className: `score-circle ${g}`,
                      children: [n, "%"],
                    }),
                    (0, i.jsxs)("div", {
                      children: [
                        (0, i.jsx)("div", {
                          style: { fontSize: "0.85rem", opacity: 0.7 },
                          children: "Overall Score",
                        }),
                        (0, i.jsxs)("div", {
                          style: { fontSize: "0.85rem", opacity: 0.7 },
                          children: [
                            t?.passed_scorecards ?? "?",
                            "/",
                            t?.total_scorecards ?? "?",
                            " ",
                            "scorecards passed",
                          ],
                        }),
                      ],
                    }),
                  ],
                }),
              (0, i.jsxs)("div", {
                style: {
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                  gap: "0.75rem",
                  marginBottom: "1.5rem",
                },
                children: [
                  (0, i.jsxs)("div", {
                    className: "stat-card",
                    children: [
                      (0, i.jsx)("div", {
                        className: "stat-card__label",
                        children: "Registry",
                      }),
                      (0, i.jsx)("div", {
                        className: "stat-card__value",
                        style: { fontSize: "1rem" },
                        children: a.registry ?? "unknown",
                      }),
                    ],
                  }),
                  (0, i.jsxs)("div", {
                    className: "stat-card",
                    children: [
                      (0, i.jsx)("div", {
                        className: "stat-card__label",
                        children: "Tag",
                      }),
                      (0, i.jsx)("div", {
                        className: "stat-card__value",
                        style: { fontSize: "1rem" },
                        children: a.tag ?? "latest",
                      }),
                    ],
                  }),
                  (0, i.jsxs)("div", {
                    className: "stat-card",
                    children: [
                      (0, i.jsx)("div", {
                        className: "stat-card__label",
                        children: "Analyzers",
                      }),
                      (0, i.jsx)("div", {
                        className: "stat-card__value",
                        style: { fontSize: "1rem" },
                        children: m.length,
                      }),
                    ],
                  }),
                  (0, i.jsxs)("div", {
                    className: "stat-card",
                    children: [
                      (0, i.jsx)("div", {
                        className: "stat-card__label",
                        children: "Timestamp",
                      }),
                      (0, i.jsx)("div", {
                        className: "stat-card__value",
                        style: { fontSize: "0.85rem" },
                        children: a.timestamp
                          ? new Date(a.timestamp).toLocaleString()
                          : "N/A",
                      }),
                    ],
                  }),
                ],
              }),
              e.links &&
                e.links.length > 0 &&
                (0, i.jsx)("div", {
                  className: "report-links",
                  children: e.links.map((e, r) =>
                    (0, i.jsx)(
                      "a",
                      {
                        href: e.url,
                        target: "_blank",
                        rel: "noopener noreferrer",
                        children: e.label,
                      },
                      r,
                    ),
                  ),
                }),
            ],
          })
        );
      }
      const m = { slug: "/", hide_title: !0 },
        g = void 0,
        p = {},
        x = [];
      function h(e) {
        return (0, i.jsx)(o, {});
      }
      function u(e = {}) {
        const { wrapper: r } = { ...(0, t.R)(), ...e.components };
        return r
          ? (0, i.jsx)(r, { ...e, children: (0, i.jsx)(h, { ...e }) })
          : h();
      }
    },
  },
]);
