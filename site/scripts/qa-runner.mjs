import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const SCREENSHOTS_DIR = '/tmp/screenshots';
fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });

async function cdpRequest(ws, method, params = {}) {
  const id = Math.floor(Math.random() * 1000000);
  const msg = JSON.stringify({ id, method, params });
  return new Promise((resolve, reject) => {
    const handler = (event) => {
      const data = JSON.parse(event.data);
      if (data.id === id) {
        ws.removeEventListener('message', handler);
        if (data.error) reject(data.error);
        else resolve(data.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(msg);
  });
}

async function captureWithCdp(url, outPath, { width, height, theme = 'light' }) {
  const chrome = spawn('google-chrome', [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--disable-gpu',
    '--no-sandbox',
    '--hide-scrollbars',
    `--window-size=${width},${height}`,
    'about:blank',
  ]);

  try {
    await new Promise((r) => setTimeout(r, 600));
    const targets = await fetch('http://localhost:9222/json/list').then((r) => r.json());
    const pageTarget = targets.find((t) => t.type === 'page') || targets[0];
    if (!pageTarget || !pageTarget.webSocketDebuggerUrl) {
      throw new Error('No page target found');
    }

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise((r) => (ws.onopen = r));

    // Enable Page and Runtime
    await cdpRequest(ws, 'Page.enable');
    await cdpRequest(ws, 'Runtime.enable');
    await cdpRequest(ws, 'Emulation.setDeviceMetricsOverride', {
      width,
      height,
      deviceScaleFactor: 1,
      mobile: width <= 768,
    });

    // Navigate to URL
    await cdpRequest(ws, 'Page.navigate', { url });
    await new Promise((r) => setTimeout(r, 1200));

    // Set Theme
    await cdpRequest(ws, 'Runtime.evaluate', {
      expression: `
        document.documentElement.dataset.theme = '${theme}';
        localStorage.setItem('starlight-theme', '${theme}');
      `,
    });
    await new Promise((r) => setTimeout(r, 300));

    // Capture screenshot
    const screenshot = await cdpRequest(ws, 'Page.captureScreenshot', {
      format: 'png',
    });

    fs.writeFileSync(outPath, Buffer.from(screenshot.data, 'base64'));
    ws.close();
    console.log(`📸 Saved screenshot: ${path.basename(outPath)} (${width}x${height}, ${theme})`);
  } finally {
    chrome.kill();
    await new Promise((r) => setTimeout(r, 300));
  }
}

async function main() {
  const BASE = 'http://localhost:8080/From-LLMs-to-Secure-Agents';

  const viewports = [
    { name: 'desktop-1440', width: 1440, height: 900 },
    { name: 'desktop-1280', width: 1280, height: 800 },
    { name: 'tablet-768', width: 768, height: 1024 },
    { name: 'mobile-390', width: 390, height: 844 },
  ];

  const routes = [
    { name: 'home', path: '/' },
    { name: 'prereq1', path: '/prerequisites/01-reader-contract-and-system-map/' },
    { name: 'prereq4', path: '/prerequisites/04-identity-authority-and-least-privilege-primer/' },
    { name: 'found1', path: '/foundations/01-what-is-an-agent/' },
    { name: 'found2', path: '/foundations/02-the-agent-loop/' },
    { name: 'found5', path: '/foundations/05-run-lifecycle-and-termination/' },
  ];

  console.log('🚀 Running Visual QA Screenshot Suite...');

  // 1. Light Mode Screenshots across viewports
  for (const vp of viewports) {
    await captureWithCdp(`${BASE}/`, `${SCREENSHOTS_DIR}/home-${vp.name}-light.png`, { ...vp, theme: 'light' });
    await captureWithCdp(`${BASE}/foundations/01-what-is-an-agent/`, `${SCREENSHOTS_DIR}/found1-${vp.name}-light.png`, { ...vp, theme: 'light' });
  }

  // 2. All canonical chapter routes in Light Mode (1440x900)
  for (const r of routes) {
    await captureWithCdp(`${BASE}${r.path}`, `${SCREENSHOTS_DIR}/${r.name}-1440-light.png`, { width: 1440, height: 900, theme: 'light' });
  }

  // 3. Dark Mode reference captures
  await captureWithCdp(`${BASE}/`, `${SCREENSHOTS_DIR}/home-1440-dark.png`, { width: 1440, height: 900, theme: 'dark' });
  await captureWithCdp(`${BASE}/foundations/01-what-is-an-agent/`, `${SCREENSHOTS_DIR}/found1-1440-dark.png`, { width: 1440, height: 900, theme: 'dark' });
  await captureWithCdp(`${BASE}/foundations/02-the-agent-loop/`, `${SCREENSHOTS_DIR}/found2-1440-dark.png`, { width: 1440, height: 900, theme: 'dark' });

  console.log('✅ Visual QA Suite completed successfully!');
}

main().catch(console.error);
