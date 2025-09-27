#!/usr/bin/env python3
"""
Intertemporal Differentials Analysis for CV Modeling and Parody Detection

This module implements the IntertemporalAnalyzer class for performing
intertemporal differential analysis with cross-validation modeling
and parody detection as specified in the OpenAI-DeepSeek AI ChatGPT
collaboration transparency project.

Hash Reference: 277828ff6bf7804a83d2e307eafcaa09
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import warnings
from pathlib import Path
import sys

# Add ACTNEWWORLDODOR to path for COMBSEC integration
current_dir = Path(__file__).parent
actnewworld_dir = current_dir / "ACTNEWWORLDODOR"
sys.path.insert(0, str(actnewworld_dir))

try:
    from emoji_combsec_generator import EmojiCombsecGenerator
    COMBSEC_AVAILABLE = True
except ImportError:
    COMBSEC_AVAILABLE = False
    warnings.warn("COMBSEC integration not available", UserWarning)

# Conditional imports for optional dependencies
try:
    from sklearn.model_selection import TimeSeriesSplit, train_test_split
    from sklearn.metrics import mean_squared_error, accuracy_score
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("scikit-learn not available, limited functionality", UserWarning)

try:
    import statsmodels.api as sm
    from statsmodels.tsa.stattools import adfuller
    from statsmodels.stats.diagnostic import het_breuschpagan
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    warnings.warn("statsmodels not available, limited functionality", UserWarning)


class IntertemporalAnalyzer:
    """
    Intertemporal differential analysis with CV modeling and parody detection
    
    This class provides comprehensive temporal analysis capabilities including:
    - Time-series cross-validation
    - Expanding window CV
    - Blocked time series CV
    - Parody detection through sentiment analysis
    - COMBSEC security integration
    """
    
    def __init__(self, security_key: Optional[str] = None, firm_id: str = "YOURFIRM"):
        """
        Initialize the IntertemporalAnalyzer with COMBSEC security context
        
        Args:
            security_key: Optional COMBSEC key for authentication
            firm_id: Firm identifier for COMBSEC integration
        """
        self.firm_id = firm_id
        self.security_key = security_key
        self.combsec_generator = None
        
        # Initialize COMBSEC if available
        if COMBSEC_AVAILABLE:
            self.combsec_generator = EmojiCombsecGenerator(firm_id)
            if not security_key:
                self.security_key = self.combsec_generator.generate_combsec_key()
        
        # Initialize analysis parameters
        self.cv_results = {}
        self.parody_markers = [
            '#parody', '#satire', '#fake', '#mock', '#joke', '#humor',
            'parody', 'satire', 'fake', 'mock', 'joke', 'not real'
        ]
        
        print(f"🌐 IntertemporalAnalyzer initialized")
        if self.security_key:
            print(f"🔐 COMBSEC Security: {self.security_key[:20]}...")
    
    def analyze_temporal_diffs(self, 
                             data: Union[pd.DataFrame, Dict],
                             cv_method: str = 'time_series',
                             parody_detection: bool = True,
                             target_column: Optional[str] = None,
                             **kwargs) -> Dict[str, Any]:
        """
        Perform intertemporal differential analysis with CV and parody detection
        
        Args:
            data: Input data (DataFrame or dict)
            cv_method: CV method ('time_series', 'expanding_window', 'blocked')
            parody_detection: Enable parody detection
            target_column: Target column for prediction (if applicable)
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with analysis results
        """
        print(f"🔍 Starting intertemporal differential analysis...")
        print(f"   Method: {cv_method}")
        print(f"   Parody Detection: {parody_detection}")
        
        # Convert data to DataFrame if needed
        if isinstance(data, dict):
            df = pd.DataFrame(data)
        else:
            df = data.copy()
        
        # Ensure we have a datetime index
        if not isinstance(df.index, pd.DatetimeIndex):
            if 'timestamp' in df.columns:
                df.set_index('timestamp', inplace=True)
            elif 'date' in df.columns:
                df.set_index('date', inplace=True)
            else:
                # Create synthetic timestamps
                df.index = pd.date_range(start='2020-01-01', periods=len(df), freq='D')
        
        results = {
            'method': cv_method,
            'timestamp': datetime.now().isoformat(),
            'security_key': self.security_key[:20] + "..." if self.security_key else None,
            'data_shape': df.shape,
            'analysis_results': {}
        }
        
        # Perform intertemporal differential calculations
        temporal_diffs = self._calculate_temporal_differentials(df)
        results['temporal_differentials'] = temporal_diffs
        
        # Perform cross-validation analysis
        cv_results = self._perform_cross_validation(df, cv_method, target_column)
        results['cv_analysis'] = cv_results
        
        # Perform parody detection if enabled
        if parody_detection:
            parody_results = self._detect_parody_patterns(df)
            results['parody_detection'] = parody_results
        
        # Add volatility clustering analysis if statsmodels available
        if STATSMODELS_AVAILABLE and target_column and target_column in df.columns:
            volatility_results = self._analyze_volatility_clustering(df[target_column])
            results['volatility_analysis'] = volatility_results
        
        # Store results for future reference
        self.cv_results = results
        
        print("✅ Intertemporal differential analysis complete")
        return results
    
    def _calculate_temporal_differentials(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate intertemporal differential metrics"""
        print("   📊 Calculating temporal differentials...")
        
        results = {}
        
        # Calculate temporal deltas for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if len(df[col].dropna()) > 1:
                # Temporal Delta = f(t+1) - f(t)
                temporal_delta = df[col].diff()
                
                results[f'{col}_temporal_delta'] = {
                    'mean': temporal_delta.mean(),
                    'std': temporal_delta.std(),
                    'min': temporal_delta.min(),
                    'max': temporal_delta.max(),
                    'trend': 'increasing' if temporal_delta.mean() > 0 else 'decreasing'
                }
                
                # Rolling correlation with lags
                if len(df[col].dropna()) > 10:
                    rolling_corrs = []
                    for k in range(1, min(6, len(df[col])//2)):
                        if len(df[col]) > k:
                            lagged_series = df[col].shift(k)
                            corr = df[col].corr(lagged_series)
                            if not np.isnan(corr):
                                rolling_corrs.append({'lag': k, 'correlation': corr})
                    
                    results[f'{col}_rolling_correlations'] = rolling_corrs
        
        return results
    
    def _perform_cross_validation(self, df: pd.DataFrame, cv_method: str, target_column: Optional[str]) -> Dict[str, Any]:
        """Perform cross-validation analysis based on specified method"""
        print(f"   🎯 Performing {cv_method} cross-validation...")
        
        if not SKLEARN_AVAILABLE:
            return {'error': 'scikit-learn not available for CV analysis'}
        
        results = {
            'method': cv_method,
            'cv_scores': [],
            'performance_metrics': {}
        }
        
        # Prepare data for CV
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return {'error': 'No numeric columns available for CV analysis'}
        
        # Use first numeric column as target if not specified
        if not target_column or target_column not in numeric_cols:
            target_column = numeric_cols[0]
        
        # Prepare features (other numeric columns)
        feature_cols = [col for col in numeric_cols if col != target_column]
        if len(feature_cols) == 0:
            # Create lagged features
            df_features = pd.DataFrame()
            for lag in range(1, 4):
                df_features[f'{target_column}_lag_{lag}'] = df[target_column].shift(lag)
            feature_cols = df_features.columns.tolist()
            df = pd.concat([df, df_features], axis=1)
        
        # Drop NaN values
        analysis_df = df[[target_column] + feature_cols].dropna()
        
        if len(analysis_df) < 10:
            return {'error': 'Insufficient data for CV analysis'}
        
        X = analysis_df[feature_cols]
        y = analysis_df[target_column]
        
        # Perform CV based on method
        if cv_method == 'time_series':
            cv_splits = TimeSeriesSplit(n_splits=min(5, len(X)//3))
        elif cv_method == 'expanding_window':
            # Custom expanding window implementation
            cv_splits = self._expanding_window_splits(len(X))
        elif cv_method == 'blocked':
            # Custom blocked time series implementation
            cv_splits = self._blocked_time_series_splits(len(X))
        else:
            cv_splits = TimeSeriesSplit(n_splits=3)
        
        # Perform cross-validation
        model = LinearRegression() if len(feature_cols) <= len(X)//2 else RandomForestRegressor(n_estimators=10)
        cv_scores = []
        
        try:
            for train_idx, test_idx in cv_splits:
                X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
                
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                mse = mean_squared_error(y_test, y_pred)
                cv_scores.append(mse)
            
            results['cv_scores'] = cv_scores
            results['performance_metrics'] = {
                'mean_cv_score': np.mean(cv_scores),
                'std_cv_score': np.std(cv_scores),
                'out_of_sample_accuracy': 1 / (1 + np.mean(cv_scores)) if np.mean(cv_scores) > 0 else 0.5
            }
            
        except Exception as e:
            results['error'] = f"CV analysis failed: {str(e)}"
        
        return results
    
    def _detect_parody_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect parody patterns in text data"""
        print("   🎭 Analyzing parody patterns...")
        
        results = {
            'parody_indicators_found': [],
            'sentiment_analysis': {},
            'pattern_confidence': 0.0
        }
        
        # Look for text columns
        text_columns = df.select_dtypes(include=['object']).columns
        parody_count = 0
        total_text_entries = 0
        
        for col in text_columns:
            col_parody_count = 0
            for text in df[col].dropna():
                if isinstance(text, str):
                    total_text_entries += 1
                    text_lower = text.lower()
                    
                    # Check for parody markers
                    for marker in self.parody_markers:
                        if marker in text_lower:
                            parody_count += 1
                            col_parody_count += 1
                            results['parody_indicators_found'].append({
                                'column': col,
                                'marker': marker,
                                'text_sample': text[:100] + "..." if len(text) > 100 else text
                            })
                            break
            
            # Sentiment differential analysis for this column
            if col_parody_count > 0:
                results['sentiment_analysis'][col] = {
                    'parody_instances': col_parody_count,
                    'total_instances': len(df[col].dropna()),
                    'parody_ratio': col_parody_count / len(df[col].dropna()) if len(df[col].dropna()) > 0 else 0
                }
        
        # Calculate overall confidence
        if total_text_entries > 0:
            results['pattern_confidence'] = parody_count / total_text_entries
        
        results['total_parody_indicators'] = parody_count
        results['total_text_entries'] = total_text_entries
        
        return results
    
    def _analyze_volatility_clustering(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze volatility clustering using GARCH-like approach"""
        print("   📈 Analyzing volatility clustering...")
        
        if not STATSMODELS_AVAILABLE:
            return {'error': 'statsmodels not available for volatility analysis'}
        
        results = {}
        
        try:
            # Calculate returns
            returns = series.pct_change().dropna()
            
            if len(returns) < 10:
                return {'error': 'Insufficient data for volatility analysis'}
            
            # Basic volatility measures
            volatility = returns.rolling(window=5).std()
            
            results['volatility_metrics'] = {
                'mean_volatility': volatility.mean(),
                'volatility_std': volatility.std(),
                'max_volatility': volatility.max(),
                'min_volatility': volatility.min()
            }
            
            # Test for stationarity
            adf_result = adfuller(returns.dropna())
            results['stationarity_test'] = {
                'adf_statistic': adf_result[0],
                'p_value': adf_result[1],
                'is_stationary': adf_result[1] < 0.05
            }
            
            # Volatility clustering detection (simplified)
            squared_returns = returns ** 2
            volatility_autocorr = []
            for lag in range(1, min(6, len(squared_returns)//3)):
                if len(squared_returns) > lag:
                    autocorr = squared_returns.autocorr(lag=lag)
                    if not np.isnan(autocorr):
                        volatility_autocorr.append({'lag': lag, 'autocorr': autocorr})
            
            results['volatility_clustering'] = volatility_autocorr
            
        except Exception as e:
            results['error'] = f"Volatility analysis failed: {str(e)}"
        
        return results
    
    def _expanding_window_splits(self, n_samples: int) -> List[tuple]:
        """Generate expanding window splits"""
        min_train_size = max(10, n_samples // 5)
        test_size = max(5, n_samples // 10)
        
        splits = []
        for i in range(min_train_size, n_samples - test_size, test_size):
            train_idx = list(range(i))
            test_idx = list(range(i, min(i + test_size, n_samples)))
            if len(test_idx) > 0:
                splits.append((train_idx, test_idx))
        
        return splits
    
    def _blocked_time_series_splits(self, n_samples: int) -> List[tuple]:
        """Generate blocked time series splits"""
        block_size = max(10, n_samples // 5)
        gap_size = max(2, block_size // 5)
        
        splits = []
        start = 0
        
        while start + 2 * block_size + gap_size <= n_samples:
            train_end = start + block_size
            test_start = train_end + gap_size
            test_end = min(test_start + block_size, n_samples)
            
            train_idx = list(range(start, train_end))
            test_idx = list(range(test_start, test_end))
            
            if len(train_idx) > 0 and len(test_idx) > 0:
                splits.append((train_idx, test_idx))
            
            start = test_end
        
        return splits
    
    def get_regime_change_detection(self, data: pd.Series, window: int = 20) -> Dict[str, Any]:
        """
        Detect structural breaks/regime changes in time series
        
        Args:
            data: Time series data
            window: Rolling window size for change detection
            
        Returns:
            Dictionary with regime change analysis
        """
        print("🔄 Detecting regime changes...")
        
        results = {
            'regime_changes': [],
            'regime_periods': [],
            'change_points': []
        }
        
        if len(data) < window * 2:
            results['error'] = 'Insufficient data for regime change detection'
            return results
        
        try:
            # Rolling statistics
            rolling_mean = data.rolling(window=window).mean()
            rolling_std = data.rolling(window=window).std()
            
            # Detect significant changes in mean
            mean_changes = rolling_mean.diff().abs()
            mean_threshold = mean_changes.quantile(0.95)
            
            # Detect significant changes in volatility
            std_changes = rolling_std.diff().abs()
            std_threshold = std_changes.quantile(0.95)
            
            # Find change points
            change_points = []
            for i in range(window, len(data) - window):
                if (mean_changes.iloc[i] > mean_threshold or 
                    std_changes.iloc[i] > std_threshold):
                    change_points.append({
                        'index': i,
                        'timestamp': data.index[i] if hasattr(data.index, 'strftime') else i,
                        'mean_change': mean_changes.iloc[i],
                        'std_change': std_changes.iloc[i]
                    })
            
            results['change_points'] = change_points
            results['total_regime_changes'] = len(change_points)
            
        except Exception as e:
            results['error'] = f"Regime change detection failed: {str(e)}"
        
        return results
    
    def validate_security_context(self) -> Dict[str, Any]:
        """
        Validate COMBSEC security context integration
        
        Returns:
            Dictionary with security validation results
        """
        if not COMBSEC_AVAILABLE:
            return {
                'valid': False,
                'error': 'COMBSEC system not available',
                'recommendation': 'Install ACTNEWWORLDODOR emoji_combsec_generator'
            }
        
        if not self.combsec_generator:
            return {
                'valid': False,
                'error': 'COMBSEC generator not initialized'
            }
        
        # Validate current security key
        if self.security_key:
            validation_result = self.combsec_generator.validate_combsec_key(self.security_key)
            return {
                'valid': validation_result.get('valid', False),
                'security_key_truncated': self.security_key[:20] + "...",
                'firm_id': self.firm_id,
                'validation_details': validation_result
            }
        
        return {
            'valid': False,
            'error': 'No security key available for validation'
        }


def create_sample_financial_data(n_samples: int = 100) -> pd.DataFrame:
    """
    Create sample financial data for testing the IntertemporalAnalyzer
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame with sample financial data
    """
    np.random.seed(42)  # For reproducible results
    
    dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='D')
    
    # Generate correlated price series with some trending behavior
    base_price = 100
    prices = [base_price]
    
    for i in range(1, n_samples):
        # Add trend and noise
        trend = 0.001 * i  # Small upward trend
        noise = np.random.normal(0, 0.02)  # 2% daily volatility
        price_change = trend + noise
        new_price = prices[-1] * (1 + price_change)
        prices.append(new_price)
    
    # Add some parody/fake markers randomly
    text_data = []
    for i in range(n_samples):
        if np.random.random() < 0.05:  # 5% chance of parody marker
            text_data.append(f"This is a parody analysis #{i}")
        elif np.random.random() < 0.03:  # 3% chance of fake marker
            text_data.append(f"Fake news about market #{i}")
        else:
            text_data.append(f"Regular market analysis #{i}")
    
    df = pd.DataFrame({
        'price': prices,
        'volume': np.random.lognormal(10, 0.5, n_samples),
        'returns': pd.Series(prices).pct_change(),
        'text_analysis': text_data,
        'timestamp': dates
    })
    
    df.set_index('timestamp', inplace=True)
    return df


if __name__ == "__main__":
    # Example usage as shown in the ChatGPT document
    print("🌐 IntertemporalAnalyzer Demo")
    print("=" * 50)
    
    # Create sample data
    financial_data = create_sample_financial_data(50)
    print(f"📊 Generated sample data: {financial_data.shape}")
    
    # Initialize analyzer
    analyzer = IntertemporalAnalyzer()
    
    # Perform analysis
    results = analyzer.analyze_temporal_diffs(
        data=financial_data,
        cv_method='time_series',
        parody_detection=True,
        target_column='price'
    )
    
    print("\n📈 Analysis Results Summary:")
    print(f"   Method: {results['method']}")
    print(f"   Data Shape: {results['data_shape']}")
    print(f"   Temporal Differentials: {len(results.get('temporal_differentials', {}))}")
    print(f"   CV Analysis: {results.get('cv_analysis', {}).get('performance_metrics', 'N/A')}")
    print(f"   Parody Detection: {results.get('parody_detection', {}).get('total_parody_indicators', 0)} indicators found")
    
    # Validate security context
    security_validation = analyzer.validate_security_context()
    print(f"\n🔐 Security Validation: {security_validation.get('valid', False)}")
    
    print("\n✅ Demo complete!")