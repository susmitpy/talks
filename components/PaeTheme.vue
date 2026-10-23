<!-- Theme for: Practical AI Engineering (Intelligence बैठक) -->
<!-- Rendered once on the title slide; its <style> block is intentionally global. -->
<!-- Colour = component type, used consistently on every diagram:
     violet = LLM, teal = deterministic code, amber = tools / MCP, sky = data, pink = human -->
<template><span class="hidden" /></template>

<style>
:root {
  --slidev-theme-primary: #ffffff;
  --slidev-theme-background: #111418;
  --slidev-theme-foreground: #e6eaf0;
  --slidev-code-background: #0b0e12;

  --pae-bg: #111418;
  --pae-panel: #1b2028;
  --pae-line: rgba(255, 255, 255, 0.14);
  --pae-fg: #e6eaf0;
  --pae-muted: #8d97a6;
  --pae-llm: #a78bfa;
  --pae-code: #2dd4bf;
  --pae-tool: #fbbf24;
  --pae-data: #60a5fa;
  --pae-human: #f472b6;
  --pae-red: #f87171;
}

.pae,
.pae.slidev-layout {
  background: var(--pae-bg);
  color: var(--pae-fg);
  font-family: Manrope, system-ui, sans-serif;
  text-align: left;
}

/* ---------- type ---------- */
.pae h1 {
  font-size: 2rem;
  line-height: 1.15;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 0.8rem;
}
.pae h1::after {
  content: "";
  display: block;
  width: 3.5rem;
  height: 4px;
  margin-top: 0.45rem;
  background: var(--pae-tool);
  border-radius: 2px;
}
.pae h1.plain::after { display: none; }
.pae h2 { font-size: 1.3rem; font-weight: 700; color: var(--pae-tool); margin-bottom: 0.4rem; }
.pae h3 { font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 0.3rem; }
.pae p, .pae li { font-size: 1.05rem; line-height: 1.5; color: var(--pae-fg); }
.pae b, .pae strong { color: #ffffff; }
.pae a { color: var(--pae-data); text-decoration: none; border-bottom: 1px solid var(--pae-data); }
.pae ul { list-style: none; padding-left: 0; }
.pae ul li { padding-left: 1.2rem; position: relative; margin: 0.35rem 0; }
.pae ul li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.62em;
  width: 0.45rem;
  height: 0.45rem;
  border-radius: 2px;
  background: var(--pae-tool);
}
.pae ol { padding-left: 1.4rem; }
.pae ol li { margin: 0.35rem 0; }
.pae ol li::marker { color: var(--pae-tool); font-weight: 700; }

.pae .eyebrow {
  font-size: 0.8rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--pae-muted);
  margin-bottom: 0.4rem;
}
.pae .muted { color: var(--pae-muted); }
.pae .small { font-size: 0.9rem; line-height: 1.4; }
.pae .tiny { font-size: 0.75rem; line-height: 1.35; }
.pae .llm { color: var(--pae-llm); }
.pae .code { color: var(--pae-code); }
.pae .tool { color: var(--pae-tool); }
.pae .data { color: var(--pae-data); }
.pae .human { color: var(--pae-human); }
.pae .red { color: var(--pae-red); }

/* ---------- key message ---------- */
.pae .key {
  margin-top: 1rem;
  padding: 0.6rem 1rem;
  border-left: 4px solid var(--pae-tool);
  background: var(--pae-panel);
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
}

/* ---------- audience question ---------- */
.pae .question {
  margin-top: 1rem;
  padding: 0.7rem 1.1rem;
  border-radius: 8px;
  background: var(--pae-tool);
  color: #111418;
  font-size: 1.15rem;
  font-weight: 600;
}
.pae .question b { color: #111418; }

/* ---------- cards ---------- */
.pae .card {
  background: var(--pae-panel);
  border: 1px solid var(--pae-line);
  border-top: 4px solid var(--pae-muted);
  border-radius: 8px;
  padding: 0.9rem 1rem;
}
.pae .card p, .pae .card li { font-size: 0.95rem; }
.pae .card p { margin: 0.3rem 0; }
.pae .card.t-llm { border-top-color: var(--pae-llm); }
.pae .card.t-code { border-top-color: var(--pae-code); }
.pae .card.t-tool { border-top-color: var(--pae-tool); }
.pae .card.t-data { border-top-color: var(--pae-data); }
.pae .card.t-human { border-top-color: var(--pae-human); }

/* ---------- block flow (boxes + arrows) ---------- */
.pae .flow { display: flex; align-items: stretch; gap: 0.5rem; }
.pae .flow .node {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  background: var(--pae-panel);
  border: 2px solid var(--pae-line);
  border-radius: 10px;
  padding: 0.8rem 0.5rem;
  font-weight: 700;
  font-size: 1.05rem;
  color: #ffffff;
}
.pae .flow .node small { display: block; font-weight: 500; font-size: 0.78rem; color: var(--pae-muted); margin-top: 0.25rem; }
.pae .flow .arrow { display: flex; align-items: center; color: var(--pae-muted); font-size: 1.4rem; }
.pae .node.n-llm { border-color: var(--pae-llm); }
.pae .node.n-code { border-color: var(--pae-code); }
.pae .node.n-tool { border-color: var(--pae-tool); }
.pae .node.n-data { border-color: var(--pae-data); }
.pae .node.n-human { border-color: var(--pae-human); }
.pae .node.n-red { border-color: var(--pae-red); }

/* ---------- legend ---------- */
.pae .legend { display: flex; gap: 1.2rem; font-size: 0.8rem; color: var(--pae-muted); }
.pae .legend span::before {
  content: "";
  display: inline-block;
  width: 0.7rem;
  height: 0.7rem;
  border-radius: 2px;
  margin-right: 0.35rem;
  vertical-align: -1px;
  background: currentColor;
}
.pae .legend span { color: var(--pae-muted); }
.pae .legend .l-llm::before { background: var(--pae-llm); }
.pae .legend .l-code::before { background: var(--pae-code); }
.pae .legend .l-tool::before { background: var(--pae-tool); }
.pae .legend .l-data::before { background: var(--pae-data); }
.pae .legend .l-human::before { background: var(--pae-human); }

/* ---------- placeholder for speaker-supplied visuals ---------- */
.pae .placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  border: 2px dashed var(--pae-tool);
  border-radius: 10px;
  color: var(--pae-tool);
  font-size: 0.95rem;
  padding: 1rem;
  min-height: 8rem;
}

/* ---------- shots ---------- */
.pae .shot {
  border: 1px solid var(--pae-line);
  border-radius: 8px;
  background: #ffffff;
  max-width: 100%;
}

/* ---------- code ---------- */
.pae .slidev-code { font-size: 0.85rem !important; line-height: 1.5 !important; }

/* ---------- tables ---------- */
.pae table { width: 100%; border-collapse: collapse; }
.pae th { color: var(--pae-tool); font-weight: 700; text-align: left; }
.pae th, .pae td { border-bottom: 1px solid var(--pae-line); padding: 0.4rem 0.5rem; font-size: 1rem; }

/* ---------- footer (global-bottom.vue) ---------- */
.pae footer, footer { color: var(--pae-muted); }
</style>
