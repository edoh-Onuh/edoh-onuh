# 📈 Custom Technical Indicators Library
# Proprietary and advanced technical indicators for enhanced analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.signal import argrelextrema
import warnings
warnings.filterwarnings('ignore')

class CustomIndicators:
    """
    Custom and proprietary technical indicators beyond standard TA
    """
    
    @staticmethod
    def momentum_acceleration(data, window=14):
        """
        Calculate momentum acceleration (rate of change of momentum)
        
        Args:
            data (pd.Series): Price data
            window (int): Lookback period
        
        Returns:
            pd.Series: Momentum acceleration values
        """
        momentum = data.pct_change(window)
        acceleration = momentum.diff()
        return acceleration
    
    @staticmethod
    def adaptive_moving_average(data, alpha_fast=0.2, alpha_slow=0.05):
        """
        Adaptive Moving Average that adjusts to market volatility
        
        Args:
            data (pd.Series): Price data
            alpha_fast (float): Fast smoothing factor
            alpha_slow (float): Slow smoothing factor
        
        Returns:
            pd.Series: Adaptive MA values
        """
        volatility = data.rolling(20).std()
        volatility_ratio = volatility / volatility.rolling(100).mean()
        
        # Adjust alpha based on volatility
        adaptive_alpha = alpha_slow + (alpha_fast - alpha_slow) * np.tanh(volatility_ratio - 1)
        
        ama = data.copy()
        for i in range(1, len(data)):
            if not np.isnan(adaptive_alpha.iloc[i]):
                ama.iloc[i] = ama.iloc[i-1] + adaptive_alpha.iloc[i] * (data.iloc[i] - ama.iloc[i-1])
        
        return ama
    
    @staticmethod
    def volume_price_trend_enhanced(high, low, close, volume, window=20):
        """
        Enhanced Volume Price Trend with momentum component
        
        Args:
            high, low, close (pd.Series): OHLC data
            volume (pd.Series): Volume data
            window (int): Smoothing window
        
        Returns:
            pd.Series: Enhanced VPT values
        """
        typical_price = (high + low + close) / 3
        price_change = typical_price.pct_change()
        
        # Volume-weighted price change
        vpt = (price_change * volume).cumsum()
        
        # Add momentum component
        vpt_momentum = vpt.diff(window)
        enhanced_vpt = vpt + 0.3 * vpt_momentum
        
        return enhanced_vpt.rolling(window).mean()
    
    @staticmethod
    def market_pressure_index(high, low, close, volume):
        """
        Custom Market Pressure Index combining price and volume dynamics
        
        Args:
            high, low, close (pd.Series): Price data
            volume (pd.Series): Volume data
        
        Returns:
            pd.Series: Market Pressure Index
        """
        # Price pressure component
        price_range = high - low
        close_position = (close - low) / price_range
        close_position = close_position.fillna(0.5)  # Neutral position for zero range
        
        # Volume pressure component
        volume_ma = volume.rolling(20).mean()
        volume_ratio = volume / volume_ma
        
        # Combine components
        pressure_index = (close_position - 0.5) * volume_ratio
        
        # Smooth the result
        return pressure_index.rolling(10).mean()
    
    @staticmethod
    def trend_strength_oscillator(data, short_window=10, long_window=30):
        """
        Measures the strength of the current trend
        
        Args:
            data (pd.Series): Price data
            short_window (int): Short-term window
            long_window (int): Long-term window
        
        Returns:
            pd.Series: Trend strength values (-1 to 1)
        """
        # Calculate multiple timeframe trends
        short_trend = data.rolling(short_window).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        long_trend = data.rolling(long_window).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        
        # Normalize trends
        short_trend_norm = short_trend / data.rolling(short_window).std()
        long_trend_norm = long_trend / data.rolling(long_window).std()
        
        # Combine trends with different weights
        trend_strength = 0.7 * short_trend_norm + 0.3 * long_trend_norm
        
        # Apply tanh to bound between -1 and 1
        return np.tanh(trend_strength)
    
    @staticmethod
    def volatility_breakout_indicator(data, window=20, threshold=2.0):
        """
        Identifies potential volatility breakouts
        
        Args:
            data (pd.Series): Price data
            window (int): Lookback window
            threshold (float): Breakout threshold
        
        Returns:
            pd.Series: Breakout signals (1=bullish, -1=bearish, 0=neutral)
        """
        # Calculate rolling volatility
        returns = data.pct_change()
        volatility = returns.rolling(window).std()
        vol_ma = volatility.rolling(window*2).mean()
        vol_ratio = volatility / vol_ma
        
        # Price momentum
        price_momentum = data.pct_change(5)
        
        # Breakout signals
        signals = pd.Series(0, index=data.index)
        signals[vol_ratio > threshold] = np.sign(price_momentum[vol_ratio > threshold])
        
        return signals
    
    @staticmethod
    def smart_money_indicator(high, low, close, volume, window=20):
        """
        Attempts to identify smart money activity
        
        Args:
            high, low, close (pd.Series): Price data
            volume (pd.Series): Volume data
            window (int): Analysis window
        
        Returns:
            pd.Series: Smart money indicator
        """
        # Price efficiency (how much price moved relative to range)
        price_range = high - low
        price_efficiency = abs(close - close.shift(1)) / price_range
        price_efficiency = price_efficiency.fillna(0)
        
        # Volume surge detection
        volume_ma = volume.rolling(window).mean()
        volume_surge = volume / volume_ma
        
        # Large move on low volume (potential smart money)
        smart_money_up = (price_efficiency > 0.7) & (volume_surge < 0.8) & (close > close.shift(1))
        smart_money_down = (price_efficiency > 0.7) & (volume_surge < 0.8) & (close < close.shift(1))
        
        # Create signal
        signals = pd.Series(0, index=close.index)
        signals[smart_money_up] = 1
        signals[smart_money_down] = -1
        
        # Smooth signals
        return signals.rolling(3).mean()
    
    @staticmethod
    def support_resistance_strength(data, window=20, min_touches=3):
        """
        Calculate support and resistance strength levels
        
        Args:
            data (pd.Series): Price data
            window (int): Analysis window
            min_touches (int): Minimum touches for valid level
        
        Returns:
            dict: Support and resistance levels with strength
        """
        # Find local maxima and minima
        highs_idx = argrelextrema(data.values, np.greater, order=window//2)[0]
        lows_idx = argrelextrema(data.values, np.less, order=window//2)[0]
        
        # Get resistance levels (highs)
        resistance_levels = []
        for idx in highs_idx:
            price = data.iloc[idx]
            # Count how many times price touched this level
            touches = sum(abs(data - price) < (price * 0.01))  # Within 1%
            if touches >= min_touches:
                resistance_levels.append({'price': price, 'strength': touches, 'type': 'resistance'})
        
        # Get support levels (lows)
        support_levels = []
        for idx in lows_idx:
            price = data.iloc[idx]
            touches = sum(abs(data - price) < (price * 0.01))  # Within 1%
            if touches >= min_touches:
                support_levels.append({'price': price, 'strength': touches, 'type': 'support'})
        
        return {
            'support': sorted(support_levels, key=lambda x: x['strength'], reverse=True),
            'resistance': sorted(resistance_levels, key=lambda x: x['strength'], reverse=True)
        }
    
    @staticmethod
    def liquidity_indicator(high, low, close, volume, window=20):
        """
        Measures market liquidity based on price impact per unit volume
        
        Args:
            high, low, close (pd.Series): Price data
            volume (pd.Series): Volume data
            window (int): Analysis window
        
        Returns:
            pd.Series: Liquidity indicator (higher = more liquid)
        """
        # Price impact per unit volume
        price_range = high - low
        volume_normalized = volume / volume.rolling(window).mean()
        
        # Low price range with high volume = high liquidity
        liquidity = volume_normalized / (price_range / close + 0.001)  # Avoid division by zero
        
        # Smooth and normalize
        liquidity_smooth = liquidity.rolling(window//2).mean()
        return (liquidity_smooth - liquidity_smooth.rolling(window*2).mean()) / liquidity_smooth.rolling(window*2).std()
    
    @staticmethod
    def institutional_activity_detector(open_price, high, low, close, volume):
        """
        Detects potential institutional activity patterns
        
        Args:
            open_price, high, low, close (pd.Series): OHLC data
            volume (pd.Series): Volume data
        
        Returns:
            pd.Series: Institutional activity signals
        """
        # Large volume with small price movement (accumulation/distribution)
        price_change = abs(close - open_price) / open_price
        volume_spike = volume / volume.rolling(20).mean()
        
        # Gap detection
        gap_up = (open_price > close.shift(1) * 1.02)
        gap_down = (open_price < close.shift(1) * 0.98)
        
        # Institutional signals
        accumulation = (volume_spike > 1.5) & (price_change < 0.02) & (close > open_price)
        distribution = (volume_spike > 1.5) & (price_change < 0.02) & (close < open_price)
        gap_fill = (gap_up & (low < close.shift(1))) | (gap_down & (high > close.shift(1)))
        
        signals = pd.Series(0, index=close.index)
        signals[accumulation] = 1
        signals[distribution] = -1
        signals[gap_fill] = 0.5 * np.sign(close - open_price)[gap_fill]
        
        return signals

class AdvancedPatterns:
    """
    Advanced pattern recognition beyond simple chart patterns
    """
    
    @staticmethod
    def dark_cloud_cover(open_price, high, low, close, threshold=0.5):
        """
        Detects Dark Cloud Cover bearish reversal pattern
        
        Args:
            open_price, high, low, close (pd.Series): OHLC data
            threshold (float): Minimum penetration into previous candle
        
        Returns:
            pd.Series: Pattern signals
        """
        # Previous candle conditions
        prev_bullish = (close.shift(1) > open_price.shift(1))
        prev_body_size = close.shift(1) - open_price.shift(1)
        
        # Current candle conditions
        current_bearish = (close < open_price)
        opens_above_prev_high = (open_price > high.shift(1))
        penetration = (close < (close.shift(1) - threshold * prev_body_size))
        
        pattern = prev_bullish & current_bearish & opens_above_prev_high & penetration
        
        return pattern.astype(int) * -1  # Bearish signal
    
    @staticmethod
    def piercing_pattern(open_price, high, low, close, threshold=0.5):
        """
        Detects Piercing Pattern bullish reversal pattern
        """
        # Previous candle conditions
        prev_bearish = (close.shift(1) < open_price.shift(1))
        prev_body_size = open_price.shift(1) - close.shift(1)
        
        # Current candle conditions
        current_bullish = (close > open_price)
        opens_below_prev_low = (open_price < low.shift(1))
        penetration = (close > (close.shift(1) + threshold * prev_body_size))
        
        pattern = prev_bearish & current_bullish & opens_below_prev_low & penetration
        
        return pattern.astype(int)  # Bullish signal
    
    @staticmethod
    def three_black_crows(open_price, high, low, close, min_body_ratio=0.6):
        """
        Detects Three Black Crows bearish pattern
        """
        # Check for three consecutive bearish candles
        bearish_1 = (close.shift(2) < open_price.shift(2))
        bearish_2 = (close.shift(1) < open_price.shift(1))
        bearish_3 = (close < open_price)
        
        # Check body sizes
        body_1 = open_price.shift(2) - close.shift(2)
        body_2 = open_price.shift(1) - close.shift(1)
        body_3 = open_price - close
        
        range_1 = high.shift(2) - low.shift(2)
        range_2 = high.shift(1) - low.shift(1)
        range_3 = high - low
        
        # Bodies should be significant portion of range
        significant_body_1 = (body_1 / range_1) > min_body_ratio
        significant_body_2 = (body_2 / range_2) > min_body_ratio
        significant_body_3 = (body_3 / range_3) > min_body_ratio
        
        # Each candle opens within previous body
        progressive_1 = (open_price.shift(1) < open_price.shift(2)) & (open_price.shift(1) > close.shift(2))
        progressive_2 = (open_price < open_price.shift(1)) & (open_price > close.shift(1))
        
        pattern = (bearish_1 & bearish_2 & bearish_3 & 
                  significant_body_1 & significant_body_2 & significant_body_3 &
                  progressive_1 & progressive_2)
        
        return pattern.astype(int) * -1  # Bearish signal

def apply_custom_indicators(df):
    """
    Apply all custom indicators to a DataFrame
    
    Args:
        df (pd.DataFrame): OHLC data with columns ['Open', 'High', 'Low', 'Close', 'Volume']
    
    Returns:
        pd.DataFrame: DataFrame with custom indicators added
    """
    print("🔧 Applying custom technical indicators...")
    
    # Initialize custom indicators
    custom = CustomIndicators()
    patterns = AdvancedPatterns()
    
    # Add custom indicators
    try:
        df['Momentum_Acceleration'] = custom.momentum_acceleration(df['Close'])
        print("  ✅ Momentum Acceleration calculated")
    except Exception as e:
        print(f"  ❌ Momentum Acceleration failed: {e}")
    
    try:
        df['Adaptive_MA'] = custom.adaptive_moving_average(df['Close'])
        print("  ✅ Adaptive Moving Average calculated")
    except Exception as e:
        print(f"  ❌ Adaptive MA failed: {e}")
    
    try:
        df['VPT_Enhanced'] = custom.volume_price_trend_enhanced(
            df['High'], df['Low'], df['Close'], df['Volume']
        )
        print("  ✅ Enhanced VPT calculated")
    except Exception as e:
        print(f"  ❌ Enhanced VPT failed: {e}")
    
    try:
        df['Market_Pressure'] = custom.market_pressure_index(
            df['High'], df['Low'], df['Close'], df['Volume']
        )
        print("  ✅ Market Pressure Index calculated")
    except Exception as e:
        print(f"  ❌ Market Pressure failed: {e}")
    
    try:
        df['Trend_Strength'] = custom.trend_strength_oscillator(df['Close'])
        print("  ✅ Trend Strength Oscillator calculated")
    except Exception as e:
        print(f"  ❌ Trend Strength failed: {e}")
    
    try:
        df['Volatility_Breakout'] = custom.volatility_breakout_indicator(df['Close'])
        print("  ✅ Volatility Breakout Indicator calculated")
    except Exception as e:
        print(f"  ❌ Volatility Breakout failed: {e}")
    
    try:
        df['Smart_Money'] = custom.smart_money_indicator(
            df['High'], df['Low'], df['Close'], df['Volume']
        )
        print("  ✅ Smart Money Indicator calculated")
    except Exception as e:
        print(f"  ❌ Smart Money failed: {e}")
    
    try:
        df['Liquidity'] = custom.liquidity_indicator(
            df['High'], df['Low'], df['Close'], df['Volume']
        )
        print("  ✅ Liquidity Indicator calculated")
    except Exception as e:
        print(f"  ❌ Liquidity Indicator failed: {e}")
    
    try:
        df['Institutional_Activity'] = custom.institutional_activity_detector(
            df['Open'], df['High'], df['Low'], df['Close'], df['Volume']
        )
        print("  ✅ Institutional Activity Detector calculated")
    except Exception as e:
        print(f"  ❌ Institutional Activity failed: {e}")
    
    # Add advanced patterns
    try:
        df['Dark_Cloud_Cover'] = patterns.dark_cloud_cover(
            df['Open'], df['High'], df['Low'], df['Close']
        )
        print("  ✅ Dark Cloud Cover pattern calculated")
    except Exception as e:
        print(f"  ❌ Dark Cloud Cover failed: {e}")
    
    try:
        df['Piercing_Pattern'] = patterns.piercing_pattern(
            df['Open'], df['High'], df['Low'], df['Close']
        )
        print("  ✅ Piercing Pattern calculated")
    except Exception as e:
        print(f"  ❌ Piercing Pattern failed: {e}")
    
    try:
        df['Three_Black_Crows'] = patterns.three_black_crows(
            df['Open'], df['High'], df['Low'], df['Close']
        )
        print("  ✅ Three Black Crows pattern calculated")
    except Exception as e:
        print(f"  ❌ Three Black Crows failed: {e}")
    
    print("🎉 Custom indicators application complete!")
    return df

def visualize_custom_indicators(df, symbol='TSLA'):
    """
    Create visualizations for custom indicators
    
    Args:
        df (pd.DataFrame): DataFrame with custom indicators
        symbol (str): Stock symbol for title
    """
    print(f"📊 Creating custom indicators visualization for {symbol}...")
    
    # Create subplots
    fig, axes = plt.subplots(4, 2, figsize=(16, 20))
    fig.suptitle(f'{symbol} - Custom Technical Indicators Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Price with Adaptive MA
    axes[0, 0].plot(df.index, df['Close'], label='Close Price', alpha=0.7)
    if 'Adaptive_MA' in df.columns:
        axes[0, 0].plot(df.index, df['Adaptive_MA'], label='Adaptive MA', linewidth=2)
    axes[0, 0].set_title('Price with Adaptive Moving Average')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Momentum Acceleration
    if 'Momentum_Acceleration' in df.columns:
        axes[0, 1].plot(df.index, df['Momentum_Acceleration'], color='purple')
        axes[0, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[0, 1].set_title('Momentum Acceleration')
        axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Market Pressure Index
    if 'Market_Pressure' in df.columns:
        axes[1, 0].plot(df.index, df['Market_Pressure'], color='orange')
        axes[1, 0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[1, 0].set_title('Market Pressure Index')
        axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Trend Strength Oscillator
    if 'Trend_Strength' in df.columns:
        axes[1, 1].plot(df.index, df['Trend_Strength'], color='green')
        axes[1, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[1, 1].axhline(y=0.5, color='red', linestyle=':', alpha=0.5)
        axes[1, 1].axhline(y=-0.5, color='red', linestyle=':', alpha=0.5)
        axes[1, 1].set_title('Trend Strength Oscillator')
        axes[1, 1].grid(True, alpha=0.3)
    
    # 5. Smart Money Indicator
    if 'Smart_Money' in df.columns:
        axes[2, 0].plot(df.index, df['Smart_Money'], color='blue')
        axes[2, 0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[2, 0].set_title('Smart Money Indicator')
        axes[2, 0].grid(True, alpha=0.3)
    
    # 6. Liquidity Indicator
    if 'Liquidity' in df.columns:
        axes[2, 1].plot(df.index, df['Liquidity'], color='cyan')
        axes[2, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[2, 1].set_title('Liquidity Indicator')
        axes[2, 1].grid(True, alpha=0.3)
    
    # 7. Volatility Breakout Signals
    if 'Volatility_Breakout' in df.columns:
        breakout_signals = df['Volatility_Breakout']
        axes[3, 0].scatter(df.index[breakout_signals == 1], df['Close'][breakout_signals == 1], 
                          color='green', marker='^', s=50, label='Bullish Breakout')
        axes[3, 0].scatter(df.index[breakout_signals == -1], df['Close'][breakout_signals == -1], 
                          color='red', marker='v', s=50, label='Bearish Breakout')
        axes[3, 0].plot(df.index, df['Close'], alpha=0.5, color='gray')
        axes[3, 0].set_title('Volatility Breakout Signals')
        axes[3, 0].legend()
        axes[3, 0].grid(True, alpha=0.3)
    
    # 8. Pattern Signals
    pattern_signals = pd.Series(0, index=df.index)
    if 'Dark_Cloud_Cover' in df.columns:
        pattern_signals += df['Dark_Cloud_Cover']
    if 'Piercing_Pattern' in df.columns:
        pattern_signals += df['Piercing_Pattern']
    if 'Three_Black_Crows' in df.columns:
        pattern_signals += df['Three_Black_Crows']
    
    axes[3, 1].plot(df.index, df['Close'], alpha=0.7, color='black', label='Close Price')
    
    # Mark pattern signals
    bullish_patterns = pattern_signals > 0
    bearish_patterns = pattern_signals < 0
    
    axes[3, 1].scatter(df.index[bullish_patterns], df['Close'][bullish_patterns], 
                      color='green', marker='^', s=100, label='Bullish Patterns', alpha=0.7)
    axes[3, 1].scatter(df.index[bearish_patterns], df['Close'][bearish_patterns], 
                      color='red', marker='v', s=100, label='Bearish Patterns', alpha=0.7)
    
    axes[3, 1].set_title('Chart Pattern Signals')
    axes[3, 1].legend()
    axes[3, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'outputs/plots/custom_indicators_{symbol}.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"✅ Custom indicators visualization saved to outputs/plots/custom_indicators_{symbol}.png")

if __name__ == "__main__":
    print("🔧 Custom Technical Indicators Library")
    print("=" * 50)
    print("This library provides advanced proprietary indicators beyond standard TA")
    print("Available indicators:")
    print("- Momentum Acceleration")
    print("- Adaptive Moving Average")
    print("- Enhanced Volume Price Trend")
    print("- Market Pressure Index")
    print("- Trend Strength Oscillator")
    print("- Volatility Breakout Indicator")
    print("- Smart Money Indicator")
    print("- Liquidity Indicator")
    print("- Institutional Activity Detector")
    print("- Advanced Chart Patterns")
