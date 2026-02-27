"use client"

import { createContext, useContext, useState, useCallback, type ReactNode } from "react"

export interface UserProfile {
  name: string
  email: string
  age: number
  gender: string
  economicClass: string
  education: string
  occupation: string
  state: string
  district: string
}

interface AuthContextType {
  user: UserProfile | null
  isLoggedIn: boolean
  login: (profile: UserProfile) => void
  logout: () => void
  updateProfile: (profile: Partial<UserProfile>) => void
  continueAsGuest: () => void
  isGuest: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(null)
  const [isGuest, setIsGuest] = useState(false)

  const login = useCallback((profile: UserProfile) => {
    setUser(profile)
    setIsGuest(false)
  }, [])

  const logout = useCallback(() => {
    setUser(null)
    setIsGuest(false)
  }, [])

  const updateProfile = useCallback((updates: Partial<UserProfile>) => {
    setUser((prev) => (prev ? { ...prev, ...updates } : null))
  }, [])

  const continueAsGuest = useCallback(() => {
    setIsGuest(true)
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider
      value={{ user, isLoggedIn: !!user, login, logout, updateProfile, continueAsGuest, isGuest }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error("useAuth must be used within an AuthProvider")
  return context
}
