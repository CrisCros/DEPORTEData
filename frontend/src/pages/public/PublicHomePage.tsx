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
import { type DashboardKpis, type DashboardSeries, dashboardApi, usageApi } from '../../services/api';

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
export function PublicHomePage() {
  const { t } = useTranslation();
  const [kpis, setKpis] = useState<DashboardKpis | null>(null);
  const [, setSeries] = useState<DashboardSeries | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void usageApi.track('public_page_view', '/', { section: 'home' });

    const loadDashboard = async () => {
      try {
        const [kpisResponse, seriesResponse] = await Promise.all([
          dashboardApi.getKpis(),
          dashboardApi.getSeries(),
        ]);
        setKpis(kpisResponse);
        setSeries(seriesResponse);
      } catch (err) {
        const details = err instanceof Error ? err.message : t('unknownError');
        setError(`${t('dashboardLoadError')} ${details}`);
      }
    };

    void loadDashboard();
  }, []);

  const features = [
    {
      icon: LayoutDashboard,
      title: t('featureDashboardTitle'),
      text: t('featureDashboardText'),
    },
    {
      icon: Globe,
      title: t('featureLanguageTitle'),
      text: t('featureLanguageText'),
    },
    {
      icon: Bot,
      title: t('featureAssistantTitle'),
      text: t('featureAssistantText'),
    },
  ];

  const publicDashboardPanels = [
    {
      title: t('panelQuarterlyTitle'),
      description: t('panelQuarterlyDescription'),
      src: buildGrafanaPanelUrl('panel-2'),
      minHeight: '420px',
    },
    {
      title: t('panelSexTitle'),
      description: t('panelSexDescription'),
      src: buildGrafanaPanelUrl('panel-3'),
      minHeight: '360px',
    },
    {
      title: t('panelEmploymentTypeTitle'),
      description: t('panelEmploymentTypeDescription'),
      src: buildGrafanaPanelUrl('panel-4'),
      minHeight: '360px',
    },
    {
      title: t('panelAgeTitle'),
      description: t('panelAgeDescription'),
      src: buildGrafanaPanelUrl('panel-5'),
      minHeight: '360px',
    },
    {
      title: t('panelStudiesTitle'),
      description: t('panelStudiesDescription'),
      src: buildGrafanaPanelUrl('panel-6'),
      minHeight: '360px',
    },
    {
      title: t('panelWorkdayTitle'),
      description: t('panelWorkdayDescription'),
      src: buildGrafanaPanelUrl('panel-7'),
      minHeight: '360px',
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
                  {t('publicBadge')}
                </Badge>
                <Title order={1} mt="md" maw={760} style={{ fontSize: 'clamp(2.4rem, 5vw, 4.4rem)', lineHeight: 1 }}>
                  {t('publicTitle')}
                </Title>
                <Text c="dimmed" size="lg" maw={620} mt="md">
                  {t('publicDescription')}
                </Text>
                <Text size="sm" mt="sm" maw={540}>
                  {t('publicIntro')}
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

              {kpis ? (
                <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="md">
                <Paper p="lg" className="metric-card">
                  <Text size="xs" tt="uppercase" c="dimmed" fw={700}>
                    {t('metricEmploymentTotal')} ({kpis?.latest_year ?? '-'})
                  </Text>
                  <Title order={2} mt={6}>
                    {kpis ? `${kpis.empleo_total}k` : '...'}
                  </Title>
                </Paper>
                <Paper p="lg" className="metric-card">
                  <Text size="xs" tt="uppercase" c="dimmed" fw={700}>
                    {t('metricAnnualGrowth')}
                  </Text>
                  <Title order={2} mt={6}>
                    {kpis ? `${kpis.growth_pct}%` : '...'}
                  </Title>
                </Paper>
                <Paper p="lg" className="metric-card">
                  <Text size="xs" tt="uppercase" c="dimmed" fw={700}>
                    {t('metricLatestValues')}
                  </Text>
                  <Title order={4} mt={6}>
                    {kpis ? kpis.latest_values.map((v) => `${v.year}:${v.value}`).join(' · ') : '...'}
                  </Title>
                </Paper>
                </SimpleGrid>
              ) : null}
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
            {t('liveIndicatorsUnavailable')}
          </Text>
        </Paper>
      ) : null}

      <div id="public-dashboard">
        <Stack gap="lg">
          <DashboardEmbed
            src={publicDashboardUrl}
            title={t('viewPublicDashboard')}
            description={t('mainTrendPanelDescription')}
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
