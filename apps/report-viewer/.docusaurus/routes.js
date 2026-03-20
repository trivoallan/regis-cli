import React from "react";
import ComponentCreator from "@docusaurus/ComponentCreator";

export default [
  {
    path: "/__docusaurus/debug",
    component: ComponentCreator("/__docusaurus/debug", "5ff"),
    exact: true,
  },
  {
    path: "/__docusaurus/debug/config",
    component: ComponentCreator("/__docusaurus/debug/config", "5ba"),
    exact: true,
  },
  {
    path: "/__docusaurus/debug/content",
    component: ComponentCreator("/__docusaurus/debug/content", "a2b"),
    exact: true,
  },
  {
    path: "/__docusaurus/debug/globalData",
    component: ComponentCreator("/__docusaurus/debug/globalData", "c3c"),
    exact: true,
  },
  {
    path: "/__docusaurus/debug/metadata",
    component: ComponentCreator("/__docusaurus/debug/metadata", "156"),
    exact: true,
  },
  {
    path: "/__docusaurus/debug/registry",
    component: ComponentCreator("/__docusaurus/debug/registry", "88c"),
    exact: true,
  },
  {
    path: "/__docusaurus/debug/routes",
    component: ComponentCreator("/__docusaurus/debug/routes", "000"),
    exact: true,
  },
  {
    path: "/",
    component: ComponentCreator("/", "a3d"),
    routes: [
      {
        path: "/",
        component: ComponentCreator("/", "1d3"),
        routes: [
          {
            path: "/",
            component: ComponentCreator("/", "1f0"),
            routes: [
              {
                path: "/playbook",
                component: ComponentCreator("/playbook", "8ae"),
                exact: true,
                sidebar: "defaultSidebar",
              },
              {
                path: "/rules",
                component: ComponentCreator("/rules", "f47"),
                exact: true,
                sidebar: "defaultSidebar",
              },
              {
                path: "/",
                component: ComponentCreator("/", "87e"),
                exact: true,
                sidebar: "defaultSidebar",
              },
            ],
          },
        ],
      },
    ],
  },
  {
    path: "*",
    component: ComponentCreator("*"),
  },
];
