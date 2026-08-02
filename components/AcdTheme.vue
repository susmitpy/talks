<!-- Theme for: Don't Call the Model Twice (AWS Community Day Mumbai 2026) -->
<!-- Rendered once on the title slide; its <style> block is intentionally global. -->
<template><span class="hidden" /></template>

<style>
:root {
  --acd-bg: #101a2b;
  --acd-panel: #17233a;
  --acd-line: rgba(255, 255, 255, 0.12);
  --acd-fg: #f2f6fc;
  --acd-muted: #93a3bc;
  --acd-orange: #ff9900;
  --acd-teal: #01a88d;
  --acd-sky: #4db8ff;
  --acd-red: #ff6b6b;
  --acd-code-bg: #0b1322;
}

.acd,
.acd.slidev-layout {
  background: var(--acd-bg);
  color: var(--acd-fg);
  font-family: Manrope, system-ui, sans-serif;
  text-align: left;
}

/* ---------- type ---------- */
.acd h1 {
  font-size: 2.5rem;
  line-height: 1.15;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 0.9rem;
}
.acd h1::after {
  content: "";
  display: block;
  width: 3.5rem;
  height: 4px;
  margin-top: 0.45rem;
  background: var(--acd-orange);
  border-radius: 2px;
}
.acd h1.plain::after { display: none; }
.acd h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--acd-orange);
  margin-bottom: 0.4rem;
}
.acd h3 { font-size: 1.05rem; font-weight: 700; color: var(--acd-fg); }
.acd p, .acd li { font-size: 1.05rem; line-height: 1.5; color: #e2e9f4; }
.acd b, .acd strong { color: #ffffff; }
.acd a { color: var(--acd-sky); text-decoration: none; border-bottom: 1px solid var(--acd-sky); }
.acd ul { list-style: none; padding-left: 0; }
.acd ul li { padding-left: 1.1rem; position: relative; margin: 0.3rem 0; }
.acd ul li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.62em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--acd-orange);
}

.acd .eyebrow {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--acd-orange);
  margin-bottom: 0.5rem;
}
.acd .muted { color: var(--acd-muted); }
.acd .tiny { font-size: 0.78rem; line-height: 1.4; }
.acd .compact { font-size: 0.95rem; line-height: 1.4; }
.acd .orange { color: var(--acd-orange); }
.acd .teal { color: var(--acd-teal); }
.acd .sky { color: var(--acd-sky); }
.acd .red { color: var(--acd-red); }
.acd .big { font-size: 3.4rem; line-height: 1.1; }
.acd .lede { font-size: 1.5rem; line-height: 1.5; margin-top: 2rem; }
.acd .lede.narrow { max-width: 58rem; margin-left: auto; margin-right: auto; }

/* ---------- surfaces ---------- */
.acd .frame {
  background: var(--acd-panel);
  border: 1px solid var(--acd-line);
  border-top: 3px solid var(--acd-line);
  border-radius: 12px;
  padding: 1rem 1.1rem;
}
.acd .frame.t-orange { border-top-color: var(--acd-orange); }
.acd .frame.t-teal { border-top-color: var(--acd-teal); }
.acd .frame.t-sky { border-top-color: var(--acd-sky); }
.acd .frame.t-red { border-top-color: var(--acd-red); }
.acd .frame p { margin: 0.35rem 0; }

.acd .callout {
  background: rgba(255, 153, 0, 0.1);
  border: 1px solid rgba(255, 153, 0, 0.52);
  border-radius: 8px;
  padding: 0.8rem 1rem;
  font-size: 1.05rem;
}

/* ---------- opening scenario ---------- */
.acd .scenario {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.55rem 1rem;
}
.acd .scenario-step {
  display: flex;
  align-items: baseline;
  gap: 0.7rem;
  padding: 0.55rem 0.75rem;
  background: var(--acd-panel);
  border: 1px solid var(--acd-line);
  border-radius: 8px;
  font-size: 0.95rem;
  line-height: 1.35;
}
.acd .scenario-step b { min-width: 1.7rem; }
.acd .scenario-step strong { margin-left: auto; color: var(--acd-teal); white-space: nowrap; }
.acd .scenario-step.success { border-color: rgba(1, 168, 141, 0.55); }
.acd .scenario-step.danger { border-color: rgba(255, 107, 107, 0.6); grid-column: 1 / -1; }
.acd .question {
  background: rgba(255, 107, 107, 0.12);
  border: 1px solid rgba(255, 107, 107, 0.6);
  border-radius: 8px;
  padding: 0.7rem 1rem;
  font-size: 1.15rem;
  color: #ffe8e8;
}

/* ---------- code ---------- */
.acd .slidev-code-wrapper, .acd pre {
  background: var(--acd-code-bg) !important;
  border: 1px solid var(--acd-line);
  border-radius: 10px;
}
.acd pre, .acd code { font-family: "JetBrains Mono", monospace; }
.acd .slidev-code { font-size: 0.76rem !important; line-height: 1.45 !important; }
.acd .slidev-code { filter: saturate(1.15) brightness(1.18); }
.acd :not(pre) > code {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 0.05em 0.35em;
  font-size: 0.9em;
  color: var(--acd-sky);
}

/* ---------- coverage matrix ---------- */
.acd .matrix {
  display: grid;
  grid-template-columns: 8rem repeat(6, 1fr);
  gap: 4px;
  font-size: 0.85rem;
}
.acd .matrix > div {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 6px;
  padding: 0.3rem 0.4rem;
  text-align: center;
  min-height: 1.9rem;
}
.acd .matrix .head { color: var(--acd-muted); font-weight: 700; background: none; }
.acd .matrix .row { text-align: left; font-weight: 600; background: none; color: var(--acd-fg); }
.acd .matrix .yes { background: rgba(1, 168, 141, 0.22); color: #4fe3c6; font-weight: 700; }
.acd .matrix .dup { background: rgba(255, 153, 0, 0.22); color: var(--acd-orange); font-weight: 700; }
.acd .matrix .no { background: rgba(255, 107, 107, 0.18); color: var(--acd-red); font-weight: 700; }

/* ---------- batch strip ---------- */
.acd .strip { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.6rem; }
.acd .chip {
  background: var(--acd-panel);
  border: 1px solid var(--acd-line);
  border-radius: 10px;
  padding: 0.55rem;
  text-align: center;
}
.acd .chip .mark { font-size: 1.5rem; line-height: 1.1; font-weight: 700; }
.acd .chip small { display: block; font-size: 0.7rem; color: var(--acd-muted); }
.acd .chip.done { border-color: rgba(1, 168, 141, 0.6); }
.acd .chip.done .mark { color: var(--acd-teal); }
.acd .chip.failed { border-color: rgba(255, 107, 107, 0.6); }
.acd .chip.failed .mark { color: var(--acd-red); }
.acd .chip.repair { border-color: rgba(255, 153, 0, 0.7); }
.acd .chip.repair .mark { color: var(--acd-orange); }
.acd .chip.pending .mark { color: var(--acd-muted); }

/* ---------- flow ---------- */
.acd .flow { display: flex; align-items: stretch; gap: 0.4rem; }
.acd .flow .node {
  flex: 1;
  background: var(--acd-panel);
  border: 1px solid var(--acd-line);
  border-radius: 10px;
  padding: 0.6rem;
  text-align: center;
  font-weight: 700;
  font-size: 0.95rem;
}
.acd .flow .node.hot { border-color: var(--acd-orange); color: var(--acd-orange); }
.acd .flow .node small { display: block; font-weight: 500; font-size: 0.7rem; color: var(--acd-muted); margin-top: 0.25rem; }
.acd .flow .arrow { align-self: center; color: var(--acd-muted); font-size: 1.1rem; }

/* ---------- timeline ---------- */
.acd .steps { border-left: 2px solid var(--acd-line); padding-left: 1rem; }
.acd .steps > div { position: relative; margin: 0.55rem 0; font-size: 1rem; }
.acd .steps > div::before {
  content: "";
  position: absolute;
  left: -1.42rem;
  top: 0.5em;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--acd-orange);
}

/* ---------- record / json ---------- */
.acd .record {
  background: var(--acd-code-bg);
  border: 1px solid var(--acd-line);
  border-radius: 10px;
  padding: 0.9rem 1.1rem;
  font-family: "JetBrains Mono", monospace;
  font-size: 0.85rem;
  line-height: 1.75;
  color: #cfe0f5;
}
.acd .record > div { white-space: pre; }
.acd .record .pin { color: var(--acd-orange); font-weight: 600; }

/* ---------- table ---------- */
.acd table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.acd th, .acd td { text-align: left; padding: 0.45rem 0.7rem; border-bottom: 1px solid var(--acd-line); }
.acd th { color: var(--acd-orange); font-weight: 700; }
.acd tbody td:first-child { color: var(--acd-muted); }

/* ---------- version tracks ---------- */
.acd .track {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: var(--acd-panel);
  border: 1px solid var(--acd-line);
  border-radius: 10px;
  padding: 0.7rem 1rem;
  margin-bottom: 0.6rem;
  font-size: 1rem;
}
.acd .track .flex-line { flex: 1; height: 2px; background: var(--acd-line); }
</style>
