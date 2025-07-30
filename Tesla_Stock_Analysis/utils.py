# Tesla Stock Analysis - Utility Functions
# Advanced utility functions for enhanced analysis

import numpy as np
import pandas as pd
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataValidator:
    """
    Validate and clean stock data
    """
    
    @staticmethod
    def validate_data_quality(df, symbol='TSLA'):
        """
        Validate data quality and identify issues
        """
        issues = []
        
        try:
            # Check for missing data
            missing_percentage = df.isnull().sum().sum() / (len(df) * len(df.columns))
            if missing_percentage > 0.05:  # 5% threshold
                issues.append(f"High missing data: {missing_percentage:.2%}")
            
            # Check for outliers
            if 'Close' in df.columns:
                daily_returns = df['Close'].pct_change().dropna()
                extreme_moves = abs(daily_returns) > 0.5  # 50% daily moves
                if extreme_moves.any():
                    issues.append(f"Extreme price movements detected: {extreme_moves.sum()} days")
            
            # Check for volume anomalies
            if 'Volume' in df.columns:
                zero_volume_days = (df['Volume'] == 0).sum()
                if zero_volume_days > 0:
                    issues.append(f"Zero volume days: {zero_volume_days}")
            
            # Check data continuity
            if len(df) < 100:
                issues.append(f"Insufficient data points: {len(df)}")
            
            logger.info(f"Data validation completed for {symbol}")
            return issues
            
        except Exception as e:
            logger.error(f"Error during data validation: {e}")
            return [f"Validation error: {str(e)}"]
    
    @staticmethod
    def clean_data(df):
        """
        Clean and prepare data for analysis
        """
        try:
            # Remove rows with all NaN values
            df = df.dropna(how='all')
            
            # Forward fill missing values (conservative approach)
            df = df.fillna(method='ffill')
            
            # Remove obvious outliers (prices that are too extreme)
            if 'Close' in df.columns:
                # Remove prices that are more than 10 standard deviations from mean
                mean_price = df['Close'].mean()
                std_price = df['Close'].std()
                outlier_threshold = 10 * std_price
                
                mask = abs(df['Close'] - mean_price) <= outlier_threshold
                df = df[mask]
            
            # Ensure positive prices and volumes
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = df[col].abs()
            
            logger.info(f"Data cleaning completed. Final shape: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Error during data cleaning: {e}")
            return df

class AlertSystem:
    """
    Alert system for price movements and technical signals
    """
    
    def __init__(self, email_config=None):
        self.email_config = email_config
    
    def check_price_alerts(self, current_data, previous_data=None):
        """
        Check for price alert conditions
        """
        alerts = []
        
        try:
            if previous_data is not None and len(current_data) > 0:
                current_price = current_data['Close'].iloc[-1]
                previous_price = previous_data['Close'].iloc[-1]
                
                # Price movement alert
                price_change = (current_price - previous_price) / previous_price
                if abs(price_change) > 0.05:  # 5% movement
                    direction = "up" if price_change > 0 else "down"
                    alerts.append({
                        'type': 'price_movement',
                        'message': f"TSLA moved {direction} by {abs(price_change):.2%}",
                        'severity': 'high' if abs(price_change) > 0.1 else 'medium'
                    })
                
                # Volume spike alert
                if 'Volume' in current_data.columns and len(current_data) > 20:
                    current_volume = current_data['Volume'].iloc[-1]
                    avg_volume = current_data['Volume'].tail(20).mean()
                    
                    if current_volume > avg_volume * 2:  # 2x average volume
                        alerts.append({
                            'type': 'volume_spike',
                            'message': f"Volume spike detected: {current_volume:,.0f} (avg: {avg_volume:,.0f})",
                            'severity': 'medium'
                        })
            
            # Technical indicator alerts
            if 'RSI' in current_data.columns and len(current_data) > 0:
                current_rsi = current_data['RSI'].iloc[-1]
                
                if current_rsi > 70:
                    alerts.append({
                        'type': 'technical',
                        'message': f"RSI overbought: {current_rsi:.1f}",
                        'severity': 'low'
                    })
                elif current_rsi < 30:
                    alerts.append({
                        'type': 'technical',
                        'message': f"RSI oversold: {current_rsi:.1f}",
                        'severity': 'low'
                    })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
            return []
    
    def send_email_alert(self, alerts):
        """
        Send email alerts (if configured)
        """
        if not self.email_config or not alerts:
            return False
        
        try:
            # Prepare email content
            subject = f"Tesla Stock Alert - {len(alerts)} Alert(s)"
            body = "Tesla Stock Analysis Alerts:\n\n"
            
            for alert in alerts:
                body += f"• {alert['message']} (Severity: {alert['severity']})\n"
            
            body += f"\nGenerated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email_user']
            msg['To'] = self.email_config['recipient_email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['email_user'], self.email_config['email_password'])
                text = msg.as_string()
                server.sendmail(self.email_config['email_user'], self.email_config['recipient_email'], text)
            
            logger.info(f"Email alert sent successfully to {self.email_config['recipient_email']}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")
            return False

class PerformanceTracker:
    """
    Track and analyze performance metrics
    """
    
    def __init__(self, benchmark_symbol='SPY'):
        self.benchmark_symbol = benchmark_symbol
    
    def calculate_performance_metrics(self, df, benchmark_df=None):
        """
        Calculate comprehensive performance metrics
        """
        try:
            metrics = {}
            
            # Basic returns
            returns = df['Close'].pct_change().dropna()
            
            # Performance metrics
            metrics['total_return'] = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1)
            metrics['annualized_return'] = (1 + metrics['total_return']) ** (252 / len(df)) - 1
            metrics['volatility'] = returns.std() * np.sqrt(252)
            
            # Risk-adjusted metrics
            risk_free_rate = 0.02  # 2% annual
            excess_returns = returns.mean() * 252 - risk_free_rate
            metrics['sharpe_ratio'] = excess_returns / metrics['volatility'] if metrics['volatility'] > 0 else 0
            
            # Drawdown analysis
            cumulative_returns = (1 + returns).cumprod()
            rolling_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - rolling_max) / rolling_max
            metrics['max_drawdown'] = drawdown.min()
            
            # Win/Loss analysis
            positive_days = (returns > 0).sum()
            total_days = len(returns)
            metrics['win_rate'] = positive_days / total_days if total_days > 0 else 0
            
            # Additional metrics
            metrics['avg_positive_return'] = returns[returns > 0].mean() if (returns > 0).any() else 0
            metrics['avg_negative_return'] = returns[returns < 0].mean() if (returns < 0).any() else 0
            
            # Benchmark comparison (if provided)
            if benchmark_df is not None:
                benchmark_returns = benchmark_df['Close'].pct_change().dropna()
                benchmark_total_return = (benchmark_df['Close'].iloc[-1] / benchmark_df['Close'].iloc[0] - 1)
                
                metrics['alpha'] = metrics['total_return'] - benchmark_total_return
                
                # Beta calculation
                if len(returns) == len(benchmark_returns):
                    covariance = np.cov(returns, benchmark_returns)[0][1]
                    benchmark_variance = benchmark_returns.var()
                    metrics['beta'] = covariance / benchmark_variance if benchmark_variance > 0 else 0
            
            logger.info("Performance metrics calculated successfully")
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {}

class DataExporter:
    """
    Export data and results in various formats
    """
    
    @staticmethod
    def export_to_csv(data, filename, directory="data"):
        """
        Export data to CSV format
        """
        try:
            os.makedirs(directory, exist_ok=True)
            filepath = os.path.join(directory, filename)
            
            if isinstance(data, pd.DataFrame):
                data.to_csv(filepath, index=True)
            elif isinstance(data, dict):
                pd.DataFrame([data]).to_csv(filepath, index=False)
            else:
                raise ValueError("Data must be DataFrame or dictionary")
            
            logger.info(f"Data exported to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return None
    
    @staticmethod
    def export_to_json(data, filename, directory="data"):
        """
        Export data to JSON format
        """
        try:
            os.makedirs(directory, exist_ok=True)
            filepath = os.path.join(directory, filename)
            
            if isinstance(data, pd.DataFrame):
                data.to_json(filepath, orient='records', date_format='iso')
            elif isinstance(data, dict):
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            else:
                raise ValueError("Data must be DataFrame or dictionary")
            
            logger.info(f"Data exported to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return None
    
    @staticmethod
    def create_backup(source_directory, backup_directory=None):
        """
        Create backup of analysis results
        """
        try:
            if backup_directory is None:
                backup_directory = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            os.makedirs(backup_directory, exist_ok=True)
            
            # Copy important files
            import shutil
            
            for root, dirs, files in os.walk(source_directory):
                for file in files:
                    if file.endswith(('.csv', '.json', '.png', '.html')):
                        source_path = os.path.join(root, file)
                        relative_path = os.path.relpath(source_path, source_directory)
                        dest_path = os.path.join(backup_directory, relative_path)
                        
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy2(source_path, dest_path)
            
            logger.info(f"Backup created at {backup_directory}")
            return backup_directory
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

# Utility functions
def format_currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"

def format_percentage(value):
    """Format value as percentage"""
    return f"{value:.2%}"

def calculate_trading_days(start_date, end_date):
    """Calculate number of trading days between dates"""
    business_days = pd.bdate_range(start_date, end_date)
    return len(business_days)

def get_market_hours():
    """Get current market hours status"""
    now = datetime.now()
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    is_weekday = now.weekday() < 5  # Monday = 0, Sunday = 6
    is_market_hours = market_open <= now <= market_close
    
    return {
        'is_open': is_weekday and is_market_hours,
        'next_open': market_open if now < market_open else market_open + timedelta(days=1),
        'next_close': market_close if now < market_close else market_close + timedelta(days=1)
    }

logger.info("Utility functions loaded successfully")
