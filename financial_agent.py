# financial_agent.py

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define agents
websearch_agent = Agent(
    name="Web Search Agent",
    role="A web search agent that can answer questions using the information from web.",
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    tools=[DuckDuckGo()],
    instructions=["Always include the source of the information in your answer."],
    show_tool_calls=False,
    markdown=True,
)

financial_agent = Agent(
    name="Financial Agent",
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    role="A financial agent that analyses stock data and provides insights.",
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=False,
    markdown=True,
)

multi_ai_agent = Agent(
    team=[websearch_agent, financial_agent],
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    instructions=["Always include sources", "Use table to display data"],
    show_tool_calls=False,
    markdown=True,
)

# ✅ Function to analyze stock and return only final summary
def analyze_stock_summary(ticker: str) -> str:
    prompt = (
        f"Summarise analyst recommendation and share the latest news for {ticker}. "
        "Provide a final financial summary at the end, under the heading '## Final Summary'."
        "Avoid forcing news search if not available. Do not give an error if agent fails. Return that no updates are available."
    )

    try:
        run_response = multi_ai_agent.run(prompt)
        response_text = run_response.messages[-1].content
        return response_text
    except Exception as e:
        return f"Error analyzing {ticker}: {str(e)}"
