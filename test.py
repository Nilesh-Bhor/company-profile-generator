from CompanyProfile import CompanyProfile

if __name__ == "__main__":
    import asyncio
    
    async def main():
        company_profile = CompanyProfile("Oracle")
        data = company_profile.get_company_profile()
        print(data)
    
    asyncio.run(main())