import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'

import { MockDetectorClient } from './api/client'
import { App } from './App'

function pngFile(name = 'foto.png'): File {
  return new File([new Uint8Array([137, 80, 78, 71])], name, { type: 'image/png' })
}

function dropzone(): HTMLElement {
  const label = screen.getByText('Arrastra una imagen aquí')
  const container = label.closest('.dropzone')
  if (!container) {
    throw new Error('No se encontró la zona de arrastre')
  }
  return container as HTMLElement
}

describe('App', () => {
  it('muestra las detecciones de una imagen válida', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())

    // Assert
    expect(await screen.findByText('Casco')).toBeInTheDocument()
    expect(screen.getByText('Chaleco')).toBeInTheDocument()
    expect(screen.getByText('2 detección(es) en foto.png')).toBeInTheDocument()
    expect(screen.getByRole('img', { name: 'Imagen analizada: foto.png' })).toBeInTheDocument()
  })

  it('informa cuando no hay detecciones sin tratarlo como error', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient([])} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())

    // Assert
    expect(await screen.findByText(/No se detectaron EPP en la imagen/)).toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('rechaza un archivo inválido y sigue disponible', async () => {
    // Arrange
    render(<App client={new MockDetectorClient()} />)
    const invalid = new File(['texto'], 'nota.txt', { type: 'text/plain' })

    // Act
    fireEvent.drop(dropzone(), { dataTransfer: { files: [invalid] } })

    // Assert
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Formato no admitido. Usa una imagen JPEG o PNG.',
    )
    expect(screen.getByLabelText('Archivo')).not.toBeDisabled()
  })

  it('muestra el enlace al código fuente y la atribución del dataset', () => {
    // Arrange / Act
    render(<App client={new MockDetectorClient()} />)

    // Assert
    expect(screen.getByRole('link', { name: 'Código fuente' })).toHaveAttribute(
      'href',
      'https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection',
    )
    expect(screen.getByText(/CC-BY-4.0/)).toBeInTheDocument()
  })
})
