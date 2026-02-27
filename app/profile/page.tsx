"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import { useAuth } from "@/lib/auth-context"
import { getEligibleSchemes, categories } from "@/lib/schemes-data"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  User,
  ArrowRight,
  CheckCircle2,
  Edit3,
  Save,
  X,
} from "lucide-react"
import { useState } from "react"

export default function ProfilePage() {
  const router = useRouter()
  const { user, isLoggedIn, updateProfile } = useAuth()
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState(user)

  useEffect(() => {
    if (!isLoggedIn) {
      router.push("/login")
    }
  }, [isLoggedIn, router])

  useEffect(() => {
    setFormData(user)
  }, [user])

  if (!isLoggedIn || !user) {
    return null
  }

  const eligibleSchemes = getEligibleSchemes({
    age: user.age,
    economicClass: user.economicClass,
    gender: user.gender,
    education: user.education,
    occupation: user.occupation,
  })

  function handleSave() {
    if (formData) {
      updateProfile(formData)
      setEditing(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <SiteHeader />

      <main className="flex-1 px-4 py-8">
        <div className="mx-auto max-w-6xl">
          <div className="mb-8 grid gap-6 lg:grid-cols-3">
            {/* Profile Card */}
            <div className="lg:col-span-1">
              <Card className="border-border">
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg text-card-foreground">My Profile</CardTitle>
                    {!editing ? (
                      <Button
                        variant="ghost"
                        size="sm"
                        className="gap-1.5 text-primary"
                        onClick={() => setEditing(true)}
                      >
                        <Edit3 className="h-3.5 w-3.5" /> Edit
                      </Button>
                    ) : (
                      <div className="flex gap-1">
                        <Button variant="ghost" size="sm" onClick={() => { setEditing(false); setFormData(user) }}>
                          <X className="h-3.5 w-3.5" />
                        </Button>
                        <Button size="sm" className="gap-1 bg-primary text-primary-foreground" onClick={handleSave}>
                          <Save className="h-3.5 w-3.5" /> Save
                        </Button>
                      </div>
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="mb-4 flex items-center gap-3">
                    <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 text-xl font-bold text-primary">
                      {user.name?.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <p className="font-semibold text-card-foreground">{user.name}</p>
                      <p className="text-xs text-muted-foreground">{user.email}</p>
                    </div>
                  </div>

                  {editing ? (
                    <div className="flex flex-col gap-3">
                      <div className="flex flex-col gap-1">
                        <Label className="text-xs text-foreground">Full Name</Label>
                        <Input
                          value={formData?.name || ""}
                          onChange={(e) => setFormData((f) => f ? { ...f, name: e.target.value } : f)}
                        />
                      </div>
                      <div className="flex flex-col gap-1">
                        <Label className="text-xs text-foreground">Age</Label>
                        <Input
                          type="number"
                          value={formData?.age || ""}
                          onChange={(e) => setFormData((f) => f ? { ...f, age: parseInt(e.target.value) || 0 } : f)}
                        />
                      </div>
                      <div className="flex flex-col gap-1">
                        <Label className="text-xs text-foreground">Gender</Label>
                        <Select
                          value={formData?.gender || ""}
                          onValueChange={(v) => setFormData((f) => f ? { ...f, gender: v } : f)}
                        >
                          <SelectTrigger><SelectValue /></SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Male">Male</SelectItem>
                            <SelectItem value="Female">Female</SelectItem>
                            <SelectItem value="Other">Other</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="flex flex-col gap-1">
                        <Label className="text-xs text-foreground">Economic Class</Label>
                        <Select
                          value={formData?.economicClass || ""}
                          onValueChange={(v) => setFormData((f) => f ? { ...f, economicClass: v } : f)}
                        >
                          <SelectTrigger><SelectValue /></SelectTrigger>
                          <SelectContent>
                            <SelectItem value="BPL">BPL</SelectItem>
                            <SelectItem value="EWS">EWS</SelectItem>
                            <SelectItem value="LIG">LIG</SelectItem>
                            <SelectItem value="MIG">MIG</SelectItem>
                            <SelectItem value="HIG">HIG</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="flex flex-col gap-1">
                        <Label className="text-xs text-foreground">Education</Label>
                        <Select
                          value={formData?.education || ""}
                          onValueChange={(v) => setFormData((f) => f ? { ...f, education: v } : f)}
                        >
                          <SelectTrigger><SelectValue /></SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Below 8th">Below 8th</SelectItem>
                            <SelectItem value="8th Pass">8th Pass</SelectItem>
                            <SelectItem value="10th Pass">10th Pass</SelectItem>
                            <SelectItem value="12th Pass">12th Pass</SelectItem>
                            <SelectItem value="Graduate">Graduate</SelectItem>
                            <SelectItem value="Post Graduate">Post Graduate</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="flex flex-col gap-1">
                        <Label className="text-xs text-foreground">Occupation</Label>
                        <Select
                          value={formData?.occupation || ""}
                          onValueChange={(v) => setFormData((f) => f ? { ...f, occupation: v } : f)}
                        >
                          <SelectTrigger><SelectValue /></SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Student">Student</SelectItem>
                            <SelectItem value="Farmer">Farmer</SelectItem>
                            <SelectItem value="Self-Employed">Self-Employed</SelectItem>
                            <SelectItem value="Entrepreneur">Entrepreneur</SelectItem>
                            <SelectItem value="Salaried">Salaried</SelectItem>
                            <SelectItem value="Unemployed">Unemployed</SelectItem>
                            <SelectItem value="Retired">Retired</SelectItem>
                            <SelectItem value="Homemaker">Homemaker</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  ) : (
                    <div className="flex flex-col gap-2.5">
                      <ProfileField label="Age" value={user.age ? `${user.age} years` : "Not set"} />
                      <ProfileField label="Gender" value={user.gender || "Not set"} />
                      <ProfileField label="Economic Class" value={user.economicClass || "Not set"} />
                      <ProfileField label="Education" value={user.education || "Not set"} />
                      <ProfileField label="Occupation" value={user.occupation || "Not set"} />
                      <ProfileField label="State" value={user.state || "Not set"} />
                      <ProfileField label="District" value={user.district || "Not set"} />
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Eligible Schemes */}
            <div className="lg:col-span-2">
              <div className="mb-4 flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent/15">
                  <CheckCircle2 className="h-5 w-5 text-accent" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-foreground">Schemes You Are Eligible For</h2>
                  <p className="text-xs text-muted-foreground">
                    Based on your profile, we found {eligibleSchemes.length} scheme{eligibleSchemes.length !== 1 ? "s" : ""} you may qualify for
                  </p>
                </div>
              </div>

              {eligibleSchemes.length > 0 ? (
                <div className="grid gap-3 sm:grid-cols-2">
                  {eligibleSchemes.map((scheme) => (
                    <Link key={scheme.id} href={`/scheme/${scheme.id}`}>
                      <Card className="group h-full cursor-pointer border-border transition-all hover:border-primary/30 hover:shadow-md">
                        <CardContent className="flex h-full flex-col p-4">
                          <Badge variant="secondary" className="mb-2 w-fit text-[10px]">
                            {categories.find((c) => c.id === scheme.category)?.name}
                          </Badge>
                          <h3 className="mb-1 text-sm font-semibold text-card-foreground group-hover:text-primary">
                            {scheme.title}
                          </h3>
                          <p className="mb-3 flex-1 text-xs leading-relaxed text-muted-foreground">
                            {scheme.shortDescription}
                          </p>
                          <div className="flex items-center justify-between border-t border-border pt-2.5">
                            <div className="flex items-center gap-1 text-[10px] text-accent">
                              <CheckCircle2 className="h-3 w-3" /> Eligible
                            </div>
                            <span className="flex items-center gap-1 text-xs font-medium text-primary">
                              Apply <ArrowRight className="h-3 w-3" />
                            </span>
                          </div>
                        </CardContent>
                      </Card>
                    </Link>
                  ))}
                </div>
              ) : (
                <Card className="border-border">
                  <CardContent className="py-12 text-center">
                    <User className="mx-auto h-10 w-10 text-muted-foreground/40" />
                    <p className="mt-3 font-medium text-foreground">Complete your profile to see eligible schemes</p>
                    <p className="mt-1 text-sm text-muted-foreground">
                      Add your economic class, education, and occupation details to find matching schemes.
                    </p>
                    <Button
                      className="mt-4 bg-primary text-primary-foreground"
                      onClick={() => setEditing(true)}
                    >
                      Complete Profile
                    </Button>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </div>
      </main>

      <SiteFooter />
    </div>
  )
}

function ProfileField({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between rounded-lg bg-secondary px-3 py-2">
      <span className="text-xs text-muted-foreground">{label}</span>
      <span className="text-xs font-medium text-foreground">{value}</span>
    </div>
  )
}
