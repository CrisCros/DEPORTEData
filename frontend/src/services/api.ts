export type DashboardPoint = {
  year: number;
  value: number;
};

export type DashboardSeries = DashboardPoint[];

export type DashboardKpis = {
  empleo_total: number;
  growth_pct: number;
  latest_year: number;
  latest_values: DashboardPoint[];
};

export type ChatResponse = {
  message: string;
  answer: string;
};

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL as string | undefined;
const normalizedBaseUrl = rawBaseUrl?.replace(/\/+$/, '');

const DEFAULT_API_BASE_URL = '/api';

const baseUrl = normalizedBaseUrl && /^https?:\/\//.test(normalizedBaseUrl)
  ? normalizedBaseUrl
  : DEFAULT_API_BASE_URL;

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const method = init?.method?.toUpperCase() ?? 'GET';
  const hasBody = init?.body !== undefined;

  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      ...(hasBody || method !== 'GET' ? { 'Content-Type': 'application/json' } : {}),
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const dashboardApi = {
  getKpis: () => requestJson<DashboardKpis>('/dashboard/kpis'),
  getSeries: () => requestJson<DashboardSeries>('/dashboard/series'),
};

export const chatApi = {
  sendMessage: (message: string) =>
    requestJson<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    }),
};
