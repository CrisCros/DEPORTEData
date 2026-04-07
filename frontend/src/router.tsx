import { createBrowserRouter } from 'react-router-dom';
import { ProtectedRoute } from './routes/ProtectedRoute';
import { AdminLayout } from './layouts/AdminLayout';
import { PublicLayout } from './layouts/PublicLayout';
import { AdminHomePage } from './pages/admin/AdminHomePage';
import { LoginPage } from './pages/admin/LoginPage';
import { SecurityPage } from './pages/admin/SecurityPage';
import { TelemetryPage } from './pages/admin/TelemetryPage';
import { UsagePage } from './pages/admin/UsagePage';
import { PublicHomePage } from './pages/public/PublicHomePage';

export const appRouter = createBrowserRouter([
  {
    path: '/',
    element: <PublicLayout />,
    children: [
      {
        index: true,
        element: <PublicHomePage />,
      },
    ],
  },
  {
    path: '/admin/login',
    element: <LoginPage />,
  },
  {
    path: '/admin',
    element: <ProtectedRoute />,
    children: [
      {
        element: <AdminLayout />,
        children: [
          {
            index: true,
            element: <AdminHomePage />,
          },
          {
            path: 'telemetrias',
            element: <TelemetryPage />,
          },
          {
            path: 'seguridad',
            element: <SecurityPage />,
          },
          {
            path: 'uso',
            element: <UsagePage />,
          },
        ],
      },
    ],
  },
]);
