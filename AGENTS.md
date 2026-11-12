<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.

## What Lovable manages

Rules outside this block are the project's own. Change the pieces below in
Lovable, not by hand. With the [Lovable MCP](https://mcp.lovable.dev)
connected, `send_message` asks Lovable to do it; otherwise ask the user to
use the editor.

- **Database.** Do not add or edit `supabase/migrations/` or `drizzle/`.
  Ask Lovable to change the schema.
- **Generated files.** Do not edit a file whose header says it is automatically
  generated.
- **AI gateway.** Keep model calls on Lovable's gateway, and keep
  `LOVABLE_API_KEY` out of browser code.
- **Connectors.** Lovable provides native connectors. `list_connectors` shows
  which are enabled; `add_connector` only returns the dashboard link. When a
  connector is enabled, calls go through the connector gateway and need
  `LOVABLE_API_KEY`. When Lovable does not provide one, users can bring their
  own key and store it in Secrets.
- **Secrets.** Lovable manages them. Do not put secret values in the repo.
<!-- LOVABLE:END -->

- Keep imported page markup in TanStack route files and reuse the source JavaScript helpers; this preserves the repository interface without introducing a second router.
- Use `VITE_API_URL` for the external Shoppy service and fail clearly when absent; never fall back to visitors' localhost or invent shopping data.
- Preserve source CSS in a separate stylesheet; visual conversion must not change the imported design.
- Admin preview data lives only in `src/shoppy/admin/mock-data.js` behind `mockAdmin`; swap it for real API calls later and keep every simulated action labelled, so mock data never mixes with the store service client.
- Admin sign-in posts to the store service; the frontend holds no credentials, and "preview mode" is a labelled, local-only session.
- Use `confirmAction()` and sonner toasts instead of `window.confirm`/`alert`, for one consistent dialog style.
- Store service address resolves from the in-app setting (localStorage) then `VITE_API_URL`; Layout loads it before rendering pages, and the Vite dev proxy forwards `/api` for local runs — so one build works on any device.
- Admin pages use `adminApi` (admin-api.js): live sessions hit REST endpoints, preview sessions use `mockAdmin`, keeping simulated and real data apart.
