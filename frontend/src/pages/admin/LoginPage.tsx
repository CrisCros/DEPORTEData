import { Anchor, Badge, Button, Center, Paper, PasswordInput, Stack, Text, TextInput, Title } from '@mantine/core';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const { t } = useTranslation();
  const [error, setError] = useState<string | null>(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const redirectTarget = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname ?? '/admin';

  return (
    <Center mih="100vh" px="md">
      <Paper withBorder radius="xl" p="xl" maw={440} w="100%" className="glass-card">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            const success = login(username, password);
            if (!success) {
              setError('Introduce credenciales validas.');
              return;
            }
            setError(null);
            navigate(redirectTarget, { replace: true });
          }}
        >
          <Stack gap="md">
            <div>
              <Badge variant="light" color="cyan" mb="sm">
                Admin access
              </Badge>
              <Title order={1}>{t('loginTitle')}</Title>
              <Text c="dimmed" size="sm">
                {t('loginDescription')}
              </Text>
            </div>

            <TextInput
              required
              autoComplete="username"
              label={t('username')}
              placeholder="admin"
              value={username}
              onChange={(event) => setUsername(event.currentTarget.value)}
            />
            <PasswordInput
              required
              autoComplete="current-password"
              label={t('password')}
              placeholder="********"
              value={password}
              onChange={(event) => setPassword(event.currentTarget.value)}
            />

            {error ? (
              <Text c="red" size="sm" role="alert">
                {error}
              </Text>
            ) : null}

            <Button type="submit" fullWidth>
              {t('signIn')}
            </Button>

            <Anchor component={Link} to="/">
              Volver a la zona publica
            </Anchor>
          </Stack>
        </form>
      </Paper>
    </Center>
  );
}
