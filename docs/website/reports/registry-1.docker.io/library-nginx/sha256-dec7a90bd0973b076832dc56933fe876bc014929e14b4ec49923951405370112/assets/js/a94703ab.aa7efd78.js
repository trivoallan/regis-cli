"use strict";
(globalThis.webpackChunk_regis_cli_report_viewer =
  globalThis.webpackChunk_regis_cli_report_viewer || []).push([
  [9048],
  {
    5676(e, t, n) {
      (n.r(t), n.d(t, { default: () => Se }));
      var a = n(162),
        i = n(851),
        s = n(3743),
        o = n(5052),
        l = n(6827),
        r = n(1032),
        c = n(4765),
        d = n(9019),
        u = n(2245);
      const b = "backToTopButton_Ne_1",
        m = "backToTopButtonShow_NcFK";
      var h = n(6730);
      function p() {
        const { shown: e, scrollToTop: t } = (function ({ threshold: e }) {
          const [t, n] = (0, a.useState)(!1),
            i = (0, a.useRef)(!1),
            { startScroll: s, cancelScroll: o } = (0, d.gk)();
          return (
            (0, d.Mq)(({ scrollY: t }, a) => {
              const s = a?.scrollY;
              s &&
                (i.current
                  ? (i.current = !1)
                  : t >= s
                    ? (o(), n(!1))
                    : t < e
                      ? n(!1)
                      : t + window.innerHeight <
                          document.documentElement.scrollHeight && n(!0));
            }),
            (0, u.$)((e) => {
              e.location.hash && ((i.current = !0), n(!1));
            }),
            { shown: t, scrollToTop: () => s(0) }
          );
        })({ threshold: 300 });
        return (0, h.jsx)("button", {
          "aria-label": (0, c.T)({
            id: "theme.BackToTopButton.buttonAriaLabel",
            message: "Scroll back to top",
            description: "The ARIA label for the back to top button",
          }),
          className: (0, i.A)(
            "clean-btn",
            o.G.common.backToTopButton,
            b,
            e && m,
          ),
          type: "button",
          onClick: t,
        });
      }
      var x = n(492),
        _ = n(9139),
        f = n(3882),
        j = n(3211),
        v = n(5131);
      function C(e) {
        return (0, h.jsx)("svg", {
          width: "20",
          height: "20",
          "aria-hidden": "true",
          ...e,
          children: (0, h.jsxs)("g", {
            fill: "#7a7a7a",
            children: [
              (0, h.jsx)("path", {
                d: "M9.992 10.023c0 .2-.062.399-.172.547l-4.996 7.492a.982.982 0 01-.828.454H1c-.55 0-1-.453-1-1 0-.2.059-.403.168-.551l4.629-6.942L.168 3.078A.939.939 0 010 2.528c0-.548.45-.997 1-.997h2.996c.352 0 .649.18.828.45L9.82 9.472c.11.148.172.347.172.55zm0 0",
              }),
              (0, h.jsx)("path", {
                d: "M19.98 10.023c0 .2-.058.399-.168.547l-4.996 7.492a.987.987 0 01-.828.454h-3c-.547 0-.996-.453-.996-1 0-.2.059-.403.168-.551l4.625-6.942-4.625-6.945a.939.939 0 01-.168-.55 1 1 0 01.996-.997h3c.348 0 .649.18.828.45l4.996 7.492c.11.148.168.347.168.55zm0 0",
              }),
            ],
          }),
        });
      }
      const g = "collapseSidebarButton_zJBK",
        A = "collapseSidebarButtonIcon_syuz";
      function k({ onClick: e }) {
        return (0, h.jsx)("button", {
          type: "button",
          title: (0, c.T)({
            id: "theme.docs.sidebar.collapseButtonTitle",
            message: "Collapse sidebar",
            description:
              "The title attribute for collapse button of doc sidebar",
          }),
          "aria-label": (0, c.T)({
            id: "theme.docs.sidebar.collapseButtonAriaLabel",
            message: "Collapse sidebar",
            description:
              "The title attribute for collapse button of doc sidebar",
          }),
          className: (0, i.A)("button button--secondary button--outline", g),
          onClick: e,
          children: (0, h.jsx)(C, { className: A }),
        });
      }
      var S = n(372),
        I = n(1089);
      const N = Symbol("EmptyContext"),
        T = a.createContext(N);
      function y({ children: e }) {
        const [t, n] = (0, a.useState)(null),
          i = (0, a.useMemo)(
            () => ({ expandedItem: t, setExpandedItem: n }),
            [t],
          );
        return (0, h.jsx)(T.Provider, { value: i, children: e });
      }
      var L = n(7615),
        w = n(454),
        E = n(3703),
        M = n(7518),
        B = n(8341),
        H = n(2708);
      const P = "menuExternalLink_l2L7",
        G = "linkLabel_rg7y";
      function D({ label: e }) {
        return (0, h.jsx)("span", { title: e, className: G, children: e });
      }
      function R({
        item: e,
        onItemClick: t,
        activePath: n,
        level: a,
        index: s,
        ...r
      }) {
        const { href: c, label: d, className: u, autoAddBaseUrl: b } = e,
          m = (0, l.w8)(e, n),
          p = (0, B.A)(c);
        return (0, h.jsx)(
          "li",
          {
            className: (0, i.A)(
              o.G.docs.docSidebarItemLink,
              o.G.docs.docSidebarItemLinkLevel(a),
              "menu__list-item",
              u,
            ),
            children: (0, h.jsxs)(E.A, {
              className: (0, i.A)("menu__link", !p && P, {
                "menu__link--active": m,
              }),
              autoAddBaseUrl: b,
              "aria-current": m ? "page" : void 0,
              to: c,
              ...(p && { onClick: t ? () => t(e) : void 0 }),
              ...r,
              children: [
                (0, h.jsx)(D, { label: d }),
                !p && (0, h.jsx)(H.A, {}),
              ],
            }),
          },
          d,
        );
      }
      const V = "categoryLink_EbuV",
        U = "categoryLinkLabel_id1M";
      function W({ collapsed: e, categoryLabel: t, onClick: n }) {
        return (0, h.jsx)("button", {
          "aria-label": e
            ? (0, c.T)(
                {
                  id: "theme.DocSidebarItem.expandCategoryAriaLabel",
                  message: "Expand sidebar category '{label}'",
                  description: "The ARIA label to expand the sidebar category",
                },
                { label: t },
              )
            : (0, c.T)(
                {
                  id: "theme.DocSidebarItem.collapseCategoryAriaLabel",
                  message: "Collapse sidebar category '{label}'",
                  description:
                    "The ARIA label to collapse the sidebar category",
                },
                { label: t },
              ),
          "aria-expanded": !e,
          type: "button",
          className: "clean-btn menu__caret",
          onClick: n,
        });
      }
      function Y({ label: e }) {
        return (0, h.jsx)("span", { title: e, className: U, children: e });
      }
      function z(e) {
        return 0 === (0, l.Y)(e.item.items, e.activePath).length
          ? (0, h.jsx)(F, { ...e })
          : (0, h.jsx)(K, { ...e });
      }
      function F({ item: e, ...t }) {
        if ("string" != typeof e.href) return null;
        const {
            type: n,
            collapsed: a,
            collapsible: i,
            items: s,
            linkUnlisted: o,
            ...l
          } = e,
          r = { type: "link", ...l };
        return (0, h.jsx)(R, { item: r, ...t });
      }
      function K({
        item: e,
        onItemClick: t,
        activePath: n,
        level: s,
        index: r,
        ...c
      }) {
        const { items: d, label: u, collapsible: b, className: m, href: p } = e,
          {
            docs: {
              sidebar: { autoCollapseCategories: x },
            },
          } = (0, j.p)(),
          _ = (function (e) {
            const t = (0, M.A)();
            return (0, a.useMemo)(
              () =>
                e.href && !e.linkUnlisted
                  ? e.href
                  : !t && e.collapsible
                    ? (0, l.Nr)(e)
                    : void 0,
              [e, t],
            );
          })(e),
          f = (0, l.w8)(e, n),
          v = (0, w.ys)(p, n),
          { collapsed: C, setCollapsed: g } = (0, L.u)({
            initialState: () => !!b && !f && e.collapsed,
          }),
          { expandedItem: A, setExpandedItem: k } = (function () {
            const e = (0, a.useContext)(T);
            if (e === N) throw new I.dV("DocSidebarItemsExpandedStateProvider");
            return e;
          })(),
          S = (e = !C) => {
            (k(e ? null : r), g(e));
          };
        (!(function ({
          isActive: e,
          collapsed: t,
          updateCollapsed: n,
          activePath: i,
        }) {
          const s = (0, I.ZC)(e),
            o = (0, I.ZC)(i);
          (0, a.useEffect)(() => {
            ((e && !s) || (e && s && i !== o)) && t && n(!1);
          }, [e, s, t, n, i, o]);
        })({ isActive: f, collapsed: C, updateCollapsed: S, activePath: n }),
          (0, a.useEffect)(() => {
            b && null != A && A !== r && x && g(!0);
          }, [b, A, r, g, x]));
        return (0, h.jsxs)("li", {
          className: (0, i.A)(
            o.G.docs.docSidebarItemCategory,
            o.G.docs.docSidebarItemCategoryLevel(s),
            "menu__list-item",
            { "menu__list-item--collapsed": C },
            m,
          ),
          children: [
            (0, h.jsxs)("div", {
              className: (0, i.A)("menu__list-item-collapsible", {
                "menu__list-item-collapsible--active": v,
              }),
              children: [
                (0, h.jsx)(E.A, {
                  className: (0, i.A)(V, "menu__link", {
                    "menu__link--sublist": b,
                    "menu__link--sublist-caret": !p && b,
                    "menu__link--active": f,
                  }),
                  onClick: (n) => {
                    (t?.(e),
                      b &&
                        (p
                          ? v
                            ? (n.preventDefault(), S())
                            : S(!1)
                          : (n.preventDefault(), S())));
                  },
                  "aria-current": v ? "page" : void 0,
                  role: b && !p ? "button" : void 0,
                  "aria-expanded": b && !p ? !C : void 0,
                  href: b ? (_ ?? "#") : _,
                  ...c,
                  children: (0, h.jsx)(Y, { label: u }),
                }),
                p &&
                  b &&
                  (0, h.jsx)(W, {
                    collapsed: C,
                    categoryLabel: u,
                    onClick: (e) => {
                      (e.preventDefault(), S());
                    },
                  }),
              ],
            }),
            (0, h.jsx)(L.N, {
              lazy: !0,
              as: "ul",
              className: "menu__list",
              collapsed: C,
              children: (0, h.jsx)(Q, {
                items: d,
                tabIndex: C ? -1 : 0,
                onItemClick: t,
                activePath: n,
                level: s + 1,
              }),
            }),
          ],
        });
      }
      const Z = "menuHtmlItem_xJnr";
      function q({ item: e, level: t, index: n }) {
        const { value: a, defaultStyle: s, className: l } = e;
        return (0, h.jsx)(
          "li",
          {
            className: (0, i.A)(
              o.G.docs.docSidebarItemLink,
              o.G.docs.docSidebarItemLinkLevel(t),
              s && [Z, "menu__list-item"],
              l,
            ),
            dangerouslySetInnerHTML: { __html: a },
          },
          n,
        );
      }
      function J({ item: e, ...t }) {
        switch (e.type) {
          case "category":
            return (0, h.jsx)(z, { item: e, ...t });
          case "html":
            return (0, h.jsx)(q, { item: e, ...t });
          default:
            return (0, h.jsx)(R, { item: e, ...t });
        }
      }
      function O({ items: e, ...t }) {
        const n = (0, l.Y)(e, t.activePath);
        return (0, h.jsx)(y, {
          children: n.map((e, n) =>
            (0, h.jsx)(J, { item: e, index: n, ...t }, n),
          ),
        });
      }
      const Q = (0, a.memo)(O),
        X = "menu_Vcmb",
        $ = "menuWithAnnouncementBar_GY4Z";
      function ee({ path: e, sidebar: t, className: n }) {
        const s = (function () {
          const { isActive: e } = (0, S.M)(),
            [t, n] = (0, a.useState)(e);
          return (
            (0, d.Mq)(
              ({ scrollY: t }) => {
                e && n(0 === t);
              },
              [e],
            ),
            e && t
          );
        })();
        return (0, h.jsx)("nav", {
          "aria-label": (0, c.T)({
            id: "theme.docs.sidebar.navAriaLabel",
            message: "Docs sidebar",
            description: "The ARIA label for the sidebar navigation",
          }),
          className: (0, i.A)("menu thin-scrollbar", X, s && $, n),
          children: (0, h.jsx)("ul", {
            className: (0, i.A)(o.G.docs.docSidebarMenu, "menu__list"),
            children: (0, h.jsx)(Q, { items: t, activePath: e, level: 1 }),
          }),
        });
      }
      const te = "sidebar_IMQ1",
        ne = "sidebarWithHideableNavbar_IU3w",
        ae = "sidebarHidden__NRH",
        ie = "sidebarLogo__shU";
      function se({ path: e, sidebar: t, onCollapse: n, isHidden: a }) {
        const {
          navbar: { hideOnScroll: s },
          docs: {
            sidebar: { hideable: o },
          },
        } = (0, j.p)();
        return (0, h.jsxs)("div", {
          className: (0, i.A)(te, s && ne, a && ae),
          children: [
            s && (0, h.jsx)(v.A, { tabIndex: -1, className: ie }),
            (0, h.jsx)(ee, { path: e, sidebar: t }),
            o && (0, h.jsx)(k, { onClick: n }),
          ],
        });
      }
      const oe = a.memo(se);
      var le = n(4489),
        re = n(5848);
      const ce = ({ sidebar: e, path: t }) => {
        const n = (0, re.M)();
        return (0, h.jsx)("ul", {
          className: (0, i.A)(o.G.docs.docSidebarMenu, "menu__list"),
          children: (0, h.jsx)(Q, {
            items: e,
            activePath: t,
            onItemClick: (e) => {
              ("category" === e.type && e.href && n.toggle(),
                "link" === e.type && n.toggle());
            },
            level: 1,
          }),
        });
      };
      function de(e) {
        return (0, h.jsx)(le.GX, { component: ce, props: e });
      }
      const ue = a.memo(de);
      function be(e) {
        const t = (0, f.l)(),
          n = "desktop" === t || "ssr" === t,
          a = "mobile" === t;
        return (0, h.jsxs)(h.Fragment, {
          children: [
            n && (0, h.jsx)(oe, { ...e }),
            a && (0, h.jsx)(ue, { ...e }),
          ],
        });
      }
      const me = "expandButton_f9n8",
        he = "expandButtonIcon_kYgG";
      function pe({ toggleSidebar: e }) {
        return (0, h.jsx)("div", {
          className: me,
          title: (0, c.T)({
            id: "theme.docs.sidebar.expandButtonTitle",
            message: "Expand sidebar",
            description:
              "The ARIA label and title attribute for expand button of doc sidebar",
          }),
          "aria-label": (0, c.T)({
            id: "theme.docs.sidebar.expandButtonAriaLabel",
            message: "Expand sidebar",
            description:
              "The ARIA label and title attribute for expand button of doc sidebar",
          }),
          tabIndex: 0,
          role: "button",
          onKeyDown: e,
          onClick: e,
          children: (0, h.jsx)(C, { className: he }),
        });
      }
      const xe = {
        docSidebarContainer: "docSidebarContainer_ab80",
        docSidebarContainerHidden: "docSidebarContainerHidden_vCP6",
        sidebarViewport: "sidebarViewport_uIPh",
      };
      function _e({ children: e }) {
        const t = (0, r.t)();
        return (0, h.jsx)(a.Fragment, { children: e }, t?.name ?? "noSidebar");
      }
      function fe({
        sidebar: e,
        hiddenSidebarContainer: t,
        setHiddenSidebarContainer: n,
      }) {
        const { pathname: s } = (0, _.zy)(),
          [l, r] = (0, a.useState)(!1),
          c = (0, a.useCallback)(() => {
            (l && r(!1), !l && (0, x.O)() && r(!0), n((e) => !e));
          }, [n, l]);
        return (0, h.jsx)("aside", {
          className: (0, i.A)(
            o.G.docs.docSidebarContainer,
            xe.docSidebarContainer,
            t && xe.docSidebarContainerHidden,
          ),
          onTransitionEnd: (e) => {
            e.currentTarget.classList.contains(xe.docSidebarContainer) &&
              t &&
              r(!0);
          },
          children: (0, h.jsx)(_e, {
            children: (0, h.jsxs)("div", {
              className: (0, i.A)(
                xe.sidebarViewport,
                l && xe.sidebarViewportHidden,
              ),
              children: [
                (0, h.jsx)(be, {
                  sidebar: e,
                  path: s,
                  onCollapse: c,
                  isHidden: l,
                }),
                l && (0, h.jsx)(pe, { toggleSidebar: c }),
              ],
            }),
          }),
        });
      }
      const je = {
        docMainContainer: "docMainContainer_LEC8",
        docMainContainerEnhanced: "docMainContainerEnhanced_ntP9",
        docItemWrapperEnhanced: "docItemWrapperEnhanced_UMV3",
      };
      function ve({ hiddenSidebarContainer: e, children: t }) {
        const n = (0, r.t)();
        return (0, h.jsx)("main", {
          className: (0, i.A)(
            je.docMainContainer,
            (e || !n) && je.docMainContainerEnhanced,
          ),
          children: (0, h.jsx)("div", {
            className: (0, i.A)(
              "container padding-top--md padding-bottom--lg",
              je.docItemWrapper,
              e && je.docItemWrapperEnhanced,
            ),
            children: t,
          }),
        });
      }
      const Ce = "docRoot_afC2",
        ge = "docsWrapper_FfM_";
      function Ae({ children: e }) {
        const t = (0, r.t)(),
          [n, i] = (0, a.useState)(!1);
        return (0, h.jsxs)("div", {
          className: ge,
          children: [
            (0, h.jsx)(p, {}),
            (0, h.jsxs)("div", {
              className: Ce,
              children: [
                t &&
                  (0, h.jsx)(fe, {
                    sidebar: t.items,
                    hiddenSidebarContainer: n,
                    setHiddenSidebarContainer: i,
                  }),
                (0, h.jsx)(ve, { hiddenSidebarContainer: n, children: e }),
              ],
            }),
          ],
        });
      }
      var ke = n(4185);
      function Se(e) {
        const t = (0, l.B5)(e);
        if (!t) return (0, h.jsx)(ke.A, {});
        const { docElement: n, sidebarName: a, sidebarItems: c } = t;
        return (0, h.jsx)(s.e3, {
          className: (0, i.A)(o.G.page.docsDocPage),
          children: (0, h.jsx)(r.V, {
            name: a,
            items: c,
            children: (0, h.jsx)(Ae, { children: n }),
          }),
        });
      }
    },
  },
]);
