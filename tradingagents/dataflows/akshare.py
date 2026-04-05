"""
AKShare data interface for A-share stocks
- Provides Chinese A-share market data (price, fundamentals, indicators)
- Compatible with TradingAgents framework interface
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from stockstats import StockDataFrame
from .stockstats_utils import _clean_dataframe

def get_akshare_stock(
    ticker: str,
    start_date: str,
    end_date: str
) -> str:
    """
    Get daily OHLCV data for A-share stock using AKShare
    ticker: A-share ticker (e.g. 300762 for 上海瀚讯)
    start_date: Start date in yyyy-mm-dd format
    end_date: End date in yyyy-mm-dd format

    Returns:
        CSV string containing the daily time series data filtered to the date range.
    """
    try:
        # Convert date formats to AKShare requirement (YYYYMMDD)
        start_fmt = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d")
        end_fmt = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d")

        # Get history data from AKShare
        df = ak.stock_zh_a_hist(symbol=ticker, period="daily", start_date=start_fmt, end_date=end_fmt)

        # Rename columns to match TradingAgents convention
        df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amplitude', 'pct_change', 'change_amount', 'turnover']

        # Ensure correct date format
        df['date'] = pd.to_datetime(df['date']).dt.strftime("%Y-%m-%d")

        # Sort by date ascending
        df = df.sort_values('date').reset_index(drop=True)

        # Return as CSV string matching the interface expectation
        return df.to_csv(index=False)
    except Exception as e:
        print(f"Error getting AKShare data for {ticker}: {e}")
        raise

def get_akshare_indicator(
    symbol: str,
    indicator: str,
    curr_date: str
) -> any:
    """
    Calculate technical indicators using stockstats
    Same interface as other vendors
    """
    from .stockstats_utils import StockstatsUtils
    return StockstatsUtils.get_stock_stats(symbol, indicator, curr_date)

def _format_akshare_symbol(ticker: str) -> str:
    """Format ticker for akshare - add exchange prefix"""
    if len(ticker) == 6:
        if ticker.startswith('60') or ticker.startswith('688'):
            return f"sh{ticker}"
        elif ticker.startswith('00') or ticker.startswith('30'):
            return f"sz{ticker}"
    return ticker

def get_akshare_fundamentals(ticker: str, curr_date: str = None) -> str:
    """
    Get fundamental data for A-share stock
    Returns formatted string for LLM consumption
    """
    try:
        # Get company profile - latest akshare uses stock_individual_info_em
        symbol = _format_akshare_symbol(ticker)
        info = ak.stock_individual_info_em(symbol=symbol)
        profile = dict(zip(info['item'], info['value']))

        # Format output as string
        output = "Company Fundamental Information (from AKShare):\n"
        output += "================================\n"
        for k, v in profile.items():
            output += f"{k}: {v}\n"

        output += "\n"
        return output
    except Exception as e:
        print(f"Error getting AKShare fundamentals for {ticker}: {e}")
        return f"Error fetching fundamentals: {e}"

def get_akshare_balance_sheet(ticker: str, curr_date: str = None, freq: str = "quarterly") -> str:
    """Get balance sheet as formatted string"""
    try:
        # latest akshare uses stock_balance_sheet_by_report_em
        symbol = _format_akshare_symbol(ticker)
        df = ak.stock_balance_sheet_by_report_em(symbol=symbol)
        return df.to_markdown()
    except Exception as e:
        print(f"Error getting balance sheet: {e}")
        return f"Error fetching balance sheet: {e}"

def get_akshare_cashflow(ticker: str, curr_date: str = None, freq: str = "quarterly") -> str:
    """Get cash flow statement as formatted string"""
    try:
        # latest akshare uses stock_cash_flow_sheet_by_report_em
        symbol = _format_akshare_symbol(ticker)
        df = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
        return df.to_markdown()
    except Exception as e:
        print(f"Error getting cash flow: {e}")
        return f"Error fetching cash flow: {e}"

def get_akshare_income_statement(ticker: str, curr_date: str = None, freq: str = "quarterly") -> str:
    """Get income statement as formatted string"""
    try:
        # latest akshare uses stock_profit_sheet_by_report_em
        symbol = _format_akshare_symbol(ticker)
        df = ak.stock_profit_sheet_by_report_em(symbol=symbol)
        return df.to_markdown()
    except Exception as e:
        print(f"Error getting income statement: {e}")
        return f"Error fetching income statement: {e}"

def get_akshare_insider_transactions(ticker: str, curr_date: str = None) -> str:
    """Get insider transactions (not available via akshare)"""
    return "Insider transaction data not available from AKShare"

def get_akshare_news(ticker: str, start_date: str = None, end_date: str = None) -> list:
    """Get news (not available via akshare) - returns empty list"""
    return []

def get_akshare_global_news(curr_date: str = None, look_back_days: int = 7, limit: int = 10) -> list:
    """Get global market news - returns empty list"""
    return []
