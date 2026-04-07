#!/usr/bin/env node

/**
 * Preinstall script - Validar que se usa pnpm y limpiar archivos innecesarios
 * Compatible con Windows, macOS y Linux
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Verificar que se está usando pnpm
const userAgent = process.env.npm_config_user_agent || '';
if (!userAgent.startsWith('pnpm')) {
  console.error('❌ Error: Debes usar pnpm como gestor de paquetes');
  console.error('Instala pnpm con: npm install -g pnpm');
  process.exit(1);
}

console.log('✅ Usando pnpm (OK)');

// Limpiar archivos de otros gestores
const filesToRemove = ['package-lock.json', 'yarn.lock'];
filesToRemove.forEach(file => {
  const filePath = path.join(__dirname, '..', file);
  if (fs.existsSync(filePath)) {
    try {
      fs.unlinkSync(filePath);
      console.log(`🗑️  Eliminado: ${file}`);
    } catch (err) {
      console.warn(`⚠️  No se pudo eliminar ${file}: ${err.message}`);
    }
  }
});

console.log('✅ Preinstall completado');
