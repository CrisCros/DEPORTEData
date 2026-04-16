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
import { DashboardEmbed } from '../../components/DashboardEmbed';
import { appConfig } from '../../config';
import { type DashboardKpis, type DashboardSeries, dashboardApi } from '../../services/api';

const grafanaBaseUrl = appConfig.grafanaBaseUrl || '/api/grafana/d-solo/adp79lb/principal';
const grafanaRange = 'orgId=1&from=1302878323442&to=1776263923442&timezone=browser&dtab=new-row';

function buildGrafanaPanelUrl(panelId: string) {
  if (appConfig.publicDashboardUrl) {
    if (appConfig.publicDashboardUrl.includes('panelId=')) {
      return appConfig.publicDashboardUrl.replace(/panelId=panel-\d+/, `panelId=${panelId}`);
    }

    const separator = appConfig.publicDashboardUrl.includes('?') ? '&' : '?';
    return `${appConfig.publicDashboardUrl}${separator}panelId=${panelId}`;
  }

  return `${grafanaBaseUrl}?${grafanaRange}&panelId=${panelId}`;
}

const publicDashboardUrl = buildGrafanaPanelUrl('panel-1');
const publicDashboardPanels = [
  {
    title: 'Evolucion trimestral total',
    description: 'Seguimiento trimestral para detectar aceleraciones, frenadas y cambios recientes.',
    src: buildGrafanaPanelUrl('panel-2'),
    minHeight: '420px',
  },
  {
    title: 'Distribucion por sexo',
    description: 'Comparativa entre hombres y mujeres en el empleo deportivo agregado.',
    src: buildGrafanaPanelUrl('panel-3'),
    minHeight: '360px',
  },
  {
    title: 'Tipo de empleo',
    description: 'Desglose entre empleo principal y secundario vinculado al deporte.',
    src: buildGrafanaPanelUrl('panel-4'),
    minHeight: '360px',
  },
  {
    title: 'Distribucion por edad',
    description: 'Foto del ultimo periodo disponible por grupos de edad.',
    src: buildGrafanaPanelUrl('panel-5'),
    minHeight: '360px',
  },
  {
    title: 'Distribucion por estudios',
    description: 'Comparativa del empleo deportivo segun nivel educativo.',
    src: buildGrafanaPanelUrl('panel-6'),
    minHeight: '360px',
  },
  {
    title: 'Jornada y situacion profesional',
    description: 'Peso relativo del empleo asalariado, no asalariado y del tipo de jornada.',
    src: buildGrafanaPanelUrl('panel-7'),
    minHeight: '360px',
  },
];

export function PublicHomePage() {
  const { t } = useTranslation();
  const [kpis, setKpis] = useState<DashboardKpis | null>(null);
  const [, setSeries] = useState<DashboardSeries | null>(null);
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
      text: 'KPIs y visualizaciones combinan datos del backend con paneles embebidos de Grafana.',
    },
    {
      icon: Globe,
      title: 'Soporte multilenguaje',
      text: 'Cambio de idioma rapido para demos, usuarios internos y presentaciones.',
    },
    {
      icon: Bot,
      title: 'Asistente contextual',
      text: 'Chat integrado con el backend para responder preguntas sobre el dataset.',
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
                  Analitica deportiva unificada
                </Badge>
                <Title order={1} mt="md" maw={760} style={{ fontSize: 'clamp(2.4rem, 5vw, 4.4rem)', lineHeight: 1 }}>
                  {t('publicTitle')}
                </Title>
                <Text c="dimmed" size="lg" maw={620} mt="md">
                  {t('publicDescription')}
                </Text>
                <Text size="sm" mt="sm" maw={540}>
                  Una capa visual para seguir rendimiento, actividad y operacion desde un unico punto.
                </Text>
              </div>

              <Group>
                <Button component={Link} to="/admin/login" size="md">
                  Admin
                </Button>
                <Button component="a" href="#public-dashboard" variant="default" size="md">
                  {t('viewPublicDashboard')}
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
                    Ultimos valores
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

      {error ? (
        <Paper p="md" mb="lg" radius="lg" className="glass-card">
          <Text size="sm" c="dimmed">
            Los indicadores en vivo del backend no estan disponibles ahora mismo. La vista publica de Grafana sigue operativa.
          </Text>
        </Paper>
      ) : null}

      <div id="public-dashboard">
        <Stack gap="lg">
          <DashboardEmbed
            src={publicDashboardUrl}
            title={t('viewPublicDashboard')}
            description="Vista principal con el panel de tendencia anual del reto C."
            minHeight="72vh"
          />

          <SimpleGrid cols={{ base: 1, xl: 2 }} spacing="lg">
            {publicDashboardPanels.map((panel) => (
              <DashboardEmbed
                key={`${panel.title}-${panel.src}`}
                src={panel.src}
                title={panel.title}
                description={panel.description}
                minHeight={panel.minHeight}
              />
            ))}
          </SimpleGrid>
        </Stack>
      </div>

      <ChatbotWidget />
    </>
  );
}
