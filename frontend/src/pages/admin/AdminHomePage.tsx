import { Card, Group, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Activity, ShieldCheck, UserRound } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { DashboardEmbed } from '../../components/DashboardEmbed';
import { appConfig } from '../../config';
import { type UsageSummary, usageApi } from '../../services/api';

const adminHomeUrl = appConfig.adminHomeDashboardUrl;

export function AdminHomePage() {
  const { t } = useTranslation();
  const [summary, setSummary] = useState<UsageSummary | null>(null);

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin', { section: 'home' });
    usageApi.getSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  const stats = [
    { label: 'Eventos 24h', value: summary ? String(summary.events_24h) : '...', icon: Activity },
    { label: 'Eventos 7 dias', value: summary ? String(summary.events_7d) : '...', icon: ShieldCheck },
    { label: 'Actores unicos', value: summary ? String(summary.unique_actors) : '...', icon: UserRound },
  ];

  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>{t('adminWelcome')}</Title>
        <Text c="dimmed">{t('adminSummary')}</Text>
      </div>

      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg">
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

      <DashboardEmbed src={adminHomeUrl} title={t('navHome')} description={t('adminSummary')} />
    </Stack>
  );
}
