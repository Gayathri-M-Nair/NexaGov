"use client"

import { use } from "react"
import Link from "next/link"
import { notFound } from "next/navigation"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { Roadmap } from "@/components/roadmap"
import { getSchemeById, categories } from "@/lib/schemes-data"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  ArrowLeft,
  ExternalLink,
  Phone,
  Calendar,
  Bot,
  CheckCircle2,
  Building2,
} from "lucide-react"

export default function SchemeDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = use(params)
  const scheme = getSchemeById(id)

  if (!scheme) {
    notFound()
  }

  const category = categories.find((c) => c.id === scheme.category)

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <SiteHeader />

      <main className="flex-1">
        {/* Scheme Header */}
        <div className="border-b border-border bg-primary px-4 py-8 text-primary-foreground">
          <div className="mx-auto max-w-5xl">
            <Link
              href="/schemes"
              className="mb-4 inline-flex items-center gap-1.5 text-xs text-primary-foreground/70 transition-colors hover:text-primary-foreground"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              Back to All Schemes
            </Link>

            <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
              <div className="flex-1">
                <div className="mb-2 flex flex-wrap items-center gap-2">
                  <Badge className="border-primary-foreground/20 bg-primary-foreground/10 text-primary-foreground text-[10px]">
                    {scheme.category}
                  </Badge>
                </div>
                <h1 className="text-2xl font-bold md:text-3xl">{scheme.name}</h1>
                <p className="mt-2 text-sm text-primary-foreground/75 md:text-base">
                  {scheme.benefit}
                </p>
              </div>
            </div>

            {/* Quick Info */}
            <div className="mt-6 flex flex-wrap gap-3">
              <div className="flex items-center gap-1.5 rounded-md bg-primary-foreground/10 px-3 py-1.5 text-xs">
                <Phone className="h-3.5 w-3.5" />
                Kerala Govt Helpline
              </div>
            </div>
          </div>
        </div>

        <div className="mx-auto max-w-5xl px-4 py-8">
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Roadmap - Main Content */}
            <div className="lg:col-span-2">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-lg font-bold text-foreground">Application Roadmap</h2>
                <span className="text-xs text-muted-foreground">{scheme.roadmap.length} steps</span>
              </div>
              <Roadmap steps={scheme.roadmap} />
            </div>

            {/* Sidebar */}
            <div className="flex flex-col gap-4 lg:col-span-1">
              {/* Benefits */}
              <Card className="border-border">
                <CardContent className="p-4">
                  <h3 className="mb-3 text-sm font-semibold text-card-foreground">Key Benefit</h3>
                  <div className="flex items-start gap-2 text-xs text-foreground/80">
                    <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-accent" />
                    {scheme.benefit}
                  </div>
                </CardContent>
              </Card>

              {/* Eligibility */}
              <Card className="border-border">
                <CardContent className="p-4">
                  <h3 className="mb-3 text-sm font-semibold text-card-foreground">Eligibility Criteria</h3>
                  <div className="flex flex-col gap-2">
                    {scheme.eligibility.min_age && (
                      <div className="flex items-center justify-between rounded bg-secondary px-2.5 py-1.5">
                        <span className="text-[10px] text-muted-foreground">Min Age</span>
                        <span className="text-xs font-medium text-foreground">{scheme.eligibility.min_age} years</span>
                      </div>
                    )}
                    {scheme.eligibility.max_age && (
                      <div className="flex items-center justify-between rounded bg-secondary px-2.5 py-1.5">
                        <span className="text-[10px] text-muted-foreground">Max Age</span>
                        <span className="text-xs font-medium text-foreground">{scheme.eligibility.max_age} years</span>
                      </div>
                    )}
                    {scheme.eligibility.income_max && (
                      <div className="flex items-center justify-between rounded bg-secondary px-2.5 py-1.5">
                        <span className="text-[10px] text-muted-foreground">Max Income</span>
                        <span className="text-xs font-medium text-foreground">₹{scheme.eligibility.income_max.toLocaleString()}</span>
                      </div>
                    )}
                    {scheme.eligibility.gender && (
                      <div className="rounded bg-secondary px-2.5 py-1.5">
                        <span className="text-[10px] text-muted-foreground">Gender</span>
                        <div className="mt-1 flex flex-wrap gap-1">
                          {scheme.eligibility.gender.map((g) => (
                            <Badge key={g} variant="outline" className="border-border text-[10px] text-foreground">
                              {g}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                    {scheme.eligibility.ration_card && (
                      <div className="rounded bg-secondary px-2.5 py-1.5">
                        <span className="text-[10px] text-muted-foreground">Ration Card</span>
                        <div className="mt-1 flex flex-wrap gap-1">
                          {scheme.eligibility.ration_card.map((r) => (
                            <Badge key={r} variant="outline" className="border-border text-[10px] text-foreground">
                              {r}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                    {scheme.eligibility.education && (
                      <div className="rounded bg-secondary px-2.5 py-1.5">
                        <span className="text-[10px] text-muted-foreground">Education</span>
                        <Badge variant="outline" className="border-border text-[10px] text-foreground">
                          {scheme.eligibility.education}
                        </Badge>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* AI Help */}
              <Card className="border-primary/20 bg-primary/5">
                <CardContent className="p-4">
                  <h3 className="mb-1.5 text-sm font-semibold text-card-foreground">Need Help?</h3>
                  <p className="mb-3 text-xs text-muted-foreground">
                    Our AI assistant can guide you through the entire application process for this scheme.
                  </p>
                  <Link href={`/ai-assistant?scheme=${scheme.id}`}>
                    <Button className="w-full gap-2 bg-primary text-primary-foreground hover:bg-primary/90" size="sm">
                      <Bot className="h-3.5 w-3.5" />
                      Get AI Assistance
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>

      <SiteFooter />
    </div>
  )
}
