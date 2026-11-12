import React from 'react';
import { Link as RouterLink, useNavigate as useRouterNavigate, useRouterState, useParams as useRouterParams } from '@tanstack/react-router';
export function Link({to, ...props}) {
 const [pathAndQuery, hash] = to.split('#');
 const [pathname, query] = pathAndQuery.split('?');
 return <RouterLink to={pathname} search={Object.fromEntries(new URLSearchParams(query || ''))} hash={hash || ''} {...props} />;
}
export function NavLink({className, end, to, ...props}) {
 const pathname = useRouterState({select: s => s.location.pathname});
 const active = end ? pathname === to : pathname === to || pathname.startsWith(to + '/');
 return <Link to={to} activeProps={{}} aria-current={active ? 'page' : undefined} className={typeof className === 'function' ? className({isActive: active}) : className} {...props} />;
}
export function useSearchParams() {
 const search = useRouterState({select: s => s.location.searchStr});
 const navigate = useRouterNavigate();
 return [new URLSearchParams(search), next => navigate({search: Object.fromEntries(next instanceof URLSearchParams ? next : new URLSearchParams(next))})];
}
export function useNavigate() { const navigate=useRouterNavigate(); return to => navigate({to}); }
export function useParams() { return useRouterParams({strict:false}); }
