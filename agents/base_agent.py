import os
from googlesearch import search
from pydantic import ValidationError
from models.models import CompanyProfileResponse

class BaseAgent:
    def __init__(self, model_name: str):
        self.model_name = model_name
        
    def generate_content(self, prompt: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_company_profile_prompt(self, company_name: str, company_website: str = None) -> str:
        prompt = f"""
        Generate a *detailed and professional company profile* for "{company_name}".
        {"The company's website is {company_website}" if company_website else ""}
        Use multiple *reliable sources* (like Official Website, S&P Capital IQ, Yahoo Finance, Financial Databases, Crunchbase, News Article, Twitter etc.).
        Ensure all data is *accurate, up-to-date, and verified*.

        *Return the response in the following valid JSON format:*
        ```json
        {{
            "overview": {{
                "name": "{company_name}",
                "website": "{company_website if company_website else 'N/A'}",
                "description": "General overview of the company",
                "industry": "Primary industry sector",
                "founded": "Year founded and by whom",
                "employees": "Number of employees",
                "certifications": "ISO certifications",
                "location": "Headquarters location (City, Country)",
                "mission": "Company mission statement",
                "vision": "Company vision statement",
                "industry_served": "Industries served",
                "logo": "URL to the company's official logo (preferably from the official website or Clearbit)"
            }},
            "geographic_presence": [
                {{
                    "presence_type": "Presence type (e.g., Corporate Offices, Manufacturing & Supply Chain, Retail Stores, Data centers, And Many more, etc.)",
                    "locations": "Location(s) of presence"
                }}
            ],
            "financial_highlights": {{
                "overview": "Financial performance summary for the last 5 years",
                "metrics": [
                    {{
                        "year": "YYYY",
                        "ebit": "EBIT",
                        "ebitda": "EBITDA",
                        "revenue": "Annual revenue in USD",
                        "growth": "YoY growth",
                        "gross_profit": "Gross profit",
                        "net_profit": "Net profit",
                        "assets": "Total assets",
                        "market_cap": "Market capitalization",
                        "ownership": "Ownership structure"
                    }}
                ]
            }},
            "products_services": {{
                "description": "Summary of products",
                "items": [
                    {{
                        "name": "Product/Service name",
                        "category": "Category",
                        "description": "Detailed description of the product/service"
                    }}
                ]
            }},
            "leadership": {{
                "description": "Overview of the executive leadership team and key members (3-5 members)",
                "members": [
                    {{
                        "name": "Executive name",
                        "position": "Role (e.g., CEO, CFO)",
                        "bio": "Brief bio of the executive"
                    }}
                ]
            }},
            "clients_competitors": {{
                "major_clients": "List of major clients and what product/services the use with description",
                "major_competitors": "List of all major competitors with description"
            }},
            "strategic_priorities": {{
                "description": "Overview of the company's strategic priorities and goals",
                "objectives": [
                    {{
                        "name": "Objective name",
                        "description": "Objective description"
                    }}
                ]
            }},
            "key_events": {{
                "description": "Significant achievement or majorly events in last 3-5 years (eg. mergers, demergers, acquisitions, expansion, product launches, exit from a country/business segment, recent Change in leadership, any other important changes in the company etc.)",
                "events": [
                    {{
                        "date": "YYYY-MM-DD",
                        "description": "Description of event",
                        "source": "Source url of information"
                    }}
                ]
            }},
            "sources": [
                "List of sources used (URLs, reports, company filings)"
            ]
        }}
        ```
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
    
    def validate_response(self, response_text: str) -> CompanyProfileResponse:
        try:
            print(f"Response : {response_text}")
            response_data = CompanyProfileResponse.parse_raw(response_text.strip())
            return response_data
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
