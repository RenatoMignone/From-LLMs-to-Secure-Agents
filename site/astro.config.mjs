// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://renatomignone.github.io',
  base: '/From-LLMs-to-Secure-Agents',
  integrations: [
    starlight({
      title: 'From LLMs to Secure Agents',
      description: 'A deep, visual, source-grounded guide to understanding complete agentic AI systems and learning how to secure them.',
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
            content: '#14a38b',
          },
        },
      ],
      sidebar: [
        {
          label: 'Overview',
          items: [
            { label: 'Guide Introduction', link: '/' },
            { label: 'Curriculum & Architecture', link: '/overview/curriculum/' },
            { label: 'Evidence & Methodology', link: '/overview/methodology/' },
          ],
        },
        {
          label: 'Pass 1: Understand the System',
          items: [
            {
              label: '00 Prerequisites',
              items: [
                { label: 'Prerequisites Overview', link: '/00-prerequisites/' },
                { label: 'Reader contract & system map', link: '/00-prerequisites/01-reader-contract-and-system-map/' },
                { label: 'Data, control & trust boundaries', link: '/00-prerequisites/02-data-control-and-trust-boundaries/' },
                { label: 'Requests, events, state & side effects', link: '/00-prerequisites/03-requests-events-state-and-side-effects/' },
                { label: 'Identity, authority & least privilege', link: '/00-prerequisites/04-identity-authority-and-least-privilege-primer/' },
              ],
            },
            {
              label: '01 Agent Foundations',
              items: [
                { label: 'Foundations Overview', link: '/01-agent-foundations/' },
                { label: 'What is an agent', link: '/01-agent-foundations/01-what-is-an-agent/' },
                { label: 'The agent loop', link: '/01-agent-foundations/02-the-agent-loop/' },
                { label: 'Workflows versus agents', link: '/01-agent-foundations/03-workflows-versus-agents/' },
                { label: 'Goals, policies, environments & autonomy', link: '/01-agent-foundations/04-goals-policies-environments-and-autonomy/' },
                { label: 'Run lifecycle & termination', link: '/01-agent-foundations/05-run-lifecycle-and-termination/' },
              ],
            },
            {
              label: '02 Agent Architectures',
              badge: { text: 'Roadmap', variant: 'note' },
              items: [
                { label: 'Architectures Overview', link: '/02-agent-architectures/' },
              ],
            },
            {
              label: '03 Building Blocks',
              badge: { text: 'Roadmap', variant: 'note' },
              items: [
                { label: 'Building Blocks Overview', link: '/03-building-blocks/' },
              ],
            },
            {
              label: '04 Frameworks & Protocols',
              badge: { text: 'Roadmap', variant: 'note' },
              items: [
                { label: 'Frameworks & MCP Overview', link: '/04-frameworks-and-protocols/' },
              ],
            },
            {
              label: '05 End-to-End Workflows',
              badge: { text: 'Roadmap', variant: 'note' },
              items: [
                { label: 'Workflows Overview', link: '/05-end-to-end-workflows/' },
              ],
            },
          ],
        },
        {
          label: 'Pass 2: Secure the System',
          items: [
            {
              label: '06 Threat Model',
              badge: { text: 'Pass 2', variant: 'caution' },
              items: [
                { label: 'Threat Model Overview', link: '/06-threat-model/' },
              ],
            },
            {
              label: '07 Security by Component',
              badge: { text: 'Pass 2', variant: 'caution' },
              items: [
                { label: 'Component Security Overview', link: '/07-security-by-component-and-workflow-stage/' },
              ],
            },
            {
              label: '08 Secure Reference Architectures',
              badge: { text: 'Pass 2', variant: 'caution' },
              items: [
                { label: 'Reference Architectures Overview', link: '/08-secure-reference-architectures/' },
              ],
            },
            {
              label: '09 Testing, Eval & Assurance',
              badge: { text: 'Pass 2', variant: 'caution' },
              items: [
                { label: 'Assurance Overview', link: '/09-security-testing-evaluation-and-assurance/' },
              ],
            },
            {
              label: '10 Open Research Questions',
              badge: { text: 'Research', variant: 'tip' },
              items: [
                { label: 'Research Frontier', link: '/10-open-research-questions/' },
              ],
            },
          ],
        },
        {
          label: 'Topic Hubs & Deep Dives',
          items: [
            { label: 'Securing AI Agents (Core Hub)', link: '/hubs/securing-ai-agents/' },
            { label: 'Prompt Injection & Untrusted Data', link: '/hubs/prompt-injection/' },
            { label: 'Identity, Delegation & Permissions', link: '/hubs/identity-and-delegation/' },
            { label: 'Tools & Excessive Agency', link: '/hubs/tools-and-excessive-agency/' },
            { label: 'Execution & Sandboxing', link: '/hubs/execution-and-sandboxing/' },
            { label: 'Model Context Protocol (MCP) Security', link: '/hubs/mcp-and-protocols/' },
          ],
        },
        {
          label: 'Reference & Agent Endpoints',
          items: [
            { label: 'System Glossary', link: '/reference/glossary/' },
            { label: 'LLM & Machine Endpoints', link: '/reference/llm-endpoints/' },
          ],
        },
      ],
    }),
  ],
});
