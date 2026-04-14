import {
  ActionIcon,
  Affix,
  Badge,
  Button,
  Drawer,
  Group,
  Paper,
  Stack,
  Text,
  TextInput,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { MessageCircleMore } from 'lucide-react';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { chatApi } from '../services/api';

type ChatMessage = {
  role: 'user' | 'assistant';
  text: string;
};

export function ChatbotWidget() {
  const [opened, { open, close }] = useDisclosure(false);
  const { t } = useTranslation();
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', text: 'Hola, pregúntame sobre la evolución del empleo deportivo.' },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    const content = input.trim();
    if (!content || loading) {
      return;
    }

    setMessages((prev) => [...prev, { role: 'user', text: content }]);
    setInput('');
    setLoading(true);

    try {
      const response = await chatApi.sendMessage(content);
      setMessages((prev) => [...prev, { role: 'assistant', text: response.answer }]);
    } catch (err) {
      const details = err instanceof Error ? err.message : 'Error desconocido';
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: `No pude consultar el backend: ${details}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

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
              Datos reales
            </Badge>
          </Group>
        }
        withCloseButton
      >
        <Stack gap="md">
          <Stack gap="xs" style={{ maxHeight: 360, overflowY: 'auto' }}>
            {messages.map((message, index) => (
              <Paper key={`${message.role}-${index}`} p="sm" radius="md" bg={message.role === 'user' ? 'blue.0' : 'gray.1'}>
                <Text size="sm" fw={600} mb={2}>
                  {message.role === 'user' ? 'Tú' : 'DEPORTEData'}
                </Text>
                <Text size="sm">{message.text}</Text>
              </Paper>
            ))}
          </Stack>

          <Group align="end" wrap="nowrap">
            <TextInput
              placeholder="Ejemplo: ¿Cómo ha crecido el empleo?"
              value={input}
              onChange={(event) => setInput(event.currentTarget.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  event.preventDefault();
                  void handleSend();
                }
              }}
              style={{ flex: 1 }}
            />
            <Button onClick={() => void handleSend()} loading={loading}>
              Enviar
            </Button>
          </Group>
        </Stack>
      </Drawer>
    </>
  );
}
