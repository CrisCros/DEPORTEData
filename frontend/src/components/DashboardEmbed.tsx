import { Alert, AspectRatio, Group, Paper, Stack, Text, ThemeIcon, Title } from '@mantine/core';
import { LayoutPanelTop } from 'lucide-react';
import { useTranslation } from 'react-i18next';

type DashboardEmbedProps = {
  src?: string;
  title: string;
  description?: string;
};

export function DashboardEmbed({ src, title, description }: DashboardEmbedProps) {
  const { t } = useTranslation();

  return (
    <Paper withBorder radius="lg" p="md" shadow="sm" className="glass-card">
      <Stack gap="sm">
        <Group justify="space-between" align="flex-start">
          <div>
            <Title order={3}>{title}</Title>
            {description ? (
              <Text c="dimmed" size="sm">
                {description}
              </Text>
            ) : null}
          </div>
          <ThemeIcon color="cyan" variant="light" radius="xl" size="lg">
            <LayoutPanelTop size={18} aria-hidden="true" />
          </ThemeIcon>
        </Group>

        {src ? (
          <div className="embed-frame">
            <div className="embed-toolbar" aria-hidden="true">
              <span className="embed-dot" />
              <span className="embed-dot" />
              <span className="embed-dot" />
              <Text size="xs" c="dimmed" ml="xs">
                {title}
              </Text>
            </div>
            <AspectRatio ratio={16 / 9}>
              <iframe
                src={src}
                title={title}
                loading="lazy"
                referrerPolicy="strict-origin-when-cross-origin"
              />
            </AspectRatio>
          </div>
        ) : (
          <Alert color="blue" title={t('embeddedPanelLabel')}>
            {t('iframeFallback')}
          </Alert>
        )}
      </Stack>
    </Paper>
  );
}
