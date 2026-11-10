import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'

import { MockDetectorClient } from './api/client'
import { App } from './App'

function pngFile(name = 'foto.png'): File {
  return new File([new Uint8Array([137, 80, 78, 71])], name, { type: 'image/png' })
}

function dropzone(): HTMLElement {
  const label = screen.getByText('Arrastra tu imagen aquí')
  const container = label.closest('.dropzone')
  if (!container) {
    throw new Error('No se encontró la zona de arrastre')
  }
  return container as HTMLElement
}

async function analyze(user: ReturnType<typeof userEvent.setup>, file = pngFile()) {
  await user.upload(screen.getByLabelText('Archivo'), file)
  await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
}

describe('App', () => {
  it('deshabilita el análisis hasta que haya una imagen', () => {
    // Arrange / Act
    render(<App client={new MockDetectorClient()} />)

    // Assert
    expect(screen.getByRole('button', { name: 'Analizar imagen' })).toBeDisabled()
  })

  it('muestra las detecciones de una imagen válida', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await analyze(user)

    // Assert
    expect(await screen.findByText('Casco')).toBeInTheDocument()
    expect(screen.getByText('Chaleco')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByRole('img', { name: 'Imagen analizada: foto.png' })).toBeInTheDocument()
    expect(screen.getByText('mock-1.0.0')).toBeInTheDocument()
  })

  it('informa cuando no hay detecciones sin tratarlo como error', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient([])} />)

    // Act
    await analyze(user)

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
      'Formato no admitido. Usa JPEG (jpg, jpeg, jfif) o PNG; AVIF no está soportado.',
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
