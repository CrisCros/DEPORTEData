import { Badge, Card, Group, Progress, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Activity, BarChart3, Bot, Gauge, MousePointerClick, Users } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { type UsageSummary, usageApi } from '../../services/api';

const EVENT_LABEL_KEYS: Record<string, string> = {
  public_page_view: 'eventPublicPageView',
  admin_page_view: 'eventAdminPageView',
  login_success: 'eventLoginSuccess',
  chat_message_sent: 'eventChatMessageSent',
};

function eventLabel(eventType: string, t: (key: string) => string) {
  const key = EVENT_LABEL_KEYS[eventType];
  return key ? t(key) : eventType.replace(/_/g, ' ');
}

export function TelemetryPage() {
  const { t } = useTranslation();
  const [summary, setSummary] = useState<UsageSummary | null>(null);

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin/telemetrias', { section: 'telemetry' });
    usageApi.getSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  const totalForChart = Math.max(...(summary?.by_type.map((item) => item.count) ?? [0]), 1);
  const publicVisits = summary?.by_type.find((item) => item.event_type === 'public_page_view')?.count ?? 0;

  const stats = [
    { label: t('registeredEvents'), value: summary?.total_events, icon: BarChart3, color: 'blue' },
    { label: t('events24h'), value: summary?.events_24h, icon: Activity, color: 'cyan' },
    { label: t('events7d'), value: summary?.events_7d, icon: MousePointerClick, color: 'lime' },
    { label: t('uniqueActors'), value: summary?.unique_actors, icon: Users, color: 'teal' },
    { label: t('publicNavigation'), value: publicVisits, icon: Gauge, color: 'indigo' },
    { label: t('chatQuestions7d'), value: summary?.chat_messages_7d, icon: Bot, color: 'grape' },
  ];

  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>{t('telemetryTitle')}</Title>
        <Text c="dimmed">{t('operationalTelemetryDescription')}</Text>
      </div>

      <SimpleGrid cols={{ base: 1, sm: 2, xl: 3 }} spacing="lg">
        {stats.map((item) => {
          const Icon = item.icon;
          return (
            <Card key={item.label} p="lg" className="admin-stat">
              <Group justify="space-between">
                <div>
                  <Text size="xs" tt="uppercase" fw={700} c="dimmed">{item.label}</Text>
                  <Title order={2}>{item.value ?? '...'}</Title>
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
          <Title order={3}>{t('interactionMix')}</Title>
          <Text c="dimmed" size="sm" mb="lg">{t('interactionMixDescription')}</Text>
          <Stack gap="md">
            {(summary?.by_type ?? []).length > 0 ? (
              summary?.by_type.map((item) => (
                <div key={item.event_type}>
                  <Group justify="space-between" mb={6}>
                    <Text fw={700} size="sm">{eventLabel(item.event_type, t)}</Text>
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
          <Title order={3}>{t('platformActivity')}</Title>
          <Text c="dimmed" size="sm" mb="lg">{t('platformActivityDescription')}</Text>
          <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="md">
            <Card withBorder radius="md" p="md">
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">{t('adminNavigation')}</Text>
              <Title order={3}>{summary?.admin_page_views_7d ?? '...'}</Title>
            </Card>
            <Card withBorder radius="md" p="md">
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">{t('chatQuestions7d')}</Text>
              <Title order={3}>{summary?.chat_messages_7d ?? '...'}</Title>
            </Card>
          </SimpleGrid>
        </Card>
      </SimpleGrid>
    </Stack>
  );
}
