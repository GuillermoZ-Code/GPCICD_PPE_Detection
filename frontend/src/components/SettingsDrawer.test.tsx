/** FR de configuración — preferencias, umbrales y descargas. */

import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { DEFAULT_SETTINGS, type Settings } from '../config'
import { SettingsDrawer } from './SettingsDrawer'

interface SetupOptions {
  open?: boolean
  canDownload?: boolean
  settings?: Settings
}

function setup(options: SetupOptions = {}) {
  const handlers = {
    onChange: vi.fn(),
    onClose: vi.fn(),
    onReset: vi.fn(),
    onDownload: vi.fn(),
  }
  const settings = options.settings ?? DEFAULT_SETTINGS
  const ui = (canDownload: boolean, open: boolean) => (
    <SettingsDrawer
      open={open}
      settings={settings}
      canDownload={canDownload}
      {...handlers}
    />
  )
  const view = render(ui(options.canDownload ?? false, options.open ?? true))
  return {
    ...handlers,
    ...view,
    rerenderWith: (canDownload: boolean, open = options.open ?? true) =>
      view.rerender(ui(canDownload, open)),
  }
}

describe('SettingsDrawer', () => {
  it('oculta el panel a la accesibilidad cuando está cerrado', () => {
    // Arrange / Act
    setup({ open: false })

    // Assert
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(screen.getByRole('dialog', { hidden: true })).toHaveAttribute(
      'aria-hidden',
      'true',
    )
  })

  it('notifica el tema elegido', async () => {
    // Arrange
    const user = userEvent.setup()
    const { onChange } = setup()

    // Act
    await user.click(screen.getByRole('button', { name: 'Oscuro' }))
    await user.click(screen.getByRole('button', { name: 'Claro' }))
    await user.click(screen.getByRole('button', { name: 'Sistema' }))

    // Assert
    expect(onChange).toHaveBeenNthCalledWith(1, { theme: 'dark' })
    expect(onChange).toHaveBeenNthCalledWith(2, { theme: 'light' })
    expect(onChange).toHaveBeenNthCalledWith(3, { theme: 'system' })
  })

  it('quita y agrega clases visibles con los chips', async () => {
    // Arrange
    const user = userEvent.setup()
    const { onChange } = setup({ settings: { ...DEFAULT_SETTINGS, classes: ['helmet'] } })

    // Act
    await user.click(screen.getByRole('button', { name: 'Casco' }))
    await user.click(screen.getByRole('button', { name: 'Gafas' }))

    // Assert
    expect(onChange).toHaveBeenNthCalledWith(1, { classes: [] })
    expect(onChange).toHaveBeenNthCalledWith(2, { classes: ['helmet', 'goggles'] })
  })

  it('convierte el porcentaje del umbral del modelo a fracción', () => {
    // Arrange
    const { onChange } = setup()
    const sliders = screen.getAllByRole('slider')

    // Act
    fireEvent.change(sliders[2], { target: { value: '40' } })

    // Assert
    expect(onChange).toHaveBeenCalledWith({ modelConfidence: 0.4 })
  })

  it('habilita las descargas y emite el formato elegido', async () => {
    // Arrange
    const user = userEvent.setup()
    const { onDownload, rerenderWith } = setup({ canDownload: false })
    expect(screen.getByRole('button', { name: 'JSON' })).toBeDisabled()

    // Act
    rerenderWith(true)
    await user.click(screen.getByRole('button', { name: 'CSV' }))

    // Assert
    expect(screen.getByRole('button', { name: 'JSON' })).toBeEnabled()
    expect(onDownload).toHaveBeenCalledWith('csv')
  })
})
