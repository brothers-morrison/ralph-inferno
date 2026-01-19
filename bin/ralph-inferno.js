#!/usr/bin/env node

import { program } from 'commander';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

program
  .name('ralph-inferno')
  .description('AI-driven autonomous development workflow')
  .version('1.0.0');

program
  .command('install')
  .description('Install Ralph Inferno in current project')
  .action(async () => {
    const { install } = await import('../cli/install.js');
    await install();
  });

program
  .command('update')
  .description('Update core files, preserve config')
  .action(async () => {
    const { update } = await import('../cli/update.js');
    await update();
  });

program.parse();
