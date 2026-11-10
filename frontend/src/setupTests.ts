import '@testing-library/jest-dom/vitest'
import { vi } from 'vitest'

// jsdom no implementa ObjectURL ni canvas 2D; se sustituyen por dobles.
Object.defineProperty(URL, 'createObjectURL', {
  writable: true,
  value: vi.fn(() => 'blob:mock'),
})
Object.defineProperty(URL, 'revokeObjectURL', {
  writable: true,
  value: vi.fn(),
})
Object.defineProperty(HTMLCanvasElement.prototype, 'getContext', {
  writable: true,
  value: vi.fn(() => null),
})
