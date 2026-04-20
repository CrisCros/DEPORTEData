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

export type ToxicKeyword = {
  word: string;
  categories: string[];
};

export type ChatResponse = {
  message: string;
  has_toxic: boolean;
  key_words_toxic_classification: ToxicKeyword[];
};

export type LoginResponse = {
  name: string;
  username: string;
  role: string;
  token: string;
};

export type UsageEvent = {
  id_event: number;
  event_type: string;
  page?: string | null;
  username_user?: string | null;
  user_role?: string | null;
  created_at: string;
};

export type UsageEventTypeCount = {
  event_type: string;
  count: number;
};

export type UsageSummary = {
  total_events: number;
  events_24h: number;
  events_7d: number;
  unique_actors: number;
  chat_messages_7d: number;
  admin_page_views_7d: number;
  by_type: UsageEventTypeCount[];
  recent_events: UsageEvent[];
};

import { appConfig } from '../config';

const rawBaseUrl = appConfig.apiBaseUrl || (import.meta.env.VITE_API_BASE_URL as string | undefined);
const normalizedBaseUrl = rawBaseUrl?.replace(/\/+$/, '');

const DEFAULT_API_BASE_URL = '/api';
const STORAGE_TOKEN_KEY = 'deportedata-admin-token';

const baseUrl = normalizedBaseUrl && /^https?:\/\//.test(normalizedBaseUrl)
  ? normalizedBaseUrl
  : DEFAULT_API_BASE_URL;

function authHeaders(): Record<string, string> {
  const token = window.localStorage.getItem(STORAGE_TOKEN_KEY);
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function requestJson<T>(path: string, init?: RequestInit, options?: { auth?: boolean }): Promise<T> {
  const method = init?.method?.toUpperCase() ?? 'GET';
  const hasBody = init?.body !== undefined;

  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      ...(hasBody || method !== 'GET' ? { 'Content-Type': 'application/json' } : {}),
      ...(options?.auth ? authHeaders() : {}),
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

async function requestEmpty(path: string, init?: RequestInit): Promise<void> {
  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      ...(init?.body !== undefined ? { 'Content-Type': 'application/json' } : {}),
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Request failed with status ${response.status}`);
  }
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

export const authApi = {
  login: (username: string, password: string) =>
    requestJson<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
};

export const usageApi = {
  track: async (event_type: string, page?: string, metadata: Record<string, unknown> = {}) => {
    try {
      await requestEmpty('/usage/events', {
        method: 'POST',
        body: JSON.stringify({ event_type, page, metadata }),
      });
    } catch {
      // La telemetria de uso no debe romper la experiencia principal.
    }
  },
  getSummary: () => requestJson<UsageSummary>('/admin/usage/summary', undefined, { auth: true }),
};
