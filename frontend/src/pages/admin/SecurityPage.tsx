import { Card, Group, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Eye, ShieldAlert, ShieldCheck } from 'lucide-react';
import { useEffect } from 'react';
import { DashboardEmbed } from '../../components/DashboardEmbed';
import { appConfig } from '../../config';
import { usageApi } from '../../services/api';

const securityUrl = appConfig.adminSecurityDashboardUrl;

export function SecurityPage() {
  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin/seguridad', { section: 'security' });
  }, []);

  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>Seguridad</Title>
        <Text c="dimmed">Vista placeholder para paneles internos relacionados con alertas, accesos y auditoria.</Text>
      </div>
      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg">
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Alertas abiertas</Text>
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
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Revisiones</Text>
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
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Controles OK</Text>
              <Title order={2}>92%</Title>
            </div>
            <ThemeIcon color="teal" variant="light" radius="xl" size="xl">
              <ShieldCheck size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
      </SimpleGrid>
      <DashboardEmbed src={securityUrl} title="Seguridad" description="Panel de controles y eventos de seguridad." />
    </Stack>
  );
}
