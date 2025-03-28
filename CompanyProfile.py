import re
import os
import json
from datetime import datetime
from utils.utility import get_logo
from agents import AIAgent, AgentType
from core.settings import Settings
from utils.finance import FinancialDataFetcher

class CompanyProfile:
    def __init__(self, company_name, company_website=None, agent_type=None):
        self.agent_type = agent_type
        self.company_name = company_name
        self.company_website = company_website
        
        self._initialize_agent()
        
    def _initialize_agent(self):
        if self.agent_type is None:
            # Get agent type from environment variable
            agent_type_str = Settings.AGENT_TYPE
            self.agent_type = AgentType[agent_type_str] if agent_type_str in AgentType.__members__ else AgentType.GOOGLE_GEMINI
        
        # Configure the agent
        self.agent = AIAgent.get_agent(self.agent_type)
    
    def _get_prompt(self) -> str:
        current_year = datetime.now().year
        last_five_years = ', '.join(str(year) for year in range(current_year - 5, current_year))
        
        prompt = f"""
        **Task:**
        Gather comprehensive and up-to-date information about {self.company_name}. Ensure all data is accurate, cross-verified, and sourced from reliable sources.
        {"The company's website is " + self.company_website + "." if self.company_website else ""}

        ### **Company Overview:**  
        - **Logo:** Provide the company’s logo; if unavailable, search on sources like Brandsoftheworld, Clearbit, or the company’s website.  
        - **Business Description:** A brief overview of the company, including core operations.  
        - **Mission Statement**  
        - **Vision Statement**  
        - **Founded:** Year and location of establishment.  
        - **Industry:** Primary industry of operation.  
        - **Headquarters Location:** Current HQ address.  
        - **Website:** Official company website.  
        - **Number of Employees:** Total number employees as of {current_year}.  
        - **Certifications:** List ISO certifications (if applicable).  
        - **Industries Served:** Key industries the company caters to.  
        - **Stock Symbol:** Stock Symbol 

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
        - Provide names and titles of the top key 5 executives of company as of {current_year} (e.g. Chairman, Vice Chairman, CTO, CEO, CFO, COO, etc.). Exclude former executives.

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
    
    def _get_context(self) -> str:
        if self.agent_type == AgentType.OPENAI:
            return (
                """
                ### CONTEXT ###
                We aim to dynamically generate a comprehensive company profile with accurate, up-to-date information. The data should be sourced from reliable financial databases, official company communications, and credible industry sources to ensure accuracy and credibility.
                """
                """
                ### **Primary Data Sources:**  
                - **Financial Information:** Yahoo Finance, Crunchbase, S&P Capital IQ, Bloomberg, annual reports, and investor relations websites.  
                - **General Company Information:** Official company websites, press releases, news articles, and corporate filings.  
                - **Geographic and Local Data:** Government websites, local newspapers, industry-specific websites, and regulatory filings.  
                """
                """
                ### **Critical Requirements:**  
                - Ensure **accuracy and cross-verification** of financial data.  
                - Provide **source attribution** for key figures and statements.  
                - Use **latest available data** (e.g., last 5 fiscal years for financials).  
                - Include **key strategic initiatives and major corporate events** from the past 3-5 years.  
                - Cover **market position, competitive landscape, and client base** where relevant.  
                """
            )
        
        return (f""""
            ### CONTEXT ###
            We want to dynamically create a company profile with all needed information.
            **Yahoo Finance**, Crunchbase, S&P Capital IQ, and other financial databases are good sources for financial information.
            Company websites, press releases, and news articles are good sources for general information.
            Local newspapers, government websites, and industry-specific websites are good sources for local information.
            ***IMPORTANT - Please ensure all data is accurate, up-to-date, and include sources.*** \n
            
            Please provide a response in a structured JSON format that matches the following schema: {self.agent.schema}'
        """)
    
    def _convert_profile_metrics(self, profile_metrics):
        """
        Converts profile metrics to the same format as financial_data metrics.

        Args:
            profile_metrics (dict): The profile metrics to convert.

        Returns:
            dict: The converted metrics.
        """
        converted_metrics = {}
        for metric in profile_metrics:
            year = metric['year']
            converted_metrics[year] = {
                "revenue": metric['revenue'],
                "ebit": metric['ebit'],
                "ebitda": metric['ebitda'],
                "gross_profit": metric['gross_profit'],
                "net_profit": metric['net_profit'],
                "market_cap": metric['market_cap'],
                "total_assets": metric['total_assets'],
                "growth": metric['growth']
            }
        return converted_metrics

    def _get_logo(self, website, fallback_logo=None):
        domain = re.sub(r'^https?://(www\.)?', '', website).split('/')[0]
        logo_url = f"https://logo.clearbit.com/{domain}"
        
        logo = get_logo(logo_url)
        if logo:
            return logo_url

        return fallback_logo

    def get_company_profile(self, fetch_finance_data=True):
        try:
            prompt = self._get_prompt()
            context = self._get_context()
            response_text = self.agent.generate_content(context, prompt)

            if response_text:
                # Clean up the response by removing markdown code block markers
                json_response = response_text.strip()
                json_response = re.sub(r'^.*?```json\s*|\s*```$', '', json_response, flags=re.DOTALL)
                profile = json.loads(json_response)

                # Convert profile metrics to the same format as financial_data metrics
                profile_metrics = self._convert_profile_metrics(profile['financial_highlights']['metrics'])
                profile['financial_highlights']['metrics'] = profile_metrics

                # update logo if found in clearbit
                website = profile['overview']['website']
                logo = profile['overview']['logo']
                profile['overview']['logo'] = self._get_logo(website, logo)

                if fetch_finance_data:
                    # Fetch financial data if available
                    company_name = profile['overview']['name']
                    data_fetcher = FinancialDataFetcher(company_name=company_name)
                    financial_data = data_fetcher.get_financial_data(use_financial_modeling_prep=True)

                    if financial_data is not None and 'metrics' in financial_data:
                        metrics = data_fetcher.merge_metrics(financial_data['metrics'], profile_metrics)
                        profile['financial_highlights']['metrics'] = metrics

                        if 'fullTimeEmployees' in financial_data['info']:
                            profile['overview']['employees'] = financial_data['info']['fullTimeEmployees']
                        
                        if 'city' in financial_data['info'] and 'state' in financial_data['info'] and 'country' in financial_data['info']:
                            if financial_data['info']['city'] not in profile['overview']['location']:
                                profile['overview']['location'] = f"{financial_data['info']['city']}, {financial_data['info']['state']}, {financial_data['info']['country']}"
                        
                        if 'https://finance.yahoo.com' not in profile['sources']:
                            profile['sources'].append('https://finance.yahoo.com')
                
                return profile

            return None
        except Exception as e:
            print(f"An error occurred while generating company profile: {str(e)}")
            return None
            
