import Link from "next/link"
import { Landmark } from "lucide-react"

export function SiteFooter() {
  return (
    <footer className="border-t border-border bg-primary text-primary-foreground">
      <div className="mx-auto max-w-7xl px-4 py-12">
        <div className="grid gap-8 md:grid-cols-4">
          <div className="md:col-span-1">
            <Link href="/" className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary-foreground/15">
                <Landmark className="h-4 w-4" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-bold tracking-wide">SahAI</span>
                <span className="text-[10px] text-primary-foreground/60">Government Policy Portal</span>
              </div>
            </Link>
            <p className="mt-3 text-xs leading-relaxed text-primary-foreground/60">
              Empowering citizens with easy access to government schemes and streamlined application processes.
            </p>
          </div>

          <div>
            <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-primary-foreground/50">Quick Links</h3>
            <ul className="flex flex-col gap-2">
              <li>
                <Link href="/" className="text-sm text-primary-foreground/70 hover:text-primary-foreground">Home</Link>
              </li>
              <li>
                <Link href="/schemes" className="text-sm text-primary-foreground/70 hover:text-primary-foreground">All Schemes</Link>
              </li>
              <li>
                <Link href="/profile" className="text-sm text-primary-foreground/70 hover:text-primary-foreground">My Profile</Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-primary-foreground/50">Categories</h3>
            <ul className="flex flex-col gap-2">
              <li>
                <Link href="/schemes?category=education" className="text-sm text-primary-foreground/70 hover:text-primary-foreground">Education</Link>
              </li>
              <li>
                <Link href="/schemes?category=healthcare" className="text-sm text-primary-foreground/70 hover:text-primary-foreground">Healthcare</Link>
              </li>
              <li>
                <Link href="/schemes?category=housing" className="text-sm text-primary-foreground/70 hover:text-primary-foreground">Housing</Link>
              </li>
              <li>
                <Link href="/schemes?category=agriculture" className="text-sm text-primary-foreground/70 hover:text-primary-foreground">Agriculture</Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-primary-foreground/50">Support</h3>
            <ul className="flex flex-col gap-2">
              <li>
                <Link href="/ai-assistant" className="text-sm text-primary-foreground/70 hover:text-primary-foreground">AI Assistant</Link>
              </li>
              <li>
                <span className="text-sm text-primary-foreground/70">Helpline: 1800-XXX-XXXX</span>
              </li>
              <li>
                <span className="text-sm text-primary-foreground/70">Mon-Sat: 9:00 AM - 6:00 PM</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 border-t border-primary-foreground/10 pt-6">
          <p className="text-center text-xs text-primary-foreground/50">
            Government of India. All rights reserved. This portal is a public service initiative.
          </p>
        </div>
      </div>
    </footer>
  )
}
