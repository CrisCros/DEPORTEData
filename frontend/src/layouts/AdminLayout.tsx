import {
  AppShell,
  Badge,
  Burger,
  Button,
  Group,
  NavLink,
  Paper,
  Stack,
  Text,
  Title,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { ChartColumn, Gauge, Lock, UserRoundCog } from 'lucide-react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../auth/AuthContext';

const navigationItems = [
  { to: '/admin', key: 'navHome', icon: Gauge },
  { to: '/admin/telemetrias', key: 'navTelemetry', icon: ChartColumn },
  { to: '/admin/seguridad', key: 'navSecurity', icon: Lock },
  { to: '/admin/uso', key: 'navUsage', icon: UserRoundCog },
] as const;

export function AdminLayout() {
  const [opened, { toggle }] = useDisclosure();
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { t } = useTranslation();

  return (
    <AppShell
      className="admin-shell"
      header={{ height: 72 }}
      navbar={{ width: 300, breakpoint: 'sm', collapsed: { mobile: !opened } }}
      padding="md"
    >
      <AppShell.Header px="md" className="admin-header">
        <Group justify="space-between" h="100%">
          <Group>
            <Burger
              hiddenFrom="sm"
              opened={opened}
              aria-label="Toggle admin navigation"
              onClick={toggle}
            />
            <div>
              <Group gap="xs">
                <Title order={3}>{t('appName')}</Title>
                <Badge color="cyan" variant="light">
                  Admin
                </Badge>
              </Group>
              <Text size="sm" c="dimmed">
                Centro interno de seguimiento y operacion
              </Text>
            </div>
          </Group>
          <Button
            variant="light"
            color="red"
            onClick={() => {
              logout();
              navigate('/admin/login', { replace: true });
            }}
          >
            {t('logout')}
          </Button>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar p="md" className="admin-navbar">
        <Stack gap="md">
          <Paper p="md" bg="rgba(255,255,255,0.05)" bd="1px solid rgba(255,255,255,0.08)">
            <Text size="xs" tt="uppercase" fw={700} c="cyan.1">
              Workspace
            </Text>
            <Title order={4} c="white" mt={4}>
              Operacion y analitica
            </Title>
            <Text size="sm" c="slate.1" mt="xs">
              Navegacion privada para dashboards de control, seguridad y uso.
            </Text>
          </Paper>

          <Stack gap="xs">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  active={pathname === item.to}
                  label={t(item.key)}
                  leftSection={<Icon size={18} aria-hidden="true" />}
                  color="cyan"
                  styles={{
                    root: {
                      color: '#f4f8fc',
                      borderRadius: '16px',
                    },
                    label: {
                      fontWeight: 600,
                    },
                  }}
                  onClick={() => navigate(item.to)}
                />
              );
            })}
          </Stack>
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main className="admin-main">
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
