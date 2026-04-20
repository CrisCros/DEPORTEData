import { Alert, Badge, Button, Card, Group, Progress, SimpleGrid, Stack, Table, Text, ThemeIcon, Title } from '@mantine/core';
import { Activity, BarChart3, Bot, Clock3, Eye, MousePointerClick, RefreshCw, Users } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { type UsageEvent, type UsageSummary, usageApi } from '../../services/api';

const EVENT_LABEL_KEYS: Record<string, string> = {
  public_page_view: 'eventPublicPageView',
  admin_page_view: 'eventAdminPageView',
  login_success: 'eventLoginSuccess',
  chat_message_sent: 'eventChatMessageSent',
};

function formatEventName(eventType: string, t: (key: string) => string) {
  const labelKey = EVENT_LABEL_KEYS[eventType];
  return labelKey ? t(labelKey) : eventType.replace(/_/g, ' ');
}

function formatDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function eventActor(event: UsageEvent, anonymousLabel: string) {
  if (event.username_user) {
    return event.user_role ? `${event.username_user} (${event.user_role})` : event.username_user;
  }

  return anonymousLabel;
}

export function UsagePage() {
  const { t } = useTranslation();
  const [summary, setSummary] = useState<UsageSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadSummary = async () => {
    setLoading(true);
    try {
      const response = await usageApi.getSummary();
      setSummary(response);
      setError(null);
    } catch (err) {
      const details = err instanceof Error ? err.message : t('unknownError');
      setError(`${t('usageLoadError')} ${details}`);
      setSummary(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin/uso', { section: 'usage' });
    void loadSummary();
  }, []);

  const totalForChart = Math.max(...(summary?.by_type.map((item) => item.count) ?? [0]), 1);

  const stats = [
    { label: t('totalEvents'), value: summary?.total_events, icon: BarChart3, color: 'blue' },
    { label: t('events24h'), value: summary?.events_24h, icon: Activity, color: 'cyan' },
    { label: t('events7d'), value: summary?.events_7d, icon: MousePointerClick, color: 'lime' },
    { label: t('uniqueActors'), value: summary?.unique_actors, icon: Users, color: 'teal' },
    { label: t('adminVisits7d'), value: summary?.admin_page_views_7d, icon: Eye, color: 'indigo' },
    { label: t('chatQuestions7d'), value: summary?.chat_messages_7d, icon: Bot, color: 'grape' },
  ];

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="flex-start">
        <div>
          <Title order={1}>{t('usageTitle')}</Title>
          <Text c="dimmed">{t('usageDescription')}</Text>
        </div>
        <Button
          leftSection={<RefreshCw size={16} aria-hidden="true" />}
          loading={loading}
          onClick={() => void loadSummary()}
          variant="default"
        >
          {t('refresh')}
        </Button>
      </Group>

      {error ? (
        <Alert color="red" title={t('usageLoadErrorTitle')}>
          {error}
        </Alert>
      ) : null}

      <SimpleGrid cols={{ base: 1, sm: 2, xl: 3 }} spacing="lg">
        {stats.map((item) => {
          const Icon = item.icon;
          return (
            <Card key={item.label} p="lg" className="admin-stat">
              <Group justify="space-between">
                <div>
                  <Text size="xs" tt="uppercase" fw={700} c="dimmed">{item.label}</Text>
                  <Title order={2}>{item.value ?? (loading ? '...' : '0')}</Title>
                </div>
                <ThemeIcon color={item.color} variant="light" radius="xl" size="xl">
                  <Icon size={20} aria-hidden="true" />
                </ThemeIcon>
              </Group>
            </Card>
          );
        })}
      </SimpleGrid>

      <SimpleGrid cols={{ base: 1, lg: 2 }} spacing="lg">
        <Card p="lg" className="admin-stat">
          <Group justify="space-between" mb="md">
            <div>
              <Title order={3}>{t('eventsByType')}</Title>
              <Text c="dimmed" size="sm">{t('eventsByTypeDescription')}</Text>
            </div>
            <ThemeIcon color="blue" variant="light" radius="xl" size="lg">
              <Clock3 size={18} aria-hidden="true" />
            </ThemeIcon>
          </Group>

          <Stack gap="md">
            {(summary?.by_type ?? []).length > 0 ? (
              summary?.by_type.map((item) => (
                <div key={item.event_type}>
                  <Group justify="space-between" mb={6}>
                    <Text fw={700} size="sm">{formatEventName(item.event_type, t)}</Text>
                    <Badge color="blue" variant="light">{item.count}</Badge>
                  </Group>
                  <Progress value={(item.count / totalForChart) * 100} radius="xl" />
                </div>
              ))
            ) : (
              <Text c="dimmed" size="sm">{t('noEventsYet')}</Text>
            )}
          </Stack>
        </Card>

        <Card p="lg" className="admin-stat">
          <Title order={3} mb="md">{t('whatIsTracked')}</Title>
          <Stack gap="sm">
            <Text size="sm"><Badge mr="xs" color="cyan" variant="light">public_page_view</Badge> {t('publicPageViewDescription')}</Text>
            <Text size="sm"><Badge mr="xs" color="indigo" variant="light">admin_page_view</Badge> {t('adminPageViewDescription')}</Text>
            <Text size="sm"><Badge mr="xs" color="teal" variant="light">login_success</Badge> {t('loginSuccessDescription')}</Text>
            <Text size="sm"><Badge mr="xs" color="grape" variant="light">chat_message_sent</Badge> {t('chatMessageDescription')}</Text>
          </Stack>
        </Card>
      </SimpleGrid>

      <Card p="lg" className="admin-stat">
        <Group justify="space-between" mb="md">
          <div>
            <Title order={3}>{t('recentEvents')}</Title>
            <Text c="dimmed" size="sm">{t('recentEventsDescription')}</Text>
          </div>
          <Badge color="cyan" variant="light">{summary?.recent_events.length ?? 0} {t('visible')}</Badge>
        </Group>
        <Table.ScrollContainer minWidth={620}>
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>{t('event')}</Table.Th>
                <Table.Th>{t('page')}</Table.Th>
                <Table.Th>{t('user')}</Table.Th>
                <Table.Th>{t('date')}</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {(summary?.recent_events ?? []).length > 0 ? (
                summary?.recent_events.map((event) => (
                  <Table.Tr key={event.id_event}>
                    <Table.Td>
                      <Badge color="blue" radius="sm" variant="light">{formatEventName(event.event_type, t)}</Badge>
                    </Table.Td>
                    <Table.Td>{event.page ?? '-'}</Table.Td>
                    <Table.Td>{eventActor(event, t('anonymous'))}</Table.Td>
                    <Table.Td>{formatDate(event.created_at)}</Table.Td>
                  </Table.Tr>
                ))
              ) : (
                <Table.Tr>
                  <Table.Td colSpan={4}>
                    <Text c="dimmed" size="sm">{t('noRecentEvents')}</Text>
                  </Table.Td>
                </Table.Tr>
              )}
            </Table.Tbody>
          </Table>
        </Table.ScrollContainer>
      </Card>
    </Stack>
  );
}
