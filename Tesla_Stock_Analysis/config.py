# Tesla Stock Analysis - Configuration Settings
# Advanced configuration for enhanced features

import os
from datetime import datetime, timedelta

# === ANALYSIS SETTINGS ===
DEFAULT_SYMBOL = 'TSLA'
DEFAULT_START_DATE = '2010-01-01'
DEFAULT_END_DATE = datetime.now().strftime('%Y-%m-%d')

# Technical Analysis Parameters
MA_PERIODS = [20, 50, 200]  # Moving average periods
RSI_PERIOD = 14
MACD_PERIODS = (12, 26, 9)  # Fast, slow, signal
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

# Advanced Indicators
STOCH_PERIOD = 14
WILLIAMS_R_PERIOD = 14
CCI_PERIOD = 20
ATR_PERIOD = 14

# === MACHINE LEARNING SETTINGS ===
LSTM_SEQUENCE_LENGTH = 60
LSTM_EPOCHS = 50
LSTM_BATCH_SIZE = 32
TRAIN_TEST_SPLIT = 0.8

# Prediction settings
PREDICTION_DAYS = 30
MODEL_SAVE_PATH = "data/models"

# === RISK MANAGEMENT SETTINGS ===
RISK_FREE_RATE = 0.02  # 2% annual risk-free rate
DEFAULT_RISK_PER_TRADE = 0.02  # 2% risk per trade
DEFAULT_ACCOUNT_BALANCE = 10000  # $10,000 default account

# VaR Confidence Levels
VAR_CONFIDENCE_LEVELS = [0.95, 0.99]

# === DATABASE SETTINGS ===
DATABASE_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'database': os.getenv('MYSQL_DATABASE', 'tesla_analysis'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'port': int(os.getenv('MYSQL_PORT', '3306')),
}

# === FILE PATHS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(BASE_DIR, "outputs", "plots")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")
MODELS_DIR = os.path.join(BASE_DIR, "outputs", "models")

# Ensure directories exist
for directory in [DATA_DIR, PLOTS_DIR, REPORTS_DIR, MODELS_DIR]:
    os.makedirs(directory, exist_ok=True)

# === VISUALIZATION SETTINGS ===
PLOT_STYLE = 'whitegrid'
FIGURE_SIZE = (15, 8)
DPI = 150
FONT_SIZE = 12

# Plot colors
COLORS = {
    'price': '#1f77b4',
    'sma': '#ff7f0e',
    'ema': '#2ca02c',
    'volume': '#d62728',
    'rsi': '#9467bd',
    'macd': '#8c564b',
    'bollinger': '#e377c2',
    'support': '#7f7f7f',
    'resistance': '#bcbd22'
}

# === API SETTINGS ===
YFINANCE_RETRY_ATTEMPTS = 3
YFINANCE_RETRY_DELAY = 120  # seconds

# Rate limiting
API_RATE_LIMIT_DELAY = 1  # seconds between API calls

# === ALERT SETTINGS ===
PRICE_ALERT_THRESHOLDS = {
    'major_move': 0.05,  # 5% price movement
    'volume_spike': 2.0,  # 2x average volume
    'rsi_overbought': 70,
    'rsi_oversold': 30
}

# Email settings (if implementing email alerts)
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'email_user': os.getenv('EMAIL_USER', ''),
    'email_password': os.getenv('EMAIL_PASSWORD', ''),
    'recipient_email': os.getenv('RECIPIENT_EMAIL', '')
}

# === REPORT SETTINGS ===
REPORT_TEMPLATE_PATH = "templates/report_template.html"
REPORT_LOGO_PATH = "assets/logo.png"

# Report sections to include
REPORT_SECTIONS = [
    'executive_summary',
    'technical_analysis',
    'risk_analysis',
    'ml_predictions',
    'recommendations'
]

# === LOGGING SETTINGS ===
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'tesla_analysis.log')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# === FEATURE FLAGS ===
FEATURES = {
    'enable_ml_predictions': True,
    'enable_risk_analysis': True,
    'enable_database_storage': True,
    'enable_automated_reports': True,
    'enable_email_alerts': False,  # Disabled by default
    'enable_real_time_data': False,  # Future feature
    'enable_sentiment_analysis': False  # Future feature
}

# === PERFORMANCE SETTINGS ===
CACHE_DURATION_HOURS = 1  # Cache data for 1 hour
MAX_MEMORY_USAGE_MB = 1024  # 1GB memory limit
PARALLEL_PROCESSING = True

# === VALIDATION SETTINGS ===
MIN_DATA_POINTS = 100  # Minimum data points for analysis
MAX_DATA_POINTS = 10000  # Maximum data points to prevent memory issues

# Data quality thresholds
DATA_QUALITY_THRESHOLDS = {
    'max_missing_percentage': 0.05,  # 5% missing data allowed
    'min_volume_threshold': 1000,  # Minimum daily volume
    'max_price_change_percentage': 0.5  # 50% max daily change (outlier detection)
}

print("✅ Configuration loaded successfully")
