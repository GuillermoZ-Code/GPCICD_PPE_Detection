/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module 'node:fs' {
  export function readFileSync(path: string, encoding: 'utf-8'): string
}

declare module 'node:path' {
  export function resolve(...paths: string[]): string
}

declare const process: { cwd(): string }
