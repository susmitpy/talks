## Best Practices & Styling Guidelines for Slidev Presentations

These guidelines are synthesized from the recurring patterns and effective techniques found across your presentations on Feature Engineering, AWS Lambda, Kafka, Firestore, and more.

### 1. Global Styling & Theming (The Foundation)

Your most polished presentations establish a strong visual identity right from the start.

**Guideline:** Use a global `<style>` block on the first or second slide to define a consistent theme.

**Best Practices:**

*   **Use CSS Variables (`:root`)**: Define a color palette in `:root` for primary, secondary, accent, background, and code colors. This makes theme changes trivial.
    ```css
    :root {
      /* Theme Colors */
      --slidev-theme-primary: #FFFFFF;
      --slidev-theme-secondary: #FFD43B; /* Python Yellow */
      --slidev-theme-accent: #3776AB;   /* Python Blue */
      --slidev-theme-background: linear-gradient(135deg, #2b2b2b 0%, #1a1a1a 100%);
      --slidev-theme-foreground: #E8E8E8;
      --slidev-code-background: rgba(13, 17, 23, 0.95);
    }
    ```
*   **Style Core Elements**: Apply your theme to fundamental HTML elements (`h1`, `h2`, `p`, `a`, `li`, `table`). This ensures consistency without needing to style every slide individually.
*   **Dramatic Title Slide**: The first slide should be impactful. You often use a custom `div` to override the global styles, ensuring title text is large, bold, and perfectly legible over a background image.
    ```html
    <!-- Override style for the first slide -->
    <div class="h-full flex flex-col justify-center items-center">
      <div style="color: white !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.7);">
        <h1 style="color: white !important; font-size: 3.5rem;">Title</h1>
        <h2 style="color: white !important; background: transparent !important;">Subtitle</h2>
      </div>
    </div>
    ```
*   **Custom Fonts**: For a unique feel (like in the Firestore presentation), define custom fonts in the frontmatter.
    ```yaml
    fonts:
        sans: Roboto
        serif: Roboto Slab
        mono: Fira Code
    ```

### 2. Structural Organization (The Blueprint)

A well-organized project is easy to maintain and reuse.

**Guideline:** Modularize your presentation by separating reusable content into external files.

**Best Practices:**

*   **Use `--- src: ./pages/....md`**: This is the most powerful technique you use. Create a `pages/` directory for common slides that appear in every talk. This follows the DRY (Don't Repeat Yourself) principle.
    *   `./pages/about.md`
    *   `./pages/disclaimer.md`
    *   `./pages/connect.md` (Contact/Socials slide)
    *   `./pages/qa.md` (Q&A slide)
*   **Start with an Agenda**: Always include an "Agenda" or "Roadmap" slide near the beginning. It sets expectations and provides a clear structure for the audience. Using `<v-switch>` or `<v-clicks>` to progressively reveal details is a nice touch.
*   **One Idea Per Slide**: Each slide has a single, clear purpose. Complex topics are broken down into a sequence of simple slides, which improves pacing and comprehension.

### 3. Content & Engagement (The Story)

Your presentations are not just data dumps; they are narratives that engage the audience.

**Guideline:** Treat your presentation as a story with interactive elements.

**Best Practices:**

*   **The "Audience Question" Callout**: You frequently pause to ask the audience a direct question. This is a fantastic engagement technique. Style these questions in a visually distinct callout box to make them stand out.
    ```html
    <div class="text-2xl" style="background: rgba(255, 212, 59, 0.95); padding: 1rem; border-radius: 8px;">
      <b>Audience Question:</b> What does the "C" in "CSV" stand for?
    </div>
    ```
*   **Progressive Reveal with `<v-click>`**: Almost every list and concept is revealed step-by-step using `<v-click>` or `<v-clicks>`. This focuses audience attention and prevents them from reading ahead.
*   **Tell a Story**: Frame the content with a narrative structure:
    1.  **The Problem**: Introduce a simple, relatable problem (e.g., real-time word count).
    2.  **The Complication**: Explain why it's a challenge (e.g., "But what if 100 users...").
    3.  **The Solution**: Present the technology or technique as the hero that solves the problem.
*   **Use Analogies**: Explain complex concepts with simple, relatable analogies (e.g., "Uber for computing," "SAS Tokens are like temporary parking passes").
*   **"When to Use" vs. "When NOT to Use"**: Providing balanced advice by showing both the strengths and limitations of a technology builds credibility and gives the audience practical wisdom.

### 4. Visual Elements (The Visuals)

Visuals are used to clarify, not just decorate.

**Guideline:** Use a mix of diagrams, code, and images to support the key message of each slide.

**Best Practices:**

*   **Mermaid for Diagrams**: Use Mermaid.js for flowcharts, architecture diagrams, and sequence diagrams. It's clean, code-based, and easy to maintain.
    ```mermaid
    graph TD
        A[Data Gathering] --> B[Data Cleaning];
        B --> C[✨ Feature Engineering ✨];
        C --> D[Modelling];
    ```
*   **Focused Code Snippets**: Code blocks are short, syntax-highlighted, and illustrate a single concept. Avoid walls of code. Highlight the most important line if possible.
*   **Memes and Humor**: Use `layout: image` with a relevant meme to break the monotony, add humor, and make a point memorable.
*   **Real-World Screenshots**: For topics like Firestore rules, showing screenshots from browser dev tools or the Firebase console is incredibly effective because it grounds the concept in reality.
*   **QR Codes & Links**: On slides that reference a GitHub repository or project, always include a URL and a QR code for easy access.

### 5. Technical Slidev Features (The Toolkit)

You leverage Slidev's rich feature set to create a dynamic experience.

**Guideline:** Go beyond basic markdown and use Slidev's built-in components and features.

**Best Practices:**

*   **Layouts**: Use frontmatter to switch layouts (`class: text-center`, `layout: image`, `layout: image-left`).
*   **Rich Media Components**: Embed content directly into your slides to make them more dynamic.
    *   `<Tweet id="..."/>`
    *   `<Youtube id="..."/>`
    *   `<SlidevVideo src="..."/>`
*   **Tailwind CSS Classes**: Use utility classes for quick layout adjustments (`grid grid-cols-2`, `mt-8`, `text-center`, `flex items-center`).
*   **Frontmatter Configuration**: Use the frontmatter not just for titles but for controlling theme, transitions, and other global settings.
    ```yaml
    ---
    theme: seriph
    transition: slide-left
    mdc: true
    background: /bg_image.png
    ---
    ```

Speaker notes should be at end of each slide and wrapped in html comment syntax
<!-- Speaker notes go here -->

Slides should be separated by `---`