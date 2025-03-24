import os
from googlesearch import search
from datetime import datetime

class BaseAgent:
    def __init__(self, model_name: str):
        self.schema = None
        self.model_name = model_name
        self._load_schema()

    def _load_schema(self):
        try:
            schema_file_path = os.path.join(os.path.dirname(__file__), 'schema.json')
            with open(schema_file_path, 'r') as schema_file:
                self.schema = schema_file.read()
        except Exception as e:
            print(f"Error loading schema: {e}")
    
    def generate_content(self, prompt: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_company_profile_prompt(self, company_name: str, company_website: str = None) -> str:
        current_year = datetime.now().year
        last_five_years = ', '.join(str(year) for year in range(current_year - 5, current_year))
        
        prompt = f"""
        **Task:**
        Gather comprehensive and up-to-date information about {company_name}. Ensure all data is accurate, cross-verified, and sourced from reliable sources.
        {"The company's website is " + company_website + "." if company_website else ""}

        ### **Company Overview:**  
        - **Logo:** Provide the company’s logo; if unavailable, search on sources like Brandsoftheworld, Clearbit, or the company’s website.  
        - **Business Description:** A brief overview of the company, including core operations.  
        - **Mission Statement**  
        - **Vision Statement**  
        - **Founded:** Year and location of establishment.  
        - **Industry:** Primary industry of operation.  
        - **Headquarters Location:** Current HQ address.  
        - **Website:** Official company website.  
        - **Number of Employees:** Total employees as of {current_year}.  
        - **Certifications:** List ISO certifications (if applicable).  
        - **Industries Served:** Key industries the company caters to.  

        ### **Geographic Presence:**  
        - **List of Locations:** Include manufacturing sites, sales offices, corporate headquarters, and other key operational locations.  

        ### **Financial Highlights (Last 5 Fiscal Years):**  
        Ensure data for the last five years ({last_five_years}) is correct and cross-verified. Include:  
        - **Revenue**  
        - **EBIT (Earnings Before Interest & Taxes)**  
        - **EBITDA (Earnings Before Interest, Taxes, Depreciation & Amortization)**  
        - **Growth Rate** (YoY or CAGR)  
        - **Gross Profit**  
        - **Net Profit**  
        - **Market Capitalization**  
        - **Total Assets**  
        - **Ownership Structure** (Public/Private, major stakeholders)  

        ### **Products & Services:**  
        - List the company’s major and most popular products/services. Provide a 1-2 line description for each.  

        ### **Leadership Team:**  
        - Provide names and titles of the top 5 executives (e.g., CEO, CFO, COO, CTO, etc.).  

        ### **Clients & Competitors:**  
        - **Major Clients:** Key customers or business partners.  
        - **Major Competitors:** Companies competing in the same industry/market.  

        ### **Company Strategies:**  
        - Outline the company’s strategic initiatives, goals, and future direction.  

        ### **Key Events (Last 3-5 Years):**  
        Include significant corporate events such as:  
        - **Mergers & Acquisitions (M&A)**  
        - **Demerger/Spin-offs**  
        - **Expansion (New markets, facilities, acquisitions, etc.)**  
        - **Exit from a country/business segment**  
        - **Recent Leadership Changes**  
        - **Other Important Developments**
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
