import { Alert, Badge, Card, Group, Progress, SimpleGrid, Stack, Table, Text, ThemeIcon, Title } from '@mantine/core';
import { AlertTriangle, Hash, MessageSquareWarning, ShieldAlert } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { type ToxicEvent, type UsageSummary, usageApi } from '../../services/api';

function formatDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function actor(event: ToxicEvent, anonymousLabel: string) {
  if (event.username_user) {
    return event.user_role ? `${event.username_user} (${event.user_role})` : event.username_user;
  }

  return anonymousLabel;
}

function toxicWordsLabel(event: ToxicEvent, fallback: string) {
  const words = event.toxic_words
    .map((item) => item.word)
    .filter(Boolean);

  return words.length ? words.join(', ') : fallback;
}

function categoriesLabel(event: ToxicEvent) {
  const categories = new Set<string>();
  event.toxic_words.forEach((item) => {
    item.categories.forEach((category) => categories.add(category));
  });

  return categories.size ? Array.from(categories).join(', ') : '-';
}

export function InsultsPage() {
  const { t } = useTranslation();
  const [summary, setSummary] = useState<UsageSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin/insultos', { section: 'insults' });
    usageApi.getSummary().then((response) => {
      setSummary(response);
      setError(null);
    }).catch((err) => {
      const details = err instanceof Error ? err.message : t('unknownError');
      setError(`${t('usageLoadError')} ${details}`);
      setSummary(null);
    });
  }, []);

  const toxicity = summary?.toxicity;
  const totalForCategories = Math.max(...(toxicity?.by_category.map((item) => item.count) ?? [0]), 1);
  const totalForWords = Math.max(...(toxicity?.by_word.map((item) => item.count) ?? [0]), 1);

  const stats = [
    { label: t('toxicMessagesTotal'), value: toxicity?.total, icon: ShieldAlert, color: 'red' },
    { label: t('toxicMessages24h'), value: toxicity?.toxic_24h, icon: AlertTriangle, color: 'orange' },
    { label: t('toxicMessages7d'), value: toxicity?.toxic_7d, icon: MessageSquareWarning, color: 'grape' },
    { label: t('toxicWordsDetected'), value: toxicity?.by_word.length, icon: Hash, color: 'cyan' },
  ];

  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>{t('insultsTitle')}</Title>
        <Text c="dimmed">{t('insultsDescription')}</Text>
      </div>

      {error ? (
        <Alert color="red" title={t('usageLoadErrorTitle')}>
          {error}
        </Alert>
      ) : null}

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

      <SimpleGrid cols={{ base: 1, lg: 2 }} spacing="lg">
        <Card p="lg" className="admin-stat">
          <Title order={3}>{t('insultTypes')}</Title>
          <Text c="dimmed" size="sm" mb="lg">{t('insultTypesDescription')}</Text>
          <Stack gap="md">
            {(toxicity?.by_category ?? []).length > 0 ? (
              toxicity?.by_category.map((item) => (
                <div key={item.category}>
                  <Group justify="space-between" mb={6}>
                    <Text fw={700} size="sm">{item.category}</Text>
                    <Badge color="red" variant="light">{item.count}</Badge>
                  </Group>
                  <Progress color="red" value={(item.count / totalForCategories) * 100} radius="xl" />
                </div>
              ))
            ) : (
              <Text c="dimmed" size="sm">{t('noToxicMessages')}</Text>
            )}
          </Stack>
        </Card>

        <Card p="lg" className="admin-stat">
          <Title order={3}>{t('toxicWords')}</Title>
          <Text c="dimmed" size="sm" mb="lg">{t('toxicWordsDescription')}</Text>
          <Stack gap="md">
            {(toxicity?.by_word ?? []).length > 0 ? (
              toxicity?.by_word.slice(0, 12).map((item) => (
                <div key={item.word}>
                  <Group justify="space-between" mb={6}>
                    <Text fw={700} size="sm">{item.word}</Text>
                    <Badge color="grape" variant="light">{item.count}</Badge>
                  </Group>
                  <Progress color="grape" value={(item.count / totalForWords) * 100} radius="xl" />
                </div>
              ))
            ) : (
              <Text c="dimmed" size="sm">{t('noToxicMessages')}</Text>
            )}
          </Stack>
        </Card>
      </SimpleGrid>

      <Card p="lg" className="admin-stat">
        <Group justify="space-between" mb="md">
          <div>
            <Title order={3}>{t('recentToxicMessages')}</Title>
            <Text c="dimmed" size="sm">{t('recentToxicMessagesDescription')}</Text>
          </div>
          <Badge color="red" variant="light">{toxicity?.recent_events.length ?? 0} {t('visible')}</Badge>
        </Group>
        <Table.ScrollContainer minWidth={860}>
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>{t('word')}</Table.Th>
                <Table.Th>{t('categories')}</Table.Th>
                <Table.Th>{t('messageLength')}</Table.Th>
                <Table.Th>{t('user')}</Table.Th>
                <Table.Th>{t('sourceIp')}</Table.Th>
                <Table.Th>{t('date')}</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {(toxicity?.recent_events ?? []).length > 0 ? (
                toxicity?.recent_events.map((event) => (
                  <Table.Tr key={event.id_event}>
                    <Table.Td>
                      <Badge color="red" radius="sm" variant="light">
                        {toxicWordsLabel(event, t('classifierOnly'))}
                      </Badge>
                    </Table.Td>
                    <Table.Td>{categoriesLabel(event)}</Table.Td>
                    <Table.Td>{event.message_length}</Table.Td>
                    <Table.Td>{actor(event, t('anonymous'))}</Table.Td>
                    <Table.Td>{event.ip_address ?? '-'}</Table.Td>
                    <Table.Td>{formatDate(event.created_at)}</Table.Td>
                  </Table.Tr>
                ))
              ) : (
                <Table.Tr>
                  <Table.Td colSpan={6}>
                    <Text c="dimmed" size="sm">{t('noToxicMessages')}</Text>
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
