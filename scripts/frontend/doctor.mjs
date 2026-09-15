import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

const root = resolve(import.meta.dirname, '../..');
const packageJson = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'));
const localSkills = join(root, '.agents', 'skills');
const packageManager = process.platform === 'win32' ? 'pnpm.cmd' : 'pnpm';

function commandOutput(command, args) {
  const result = spawnSync(command, args, {
    cwd: root,
    encoding: 'utf8',
    windowsHide: true,
    shell: process.platform === 'win32',
  });
  return result.status === 0 ? result.stdout.trim() : '';
}

function hasCommand(command, args = ['--version']) {
  return Boolean(commandOutput(command, args));
}

function dependency(name, section = 'dependencies') {
  return packageJson[section]?.[name] ?? null;
}

function fileStatus(relativePath) {
  return existsSync(join(root, relativePath)) ? 'configured' : 'missing';
}

function skillStatus(name) {
  return existsSync(join(localSkills, name, 'SKILL.md')) ? 'available' : 'missing';
}

function userSkillStatus(name) {
  const codexHome = process.env.CODEX_HOME || join(homedir(), '.codex');
  return existsSync(join(codexHome, 'skills', name, 'SKILL.md')) ? 'available' : 'missing';
}

function registeredMcpNames() {
  const output = commandOutput('codex', ['mcp', 'list']);
  return new Set(
    output
      .split(/\r?\n/)
      .map((line) => line.trim().match(/^([a-z0-9_-]+)\s+/i)?.[1]?.toLowerCase())
      .filter(Boolean),
  );
}

async function endpointStatus(url) {
  try {
    // The MCP endpoint keeps GET/SSE connections open. A short initialize POST
    // is the deterministic health check and does not expose any project data.
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        accept: 'application/json, text/event-stream',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {
          protocolVersion: '2025-06-18',
          capabilities: {},
          clientInfo: { name: 'grimo-frontend-doctor', version: '1.0' },
        },
      }),
      signal: AbortSignal.timeout(1_500),
    });
    return response.ok || response.status < 500 ? 'available' : 'configured';
  } catch {
    return 'configured (start Storybook)';
  }
}

const mcpNames = registeredMcpNames();
const rows = [
  ['Node', process.version, hasCommand('node') ? 'installed' : 'missing'],
  ['pnpm', commandOutput(packageManager, ['--version']) || 'missing', hasCommand(packageManager) ? 'installed' : 'missing'],
  ['Next.js', dependency('next'), dependency('next') ? 'installed' : 'missing'],
  ['React', dependency('react'), dependency('react') ? 'installed' : 'missing'],
  ['Tailwind CSS', dependency('tailwindcss', 'devDependencies'), dependency('tailwindcss', 'devDependencies') ? 'installed' : 'missing'],
  ['Motion for React', dependency('motion'), dependency('motion') ? 'installed' : 'missing'],
  ['Storybook', dependency('storybook', 'devDependencies'), dependency('storybook', 'devDependencies') ? 'installed' : 'missing'],
  ['Storybook framework', dependency('@storybook/nextjs-vite', 'devDependencies'), fileStatus('.storybook/main.ts')],
  ['Storybook MCP addon', dependency('@storybook/addon-mcp', 'devDependencies'), dependency('@storybook/addon-mcp', 'devDependencies') ? 'installed' : 'missing'],
  ['Storybook a11y addon', dependency('@storybook/addon-a11y', 'devDependencies'), dependency('@storybook/addon-a11y', 'devDependencies') ? 'installed' : 'missing'],
  ['Storybook Skills', 'stories / setup / init / upgrade', ['stories', 'storybook-setup', 'storybook-init', 'storybook-upgrade'].every((name) => skillStatus(name) === 'available') ? 'available' : 'missing'],
  ['react-best-practices Skill', 'Vercel Engineering', skillStatus('vercel-react-best-practices')],
  ['web-design-guidelines Skill', 'Vercel', skillStatus('web-design-guidelines')],
  ['frontend-design Skill', 'Codex built-in', userSkillStatus('frontend-design')],
  ['Playwright', dependency('@playwright/test', 'devDependencies'), hasCommand(packageManager, ['exec', 'playwright', '--version']) ? 'available' : 'missing'],
  ['Visual test config', 'playwright.config.ts', fileStatus('playwright.config.ts')],
  ['Storybook/Vitest config', 'vitest.config.ts', fileStatus('vitest.config.ts')],
  ['Figma MCP', 'existing registration only', mcpNames.has('figma') ? 'registered' : 'unavailable'],
  ['Storybook MCP', 'http://127.0.0.1:6006/mcp', mcpNames.has('storybook') ? 'registered' : 'missing'],
  ['Blender MCP', 'existing registration only', mcpNames.has('blender') ? 'registered' : 'unavailable'],
  ['PlayCanvas MCP', 'existing registration only', mcpNames.has('playcanvas') ? 'registered' : 'unavailable'],
  ['Chrome DevTools MCP', 'existing registration only', mcpNames.has('chrome-devtools') ? 'registered' : 'unavailable'],
];

rows.push(['Storybook MCP endpoint', 'localhost only', await endpointStatus('http://127.0.0.1:6006/mcp')]);

const nameWidth = Math.max(...rows.map(([name]) => name.length), 20);
const valueWidth = Math.max(...rows.map(([, value]) => String(value).length), 30);
console.log(`Frontend Doctor — ${new Date().toISOString()}`);
console.log(`${'Check'.padEnd(nameWidth)}  ${'Value'.padEnd(valueWidth)}  Status`);
console.log(`${'-'.repeat(nameWidth)}  ${'-'.repeat(valueWidth)}  ------`);
for (const [name, value, status] of rows) {
  console.log(`${name.padEnd(nameWidth)}  ${String(value).padEnd(valueWidth)}  ${status}`);
}

const required = rows.filter(([name]) => !['Figma MCP', 'Blender MCP', 'PlayCanvas MCP', 'Chrome DevTools MCP', 'Storybook MCP endpoint'].includes(name));
const failed = required.filter(([, , status]) => ['missing', 'unavailable'].includes(status));
console.log(`\nResult: ${failed.length === 0 ? 'PASS' : 'FAIL'} (${failed.length} required checks missing)`);
process.exitCode = failed.length === 0 ? 0 : 1;
