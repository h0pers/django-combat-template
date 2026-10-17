---
paths:
  - "frontend/**"
---

# Frontend (Vue 3 + Vite)

- Source lives in `frontend/src/`: the app entry, router, stores and views in `src/app/`, shared UI components in `src/components/ui/`, helpers in `src/lib/`, styles in `src/assets/styles/`.
- Django renders the page shell (`website/apps/polls/templates/polls/app.html`) and django-vite injects the Vite bundle; `/app/` serves the SPA.
- Run commands from `frontend/`: `npm run dev` (Vite dev server, used by Django when `DEBUG` is on), `npm run build`, `npm run lint`, `npm run format`.
- Run `npm run lint` and `npm run format` before finishing a frontend change.
- Talk to Django through its JSON API under `/api/`; don't duplicate business rules in the frontend.
- Add packages with `npm install <pkg>` from `frontend/`; don't hand-edit `package-lock.json`.
