type RuntimeConfig = {
  VITE_API_BASE_URL?: string;
  VITE_GRAFANA_BASE_URL?: string;
  VITE_PUBLIC_DASHBOARD_URL?: string;
  VITE_ADMIN_HOME_DASHBOARD_URL?: string;
  VITE_ADMIN_TELEMETRY_DASHBOARD_URL?: string;
  VITE_ADMIN_SECURITY_DASHBOARD_URL?: string;
  VITE_ADMIN_USAGE_DASHBOARD_URL?: string;
  VITE_CHATBOT_URL?: string;
};

declare global {
  interface Window {
    __APP_CONFIG__?: RuntimeConfig;
  }
}

const runtimeConfig = window.__APP_CONFIG__ ?? {};

function readConfigValue(key: keyof RuntimeConfig): string {
  const runtimeValue = runtimeConfig[key];
  const buildValue = import.meta.env[key] as string | undefined;

  return runtimeValue || buildValue || '';
}

export const appConfig = {
  apiBaseUrl: readConfigValue('VITE_API_BASE_URL'),
  grafanaBaseUrl: readConfigValue('VITE_GRAFANA_BASE_URL'),
  publicDashboardUrl: readConfigValue('VITE_PUBLIC_DASHBOARD_URL'),
  adminHomeDashboardUrl: readConfigValue('VITE_ADMIN_HOME_DASHBOARD_URL'),
  adminTelemetryDashboardUrl: readConfigValue('VITE_ADMIN_TELEMETRY_DASHBOARD_URL'),
  adminSecurityDashboardUrl: readConfigValue('VITE_ADMIN_SECURITY_DASHBOARD_URL'),
  adminUsageDashboardUrl: readConfigValue('VITE_ADMIN_USAGE_DASHBOARD_URL'),
  chatbotUrl: readConfigValue('VITE_CHATBOT_URL'),
};
