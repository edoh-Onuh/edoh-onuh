# Tesla Stock Analysis - Real-time Data & Automation
# Advanced features for real-time monitoring and automated analysis

import schedule
import time
import threading
import websocket
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from utils import AlertSystem, DataValidator, PerformanceTracker
import logging

logger = logging.getLogger(__name__)

class RealTimeDataFeed:
    """
    Real-time data feed for live market data
    """
    
    def __init__(self, symbol='TSLA', callback=None):
        self.symbol = symbol
        self.callback = callback
        self.ws = None
        self.is_connected = False
        self.latest_data = {}
    
    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            # Process the data based on the API format
            if 'data' in data:
                self.latest_data = {
                    'symbol': data.get('symbol', self.symbol),
                    'price': float(data['data'].get('price', 0)),
                    'volume': int(data['data'].get('volume', 0)),
                    'timestamp': datetime.now(),
                    'change': float(data['data'].get('change', 0)),
                    'change_percent': float(data['data'].get('change_percent', 0))
                }
                
                if self.callback:
                    self.callback(self.latest_data)
                    
                logger.info(f"Real-time data received: {self.symbol} - ${self.latest_data['price']:.2f}")
        
        except Exception as e:
            logger.error(f"Error processing real-time data: {e}")
    
    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        logger.error(f"WebSocket error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close"""
        self.is_connected = False
        logger.info("WebSocket connection closed")
    
    def on_open(self, ws):
        """Handle WebSocket open"""
        self.is_connected = True
        logger.info(f"WebSocket connected for {self.symbol}")
        
        # Subscribe to the symbol
        subscribe_message = {
            "action": "subscribe",
            "symbols": [self.symbol]
        }
        ws.send(json.dumps(subscribe_message))
    
    def start_real_time_feed(self, ws_url="wss://ws.finnhub.io"):
        """Start real-time data feed"""
        try:
            # Note: This is a placeholder - you'd need actual WebSocket URL and API key
            # For demo purposes, we'll simulate real-time data
            logger.warning("Real-time feed is simulated - replace with actual WebSocket URL")
            self.simulate_real_time_data()
            
        except Exception as e:
            logger.error(f"Error starting real-time feed: {e}")
    
    def simulate_real_time_data(self):
        """Simulate real-time data for demonstration"""
        import random
        
        base_price = 250.0  # Tesla base price for simulation
        
        def generate_data():
            while True:
                # Simulate price movement
                change = random.uniform(-0.02, 0.02)  # ±2% change
                base_price *= (1 + change)
                
                self.latest_data = {
                    'symbol': self.symbol,
                    'price': base_price,
                    'volume': random.randint(100000, 1000000),
                    'timestamp': datetime.now(),
                    'change': change * base_price,
                    'change_percent': change * 100
                }
                
                if self.callback:
                    self.callback(self.latest_data)
                
                time.sleep(5)  # Update every 5 seconds
        
        # Run in separate thread
        thread = threading.Thread(target=generate_data, daemon=True)
        thread.start()
        self.is_connected = True

class AutomatedAnalysis:
    """
    Automated analysis scheduler
    """
    
    def __init__(self, symbol='TSLA'):
        self.symbol = symbol
        self.alert_system = AlertSystem()
        self.validator = DataValidator()
        self.performance_tracker = PerformanceTracker()
        self.last_analysis_time = None
        self.historical_data = None
    
    def run_daily_analysis(self):
        """Run daily automated analysis"""
        try:
            logger.info(f"Starting daily analysis for {self.symbol}")
            
            # Fetch latest data
            import yfinance as yf
            ticker = yf.Ticker(self.symbol)
            
            # Get last 30 days of data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            current_data = ticker.history(start=start_date, end=end_date)
            
            if current_data.empty:
                logger.warning("No data available for analysis")
                return
            
            # Validate data quality
            issues = self.validator.validate_data_quality(current_data, self.symbol)
            if issues:
                logger.warning(f"Data quality issues: {issues}")
            
            # Clean data
            current_data = self.validator.clean_data(current_data)
            
            # Check for alerts
            alerts = self.alert_system.check_price_alerts(current_data, self.historical_data)
            
            if alerts:
                logger.info(f"Generated {len(alerts)} alerts")
                # Send alerts if configured
                self.alert_system.send_email_alert(alerts)
                
                # Print alerts to console
                for alert in alerts:
                    print(f"🚨 ALERT: {alert['message']}")
            
            # Calculate performance metrics
            performance = self.performance_tracker.calculate_performance_metrics(current_data)
            logger.info(f"Performance calculated: {performance.get('total_return', 0):.2%} total return")
            
            # Save analysis results
            analysis_results = {
                'timestamp': datetime.now().isoformat(),
                'symbol': self.symbol,
                'current_price': float(current_data['Close'].iloc[-1]),
                'alerts': alerts,
                'performance': performance,
                'data_points': len(current_data)
            }
            
            # Export results
            from utils import DataExporter
            DataExporter.export_to_json(
                analysis_results, 
                f"daily_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                "outputs/daily_reports"
            )
            
            # Update historical data
            self.historical_data = current_data
            self.last_analysis_time = datetime.now()
            
            logger.info("Daily analysis completed successfully")
            
        except Exception as e:
            logger.error(f"Error in daily analysis: {e}")
    
    def run_hourly_check(self):
        """Run hourly market check"""
        try:
            from utils import get_market_hours
            market_status = get_market_hours()
            
            if not market_status['is_open']:
                logger.info("Market is closed - skipping hourly check")
                return
            
            logger.info("Running hourly market check")
            
            # Quick data fetch for alerts only
            import yfinance as yf
            ticker = yf.Ticker(self.symbol)
            
            # Get last 2 days for comparison
            current_data = ticker.history(period="2d")
            
            if len(current_data) >= 2:
                # Check for immediate alerts
                alerts = self.alert_system.check_price_alerts(current_data)
                
                if alerts:
                    high_priority_alerts = [a for a in alerts if a['severity'] == 'high']
                    if high_priority_alerts:
                        logger.warning(f"High priority alerts detected: {len(high_priority_alerts)}")
                        # Send immediate notifications for high priority alerts
                        self.alert_system.send_email_alert(high_priority_alerts)
            
        except Exception as e:
            logger.error(f"Error in hourly check: {e}")
    
    def schedule_tasks(self):
        """Schedule automated tasks"""
        try:
            # Schedule daily analysis at market close (4:30 PM)
            schedule.every().day.at("16:30").do(self.run_daily_analysis)
            
            # Schedule hourly checks during market hours
            for hour in range(9, 17):  # 9 AM to 4 PM
                schedule.every().day.at(f"{hour:02d}:00").do(self.run_hourly_check)
            
            # Schedule weekend summary (Saturday at 9 AM)
            schedule.every().saturday.at("09:00").do(self.generate_weekly_summary)
            
            logger.info("Automated tasks scheduled successfully")
            
        except Exception as e:
            logger.error(f"Error scheduling tasks: {e}")
    
    def generate_weekly_summary(self):
        """Generate weekly summary report"""
        try:
            logger.info("Generating weekly summary")
            
            # Get week's data
            import yfinance as yf
            ticker = yf.Ticker(self.symbol)
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            week_data = ticker.history(start=start_date, end=end_date)
            
            if week_data.empty:
                logger.warning("No weekly data available")
                return
            
            # Calculate weekly metrics
            weekly_return = (week_data['Close'].iloc[-1] / week_data['Close'].iloc[0] - 1)
            avg_volume = week_data['Volume'].mean()
            volatility = week_data['Close'].pct_change().std()
            
            summary = {
                'week_ending': end_date.strftime('%Y-%m-%d'),
                'symbol': self.symbol,
                'weekly_return': weekly_return,
                'avg_volume': avg_volume,
                'volatility': volatility,
                'high_price': week_data['High'].max(),
                'low_price': week_data['Low'].min(),
                'trading_days': len(week_data)
            }
            
            # Export weekly summary
            from utils import DataExporter
            DataExporter.export_to_json(
                summary,
                f"weekly_summary_{end_date.strftime('%Y%m%d')}.json",
                "outputs/weekly_reports"
            )
            
            logger.info(f"Weekly summary generated: {weekly_return:.2%} return")
            
        except Exception as e:
            logger.error(f"Error generating weekly summary: {e}")
    
    def start_automation(self):
        """Start the automation system"""
        try:
            logger.info("Starting automation system...")
            
            # Schedule tasks
            self.schedule_tasks()
            
            # Run initial analysis
            self.run_daily_analysis()
            
            # Start scheduler loop
            def run_scheduler():
                while True:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
            
            # Run scheduler in separate thread
            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()
            
            logger.info("Automation system started successfully")
            
        except Exception as e:
            logger.error(f"Error starting automation: {e}")

class LiveDashboard:
    """
    Live dashboard for real-time monitoring
    """
    
    def __init__(self, symbol='TSLA'):
        self.symbol = symbol
        self.real_time_feed = None
        self.dashboard_data = {
            'prices': [],
            'volumes': [],
            'timestamps': [],
            'alerts': []
        }
    
    def update_dashboard(self, data):
        """Update dashboard with new data"""
        try:
            # Store recent data (last 100 points)
            self.dashboard_data['prices'].append(data['price'])
            self.dashboard_data['volumes'].append(data['volume'])
            self.dashboard_data['timestamps'].append(data['timestamp'])
            
            # Keep only recent data
            max_points = 100
            for key in ['prices', 'volumes', 'timestamps']:
                if len(self.dashboard_data[key]) > max_points:
                    self.dashboard_data[key] = self.dashboard_data[key][-max_points:]
            
            # Generate live chart (placeholder)
            self.create_live_chart()
            
        except Exception as e:
            logger.error(f"Error updating dashboard: {e}")
    
    def create_live_chart(self):
        """Create live chart with current data"""
        try:
            # This would create a live updating chart
            # For demonstration, we'll just log the current status
            if self.dashboard_data['prices']:
                current_price = self.dashboard_data['prices'][-1]
                price_change = (current_price - self.dashboard_data['prices'][0]) / self.dashboard_data['prices'][0] * 100
                
                logger.info(f"Live Update - {self.symbol}: ${current_price:.2f} ({price_change:+.2f}%)")
        
        except Exception as e:
            logger.error(f"Error creating live chart: {e}")
    
    def start_live_monitoring(self):
        """Start live monitoring dashboard"""
        try:
            logger.info("Starting live dashboard...")
            
            # Initialize real-time feed
            self.real_time_feed = RealTimeDataFeed(self.symbol, self.update_dashboard)
            self.real_time_feed.start_real_time_feed()
            
            logger.info("Live dashboard started successfully")
            
        except Exception as e:
            logger.error(f"Error starting live dashboard: {e}")

# Example usage functions
def setup_automated_analysis(symbol='TSLA'):
    """Setup and start automated analysis"""
    automation = AutomatedAnalysis(symbol)
    automation.start_automation()
    return automation

def setup_live_dashboard(symbol='TSLA'):
    """Setup and start live dashboard"""
    dashboard = LiveDashboard(symbol)
    dashboard.start_live_monitoring()
    return dashboard

def run_comprehensive_automation(symbol='TSLA'):
    """Run complete automation suite"""
    logger.info(f"Starting comprehensive automation for {symbol}")
    
    # Start automated analysis
    automation = setup_automated_analysis(symbol)
    
    # Start live dashboard
    dashboard = setup_live_dashboard(symbol)
    
    logger.info("Comprehensive automation suite started")
    
    return {
        'automation': automation,
        'dashboard': dashboard
    }

logger.info("Real-time automation module loaded successfully")
