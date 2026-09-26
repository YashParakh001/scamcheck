# ScamCheck

## UI design system

The `:root` block at the top of `static/index.html` is the design system. It is the only place raw color values live.

- Before writing any color, radius or shadow, reuse an existing `:root` token (`var(--…)`). For tints use `color-mix(in srgb, var(--token) N%, transparent)`.
- Do not add new hex values, radii or font families outside `:root`.
- If no existing token fits, stop and ask before adding a new one.
- Verdict colors are fixed: `--scam`, `--sus`, `--safe`. Do not use them for anything else.
- Look: an "evidence file" on paper. Ink text, one cobalt accent (`--accent`), 2px ink borders, hard offset shadows (`--shadow`).
- Fonts: `--display` (Fraunces) for headings, `--body` (Bricolage Grotesque) for text, `--mono` (JetBrains Mono) for labels, quotes and numbers.
- Never use Inter, Roboto, system-font stacks as the main font, purple gradients or emoji headings.
- Animation: page elements enter through the `.reveal` class with `--i` stagger. Don't add scattered one-off animations.
