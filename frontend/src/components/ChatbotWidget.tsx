import { ActionIcon, Affix, Badge, Drawer, Group, Paper, Stack, Text, Title } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { MessageCircleMore } from 'lucide-react';
import { useTranslation } from 'react-i18next';

const chatbotUrl = import.meta.env.VITE_CHATBOT_URL;

export function ChatbotWidget() {
  const [opened, { open, close }] = useDisclosure(false);
  const { t } = useTranslation();

  return (
    <>
      <Affix position={{ bottom: 24, right: 24 }}>
        <ActionIcon
          aria-label={opened ? t('closeChat') : t('openChat')}
          color="blue"
          gradient={{ from: 'blue', to: 'cyan', deg: 135 }}
          radius="xl"
          size={56}
          variant="gradient"
          onClick={open}
        >
          <MessageCircleMore aria-hidden="true" size={26} />
        </ActionIcon>
      </Affix>

      <Drawer
        opened={opened}
        onClose={close}
        position="right"
        size="md"
        padding="lg"
        title={
          <Group gap="sm">
            <Text fw={700}>{t('chatbotTitle')}</Text>
            <Badge color="cyan" variant="light">
              Beta
            </Badge>
          </Group>
        }
        withCloseButton
      >
        <Stack gap="md">
          <Paper p="md" className="glass-card">
            <Text c="dimmed" size="sm">
              {t('chatbotDescription')}
            </Text>
          </Paper>
          {chatbotUrl ? (
            <iframe
              src={chatbotUrl}
              title={t('chatbotTitle')}
              style={{ width: '100%', minHeight: 480, borderRadius: 20, background: '#f4f8fc' }}
            />
          ) : (
            <Title order={5}>{t('iframeFallback')}</Title>
          )}
        </Stack>
      </Drawer>
    </>
  );
}
