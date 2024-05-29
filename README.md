# investment_portfolio




# `portfolio.py`

The `Portfolio` class represents a financial portfolio and provides methods for analyzing its performance via a variety of commonly used return and volatility metrics.

## Attributes

- `assets`: A list of TickerWeight tuples representing assets in the portfolio, where each tuple contains a ticker symbol (string) and its corresponding weight (float). These weights need not be normalized in advance.
  -`TickerWeight`: A namedtuple for holding ticker symbol and its corresponding weight in the portfolio.
    - `ticker`: A string representing the ticker symbol of the asset.
    - `weight`: A float representing the weight of the asset in the portfolio. 
- `start_date`: The start date of the portfolio analysis.
- `end_date`: The end date of the portfolio analysis.
- `rebalancing_frequency` (optional): The frequency at which the portfolio is rebalanced. Default is '1mo' (monthly).

## Methods

### Initialization

#### `__init__(assets: list[TickerWeight], start_date: date, end_date: date, rebalancing_frequency: str = '1mo') -> None`

Initializes a new Portfolio instance with the provided attributes.

- `assets`: List of (ticker, weight) tuples representing assets and their weights in the portfolio.
- `start_date`: Start date of the portfolio analysis.
- `end_date`: End date of the portfolio analysis.
- `rebalancing_frequency`: Frequency of portfolio rebalancing (default: '1mo', monthly).
  - Valid frequencies: `'1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'`, as per `yfinance`.

### Data Retrieval and Calculation

#### `get_market_data() -> pd.DataFrame`

Fetches adjusted closing prices from Yahoo Finance for the assets within the specified date range.

#### `calculate_market_returns() -> pd.DataFrame`

Calculates the market returns for the assets based on the provided rebalancing frequency.

### Portfolio Metrics

#### `asset_volatility_decomposition() -> np.ndarray`

Calculates the contribution of each asset to the overall portfolio volatility.

#### `portfolio_return_metrics() -> tuple[np.ndarray, pd.Series, pd.Series, pd.Series]`

Calculates various return metrics for the portfolio, including returns, cumulative portfolio value, cumulative profit and loss, and monthly profit and loss.

#### `portfolio_volatility_metrics(risk_free_rate: float = 0.0, alpha: float = 0.05) -> tuple[float, float, float, float, float]`

Calculates various volatility metrics for the portfolio, including annualized standard deviation, portfolio beta, Sharpe ratio, Conditional Value at Risk (CVaR), and Sortino ratio.

- `risk_free_rate` (optional): Risk-free rate for calculating Sharpe ratio (default: 0.0).
- `alpha` (optional): Significance level for CVaR calculation (default: 0.05).

## Example Usage

```python
# Example usage of Portfolio class
from datetime import date
portfolio = Portfolio(
    assets=[TickerWeight('AAPL', 0.5), TickerWeight('MSFT', 0.5)],
    start_date=date(2023, 1, 1),
    end_date=date(2023, 12, 31)
)
```


# `comparative_analysis.py`

The `plot_portfolio_metrics` function generates various plots and metrics for an arbitrary number of portfolios.

## Arguments

- `*portfolios`: Variable number of `Portfolio` objects to analyze and plot metrics for.
- `initial_investment` (optional): Initial investment amount, in USD. Default is 10,000 USD.

## Functionality

- Generates the following plots:
  - **Monthly Returns**: Bar plot showing monthly returns for each portfolio.
  - **Portfolio Value**: Line plot showing the cumulative value of each portfolio over time.
  - **Portfolio Cumulative P&L**: Line plot showing the cumulative profit and loss of each portfolio over time.
  - **Portfolio Monthly P&L**: Line plot showing the monthly profit and loss of each portfolio over time.
  - **Asset Volatility Decomposition**: Pie chart showing the contribution of each asset to the portfolio's volatility for each portfolio.
- Additionally, it prints formatted volatility metrics for each portfolio, including:
  - Portfolio standard deviation
  - Portfolio beta
  - Annualized Sharpe ratio
  - Portfolio Conditional Value at Risk (CVaR) at 5% significance level
  - Sortino ratio

## Example Usage

```python
# Example usage of plot_portfolio_metrics function
from datetime import date
from portfolio import Portfolio, TickerWeight

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
```

# `sensitivity_analysis.py`

The `plot_sensitivity_to_allocation` function performs sensitivity analysis on portfolio metrics with respect to TIPS (Treasury Inflation-Protected Securities) allocation.

## Arguments

- `start_date_str` (str): Start date of the analysis in YYYY-MM-DD format.
- `end_date_str` (str): End date of the analysis in YYYY-MM-DD format.

## Functionality

- Generates three plots:
  - **Sensitivity Analysis of Portfolio Performance Metrics**: Line plot showing the sensitivity of the Sharpe ratio to changes in TIPS allocation.
  - **Portfolio Cumulative Return for Different TIPS Allocations**: Line plot showing the cumulative return of the portfolio for different TIPS allocations over time.
  - **Net Return Over Three Years for Different TIPS Allocations**: Line plot showing the net return of the portfolio over three years for different TIPS allocations.

## Example Usage

```python
# Example usage of plot_sensitivity_to_allocation function
plot_sensitivity_to_allocation('2021-01-01', '2023-12-31')
```

# `generate_excel.py`

The `generate_portfolio_excel` function creates an Excel sheet containing volatility and return metrics for two portfolios.

## Arguments

- `portfolio_1` (Portfolio): First portfolio.
- `portfolio_2` (Portfolio): Second portfolio.

## Functionality

- Generates two `XSLX` sheets:
  - **Volatility Metrics**: Contains volatility metrics such as portfolio standard deviation, beta, Sharpe ratio, CVaR (Conditional Value at Risk), and Sortino ratio for each portfolio.
  - **Return Metrics**: Contains return metrics such as returns, profit and loss (P&L), and cumulative P&L for each portfolio.

## Example Usage

```python
# Example usage of generate_portfolio_excel function
from datetime import date
from portfolio import Portfolio, TickerWeight

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
```
