import type { Metadata, Viewport } from 'next'
import { Inter, Source_Sans_3 } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import { AuthProvider } from '@/lib/auth-context'
import { Toaster } from '@/components/ui/sonner'
import { Chatbot } from '@/components/chatbot'
import './globals.css'

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" })
const sourceSans = Source_Sans_3({ subsets: ["latin"], variable: "--font-source-sans" })

export const metadata: Metadata = {
  title: 'SahAI- Government Policy Portal',
  description: 'Your one-stop portal to discover government schemes, check eligibility, and get step-by-step roadmaps for applications.',
  generator: 'v0.app',
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export const viewport: Viewport = {
  themeColor: '#1e3a5f',
  userScalable: true,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${sourceSans.variable} font-sans antialiased`}>
        <AuthProvider>
          {children}
          <Toaster />
          <Chatbot />
        </AuthProvider>
        <Analytics />
      </body>
    </html>
  )
}
