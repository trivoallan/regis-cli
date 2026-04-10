"use strict";
(globalThis.webpackChunk_regis_report_viewer =
  globalThis.webpackChunk_regis_report_viewer || []).push([
  [9213],
  {
    57118(e, r, t) {
      (t.r(r),
        t.d(r, {
          assets: () => p,
          contentTitle: () => o,
          default: () => y,
          frontMatter: () => n,
          metadata: () => i,
          toc: () => u,
        }));
      const i = JSON.parse(
        '{"id":"analyzers/trivy","title":"Trivy","description":"","source":"@site/docs/analyzers/trivy.mdx","sourceDirName":"analyzers","slug":"/analyzers/trivy","permalink":"/regis/examples/playbooks/default/alpine/report/analyzers/trivy","draft":false,"unlisted":false,"tags":[],"version":"current","frontMatter":{"title":"Trivy","hide_title":true},"sidebar":"defaultSidebar","previous":{"title":"Size","permalink":"/regis/examples/playbooks/default/alpine/report/analyzers/size"},"next":{"title":"Versioning","permalink":"/regis/examples/playbooks/default/alpine/report/analyzers/versioning"}}',
      );
      var a = t(56730),
        s = t(26451),
        l = t(39796);
      const n = { title: "Trivy", hide_title: !0 },
        o = void 0,
        p = {},
        u = [];
      function d(e) {
        return (0, a.jsx)(l.e, { name: "trivy" });
      }
      function y(e = {}) {
        const { wrapper: r } = { ...(0, s.R)(), ...e.components };
        return r
          ? (0, a.jsx)(r, { ...e, children: (0, a.jsx)(d, { ...e }) })
          : d();
      }
    },
  },
]);
