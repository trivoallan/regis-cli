/**
 * Docusaurus Root wrapper — wraps the entire app in ReportProvider.
 *
 * Supports a `?report=<url>` query parameter to load a report from an
 * arbitrary URL. Falls back to the default `report.json` served alongside
 * the site when the parameter is absent.
 *
 * @see https://docusaurus.io/docs/swizzling#wrapper-your-site-with-root
 */

import React, { useEffect } from "react";
import { ReportProvider, useReport } from "@site/src/components/ReportProvider";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import { useLocation, useHistory } from "@docusaurus/router";

interface RootProps {
  children: React.ReactNode;
}

/**
 * Validate that a URL is safe to fetch (no file://, no private IPs, etc.).
 * Returns the URL string if valid, or null if rejected.
 */
function sanitizeExternalUrl(raw: string): string | null {
  try {
    const url = new URL(raw, window.location.origin);
    const blocked = ["file:", "javascript:", "data:", "blob:"];
    if (blocked.includes(url.protocol)) return null;
    // Block private/loopback IPs when not already on localhost
    if (window.location.hostname !== "localhost") {
      const host = url.hostname;
      if (
        host === "localhost" ||
        host === "127.0.0.1" ||
        host === "0.0.0.0" ||
        host.startsWith("10.") ||
        host.startsWith("192.168.") ||
        /^172\.(1[6-9]|2\d|3[01])\./.test(host)
      )
        return null;
    }
    return url.toString();
  } catch {
    return null;
  }
}

/**
 * Inner component that can consume useReport() from the provider.
 */
function RootContent({
  children,
}: {
  children: React.ReactNode;
}): React.JSX.Element {
  return <>{children}</>;
}

export default function Root({ children }: RootProps): React.JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  const { search } = useLocation();

  // 1. Determine the report URL to load
  // Order: 1. query param, 2. session storage, 3. default report.json
  const params = new URLSearchParams(search);
  const rawParamUrl = params.get("url");
  const paramUrl = rawParamUrl ? sanitizeExternalUrl(rawParamUrl) : null;

  // On client side, read from sessionStorage if param is missing
  const [activeReportUrl, setActiveReportUrl] = React.useState<string | null>(
    null,
  );

  // 2. Handle archive URL persistence
  const rawArchiveUrl = params.get("archive_url");
  const paramArchiveUrl = rawArchiveUrl
    ? sanitizeExternalUrl(rawArchiveUrl)
    : null;

  useEffect(() => {
    // Report persistence
    if (paramUrl) {
      sessionStorage.setItem("regis_active_url", paramUrl);
      setActiveReportUrl(paramUrl);
    } else {
      const savedReport = sessionStorage.getItem("regis_active_url");
      if (savedReport) setActiveReportUrl(savedReport);
    }

    // Archive persistence
    if (paramArchiveUrl) {
      sessionStorage.setItem("regis_active_archive_url", paramArchiveUrl);
    }
  }, [paramUrl, paramArchiveUrl]);

  const reportUrl =
    paramUrl || activeReportUrl || `${siteConfig.baseUrl}report.json`;

  return (
    <ReportProvider reportUrl={reportUrl}>
      <RootContent>{children}</RootContent>
    </ReportProvider>
  );
}
