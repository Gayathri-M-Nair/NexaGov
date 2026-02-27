"use client"

import { useState, useMemo } from "react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { schemes, categories, searchSchemes } from "@/lib/schemes-data"
import { Search, ArrowRight, Filter, X } from "lucide-react"
import { Suspense } from "react"

function SchemesContent() {
  const searchParams = useSearchParams()
  const initialCategory = searchParams.get("category") || ""
  const initialSearch = searchParams.get("search") || ""

  const [query, setQuery] = useState(initialSearch)
  const [selectedCategory, setSelectedCategory] = useState(initialCategory)

  const filteredSchemes = useMemo(() => {
    let result = query ? searchSchemes(query) : schemes
    if (selectedCategory) {
      result = result.filter((s) => s.category === selectedCategory)
    }
    return result
  }, [query, selectedCategory])

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <SiteHeader />

      <main className="flex-1 px-4 py-8">
        <div className="mx-auto max-w-7xl">
          {/* Page Header */}
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-foreground">All Government Schemes</h1>
            <p className="mt-1 text-sm text-muted-foreground">
              Browse and search through all available government schemes
            </p>
          </div>

          {/* Search & Filter Bar */}
          <div className="mb-6 flex flex-col gap-3 md:flex-row md:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                className="h-11 pl-10"
                placeholder="Search schemes by name, ministry, or category..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
            {selectedCategory && (
              <Button
                variant="outline"
                size="sm"
                className="gap-1.5 border-border text-foreground"
                onClick={() => setSelectedCategory("")}
              >
                <Filter className="h-3.5 w-3.5" />
                {categories.find((c) => c.id === selectedCategory)?.name}
                <X className="h-3.5 w-3.5" />
              </Button>
            )}
          </div>

          {/* Category Pills */}
          <div className="mb-6 flex flex-wrap gap-2">
            <button
              className={`rounded-full px-3.5 py-1.5 text-xs font-medium transition-colors ${
                !selectedCategory
                  ? "bg-primary text-primary-foreground"
                  : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
              }`}
              onClick={() => setSelectedCategory("")}
            >
              All
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                className={`rounded-full px-3.5 py-1.5 text-xs font-medium transition-colors ${
                  selectedCategory === cat.id
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
                }`}
                onClick={() => setSelectedCategory(cat.id)}
              >
                {cat.name}
              </button>
            ))}
          </div>

          {/* Results Count */}
          <p className="mb-4 text-xs text-muted-foreground">
            Showing {filteredSchemes.length} scheme{filteredSchemes.length !== 1 ? "s" : ""}
            {query && <> for &quot;{query}&quot;</>}
            {selectedCategory && <> in {categories.find((c) => c.id === selectedCategory)?.name}</>}
          </p>

          {/* Schemes Grid */}
          {filteredSchemes.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {filteredSchemes.map((scheme) => (
                <Link key={scheme.id} href={`/scheme/${scheme.id}`}>
                  <Card className="group h-full cursor-pointer border-border transition-all hover:border-primary/30 hover:shadow-md">
                    <CardContent className="flex h-full flex-col p-5">
                      <div className="mb-3 flex items-start justify-between gap-2">
                        <Badge variant="secondary" className="shrink-0 text-[10px]">
                          {categories.find((c) => c.id === scheme.category)?.name}
                        </Badge>
                        <span className="text-[10px] text-muted-foreground">{scheme.steps.length} steps</span>
                      </div>
                      <h3 className="mb-1.5 font-semibold leading-snug text-card-foreground group-hover:text-primary">
                        {scheme.title}
                      </h3>
                      <p className="mb-3 flex-1 text-xs leading-relaxed text-muted-foreground">
                        {scheme.shortDescription}
                      </p>
                      <div className="flex flex-wrap gap-1.5 border-t border-border pt-3">
                        {scheme.benefits.slice(0, 2).map((b, i) => (
                          <span key={i} className="rounded bg-accent/10 px-2 py-0.5 text-[10px] text-accent">
                            {b.split(" ").slice(0, 5).join(" ")}...
                          </span>
                        ))}
                      </div>
                      <div className="mt-3 flex items-center justify-between">
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
          ) : (
            <div className="py-16 text-center">
              <p className="text-lg font-medium text-foreground">No schemes found</p>
              <p className="mt-1 text-sm text-muted-foreground">
                Try adjusting your search or filter criteria
              </p>
            </div>
          )}
        </div>
      </main>

      <SiteFooter />
    </div>
  )
}

export default function SchemesPage() {
  return (
    <Suspense fallback={<div className="flex min-h-screen items-center justify-center text-muted-foreground">Loading...</div>}>
      <SchemesContent />
    </Suspense>
  )
}
