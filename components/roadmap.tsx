"use client"

import { useState } from "react"
import type { SchemeStep } from "@/lib/schemes-data"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  CheckCircle2,
  Circle,
  Clock,
  MapPin,
  FileText,
  Copy,
  Lightbulb,
  ChevronDown,
  ChevronUp,
} from "lucide-react"
import { cn } from "@/lib/utils"

interface RoadmapProps {
  steps: SchemeStep[]
}

export function Roadmap({ steps }: RoadmapProps) {
  const [expandedStep, setExpandedStep] = useState<number | null>(steps[0]?.step || null)
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set())

  function toggleStep(stepNum: number) {
    setExpandedStep(expandedStep === stepNum ? null : stepNum)
  }

  function toggleComplete(stepNum: number, e: React.MouseEvent) {
    e.stopPropagation()
    setCompletedSteps((prev) => {
      const next = new Set(prev)
      if (next.has(stepNum)) {
        next.delete(stepNum)
      } else {
        next.add(stepNum)
      }
      return next
    })
  }

  const completedCount = completedSteps.size
  const progress = steps.length > 0 ? (completedCount / steps.length) * 100 : 0

  return (
    <div className="flex flex-col gap-0">
      {/* Progress Bar */}
      <div className="mb-6 rounded-lg bg-secondary p-4">
        <div className="mb-2 flex items-center justify-between">
          <span className="text-xs font-medium text-foreground">Application Progress</span>
          <span className="text-xs text-muted-foreground">
            {completedCount} of {steps.length} steps completed
          </span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-border">
          <div
            className="h-full rounded-full bg-accent transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Steps */}
      <div className="relative">
        {steps.map((step, index) => {
          const isExpanded = expandedStep === step.step
          const isCompleted = completedSteps.has(step.step)
          const isLast = index === steps.length - 1

          return (
            <div key={step.step} className="relative flex gap-4">
              {/* Timeline Line & Circle */}
              <div className="flex flex-col items-center">
                <button
                  onClick={(e) => toggleComplete(step.step, e)}
                  className={cn(
                    "relative z-10 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border-2 transition-all",
                    isCompleted
                      ? "border-accent bg-accent text-accent-foreground"
                      : isExpanded
                        ? "border-primary bg-primary text-primary-foreground"
                        : "border-border bg-card text-muted-foreground hover:border-primary/50"
                  )}
                  aria-label={isCompleted ? `Mark step ${step.step} as incomplete` : `Mark step ${step.step} as complete`}
                >
                  {isCompleted ? (
                    <CheckCircle2 className="h-4 w-4" />
                  ) : (
                    <span className="text-xs font-bold">{step.step}</span>
                  )}
                </button>
                {!isLast && (
                  <div
                    className={cn(
                      "w-0.5 flex-1",
                      isCompleted ? "bg-accent" : "bg-border"
                    )}
                  />
                )}
              </div>

              {/* Step Content */}
              <div className={cn("mb-4 flex-1 pb-2", !isLast && "pb-4")}>
                <button
                  onClick={() => toggleStep(step.step)}
                  className="flex w-full items-start justify-between text-left"
                >
                  <div className="flex-1">
                    <h3
                      className={cn(
                        "text-sm font-semibold",
                        isCompleted
                          ? "text-accent"
                          : isExpanded
                            ? "text-foreground"
                            : "text-foreground/80"
                      )}
                    >
                      {step.title}
                    </h3>
                    <p className="mt-0.5 text-xs text-muted-foreground">{step.action}</p>
                  </div>
                  <div className="ml-2 mt-0.5 shrink-0 text-muted-foreground">
                    {isExpanded ? (
                      <ChevronUp className="h-4 w-4" />
                    ) : (
                      <ChevronDown className="h-4 w-4" />
                    )}
                  </div>
                </button>

                {/* Expanded Details */}
                {isExpanded && (
                  <Card className="mt-3 border-border">
                    <CardContent className="flex flex-col gap-4 p-4">
                      {/* Detailed Description */}
                      <p className="text-xs leading-relaxed text-foreground/80">
                        {step.action}
                      </p>

                      {/* Meta Info */}
                      <div className="grid gap-2 sm:grid-cols-3">
                        {step.location && (
                          <div className="flex items-center gap-2 rounded-md bg-secondary px-3 py-2">
                            <MapPin className="h-3.5 w-3.5 shrink-0 text-primary" />
                            <div>
                              <p className="text-[10px] text-muted-foreground">Location</p>
                              <p className="text-xs font-medium text-foreground">{step.location}</p>
                            </div>
                          </div>
                        )}
                        <div className="flex items-center gap-2 rounded-md bg-secondary px-3 py-2">
                          <Clock className="h-3.5 w-3.5 shrink-0 text-primary" />
                          <div>
                            <p className="text-[10px] text-muted-foreground">Estimated Time</p>
                            <p className="text-xs font-medium text-foreground">{step.time}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 rounded-md bg-secondary px-3 py-2">
                          <FileText className="h-3.5 w-3.5 shrink-0 text-primary" />
                          <div>
                            <p className="text-[10px] text-muted-foreground">Method</p>
                            <p className="text-xs font-medium text-foreground">{step.method}</p>
                          </div>
                        </div>
                      </div>

                      {/* Documents Required */}
                      {step.documents.length > 0 && (
                        <div>
                          <h4 className="mb-2 flex items-center gap-1.5 text-xs font-semibold text-foreground">
                            <FileText className="h-3.5 w-3.5 text-primary" />
                            Documents Required
                          </h4>
                          <div className="flex flex-wrap gap-1.5">
                            {step.documents.map((doc, i) => (
                              <Badge
                                key={i}
                                variant="outline"
                                className="border-border bg-card text-[10px] text-foreground"
                              >
                                {doc}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Complete Button */}
                      <button
                        onClick={(e) => toggleComplete(step.step, e)}
                        className={cn(
                          "flex items-center justify-center gap-2 rounded-md px-4 py-2 text-xs font-medium transition-colors",
                          isCompleted
                            ? "bg-accent/10 text-accent"
                            : "bg-primary text-primary-foreground hover:bg-primary/90"
                        )}
                      >
                        {isCompleted ? (
                          <>
                            <CheckCircle2 className="h-3.5 w-3.5" />
                            Completed - Click to Undo
                          </>
                        ) : (
                          <>
                            <Circle className="h-3.5 w-3.5" />
                            Mark as Completed
                          </>
                        )}
                      </button>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
