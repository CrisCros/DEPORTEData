import { Card, Group, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Activity, Cpu, Waves } from 'lucide-react';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { DashboardEmbed } from '../../components/DashboardEmbed';
import { appConfig } from '../../config';
import { usageApi } from '../../services/api';

const telemetryUrl = appConfig.adminTelemetryDashboardUrl;

export function TelemetryPage() {
  const { t } = useTranslation();

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin/telemetrias', { section: 'telemetry' });
  }, []);

  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>{t('telemetryTitle')}</Title>
        <Text c="dimmed">{t('telemetryDescription')}</Text>
      </div>
      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg">
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">{t('telemetryCpu')}</Text>
              <Title order={2}>47%</Title>
            </div>
            <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
              <Cpu size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">{t('telemetryEventsMinute')}</Text>
              <Title order={2}>1.2k</Title>
            </div>
            <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
              <Activity size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">{t('telemetryBandwidth')}</Text>
              <Title order={2}>310 Mb/s</Title>
            </div>
            <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
              <Waves size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
      </SimpleGrid>
      <DashboardEmbed src={telemetryUrl} title={t('telemetryTitle')} description={t('telemetryPanelDescription')} />
    </Stack>
  );
}
