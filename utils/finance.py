import os
import yfinance as yf
import requests
from alpha_vantage.fundamentaldata import FundamentalData

class FinancialDataFetcher:
    def __init__(self, company_name):
        self.company_name = company_name
        self.company_symbol = self._get_company_symbol()

    def _get_company_symbol(self):
        """
        Fetches company symbol for a given company name.

        Returns:
            str: A company symbol.
        """
        try:
            search_api = "https://query2.finance.yahoo.com/v1/finance/search"
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            params = {"q": self.company_name, "quotes_count": 1, "news_count": 0}

            res = requests.get(url=search_api, params=params, headers={'User-Agent': user_agent})
            
            if res.status_code != 200:
                raise Exception(f"Failed to fetch company symbol for {self.company_name}")
            
            data = res.json()
            company_code = data['quotes'][0]['symbol']
            return company_code
        except Exception as e:
            print(f"Error fetching company symbol for {self.company_name}: {e}")
            return None

    def _get_financial_data_yfinance(self):
        """
        Fetches financial data for a given ticker symbol using yfinance.

        Returns:
            dict: A dictionary containing financial data.
        """
        try:
            stock = yf.Ticker(self.company_symbol)
            
            # Fetch financial statements
            financials = stock.financials.T.fillna(0)
            balance_sheet = stock.balance_sheet.T.fillna(0)
            info = stock.info
            
            # Extract required financial metrics for the last 5 years
            metrics = {}
            for year in range(5):
                year_str = str(financials.index[-(year+1)].year)
                metrics[year_str] = {
                    "revenue": financials.get('Total Revenue').iloc[-(year+1)] if 'Total Revenue' in financials else 0,
                    "ebit": financials.get('EBIT').iloc[-(year+1)] if 'EBIT' in financials else 0,
                    "ebitda": financials.get('EBITDA').iloc[-(year+1)] if 'EBITDA' in financials else 0,
                    "gross_profit": financials.get('Gross Profit').iloc[-(year+1)] if 'Gross Profit' in financials else 0,
                    "net_profit": financials.get('Net Income').iloc[-(year+1)] if 'Net Income' in financials else 0,
                    "market_cap": info.get('marketCap', 0),
                    "total_assets": balance_sheet.get('Total Assets').iloc[-(year+1)] if 'Total Assets' in balance_sheet else 0
                }
            
            return { "info": {}, "metrics": metrics }
        except Exception as e:
            print(f"Error fetching financial data for {self.company_name}: {e}")
            return None

    def _get_financial_data_alphavantage(self):
        """
        Fetches financial data for a given ticker symbol using Alpha Vantage.

        Returns:
            dict: A dictionary containing financial data.
        """
        try:
            API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
            fundamentel_data = FundamentalData(API_KEY)
            
            # Fetch financial statements
            income_statement, _ = fundamentel_data.get_income_statement_annual(self.company_symbol)
            balance_sheet, _ = fundamentel_data.get_balance_sheet_annual(self.company_symbol)
            
            # Extract required financial metrics for the last 5 years
            metrics = {}
            for year in range(6):
                year_str = income_statement['fiscalDateEnding'][year][:4]
                metrics[year_str] = {
                    "revenue": float(income_statement['totalRevenue'][year]) if 'totalRevenue' in income_statement else 0,
                    "ebit": float(income_statement['ebit'][year]) if 'ebit' in income_statement else 0,
                    "ebitda": float(income_statement['ebitda'][year]) if 'ebitda' in income_statement else 0,
                    "gross_profit": float(income_statement['grossProfit'][year]) if 'grossProfit' in income_statement else 0,
                    "net_profit": float(income_statement['netIncome'][year]) if 'netIncome' in income_statement else 0,
                    "market_cap": 0,  # Alpha Vantage does not provide market cap in fundamental data
                    "total_assets": float(balance_sheet['totalAssets'][year]) if 'totalAssets' in balance_sheet else 0
                }
            
            return { "info": {}, "metrics": metrics }
        except Exception as e:
            print(f"Error fetching financial data for {self.company_name} from Alpha Vantage: {e}")
            return None

    def _get_financial_data_fmp(self):
        """
        Fetches financial data for a given ticker symbol using Financial Modeling Prep API.

        Returns:
            dict: A dictionary containing financial data.
        """
        try:
            API_KEY = os.getenv('FMP_API_KEY', '')
            base_url = "https://financialmodelingprep.com/api/v3"

            # Fetch financial statements
            income_statement_url = f"{base_url}/income-statement/{self.company_symbol}?apikey={API_KEY}"            
            income_statement_res = requests.get(income_statement_url)
            
            if income_statement_res.status_code != 200:
                raise Exception(f"Failed to fetch financial data for {self.company_symbol} from FMP")
            
            income_statement = income_statement_res.json()
            
            # Extract required financial metrics for the last 5 years
            metrics = {}
            for year in range(5):
                year_str = income_statement[year]['date'][:4]
                metrics[year_str] = {
                    "revenue": income_statement[year].get('revenue', 0),
                    "ebit": income_statement[year].get('ebit', 0),
                    "ebitda": income_statement[year].get('ebitda', 0),
                    "gross_profit": income_statement[year].get('grossProfit', 0),
                    "net_profit": income_statement[year].get('netIncome', 0),
                    "market_cap": 0,  # FMP does not provide market cap in fundamental data
                    "total_assets": 0 # use balance-sheet-statement api
                }
            
            return { "info": {}, "metrics": metrics }
        except Exception as e:
            print(f"Error fetching financial data for {self.company_name} from FMP: {e}")
            return None
        
    def _format_metric_value(self, value):
        """
        Converts a given metric value to a human-readable format.

        Returns:
            str: A human-readable metric value.
        """
        if value >= 1e6:
            return f"{value / 1e9:.2f}B"
        
        return f"{value / 1e6:.2f}M"
        
    def _update_metrics_value(self, metrics_data):
        metrics={}
        for year in sorted(set(metrics_data.keys())):
            prev_year = str(int(year) - 1)
            year_metric = metrics_data[year]
            revenue = year_metric.get("revenue", 0)
            
            metrics[year] = {
                "t_revenue": revenue,
                "revenue": self._format_metric_value(revenue),
                "ebit": self._format_metric_value(year_metric.get("ebit", 0)),
                "ebitda": self._format_metric_value(year_metric.get("ebitda", 0)),
                "gross_profit": self._format_metric_value(year_metric.get("gross_profit", 0)),
                "net_profit": self._format_metric_value(year_metric.get("net_profit", 0)),
                "market_cap": self._format_metric_value(year_metric.get("market_cap", 0)),
                "total_assets": self._format_metric_value(year_metric.get("total_assets", 0))
            }

            if prev_year in metrics:
                prev_revenue = metrics[prev_year]["t_revenue"]
                metrics[year]["growth"] = f"{((revenue - prev_revenue) / prev_revenue) * 100:.2f}%" if prev_revenue != 0 else "0%"

        return metrics
    
    def merge_metrics(self, yfinance_metrics, other_metrics):
        metrics = {}
        years = sorted(set(yfinance_metrics.keys()).union(set(other_metrics.keys())))

        for year in years:
            yfinance_year = yfinance_metrics.get(year, {})
            other_finance_year = other_metrics.get(year, {})

            metrics[year] = {
                "growth": yfinance_year.get("growth", "0%") if yfinance_year.get("growth", "0%") != "0%" else other_finance_year.get("growth", "0%")
            }
            for key in ["revenue", "ebit", "ebitda", "gross_profit", "net_profit", "market_cap", "total_assets"]:
                yfinance_value = yfinance_year.get(key, 0)
                if isinstance(yfinance_value, str) and (yfinance_value.endswith('M') or yfinance_value.endswith('B')):
                    metrics[year][key] = yfinance_value if float(yfinance_value[:-1]) > 0 else other_finance_year.get(key, 0)
                else:
                     metrics[year][key] = yfinance_value or other_finance_year.get(key, 0)

        return metrics
        
    def get_financial_data(self, use_alphavantage=False, use_financial_modeling_prep=False):
        """
        Fetches financial data from yfinance if use_alphavantage set to False,
        otherwise fetches financial data from both yfinance and Alpha Vantage and merges them.

        Returns:
            dict: A dictionary containing financial data.
        """
        if not self.company_symbol:
            return None

        yfinance_data = self._get_financial_data_yfinance()
        if yfinance_data is None:
            return None
        
        financial_data = {
            "metrics": {},
            "info": yfinance_data.get("info", {}),
        }

        if use_alphavantage:
            data_alphavantage = self._get_financial_data_alphavantage()
            if data_alphavantage and yfinance_data:
                metrics = self.merge_metrics(yfinance_data["metrics"], data_alphavantage["metrics"])
                financial_data["metrics"] = self._update_metrics_value(metrics)

                return financial_data
        
        if use_financial_modeling_prep:
            fmp_data = self._get_financial_data_fmp()
            if fmp_data and yfinance_data:
                metrics = self.merge_metrics(yfinance_data["metrics"], fmp_data['metrics'])
                financial_data["metrics"] = self._update_metrics_value(metrics)

                return financial_data
        
        financial_data["metrics"] = self._update_metrics_value(yfinance_data["metrics"])
        return financial_data

