import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  es: {
    translation: {
      appName: 'DEPORTEData',
      publicTitle: 'Panel publico de analitica deportiva',
      publicDescription:
        'Visualiza indicadores abiertos y consulta el asistente contextual para explorar los datos publicados.',
      viewPublicDashboard: 'Dashboard publico',
      chatbotTitle: 'Asistente DEPORTEData',
      chatbotDescription: 'Espacio preparado para integrar el chatbot del proyecto.',
      openChat: 'Abrir chatbot',
      closeChat: 'Cerrar chatbot',
      language: 'Idioma',
      loginTitle: 'Acceso administrador',
      loginDescription: 'Inicia sesion para revisar los paneles privados de operacion.',
      username: 'Usuario',
      password: 'Contrasena',
      signIn: 'Entrar',
      logout: 'Salir',
      navHome: 'Inicio',
      navTelemetry: 'Telemetrias',
      navSecurity: 'Seguridad',
      navUsage: 'Uso',
      adminWelcome: 'Centro de control',
      adminSummary:
        'Monitorea telemetrias, seguridad y uso desde paneles internos preparados para Grafana.',
      embeddedPanelLabel: 'Panel incrustado',
      iframeFallback:
        'Configura una URL valida en las variables VITE_* para cargar el panel.',
    },
  },
  en: {
    translation: {
      appName: 'DEPORTEData',
      publicTitle: 'Public sports analytics dashboard',
      publicDescription:
        'Review open indicators and use the contextual assistant to explore published data.',
      viewPublicDashboard: 'Public dashboard',
      chatbotTitle: 'DEPORTEData assistant',
      chatbotDescription: 'Placeholder area for the project chatbot integration.',
      openChat: 'Open chatbot',
      closeChat: 'Close chatbot',
      language: 'Language',
      loginTitle: 'Admin access',
      loginDescription: 'Sign in to review the private operational dashboards.',
      username: 'Username',
      password: 'Password',
      signIn: 'Sign in',
      logout: 'Logout',
      navHome: 'Home',
      navTelemetry: 'Telemetry',
      navSecurity: 'Security',
      navUsage: 'Usage',
      adminWelcome: 'Control center',
      adminSummary:
        'Monitor telemetry, security and usage from internal Grafana-ready panels.',
      embeddedPanelLabel: 'Embedded panel',
      iframeFallback:
        'Set a valid VITE_* environment variable to load the embedded panel.',
    },
  },
} as const;

const preferredLanguage =
  typeof navigator !== 'undefined' && navigator.language.toLowerCase().startsWith('en')
    ? 'en'
    : 'es';

void i18n.use(initReactI18next).init({
  resources,
  lng: preferredLanguage,
  fallbackLng: 'es',
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;
