import { Badge, Card, Group, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Activity, Bot, ShieldCheck, UserRound } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { type UsageSummary, usageApi } from '../../services/api';

const EVENT_LABEL_KEYS: Record<string, string> = {
  public_page_view: 'eventPublicPageView',
  admin_page_view: 'eventAdminPageView',
  login_success: 'eventLoginSuccess',
  chat_message_sent: 'eventChatMessageSent',
};

export function AdminHomePage() {
  const { t } = useTranslation();
  const [summary, setSummary] = useState<UsageSummary | null>(null);

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin', { section: 'home' });
    usageApi.getSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  const stats = [
    { label: t('events24h'), value: summary ? String(summary.events_24h) : '...', icon: Activity },
    { label: t('events7d'), value: summary ? String(summary.events_7d) : '...', icon: ShieldCheck },
    { label: t('uniqueActors'), value: summary ? String(summary.unique_actors) : '...', icon: UserRound },
    { label: t('chatQuestions7d'), value: summary ? String(summary.chat_messages_7d) : '...', icon: Bot },
  ];

  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>{t('adminWelcome')}</Title>
        <Text c="dimmed">{t('adminSummary')}</Text>
      </div>

      <SimpleGrid cols={{ base: 1, sm: 2, xl: 4 }} spacing="lg">
        {stats.map((item) => {
          const Icon = item.icon;
          return (
            <Card key={item.label} p="lg" className="admin-stat">
              <Group justify="space-between">
                <div>
                  <Text size="xs" tt="uppercase" fw={700} c="dimmed">
                    {item.label}
                  </Text>
                  <Title order={2} mt={8}>
                    {item.value}
                  </Title>
                </div>
                <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
                  <Icon size={20} aria-hidden="true" />
                </ThemeIcon>
              </Group>
            </Card>
          );
        })}
      </SimpleGrid>

      {summary?.by_type.length ? (
        <Card p="lg" className="admin-stat">
          <Group justify="space-between" mb="md">
            <div>
              <Title order={3}>{t('eventsByType')}</Title>
              <Text c="dimmed" size="sm">{t('eventsByTypeDescription')}</Text>
            </div>
            <Badge color="cyan" variant="light">{summary.total_events} {t('total')}</Badge>
          </Group>
          <Group gap="sm">
            {summary.by_type.slice(0, 6).map((item) => (
              <Badge key={item.event_type} color="blue" radius="sm" size="lg" variant="light">
                {EVENT_LABEL_KEYS[item.event_type] ? t(EVENT_LABEL_KEYS[item.event_type]) : item.event_type.replace(/_/g, ' ')}: {item.count}
              </Badge>
            ))}
          </Group>
        </Card>
      ) : null}
    </Stack>
  );
}
