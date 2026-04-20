import { Badge, Card, Group, SimpleGrid, Stack, Table, Text, ThemeIcon, Title } from '@mantine/core';
import { Eye, Lock, ShieldAlert, ShieldCheck } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { type UsageEvent, type UsageSummary, usageApi } from '../../services/api';

function formatDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function actor(event: UsageEvent, anonymousLabel: string) {
  if (event.username_user) {
    return event.user_role ? `${event.username_user} (${event.user_role})` : event.username_user;
  }

  return anonymousLabel;
}

export function SecurityPage() {
  const { t } = useTranslation();
  const [summary, setSummary] = useState<UsageSummary | null>(null);

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin/seguridad', { section: 'security' });
    usageApi.getSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  const loginSuccess = summary?.by_type.find((item) => item.event_type === 'login_success')?.count ?? 0;
  const privateEvents = (summary?.recent_events ?? []).filter((event) =>
    event.event_type === 'login_success' || event.page?.startsWith('/admin'),
  );

  const stats = [
    { label: t('successfulLogins'), value: loginSuccess, icon: Lock, color: 'teal' },
    { label: t('privateAreaVisits'), value: summary?.admin_page_views_7d, icon: Eye, color: 'cyan' },
    { label: t('trackedSecurityEvents'), value: privateEvents.length, icon: ShieldCheck, color: 'green' },
    { label: t('securityOpenAlerts'), value: 0, icon: ShieldAlert, color: 'red' },
  ];

  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>{t('securityTitle')}</Title>
        <Text c="dimmed">{t('securityAccessDescription')}</Text>
      </div>

      <SimpleGrid cols={{ base: 1, sm: 2, xl: 4 }} spacing="lg">
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

      <Card p="lg" className="admin-stat">
        <Group justify="space-between" mb="md">
          <div>
            <Title order={3}>{t('recentPrivateActivity')}</Title>
            <Text c="dimmed" size="sm">{t('recentPrivateActivityDescription')}</Text>
          </div>
          <Badge color="cyan" variant="light">{privateEvents.length} {t('visible')}</Badge>
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
              {privateEvents.length > 0 ? (
                privateEvents.map((event) => (
                  <Table.Tr key={event.id_event}>
                    <Table.Td>
                      <Badge color="blue" radius="sm" variant="light">{event.event_type.replace(/_/g, ' ')}</Badge>
                    </Table.Td>
                    <Table.Td>{event.page ?? '-'}</Table.Td>
                    <Table.Td>{actor(event, t('anonymous'))}</Table.Td>
                    <Table.Td>{formatDate(event.created_at)}</Table.Td>
                  </Table.Tr>
                ))
              ) : (
                <Table.Tr>
                  <Table.Td colSpan={4}>
                    <Text c="dimmed" size="sm">{t('noPrivateEvents')}</Text>
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
