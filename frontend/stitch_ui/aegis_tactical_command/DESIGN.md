# DESIGN SYSTEM SPECIFICATION: TACTICAL TERMINAL ARCHITECTURE

## 1. Overview & Creative North Star
**Creative North Star: "The Sovereign Hard-Line"**

This design system rejects the "soft" trends of modern SaaS. It is a high-fidelity, high-stakes interface inspired by cold-war era telemetry and near-future orbital defense consoles. The aesthetic is **Brutalist Cyberpunk**: a world of absolute blacks, sharp geometries, and phosphorescent data. 

To move beyond a generic "hacker" template, we utilize **Intentional Asymmetry**. Dashboards should not be perfectly balanced; they should feel like a modular rack of hardware where different units (widgets) are "slotted" into a physical frame. We replace traditional airiness with "Technical Density"—using the Monospace typeface to create a rhythmic, machine-readable texture across the screen.

---

## 2. Colors: The High-Contrast Vacuum
The palette is built on a "Void-State" philosophy. Content does not sit *on* the background; it is *carved out* of the darkness.

*   **Background (#050505):** The absolute floor. 
*   **Primary (#FFFFFF) & Primary Container (#00FBFB):** Used for critical data readouts. The `primary_container` is our "Electric Cyan" neon source.
*   **Secondary (#FFB778):** Reserved for latency anomalies and secondary warnings.
*   **Tertiary/Error (#FFB4AB):** Reserved strictly for system infections or critical breaches.

### The "No-Line" Rule
Standard 1px borders are strictly prohibited for layout sectioning. Separation is achieved through:
1.  **Background Shifts:** Moving from `surface_container_lowest` (#0E0E0E) to `surface_container` (#201F1F).
2.  **Glow-Defined Boundaries:** Use the `primary_container` (#00FBFB) with a CSS `box-shadow: 0 0 8px rgba(0, 251, 251, 0.4)` to define the outer edge of a module rather than a solid line.

### Surface Hierarchy & Nesting
Treat the UI as a physical motherboard. 
*   **The Chassis:** Use `surface_dim` (#131313) for the main application shell.
*   **The Modules:** Use `surface_container_low` (#1C1B1B) for individual data panels.
*   **The Active Components:** Use `surface_container_high` (#2A2A2A) for focused or hovering states.

### The "Glass & Gradient" Rule
To add "soul," interactive elements should use a **Sub-Surface Gradient**. A button shouldn't just be cyan; it should transition from `on_primary_container` (#007070) at the bottom to `primary_fixed` (#00FBFB) at the top, mimicking the flicker of a gas-discharge tube.

---

## 3. Typography: Monospace Authority
We use **Space Grotesk** as our primary driver, but it must be tracked and set to feel like a terminal.

*   **Display (3.5rem - 2.25rem):** High-impact system status (e.g., "SYSTEM: DEFCON 1"). Use `all-caps` with `-2%` letter spacing.
*   **Headline (2rem - 1.5rem):** Module titles. These define the "Sovereign Hard-Line."
*   **Body (1rem - 0.75rem):** Technical readouts and logs. 
*   **Label (0.75rem - 0.68rem):** For metadata, timestamps, and coordinate values.

**Typography as Brand:** The rigid alignment of Space Grotesk creates a "grid-within-a-grid" feel. Every character should feel like it occupies a specific byte of memory.

---

## 4. Elevation & Depth: Tonal Layering
Traditional shadows have no place here. In a terminal, depth is light.

*   **The Layering Principle:** Instead of lifting a card with a shadow, "sink" the background. A card sits on `surface_container_low`; the area *around* it should be `surface_container_lowest`. 
*   **Ambient Glows:** When a component is "active," it emits light. Use a 15% opacity `primary` color glow that bleeds into the surrounding `surface`.
*   **The "Ghost Border" Fallback:** For secondary modules, use the `outline_variant` (#3A4A49) at **15% opacity**. It should be barely visible—a "ghost" of a container.
*   **CRT Scanline Overlay:** Apply a global fixed overlay using a linear gradient of `rgba(255,255,255, 0.03)` every 2px. This unifies the layers under a "physical screen" texture.

---

## 5. Components

### Buttons
*   **Primary:** Sharp corners (`0px`). Background is `primary_container`. Text is `on_primary_fixed` (#002020). Add a `1px` inner-stroke of `primary` for a "lit" edge.
*   **Tertiary (The Ghost):** No background. `outline` color text. On hover, the text flickers to `primary_fixed`.

### Data Modules (Cards)
*   **Rule:** Forbid divider lines. 
*   **Structure:** Use `spacing.4` (0.9rem) to separate headers from content. Use a small "corner bracket" (a 4px L-shape) in `primary_container` at the top-left and bottom-right to define the container limits.

### Input Fields
*   **State:** Default state is a `surface_container_highest` background with a `label-sm` floating above the box.
*   **Active:** The border "lights up" with an Electric Cyan glow. The cursor should be a solid block `█` rather than a line.

### System Logs (Lists)
*   Use `body-sm`. Alternate row backgrounds between `surface` and `surface_container_low`. 
*   **Error Row:** Background transitions to `error_container` (#93000A) at 20% opacity.

---

## 6. Do's and Don'ts

### Do:
*   **Embrace the Grid:** Use the `spacing.px` and `spacing.0.5` for micro-adjustments to ensure elements look "mechanically aligned."
*   **Use Visual Glitches:** Occasional 1px offsets or slight color-fringing on hover can enhance the high-security aesthetic.
*   **Prioritize Density:** High-security consoles are about information volume. Don't fear "busy" layouts; fear "empty" ones.

### Don't:
*   **No Rounding:** `0px` is the only acceptable radius. Anything else breaks the "Hard-Line" philosophy.
*   **No Soft Shadows:** If it doesn't look like it's emitting light or carved out of rock, it doesn't belong.
*   **No Standard Blue:** Blue is for consumer apps. Use the Electric Cyan (`primary_container`) for tactical clarity.

---

## 7. Signature Technical Visualization
Every dashboard must include at least one "non-functional" decorative element: a coordinate string, a rolling checksum, or a simulated wave-form in the footer. Use `label-sm` in `outline` color. This reinforces the "Aegis" persona of a system that is constantly processing more data than a human can read.