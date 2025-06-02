# Component Libraries & CSS Frameworks Guide

---

## 1 Why Use a Library or Framework?

|Benefit|Frameworks (e.g., **Tailwind, Bootstrap**)|Component Libraries (e.g., **Material UI, Chakra, shadcn/ui**)|
|---|---|---|
|Speed|Pre‑built utilities for spacing, color, layout|Ready‑made, accessible components|
|Consistency|Design tokens & docs|Opinionated/controlled design language|
|Learning Curve|Low (utility classes) to medium|Medium (APIs)|
|Customization|Configure theme file or extend utilities|Override theme, props, or CSS vars|

_Framework = ****class-based styling toolkit****; Component Library = ****React/Vue components**** you import and style via props/theme._

---

## 2 Categories at a Glance

1. **Utility‑First CSS** – Tailwind CSS, Windi CSS, UnoCSS.
    
2. **Traditional CSS Frameworks** – Bootstrap 5, Bulma, Foundation.
    
3. **Headless Primitives** – Radix UI, Headless UI (unstyled, accessible).
    
4. **Opinionated Component Libraries** – Material UI (MUI), Ant Design, Chakra UI, Mantine.
    
5. **Styled Wrappers Around Primitives** – shadcn/ui (Radix + Tailwind), DaisyUI.
    

---

## 3 Decision Matrix

|Question|Pick Utility‑First|Pick Component Library|Pick Headless Primitives|
|---|---|---|---|
|Need pixel‑perfect custom brand?|✔️|⚠️ (requires overrides)|✔️|
|Need accessible complex widgets quickly?|⚠️ (extra work)|✔️|✔️|
|Bundle size a major concern?|✔️ (purge)|⚠️ (tree‑shake)|✔️|
|Design team hands you Figma tokens?|✔️|✔️|✔️|

---

## 4 Quick Starts

### 4.1 Tailwind CSS (Utility‑First)

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

``

```js
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#0d47a1",
          light: "#5472d3",
        },
      },
    },
  },
};
```

Use classes directly:

```html
<button class="px-4 py-2 bg-brand text-white rounded-lg hover:bg-brand-light">
  Click me
</button>
```

### 4.2 Material UI (React Component Library)

```bash
npm install @mui/material @emotion/react @emotion/styled
```

```tsx
import Button from "@mui/material/Button";
function App() {
  return <Button variant="contained">Hello MUI</Button>;
}
```

**Custom theme:**

```tsx
import { createTheme, ThemeProvider } from "@mui/material/styles";
const theme = createTheme({ palette: { primary: { main: "#0d47a1" } } });
```

### 4.3 DaisyUI + Tailwind (Styled Headless)

```bash
 npm i -D daisyui@latest
```

Buttons come pre‑styled with Tailwind + DaisyUI primitives and are fully theme‑able via CSS variables.

---

## 5 Theming & Design Tokens

|Library|Theming Mechanism|Dark Mode|
|---|---|---|
|Tailwind|`tailwind.config` + CSS vars (`:root { --color-brand: ...; }`)|`class="dark"` strategy|
|MUI|`createTheme()` object, Emotion/CSS-in-JS|`palette.mode = "dark"`|
|Chakra|`extendTheme`, style props|automatic `colorMode`|
|Radix|CSS variables (`--gray-1`)|Use `data-theme="dark"`|

**Best practice:** centralize brand palette & spacing scale as tokens (e.g., design‑tokens.css) and reference in both Tailwind and MUI theme for cross‑system consistency.

---

## 6 Performance & Tree‑Shaking

1. **Tailwind** – Purge unused classes in production (`mode: "jit"`, `NODE_ENV=production`).
    
2. **MUI** – Use `babel-plugin-import` or `@mui/material/Unstable_Grid2` for treeshaking; import icons individually.
    
3. **Ant Design** – `babel-plugin-import` + `antd/dist/reset.css` v6.
    
4. **Radix** – lightweight (CSS vars only). Combine with Tailwind for utility purge.
    

> **Tip:** run `npx why‑is‑bundled` or Vite’s `--build --report` to inspect bundle size.

---

## 7 Accessibility Checklist

- **Role & ARIA**: Libraries like MUI & Radix ship with correct roles, but test with Axe.
    
- **Focus management**: Confirm modals/traps (Radix Dialog) return focus.
    
- **Color contrast**: ensure custom themes keep ≥ 4.5:1 ratio.
    
- **Keyboard**: Tab through every interactive element.
    

---

## 8 Integrating with Frameworks

| Framework              | Recommended Styling Stack                                              |
| ---------------------- | ---------------------------------------------------------------------- |
| **Next.js**            | Tailwind + DaisyUI, or MUI with App Router (`use client`) where needed |
| **React Native** (web) | Tamagui or Nativewind                                                  |
| **Svelte / SvelteKit** | UnoCSS or DaisyUI + svelte‑headless‑ui                                 |
| **Vue 3 / Nuxt**       | Windi CSS, Vuetify, Naive UI                                           |

---

## 9 Best Practices Cheat‑Sheet

- **Start small**: import only components you need (shadcn CLI, MUI v6 tree‑shake).
    
- **Token‑driven**: expose colors, radius, spacing via CSS vars for runtime theming.
    
- **Component boundary**: wrap third‑party components in your own to decouple.
    
- **Upgrade path**: watch release notes—major versions may drop class prefixes or rename props.
    
- **Accessibility first**: don’t override native focus outlines without providing a visible alternative.
    

---

## 10 Further Resources

- **Tailwind Docs & UI Patterns** (tailwindcss.com)
    
- **MUI X / Pro components** – advanced data grid, date pickers.
    
- **Radix UI Docs** – headless primitives & accessibility guides.
    
- **shadcn/ui GitHub** – CLI, theming docs, patterns.
    
- **Component Party** (component.party) – compare frameworks & libraries.
    
