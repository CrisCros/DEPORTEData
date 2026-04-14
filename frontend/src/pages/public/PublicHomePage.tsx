import {
  Badge,
  Button,
  Grid,
  Group,
  Paper,
  SimpleGrid,
  Stack,
  Text,
  ThemeIcon,
  Title,
} from '@mantine/core';
import { Bot, Globe, LayoutDashboard } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ChatbotWidget } from '../../components/ChatbotWidget';
import { EmploymentLineChart } from '../../components/EmploymentLineChart';
import { type DashboardKpis, type DashboardSeries, dashboardApi } from '../../services/api';

export function PublicHomePage() {
  const { t } = useTranslation();
  const [kpis, setKpis] = useState<DashboardKpis | null>(null);
  const [series, setSeries] = useState<DashboardSeries | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [kpisResponse, seriesResponse] = await Promise.all([
          dashboardApi.getKpis(),
          dashboardApi.getSeries(),
        ]);
        setKpis(kpisResponse);
        setSeries(seriesResponse);
      } catch (err) {
        const details = err instanceof Error ? err.message : 'Error desconocido';
        setError(`No se pudieron cargar los datos del backend. ${details}`);
      }
    };

    void loadDashboard();
  }, []);

  const features = [
    {
      icon: LayoutDashboard,
      title: 'Dashboard conectado',
      text: 'Los KPIs y la gráfica ya usan datos reales provenientes de CSV procesados por FastAPI.',
    },
    {
      icon: Globe,
      title: 'Soporte multilenguaje',
      text: 'Cambio de idioma rápido para demos, usuarios internos y presentaciones.',
    },
    {
      icon: Bot,
      title: 'Asistente contextual',
      text: 'Chat integrado con el endpoint /chat para responder con métricas del dataset.',
    },
  ];

  return (
    <>
      <Grid gutter="lg" mb="xl" align="stretch">
        <Grid.Col span={{ base: 12, lg: 8 }}>
          <Paper p="xl" className="glass-card public-hero">
            <Stack gap="lg">
              <div>
                <Badge size="lg" radius="sm" variant="light" color="cyan">
                  Analítica deportiva unificada
                </Badge>
                <Title order={1} mt="md" maw={760} style={{ fontSize: 'clamp(2.4rem, 5vw, 4.4rem)', lineHeight: 1 }}>
                  {t('publicTitle')}
                </Title>
                <Text c="dimmed" size="lg" maw={620} mt="md">
                  {t('publicDescription')}
                </Text>
              </div>

              <Group>
                <Button component={Link} to="/admin/login" size="md">
                  Admin
                </Button>
              </Group>

              <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="md">
                <Paper p="lg" className="metric-card">
                  <Text size="xs" tt="uppercase" c="dimmed" fw={700}>
                    Empleo total ({kpis?.latest_year ?? '-'})
                  </Text>
                  <Title order={2} mt={6}>
                    {kpis ? `${kpis.empleo_total}k` : '...'}
                  </Title>
                </Paper>
                <Paper p="lg" className="metric-card">
                  <Text size="xs" tt="uppercase" c="dimmed" fw={700}>
                    Crecimiento anual
                  </Text>
                  <Title order={2} mt={6}>
                    {kpis ? `${kpis.growth_pct}%` : '...'}
                  </Title>
                </Paper>
                <Paper p="lg" className="metric-card">
                  <Text size="xs" tt="uppercase" c="dimmed" fw={700}>
                    Últimos valores
                  </Text>
                  <Title order={4} mt={6}>
                    {kpis ? kpis.latest_values.map((v) => `${v.year}:${v.value}`).join(' · ') : '...'}
                  </Title>
                </Paper>
              </SimpleGrid>
            </Stack>
          </Paper>
        </Grid.Col>
      </Grid>

      {error ? (
        <Paper p="md" mb="lg" withBorder>
          <Text c="red">{error}</Text>
        </Paper>
      ) : null}

      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg" mb="xl">
        {features.map((feature) => {
          const Icon = feature.icon;
          return (
            <Paper key={feature.title} p="xl" className="glass-card">
              <Stack gap="md">
                <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
                  <Icon size={20} aria-hidden="true" />
                </ThemeIcon>
                <div>
                  <Title order={3}>{feature.title}</Title>
                  <Text c="dimmed" mt="xs">
                    {feature.text}
                  </Text>
                </div>
              </Stack>
            </Paper>
          );
        })}
      </SimpleGrid>

      {series ? <EmploymentLineChart series={series} /> : null}

      <ChatbotWidget />
    </>
  );
}
