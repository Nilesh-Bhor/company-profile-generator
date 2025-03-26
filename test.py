import os
import json
from dotenv import load_dotenv
from CompanyProfile import CompanyProfile
from utils.finance import FinancialDataFetcher

if __name__ == "__main__":
    import asyncio

    load_dotenv('.env')
    
    async def main():
        company_name = "Oracle"
        
        profile = CompanyProfile(company_name=company_name) 
        # profile = FinancialDataFetcher(company_name=company_name)

        data = profile.get_company_profile(fetch_finance_data=True)
        # data = profile.get_financial_data(use_financial_modeling_prep=False)

        if data:
            print(f"Data: \n {json.dumps(data, indent=2)}")
    
    asyncio.run(main())