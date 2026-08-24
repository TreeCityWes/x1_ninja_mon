# X1.Ninja Color Brand Guidelines

Source: live site [x1.ninja](https://x1.ninja) and compiled CSS tokens, reviewed 24 Aug 2026.

X1.Ninja is a dark-only DEX screener and analytics surface for the X1 network. The brand reads as stealth hardware: void black, cool steel neutrals, and a single electric cyan that behaves like a targeting reticle.

There are **two blues**. Mixing them up is the fastest way to look off-brand.

| Role | Hex | Where it lives |
| --- | --- | --- |
| **X1 Cyan** | `#00B8FF` | Product UI: links, selected chips, focus, primary actions |
| **Ninja Navy → Mid** | `#003A93` → `#0078C0` | Logo X, headband, “X1” wordmark |

Cyan is the interface. Navy is the mascot. Cyan is never the fill of the big X. Navy is never small UI copy.

## Core palette

### Surfaces

| Token | Hex | RGB | Use |
| --- | --- | --- | --- |
| Void / `bg-primary` | `#000000` | 0, 0, 0 | App canvas |
| Chrome | `#0A0A0F` | 10, 10, 15 | Browser `theme-color` |
| `bg-secondary` | `#0B0F14` | 11, 15, 20 | Sidebar, sticky bars, raised panels |
| `bg-tertiary` | `#121821` | 18, 24, 33 | Nested wells, logo rail |
| `bg-hover` | `#1A2332` | 26, 35, 50 | Row and control hover |
| `border-subtle` | `#1C2430` | 28, 36, 48 | Default 1px rules |
| `border-bright` | `#263244` | 38, 50, 68 | Emphasized edges |

Surfaces are cool (hue ~213–218). Do not warm them up.

### Type

| Token | Hex | On `#000` | Use |
| --- | --- | --- | --- |
| `text-primary` | `#FFFFFF` | 21:1 AAA | Titles, prices, primary labels |
| `text-secondary` | `#9AA4B2` | 8.33:1 AAA | Body, values, helper copy |
| `text-muted` | `#768291` | 5.37:1 AA | Column headers, placeholders |

UI type is **Inter**. Numeric / code type is **JetBrains Mono**.

### Accent and market data

| Token | Hex | On `#000` | Use |
| --- | --- | --- | --- |
| `x1-blue` | `#00B8FF` | 9.30:1 AAA | Interactive brand color |
| `buy-green` | `#00FF9C` | 15.78:1 AAA | Up / buy only |
| `sell-red` | `#FF3355` | 5.86:1 AA | Down / sell only |
| `warn-yellow` | `#FFD166` | 14.56:1 AAA | Caution, pending |

Button label on cyan fills is **black**, never white (white on `#00B8FF` is 2.26:1 and fails).

## Identity colors (logo)

The mark is a navy→cerulean X, a slate ninja with a navy headband and white eyes, gold only on the katana guards, and the wordmark **X1** (blue) **NINJA** (white) on void black.

| Stop | Hex | Use |
| --- | --- | --- |
| Navy | `#003A93` | Dark end of the X, headband |
| Blue | `#0060AE` | Mid X, “X1” letters |
| Mid | `#0078C0` | Light end of the X |
| Steel | `#243030` | Hood / mask |
| Gold | `#C9A227` | Tsuba dots only |

Do not use navy or mid-blue for body text. They fail or barely pass on black.

## How color is used on the site

1. **Almost everything is surface + gray type.** Cyan is sparse: selected Sort chip, search focus, Submit Token, active nav.
2. **Green and red are data, not decoration.** They appear on 1H/24H deltas and trade flashes, then recede.
3. **Opacity is part of the system.** Cyan often shows as `/10`, `/20`, `/25` fills with a solid cyan border or type.
4. **No light mode.** `color-scheme: dark` and `theme-color: #0A0A0F` are hardcoded.

## Pairing recipes

- **Page:** `#000000` canvas, `#0B0F14` chrome, `#1C2430` borders, white titles, `#9AA4B2` body.
- **Selected control:** `bg #00B8FF` at 20% · border and label `#00B8FF`.
- **Primary button:** fill `#00B8FF`, label `#000000`.
- **Up cell:** `#00FF9C`. **Down cell:** `#FF3355`.
- **Logo lockup:** only the identity gradient + white, on `#000000`.

## Do / don’t

**Do**

- Keep the UI ≥90% black/steel, ≤10% cyan.
- Put focus rings and selected states on `#00B8FF`.
- Use black type on solid cyan buttons.
- Keep green/red reserved for market direction.

**Don’t**

- Swap in Tailwind `blue-500`, `sky-400`, or generic neon.
- Set white type on `#00B8FF`.
- Use `#003A93` as a link or small label.
- Introduce beige, purple-black, or a light theme.
- Treat `#39FF14` as brand (it exists as a one-off, not a token).

## Files

- Visual book: [`index.html`](index.html)
- CSS variables: [`tokens.css`](tokens.css)
- Machine-readable: [`tokens.json`](tokens.json)
- Logo: [`assets/logo.png`](assets/logo.png)
