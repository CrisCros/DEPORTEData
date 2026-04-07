import { Card, Group, SimpleGrid, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { Clock3, MousePointerClick, Users } from 'lucide-react';
import { DashboardEmbed } from '../../components/DashboardEmbed';

const usageUrl = import.meta.env.VITE_ADMIN_USAGE_DASHBOARD_URL;

export function UsagePage() {
  return (
    <Stack gap="lg">
      <div>
        <Title order={1}>Uso</Title>
        <Text c="dimmed">Vista preparada para paneles de adopcion, sesiones y consumo de funcionalidades.</Text>
      </div>
      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg">
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Usuarios semanales</Text>
              <Title order={2}>2.4k</Title>
            </div>
            <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
              <Users size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">CTR acciones</Text>
              <Title order={2}>31%</Title>
            </div>
            <ThemeIcon color="lime" variant="light" radius="xl" size="xl">
              <MousePointerClick size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Tiempo medio</Text>
              <Title order={2}>08:42</Title>
            </div>
            <ThemeIcon color="grape" variant="light" radius="xl" size="xl">
              <Clock3 size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
      </SimpleGrid>
      <DashboardEmbed src={usageUrl} title="Uso" description="Panel de uso y comportamiento de la plataforma." />
    </Stack>
  );
}
