# Design System Specification: High-Contrast Retro-Futurism

## 1. Overview & Creative North Star
**Creative North Star: "The Obsidian Architect"**

This design system is not a mere "dark mode" theme; it is a digital manifest of 1980s high-end terminal hardware. It rejects the soft, approachable "SaaS-blue" aesthetics of the modern web in favor of a rigid, authoritative, and immersive command-line experience. 

The system breaks the "template" look by utilizing **Intentional Asymmetry**. Instead of balanced grids, we use heavy left-aligned typographic blocks contrasted against wide, empty "dead zones" (Pitch Black space). Overlapping elements—such as status modules floating over scanline-textured backgrounds—create a sense of a deep, multi-layered CRT monitor. Every interaction should feel like an intentional command, not a casual click.

---

## 2. Colors & Surface Philosophy

The palette is rooted in absolute contrast. We utilize a "Pitch Black" foundation to ensure the Electric Cyan and Neon Magenta "emit light" rather than just sitting on a page.

### Color Tokens
*   **Surface (Pitch Black):** `#050505` (Use `surface-container-lowest` for the absolute base).
*   **Primary (Electric Cyan):** `#00ffff` (For primary borders, telemetry data, and critical text).
*   **Secondary (Neon Magenta):** `#ff00ff` (Reserved for highlights, progress indicators, and "active" states).
*   **Neutral/Outline:** `outline-variant` at 20% opacity for non-critical structural hints.

### The "No-Line" Rule & Surface Hierarchy
Standard 1px solid borders are strictly prohibited for layout sectioning. In this system, boundaries are defined by **Light Emission** or **Tonal Shifts**:
*   **Nesting:** A `surface-container-high` (`#2a2a2a`) module should sit on a `surface` (`#131313`) background to imply physical depth.
*   **Glass & Gradient:** For high-end floating modals, use a backdrop-blur (12px) with a semi-transparent `surface-variant`. Apply a subtle linear gradient from `primary` to `primary-container` on the top edge only to simulate a glowing bezel.
*   **Signature Texture:** All main surfaces must include a `noise-texture` overlay at 3% opacity and a fixed `scanline` CSS pattern to prevent the pitch-black areas from feeling "dead."

---

## 3. Typography
We utilize a single-family Monospace system (**Space Grotesk** for proportional balance with a monospace "feel") to maintain the terminal aesthetic while ensuring professional legibility.

*   **Display-LG (3.5rem):** Reserved for system-level headers. Should always be uppercase with `letter-spacing: -0.05em`.
*   **Headline-SM (1.5rem):** Used for section titles. Pair with a `secondary` (Magenta) highlight character (e.g., `> HEADER`).
*   **Body-MD (0.875rem):** The workhorse. High line-height (1.6) is required to offset the high-contrast fatigue.
*   **Label-SM (0.6875rem):** Used for "metadata" (timestamps, coordinates, file sizes).

**Hierarchy Principle:** Identity is conveyed through **Monospaced Precision**. Use `title-sm` for interactive labels to mimic a functional BIOS environment.

---

## 4. Elevation & Depth: The Layering Principle

Traditional dropshadows are banned. In a terminal, depth is "optical glow" or "tonal stacking."

*   **Tonal Layering:** To lift a card, move from `surface-container-low` to `surface-container-highest`. The higher the tier, the more "backlight" the component appears to have.
*   **The "Ghost Border":** For containment, use the `outline-variant` token at 10% opacity. It should be barely visible, acting as a "hint" of a container rather than a hard wall.
*   **Ambient Glow:** Floating elements (like Tooltips) use `box-shadow: 0 0 12px rgba(0, 255, 255, 0.2)`. This simulates light bleeding from the "phosphor screen."
*   **Glitch Displacements:** On hover, high-priority elements should trigger a 150ms "glitch" animation—a horizontal shift of 2px with a momentary color-split effect.

---

## 5. Components

### Buttons
*   **Primary:** No background fill. `0px` radius. `1px` border using `primary` (Cyan) with a `box-shadow: 0 0 8px #00ffff`. Text is always uppercase.
*   **Secondary:** Magenta text, no border. On hover, a scanline-patterned background fill appears at 20% opacity.
*   **Tertiary:** Low-opacity Cyan text with a leading `[ ]` bracket character.

### Input Fields
*   **Style:** Underline only (2px Cyan). The cursor should be a solid Magenta block (`#ff00ff`) that blinks at a 500ms interval.
*   **States:** Error states switch the entire glow and text to `error` (`#ffb4ab`), mimicking a system-wide alert.

### Cards & Lists
*   **Forbid Divider Lines:** Use `24` (5.5rem) vertical spacing to separate groups. 
*   **List Items:** Every list item must be preceded by a hex-code index (e.g., `0x01`, `0x02`) in `label-sm` to maintain the "Data Terminal" feel.

### Progress Bars
*   **Style:** Segmented blocks rather than a smooth fill. Use `secondary` (Magenta) for the fill blocks. Each segment represents 5% of the total.

---

## 6. Do’s and Don’ts

### Do:
*   **DO** use intentional asymmetry. Leave the right 1/3rd of a dashboard empty for "system telemetry" or purely aesthetic data noise.
*   **DO** use 0px roundedness for everything. The system is brutal and sharp.
*   **DO** ensure all text passes AA accessibility against the `#050505` background.

### Don’t:
*   **DON’T** use standard "drop shadows." They break the illusion of a flat CRT screen.
*   **DON’T** use "Border Radius." If a corner must be softened, use a 45-degree "clipped corner" (chamfer), not a curve.
*   **DON’T** use generic icons. Use ASCII-inspired icons or custom-stroked Cyan SVG glyphs with 1.5px stroke widths.

---

## 7. Signature Interaction: The "Boot Sequence"
Upon page load, components must not simply "fade in." They should use a "staggered-wipe" animation—appearing line-by-line from top to bottom, mimicking the slow data-draw of an 80s terminal.