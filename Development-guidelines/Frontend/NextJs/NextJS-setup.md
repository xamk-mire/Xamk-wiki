# Next.js Project Setup — Step‑by‑Step with Explanations (2025)

This guide walks you from zero to a production‑ready Next.js app using the **App Router** (Next.js 13+), **TypeScript**, and modern best practices. It explains not just *how* but *why*.

---

## What you’ll build

* A baseline Next.js app with TypeScript, ESLint, and optional Tailwind CSS.
* App Router structure (server components by default) with a couple of routes and layout.
* Sensible dev scripts, environment variable handling, and a production build.

---

## 1) Prerequisites

### Install Node.js (LTS)

* **Why LTS?** It prioritizes stability and long‑term support. Next.js tracks modern Node versions; using LTS avoids ecosystem breakage.
* **Check versions:**

  ```bash
  node -v
  npm -v
  ```

  Aim for **Node ≥ 18** (Next.js supports maintained Node majors). If you work on multiple projects, consider a version manager (e.g., nvm) to switch Node versions per project.

### Choose a package manager

* **npm** (default), **pnpm** (fast, disk‑efficient), or **yarn** (classic alternative). Any is fine—pick one and stay consistent per project to avoid lockfile conflicts.

---

## 2) Create a new Next.js app

Run the official scaffolding tool:

```bash
npx create-next-app@latest my-next-app
```

**What this does**

* Downloads the latest `create-next-app` and scaffolds files.
* Sets up scripts in `package.json` (e.g., `dev`, `build`, `start`, `lint`).
* Optionally configures TypeScript, ESLint, Tailwind, and `src/` structure.

### CLI prompts (and how to choose)

1. **TypeScript?** → **Yes**. Strong typing reduces runtime bugs and documents your code. Next.js templates come with a tuned `tsconfig.json`.
2. **ESLint?** → **Yes**. Linting catches mistakes (unused vars, incorrect hooks usage) and enforces consistent style.
3. **Tailwind CSS?** → Optional but recommended for rapid, consistent styling without context switching to CSS files.
4. **Use `src/` directory?** → **Yes**. Keeps source organized (`src/app`, `src/components`, etc.).
5. **Use App Router?** → **Yes**. The App Router is the modern routing system with server components by default, layouts, and streaming.
6. **Import alias?** → Accept `@/*`. It avoids brittle relative paths like `../../../component`.

> **Tip:** If you forget an option, you can always add it later; Tailwind, for example, can be installed at any time.

---

## 3) Explore the project structure

Typical structure (App Router + `src/`):

```
my-next-app/
├─ src/
│  ├─ app/                 # Route tree (folders = routes)
│  │  ├─ layout.tsx        # Root layout (shared UI, metadata)
│  │  ├─ page.tsx          # `/` route
│  │  ├─ globals.css       # Global styles (imported by root layout)
│  │  └─ about/
│  │     └─ page.tsx       # `/about` route
│  ├─ components/          # Reusable UI building blocks
│  ├─ lib/                  # Utilities, data access, helpers
│  └─ styles/              # (Optional) Additional CSS modules or files
├─ public/                  # Static assets served at root path
├─ .env.local               # Local environment variables (ignored by git)
├─ next.config.mjs          # Next.js configuration
├─ package.json             # Dependencies and scripts
├─ tsconfig.json            # TypeScript configuration
└─ eslint.config.mjs        # Flat-config ESLint (if selected)
```

**Key idea: App Router**

* **Server Components by default** → Smaller bundles, data fetched on the server, better performance.
* **Client Components** → Opt‑in via `"use client"` at the top of a file when you need browser‑only APIs, event handlers, or stateful hooks.
* **Layouts** → Persist UI between pages and compose nested layouts.
* **Streaming/SSR/SSG** → Mix rendering strategies per route.

---

## 4) Run the dev server

```bash
npm run dev
```

* Starts on `http://localhost:3000`.
* Auto‑reloads on save.
* Displays errors with helpful overlays.

**Common script list** (in `package.json`):

* `dev` → Development server.
* `build` → Production build (optimizes, pre‑renders, bundles).
* `start` → Starts the production server after `build`.
* `lint` → Runs ESLint.
* `test` → (Optional) Your chosen test runner.

---

## 5) Create your first routes

**`src/app/about/page.tsx`**

```tsx
export default function AboutPage() {
  return (
    <main>
      <h1>About Us</h1>
      <p>We build delightful web apps with Next.js.</p>
    </main>
  );
}
```

* In the App Router, any folder with `page.tsx` becomes a route. The folder name is the path segment.
* The default export is the route’s UI. No `React.FC` needed.

**Add a nested route with its own layout**

```
src/app/(marketing)/
  layout.tsx
  page.tsx
  pricing/
    page.tsx
```

* Group routes using **Route Groups**: folders like `(marketing)` don’t affect the URL but help organize layouts.

**`src/app/(marketing)/layout.tsx`**

```tsx
export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <section>
      {/* shared header/nav for marketing pages */}
      {children}
    </section>
  );
}
```

---

## 6) Data fetching & caching (App Router mental model)

* **Server Components** can run async and call databases or fetch APIs directly (no `useEffect` required). They never ship their server‑only code to the client.
* **`fetch` caching**: by default, `fetch` in Server Components is **cached** and deduped during a request. Control with options:

  * `cache: 'no-store'` → always fetch fresh data (SSR)
  * `next: { revalidate: n }` → ISR; cache for `n` seconds, then revalidate

**Example: ISR (Incremental Static Regeneration)**

```tsx
// src/app/blog/page.tsx
import { Suspense } from 'react';

export const revalidate = 60; // revalidate this route every 60s

async function getPosts() {
  const res = await fetch('https://example.com/api/posts', { next: { revalidate: 60 } });
  if (!res.ok) throw new Error('Failed to load posts');
  return res.json();
}

export default async function BlogPage() {
  const posts = await getPosts();
  return (
    <main>
      <h1>Blog</h1>
      <ul>
        {posts.map((p: any) => (
          <li key={p.id}>{p.title}</li>
        ))}
      </ul>
    </main>
  );
}
```

**When to use Client Components**

* Need interactivity (click handlers), state (`useState`), or browser APIs (`localStorage`, `window`).
* **Mark the file:**

  ```tsx
  'use client';
  import { useState } from 'react';
  export default function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
  }
  ```

---

## 7) Metadata, fonts, and images

**Metadata**

* Use the `metadata` export or `generateMetadata` in App Router to set SEO and social previews per route.

```tsx
// src/app/page.tsx
export const metadata = {
  title: 'Home | My App',
  description: 'Welcome to my app',
};
```

**Fonts**

* Use `next/font` for automatic font optimization, no CLS from @import.

```tsx
// src/app/layout.tsx
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

**Images**

* Use `next/image` for responsive, optimized images.

```tsx
import Image from 'next/image';
<Image src="/hero.png" alt="Hero" width={1200} height={600} priority />
```

---

## 8) Styling options

### Tailwind CSS (recommended for speed)

If you didn’t select it in the wizard:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

* Add `./src/**/*.{ts,tsx}` to `content` in `tailwind.config.js`.
* Import `globals.css` in the root layout (if not already):

```css
/* src/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### CSS Modules

* Create `Component.module.css` and import it. Class names are locally scoped.

### Vanilla Extract / Styled‑Components

* Supported if you prefer typed styles or CSS‑in‑JS; check the Next.js docs for specific setup.

---

## 9) Environment variables

* Create `.env.local` for secrets (API keys, DB URLs). It’s git‑ignored by default.
* Prefix **public** variables with `NEXT_PUBLIC_` to expose them to the browser; others remain server‑only.

```dotenv
# .env.local
DATABASE_URL=postgres://...
NEXT_PUBLIC_ANALYTICS_KEY=abc123
```

Access in code:

```ts
process.env.DATABASE_URL // server only
process.env.NEXT_PUBLIC_ANALYTICS_KEY // available on client & server
```

> **Caution:** Never commit secrets. Use environment management in your hosting provider for production.

---

## 10) Absolute imports & path aliases

* The wizard sets an alias like `@/*`. In `tsconfig.json`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

Use it in code: `import Button from '@/components/Button';`

---

## 11) API routes (Route Handlers)

* In App Router, create `route.ts` inside a folder to handle HTTP verbs.

```ts
// src/app/api/health/route.ts
import { NextResponse } from 'next/server';

export function GET() {
  return NextResponse.json({ ok: true, time: new Date().toISOString() });
}
```

* Accessible at `/api/health`.
* Handlers run on the **Edge** or **Node** runtime depending on your config; choose Edge for lower latency and Node for broader API support.

---

## 12) Middleware

* File `src/middleware.ts` (or `middleware.ts` at root) runs **before** requests and can rewrite, redirect, or auth‑gate.

```ts
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
  const isLoggedIn = Boolean(req.cookies.get('session'));
  if (!isLoggedIn && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

---

## 13) Linting & formatting

* **ESLint**: catches issues and enforces best practices (including React and accessibility rules).
* **Prettier**: consistent formatting. You can integrate with ESLint via a config and a `format` script.

```bash
npm run lint
```

Add scripts:

```json
{
  "scripts": {
    "lint": "eslint .",
    "format": "prettier --write ."
  }
}
```

> With the modern ESLint flat config (`eslint.config.mjs`), ensure compatible plugins/presets. The Next.js template handles this for you.

---

## 14) Testing (quick picks)

* **Unit/component:** **Vitest** + **Testing Library** for fast TS support.
* **E2E:** **Playwright** for browser automation.

Example setup (Vitest):

```bash
npm i -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

Add `vitest.config.ts` and a `test` script. Render React components with Testing Library and assert accessible roles/text.

---

## 15) Building for production

```bash
npm run build
npm start
```

* `build` performs tree‑shaking, code splitting, image/font optimization, and static generation where possible.
* `start` launches the optimized server. Use a process manager (PM2) or your platform’s service runner in production.

**Common build flags**

* `next build` respects `NEXT_TELEMETRY_DISABLED=1` if you need to disable telemetry.
* Customize behavior in `next.config.mjs` (images, redirects, headers, experimental flags).

---

## 16) Deployment options

### Vercel (recommended)

* Zero‑config for most apps, supports **Edge** and **ISR** out of the box.
* Connect your Git repo → push to `main`/`prod` branch → Vercel builds automatically.
* Set environment variables in Vercel dashboard. Preview deployments for PRs.

### Other hosts

* **Netlify**, **AWS Amplify**, **Render**, **Fly.io**, **Railway**, or your own Node server.
* Ensure you run `next build` in CI, then `next start` (or their Next.js adapter) and configure environment variables.

### Docker (self‑hosting)

Minimal example:

```dockerfile
# Dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY package.json .
EXPOSE 3000
CMD ["npx", "next", "start", "-p", "3000"]
```

---

## 17) Common gotchas

* **Forgetting `'use client'`:** If a component needs hooks (`useState`, `useEffect`) or event handlers, add the directive at the top.
* **Misusing env vars:** Only `NEXT_PUBLIC_*` are exposed to the client; everything else is server‑only. Don’t put secrets in the browser.
* **Stale caches:** If your data isn’t updating, check `revalidate` and `cache` options. Use `no-store` for always‑fresh SSR.
* **Image domains:** If loading remote images, add allowed domains in `next.config.mjs` under `images.domains`.
* **Route conflicts:** Route Groups `(group)` help organize layouts without changing URLs.

---

## 18) Performance & accessibility

* Prefer **Server Components**; they reduce client JS. Only opt into Client Components when needed.
* Use **`<Image>`** and **`<Link>`** for performance and prefetching.
* Audit with **Lighthouse** and **eslint-plugin-jsx-a11y** for accessible markup.
* Stream large pages with `Suspense` to improve perceived performance.

---

## 19) Next steps

* Add a real data source (e.g., Postgres via Prisma) and fetch directly in Server Components.
* Introduce authentication (NextAuth/Auth.js, custom JWT, or provider auth) using Route Handlers and Middleware.
* Set up CI (GitHub Actions) for lint/test/build on every PR.

---

## 20) Quick reference (TL;DR)

```bash
# 1) Scaffold
npx create-next-app@latest my-next-app
cd my-next-app

# 2) Dev
npm run dev

# 3) New route
mkdir -p src/app/about
# create src/app/about/page.tsx

# 4) Build & run prod
npm run build
npm start
```

That’s it! You now have a solid Next.js foundation with the *why* behind each decision. Adjust pieces (styling, testing, hosting) to fit your stack and team preferences.
