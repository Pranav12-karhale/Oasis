import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navigation from '@/components/Navigation'
import AccessibilityPanel from '@/components/AccessibilityPanel'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Oasis — Health & Safety Platform',
  description: 'AI-powered health and safety recommendations across India.',
  manifest: '/manifest.json',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen flex flex-col`}>
        {/* Hidden region for screen reader live announcements */}
        <div aria-live="assertive" className="sr-only" id="sr-announcer"></div>
        
        <header className="sticky top-0 z-50 w-full border-b bg-white/80 dark:bg-gray-950/80 backdrop-blur">
          <div className="container mx-auto px-4 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold bg-gradient-to-r from-teal-500 to-blue-600 bg-clip-text text-transparent">
                Oasis
              </span>
            </div>
            <div className="flex items-center gap-4">
              <AccessibilityPanel />
            </div>
          </div>
        </header>

        <div className="flex flex-1 container mx-auto px-4 py-6 gap-6">
          <aside className="hidden md:block w-64 shrink-0">
            <Navigation />
          </aside>
          
          <main className="flex-1 w-full max-w-4xl mx-auto">
            {children}
          </main>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden fixed bottom-0 w-full bg-white dark:bg-gray-950 border-t pb-safe">
          <Navigation mobile />
        </div>
      </body>
    </html>
  )
}
