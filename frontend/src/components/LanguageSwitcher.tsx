import { ActionIcon, Group, Text } from '@mantine/core';
import { Languages } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export function LanguageSwitcher() {
  const { i18n, t } = useTranslation();
  const nextLanguage = i18n.language.startsWith('es') ? 'en' : 'es';

  return (
    <Group gap="xs" aria-label={t('language')}>
      <Text size="sm" fw={500}>
        {t('language')}: {i18n.language.toUpperCase()}
      </Text>
      <ActionIcon
        aria-label={`${t('language')}: ${nextLanguage.toUpperCase()}`}
        color="blue"
        variant="light"
        onClick={() => {
          void i18n.changeLanguage(nextLanguage);
        }}
      >
        <Languages size={18} aria-hidden="true" />
      </ActionIcon>
    </Group>
  );
}
