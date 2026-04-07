import {
  Badge,
  Button,
  Card,
  Grid,
  Group,
  Paper,
  RingProgress,
  SimpleGrid,
  Stack,
  Text,
  ThemeIcon,
  Title,
} from '@mantine/core';
import { Bot, Globe, LayoutDashboard, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ChatbotWidget } from '../../components/ChatbotWidget';
import { DashboardEmbed } from '../../components/DashboardEmbed';

const publicDashboardUrl = import.meta.env.VITE_PUBLIC_DASHBOARD_URL;

export function PublicHomePage() {
  const { t } = useTranslation();
  const features = [
    {
      icon: LayoutDashboard,
      title: 'Paneles embebidos',
      text: 'Espacios listos para integrar dashboards publicos de Grafana sin rehacer la UI.',
    },
    {
      icon: Globe,
      title: 'Soporte multilenguaje',
      text: 'Cambio de idioma rapido para demos, usuarios internos y presentaciones.',
    },
    {
      icon: Bot,
      title: 'Asistente contextual',
      text: 'Un widget preparado para incorporar preguntas guiadas o soporte conversacional.',
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
                    Fuentes conectadas
                  </Text>
                  <Title order={2} mt={6}>
                    12
                  </Title>
                </Paper>
                <Paper p="lg" className="metric-card">
                  <Text size="xs" tt="uppercase" c="dimmed" fw={700}>
                    Paneles activos
                  </Text>
                  <Title order={2} mt={6}>
                    08
                  </Title>
                </Paper>
                <Paper p="lg" className="metric-card">
                  <Text size="xs" tt="uppercase" c="dimmed" fw={700}>
                    Alertas monitoreadas
                  </Text>
                  <Title order={2} mt={6}>
                    24/7
                  </Title>
                </Paper>
              </SimpleGrid>
            </Stack>
          </Paper>
        </Grid.Col>

        <Grid.Col span={{ base: 12, lg: 4 }}>
          <Card p="xl" className="glass-card" h="100%">
            <Stack justify="space-between" h="100%">
              <div>
                <Group justify="space-between" align="flex-start">
                  <div>
                    <Text size="xs" tt="uppercase" fw={700} c="dimmed">
                      Ready for embed
                    </Text>
                    <Title order={2} mt={4}>
                      Grafana + chatbot
                    </Title>
                  </div>
                  <ThemeIcon color="cyan" variant="light" radius="xl" size="xl">
                    <Sparkles size={20} aria-hidden="true" />
                  </ThemeIcon>
                </Group>
                <Text c="dimmed" mt="md">
                  {t('chatbotDescription')}
                </Text>
              </div>
              <Group justify="space-between" align="center">
                <RingProgress
                  size={110}
                  thickness={12}
                  sections={[{ value: 78, color: 'cyan' }]}
                  label={
                    <Text ta="center" fw={700} size="lg">
                      78%
                    </Text>
                  }
                />
                <Stack gap={4}>
                  <Text fw={700}>{t('chatbotTitle')}</Text>
                  <Text size="sm" c="dimmed" maw={180}>
                    UI lista para demos, integracion de preguntas y soporte contextual.
                  </Text>
                </Stack>
              </Group>
            </Stack>
          </Card>
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

      <div id="public-dashboard">
        <DashboardEmbed
          src={publicDashboardUrl}
          title={t('viewPublicDashboard')}
          description={t('publicDescription')}
        />
      </div>

      <ChatbotWidget />
    </>
  );
}
