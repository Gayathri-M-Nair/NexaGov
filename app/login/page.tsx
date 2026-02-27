"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useAuth, type UserProfile } from "@/lib/auth-context"
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
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Landmark, ArrowRight, UserPlus } from "lucide-react"
import Link from "next/link"

export default function LoginPage() {
  const router = useRouter()
  const { login, continueAsGuest } = useAuth()
  const [mode, setMode] = useState<"choice" | "register">("choice")
  const [formData, setFormData] = useState<Partial<UserProfile>>({
    name: "",
    email: "",
    age: undefined,
    gender: "",
    economicClass: "",
    education: "",
    occupation: "",
    state: "",
    district: "",
  })

  function handleRegister(e: React.FormEvent) {
    e.preventDefault()
    if (formData.name && formData.email && formData.age) {
      login(formData as UserProfile)
      router.push("/profile")
    }
  }

  function handleGuest() {
    continueAsGuest()
    router.push("/")
  }

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <div className="flex flex-1 flex-col items-center justify-center px-4 py-12">
        <Link href="/" className="mb-8 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary">
            <Landmark className="h-6 w-6 text-primary-foreground" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-wide text-foreground">JAN SEVA KENDRA</span>
            <span className="text-xs text-muted-foreground">Government Policy Portal</span>
          </div>
        </Link>

        {mode === "choice" ? (
          <Card className="w-full max-w-md border-border">
            <CardHeader className="text-center">
              <CardTitle className="text-xl font-bold text-foreground">Welcome to Jan Seva Kendra</CardTitle>
              <CardDescription className="text-muted-foreground">
                Sign in to access personalized scheme recommendations or continue as a guest to browse all schemes.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <Button
                className="h-12 gap-2 bg-primary text-primary-foreground hover:bg-primary/90"
                onClick={() => setMode("register")}
              >
                <UserPlus className="h-4 w-4" />
                Create Account / Sign In
              </Button>
              <div className="relative flex items-center py-1">
                <div className="flex-1 border-t border-border" />
                <span className="px-4 text-xs text-muted-foreground">OR</span>
                <div className="flex-1 border-t border-border" />
              </div>
              <Button
                variant="outline"
                className="h-12 gap-2 border-border text-foreground hover:bg-secondary"
                onClick={handleGuest}
              >
                <ArrowRight className="h-4 w-4" />
                Continue Without Account
              </Button>
              <p className="mt-2 text-center text-xs text-muted-foreground">
                Creating an account allows us to find schemes you are eligible for based on your profile.
              </p>
            </CardContent>
          </Card>
        ) : (
          <Card className="w-full max-w-lg border-border">
            <CardHeader>
              <CardTitle className="text-lg font-bold text-foreground">Create Your Profile</CardTitle>
              <CardDescription className="text-muted-foreground">
                Fill in your details so we can find schemes you are eligible for.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleRegister} className="flex flex-col gap-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="flex flex-col gap-1.5">
                    <Label htmlFor="name" className="text-foreground">Full Name *</Label>
                    <Input
                      id="name"
                      placeholder="Enter your full name"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                    />
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <Label htmlFor="email" className="text-foreground">Email *</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="you@example.com"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      required
                    />
                  </div>
                </div>

                <div className="grid gap-4 md:grid-cols-3">
                  <div className="flex flex-col gap-1.5">
                    <Label htmlFor="age" className="text-foreground">Age *</Label>
                    <Input
                      id="age"
                      type="number"
                      placeholder="Age"
                      min={1}
                      max={120}
                      value={formData.age || ""}
                      onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) || undefined })}
                      required
                    />
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <Label className="text-foreground">Gender</Label>
                    <Select
                      value={formData.gender}
                      onValueChange={(v) => setFormData({ ...formData, gender: v })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Male">Male</SelectItem>
                        <SelectItem value="Female">Female</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <Label className="text-foreground">Economic Class</Label>
                    <Select
                      value={formData.economicClass}
                      onValueChange={(v) => setFormData({ ...formData, economicClass: v })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="BPL">BPL (Below Poverty Line)</SelectItem>
                        <SelectItem value="EWS">EWS (Economically Weaker)</SelectItem>
                        <SelectItem value="LIG">LIG (Low Income Group)</SelectItem>
                        <SelectItem value="MIG">MIG (Middle Income Group)</SelectItem>
                        <SelectItem value="HIG">HIG (High Income Group)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="flex flex-col gap-1.5">
                    <Label className="text-foreground">Education</Label>
                    <Select
                      value={formData.education}
                      onValueChange={(v) => setFormData({ ...formData, education: v })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
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
                  <div className="flex flex-col gap-1.5">
                    <Label className="text-foreground">Occupation</Label>
                    <Select
                      value={formData.occupation}
                      onValueChange={(v) => setFormData({ ...formData, occupation: v })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
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

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="flex flex-col gap-1.5">
                    <Label htmlFor="state" className="text-foreground">State</Label>
                    <Input
                      id="state"
                      placeholder="Your state"
                      value={formData.state}
                      onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                    />
                  </div>
                  <div className="flex flex-col gap-1.5">
                    <Label htmlFor="district" className="text-foreground">District</Label>
                    <Input
                      id="district"
                      placeholder="Your district"
                      value={formData.district}
                      onChange={(e) => setFormData({ ...formData, district: e.target.value })}
                    />
                  </div>
                </div>

                <div className="mt-2 flex gap-3">
                  <Button
                    type="button"
                    variant="outline"
                    className="flex-1 border-border text-foreground"
                    onClick={() => setMode("choice")}
                  >
                    Back
                  </Button>
                  <Button type="submit" className="flex-1 bg-primary text-primary-foreground hover:bg-primary/90">
                    Create Account
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
