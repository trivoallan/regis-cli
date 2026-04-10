"use strict";
(globalThis.webpackChunk_regis_report_viewer =
  globalThis.webpackChunk_regis_report_viewer || []).push([
  [9157],
  {
    99533(e, s, r) {
      (r.r(s),
        r.d(s, {
          assets: () => p,
          contentTitle: () => o,
          default: () => u,
          frontMatter: () => l,
          metadata: () => t,
          toc: () => d,
        }));
      const t = JSON.parse(
        '{"id":"analyzers/freshness","title":"Freshness","description":"","source":"@site/docs/analyzers/freshness.mdx","sourceDirName":"analyzers","slug":"/analyzers/freshness","permalink":"/regis/examples/playbooks/default/alpine/report/analyzers/freshness","draft":false,"unlisted":false,"tags":[],"version":"current","frontMatter":{"title":"Freshness","hide_title":true},"sidebar":"defaultSidebar","previous":{"title":"End of Life","permalink":"/regis/examples/playbooks/default/alpine/report/analyzers/endoflife"},"next":{"title":"Hadolint","permalink":"/regis/examples/playbooks/default/alpine/report/analyzers/hadolint"}}',
      );
      var a = r(56730),
        n = r(26451),
        i = r(39796);
      const l = { title: "Freshness", hide_title: !0 },
        o = void 0,
        p = {},
        d = [];
      function f(e) {
        return (0, a.jsx)(i.e, { name: "freshness" });
      }
      function u(e = {}) {
        const { wrapper: s } = { ...(0, n.R)(), ...e.components };
        return s
          ? (0, a.jsx)(s, { ...e, children: (0, a.jsx)(f, { ...e }) })
          : f();
      }
    },
  },
]);
