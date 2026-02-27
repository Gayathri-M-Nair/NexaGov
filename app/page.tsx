"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { categories, schemes, searchSchemes } from "@/lib/schemes-data"
import { useAuth } from "@/lib/auth-context"
import {
  Search,
  ArrowRight,
  GraduationCap,
  Heart,
  Home,
  Wheat,
  Briefcase,
  Users,
  Shield,
  Landmark,
  Sparkles,
  ChevronRight,
  FileText,
  Bot,
} from "lucide-react"

const iconMap: Record<string, React.ReactNode> = {
  GraduationCap: <GraduationCap className="h-6 w-6" />,
  Heart: <Heart className="h-6 w-6" />,
  Home: <Home className="h-6 w-6" />,
  Wheat: <Wheat className="h-6 w-6" />,
  Briefcase: <Briefcase className="h-6 w-6" />,
  Users: <Users className="h-6 w-6" />,
  Shield: <Shield className="h-6 w-6" />,
  Landmark: <Landmark className="h-6 w-6" />,
}

export default function HomePage() {
  const router = useRouter()
  const { isLoggedIn } = useAuth()
  const [searchQuery, setSearchQuery] = useState("")
  const [searchResults, setSearchResults] = useState<ReturnType<typeof searchSchemes>>([])
  const [showResults, setShowResults] = useState(false)

  function handleSearch(q: string) {
    setSearchQuery(q)
    if (q.trim().length > 1) {
      setSearchResults(searchSchemes(q))
      setShowResults(true)
    } else {
      setShowResults(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <SiteHeader />

      {/* Hero Section */}
      <section className="relative bg-primary px-4 py-16 text-primary-foreground md:py-24">
        <div className="mx-auto max-w-4xl text-center">
          <Badge className="mb-4 border-primary-foreground/20 bg-primary-foreground/10 text-primary-foreground hover:bg-primary-foreground/15">
            Government of India Initiative
          </Badge>
          <h1 className="text-balance text-3xl font-bold leading-tight tracking-tight md:text-5xl">
            Find Government Schemes
            <br />
            Made For You
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-pretty text-base text-primary-foreground/75 md:text-lg">
            Discover schemes you are eligible for, get step-by-step application roadmaps, and let AI automate the process for you.
          </p>

          {/* Search */}
          <div className="relative mx-auto mt-8 max-w-2xl">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
              <Input
                className="h-14 rounded-xl border-0 bg-card pl-12 pr-4 text-base text-card-foreground shadow-lg placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring"
                placeholder="Search for schemes, benefits, or categories..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                onFocus={() => searchQuery.length > 1 && setShowResults(true)}
                onBlur={() => setTimeout(() => setShowResults(false), 200)}
              />
            </div>

            {showResults && searchResults.length > 0 && (
              <div className="absolute left-0 right-0 top-full z-50 mt-2 overflow-hidden rounded-xl border border-border bg-card shadow-xl">
                {searchResults.slice(0, 5).map((scheme) => (
                  <Link
                    key={scheme.id}
                    href={`/scheme/${scheme.id}`}
                    className="flex items-center gap-3 px-4 py-3 text-left transition-colors hover:bg-secondary"
                  >
                    <FileText className="h-4 w-4 shrink-0 text-muted-foreground" />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium text-card-foreground">{scheme.title}</p>
                      <p className="truncate text-xs text-muted-foreground">{scheme.ministry}</p>
                    </div>
                    <Badge variant="secondary" className="shrink-0 text-[10px]">
                      {categories.find((c) => c.id === scheme.category)?.name}
                    </Badge>
                  </Link>
                ))}
                {searchResults.length > 5 && (
                  <Link
                    href={`/schemes?search=${encodeURIComponent(searchQuery)}`}
                    className="flex items-center justify-center gap-1 border-t border-border px-4 py-2.5 text-xs font-medium text-primary hover:bg-secondary"
                  >
                    View all {searchResults.length} results
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                )}
              </div>
            )}

            {showResults && searchQuery.length > 1 && searchResults.length === 0 && (
              <div className="absolute left-0 right-0 top-full z-50 mt-2 rounded-xl border border-border bg-card p-6 text-center shadow-xl">
                <p className="text-sm text-muted-foreground">No schemes found for &quot;{searchQuery}&quot;</p>
              </div>
            )}
          </div>

          <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
            {!isLoggedIn && (
              <Link href="/login">
                <Button className="gap-2 bg-primary-foreground text-primary hover:bg-primary-foreground/90">
                  Get Personalized Recommendations
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            )}
            <Link href="/ai-assistant">
              <Button
                variant="outline"
                className="gap-2 border-primary-foreground/30 bg-transparent text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground"
              >
                <Bot className="h-4 w-4" />
                Try AI Assistant
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="border-b border-border bg-card px-4 py-6">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-center gap-8 md:gap-16">
          <div className="text-center">
            <p className="text-2xl font-bold text-foreground">{schemes.length}+</p>
            <p className="text-xs text-muted-foreground">Schemes Listed</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-foreground">{categories.length}</p>
            <p className="text-xs text-muted-foreground">Categories</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-foreground">8+</p>
            <p className="text-xs text-muted-foreground">Ministries Covered</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-foreground">24/7</p>
            <p className="text-xs text-muted-foreground">AI Assistance</p>
          </div>
        </div>
      </section>

      {/* Categories Grid */}
      <section className="px-4 py-16">
        <div className="mx-auto max-w-7xl">
          <div className="mb-8 flex items-end justify-between">
            <div>
              <h2 className="text-2xl font-bold text-foreground">Browse by Category</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                Explore government schemes organized by sector
              </p>
            </div>
            <Link href="/schemes" className="hidden items-center gap-1 text-sm font-medium text-primary hover:underline md:flex">
              View All Schemes <ChevronRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {categories.map((cat) => (
              <Link key={cat.id} href={`/schemes?category=${cat.id}`}>
                <Card className="group cursor-pointer border-border transition-all hover:border-primary/30 hover:shadow-md">
                  <CardContent className="flex items-start gap-4 p-5">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                      {iconMap[cat.icon]}
                    </div>
                    <div className="min-w-0 flex-1">
                      <h3 className="font-semibold text-card-foreground">{cat.name}</h3>
                      <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">{cat.description}</p>
                      <p className="mt-2 text-xs font-medium text-primary">{cat.count} schemes</p>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>

          <div className="mt-6 text-center md:hidden">
            <Link href="/schemes">
              <Button variant="outline" className="gap-1 border-border text-foreground">
                View All Schemes <ChevronRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Schemes */}
      <section className="bg-secondary px-4 py-16">
        <div className="mx-auto max-w-7xl">
          <h2 className="mb-2 text-2xl font-bold text-foreground">Popular Schemes</h2>
          <p className="mb-8 text-sm text-muted-foreground">Most searched and applied-for government schemes</p>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {schemes.slice(0, 6).map((scheme) => (
              <Link key={scheme.id} href={`/scheme/${scheme.id}`}>
                <Card className="group h-full cursor-pointer border-border transition-all hover:border-primary/30 hover:shadow-md">
                  <CardContent className="flex h-full flex-col p-5">
                    <div className="mb-3 flex items-start justify-between gap-2">
                      <Badge variant="secondary" className="shrink-0 text-[10px]">
                        {scheme.category}
                      </Badge>
                      <span className="text-[10px] text-muted-foreground">{scheme.roadmap.length} steps</span>
                    </div>
                    <h3 className="mb-1.5 font-semibold leading-snug text-card-foreground group-hover:text-primary">
                      {scheme.name}
                    </h3>
                    <p className="mb-3 flex-1 text-xs leading-relaxed text-muted-foreground">
                      {scheme.benefit}
                    </p>
                    <div className="flex items-center justify-between border-t border-border pt-3">
                      <span className="text-[10px] text-muted-foreground">{scheme.ministry}</span>
                      <span className="flex items-center gap-1 text-xs font-medium text-primary">
                        View Roadmap <ArrowRight className="h-3 w-3" />
                      </span>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* AI CTA */}
      <section className="px-4 py-16">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-accent/15">
            <Sparkles className="h-7 w-7 text-accent" />
          </div>
          <h2 className="text-2xl font-bold text-foreground">
            Let AI Handle Your Applications
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-sm leading-relaxed text-muted-foreground">
            Our AI assistant can help you understand any scheme, check your eligibility, gather the right documents, and guide you through every step of the application process.
          </p>
          <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
            <Link href="/ai-assistant">
              <Button className="gap-2 bg-primary text-primary-foreground hover:bg-primary/90">
                <Bot className="h-4 w-4" />
                Start AI Assistant
              </Button>
            </Link>
            {!isLoggedIn && (
              <Link href="/login">
                <Button variant="outline" className="gap-2 border-border text-foreground">
                  Create Profile First
                </Button>
              </Link>
            )}
          </div>
        </div>
      </section>

      <SiteFooter />
    </div>
  )
}
