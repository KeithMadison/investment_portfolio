import yfinance as yf
import pandas as pd
import numpy as np
from dataclasses import dataclass
from collections import namedtuple
from datetime import date

# Define a namedtuple for holding ticker and weight together
TickerWeight = namedtuple('TickerWeight', ['ticker', 'weight'])

@dataclass
class Portfolio:
    """Class for representing a financial portfolio.

    Attributes:
        assets (list[TickerWeight]): List of (ticker: str, weight: float) tuples representing assets and their weights.
        start_date (date): Start date of the portfolio.
        end_date (date): End date of the portfolio.
        rebalancing_frequency (str, optional): Frequency of portfolio rebalancing (default: '1mo', monthly).
    """
    assets: list[TickerWeight]
    start_date: date
    end_date: date
    rebalancing_frequency: str = '1mo'

    def __post_init__(self):
        """Post-initialization to set up additional attributes."""
        self.tickers = [asset.ticker for asset in self.assets]
        self.weights = np.array([asset.weight for asset in self.assets])
        self.weights = self.weights / np.sum(self.weights)  # Normalize weights
        self.market_data = self.get_market_data()
        self.market_returns = self.calculate_market_returns()

    def get_market_data(self) -> pd.DataFrame:
        """Fetch adjusted closing prices for the given tickers and date range."""
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date, 
                           interval=self.rebalancing_frequency, progress=False)['Adj Close']
        return data

    def calculate_market_returns(self) -> pd.DataFrame:
        """Calculate market returns with specified frequency."""
        returns = self.market_data.pct_change().dropna()
        return returns

    def asset_volatility_decomposition(self) -> np.ndarray:
        """Calculate the contribution of each asset to portfolio volatility.

        Returns:
            np.ndarray: Array of asset volatility contributions.
        """
        asset_volatilities = self.market_returns.std(axis=0)
        asset_volatility_decomposition = asset_volatilities * self.weights
        return asset_volatility_decomposition

    def portfolio_return_metrics(self) -> tuple[np.ndarray, pd.Series, pd.Series, pd.Series]:
        """Calculate portfolio return metrics.

        Returns:
            tuple[np.ndarray, pd.Series, pd.Series, pd.Series]: Tuple containing portfolio returns,
            cumulative portfolio value, cumulative profit and loss, and monthly profit and loss.
        """
        portfolio_returns = self.market_returns @ self.weights
        portfolio_value = (1 + portfolio_returns).cumprod()
        cumulative_pnl = portfolio_value - 1
        pnl = portfolio_value.diff().fillna(0)
        return portfolio_returns, portfolio_value, cumulative_pnl, pnl

    def portfolio_volatility_metrics(self, risk_free_rate: float = 0.0, alpha: float = 0.05) -> tuple[float, float, float, float, float]:
        """Calculate portfolio volatility metrics.

        Args:
            risk_free_rate (float, optional): Risk-free rate (default: 0.0).
            alpha (float, optional): Significance level for Value at Risk (default: 0.05).

        Returns:
            tuple[float, float, float, float, float]: Tuple containing annualized standard deviation,
            portfolio beta, annualized Sharpe ratio, Conditional Value at Risk (CVaR), and Sortino ratio.
        """
        portfolio_returns, _, _, _ = self.portfolio_return_metrics()
        market_returns = self.market_returns.mean(axis=1)
        portfolio_beta = portfolio_returns.cov(market_returns) / market_returns.var()
        portfolio_var = portfolio_returns.quantile(alpha)
        portfolio_cvar = portfolio_returns[portfolio_returns <= portfolio_var].mean()
        portfolio_annualized_std = portfolio_returns.std() * np.sqrt(12) * 100
        annualized_sharpe_ratio = (portfolio_returns.mean() - risk_free_rate) / portfolio_annualized_std * np.sqrt(12)
        downside_returns = portfolio_returns[portfolio_returns < risk_free_rate]
        downside_std = downside_returns.std() if not downside_returns.empty else np.nan
        sortino_ratio = (portfolio_returns.mean() - risk_free_rate) / downside_std if not np.isnan(downside_std) else np.nan
        return portfolio_annualized_std, portfolio_beta, annualized_sharpe_ratio, portfolio_cvar, sortino_ratio
