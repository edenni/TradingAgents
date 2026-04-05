import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "openai",
    "deep_think_llm": "accounts/fireworks/routers/kimi-k2p5-turbo",
    "quick_think_llm": "accounts/fireworks/routers/kimi-k2p5-turbo",
    "backend_url": "https://api.fireworks.ai/inference/v1",
    "max_tokens": 12000,
    # Provider-specific thinking configuration
    "google_thinking_level": None,      # "high", "minimal", etc.
    "openai_reasoning_effort": None,    # "medium", "high", "low"
    "anthropic_effort": None,           # "high", "medium", "low"
    # Output language for analyst reports and final decision
    # Internal agent debate stays in English for reasoning quality
    "output_language": "Chinese",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Data vendor configuration
    # Category-level configuration (default for all tools in category)
    "data_vendors": {
        "core_stock_apis": "baostock",        # Options: alpha_vantage, yfinance, akshare, baostock (for A-share)
        "technical_indicators": "baostock",   # Options: alpha_vantage, yfinance, akshare, baostock (for A-share)
        "fundamental_data": "akshare",       # Options: alpha_vantage, yfinance, akshare, baostock (for A-share)
        "news_data": "yfinance",             # Options: alpha_vantage, yfinance, akshare, baostock (akshare/baostock has no news)
    },
    # Tool-level configuration (takes precedence over category-level)
    "tool_vendors": {
        # Example: "get_stock_data": "alpha_vantage",  # Override category default
    },
}
