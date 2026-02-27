import keralaSchemes from "@/bot/data/kerala_schemes.json"

export interface SchemeStep {
  step: number
  title: string
  action: string
  method: string
  documents: string[]
  time: string
  location?: string
}

export interface Scheme {
  id: string
  name: string
  category: string
  eligibility: {
    min_age?: number
    max_age?: number
    gender?: string[]
    income_max?: number
    ration_card?: string[]
    marital_status?: string
    housing_status?: string[]
    education?: string
    child_age_max?: number
  }
  benefit: string
  roadmap: SchemeStep[]
}

export type Category = {
  id: string
  name: string
  description: string
  icon: string
  count: number
}

// Map Kerala scheme categories to UI categories
const categoryMap: Record<string, { name: string; description: string; icon: string }> = {
  "Women Welfare": {
    name: "Women Welfare",
    description: "Welfare schemes for women and mothers",
    icon: "Users",
  },
  "Senior Citizens": {
    name: "Senior Citizens",
    description: "Pension and welfare schemes for senior citizens",
    icon: "Shield",
  },
  "Employment": {
    name: "Employment",
    description: "Employment and skill development schemes",
    icon: "Briefcase",
  },
  "Housing": {
    name: "Housing",
    description: "Housing and shelter schemes",
    icon: "Home",
  },
}

// Transform Kerala schemes to match UI format
export const schemes: Scheme[] = keralaSchemes.kerala_schemes.map((scheme: any) => ({
  id: scheme.id,
  name: scheme.name,
  category: scheme.category,
  eligibility: scheme.eligibility,
  benefit: scheme.benefit,
  roadmap: scheme.roadmap,
}))

// Generate categories from schemes
const categoryCount: Record<string, number> = {}
schemes.forEach((scheme) => {
  categoryCount[scheme.category] = (categoryCount[scheme.category] || 0) + 1
})

export const categories: Category[] = Object.entries(categoryMap).map(([key, value]) => ({
  id: key,
  name: value.name,
  description: value.description,
  icon: value.icon,
  count: categoryCount[key] || 0,
}))

// Search function
export function searchSchemes(query: string): Scheme[] {
  const lowerQuery = query.toLowerCase()
  return schemes.filter(
    (scheme) =>
      scheme.name.toLowerCase().includes(lowerQuery) ||
      scheme.category.toLowerCase().includes(lowerQuery) ||
      scheme.benefit.toLowerCase().includes(lowerQuery)
  )
}

// Get scheme by ID
export function getSchemeById(id: string): Scheme | undefined {
  return schemes.find((scheme) => scheme.id === id)
}

// Get eligible schemes based on user profile
export function getEligibleSchemes(userProfile: {
  age?: number
  gender?: string
  income?: number
  rationCard?: string
  education?: string
}): Scheme[] {
  return schemes.filter((scheme) => {
    const { eligibility } = scheme

    // Check age
    if (userProfile.age) {
      if (eligibility.min_age && userProfile.age < eligibility.min_age) return false
      if (eligibility.max_age && userProfile.age > eligibility.max_age) return false
    }

    // Check gender
    if (userProfile.gender && eligibility.gender) {
      if (!eligibility.gender.includes(userProfile.gender)) return false
    }

    // Check income
    if (userProfile.income && eligibility.income_max) {
      if (userProfile.income > eligibility.income_max) return false
    }

    // Check ration card
    if (userProfile.rationCard && eligibility.ration_card) {
      if (!eligibility.ration_card.includes(userProfile.rationCard)) return false
    }

    // Check education
    if (userProfile.education && eligibility.education) {
      if (userProfile.education !== eligibility.education) return false
    }

    return true
  })
}
