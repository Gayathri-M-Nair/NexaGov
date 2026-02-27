"use client"

import Link from "next/link"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Landmark, User, LogOut, Menu, X } from "lucide-react"
import { useState } from "react"

export function SiteHeader() {
  const { user, isLoggedIn, isGuest, logout } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-primary text-primary-foreground">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-primary-foreground/15">
            <Landmark className="h-5 w-5" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-bold leading-tight tracking-wide">NexaGov</span>
            <span className="text-[10px] leading-tight text-primary-foreground/70">Government Policy Portal</span>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          <Link
            href="/"
            className="rounded-md px-3 py-2 text-sm font-medium text-primary-foreground/80 transition-colors hover:bg-primary-foreground/10 hover:text-primary-foreground"
          >
            Home
          </Link>
          <Link
            href="/schemes"
            className="rounded-md px-3 py-2 text-sm font-medium text-primary-foreground/80 transition-colors hover:bg-primary-foreground/10 hover:text-primary-foreground"
          >
            All Schemes
          </Link>
          <Link
            href="/ai-assistant"
            className="rounded-md px-3 py-2 text-sm font-medium text-primary-foreground/80 transition-colors hover:bg-primary-foreground/10 hover:text-primary-foreground"
          >
            AI Assistant
          </Link>
        </nav>

        <div className="hidden items-center gap-2 md:flex">
          {isLoggedIn ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  className="gap-2 text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
                >
                  <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary-foreground/20 text-xs font-bold">
                    {user?.name?.charAt(0).toUpperCase()}
                  </div>
                  <span className="max-w-[120px] truncate text-sm">{user?.name}</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem asChild>
                  <Link href="/profile" className="cursor-pointer">
                    <User className="mr-2 h-4 w-4" />
                    My Profile
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={logout} className="cursor-pointer text-destructive">
                  <LogOut className="mr-2 h-4 w-4" />
                  Sign Out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <>
              {isGuest ? (
                <Link href="/login">
                  <Button
                    size="sm"
                    variant="ghost"
                    className="text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
                  >
                    Sign In
                  </Button>
                </Link>
              ) : (
                <Link href="/login">
                  <Button
                    size="sm"
                    className="bg-primary-foreground text-primary hover:bg-primary-foreground/90"
                  >
                    Sign In
                  </Button>
                </Link>
              )}
            </>
          )}
        </div>

        <button
          className="flex items-center justify-center rounded-md p-2 text-primary-foreground md:hidden"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {mobileMenuOpen && (
        <div className="border-t border-primary-foreground/10 bg-primary md:hidden">
          <nav className="flex flex-col px-4 py-3">
            <Link
              href="/"
              className="rounded-md px-3 py-2.5 text-sm font-medium text-primary-foreground/80 hover:bg-primary-foreground/10"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              href="/schemes"
              className="rounded-md px-3 py-2.5 text-sm font-medium text-primary-foreground/80 hover:bg-primary-foreground/10"
              onClick={() => setMobileMenuOpen(false)}
            >
              All Schemes
            </Link>
            <Link
              href="/ai-assistant"
              className="rounded-md px-3 py-2.5 text-sm font-medium text-primary-foreground/80 hover:bg-primary-foreground/10"
              onClick={() => setMobileMenuOpen(false)}
            >
              AI Assistant
            </Link>
            <div className="mt-2 border-t border-primary-foreground/10 pt-2">
              {isLoggedIn ? (
                <>
                  <Link
                    href="/profile"
                    className="flex items-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium text-primary-foreground/80 hover:bg-primary-foreground/10"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <User className="h-4 w-4" /> My Profile
                  </Link>
                  <button
                    onClick={() => { logout(); setMobileMenuOpen(false) }}
                    className="flex w-full items-center gap-2 rounded-md px-3 py-2.5 text-left text-sm font-medium text-primary-foreground/80 hover:bg-primary-foreground/10"
                  >
                    <LogOut className="h-4 w-4" /> Sign Out
                  </button>
                </>
              ) : (
                <Link
                  href="/login"
                  className="flex items-center justify-center rounded-md bg-primary-foreground px-3 py-2.5 text-sm font-medium text-primary"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Sign In
                </Link>
              )}
            </div>
          </nav>
        </div>
      )}
    </header>
  )
}
