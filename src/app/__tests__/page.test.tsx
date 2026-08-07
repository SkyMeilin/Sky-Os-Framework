import { render, screen } from '@testing-library/react'
import Home from '../page'

// Mock the getCurrentUser function
jest.mock('@/lib/fanvue', () => ({
  getCurrentUser: jest.fn(async () => null),
}))

describe('Home Page', () => {
  it('renders the Fanvue App Starter header', async () => {
    const { container } = render(await Home({ searchParams: Promise.resolve({}) }))
    expect(screen.getByText('Fanvue App Starter')).toBeInTheDocument()
  })

  it('renders login button when not authenticated', async () => {
    render(await Home({ searchParams: Promise.resolve({}) }))
    expect(screen.getByText('Login with Fanvue')).toBeInTheDocument()
  })

  it('renders Fanvue API Docs link', async () => {
    render(await Home({ searchParams: Promise.resolve({}) }))
    const docsLink = screen.getByText('Fanvue API Docs')
    expect(docsLink).toHaveAttribute('href', 'https://api.fanvue.com/docs')
  })

  it('renders fanvue.com link', async () => {
    render(await Home({ searchParams: Promise.resolve({}) }))
    const fanvueLink = screen.getByText(/Visit fanvue.com/i)
    expect(fanvueLink).toHaveAttribute('href', 'https://fanvue.com')
  })
})
