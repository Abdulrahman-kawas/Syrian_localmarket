# DESIGN_SYSTEM.md — Visual Language & Tokens

> Companion to `BUILD_PROMPT.md` and `PROJECT_MAP.md`. This is the **single source of truth for the app's look and motion**. Every color, size, and animation below is taken directly from the approved prototype (`app_design.html`). Agents must implement these values exactly — do not substitute "close enough" colors or fonts.
> **Target:** React Native + Expo. Tokens map to a theme object consumed via context; light/dark are switched at runtime; RTL/LTR via `I18nManager` + logical `start`/`end`.

---

## 1. Brand DNA

- **Concept:** *"Fresh, but on a clock."* The product rescues good food before it expires — so the design feels **premium and kind**, never a shouty clearance. Dignity for buyers of every income level.
- **Signature element:** the **brass countdown ring** (and ticking mini-timers). This is the one bold, memorable device. Everything else stays quiet around it.
- **Feel:** modern, luxurious, calm, highly readable — in both day and night.

---

## 2. Color Tokens

### 2.1 Brand constants (theme-independent)
| Token | Hex |
|---|---|
| `pine` | `#0F3D2E` |
| `pine600` | `#155540` |
| `brass` | `#C9A24B` |
| `brassSoft` | `#D8B876` |
| `coral` (urgent only) | `#E8763A` |
| `ivory` | `#F6F2E9` |
| `ink` | `#0A1F17` |

### 2.2 Semantic tokens — LIGHT (day)
| Token | Value | Use |
|---|---|---|
| `bg` | `#F6F2E9` | app background (warm ivory) |
| `bgElev` | `#FFFFFF` | cards, sheets, elevated surfaces |
| `bgSunk` | `#EEE8DA` | search bars, inset fields, chips (off) |
| `text` | `#132C22` | primary text |
| `textSoft` | `#5C6B63` | secondary text, captions |
| `line` | `rgba(15,61,46,0.12)` | borders, dividers |
| `primary` | `#0F3D2E` (pine) | primary buttons, active nav, CTAs |
| `onPrimary` | `#F6F2E9` | text/icon on primary |
| `accent` | `#C9A24B` (brass) | prices, links, highlights |

### 2.3 Semantic tokens — DARK (night)
| Token | Value | Use |
|---|---|---|
| `bg` | `#0A1F17` | app background (green-black) |
| `bgElev` | `#122A20` | cards, sheets |
| `bgSunk` | `#0E241B` | inset fields, chips (off) |
| `text` | `#EDE7D6` | primary text |
| `textSoft` | `#9DB0A5` | secondary text |
| `line` | `rgba(214,203,168,0.14)` | borders, dividers |
| `primary` | `#C9A24B` (brass) | primary buttons, active nav |
| `onPrimary` | `#0A1F17` | text/icon on primary |
| `accent` | `#D8B876` (brassSoft) | prices, links |

> **Note the theme inversion:** in light mode the primary action is **pine green**; in dark mode it becomes **brass**. This keeps CTAs luxurious and legible on each background.

### 2.4 Status & map tokens
| Token | Light | Dark |
|---|---|---|
| `urgent` (coral) | `#E8763A` | `#E8763A` |
| `mapBg` | `#E7E2D3` | `#0E2419` |
| `mapRoad` | `#D8D2C0` | `#173322` |
| `mapPark` | `#DDE6CE` | `#12321F` |
| `mapWater` | `#CFE0DB` | `#0F2E2C` |

---

## 3. Typography

- **Arabic + display + body:** **Tajawal** (weights 400/500/700/800). Arabic is the primary language — set it first.
- **Latin/English:** **Plus Jakarta Sans** (500/600/700/800).
- Load both (Expo: `expo-font` / Google Fonts). Choose family per active language.
- **Numerals in countdowns and prices use tabular figures** (`fontVariant: ['tabular-nums']`) so digits don't jump.

### Type scale (dp)
| Role | Size | Weight | Notes |
|---|---|---|---|
| Screen headline | 26 | 800 | letter-spacing ≈ −0.02em, line-height 1.2 |
| Section title | 17 | 800 | −0.01em |
| Card / list title | 16 | 700 | truncate to 1 line |
| Body | 15 | 500 | line-height 1.6–1.7 |
| Price (now, hero) | 24 | 800 | `accent` color |
| Price (now, card) | 17 | 800 | `accent` color |
| Price (was) | 14 | — | `textSoft`, line-through |
| Caption / meta | 12–13 | 500–700 | `textSoft` |
| Micro (pills, labels) | 10–11 | 800 | uppercase for eyebrows only |

---

## 4. Spacing, Radius, Elevation

- **Spacing scale (dp):** 4, 8, 12, 14, 16, 18, 24. Screen horizontal padding = **18**.
- **Radii (dp):** buttons **16**, cards **20–24**, hero card **24**, QR card **26**, thumbnails **15**, chips/pills/badges **999** (full), FAB **18**, device screen corners large.
- **Shadows:**
  - Light card: `0 12px 30px -14px rgba(15,61,46,0.35)`
  - Dark card: `0 18px 40px -18px rgba(0,0,0,0.7)`
  - Primary button glow: `0 14px 30px -12px (primary @70%)`
- Elevated surfaces use `bgElev` + border `line` + the card shadow. Keep elevation subtle; let the countdown ring be the focal energy.

---

## 5. Motion (restrained, purposeful)

Implement with `react-native-reanimated` (or Moti). **Respect reduced-motion** (`AccessibilityInfo.isReduceMotionEnabled`) — disable all non-essential animation when on.

| Motion | Spec |
|---|---|
| Theme switch | cross-fade colors ~500ms ease |
| Screen change | fade + 10dp rise, ~400ms ease |
| Press feedback | scale to 0.97–0.985, ~150–180ms |
| Card entrance | staggered rise (14dp + fade), 60ms step delay |
| Countdown ring | gentle glow pulse, ~2.4s loop (brass drop-shadow in/out) |
| Map pins | drop-in from above with slight overshoot, staggered |
| "Me" marker & urgent dot | soft radial pulse, ~2.2s loop (coral/brass) |
| Primary CTA | slow diagonal shine sweep, ~3.4s loop (very subtle) |
| QR scan line | vertical sweep, ~2.6s ease-in-out loop |
| Live timers | tick every 1s, `mm:ss`, tabular figures |

> Rule: motion should feel like the product breathing, not fireworks. If in doubt, slow it down and reduce it.

---

## 6. Core Components

### 6.1 Buttons
- **Primary:** bg `primary`, text `onPrimary`, radius 16, padding 15dp, weight 800, optional shine sweep. Icon 18dp, gap 8.
- **Ghost / icon:** bg `bgSunk`, border `line`, text `text`, radius 16 (icon buttons 54dp square).
- Action dock (detail screen): ghost call + chat icons **+** full-width primary "Get this deal / استلم الصفقة", pinned above the tab bar with a fade backdrop.

### 6.2 Chips (filters)
- Off: bg `bgElev`, border `line`, text `textSoft`, weight 700, radius 999, padding 9×15, leading emoji.
- On: bg `primary`, text `onPrimary`, no border. Horizontal scroll, hidden scrollbar.

### 6.3 List card
- Row: 88dp rounded thumb (gradient tint by category) + main column. Radius 20, `bgElev`, border `line`, card shadow.
- Thumb carries a **type pill** (bottom-start): `expiry` = coral bg/white; `market` = pine bg/brass text.
- Foot: price block (`now` accent + `was` struck) and either a **timer pill** (coral, tabular) or a **save badge**.
- Optional **stock bar**: 5dp track (`bgSunk`) + gradient fill (`brass→coral`), with "X left / باقي X".

### 6.4 Hero rescue card (the star)
- Pine gradient bg + brass radial glow, 150dp photo zone, "rescue" tag (coral, ⏳) top-start, gradient scrim bottom.
- Body: title (ivory), meta, then price block + **countdown ring** on the trailing side.

### 6.5 Countdown ring — signature spec
- 66dp circle, SVG, rotated −90°. Track stroke `ivory@18%` width 6; progress stroke `brass` width 6, round cap, brass drop-shadow with the glow-pulse loop.
- Center: `mm:ss` (800, tabular) + tiny label ("left / متبقّي").
- Also used compact in the detail price card (number + "ends in / تنتهي بعد").

### 6.6 Type pills / badges
- `expiry`: coral bg, white, 800, radius 8. `market`: pine bg, brassSoft text.
- `save`: subtle — `bgSunk` bg, `accent` text, border `line`.

### 6.7 Map
- Stylized tiles using `mapBg/road/park/water` tokens (both themes). Floating search bar (elevated). **Seller pins** = bubble (emoji + coral discount) → stem → pine foot dot with halo. **"Me"** = brass dot, `bgElev` ring, pulsing halo. Bottom **sheet** with grabber + one featured listing.

### 6.8 Tab bar
- Height 84dp, translucent `bgElev` + blur, top border `line`. 4 tabs + a **center FAB** (primary, 52dp, radius 18, −14dp lift) for the QR scanner. Active tab: `primary` color, icon lifts 2dp, 3dp pill indicator above.

### 6.9 QR proof screen
- White QR frame 196dp, radius 20, 4 pine corner brackets, mosaic modules (pine on white) that fade in, coral scan line sweeping. Product row (emoji + name + price/shop). **Info note** with the rule: *"No in-app payment. Only the seller confirms — no confirmation, no proof."* Actions: Print (ghost) + Done (solid).

### 6.10 Safety note (detail)
- Shield icon + brass-tinted card: *"Please inspect the product on pickup. The platform only connects sellers and buyers."* Always present on near-expiry items.

---

## 7. Iconography
- Line icons, 24 viewBox, stroke width 2 (2.2–2.4 for small), round caps/joins. Filled only for the verified badge and stars. Keep a single consistent set (e.g., Lucide) across the app.

---

## 8. RTL / Bilingual Rules (critical)
- **Arabic (RTL) is the default**; English (LTR) via toggle. Use `I18nManager` and **logical properties** (`start`/`end`, `marginStart`, `paddingEnd`) everywhere — never hardcode left/right.
- **Mirror** layouts on RTL; **flip directional icons** (back chevron, etc.). Do not mirror the QR, logos, or media.
- All strings come from `i18n/ar` and `i18n/en` — **no hardcoded text**. Switch font family with the language.
- Numbers/prices: keep currency glyph placement correct per locale; use tabular figures for timers.

---

## 9. Voice & Copy
- Arabic-first, warm, plain. Name things by what the user does: "استلم الصفقة" (Get this deal), "طباعة" (Print), "تم" (Done).
- Framing is **rescue, not clearance**: "فرص اليوم / Today's rescues", "تنتهي بعد / ends in".
- Errors/empty states: direct and actionable, in the interface's voice — never apologetic or vague.
- Reused key line (trust): *"بدون تأكيد لا يوجد إثبات — No confirmation, no proof."*

---

## 10. Implementation checklist for agents
- [ ] Theme object with **both** palettes (§2), switchable at runtime, persisted.
- [ ] Fonts loaded (Tajawal + Plus Jakarta Sans); family follows language.
- [ ] Logical-property styling; `I18nManager` RTL verified by flipping languages.
- [ ] Reduced-motion honored; motion specs (§5) via Reanimated.
- [ ] Components built to §6 specs; countdown ring is a shared component.
- [ ] Tabular figures on all timers/prices.
- [ ] AA contrast confirmed in **both** themes.

*Placeholder brand name in the prototype: **فرصة / Farṣa** ("an opportunity"). Rename freely — only the name, not the tokens.*
