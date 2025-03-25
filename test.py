import os
import json
from dotenv import load_dotenv
from utils.finance import FinancialDataFetcher

if __name__ == "__main__":
    import asyncio

    load_dotenv('.env')
    
    async def main():
        company_name = "Oracle"
        profile = FinancialDataFetcher(company_name)
        data = profile.get_financial_data(use_alphavantage=True)
        if data:
            print(f"Data: \n {json.dumps(data, indent=2)}")
    
    asyncio.run(main())