// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Redirects preserve the URLs of the old Jekyll site (meta-refresh stubs in dist/).
const legacyRedirects = {
  '/2022/10/03/Impediments-Scrum.html': '/blog/impediments-scrum/',
  '/2022/10/26/RFID-for-Food-Industry.html': '/blog/rfid-for-food-industry/',
  '/2022/11/27/Servant-leader.html': '/blog/servant-leader/',
  '/2022/12/07/IT-values-mission-vision.html': '/blog/it-values-mission-vision/',
  '/2022/12/20/IT-risk-management.html': '/blog/it-risk-management/',
  '/2023/01/07/Digital-transformation-and-navigating-change.html':
    '/blog/digital-transformation-and-navigating-change/',
  '/2023/01/23/Technical-debt.html': '/blog/technical-debt/',
  '/2023/02/15/Tech-Stack-Selection.html': '/blog/tech-stack-selection/',
  '/2023/02/28/Importance-Of-Cadence.html': '/blog/importance-of-cadence/',
  '/2023/03/14/Data-Science-Skills.html': '/blog/data-science-skills/',
  '/2023/03/23/Setting-up-data-science.html': '/blog/setting-up-data-science/',
  '/archive.html': '/blog/',
};

export default defineConfig({
  site: 'https://tdesmedt-tdsgn.github.io',
  trailingSlash: 'ignore',
  integrations: [sitemap()],
  redirects: legacyRedirects,
});
