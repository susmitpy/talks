# Welcome to [Slidev](https://github.com/slidevjs/slidev)!

To build a slide show in template.md under /template route
```bash
export NODE_OPTIONS=--max-old-space-size=8192
npm exec slidev build template.md -- --base /template/ --out docs/template
```

To start the slide show:

- `npm install`
- `npm run dev`
- visit <http://localhost:3030>

Edit the [slides.md](./slides.md) to see the changes.

Learn more about Slidev at the [documentation](https://sli.dev/).
