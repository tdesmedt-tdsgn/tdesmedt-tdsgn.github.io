# Pointing tdsgn.be at this site (later, ~5 minutes)

The site works today at <https://tdesmedt-tdsgn.github.io>. When you're ready to
serve it from your own domain, GitHub Pages makes the switch non-breaking:
after the custom domain is active, every `tdesmedt-tdsgn.github.io/...` URL
**redirects automatically** to the same path on the new domain.

## Option A — `www.tdsgn.be` + apex (recommended)

1. **In Bluehost DNS** (or wherever tdsgn.be's DNS is managed), add:

   | Type  | Host  | Value                     |
   |-------|-------|---------------------------|
   | A     | `@`   | `185.199.108.153`         |
   | A     | `@`   | `185.199.109.153`         |
   | A     | `@`   | `185.199.110.153`         |
   | A     | `@`   | `185.199.111.153`         |
   | AAAA  | `@`   | `2606:50c0:8000::153`     |
   | AAAA  | `@`   | `2606:50c0:8001::153`     |
   | AAAA  | `@`   | `2606:50c0:8002::153`     |
   | AAAA  | `@`   | `2606:50c0:8003::153`     |
   | CNAME | `www` | `tdesmedt-tdsgn.github.io` |

   (Remove any existing A/CNAME records Bluehost parked on `@`/`www` first.)

2. **In the repo**: GitHub → Settings → Pages → Custom domain → enter
   `www.tdsgn.be` → Save. GitHub commits a `CNAME` file; wait for the DNS
   check, then tick **Enforce HTTPS** (certificate takes a few minutes).

3. Update `site` in `astro.config.mjs` to `https://www.tdsgn.be` and merge —
   this fixes canonical URLs, the sitemap and the RSS feed.

## Option B — `blog.tdsgn.be` only

Keep the apex wherever it is; add just one record:

| Type  | Host   | Value                      |
|-------|--------|----------------------------|
| CNAME | `blog` | `tdesmedt-tdsgn.github.io` |

Then set the custom domain to `blog.tdsgn.be` in Pages settings and update
`site` in `astro.config.mjs` as above.

## Checks

```sh
dig +short www.tdsgn.be        # should list the GitHub IPs / CNAME
curl -I https://www.tdsgn.be   # 200 after cert is issued
curl -I https://tdesmedt-tdsgn.github.io  # 301 to the custom domain
```
