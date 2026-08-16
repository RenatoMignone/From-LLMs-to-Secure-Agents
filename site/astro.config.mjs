// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://renatomignone.github.io',
  base: '/From-LLMs-to-Secure-Agents',
  integrations: [
    starlight({
      title: 'From LLMs to Secure Agents',
      description: 'A visual, source-grounded engineering guide to understanding complete agentic AI architectures and learning how to secure them.',
      logo: {
        src: './src/assets/logo.svg',
      },
      social: {
        github: 'https://github.com/RenatoMignone/From-LLMs-to-Secure-Agents',
      },
      customCss: [
        './src/custom.css',
      ],
      head: [
        {
          tag: 'meta',
          attrs: {
            name: 'theme-color',
            content: '#0d9488',
          },
        },
      ],
      sidebar: [
        {
          label: 'Getting Started',
          items: [
            { label: 'Handbook Overview', link: '/' },
            { label: 'Curriculum & Architecture', link: '/overview/curriculum/' },
            { label: 'Evidence Methodology', link: '/overview/methodology/' },
          ],
        },
        {
          label: '01 Agent Foundations',
          items: [
            { label: '1. What is an AI Agent', link: '/foundations/what-is-an-ai-agent/' },
            { label: '2. The Agent Loop Explained', link: '/foundations/the-agent-loop-explained/' },
            { label: '3. Workflows vs Autonomous Agents', link: '/foundations/workflows-versus-autonomous-agents/' },
            { label: '4. Goals, Policies & Autonomy', link: '/foundations/goals-policies-environments-and-autonomy/' },
            { label: '5. Run Lifecycle & Termination', link: '/foundations/run-lifecycle-and-termination/' },
            { label: '6. Identity & Least Privilege', link: '/foundations/identity-authority-and-least-privilege/' },
          ],
        },
        {
          label: 'Security & Threat Modeling',
          items: [
            { label: 'Securing AI Agents (Master Guide)', link: '/security/securing-ai-agents/' },
            { label: 'Indirect Prompt Injection Defense', link: '/security/indirect-prompt-injection-defense/' },
            { label: 'Identity & Scoped Delegation', link: '/security/identity-and-scoped-delegation/' },
            { label: 'Tools & Excessive Agency', link: '/security/tools-and-excessive-agency-prevention/' },
            { label: 'Execution & Sandboxing', link: '/security/execution-environments-and-sandboxing/' },
            { label: 'Model Context Protocol (MCP) Security', link: '/security/model-context-protocol-security/' },
          ],
        },
        {
          label: 'Architecture & Subsystems (Roadmap)',
          badge: { text: 'Roadmap', variant: 'note' },
          items: [
            { label: 'Agent Architectures & Patterns', link: '/architecture/selection-and-tradeoffs/' },
            { label: 'Building Blocks & Subsystems', link: '/building-blocks/components-overview/' },
          ],
        },
        {
          label: 'Reference & Agent Endpoints',
          items: [
            { label: 'System Glossary', link: '/reference/glossary/' },
            { label: 'Machine & AI Endpoints', link: '/reference/agent-endpoints/' },
          ],
        },
      ],
    }),
  ],
});
