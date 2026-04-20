import { Card, Group, SimpleGrid, Stack, Table, Text, ThemeIcon, Title } from '@mantine/core';
import { Clock3, MousePointerClick, Users } from 'lucide-react';
import { useEffect, useState } from 'react';
import { DashboardEmbed } from '../../components/DashboardEmbed';
import { appConfig } from '../../config';
import { type UsageSummary, usageApi } from '../../services/api';

const usageUrl = appConfig.adminUsageDashboardUrl;

export function UsagePage() {
  const [summary, setSummary] = useState<UsageSummary | null>(null);

  useEffect(() => {
    void usageApi.track('admin_page_view', '/admin/uso', { section: 'usage' });
    usageApi.getSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

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
              <Title order={2}>{summary ? summary.unique_actors : '...'}</Title>
            </div>
            <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
              <Users size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Eventos 7 dias</Text>
              <Title order={2}>{summary ? summary.events_7d : '...'}</Title>
            </div>
            <ThemeIcon color="lime" variant="light" radius="xl" size="xl">
              <MousePointerClick size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
        <Card p="lg" className="admin-stat">
          <Group justify="space-between">
            <div>
              <Text size="xs" tt="uppercase" fw={700} c="dimmed">Preguntas chat 7 dias</Text>
              <Title order={2}>{summary ? summary.chat_messages_7d : '...'}</Title>
            </div>
            <ThemeIcon color="grape" variant="light" radius="xl" size="xl">
              <Clock3 size={20} aria-hidden="true" />
            </ThemeIcon>
          </Group>
        </Card>
      </SimpleGrid>
      <Card p="lg" className="admin-stat">
        <Title order={3} mb="md">Eventos recientes</Title>
        <Table.ScrollContainer minWidth={620}>
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Evento</Table.Th>
                <Table.Th>Pagina</Table.Th>
                <Table.Th>Usuario</Table.Th>
                <Table.Th>Fecha</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {(summary?.recent_events ?? []).map((event) => (
                <Table.Tr key={event.id_event}>
                  <Table.Td>{event.event_type}</Table.Td>
                  <Table.Td>{event.page ?? '-'}</Table.Td>
                  <Table.Td>{event.username_user ?? 'anonimo'}</Table.Td>
                  <Table.Td>{new Date(event.created_at).toLocaleString()}</Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        </Table.ScrollContainer>
      </Card>
      <DashboardEmbed src={usageUrl} title="Uso" description="Panel de uso y comportamiento de la plataforma." />
    </Stack>
  );
}
