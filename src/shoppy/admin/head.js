export const adminHead = (title, description = 'AgentCart admin dashboard.') => () => ({ meta: [
  { title: `${title} — AgentCart Admin` }, { name: 'description', content: description }, { name: 'robots', content: 'noindex,nofollow' },
  { property: 'og:title', content: `${title} — AgentCart Admin` }, { property: 'og:description', content: description }, { property: 'og:type', content: 'website' }, { name: 'twitter:card', content: 'summary' },
] });
