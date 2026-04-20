import { AppShell, Badge, Burger, Button, Container, Group, Text, Title } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Link, Outlet } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { LanguageSwitcher } from '../components/LanguageSwitcher';

export function PublicLayout() {
  const [opened, { toggle }] = useDisclosure(false);
  const { t } = useTranslation();

  return (
    <AppShell
      className="public-shell"
      header={{ height: 72 }}
      navbar={{ width: 280, breakpoint: 'sm', collapsed: { mobile: !opened, desktop: true } }}
      padding="md"
    >
      <AppShell.Header className="public-header">
        <Container size="xl" h="100%">
          <Group justify="space-between" h="100%">
            <Group>
              <Burger
                hiddenFrom="sm"
                opened={opened}
                onClick={toggle}
                aria-label="Toggle navigation"
              />
              <div>
                <Group gap="xs">
                  <Title order={2}>{t('appName')}</Title>
                  <Badge variant="light" color="cyan">{t('clientArea')}</Badge>
                </Group>
                <Text size="sm" c="dimmed">
                  {t('publicHeaderSubtitle')}
                </Text>
              </div>
            </Group>
            <Group gap="sm">
              <LanguageSwitcher />
              <Button component={Link} to="/admin/login" variant="default">
                Admin
              </Button>
            </Group>
          </Group>
        </Container>
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <Group justify="space-between" mb="lg">
          <div>
            <Text size="sm" c="dimmed">
              {t('publicSpace')}
            </Text>
            <Text fw={700}>{t('appName')}</Text>
          </div>
          <LanguageSwitcher />
        </Group>
        <Text size="sm" c="dimmed">
          {t('publicNavbarDescription')}
        </Text>
      </AppShell.Navbar>

      <AppShell.Main>
        <Container size="xl" py="xl">
          <Outlet />
        </Container>
      </AppShell.Main>
    </AppShell>
  );
}
