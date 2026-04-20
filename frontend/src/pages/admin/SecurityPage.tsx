import { Card, Group, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Eye, ShieldAlert, ShieldCheck } from 'lucide-react';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { DashboardEmbed } from '../../components/DashboardEmbed';
import { appConfig } from '../../config';
import { usageApi } from '../../services/api';

const securityUrl = appConfig.adminSecurityDashboardUrl;

export function SecurityPage() {
  const { t } = useTranslation();

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin/seguridad', { section: 'security' });
  }, []);

  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>{t('securityTitle')}</Title>
        <Text c="dimmed">{t('securityDescription')}</Text>
      </div>
      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg">
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">{t('securityOpenAlerts')}</Text>
              <Title order={2}>06</Title>
            </div>
            <ThemeIcon color="red" variant="light" radius="xl" size="xl">
              <ShieldAlert size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">{t('securityReviews')}</Text>
              <Title order={2}>18</Title>
            </div>
            <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
              <Eye size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">{t('securityControlsOk')}</Text>
              <Title order={2}>92%</Title>
            </div>
            <ThemeIcon color="teal" variant="light" radius="xl" size="xl">
              <ShieldCheck size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
      </SimpleGrid>
      <DashboardEmbed src={securityUrl} title={t('securityTitle')} description={t('securityPanelDescription')} />
    </Stack>
  );
}
