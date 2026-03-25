# Design System Specification: The Tactical Singularity

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Tactical Singularity."** 

This is not a generic dashboard; it is a high-fidelity digital cockpit. While many terminal interfaces feel flat and antiquated, this system utilizes a "High-End Editorial" approach to cyberpunk aesthetics. We achieve this through a tension between rigid, brutalist modularity and fluid, atmospheric depth. We break the standard "web template" look by treating the screen as a physical hardware array—incorporating intentional asymmetry, "glitch" textures, and a hierarchy that prioritizes data-density without sacrificing elegance.

## 2. Colors & Surface Architecture
The color palette is built on a foundation of absolute darkness, punctuated by high-energy luminescence.

*   **Primary Identity (Electric Cyan):** Used for structural framing and system-critical headers. Use the `primary` (#ffffff) and `primary_fixed` (#00fbfb) tokens.
*   **Action Intervention (Neon Pink):** Reserved exclusively for high-priority user actions and destructive states. Use `secondary_container` (#e00460) for buttons and `on_secondary_container` (#fff6f6) for text.

### The "No-Line" Rule (Internal Sectioning)
While the main modular panels utilize a 2px cyan border as requested, **internal sectioning must never use 1px solid lines.** To divide content within a panel:
1.  **Background Shifts:** Use `surface_container_low` (#1c1b1b) against a `surface` (#131313) background.
2.  **Tonal Transitions:** Define hierarchy by nesting surfaces. A `surface_container_highest` (#353534) block should house the most critical data points within a standard panel to provide "lift" without adding visual noise.

### The Glass & Gradient Rule
Floating HUD elements (like tooltips or temporary overlays) must utilize a **Glassmorphic** approach. Use semi-transparent `surface_variant` (#353534) with a `backdrop-filter: blur(8px)`. To give CTAs "soul," apply a subtle linear gradient from `primary_fixed` to `primary_fixed_dim` (#00dddd) at a 45-degree angle.

## 3. Typography
The typography is the "voice" of the machine: cold, precise, and authoritative.

*   **Headline & Display:** All headers (`headline-lg` to `headline-sm`) must be **All-Caps**. This creates a block-like, architectural feel that mirrors the modular panels.
*   **Body & Labels:** Use `body-md` for standard logs. Maintain the monospace rhythm of *Space Grotesk* to ensure column alignment across the tiled interface.
*   **Textural Contrast:** High-end editorial design relies on scale. Contrast a `display-lg` status number (e.g., "99%") with a `label-sm` technical description to create a sophisticated, data-rich aesthetic.

## 4. Elevation & Depth
Depth in this system is achieved through **Tonal Layering** and **Luminescence**, rather than traditional shadows.

*   **The Layering Principle:** Stack containers to create a "Z-axis." 
    *   *Base:* `background` (#050505)
    *   *Panel:* `surface_container` (#201f1f)
    *   *Interactive Card:* `surface_container_high` (#2a2a2a)
*   **Glow Elevation:** Instead of dark drop shadows, use `primary` (#ffffff) with a 10px-20px spread at 15% opacity to create a "bloom" effect around active panels, mimicking the glow of a CRT monitor.
*   **The "Ghost Border" Fallback:** For non-critical containment (like input fields), use the `outline_variant` (#3a4a49) at 20% opacity. Never use 100% opaque borders for secondary elements.

## 5. Components

### Modular Panels (The Core)
*   **Structure:** 2px solid border using `primary_fixed`. 0px border radius (referencing the **Roundedness Scale**).
*   **Header:** A solid `primary_fixed` bar with `on_primary_fixed` text. Every header must begin with the `>` symbol (e.g., `>STATUS_REPORT`).
*   **Effects:** Apply a persistent `noise-texture.png` overlay at 3% opacity and a `scanline` CSS animation (horizontal lines moving vertically) to the panel background.

### Buttons
*   **Primary (LAUNCH):** Background `secondary_container` (#e00460). Text `on_secondary_container` in All-Caps. On hover, apply a 2px "offset" glitch effect where the button clones move slightly left/right in cyan and pink.
*   **Secondary:** Ghost style. `primary_fixed` 2px border, transparent background, text in All-Caps.

### Input Fields
*   **Style:** `surface_container_lowest` background. No top/left/right borders—only a bottom border (2px) using `primary_fixed`. 
*   **Active State:** The bottom border glows and the cursor should be a solid `primary_fixed` block that blinks.

### Selection Chips
*   **Unselected:** `surface_container_high` background with `on_surface_variant` text.
*   **Selected:** `primary_fixed` background with `on_primary_fixed` text. Square corners only.

## 6. Do's and Don'ts

### Do:
*   **Use Intentional Asymmetry:** If three panels are in a row, make one 1.5x wider than the others to break the "bootstrap" grid feel.
*   **Embrace the Glitch:** Add a 100ms "flicker" animation when a panel first loads or when a user clicks a button.
*   **Strict Monospace Alignment:** Ensure all text labels in a column align perfectly to the same X-coordinate to maintain the terminal "grid" logic.

### Don't:
*   **No Rounded Corners:** Absolute 0px radius across the board. Rounding breaks the retro-futurist immersion.
*   **No Standard Shadows:** Never use `rgba(0,0,0,0.5)` shadows. Use luminescence (glows) or background color shifts to define depth.
*   **No Generic Icons:** Avoid Material or FontAwesome icons. Use ASCII-style characters (e.g., `[+]`, `[x]`, `==>`) or custom-drawn, pixel-perfect geometric SVG icons.
*   **No 1px Lines:** As per the "No-Line" rule, avoid thin, wimpy dividers. If it needs a line, make it a 2px structural border or a color-block transition.