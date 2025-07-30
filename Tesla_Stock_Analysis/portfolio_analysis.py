# 📊 Multi-Symbol Portfolio Analysis Extension
# Advanced portfolio analysis for multiple stocks

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Machine Learning imports
try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

class PortfolioAnalyzer:
    """
    Advanced multi-symbol portfolio analysis system
    """
    
    def __init__(self, symbols=None, start_date=None, end_date=None):
        """
        Initialize portfolio analyzer
        
        Args:
            symbols (list): List of stock symbols to analyze
            start_date (str): Start date for analysis (YYYY-MM-DD)
            end_date (str): End date for analysis (YYYY-MM-DD)
        """
        # Default tech portfolio
        self.symbols = symbols or ['TSLA', 'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'META', 'NFLX']
        self.start_date = start_date or (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d')
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        
        # Data containers
        self.data = {}
        self.portfolio_data = None
        self.returns_data = None
        self.correlation_matrix = None
        self.portfolio_metrics = {}
        
        print(f"🎯 Portfolio Analyzer initialized for {len(self.symbols)} symbols")
        print(f"📅 Analysis period: {self.start_date} to {self.end_date}")
    
    def fetch_portfolio_data(self, use_existing_data=None, delay_seconds=2):
        """
        Fetch data for all symbols in the portfolio with rate limiting
        
        Args:
            use_existing_data (dict): Existing data to reuse (e.g., Tesla data already loaded)
            delay_seconds (float): Delay between API calls to avoid rate limiting
        """
        print("\n📥 Fetching portfolio data...")
        
        all_data = {}
        successful_symbols = []
        
        # Use existing data if provided
        if use_existing_data:
            for symbol, data in use_existing_data.items():
                if symbol in self.symbols and not data.empty:
                    all_data[symbol] = data
                    successful_symbols.append(symbol)
                    print(f"  ✅ {symbol}: Using existing data ({len(data)} days)")
        
        # Fetch remaining symbols with rate limiting
        remaining_symbols = [s for s in self.symbols if s not in successful_symbols]
        
        if remaining_symbols:
            print(f"  🔄 Fetching {len(remaining_symbols)} additional symbols with rate limiting...")
            
            for i, symbol in enumerate(remaining_symbols):
                try:
                    # Add delay to avoid rate limiting
                    if i > 0:
                        print(f"  ⏱️  Waiting {delay_seconds}s to avoid rate limiting...")
                        time.sleep(delay_seconds)
                    
                    print(f"  📊 Fetching {symbol} ({i+1}/{len(remaining_symbols)})...")
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(start=self.start_date, end=self.end_date)
                    
                    if not data.empty:
                        all_data[symbol] = data
                        successful_symbols.append(symbol)
                        print(f"  ✅ {symbol}: {len(data)} days of data")
                    else:
                        print(f"  ❌ {symbol}: No data available")
                        
                except Exception as e:
                    if "rate limited" in str(e).lower() or "too many requests" in str(e).lower():
                        print(f"  ⚠️  {symbol}: Rate limited - increasing delay...")
                        delay_seconds *= 1.5  # Increase delay for next request
                        time.sleep(delay_seconds)
                        
                        # Retry once with longer delay
                        try:
                            print(f"  🔄 Retrying {symbol} with {delay_seconds:.1f}s delay...")
                            ticker = yf.Ticker(symbol)
                            data = ticker.history(start=self.start_date, end=self.end_date)
                            
                            if not data.empty:
                                all_data[symbol] = data
                                successful_symbols.append(symbol)
                                print(f"  ✅ {symbol}: {len(data)} days of data (retry successful)")
                            else:
                                print(f"  ❌ {symbol}: No data available (retry)")
                        except Exception as retry_e:
                            print(f"  ❌ {symbol}: Retry failed - {retry_e}")
                    else:
                        print(f"  ❌ {symbol}: Error - {e}")
        
        # Fallback: If we have Tesla data but no other symbols, create a demo portfolio
        if len(successful_symbols) == 1 and 'TSLA' in successful_symbols:
            print("\n  💡 Creating synthetic portfolio data for demonstration...")
            tsla_data = all_data['TSLA'].copy()
            
            # Create synthetic data based on Tesla with different volatility and correlation
            np.random.seed(42)  # For reproducibility
            
            synthetic_symbols = ['TECH_STOCK_A', 'TECH_STOCK_B', 'GROWTH_STOCK_C']
            correlations = [0.7, 0.5, 0.3]  # Different correlations with Tesla
            volatility_multipliers = [0.8, 1.2, 1.5]  # Different volatility levels
            
            for i, (synth_symbol, corr, vol_mult) in enumerate(zip(synthetic_symbols, correlations, volatility_multipliers)):
                # Generate correlated returns
                tsla_returns = tsla_data['Close'].pct_change().fillna(0)
                noise = np.random.normal(0, tsla_returns.std() * vol_mult, len(tsla_returns))
                
                # Create correlated returns
                synthetic_returns = corr * tsla_returns + (1 - corr) * noise
                
                # Generate synthetic price series
                initial_price = 100 + i * 50  # Different starting prices
                synthetic_prices = initial_price * (1 + synthetic_returns).cumprod()
                
                # Create synthetic OHLCV data
                synthetic_data = tsla_data.copy()
                price_factor = synthetic_prices / tsla_data['Close']
                
                synthetic_data['Open'] = tsla_data['Open'] * price_factor
                synthetic_data['High'] = tsla_data['High'] * price_factor * (1 + np.random.uniform(0, 0.02, len(tsla_data)))
                synthetic_data['Low'] = tsla_data['Low'] * price_factor * (1 - np.random.uniform(0, 0.02, len(tsla_data)))
                synthetic_data['Close'] = synthetic_prices
                synthetic_data['Volume'] = tsla_data['Volume'] * np.random.uniform(0.5, 1.5, len(tsla_data))
                
                all_data[synth_symbol] = synthetic_data
                successful_symbols.append(synth_symbol)
                print(f"  ✅ {synth_symbol}: Synthetic data created (correlation: {corr:.1f})")
        
        self.symbols = successful_symbols
        self.data = all_data
        
        # Create combined portfolio DataFrame
        if self.data:
            self.create_portfolio_dataframe()
            print(f"\n✅ Portfolio data ready for {len(self.symbols)} symbols")
        else:
            print(f"\n❌ No portfolio data available")
        
        return all_data
    
    def create_portfolio_dataframe(self):
        """Create unified portfolio DataFrame"""
        if not self.data:
            print("❌ No data available. Please fetch data first.")
            return
        
        # Create price DataFrame
        price_data = {}
        volume_data = {}
        
        for symbol in self.symbols:
            price_data[symbol] = self.data[symbol]['Close']
            volume_data[f'{symbol}_Volume'] = self.data[symbol]['Volume']
        
        self.portfolio_data = pd.DataFrame(price_data)
        self.volume_data = pd.DataFrame(volume_data)
        
        # Calculate returns
        self.returns_data = self.portfolio_data.pct_change().dropna()
        self.portfolio_returns = self.returns_data  # Add this alias for consistency
        
        # Calculate correlation matrix
        self.correlation_matrix = self.returns_data.corr()
        
        print(f"📊 Portfolio DataFrame created: {self.portfolio_data.shape}")
        print(f"📈 Returns data shape: {self.returns_data.shape}")
    
    def calculate_portfolio_metrics(self, weights=None):
        """
        Calculate comprehensive portfolio metrics
        
        Args:
            weights (list): Portfolio weights (default: equal weights)
        """
        if self.returns_data is None:
            print("❌ No returns data available")
            return
        
        # Default to equal weights
        if weights is None:
            weights = np.array([1/len(self.symbols)] * len(self.symbols))
        else:
            weights = np.array(weights)
            weights = weights / weights.sum()  # Normalize to sum to 1
        
        # Portfolio returns
        portfolio_returns = (self.returns_data * weights).sum(axis=1)
        
        # Calculate metrics
        annual_return = portfolio_returns.mean() * 252
        annual_volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0
        
        # Individual stock metrics
        individual_metrics = {}
        for symbol in self.symbols:
            stock_returns = self.returns_data[symbol]
            individual_metrics[symbol] = {
                'annual_return': stock_returns.mean() * 252,
                'annual_volatility': stock_returns.std() * np.sqrt(252),
                'sharpe_ratio': (stock_returns.mean() * 252) / (stock_returns.std() * np.sqrt(252)) if stock_returns.std() > 0 else 0,
                'max_drawdown': self.calculate_max_drawdown(self.portfolio_data[symbol]),
                'current_price': self.portfolio_data[symbol].iloc[-1],
                'ytd_return': (self.portfolio_data[symbol].iloc[-1] / self.portfolio_data[symbol].iloc[0] - 1) * 100
            }
        
        # Portfolio metrics
        self.portfolio_metrics = {
            'portfolio_annual_return': annual_return,
            'portfolio_annual_volatility': annual_volatility,
            'portfolio_sharpe_ratio': sharpe_ratio,
            'portfolio_weights': dict(zip(self.symbols, weights)),
            'individual_metrics': individual_metrics,
            'correlation_matrix': self.correlation_matrix,
            'total_return': (portfolio_returns + 1).cumprod().iloc[-1] - 1,
            'max_drawdown': self.calculate_max_drawdown_returns(portfolio_returns)
        }
        
        return self.portfolio_metrics
    
    def calculate_max_drawdown(self, price_series):
        """Calculate maximum drawdown for a price series"""
        peak = price_series.expanding().max()
        drawdown = (price_series - peak) / peak
        return drawdown.min()
    
    def calculate_max_drawdown_returns(self, returns_series):
        """Calculate maximum drawdown from returns series"""
        cumulative = (1 + returns_series).cumprod()
        peak = cumulative.expanding().max()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()
    
    def optimize_portfolio(self, method='sharpe'):
        """
        Optimize portfolio weights
        
        Args:
            method (str): Optimization method ('sharpe', 'min_variance', 'equal')
        """
        if self.returns_data is None:
            print("❌ No returns data available")
            return
        
        print(f"\n🎯 Optimizing portfolio using {method} method...")
        
        if method == 'equal':
            # Equal weights
            optimal_weights = np.array([1/len(self.symbols)] * len(self.symbols))
        
        elif method == 'min_variance':
            # Minimum variance portfolio
            cov_matrix = self.returns_data.cov() * 252
            inv_cov = np.linalg.pinv(cov_matrix)
            ones = np.ones((len(self.symbols), 1))
            optimal_weights = (inv_cov @ ones) / (ones.T @ inv_cov @ ones)
            optimal_weights = optimal_weights.flatten()
        
        elif method == 'sharpe':
            # Maximum Sharpe ratio (simplified)
            # This is a simplified approach - in practice, you'd use optimization libraries
            mean_returns = self.returns_data.mean() * 252
            cov_matrix = self.returns_data.cov() * 252
            
            # Simple approach: weight by return/volatility ratio
            individual_sharpe = mean_returns / np.sqrt(np.diag(cov_matrix))
            optimal_weights = individual_sharpe / individual_sharpe.sum()
        
        # Ensure weights are non-negative and sum to 1
        optimal_weights = np.maximum(optimal_weights, 0)
        optimal_weights = optimal_weights / optimal_weights.sum()
        
        # Calculate optimized portfolio metrics
        optimized_metrics = self.calculate_portfolio_metrics(optimal_weights)
        
        print(f"✅ Portfolio optimized using {method} method")
        print(f"📊 Expected Annual Return: {optimized_metrics['portfolio_annual_return']:.2%}")
        print(f"📊 Expected Annual Volatility: {optimized_metrics['portfolio_annual_volatility']:.2%}")
        print(f"📊 Expected Sharpe Ratio: {optimized_metrics['portfolio_sharpe_ratio']:.3f}")
        
        return optimal_weights, optimized_metrics
    
    def create_portfolio_dashboard(self):
        """Create comprehensive portfolio dashboard"""
        if self.portfolio_data is None:
            print("❌ No portfolio data available")
            return
        
        print("\n📊 Creating portfolio dashboard...")
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=['Portfolio Price Performance', 'Correlation Heatmap',
                          'Individual Stock Performance', 'Returns Distribution',
                          'Risk-Return Scatter', 'Portfolio Composition'],
            specs=[[{"secondary_y": True}, {"type": "heatmap"}],
                   [{"colspan": 2}, None],
                   [{"type": "scatter"}, {"type": "pie"}]]
        )
        
        # 1. Portfolio Performance (normalized)
        normalized_data = self.portfolio_data / self.portfolio_data.iloc[0] * 100
        for symbol in self.symbols:
            fig.add_trace(
                go.Scatter(x=normalized_data.index, y=normalized_data[symbol],
                          name=symbol, mode='lines'),
                row=1, col=1
            )
        
        # 2. Correlation Heatmap
        fig.add_trace(
            go.Heatmap(z=self.correlation_matrix.values,
                      x=self.correlation_matrix.columns,
                      y=self.correlation_matrix.index,
                      colorscale='RdBu', zmid=0,
                      showscale=False),
            row=1, col=2
        )
        
        # 3. Individual Stock Performance Bar Chart
        if self.portfolio_metrics:
            symbols = list(self.portfolio_metrics['individual_metrics'].keys())
            returns = [self.portfolio_metrics['individual_metrics'][s]['ytd_return'] for s in symbols]
            
            fig.add_trace(
                go.Bar(x=symbols, y=returns, name='YTD Returns (%)',
                      marker_color=['green' if r > 0 else 'red' for r in returns]),
                row=2, col=1
            )
        
        # 4. Returns Distribution
        portfolio_returns = self.returns_data.mean(axis=1) * 100
        fig.add_trace(
            go.Histogram(x=portfolio_returns, name='Daily Returns (%)',
                        nbinsx=50, opacity=0.7),
            row=2, col=2
        )
        
        # 5. Risk-Return Scatter
        if self.portfolio_metrics:
            risks = [self.portfolio_metrics['individual_metrics'][s]['annual_volatility'] for s in symbols]
            returns_annual = [self.portfolio_metrics['individual_metrics'][s]['annual_return'] for s in symbols]
            
            fig.add_trace(
                go.Scatter(x=risks, y=returns_annual, mode='markers+text',
                          text=symbols, textposition="top center",
                          marker=dict(size=12, color=returns_annual, colorscale='RdYlGn'),
                          name='Risk-Return'),
                row=3, col=1
            )
        
        # 6. Portfolio Composition (Equal weights for now)
        fig.add_trace(
            go.Pie(labels=self.symbols, 
                  values=[1/len(self.symbols)]*len(self.symbols),
                  name="Portfolio Weights"),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=1200,
            title_text="📊 Multi-Symbol Portfolio Analysis Dashboard",
            showlegend=True
        )
        
        # Save and show
        fig.write_html("outputs/plots/portfolio_dashboard.html")
        fig.show()
        
        print("✅ Portfolio dashboard created!")
        print("📁 Saved to: outputs/plots/portfolio_dashboard.html")
    
    def generate_portfolio_report(self):
        """Generate comprehensive portfolio analysis report"""
        if not self.portfolio_metrics:
            print("❌ No portfolio metrics available. Run calculate_portfolio_metrics() first.")
            return
        
        print("\n📋 Generating Portfolio Analysis Report...")
        
        report = f"""
# 📊 Multi-Symbol Portfolio Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 Portfolio Overview
- **Symbols Analyzed**: {', '.join(self.symbols)}
- **Analysis Period**: {self.start_date} to {self.end_date}
- **Total Trading Days**: {len(self.portfolio_data)}

## 📈 Portfolio Performance Metrics
- **Annual Return**: {self.portfolio_metrics['portfolio_annual_return']:.2%}
- **Annual Volatility**: {self.portfolio_metrics['portfolio_annual_volatility']:.2%}
- **Sharpe Ratio**: {self.portfolio_metrics['portfolio_sharpe_ratio']:.3f}
- **Total Return**: {self.portfolio_metrics['total_return']:.2%}
- **Maximum Drawdown**: {self.portfolio_metrics['max_drawdown']:.2%}

## 🏆 Individual Stock Performance
"""
        
        for symbol in self.symbols:
            metrics = self.portfolio_metrics['individual_metrics'][symbol]
            report += f"""
### {symbol}
- **Current Price**: ${metrics['current_price']:.2f}
- **YTD Return**: {metrics['ytd_return']:.2%}
- **Annual Return**: {metrics['annual_return']:.2%}
- **Annual Volatility**: {metrics['annual_volatility']:.2%}
- **Sharpe Ratio**: {metrics['sharpe_ratio']:.3f}
- **Max Drawdown**: {metrics['max_drawdown']:.2%}
"""
        
        report += f"""
## 🔗 Correlation Analysis
The correlation matrix shows how stocks move together:

**Highest Correlations:**
"""
        # Find highest correlations
        corr_pairs = []
        for i in range(len(self.symbols)):
            for j in range(i+1, len(self.symbols)):
                corr_pairs.append((
                    self.symbols[i], 
                    self.symbols[j], 
                    self.correlation_matrix.iloc[i, j]
                ))
        
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        for i, (stock1, stock2, corr) in enumerate(corr_pairs[:5]):
            report += f"- {stock1} - {stock2}: {corr:.3f}\n"
        
        report += """
## 📊 Risk Analysis
- Diversification benefits are visible when correlations are low
- High correlation (>0.7) indicates similar price movements
- Low correlation (<0.3) provides good diversification

## 🎯 Investment Recommendations
Based on the analysis:
1. **Diversification**: Consider rebalancing if correlations are too high
2. **Risk Management**: Monitor maximum drawdown levels
3. **Performance**: Focus on risk-adjusted returns (Sharpe ratio)
4. **Rebalancing**: Consider periodic rebalancing to maintain target weights

---
*This report was generated by the Advanced Portfolio Analysis System*
"""
        
        # Save report
        report_file = f"outputs/reports/portfolio_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"✅ Portfolio report generated!")
        print(f"📁 Saved to: {report_file}")
        
        return report

# Usage Example and Helper Functions
def analyze_tech_portfolio():
    """Analyze a technology-focused portfolio"""
    tech_symbols = ['TSLA', 'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'META', 'NFLX']
    
    analyzer = PortfolioAnalyzer(tech_symbols)
    analyzer.fetch_portfolio_data()
    analyzer.calculate_portfolio_metrics()
    analyzer.create_portfolio_dashboard()
    
    # Try different optimization methods
    print("\n🎯 Testing Different Portfolio Optimization Methods:")
    
    methods = ['equal', 'sharpe', 'min_variance']
    results = {}
    
    for method in methods:
        weights, metrics = analyzer.optimize_portfolio(method)
        results[method] = {
            'weights': weights,
            'annual_return': metrics['portfolio_annual_return'],
            'annual_volatility': metrics['portfolio_annual_volatility'],
            'sharpe_ratio': metrics['portfolio_sharpe_ratio']
        }
    
    # Compare methods
    print("\n📊 Optimization Methods Comparison:")
    comparison_df = pd.DataFrame({
        method: {
            'Annual Return': f"{results[method]['annual_return']:.2%}",
            'Annual Volatility': f"{results[method]['annual_volatility']:.2%}",
            'Sharpe Ratio': f"{results[method]['sharpe_ratio']:.3f}"
        }
        for method in methods
    }).T
    
    print(comparison_df)
    
    analyzer.generate_portfolio_report()
    
    return analyzer, results

def analyze_diversified_portfolio():
    """Analyze a diversified portfolio across sectors"""
    diversified_symbols = [
        'TSLA',    # Electric Vehicles
        'AAPL',    # Technology
        'JPM',     # Banking
        'JNJ',     # Healthcare
        'XOM',     # Energy
        'DIS',     # Entertainment
        'WMT',     # Retail
        'BA'       # Aerospace
    ]
    
    analyzer = PortfolioAnalyzer(diversified_symbols)
    analyzer.fetch_portfolio_data()
    analyzer.calculate_portfolio_metrics()
    analyzer.create_portfolio_dashboard()
    analyzer.generate_portfolio_report()
    
    return analyzer

def compare_portfolios():
    """Compare different portfolio strategies"""
    print("🔄 Comparing Portfolio Strategies...")
    
    # Tech-focused portfolio
    tech_analyzer = PortfolioAnalyzer(['TSLA', 'AAPL', 'GOOGL', 'MSFT', 'AMZN'])
    tech_analyzer.fetch_portfolio_data()
    tech_metrics = tech_analyzer.calculate_portfolio_metrics()
    
    # Diversified portfolio
    div_analyzer = PortfolioAnalyzer(['TSLA', 'AAPL', 'JPM', 'JNJ', 'XOM'])
    div_analyzer.fetch_portfolio_data()
    div_metrics = div_analyzer.calculate_portfolio_metrics()
    
    # Compare results
    comparison = pd.DataFrame({
        'Tech Portfolio': {
            'Annual Return': f"{tech_metrics['portfolio_annual_return']:.2%}",
            'Annual Volatility': f"{tech_metrics['portfolio_annual_volatility']:.2%}",
            'Sharpe Ratio': f"{tech_metrics['portfolio_sharpe_ratio']:.3f}",
            'Max Drawdown': f"{tech_metrics['max_drawdown']:.2%}"
        },
        'Diversified Portfolio': {
            'Annual Return': f"{div_metrics['portfolio_annual_return']:.2%}",
            'Annual Volatility': f"{div_metrics['portfolio_annual_volatility']:.2%}",
            'Sharpe Ratio': f"{div_metrics['portfolio_sharpe_ratio']:.3f}",
            'Max Drawdown': f"{div_metrics['max_drawdown']:.2%}"
        }
    })
    
    print("\n📊 Portfolio Strategy Comparison:")
    print(comparison)
    
    return comparison

if __name__ == "__main__":
    print("🚀 Multi-Symbol Portfolio Analysis System")
    print("=" * 50)
    
    # Run tech portfolio analysis
    analyzer, results = analyze_tech_portfolio()
    
    print("\n✅ Portfolio analysis complete!")
    print("📊 Dashboard saved to: outputs/plots/portfolio_dashboard.html")
    print("📋 Report saved to: outputs/reports/")
