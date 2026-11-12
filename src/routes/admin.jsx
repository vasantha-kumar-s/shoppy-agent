import { createFileRoute, Outlet, useRouterState, Navigate } from '@tanstack/react-router';
import React from 'react';
import { AdminShell, useAdminSession } from '@/shoppy/admin/components';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin')({ ssr: false, head: adminHead('Dashboard'), component: AdminLayout });

function AdminLayout() {
  const session = useAdminSession();
  const pathname = useRouterState({ select: s => s.location.pathname });
  const onLogin = pathname.replace(/\/$/, '') === '/admin/login';
  if (onLogin) return <Outlet />;
  if (!session) return <Navigate to="/admin/login" replace />;
  return <AdminShell session={session}><Outlet /></AdminShell>;
}
