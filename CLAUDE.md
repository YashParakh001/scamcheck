# ScamCheck

## UI design system

The `:root` block at the top of `static/index.html` is the design system. It is the only place raw color values live.

- Before writing any color, radius or shadow, reuse an existing `:root` token (`var(--…)`). For tints use `color-mix(in srgb, var(--token) N%, transparent)`.
- Do not add new hex values, radii or font families outside `:root`.
- If no existing token fits, stop and ask before adding a new one.
- Light and dark mode: every color token has a dark value in both dark blocks (the `prefers-color-scheme` one and `[data-theme="dark"]`). Keep them in sync.
- Verdict colors are fixed: `--scam`, `--sus`, `--safe`. Do not use them for anything else.
- Look: calm and basic. Paper background, ink text, one cobalt accent (`--accent`), 1px `--line` borders, soft `--shadow`. Verdict color shows as a left border. No decorative patterns or offset shadows.
- Fonts: `--display` (Fraunces) for headings, `--body` (Bricolage Grotesque) for text, `--mono` (JetBrains Mono) for small labels and numbers only.
- Never use Inter, Roboto, system-font stacks as the main font, purple gradients or emoji headings.
- Animation: page elements enter through the `.reveal` class with `--i` stagger. Don't add scattered one-off animations.
