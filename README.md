# tdesmedt-tdsgn.github.io

Tom De Smedt's blog and portfolio — **Astro** static site, deployed to GitHub
Pages by Actions. The previous Jekyll site lives in git history (pre
`astro-rebuild` merge); its URLs are preserved via redirects in
`astro.config.mjs`.

## How publishing works

1. A post lands as a Pull Request touching `src/content/blog/<slug>.md`
   (usually opened by the blog pipeline in the private `CTOBlog` repo).
2. Review the PR — the rendered markdown *is* the post. Request changes or
   **merge to publish**: pushing `main` triggers `.github/workflows/deploy.yml`
   which builds and deploys to Pages.
3. `notify.yml` makes the Actions bot @mention Tom on new issues/PRs so GitHub
   sends a notification email (self-created items never notify otherwise).

## Post frontmatter

```yaml
title: "..."
description: "1–2 sentence summary (also used in RSS + meta tags)"
pubDate: 2026-09-14
tags: ["agents", "engineering"]
demo: https://github.com/tdesmedt-tdsgn/labs/tree/main/<slug>   # optional
businessNote: "One-paragraph 'for business leaders' callout."   # optional
legacy: true    # only on migrated Jekyll-era posts
draft: true     # keeps a post out of the build
```

## Local dev

```sh
npm install
npm run dev        # http://localhost:4321
npm run build      # output in dist/
npm run preview
```

`scripts/og.py` regenerates the default Open Graph image (`public/og.png`);
`scripts/migrate_posts.py` is the one-shot Jekyll migration, kept for
provenance. `docs/custom-domain.md` has the tdsgn.be cut-over steps.
