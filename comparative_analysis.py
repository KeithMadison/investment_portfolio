import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import date
import pandas as pd
from portfolio import Portfolio, TickerWeight

def plot_portfolio_metrics(*portfolios, initial_investment=10000):
    """
    Plot various metrics for given portfolios.

    Args:
        *portfolios: Variable number of Portfolio objects.
        initial_investment (int, optional): Initial investment amount, in USD. Defaults to 10000.
    """
    metrics = []

    # Compute metrics for each portfolio
    for portfolio in portfolios:
        returns, value, cumulative_pnl, pnl = portfolio.portfolio_return_metrics()
        monthly_returns = returns.resample('ME').apply(lambda x: (1 + x).prod() - 1)
        metrics.append((monthly_returns, value, cumulative_pnl, pnl))

    # Plot monthly returns
    plt.figure(figsize=(7, 3.5))
    for i, (monthly_returns, _, _, _) in enumerate(metrics):
        plt.bar(monthly_returns.index, monthly_returns * 100, label=f'Portfolio {i+1}', alpha=0.5, width=20)
    plt.title('Monthly Returns')
    plt.xlabel('Date')
    plt.ylabel('Monthly Returns (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Plot portfolio value
    plt.figure(figsize=(7, 3.5))
    for i, (_, value, _, _) in enumerate(metrics):
        plt.plot(value.index, value * initial_investment, label=f'Portfolio {i+1}')
    plt.title(f'Portfolio Value (Initial Investment ${initial_investment:d})')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:.2f}'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Plot portfolio cumulative P&L
    plt.figure(figsize=(7, 3.5))
    for i, (_, _, cumulative_pnl, _) in enumerate(metrics):
        plt.plot(cumulative_pnl.index, cumulative_pnl * 100, label=f'Portfolio {i+1}')
    plt.title('Portfolio Cumulative P&L')
    plt.xlabel('Date')
    plt.ylabel('P&L (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Plot portfolio monthly P&L
    plt.figure(figsize=(7, 3.5))
    for i, (_, _, _, pnl) in enumerate(metrics):
        plt.plot(pnl.index, pnl * initial_investment, label=f'Portfolio {i+1}')
    plt.title(f'Portfolio Monthly P&L (Initial Investment ${initial_investment:d})')
    plt.xlabel('Date')
    plt.ylabel('P&L')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:.2f}'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Plot asset volatility decomposition for each portfolio
    for i, portfolio in enumerate(portfolios):
        plt.figure(figsize=(7, 7))
        asset_volatilities = portfolio.asset_volatility_decomposition()
        plt.pie(asset_volatilities, labels=[tw.ticker for tw in portfolio.assets], autopct='%1.1f%%', startangle=90, pctdistance=0.85,
                wedgeprops=dict(width=0.4), colors=plt.cm.tab20.colors)
        plt.title(f'Asset Volatility Decomposition (Portfolio {i+1})', loc='center')
        plt.axis('equal')
        plt.show()

    # Print formatted volatility metrics for each portfolio
    for i, portfolio in enumerate(portfolios):
        portfolio_std, portfolio_beta, annualized_sharpe_ratio, portfolio_cvar, sortino_ratio = portfolio.portfolio_volatility_metrics()

        metrics_table = pd.DataFrame({
            "Metric": ["Portfolio Std", "Portfolio Beta", "Annualized Sharpe Ratio", "Portfolio CVaR (5%)", "Sortino Ratio"],
            "Value": [portfolio_std, portfolio_beta, annualized_sharpe_ratio, portfolio_cvar, sortino_ratio]
        })

        print(f"Portfolio {i+1} Volatility Metrics:")
        print(metrics_table.to_string(index=False))

# Initialize two portfolios
assets_1 = [TickerWeight('SPY', 0.6), TickerWeight('AGG', 0.4)]
assets_2 = [TickerWeight('SPY', 0.6), TickerWeight('AGG', 0.3), TickerWeight('TIP', 0.1)]
start_date = date(2021, 1, 1)
end_date = date(2023, 12, 31)

portfolio_1 = Portfolio(
    assets=assets_1,
    start_date=start_date,
    end_date=end_date
)

portfolio_2 = Portfolio(
    assets=assets_2,
    start_date=start_date,
    end_date=end_date
)

plot_portfolio_metrics(portfolio_1, portfolio_2)
