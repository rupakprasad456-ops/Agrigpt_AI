# Try to import google.generativeai, but make it optional for testing
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-generativeai not available. Some features will be limited.")

from typing import List, Dict, Any, Optional
import re

class AgentError(Exception):
    pass

# Pests and Diseases Knowledge Base
PESTS_KNOWLEDGE_BASE = {
    "rice": {
        "pests": {
            "stem borer": {
                "scientific_name": "Scirpophaga incertulas",
                "symptoms": "Causes 'dead heart' in vegetative stage and 'white ear' at heading. Larvae bore into stems.",
                "control": "carbofuran 3G @ 25 kg/ha, light traps, release of Trichogramma parasitoids."
            },
            "brown planthopper": {
                "scientific_name": "Nilaparvata lugens",
                "symptoms": "Sucks phloem sap causing 'hopper burn' — circular patches of dried plants.",
                "control": "Avoid excessive nitrogen, buprofezin 25 SC @ 1 ml/L, preserve natural enemies."
            },
            "gall midge": {
                "scientific_name": "Orseolia oryzae",
                "symptoms": "Converts tillers into tubular galls called 'silver shoots'.",
                "control": "carbofuran 3G @ 25 kg/ha during tillering; resistant varieties Jaya, Vikram."
            },
            "leaf folder": {
                "scientific_name": "Cnaphalocrocis medinalis",
                "symptoms": "Folds leaves longitudinally and feeds inside.",
                "control": "chlorpyrifos 20 EC @ 2 ml/L."
            }
        },
        "diseases": {
            "blast": {
                "scientific_name": "Magnaporthe oryzae",
                "symptoms": "Diamond-shaped lesions with grey centers on leaves and neck.",
                "control": "tricyclazole 75 WP @ 0.6 g/L, use resistant varieties."
            },
            "bacterial leaf blight": {
                "scientific_name": "Xanthomonas oryzae",
                "symptoms": "Water-soaked to yellow lesions along leaf margins.",
                "control": "copper oxychloride 50 WP @ 3 g/L, avoid flood irrigation."
            },
            "sheath blight": {
                "scientific_name": "Rhizoctonia solani",
                "symptoms": "Oval lesions on sheath with whitish center and brown border.",
                "control": "hexaconazole 5 EC @ 2 ml/L."
            },
            "brown spot": {
                "scientific_name": "Helminthosporium oryzae",
                "symptoms": "Circular to oval brown spots on leaves.",
                "control": "mancozeb 75 WP @ 2.5 g/L, balanced fertilization."
            }
        }
    },
    "wheat": {
        "pests": {
            "aphids": {
                "scientific_name": "Sitobion avenae",
                "symptoms": "Cluster on leaves and heads, cause yellowing and sooty mold.",
                "control": "imidacloprid 17.8 SL @ 0.5 ml/L."
            },
            "termites": {
                "scientific_name": "Odontotermes spp.",
                "symptoms": "Feed on roots causing wilting.",
                "control": "chlorpyrifos 20 EC @ 4 L/ha in irrigation water."
            }
        },
        "diseases": {
            "yellow rust": {
                "scientific_name": "Puccinia striiformis",
                "symptoms": "Yellow stripes of pustules on leaves.",
                "control": "propiconazole 25 EC @ 1 ml/L at first appearance."
            },
            "brown rust": {
                "scientific_name": "Puccinia recondita",
                "symptoms": "Orange-brown pustules scattered on leaves.",
                "control": "mancozeb 75 WP @ 2.5 g/L."
            },
            "loose smut": {
                "scientific_name": "Ustilago tritici",
                "symptoms": "Entire ear replaced by black smut mass.",
                "control": "seed treatment with carboxin 75 WP @ 2 g/kg seed."
            },
            "karnal bunt": {
                "scientific_name": "Tilletia indica",
                "symptoms": "Partial conversion of grain to black powder.",
                "control": "seed treatment with thiram 75 WP @ 2.5 g/kg."
            }
        }
    },
    "tomato": {
        "pests": {
            "fruit borer": {
                "scientific_name": "Helicoverpa armigera",
                "symptoms": "Larvae bore into fruits leaving circular holes with frass.",
                "control": "spinosad 45 SC @ 0.3 ml/L, pheromone traps."
            },
            "whitefly": {
                "scientific_name": "Bemisia tabaci",
                "symptoms": "Transmits leaf curl virus; adults and nymphs suck sap from underside of leaves.",
                "control": "imidacloprid 17.8 SL @ 0.5 ml/L, yellow sticky traps."
            },
            "leaf miner": {
                "scientific_name": "Liriomyza trifolii",
                "symptoms": "Serpentine mines on leaves.",
                "control": "abamectin 1.9 EC @ 1 ml/L."
            }
        },
        "diseases": {
            "early blight": {
                "scientific_name": "Alternaria solani",
                "symptoms": "Dark brown spots with concentric rings (target board appearance) on older leaves.",
                "control": "mancozeb 75 WP @ 2.5 g/L every 7–10 days."
            },
            "late blight": {
                "scientific_name": "Phytophthora infestans",
                "symptoms": "Irregular water-soaked lesions turning brown on leaves and fruits.",
                "control": "metalaxyl + mancozeb @ 2.5 g/L, avoid overhead irrigation."
            },
            "leaf curl virus": {
                "scientific_name": "TYLCV",
                "symptoms": "Upward curling, yellowing, and stunting of leaves. Transmitted by whitefly.",
                "control": "vector control, resistant varieties, remove infected plants."
            },
            "fusarium wilt": {
                "scientific_name": "Fusarium oxysporum",
                "symptoms": "Yellowing from lower leaves upward, vascular browning.",
                "control": "carbendazim soil treatment, grafted plants, crop rotation."
            }
        }
    },
    "cotton": {
        "pests": {
            "pink bollworm": {
                "scientific_name": "Pectinophora gossypiella",
                "symptoms": "Larvae bore into bolls; 'rosette flowers' are a sign of infestation.",
                "control": "pheromone traps @ 5/ha, spinosad 45 SC @ 0.3 ml/L, Bt cotton varieties."
            },
            "american bollworm": {
                "scientific_name": "Helicoverpa armigera",
                "symptoms": "Larvae feed on squares, flowers, and bolls.",
                "control": "indoxacarb 14.5 SC @ 1 ml/L, HaNPV @ 250 LE/ha."
            },
            "sucking pests": {
                "scientific_name": "Aphids, Jassids, Thrips, Whitefly",
                "symptoms": "Cause leaf curling, yellowing, and honeydew deposits.",
                "control": "thiamethoxam 25 WG @ 0.3 g/L."
            },
            "mealy bug": {
                "scientific_name": "Phenacoccus solenopsis",
                "symptoms": "White cottony masses on stems; wilting and drying of plants.",
                "control": "profenofos 50 EC @ 2 ml/L."
            }
        },
        "diseases": {
            "cotton leaf curl disease": {
                "scientific_name": "CLCuD",
                "symptoms": "Upward or downward curling of leaves, thickening of veins, enations. Spread by whitefly.",
                "control": "vector control, remove infected plants, tolerant varieties."
            },
            "bacterial blight": {
                "scientific_name": "Xanthomonas axonopodis",
                "symptoms": "Angular water-soaked spots on cotyledons and leaves.",
                "control": "streptocycline seed treatment, copper oxychloride 50 WP @ 3 g/L."
            }
        }
    },
    "maize": {
        "pests": {
            "fall armyworm": {
                "scientific_name": "Spodoptera frugiperda",
                "symptoms": "Feeds on whorl leaves leaving ragged holes and frass.",
                "control": "chlorpyrifos 20 EC @ 2 ml/L in whorl, Bt-based biopesticides."
            },
            "stem borer": {
                "scientific_name": "Chilo partellus",
                "symptoms": "Dead heart at vegetative stage; tunnels in stem.",
                "control": "carbofuran 3G @ 20 kg/ha in whorl."
            }
        },
        "diseases": {
            "turcicum leaf blight": {
                "scientific_name": "Exserohilum turcicum",
                "symptoms": "Long elliptical grey-green to tan lesions.",
                "control": "mancozeb 75 WP @ 2.5 g/L, resistant hybrids."
            },
            "maydis leaf blight": {
                "scientific_name": "Helminthosporium maydis",
                "symptoms": "Yellowish or tan lesions parallel to leaf margins.",
                "control": "zineb 75 WP @ 2 g/L."
            }
        }
    }
}

# Government Schemes Knowledge Base
SCHEMES_KNOWLEDGE_BASE = {
    "pm-kisan": {
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "benefit": "Rs 6,000 per year paid in 3 instalments of Rs 2,000 directly to farmer's bank account.",
        "eligibility": "All small and marginal landholding farmer families across India.",
        "exclusions": "Income tax payers, institutional land holders, government employees, constitutional post holders.",
        "how_to_apply": "Visit pmkisan.gov.in or nearest Common Service Centre (CSC). Submit Aadhaar + land records + bank account.",
        "helpline": "155261 / 011-24300606",
        "portal": "pmkisan.gov.in"
    },
    "pmfb": {
        "full_name": "PM Fasal Bima Yojana (PMFBY)",
        "benefit": "Covers crop loss due to natural calamities, pests, diseases, post-harvest losses.",
        "farmer_premium": "Kharif crops — 2% of sum insured; Rabi crops — 1.5%; Commercial/Horticulture — 5%.",
        "how_to_apply": "Through bank (automatic if crop loan taken), CSC, or insurance company before sowing cut-off date.",
        "helpline": "14447 / 1800-200-7710"
    },
    "kcc": {
        "full_name": "Kisan Credit Card (KCC)",
        "purpose": "Short-term credit for crop cultivation, post-harvest expenses, and allied activities (fisheries, animal husbandry).",
        "credit_limit": "Typically Rs 1.60 lakh without collateral, based on land holding, crop cultivated, and scale of finance.",
        "interest_rate": "7% per annum (effective 4% with interest subvention if repaid on time).",
        "validity": "5 years (renewable).",
        "how_to_apply": "Visit nearest bank branch — all nationalised banks, RRBs, cooperative banks.",
        "documents": "Aadhaar card, land ownership/lease documents, passport photo, bank account details."
    },
    "soil health card": {
        "purpose": "Provides farmers a card with details of soil nutrient status and crop-wise fertilizer recommendations.",
        "benefit": "Helps reduce input costs and improve yields through correct fertilizer application.",
        "frequency": "Issued every 2 years.",
        "how_to_get": "Contact local Agriculture Department, Krishi Vigyan Kendra (KVK), or apply at soilhealth.dac.gov.in.",
        "contains": "pH, EC, organic carbon, N/P/K, S, Zn, Fe, Mn, Cu, B levels and crop-wise fertilizer recommendations.",
        "portal": "soilhealth.dac.gov.in"
    },
    "pm kisan maan dhan yojana": {
        "full_name": "PM Kisan Maan Dhan Yojana",
        "benefit": "Rs 3,000 per month pension after age 60.",
        "eligibility": "Age 18–40 years, land holding up to 2 hectares, not covered under other pension schemes.",
        "contribution": "Rs 55 to Rs 200 per month (based on age of entry), matched equally by Central Government.",
        "how_to_apply": "Visit nearest CSC with Aadhaar and Kisan passbook/land records."
    },
    "nmsa": {
        "full_name": "National Mission for Sustainable Agriculture",
        "focus": "Soil health, water use efficiency, and climate-resilient farming.",
        "sub_scheme": "Paramparagat Krishi Vikas Yojana (PKVY): Rs 50,000/ha over 3 years for organic farming clusters.",
        "how_to_join": "Through State Agriculture Department or FPO (Farmer Producer Organization)."
    },
    "per drop more crop": {
        "full_name": "Per Drop More Crop (Micro Irrigation) Under Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)",
        "benefit": "55% subsidy on drip/sprinkler irrigation systems for small and marginal farmers; 45% for other farmers.",
        "purpose": "Reduce water usage and increase crop yield per drop of water.",
        "how_to_apply": "Through State Horticulture or Agriculture Department, or PMKSY portal."
    },
    "enam": {
        "full_name": "eNAM — National Agriculture Market",
        "purpose": "Online trading platform connecting farmers directly to buyers, traders, and exporters.",
        "benefit": "Transparent price discovery, better prices, no middlemen.",
        "how_to_register": "Contact nearest APMC (Mandi). Register with Aadhaar + bank account + land/produce details.",
        "portal": "enam.gov.in"
    },
    "rkvy": {
        "full_name": "Rashtriya Krishi Vikas Yojana",
        "purpose": "Overall agricultural development — infrastructure, equipment, technology.",
        "benefit": "Subsidies on farm machinery, cold storage, post-harvest infrastructure, and value addition units.",
        "how_to_access": "Apply through State Agriculture Department or District Agriculture Officer."
    },
    "agri infrastructure fund": {
        "purpose": "Finance for post-harvest management and agri-logistics infrastructure.",
        "benefit": "Loans up to Rs 2 crore with 3% interest subvention and credit guarantee.",
        "eligible_projects": "Cold storage, warehouses, sorting/grading units.",
        "eligibility": "Farmers, FPOs, SHGs, agri-startups.",
        "how_to_apply": "Through banks or agriinfra.dac.gov.in.",
        "portal": "agriinfra.dac.gov.in"
    }
}

class FarmerAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if GENAI_AVAILABLE:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_ai = True
        else:
            self.use_ai = False
            print("Warning: Running without AI capabilities. Using knowledge base only.")

    def _is_pest_question(self, question: str) -> bool:
        """Check if question is about pests, diseases, or treatments"""
        pest_keywords = [
            'pest', 'insect', 'disease', 'fungus', 'bacterial', 'viral', 'treatment',
            'control', 'symptom', 'damage', 'infestation', 'infection', 'bore',
            'mite', 'worm', 'beetle', 'fly', 'moth', 'caterpillar', 'aphid',
            'whitefly', 'jassid', 'thrip', 'mealybug', 'scale', 'rust', 'blight',
            'spot', 'rot', 'wilt', 'curl', 'yellow', 'brown', 'black', 'spot'
        ]

        question_lower = question.lower()
        return any(keyword in question_lower for keyword in pest_keywords)

    def _is_scheme_question(self, question: str) -> bool:
        """Check if question is about government schemes or financial help"""
        scheme_keywords = [
            'scheme', 'subsidy', 'government', 'pm-kisan', 'kisan', 'insurance',
            'credit', 'loan', 'pension', 'fund', 'grant', 'assistance', 'help',
            'financial', 'support', 'benefit', 'eligibility', 'apply', 'application',
            'pmfb', 'kcc', 'enam', 'soil health', 'infrastructure', 'market'
        ]

        question_lower = question.lower()
        return any(keyword in question_lower for keyword in scheme_keywords)

    def _search_pests_knowledge(self, query: str) -> Dict[str, Any]:
        """Search pests knowledge base for relevant information"""
        query_lower = query.lower()

        # Try to identify the crop mentioned
        crops = ['rice', 'wheat', 'tomato', 'cotton', 'maize']
        mentioned_crop = None
        for crop in crops:
            if crop in query_lower:
                mentioned_crop = crop
                break

        if not mentioned_crop:
            # Default to rice if no crop specified
            mentioned_crop = 'rice'

        crop_data = PESTS_KNOWLEDGE_BASE.get(mentioned_crop, {})

        # Search for specific pest or disease
        all_entries = {}
        all_entries.update(crop_data.get('pests', {}))
        all_entries.update(crop_data.get('diseases', {}))

        # Look for matches in the query
        for name, info in all_entries.items():
            if name.replace(' ', '') in query_lower.replace(' ', '') or \
               any(word in query_lower for word in name.split()):
                return {
                    'pest': f"{name.title()} ({info['scientific_name']})",
                    'details': f"Symptoms: {info['symptoms']}\nControl measures: {info['control']}"
                }

        # If no specific match, return general information for the crop
        pest_list = list(crop_data.get('pests', {}).keys())
        disease_list = list(crop_data.get('diseases', {}).keys())

        return {
            'pest': f"Common pests and diseases for {mentioned_crop.title()}",
            'details': f"Common pests: {', '.join(pest_list)}\nCommon diseases: {', '.join(disease_list)}\nPlease specify a particular pest or disease for detailed information."
        }

    def _search_schemes_knowledge(self, query: str) -> Dict[str, Any]:
        """Search government schemes knowledge base for relevant information"""
        query_lower = query.lower()

        # Look for specific scheme mentions
        for scheme_key, scheme_info in SCHEMES_KNOWLEDGE_BASE.items():
            if scheme_key.replace('-', ' ') in query_lower or \
               scheme_key in query_lower or \
               scheme_info.get('full_name', '').lower() in query_lower:
                details = []
                for key, value in scheme_info.items():
                    if key not in ['full_name']:
                        details.append(f"{key.replace('_', ' ').title()}: {value}")
                return {
                    'scheme': scheme_info.get('full_name', scheme_key.upper()),
                    'details': '\n'.join(details)
                }

        # If no specific scheme found, return general information
        scheme_list = [info.get('full_name', key.upper()) for key, info in SCHEMES_KNOWLEDGE_BASE.items()]

        return {
            'scheme': 'Available Government Schemes',
            'details': f"Common schemes include: {', '.join(scheme_list[:5])}...\nPlease specify a particular scheme for detailed information."
        }

    def simulate_pests(self, query: str) -> str:
        """Handle pest-related questions"""
        try:
            result = self._search_pests_knowledge(query)

            if self.use_ai:
                # Use Gemini to generate a natural response
                prompt = f"""
                Based on this pest/disease information:
                Pest: {result['pest']}
                Details: {result['details']}

                Generate a helpful, natural response for a farmer asking: "{query}"
                Include symptoms, control measures, and any additional practical advice.
                Keep it concise but informative.
                """

                response = self.model.generate_content(prompt)
                return response.text.strip()
            else:
                # Return structured information without AI enhancement
                return f"Information about {result['pest']}:\n\n{result['details']}"

        except Exception as e:
            return f"Error accessing pest information: {str(e)}"

    def government_schemes(self, query: str) -> str:
        """Handle government scheme questions"""
        try:
            result = self._search_schemes_knowledge(query)

            if self.use_ai:
                # Use Gemini to generate a natural response
                prompt = f"""
                Based on this government scheme information:
                Scheme: {result['scheme']}
                Details: {result['details']}

                Generate a helpful, natural response for a farmer asking: "{query}"
                Include eligibility, benefits, how to apply, and any important requirements.
                Keep it concise but informative.
                """

                response = self.model.generate_content(prompt)
                return response.text.strip()
            else:
                # Return structured information without AI enhancement
                return f"Information about {result['scheme']}:\n\n{result['details']}"

        except Exception as e:
            return f"Error accessing scheme information: {str(e)}"

    def chat(self, message: str, chat_id: str, phone_number: str) -> Dict[str, Any]:
        """Main chat endpoint that routes to appropriate tools"""
        message = message.strip()
        if not message:
            return {
                "response": "Please provide a question about farming.",
                "sources": []
            }

        # Check if question is agriculture-related
        agriculture_keywords = [
            'crop', 'farm', 'agriculture', 'plant', 'soil', 'water', 'fertilizer',
            'pest', 'disease', 'scheme', 'subsidy', 'government', 'kisan', 'insurance',
            'credit', 'loan', 'market', 'harvest', 'seed', 'yield', 'cultivation'
        ]

        message_lower = message.lower()
        is_agriculture_related = any(keyword in message_lower for keyword in agriculture_keywords)

        if not is_agriculture_related:
            return {
                "response": "I'm sorry, I can only help with agriculture-related questions about crop pests, diseases, and government schemes for farmers.",
                "sources": []
            }

        # Route to appropriate tool
        sources = []

        if self._is_pest_question(message):
            response = self.simulate_pests(message)
            sources = ["simulate_pests"]
        elif self._is_scheme_question(message):
            response = self.government_schemes(message)
            sources = ["government_schemes"]
        else:
            # Use Gemini for general agriculture questions or fallback to knowledge base
            try:
                if self.use_ai:
                    prompt = f"""
                    You are AgriGPT, an AI assistant for farmers. Answer this agriculture-related question helpfully and practically: "{message}"

                    Focus on practical farming advice. If you don't know something specific, suggest consulting local agricultural experts.
                    """

                    gemini_response = self.model.generate_content(prompt)
                    response = gemini_response.text.strip()
                    sources = []
                else:
                    # Fallback response without AI
                    response = "I can help with questions about crop pests and government schemes. Please ask about specific pests, diseases, or government programs for farmers."
                    sources = []
            except Exception as e:
                response = f"I apologize, but I encountered an error processing your question: {str(e)}"
                sources = []

        return {
            "response": response,
            "sources": sources
        }

    def get_pest_info(self, query: str) -> Dict[str, Any]:
        """Direct endpoint for pest information"""
        result = self._search_pests_knowledge(query)
        return result

    def get_scheme_info(self, query: str) -> Dict[str, Any]:
        """Direct endpoint for scheme information"""
        result = self._search_schemes_knowledge(query)
        return result
