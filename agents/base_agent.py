import os
from googlesearch import search

class BaseAgent:
    def generate_content(self, prompt: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_company_profile_prompt(self, company_name: str, company_website: str = None) -> str:
        prompt = f"""
        Generate a detailed and professional company profile for {company_name}.
        {"The company's website is " + company_website + "." if company_website else ""}
        Provide the response in the following JSON structure:
        {{
            "company_overview": {{
                "name": "Company Name",
                "website": "Company Website",
                "description": "General overview of the company",
                "industry": "Primary industry",
                "location": "Headquarters location",
                "mission": "Company mission statement",
                "vision": "Company vision statement",
                "logo_url": "URL to the company's official logo from website or clearbit.com if not available"
            }},
            "products_and_services": {{
                "products": {{
                    "description": "Overview of offerings",
                    "items": [
                        {{
                            "name": "Product name",
                            "description": "Detailed description",
                            "features": ["feature1", "feature2"],
                            "benefits": ["benefit1", "benefit2"]
                        }}
                    ]
                }},
                "services": {{
                    "description": "Overview of services",
                    "items": [
                        {{
                            "name": "Service name",
                            "description": "Detailed description",
                            "features": ["feature1", "feature2"],
                            "benefits": ["benefit1", "benefit2"]
                        }}
                    ]   
                }}
            }},
            "management_team": {{
                "description": "Overview of leadership",
                "members": [
                    {{
                        "name": "Executive name",
                        "position": "Role",
                        "qualifications": "Key qualifications"
                    }}
                ]
            }},
            "milestones": [
                {{
                    "date": "Date of milestone",
                    "description": "Description of achievement"
                }}
            ],
            "financial_highlights": {{
                "overview": "Financial performance summary for the last 5 years",
                "metrics": [
                    {{
                        "year": "Year",
                        "revenue": "Annual revenue",
                        "growth": "YoY growth"
                    }}
                ]
            }},
            sources: ["list of the sources used"]
        }}
        
        Ensure all data is accurate, up-to-date and include sources.
        For the logo_url, provide a direct link to the company's official logo image.
        Format the response as valid JSON.
        """
        return prompt

    def search_company_info(self, company_name: str) -> str:
        additional_info = ""
        include_search = os.getenv('INCLUDE_GOOGLE_SEARCH', 'False').lower() == 'true'
        if include_search:
            query = f"{company_name} company profile"
            search_results = search(query, num_results=2, advanced=True)
            if search_results:
                company_search = None
                
                for search_result in list(search_results):
                    if search_result.title and search_result.url:
                        company_search = search_result
                        break

                if company_search:
                    additional_info = f"""
                    Here is an additional info about the company:
                    title: {company_search.title}
                    url: {company_search.url}
                    description: {company_search.description}
                    """
        return additional_info
