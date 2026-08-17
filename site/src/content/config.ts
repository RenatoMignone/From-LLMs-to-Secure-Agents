import { defineCollection, z } from 'astro:content';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    schema: docsSchema({
      extend: z.object({
        unit_id: z.string().optional(),
        pass: z.string().optional(),
        learning_path: z.string().optional(),
        status: z.string().optional(),
        last_reviewed: z.string().optional(),
        reviewed_label: z.string().optional(),
        summary: z.string().optional(),
        prerequisites: z.array(z.string()).optional(),
        learning_objectives: z.array(z.string()).optional(),
        source_records: z.array(z.string()).optional(),
        visual_assets: z.array(z.string()).optional(),
        example_paths: z.array(z.string()).optional(),
      }),
    }),
  }),
};
