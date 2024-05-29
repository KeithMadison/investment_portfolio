import pandas as pd
from portfolio import Portfolio, TickerWeight
from datetime import date


def generate_portfolio_excel(portfolio_1: Portfolio, portfolio_2: Portfolio):
    """
    Generate an Excel sheet with volatility and return metrics for two portfolios.

    Args:
        portfolio_1 (Portfolio): First portfolio.
        portfolio_2 (Portfolio): Second portfolio.
    """

    # Get volatility metrics for both portfolios
    metrics_data = []
    for i, portfolio in enumerate([portfolio_1, portfolio_2], start=1):
        portfolio_std, portfolio_beta, annualized_sharpe_ratio, portfolio_cvar, sortino_ratio = portfolio.portfolio_volatility_metrics()
        metrics_data.append({
            'Portfolio': f'Portfolio {i}',
            'Portfolio Std': portfolio_std,
            'Portfolio Beta': portfolio_beta,
            'Annualized Sharpe Ratio': annualized_sharpe_ratio,
            'Portfolio CVaR (5%)': portfolio_cvar,
            'Sortino Ratio': sortino_ratio
        })

    metrics_df = pd.DataFrame(metrics_data)

    # Get return metrics data for both portfolios
    return_data = []
    for i, portfolio in enumerate([portfolio_1, portfolio_2], start=1):
        returns, _, cumulative_pnl, pnl = portfolio.portfolio_return_metrics()
        returns_df = pd.DataFrame({'Date': returns.index.strftime('%Y-%m-%d'), f'Portfolio {i} Returns': returns.values})
        pnl_df = pd.DataFrame({'Date': pnl.index.strftime('%Y-%m-%d'), f'Portfolio {i} P&L': pnl.values})
        cumulative_pnl_df = pd.DataFrame({'Date': cumulative_pnl.index.strftime('%Y-%m-%d'), f'Portfolio {i} Cumulative P&L': cumulative_pnl.values})
        return_data.extend([returns_df, pnl_df, cumulative_pnl_df])

    return_df = pd.concat(return_data, axis=1)

    # Write to Excel
    with pd.ExcelWriter("portfolio_metrics.xlsx") as writer:
        metrics_df.to_excel(writer, sheet_name='Volatility Metrics', index=False)
        return_df.to_excel(writer, sheet_name='Return Metrics', index=False)


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

# Generate Excel sheet
generate_portfolio_excel(portfolio_1, portfolio_2)
