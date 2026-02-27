export interface SchemeStep {
  id: string
  title: string
  description: string
  details: string
  documents: string[]
  copies: number
  location: string
  estimatedTime: string
  tips: string[]
}

export interface Scheme {
  id: string
  title: string
  shortDescription: string
  description: string
  category: string
  ministry: string
  eligibility: {
    minAge?: number
    maxAge?: number
    economicClass?: string[]
    gender?: string[]
    education?: string[]
    occupation?: string[]
  }
  benefits: string[]
  steps: SchemeStep[]
  applicationDeadline?: string
  websiteUrl?: string
  helplineNumber?: string
}

export type Category = {
  id: string
  name: string
  description: string
  icon: string
  count: number
}

export const categories: Category[] = [
  {
    id: "education",
    name: "Education",
    description: "Scholarships, skill development, and educational support programs",
    icon: "GraduationCap",
    count: 5,
  },
  {
    id: "healthcare",
    name: "Healthcare",
    description: "Medical insurance, health programs, and welfare schemes",
    icon: "Heart",
    count: 4,
  },
  {
    id: "housing",
    name: "Housing",
    description: "Affordable housing and urban development programs",
    icon: "Home",
    count: 3,
  },
  {
    id: "agriculture",
    name: "Agriculture",
    description: "Farm subsidies, crop insurance, and rural development",
    icon: "Wheat",
    count: 4,
  },
  {
    id: "employment",
    name: "Employment",
    description: "Job creation, skill training, and livelihood programs",
    icon: "Briefcase",
    count: 3,
  },
  {
    id: "women-child",
    name: "Women & Child",
    description: "Empowerment programs for women and child welfare",
    icon: "Users",
    count: 4,
  },
  {
    id: "social-welfare",
    name: "Social Welfare",
    description: "Pension schemes, disability support, and social security",
    icon: "Shield",
    count: 3,
  },
  {
    id: "finance",
    name: "Financial Inclusion",
    description: "Banking, loans, and financial literacy programs",
    icon: "Landmark",
    count: 3,
  },
]

export const schemes: Scheme[] = [
  {
    id: "pm-scholarship",
    title: "PM National Scholarship Scheme",
    shortDescription: "Financial assistance for higher education to meritorious students from economically weaker sections.",
    description: "The Prime Minister's National Scholarship Scheme provides financial assistance to meritorious students from economically weaker sections of society. The scheme covers tuition fees and provides a monthly stipend to students pursuing higher education in recognized institutions across the country.",
    category: "education",
    ministry: "Ministry of Education",
    eligibility: {
      minAge: 17,
      maxAge: 25,
      economicClass: ["BPL", "EWS", "LIG"],
      education: ["12th Pass", "Graduate"],
    },
    benefits: [
      "Annual scholarship of up to Rs. 75,000",
      "Monthly stipend of Rs. 3,000",
      "Book allowance of Rs. 5,000 per year",
      "One-time laptop grant of Rs. 25,000",
    ],
    steps: [
      {
        id: "step-1",
        title: "Check Eligibility",
        description: "Verify you meet all eligibility criteria before applying.",
        details: "Ensure your family income is below Rs. 8 lakh per annum, you have scored above 60% in your last qualifying examination, and you are enrolled or seeking enrollment in a recognized institution. You must be an Indian citizen and must not be receiving any other government scholarship.",
        documents: ["Aadhaar Card", "Income Certificate"],
        copies: 1,
        location: "Online - Official Portal",
        estimatedTime: "15 minutes",
        tips: ["Verify your Aadhaar is linked to your mobile number", "Keep digital copies of all documents ready"],
      },
      {
        id: "step-2",
        title: "Register Online",
        description: "Create an account on the National Scholarship Portal.",
        details: "Visit the National Scholarship Portal (scholarships.gov.in) and create a new account using your Aadhaar number and mobile number. You will receive an OTP for verification. Complete the registration by setting a strong password and filling in basic personal details.",
        documents: ["Aadhaar Card", "Mobile Number", "Email ID", "Passport-size Photograph"],
        copies: 1,
        location: "National Scholarship Portal (scholarships.gov.in)",
        estimatedTime: "20 minutes",
        tips: ["Use a personal email for future communications", "Save your login credentials securely"],
      },
      {
        id: "step-3",
        title: "Fill Application Form",
        description: "Complete the detailed application form with personal and academic details.",
        details: "Log in to your account and fill in the complete application form. This includes personal details, family information, academic records from the last 3 years, bank account details for direct benefit transfer, and the institution where you are enrolled or seeking admission.",
        documents: ["10th Marksheet", "12th Marksheet", "College Admission Letter", "Bank Passbook", "Caste Certificate (if applicable)"],
        copies: 1,
        location: "National Scholarship Portal (scholarships.gov.in)",
        estimatedTime: "45 minutes",
        tips: ["Double-check all academic details before submission", "Ensure bank account is in your name and is active"],
      },
      {
        id: "step-4",
        title: "Upload Documents",
        description: "Upload scanned copies of all required documents.",
        details: "Upload clear, legible scanned copies of all required documents. Each document should be in PDF or JPEG format with file size between 50KB and 500KB. Ensure all documents are recent (within the last 6 months for income and domicile certificates).",
        documents: ["Income Certificate", "Domicile Certificate", "Caste Certificate", "Bank Passbook First Page", "Passport-size Photo", "Signature"],
        copies: 1,
        location: "National Scholarship Portal (scholarships.gov.in)",
        estimatedTime: "30 minutes",
        tips: ["Keep file sizes between 50KB-500KB", "Use a good scanner or high-quality phone camera"],
      },
      {
        id: "step-5",
        title: "Institute Verification",
        description: "Your institution will verify and forward your application.",
        details: "After submission, your application goes to your institution's nodal officer for verification. The institute verifies your enrollment, academic records, and other details. This process typically takes 2-3 weeks. You can track the status on the portal.",
        documents: [],
        copies: 0,
        location: "Your Educational Institution",
        estimatedTime: "2-3 weeks",
        tips: ["Follow up with your institution's scholarship cell", "Keep the application reference number safe"],
      },
      {
        id: "step-6",
        title: "District/State Verification",
        description: "District and state authorities verify the application.",
        details: "Post institute verification, the application is forwarded to district and then state-level authorities for further verification of income, domicile, and other eligibility criteria. This stage involves cross-verification with government databases.",
        documents: [],
        copies: 0,
        location: "District/State Scholarship Office",
        estimatedTime: "3-4 weeks",
        tips: ["Check portal regularly for any queries or document requests", "Respond to any verification queries within 48 hours"],
      },
      {
        id: "step-7",
        title: "Scholarship Disbursement",
        description: "Scholarship amount is transferred to your bank account via DBT.",
        details: "Upon successful verification at all levels, the scholarship amount is disbursed directly to your bank account through Direct Benefit Transfer (DBT). The first installment typically covers the annual scholarship and first quarter stipend. Subsequent stipends are disbursed quarterly.",
        documents: [],
        copies: 0,
        location: "Direct Bank Transfer",
        estimatedTime: "4-6 weeks after final verification",
        tips: ["Ensure your bank account is DBT-enabled", "Keep your bank KYC updated"],
      },
    ],
    applicationDeadline: "November 30, 2026",
    websiteUrl: "https://scholarships.gov.in",
    helplineNumber: "1800-XXX-XXXX",
  },
  {
    id: "ayushman-bharat",
    title: "Ayushman Bharat - PMJAY",
    shortDescription: "Health insurance coverage of Rs. 5 lakh per family per year for secondary and tertiary hospitalizations.",
    description: "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PMJAY) is the world's largest health insurance scheme. It provides health insurance coverage of Rs. 5 lakh per family per year for secondary and tertiary care hospitalization to over 12 crore poor and vulnerable families.",
    category: "healthcare",
    ministry: "Ministry of Health & Family Welfare",
    eligibility: {
      economicClass: ["BPL", "EWS"],
    },
    benefits: [
      "Health coverage of Rs. 5 lakh per family per year",
      "Cashless treatment at empaneled hospitals",
      "Coverage for pre and post hospitalization expenses",
      "No restriction on family size or age",
    ],
    steps: [
      {
        id: "step-1",
        title: "Check Eligibility",
        description: "Verify if your family is listed in the SECC 2011 database.",
        details: "Your eligibility is determined based on the Socio-Economic Caste Census (SECC) 2011 data. Visit the official PMJAY website or call the helpline to check if your family is listed. You can also visit any Common Service Center (CSC) or empaneled hospital to verify your eligibility.",
        documents: ["Aadhaar Card", "Ration Card"],
        copies: 1,
        location: "PMJAY Website / CSC Center / Empaneled Hospital",
        estimatedTime: "10 minutes",
        tips: ["Check online at mera.pmjay.gov.in", "Your family should be in the SECC 2011 database"],
      },
      {
        id: "step-2",
        title: "Visit Empaneled Hospital or CSC",
        description: "Visit any Ayushman Bharat empaneled hospital or CSC to create your e-card.",
        details: "Visit the nearest empaneled hospital's Ayushman Mitra desk or a Common Service Center with your Aadhaar card and ration card. The Ayushman Mitra will verify your identity and eligibility, then generate your Ayushman Bharat e-card on the spot.",
        documents: ["Aadhaar Card", "Ration Card", "Any Government ID Proof"],
        copies: 2,
        location: "Nearest Empaneled Hospital / Common Service Center",
        estimatedTime: "30 minutes",
        tips: ["Carry both original and photocopies of documents", "All family members should be present for family e-card"],
      },
      {
        id: "step-3",
        title: "Get Your Ayushman Card",
        description: "Receive your Ayushman Bharat health card.",
        details: "After successful verification and eKYC, your Ayushman Bharat e-card will be generated. This card is linked to your Aadhaar and can be used at any empaneled hospital across India for cashless treatment. Save the digital copy on your phone as well.",
        documents: [],
        copies: 0,
        location: "Same location as Step 2",
        estimatedTime: "15 minutes",
        tips: ["Download the Ayushman Bharat app for digital card access", "Save the helpline number: 14555"],
      },
      {
        id: "step-4",
        title: "Avail Treatment",
        description: "Visit any empaneled hospital for cashless treatment when needed.",
        details: "When you need hospitalization, visit any Ayushman Bharat empaneled hospital. Show your Ayushman card at the Ayushman Mitra desk. The hospital will verify your identity, check your coverage, and provide cashless treatment. Pre-authorization is done electronically.",
        documents: ["Ayushman Bharat Card", "Aadhaar Card"],
        copies: 1,
        location: "Any Empaneled Hospital",
        estimatedTime: "As per treatment",
        tips: ["Find nearest empaneled hospitals on the PMJAY app", "For emergencies, hospitals cannot deny treatment"],
      },
    ],
    websiteUrl: "https://pmjay.gov.in",
    helplineNumber: "14555",
  },
  {
    id: "pmay-urban",
    title: "PM Awas Yojana - Urban",
    shortDescription: "Affordable housing for urban poor with interest subsidy on home loans.",
    description: "Pradhan Mantri Awas Yojana - Urban (PMAY-U) provides affordable housing for the urban poor. The scheme offers interest subsidy on home loans, making housing accessible to economically weaker sections, low-income groups, and middle-income groups.",
    category: "housing",
    ministry: "Ministry of Housing & Urban Affairs",
    eligibility: {
      minAge: 21,
      economicClass: ["EWS", "LIG", "MIG"],
    },
    benefits: [
      "Interest subsidy of up to 6.5% on home loans",
      "Subsidy for house construction or enhancement",
      "Beneficiary-led individual house construction support",
      "Affordable housing in partnership with private developers",
    ],
    steps: [
      {
        id: "step-1",
        title: "Check Eligibility",
        description: "Determine your income category and verify eligibility.",
        details: "PMAY-U categorizes beneficiaries as: EWS (income up to Rs. 3 lakh), LIG (Rs. 3-6 lakh), MIG-I (Rs. 6-12 lakh), or MIG-II (Rs. 12-18 lakh). You or your family should not own a pucca house anywhere in India. At least one female member should be a co-owner.",
        documents: ["Income Certificate", "Aadhaar Card"],
        copies: 1,
        location: "Online / Municipal Office",
        estimatedTime: "15 minutes",
        tips: ["Check eligibility at pmaymis.gov.in", "Family income means combined income of all earning members"],
      },
      {
        id: "step-2",
        title: "Apply Online or at CSC",
        description: "Submit your application through the official portal or CSC.",
        details: "Apply online at pmaymis.gov.in or visit a Common Service Center. Fill in the application form with personal details, income details, and property preferences. A nominal fee may be charged at CSC. After submission, you will receive an application number.",
        documents: ["Aadhaar Card", "Income Certificate", "Bank Account Details", "Address Proof", "Passport-size Photograph"],
        copies: 2,
        location: "PMAY-MIS Portal / Common Service Center",
        estimatedTime: "30-45 minutes",
        tips: ["Apply through CSC if you need assistance", "Keep a copy of the application form"],
      },
      {
        id: "step-3",
        title: "Document Verification",
        description: "Municipal body verifies your application and documents.",
        details: "The Urban Local Body (ULB) / Municipal Corporation will verify your application, conduct a physical survey if needed, and validate your documents. They will check if you already own a pucca house and verify your income category.",
        documents: ["Original Documents for Verification", "Property Documents (if applicable)"],
        copies: 2,
        location: "Municipal Corporation / ULB Office",
        estimatedTime: "4-6 weeks",
        tips: ["Cooperate with survey teams for faster processing", "Keep all original documents ready"],
      },
      {
        id: "step-4",
        title: "Loan Sanction & Subsidy",
        description: "Get home loan sanctioned and receive interest subsidy.",
        details: "After approval, approach any scheduled bank or housing finance company for a home loan. The interest subsidy will be credited upfront to your loan account, reducing your EMI burden. The subsidy amount depends on your income category.",
        documents: ["PMAY Approval Letter", "Property Documents", "Bank Loan Application", "Income Proof"],
        copies: 3,
        location: "Bank / Housing Finance Company",
        estimatedTime: "2-4 weeks",
        tips: ["Compare home loan rates across banks", "The subsidy is credited directly to your loan account"],
      },
      {
        id: "step-5",
        title: "Construction & Possession",
        description: "Begin construction or receive possession of the house.",
        details: "For beneficiary-led construction, start building as per approved plan. For affordable housing projects, the developer will provide possession. Construction progress is monitored through geo-tagged photographs and inspections.",
        documents: [],
        copies: 0,
        location: "Construction Site",
        estimatedTime: "12-18 months",
        tips: ["Upload construction progress photos on the PMAY app", "Ensure construction follows approved building plan"],
      },
    ],
    websiteUrl: "https://pmaymis.gov.in",
    helplineNumber: "1800-11-3377",
  },
  {
    id: "pm-kisan",
    title: "PM-KISAN Samman Nidhi",
    shortDescription: "Direct income support of Rs. 6,000 per year to farmer families across the country.",
    description: "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) is a central sector scheme that provides income support of Rs. 6,000 per year to all landholding farmer families across the country in three equal installments of Rs. 2,000 each.",
    category: "agriculture",
    ministry: "Ministry of Agriculture & Farmers Welfare",
    eligibility: {
      minAge: 18,
      occupation: ["Farmer"],
    },
    benefits: [
      "Rs. 6,000 per year in three installments",
      "Direct benefit transfer to bank account",
      "No restriction on land holding size",
      "Both small and marginal farmers eligible",
    ],
    steps: [
      {
        id: "step-1",
        title: "Registration at CSC/Portal",
        description: "Register yourself on the PM-KISAN portal or through a CSC.",
        details: "Visit pmkisan.gov.in and click on 'New Farmer Registration'. Enter your Aadhaar number, select your state, and enter the captcha. If registered, your status will show. If not, proceed to fill the registration form with land and bank details.",
        documents: ["Aadhaar Card", "Land Ownership Documents", "Bank Passbook"],
        copies: 2,
        location: "PM-KISAN Portal / CSC / Lekhpal Office",
        estimatedTime: "20 minutes",
        tips: ["Ensure Aadhaar is linked to bank account", "Land records should be updated"],
      },
      {
        id: "step-2",
        title: "Land Record Verification",
        description: "State government verifies your land ownership records.",
        details: "After registration, the state government verifies your land ownership records through their revenue department. This involves cross-checking with the land records database. The Patwari/Lekhpal may visit for physical verification.",
        documents: ["Khatauni / Land Records", "Identity Proof"],
        copies: 1,
        location: "Revenue Department / Tehsil Office",
        estimatedTime: "2-4 weeks",
        tips: ["Keep land records updated and mutation done", "Follow up at the local revenue office"],
      },
      {
        id: "step-3",
        title: "Receive Benefits",
        description: "Receive Rs. 2,000 every four months directly in your bank account.",
        details: "Upon successful verification, you will start receiving Rs. 2,000 every four months (April-July, August-November, December-March) directly in your Aadhaar-linked bank account through DBT.",
        documents: [],
        copies: 0,
        location: "Direct Bank Transfer",
        estimatedTime: "Benefits start from next installment cycle",
        tips: ["Check payment status at pmkisan.gov.in", "Update bank details if you change your account"],
      },
    ],
    websiteUrl: "https://pmkisan.gov.in",
    helplineNumber: "1800-115-526",
  },
  {
    id: "skill-india",
    title: "Skill India - PMKVY",
    shortDescription: "Free skill training and certification for youth to improve employability.",
    description: "Pradhan Mantri Kaushal Vikas Yojana (PMKVY) under Skill India Mission provides free skill training and certification to Indian youth. The scheme aims to enable youth to take up industry-relevant skill training that helps them secure a better livelihood.",
    category: "employment",
    ministry: "Ministry of Skill Development & Entrepreneurship",
    eligibility: {
      minAge: 15,
      maxAge: 45,
      education: ["8th Pass", "10th Pass", "12th Pass", "Graduate"],
    },
    benefits: [
      "Free skill training in 300+ job roles",
      "Government-recognized certification",
      "Placement assistance post training",
      "Training allowance for certain courses",
    ],
    steps: [
      {
        id: "step-1",
        title: "Find a Training Center",
        description: "Locate a PMKVY-affiliated training center near you.",
        details: "Visit the Skill India portal (skillindia.nsdcindia.org) to find affiliated training centers in your area. You can search by location, sector, or job role. Each center offers specific courses with defined durations.",
        documents: ["Aadhaar Card", "Education Certificate"],
        copies: 2,
        location: "Skill India Portal / District Skill Office",
        estimatedTime: "15 minutes",
        tips: ["Choose a center close to your residence", "Check the center's rating and placement record"],
      },
      {
        id: "step-2",
        title: "Enroll in Training",
        description: "Visit the center and enroll in your chosen skill course.",
        details: "Visit the selected training center with required documents. The center will assess your existing skills and recommend an appropriate course. Complete the enrollment formalities including biometric registration and Aadhaar verification.",
        documents: ["Aadhaar Card", "Education Certificates", "Passport-size Photographs", "Bank Account Details"],
        copies: 2,
        location: "Selected Training Center",
        estimatedTime: "1 hour",
        tips: ["Attend the orientation session", "Understand the course curriculum and duration"],
      },
      {
        id: "step-3",
        title: "Complete Training",
        description: "Attend all sessions and complete the full training course.",
        details: "Attend the training program regularly. Courses typically range from 150-300 hours spread over 2-6 months. The training includes both theoretical knowledge and practical hands-on experience. Regular attendance is mandatory.",
        documents: [],
        copies: 0,
        location: "Training Center",
        estimatedTime: "2-6 months",
        tips: ["Maintain minimum 80% attendance", "Practice regularly during and after sessions"],
      },
      {
        id: "step-4",
        title: "Assessment & Certification",
        description: "Appear for the assessment exam and receive your certificate.",
        details: "After completing the training, you'll appear for an assessment conducted by an independent assessment body. The assessment tests both theoretical knowledge and practical skills. Upon passing, you receive an NSQF-aligned government certificate.",
        documents: ["Training Completion Certificate", "Aadhaar Card"],
        copies: 1,
        location: "Assessment Center",
        estimatedTime: "1 day for assessment, 2-4 weeks for certificate",
        tips: ["Review all training materials before assessment", "Certificate is digitally verifiable"],
      },
      {
        id: "step-5",
        title: "Placement Support",
        description: "Get placement assistance and job referrals.",
        details: "Post certification, the training center and NSDC provide placement assistance. This includes job fairs, employer connections, and referrals. Many empaneled employers prefer PMKVY-certified candidates.",
        documents: ["PMKVY Certificate", "Resume"],
        copies: 3,
        location: "Training Center / Job Fairs",
        estimatedTime: "Ongoing support",
        tips: ["Update your profile on the Skill India portal", "Attend all placement drives"],
      },
    ],
    websiteUrl: "https://pmkvyofficial.org",
    helplineNumber: "1800-123-9626",
  },
  {
    id: "ujjwala-yojana",
    title: "PM Ujjwala Yojana",
    shortDescription: "Free LPG connections and subsidized refills for women from BPL households.",
    description: "Pradhan Mantri Ujjwala Yojana provides free LPG connections to women from Below Poverty Line (BPL) households. The scheme aims to safeguard the health of women and children by providing them with clean cooking fuel.",
    category: "women-child",
    ministry: "Ministry of Petroleum & Natural Gas",
    eligibility: {
      minAge: 18,
      economicClass: ["BPL"],
      gender: ["Female"],
    },
    benefits: [
      "Free LPG connection with security deposit waiver",
      "Free first refill and hot plate",
      "Subsidized LPG refills",
      "EMI facility for stove and first refill",
    ],
    steps: [
      {
        id: "step-1",
        title: "Visit LPG Distributor",
        description: "Visit your nearest LPG distributor with required documents.",
        details: "Identify your nearest LPG distributor (HP, Bharat, or Indane). Visit with your Aadhaar card, BPL ration card, and a passport-size photograph. The distributor will check if there's already an LPG connection in your household.",
        documents: ["Aadhaar Card", "BPL Ration Card", "Bank Account Passbook", "Passport-size Photograph"],
        copies: 2,
        location: "Nearest LPG Distributor",
        estimatedTime: "30 minutes",
        tips: ["No existing LPG connection should be in the household", "The connection must be in the woman's name"],
      },
      {
        id: "step-2",
        title: "Submit Application",
        description: "Fill and submit the Ujjwala application form.",
        details: "The distributor will provide the Ujjwala application form. Fill in your details, attach required documents, and submit. The distributor will verify your documents and process the application.",
        documents: ["Filled Application Form", "Self-declaration (if no address proof)"],
        copies: 1,
        location: "LPG Distributor",
        estimatedTime: "20 minutes",
        tips: ["Get a receipt for your application", "Provide correct mobile number for updates"],
      },
      {
        id: "step-3",
        title: "Receive LPG Connection",
        description: "Get your free LPG connection, cylinder, and stove.",
        details: "After verification, you will receive your LPG connection within 7-15 days. This includes the gas cylinder, pressure regulator, and if eligible, a free stove. The connection will be in the name of the adult woman of the household.",
        documents: ["Application Receipt", "Aadhaar Card"],
        copies: 1,
        location: "Home Delivery / LPG Distributor",
        estimatedTime: "7-15 days",
        tips: ["Ensure someone is home for delivery", "Check all equipment for safety before use"],
      },
    ],
    websiteUrl: "https://pmuy.gov.in",
    helplineNumber: "1800-266-6696",
  },
  {
    id: "old-age-pension",
    title: "National Old Age Pension Scheme",
    shortDescription: "Monthly pension of Rs. 200-500 for senior citizens from BPL families.",
    description: "The National Old Age Pension Scheme under the National Social Assistance Programme provides a monthly pension to destitute senior citizens aged 60 years and above who belong to Below Poverty Line (BPL) families.",
    category: "social-welfare",
    ministry: "Ministry of Rural Development",
    eligibility: {
      minAge: 60,
      economicClass: ["BPL", "EWS"],
    },
    benefits: [
      "Monthly pension of Rs. 200 (age 60-79)",
      "Monthly pension of Rs. 500 (age 80+)",
      "State government may add additional amount",
      "Direct benefit transfer to bank account",
    ],
    steps: [
      {
        id: "step-1",
        title: "Obtain Required Certificates",
        description: "Get age proof and BPL certificate from concerned authorities.",
        details: "You need a valid age proof (Aadhaar, voter ID, or birth certificate) and BPL certificate or income certificate. Visit your Gram Panchayat office (rural) or Municipal office (urban) for the BPL certificate.",
        documents: ["Aadhaar Card", "Age Proof", "BPL Certificate / Income Certificate", "Bank Passbook"],
        copies: 3,
        location: "Gram Panchayat / Municipal Office",
        estimatedTime: "1-2 weeks",
        tips: ["If you don't have age proof, a medical age certificate works", "Get BPL certificate from Block Development Officer"],
      },
      {
        id: "step-2",
        title: "Submit Application",
        description: "Apply at your Gram Panchayat, Block office, or District Social Welfare office.",
        details: "Submit the pension application form along with required documents at your Gram Panchayat (rural) or District Social Welfare office (urban). Many states also allow online applications through their respective portals.",
        documents: ["Application Form", "Aadhaar Card", "BPL Certificate", "Bank Passbook", "Passport-size Photographs"],
        copies: 2,
        location: "Gram Panchayat / Block Office / District Social Welfare Office",
        estimatedTime: "30 minutes",
        tips: ["Get an acknowledgment receipt", "Some states accept online applications"],
      },
      {
        id: "step-3",
        title: "Verification & Approval",
        description: "Application is verified by block and district authorities.",
        details: "The application is verified at the block level and then approved at the district level. A physical verification may be conducted. The approval process typically takes 1-3 months depending on the state.",
        documents: [],
        copies: 0,
        location: "Block / District Office",
        estimatedTime: "1-3 months",
        tips: ["Follow up at the block office periodically", "Keep the receipt number for tracking"],
      },
      {
        id: "step-4",
        title: "Receive Monthly Pension",
        description: "Start receiving pension in your bank account.",
        details: "Once approved, the pension is credited to your bank account monthly. The central government contributes Rs. 200/500 per month, and states may add their own contribution making the total pension higher.",
        documents: [],
        copies: 0,
        location: "Direct Bank Transfer",
        estimatedTime: "Monthly from approval date",
        tips: ["Keep bank account active with minimum transactions", "Report any issues to the District Social Welfare Office"],
      },
    ],
    websiteUrl: "https://nsap.nic.in",
    helplineNumber: "1800-111-555",
  },
  {
    id: "mudra-loan",
    title: "PM MUDRA Yojana",
    shortDescription: "Collateral-free loans up to Rs. 10 lakh for small and micro enterprises.",
    description: "Pradhan Mantri MUDRA Yojana provides collateral-free loans up to Rs. 10 lakh to non-corporate, non-farm small/micro enterprises. Loans are given under three categories: Shishu (up to Rs. 50,000), Kishore (Rs. 50,000 - Rs. 5 lakh), and Tarun (Rs. 5 lakh - Rs. 10 lakh).",
    category: "finance",
    ministry: "Ministry of Finance",
    eligibility: {
      minAge: 18,
      occupation: ["Self-Employed", "Entrepreneur"],
    },
    benefits: [
      "Collateral-free loans up to Rs. 10 lakh",
      "Low interest rates",
      "No processing fees for Shishu loans",
      "MUDRA Card for working capital management",
    ],
    steps: [
      {
        id: "step-1",
        title: "Prepare Business Plan",
        description: "Create a brief business plan or project report.",
        details: "Prepare a simple business plan outlining your business idea, expected income, market opportunity, and how you plan to use the loan. For Shishu loans, a detailed plan may not be required, but for Kishore and Tarun, banks may ask for a project report.",
        documents: ["Business Plan / Project Report", "Identity Proof", "Address Proof"],
        copies: 2,
        location: "Self-preparation / CA / Business Advisor",
        estimatedTime: "1-3 days",
        tips: ["Keep the plan simple and realistic", "Include revenue projections for 3 years"],
      },
      {
        id: "step-2",
        title: "Apply at Bank/NBFC",
        description: "Visit any bank, NBFC, or MFI to apply for MUDRA loan.",
        details: "Visit any commercial bank, Regional Rural Bank, Small Finance Bank, NBFC, or Microfinance Institution. Submit the MUDRA loan application form along with your business plan and required documents. You can also apply online through the Udyamimitra portal.",
        documents: ["MUDRA Application Form", "Identity Proof (Aadhaar/PAN)", "Address Proof", "Business Plan", "Photographs", "Category Certificate (SC/ST/OBC if applicable)"],
        copies: 2,
        location: "Any Bank / NBFC / MFI / Udyamimitra Portal",
        estimatedTime: "1-2 hours",
        tips: ["Compare offerings across multiple banks", "Government banks are generally more responsive"],
      },
      {
        id: "step-3",
        title: "Loan Processing",
        description: "Bank processes your application and conducts due diligence.",
        details: "The bank will process your application, verify your documents, and may conduct a field visit. They assess your creditworthiness, business viability, and repayment capacity. No collateral or guarantor is required for MUDRA loans.",
        documents: ["Additional Documents (if requested by bank)"],
        copies: 1,
        location: "Bank Branch",
        estimatedTime: "1-3 weeks",
        tips: ["Respond promptly to any bank queries", "Having a good CIBIL score helps"],
      },
      {
        id: "step-4",
        title: "Loan Disbursement",
        description: "Receive loan amount in your bank account.",
        details: "Upon approval, the loan amount is disbursed to your bank account. For Shishu loans, disbursement may be immediate. For larger loans, it may be phased. You'll also receive a MUDRA Card for managing working capital needs.",
        documents: ["Loan Agreement", "Post-dated Cheques / ECS Mandate"],
        copies: 1,
        location: "Bank Branch",
        estimatedTime: "3-7 days after approval",
        tips: ["Read the loan agreement carefully", "Understand the repayment schedule"],
      },
    ],
    websiteUrl: "https://mudra.org.in",
    helplineNumber: "1800-180-1111",
  },
  {
    id: "sukanya-samriddhi",
    title: "Sukanya Samriddhi Yojana",
    shortDescription: "Savings scheme for the girl child with high interest rates and tax benefits.",
    description: "Sukanya Samriddhi Yojana is a government-backed savings scheme for the girl child under the Beti Bachao Beti Padhao campaign. It offers one of the highest interest rates among small savings schemes with tax benefits under Section 80C.",
    category: "women-child",
    ministry: "Ministry of Finance",
    eligibility: {
      maxAge: 10,
      gender: ["Female"],
    },
    benefits: [
      "High interest rate (currently 8.2% p.a.)",
      "Tax-free returns under Section 80C",
      "Partial withdrawal allowed after age 18 for education",
      "Account matures at age 21",
    ],
    steps: [
      {
        id: "step-1",
        title: "Visit Bank or Post Office",
        description: "Open account at any authorized bank or post office.",
        details: "Visit any authorized bank (SBI, PNB, ICICI, etc.) or post office to open a Sukanya Samriddhi Account. The account must be opened by the parent or legal guardian of the girl child below 10 years of age. Maximum 2 accounts can be opened for 2 girl children.",
        documents: ["Girl Child's Birth Certificate", "Parent's/Guardian's ID Proof", "Parent's/Guardian's Address Proof", "Passport-size Photos of Child and Guardian"],
        copies: 2,
        location: "Authorized Bank / Post Office",
        estimatedTime: "30-45 minutes",
        tips: ["Post offices in rural areas also offer this scheme", "Minimum deposit is just Rs. 250"],
      },
      {
        id: "step-2",
        title: "Make Initial Deposit",
        description: "Deposit minimum Rs. 250 to open the account.",
        details: "Make the initial deposit (minimum Rs. 250, maximum Rs. 1.5 lakh per year). You can deposit through cash, cheque, demand draft, or online transfer. The account must be funded within the same financial year of opening.",
        documents: ["Deposit Slip", "Cash/Cheque/DD"],
        copies: 1,
        location: "Bank / Post Office",
        estimatedTime: "15 minutes",
        tips: ["Regular deposits build a good corpus", "Set up standing instructions for monthly deposits"],
      },
      {
        id: "step-3",
        title: "Continue Annual Deposits",
        description: "Make deposits regularly for 15 years from account opening.",
        details: "Continue making deposits for 15 years from the date of account opening. The minimum annual deposit is Rs. 250 and maximum is Rs. 1.5 lakh. If minimum deposit is missed, a penalty of Rs. 50 applies. After 15 years, the account continues to earn interest until maturity.",
        documents: [],
        copies: 0,
        location: "Bank / Post Office / Online Banking",
        estimatedTime: "Annual process for 15 years",
        tips: ["Automate deposits for consistency", "Maximize deposits early for compound interest benefits"],
      },
      {
        id: "step-4",
        title: "Maturity & Withdrawal",
        description: "Account matures when the girl turns 21.",
        details: "The account matures 21 years from the date of opening. Partial withdrawal (up to 50% of balance) is allowed after the girl turns 18 for higher education. Full maturity amount is tax-free and can be withdrawn by presenting the passbook and withdrawal form.",
        documents: ["Passbook", "Withdrawal Form", "Identity Proof of the Girl", "Educational Documents (for partial withdrawal)"],
        copies: 1,
        location: "Bank / Post Office where account is held",
        estimatedTime: "1-2 weeks for processing",
        tips: ["Plan partial withdrawal timing with college admission", "Full maturity amount is completely tax-free"],
      },
    ],
    websiteUrl: "https://www.nsiindia.gov.in",
    helplineNumber: "1800-267-6868",
  },
  {
    id: "crop-insurance",
    title: "PM Fasal Bima Yojana",
    shortDescription: "Crop insurance scheme protecting farmers against natural calamities and crop losses.",
    description: "Pradhan Mantri Fasal Bima Yojana provides comprehensive crop insurance against non-preventable natural risks from pre-sowing to post-harvest. Farmers pay minimal premium while the government subsidizes the rest.",
    category: "agriculture",
    ministry: "Ministry of Agriculture & Farmers Welfare",
    eligibility: {
      minAge: 18,
      occupation: ["Farmer"],
    },
    benefits: [
      "Crop insurance at very low premium (1.5-5%)",
      "Coverage against all natural calamities",
      "Post-harvest loss coverage for 14 days",
      "Quick claim settlement through technology",
    ],
    steps: [
      {
        id: "step-1",
        title: "Register Before Sowing",
        description: "Register for crop insurance before the sowing season deadline.",
        details: "Registration must be done before the cut-off date of the sowing season. For Kharif, apply by July 31; for Rabi, by December 31. Registration can be done through CSC, bank, or the PMFBY portal/app.",
        documents: ["Aadhaar Card", "Land Records (Khatauni)", "Bank Passbook", "Sowing Declaration"],
        copies: 2,
        location: "CSC / Bank / PMFBY Portal",
        estimatedTime: "30 minutes",
        tips: ["Register well before the deadline", "Insure all your crops for complete protection"],
      },
      {
        id: "step-2",
        title: "Pay Premium",
        description: "Pay the farmer's share of premium (1.5-5% of sum insured).",
        details: "The farmer's premium is very low: 2% for Kharif crops, 1.5% for Rabi crops, and 5% for horticulture/commercial crops. For loanee farmers, premium is auto-debited. Non-loanee farmers pay at the bank or CSC.",
        documents: ["Premium Payment Receipt"],
        copies: 1,
        location: "Bank / CSC / Online",
        estimatedTime: "15 minutes",
        tips: ["Premium is deducted from crop loan for loanee farmers", "Keep the insurance policy document safe"],
      },
      {
        id: "step-3",
        title: "Report Crop Loss (if any)",
        description: "Report crop damage within 72 hours of calamity.",
        details: "In case of crop loss due to natural calamity, report within 72 hours through the PMFBY app, toll-free number, or at the insurance company's local office. Provide details of the crop, area affected, and nature of damage.",
        documents: ["Crop Loss Report", "Photographs of Damage", "Insurance Policy Number"],
        copies: 1,
        location: "PMFBY App / Toll-free Number / Insurance Office",
        estimatedTime: "30 minutes",
        tips: ["Report immediately - don't wait", "Take date-stamped photos of damage"],
      },
      {
        id: "step-4",
        title: "Claim Assessment & Settlement",
        description: "Insurance company assesses damage and settles the claim.",
        details: "After reporting, the insurance company sends an assessor who evaluates the damage using technology (satellite imagery, drones, ground surveys). Claims are settled based on area-approach for widespread calamities or individual assessment for localized events.",
        documents: [],
        copies: 0,
        location: "Field / Insurance Office",
        estimatedTime: "2-8 weeks",
        tips: ["Cooperate with the assessment team", "Claim amount is deposited directly to bank account"],
      },
    ],
    websiteUrl: "https://pmfby.gov.in",
    helplineNumber: "1800-200-7710",
  },
]

export function getSchemesByCategory(categoryId: string): Scheme[] {
  return schemes.filter((s) => s.category === categoryId)
}

export function getSchemeById(id: string): Scheme | undefined {
  return schemes.find((s) => s.id === id)
}

export function searchSchemes(query: string): Scheme[] {
  const q = query.toLowerCase()
  return schemes.filter(
    (s) =>
      s.title.toLowerCase().includes(q) ||
      s.shortDescription.toLowerCase().includes(q) ||
      s.category.toLowerCase().includes(q) ||
      s.ministry.toLowerCase().includes(q)
  )
}

export function getEligibleSchemes(profile: {
  age?: number
  economicClass?: string
  gender?: string
  education?: string
  occupation?: string
}): Scheme[] {
  return schemes.filter((scheme) => {
    const e = scheme.eligibility
    if (profile.age !== undefined) {
      if (e.minAge && profile.age < e.minAge) return false
      if (e.maxAge && profile.age > e.maxAge) return false
    }
    if (profile.economicClass && e.economicClass && !e.economicClass.includes(profile.economicClass)) return false
    if (profile.gender && e.gender && !e.gender.includes(profile.gender)) return false
    if (profile.education && e.education && !e.education.includes(profile.education)) return false
    if (profile.occupation && e.occupation && !e.occupation.includes(profile.occupation)) return false
    return true
  })
}
