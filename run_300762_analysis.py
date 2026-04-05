
#!/usr/bin/env python3
"""
Run TradingAgents analysis for 上海瀚讯 (300762.SZ)
Using AKShare for A-share data and OpenRouter for LLM
"""

import os
import sys
import tradingagents

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Unset proxies for domestic data access
for k in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    if k in os.environ:
        del os.environ[k]

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

print("=" * 60)
print("TradingAgents - 上海瀚讯 (300762) 多智能体分析")
print("=" * 60)
print(f"LLM Provider: {DEFAULT_CONFIG['llm_provider']}")
print(f"Deep Think Model: {DEFAULT_CONFIG['deep_think_llm']}")
print(f"Data Vendor: {DEFAULT_CONFIG['data_vendors']}")
print()

# Initialize trading graph
config = DEFAULT_CONFIG.copy()
ta = TradingAgentsGraph(debug=True, config=config)

# Run propagation for 上海瀚讯 on today's date
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")
ticker = "300762.sz"

print(f"Starting analysis for {ticker} (上海瀚讯) at {today}")
print("-" * 60)
print()

summary, decision = ta.propagate(ticker, today)

print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)
print("\nSUMMARY:")
print(summary)
print("\nDECISION:")
print(decision)
print()

# Save result to file
output_dir = "./results"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"{ticker}_analysis_{today}.md")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("# TradingAgents Analysis: 上海瀚讯 (300762)\n\n")
    f.write(f"Date: {today}\n")
    f.write(f"LLM: {config['llm_provider']} - {config['deep_think_llm']}\n\n")
    f.write("## Summary\n\n")
    f.write(str(summary))
    f.write("\n\n## Decision\n\n")
    f.write(str(decision))
    f.write("\n")

print(f"Result saved to: {output_file}")
