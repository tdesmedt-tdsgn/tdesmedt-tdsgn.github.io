import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    legacy: z.boolean().default(false),
    draft: z.boolean().default(false),
    businessNote: z.string().optional(),
    demo: z.string().url().optional(),
  }),
});

export const collections = { blog };
