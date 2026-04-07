import { Card, Group, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Activity, ShieldCheck, UserRound } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { DashboardEmbed } from '../../components/DashboardEmbed';

const adminHomeUrl = import.meta.env.VITE_ADMIN_HOME_DASHBOARD_URL;

export function AdminHomePage() {
  const { t } = useTranslation();
  const stats = [
    { label: 'Latencia media', value: '214 ms', icon: Activity },
    { label: 'Eventos de seguridad', value: '03', icon: ShieldCheck },
    { label: 'Sesiones activas', value: '128', icon: UserRound },
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
