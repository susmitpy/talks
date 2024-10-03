# Welcome to [Slidev](https://github.com/slidevjs/slidev)!

To build a slide show in template.md under /template route when being hosted on github pages in repo talks
```bash
export NODE_OPTIONS=--max-old-space-size=8192
npm exec slidev build template.md -- --base /talks/template/ --out docs/template

npm exec slidev build pres1.md -- --base /talks/pres1/ --out docs/pres1
```

Using remote control
```bash
npm exec slidev -- --open template.md --remote
```
Press 'c' to get the qr code to scan and control the slides

To start the slide show:

- `npm install`
- `npm run dev`
- visit <http://localhost:3030>

Edit the [slides.md](./slides.md) to see the changes.

Learn more about Slidev at the [documentation](https://sli.dev/).
