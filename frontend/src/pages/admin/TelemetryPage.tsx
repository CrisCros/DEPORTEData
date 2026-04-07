import { Card, Group, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Activity, Cpu, Waves } from 'lucide-react';
import { DashboardEmbed } from '../../components/DashboardEmbed';

const telemetryUrl = import.meta.env.VITE_ADMIN_TELEMETRY_DASHBOARD_URL;

export function TelemetryPage() {
  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>Telemetrias</Title>
        <Text c="dimmed">Vista preparada para incrustar paneles privados de Grafana orientados a observabilidad.</Text>
      </div>
      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg">
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">CPU media</Text>
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
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Eventos por min</Text>
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
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Ancho de banda</Text>
              <Title order={2}>310 Mb/s</Title>
            </div>
            <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
              <Waves size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
      </SimpleGrid>
      <DashboardEmbed src={telemetryUrl} title="Telemetrias" description="Panel de metricas tecnicas y operativas." />
    </Stack>
  );
}
