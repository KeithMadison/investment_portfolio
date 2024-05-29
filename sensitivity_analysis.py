import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from portfolio import Portfolio, TickerWeight

def plot_sensitivity_analysis(start_date_str, end_date_str):
    """
    Perform sensitivity analysis on portfolio metrics.

    Args:
        start_date_str (str): Start date in YYYY-MM-DD format.
        end_date_str (str): End date in YYYY-MM-DD format.
    """
    # Convert string dates to datetime.date objects
    start_date = date.fromisoformat(start_date_str)
    end_date = date.fromisoformat(end_date_str)

    tickers = ['SPY', 'AGG', 'TIP']
    portfolios = []

    # Generate portfolios with varying TIPS allocation
    for tips_allocation in np.arange(0, 0.21, 0.05):
        weights = [0.6, 0.4 - tips_allocation, tips_allocation]
        assets = [TickerWeight(ticker, weight) for ticker, weight in zip(tickers, weights)]
        portfolios.append(Portfolio(assets, start_date, end_date))

    # Calculate portfolio metrics
    sharpe_ratios = []
    cvars = []
    sortino_ratios = []
    portfolio_values = []
    net_returns = []

    for portfolio in portfolios:
        _, portfolio_value, _, _ = portfolio.portfolio_return_metrics()
        _, _, sharpe_ratio, cvar, sortino_ratio = portfolio.portfolio_volatility_metrics()
        sharpe_ratios.append(sharpe_ratio)
        cvars.append(cvar)
        sortino_ratios.append(sortino_ratio)
        portfolio_values.append(portfolio_value)
        net_returns.append(portfolio_value.iloc[-1])

    # Plot sensitivity analysis
    plt.figure(figsize=(7, 3.5))
    plt.plot(np.arange(0, 21, 5), sharpe_ratios, marker='o', label='Sharpe Ratio')
    plt.xlabel('TIPS Allocation (%)')
    plt.ylabel('Metrics')
    plt.title('Sensitivity Analysis of Portfolio Performance Metrics')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(7, 3.5))
    for portfolio_value, tips_allocation in zip(portfolio_values, np.arange(0, 0.21, 0.05)):
        plt.plot(portfolio_value.index, portfolio_value, label=f'TIPS {tips_allocation*100:.0f}%')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.title('Portfolio Cumulative Return for Different TIPS Allocations')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(7, 3.5))
    plt.plot(np.arange(0, 21, 5), net_returns, marker='o')
    plt.xlabel('TIPS Allocation (%)')
    plt.ylabel('Net Return / Initial Investment')
    plt.title('Net Return Over Three Years for Different TIPS Allocations')
    plt.grid(True)
    plt.show()

# Run the sensitivity analysis
plot_sensitivity_analysis('2021-01-01', '2023-12-31')
