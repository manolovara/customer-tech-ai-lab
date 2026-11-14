# Edge Delivery block development

## What a block is

In Edge Delivery Services (EDS), a block is the unit of reusable functionality and styling. Authors create it in a document as a table whose first cell holds the block name. The platform converts that table into semantic HTML, and your code decorates it in the browser.

## Folder structure

Each block lives in its own folder under `blocks/`:

```
blocks/
  cards/
    cards.js
    cards.css
```

The folder name, the JavaScript file and the CSS file must share the same name. The block name from the authoring table is lowercased and hyphenated, so "Hero Banner" maps to `hero-banner`.

## The decorate function

Every block exports a default `decorate` function that receives the block element:

```js
export default function decorate(block) {
  const rows = [...block.children];
  rows.forEach((row) => {
    row.classList.add('cards-item');
  });
}
```

Keep decoration idempotent and cheap. Do not fetch data or load heavy libraries before the block is needed, and avoid layout shifts by reserving space in CSS.

## Styling rules

- Scope every selector with the block class, for example `.cards .cards-item`.
- Write mobile-first CSS and add `min-width` media queries (commonly 600px, 900px and 1200px).
- Use CSS custom properties defined in `styles/styles.css` rather than hard-coded colors.
- Do not depend on a build step; plain CSS and modern JavaScript modules are enough.

## Variants

Authors add variants in parentheses after the block name, such as "Cards (dark, wide)". Each variant becomes a class on the block element, so `.cards.dark` can restyle it without a new block.

## Loading behavior

The page is loaded in three phases: eager (the LCP content), lazy (the rest of the page) and delayed (third-party tools such as analytics and consent). Place blocks that contain the largest image or heading above the fold and avoid adding scripts to the eager phase.

## Content-first mindset

Design the authoring model before the code. A good block has a small number of columns and rows that authors can understand without documentation. Prefer plain text, links and images over custom fields.

## Testing and linting

- Run the linter (ESLint and Stylelint) before every pull request.
- Test with the local dev server pointing at real content.
- Check Lighthouse on a branch preview; the target is a score of 100 on mobile.
- Review the block with keyboard navigation and a screen reader.

## Common pitfalls

1. Rewriting the DOM so heavily that authors' content is lost.
2. Loading fonts or libraries from the block instead of the delayed phase.
3. Adding block-specific global CSS that leaks into other blocks.
4. Skipping a fallback for missing images or empty rows.

## Checklist before merging

- Block works with empty and minimal content.
- Variants documented in the block's README or authoring guide.
- No console errors or warnings.
- Performance budget respected.
- Accessibility reviewed.

For the current platform reference, consult the official documentation, including the machine-readable index at aem.live/llms.txt.
