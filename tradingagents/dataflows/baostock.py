"""
Baostock data interface for A-share stocks
- Provides free Chinese A-share market data (price, OHLCV)
- Compatible with TradingAgents framework interface
- Completely free, no token or积分 required
"""

import baostock as bs
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from stockstats import StockDataFrame
from .stockstats_utils import _clean_dataframe


def get_baostock_stock(
    ticker: str,
    start_date: str,
    end_date: str
) -> str:
    """
    Get daily OHLCV data for A-share stock using Baostock
    ticker: A-share ticker (e.g. 300762 for 上海瀚讯)
    start_date: Start date in yyyy-mm-dd format
    end_date: End date in yyyy-mm-dd format

    Returns:
        CSV string containing the daily time series data filtered to the date range.
    """
    try:
        # Login to baostock
        lg = bs.login()
        if lg.error_code != '0':
            print(f"Baostock login failed: {lg.error_msg}")
            raise Exception(f"Baostock login failed: {lg.error_msg}")

        # Format stock code for baostock: sz/sh prefix
        if len(ticker) == 6:
            # A-share: 6开头 sh, 0/3开头 sz
            if ticker.startswith('6'):
                bs_ticker = f"sh.{ticker}"
            else:
                bs_ticker = f"sz.{ticker}"
        else:
            # Already has prefix
            bs_ticker = ticker

        # Get history data from Baostock
        # Fields: date,code,open,high,low,close,volume,amount,turn
        rs = bs.query_history_k_data_plus(
            bs_ticker,
            "date,code,open,high,low,close,volume,amount,turn",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"  # 3 = post-adjustment (后复权)
        )

        if rs.error_code != '0':
            raise Exception(f"Baostock query failed: {rs.error_msg}")

        # Convert to DataFrame
        data_list = []
        while (rs.next()):
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)

        # Rename columns to match TradingAgents convention
        # Existing columns: date,code,open,high,low,close,volume,amount,turn
        df = df.rename(columns={
            'turn': 'turnover'
        })

        # Ensure all required columns exist (match akshare output format)
        required_cols = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'turnover']
        for col in required_cols:
            if col not in df.columns:
                df[col] = np.nan

        # Convert numeric columns
        numeric_cols = ['open', 'close', 'high', 'low', 'volume', 'amount', 'turnover']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Filter by date range (baostock already does this, just double-check)
        df['date'] = pd.to_datetime(df['date'])
        df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
        df['date'] = df['date'].dt.strftime("%Y-%m-%d")

        # Sort by date ascending
        df = df.sort_values('date').reset_index(drop=True)

        # Logout
        bs.logout()

        # Also save to cache in Yahoo Finance format for StockstatsUtils to use
        from .config import get_config
        config = get_config()
        
        # Rename columns to match yfinance format that StockstatsUtils expects
        df_yfin = df[required_cols].rename(columns={
            'date': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume',
        })
        
        # Save to cache with same naming convention as yfinance
        today_date = pd.Timestamp.today()
        start_date = today_date - pd.DateOffset(years=5)
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = today_date.strftime("%Y-%m-%d")
        
        os.makedirs(config["data_cache_dir"], exist_ok=True)
        data_file = os.path.join(
            config["data_cache_dir"],
            f"{ticker}-YFin-data-{start_str}-{end_str}.csv",
        )
        df_yfin.to_csv(data_file, index=False)
        
        # Return as CSV string matching the interface expectation
        return df[required_cols].to_csv(index=False)

    except Exception as e:
        # Ensure logout even on error
        try:
            bs.logout()
        except:
            pass
        print(f"Error getting Baostock data for {ticker}: {e}")
        raise


def get_baostock_indicator(
    symbol: str,
    indicator: str,
    curr_date: str,
    look_back_days: int = 90
) -> any:
    """
    Calculate technical indicators using stockstats
    Same interface as other vendors
    """
    from .stockstats_utils import StockstatsUtils
    # look_back_days is ignored by StockstatsUtils which always loads 5 years of data
    return StockstatsUtils.get_stock_stats(symbol, indicator, curr_date)


def get_baostock_fundamentals(ticker: str, curr_date: str = None) -> str:
    """
    Get fundamental data for A-share stock
    Baostock doesn't provide fundamental data directly
    """
    return "Fundamental data (balance sheet, income statement) not available from Baostock. Please switch to another vendor (akshare/alpha_vantage) for fundamentals."


def get_baostock_balance_sheet(ticker: str, curr_date: str = None, freq: str = "quarterly") -> str:
    """Get balance sheet - not available from Baostock"""
    return "Balance sheet data not available from Baostock. Please use akshare or alpha_vantage."


def get_baostock_cashflow(ticker: str, curr_date: str = None, freq: str = "quarterly") -> str:
    """Get cash flow statement - not available from Baostock"""
    return "Cash flow data not available from Baostock. Please use akshare or alpha_vantage."


def get_baostock_income_statement(ticker: str, curr_date: str = None, freq: str = "quarterly") -> str:
    """Get income statement - not available from Baostock"""
    return "Income statement data not available from Baostock. Please use akshare or alpha_vantage."


def get_baostock_insider_transactions(ticker: str, curr_date: str = None) -> str:
    """Get insider transactions (not available via baostock)"""
    return "Insider transaction data not available from Baostock"


def get_baostock_news(ticker: str, start_date: str = None, end_date: str = None) -> list:
    """Get news (not available via baostock) - returns empty list"""
    return []


def get_baostock_global_news(curr_date: str = None, look_back_days: int = 7, limit: int = 10) -> list:
    """Get global market news - returns empty list"""
    return []
