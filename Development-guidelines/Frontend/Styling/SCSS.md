## 1  What Is SCSS?

**Sass** (Syntactically Awesome Style Sheets) is a CSS pre‑processor that adds variables, nesting, logic, and reusable snippets. The **SCSS syntax** looks like regular CSS—but with super‑powers.

* Write in `.scss` → compile to `.css` using the Sass compiler.
* Everything valid CSS is valid SCSS, so you can migrate incrementally.

---

## 2  Getting Set Up

### 2.1 Install the Compiler

* **Dart Sass (official)** – single binary, cross‑platform.

  ```bash
  npm install -D sass         # project‑local
  # or
  brew install sass/sass/sass # macOS
  ```
* Alternative: **Vite**, **Webpack**, **Parcel** loaders—handled for you by plugins.

### 2.2 Folder Structure

```
project/
├── scss/
│   ├── main.scss
│   ├── _variables.scss   # partials start with _
│   ├── _mixins.scss
│   └── components/
│       └── _buttons.scss
└── css/
    └── main.css          # compiled output
```

### 2.3 Compile Watch Mode

```bash
npx sass scss:css --watch --style=expanded   # dev
npx sass scss:css --style=compressed         # prod
```

---

## 3  SCSS Syntax Basics

### 3.1 Variables

```scss
$brand-hue: 200;
$gap: 1.25rem;

nav {
  background: hsl($brand-hue 80% 50%);
  padding: $gap;
}
```

### 3.2 Nesting & the Parent Selector `&`

```scss
.card {
  border: 1px solid #ddd;
  padding: 1rem;

  h2 {
    margin-top: 0;
  }

  &:hover {
    box-shadow: 0 4px 6px rgb(0 0 0 / .1);
  }
}
```

> **Rule of thumb:** keep nesting to **3 levels or fewer** to avoid overly specific selectors.

### 3.3 Partials & `@use`

```scss
// _variables.scss
$radius: 0.75rem;

// _buttons.scss
@use "../variables" as v;

.btn {
  border-radius: v.$radius;
}
```

*Use the modern module system (`@use` + `@forward`) instead of the legacy `@import`.*

---

## 4  Reuse & Logic

### 4.1 Mixins

```scss
@mixin flex-center($gap: 1rem) {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: $gap;
}

.header {
  @include flex-center(2rem);
}
```

### 4.2 Functions

```scss
@function tint($color, $amount) {
  @return mix(white, $color, $amount);
}

.alert {
  background: tint(red, 30%);
}
```

### 4.3 `@extend` & Placeholders

```scss
%btn-base {
  display: inline-block;
  padding: .6rem 1rem;
  border-radius: .4rem;
}

.btn-primary {
  @extend %btn-base;
  background: hsl($brand-hue 80% 50%);
  color: white;
}
```

> Prefer `%placeholders` over extending concrete classes to avoid unintended side effects.

---

## 5  Control Directives

| Directive       | Purpose              | Mini‑Example                                                     |
| --------------- | -------------------- | ---------------------------------------------------------------- |
| `@if` / `@else` | Conditional styles   | `@if $dark { color: white; }`                                    |
| `@for`          | Indexed loop         | `@for $i from 1 through 4 { .m-#{$i} { margin: $i * .25rem; } }` |
| `@each`         | Iterate lists/maps   | `@each $brkpt, $width in $breakpoints { … }`                     |
| `@while`        | Loop until condition | Rarely needed                                                    |

---

## 6  Math & Built‑in Modules (Sass ≥1.33)

```scss
@use "sass:math";

.container {
  width: math.div(100%, 3); // safe division → 33.333%
}
```

Other core modules: `sass:color`, `sass:list`, `sass:map`, `sass:string`.

---

## 7  Architecture Patterns

### 7.1 The 7‑1 Pattern

```
scss/
├── abstracts/   # variables, functions, mixins
├── base/        # reset, typography
├── components/  # buttons, cards
├── layout/      # header, sidebar, grid
├── pages/       # page‑specific styles
├── themes/      # light, dark
└── vendors/     # third‑party libs
```

### 7.2 Utility‑First with SCSS

Generate spacing helpers on the fly:

```scss
$spacings: (0, .25rem, .5rem, 1rem, 2rem);

@for $i from 1 through length($spacings) {
  $space: nth($spacings, $i);
  .mt-#{$i} { margin-top: $space; }
}
```

---

## 8  Workflow & Tooling

1. **Bundlers** – Vite/Webpack with `sass-loader`, PostCSS, Autoprefixer.
2. **Source maps** – keep `--source-map` on in dev for easier debugging.
3. **Stylelint** – add `stylelint-scss` plugin to enforce conventions.
4. **HMR** – use Vite for instant reload on `.scss` edits.

---

## 9  Hands‑On Project: Theme‑able Card Grid

### 9.1 SCSS

```scss
// _themes.scss
$themes: (
  light: (
    bg: #fff,
    fg: #222,
  ),
  dark: (
    bg: #1a1d24,
    fg: #e5e7eb,
  ),
);

@each $name, $theme in $themes {
  .theme-#{$name} {
    --bg: map.get($theme, bg);
    --fg: map.get($theme, fg);
  }
}

// cards.scss
@use "themes";

.card {
  background: var(--bg);
  color: var(--fg);
  border-radius: .75rem;
  box-shadow: 0 4px 8px rgb(0 0 0 / .05);
  transition: transform .2s;

  &:hover { transform: translateY(-4px); }
}
```

### 9.2 HTML   *(toggle themes by switching `.theme-light` / `.theme-dark` on `<body>`)*

```html
<body class="theme-light">
  <section class="grid">
    <article class="card"> … </article>
  </section>
</body>
```

---

## 10  Best Practices

* **Keep calculations in SCSS, not runtime.**
* **Prefer `@use`/`@forward`**—they scope variables and avoid global leaks.
* **Limit nesting** and avoid deep `&` chains.
* **Document mixins & functions** with comments and unit tests (e.g., True Sass).
* **Run Stylelint + Prettier** to enforce code style.

