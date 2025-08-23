#!/usr/bin/env python3
"""
Donor Prediction Model for ThalaNet Emergency Blood Management Platform
Predicts donor availability in the next 30 days using machine learning
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, classification_report
import joblib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class DonorPredictionModel:
    def __init__(self, model_type: str = 'random_forest'):
        """
        Initialize the donor prediction model
        
        Args:
            model_type: Type of ML model ('random_forest', 'gradient_boosting', 'logistic')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.target_column = 'predicted_availability_score'
        self.model_path = f"models/donor_prediction_{model_type}.pkl"
        self.scaler_path = f"models/donor_prediction_scaler.pkl"
        self.encoders_path = f"models/donor_prediction_encoders.pkl"
        
    def prepare_features(self, donors_df: pd.DataFrame, donations_df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for the ML model
        
        Args:
            donors_df: Donor dataset
            donations_df: Historical donations dataset
            
        Returns:
            DataFrame with prepared features
        """
        print("Preparing features for ML model...")
        
        # Merge donor and donation data
        merged_df = donors_df.merge(
            donations_df.groupby('donor_id').agg({
                'donation_date': 'count',
                'was_successful': 'sum',
                'units_donated': 'sum'
            }).reset_index(),
            on='donor_id',
            how='left'
        )
        
        # Fill NaN values
        merged_df['donation_date'] = merged_df['donation_date'].fillna(0)
        merged_df['was_successful'] = merged_df['was_successful'].fillna(0)
        merged_df['units_donated'] = merged_df['units_donated'].fillna(0)
        
        # Calculate days since last donation
        merged_df['last_donation_date'] = pd.to_datetime(merged_df['last_donation_date'])
        merged_df['days_since_donation'] = (datetime.now() - merged_df['last_donation_date']).dt.days
        
        # Calculate donation success rate
        merged_df['success_rate'] = np.where(
            merged_df['donation_date'] > 0,
            merged_df['was_successful'] / merged_df['donation_date'],
            0
        )
        
        # Calculate average units per donation
        merged_df['avg_units_per_donation'] = np.where(
            merged_df['donation_date'] > 0,
            merged_df['units_donated'] / merged_df['donation_date'],
            0
        )
        
        # Encode categorical variables
        categorical_columns = ['gender', 'blood_type', 'health_conditions', 'availability_status']
        
        for col in categorical_columns:
            if col in merged_df.columns:
                le = LabelEncoder()
                merged_df[f'{col}_encoded'] = le.fit_transform(merged_df[col].astype(str))
                self.label_encoders[col] = le
        
        # Create feature matrix
        feature_columns = [
            'age', 'days_since_donation', 'donation_frequency', 'responsiveness_score',
            'donation_date', 'was_successful', 'units_donated', 'success_rate',
            'avg_units_per_donation'
        ]
        
        # Add encoded categorical features
        for col in categorical_columns:
            if col in merged_df.columns:
                feature_columns.append(f'{col}_encoded')
        
        # Filter out rows with missing values
        merged_df = merged_df.dropna(subset=feature_columns)
        
        # Create target variable (availability score for next 30 days)
        merged_df[self.target_column] = self._calculate_availability_score(merged_df)
        
        self.feature_columns = feature_columns
        
        print(f"Prepared {len(merged_df)} samples with {len(feature_columns)} features")
        return merged_df
    
    def _calculate_availability_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate availability score for next 30 days
        
        Args:
            df: DataFrame with donor features
            
        Returns:
            Series with availability scores (0-1)
        """
        scores = []
        
        for _, row in df.iterrows():
            score = 0.0
            
            # Base score from current availability status
            if row['availability_status'] == 'Available':
                score += 0.3
            
            # Days since last donation (longer = higher score)
            days_since = row['days_since_donation']
            if days_since >= 56:  # 8 weeks minimum
                score += 0.2
            elif days_since >= 30:
                score += 0.1
            
            # Health conditions
            if row['health_conditions'] == 'None':
                score += 0.2
            else:
                score += 0.05  # Reduced score for health issues
            
            # Responsiveness score
            score += row['responsiveness_score'] * 0.15
            
            # Success rate in donations
            score += row['success_rate'] * 0.1
            
            # Age factor (18-45 preferred)
            age = row['age']
            if 18 <= age <= 45:
                score += 0.05
            
            # Normalize to 0-1 range
            score = min(1.0, max(0.0, score))
            scores.append(score)
        
        return pd.Series(scores)
    
    def train(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict:
        """
        Train the ML model
        
        Args:
            df: DataFrame with features and target
            test_size: Fraction of data to use for testing
            
        Returns:
            Dictionary with training results
        """
        print(f"Training {self.model_type} model...")
        
        # Prepare features and target
        X = df[self.feature_columns]
        y = df[self.target_column]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Initialize and train model
        if self.model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                random_state=42
            )
        elif self.model_type == 'logistic':
            # Convert to classification problem
            y_train_binary = (y_train > 0.5).astype(int)
            y_test_binary = (y_test > 0.5).astype(int)
            
            self.model = LogisticRegression(random_state=42, max_iter=1000)
            self.model.fit(X_train_scaled, y_train_binary)
            
            # Evaluate classification model
            y_pred_binary = self.model.predict(X_test_scaled)
            classification_metrics = classification_report(y_test_binary, y_pred_binary, output_dict=True)
            
            # For regression metrics, use probability predictions
            y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
            mse = mean_squared_error(y_test, y_pred_proba)
            r2 = r2_score(y_test, y_pred_proba)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Train regression models
        if self.model_type in ['random_forest', 'gradient_boosting']:
            self.model.fit(X_train_scaled, y_train)
            y_pred = self.model.predict(X_test_scaled)
            
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            classification_metrics = None
        
        # Cross-validation score
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5, scoring='r2')
        
        # Feature importance (for tree-based models)
        feature_importance = None
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = dict(zip(self.feature_columns, self.model.feature_importances_))
        
        # Results
        results = {
            'model_type': self.model_type,
            'test_size': test_size,
            'training_samples': len(X_train),
            'testing_samples': len(X_test),
            'features': len(self.feature_columns),
            'mse': mse,
            'r2_score': r2,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': feature_importance,
            'classification_metrics': classification_metrics
        }
        
        print(f"Training completed!")
        print(f"R² Score: {r2:.4f}")
        print(f"Cross-validation R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        
        return results
    
    def predict(self, donor_features: pd.DataFrame) -> np.ndarray:
        """
        Predict availability scores for donors
        
        Args:
            donor_features: DataFrame with donor features
            
        Returns:
            Array of predicted availability scores
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare features
        X = donor_features[self.feature_columns]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        if self.model_type == 'logistic':
            # Return probability of being available
            predictions = self.model.predict_proba(X_scaled)[:, 1]
        else:
            predictions = self.model.predict(X_scaled)
        
        # Ensure predictions are in 0-1 range
        predictions = np.clip(predictions, 0, 1)
        
        return predictions
    
    def save_model(self, output_dir: str = "models"):
        """Save the trained model and preprocessing objects"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save model
        joblib.dump(self.model, self.model_path)
        
        # Save scaler
        joblib.dump(self.scaler, self.scaler_path)
        
        # Save label encoders
        joblib.dump(self.label_encoders, self.encoders_path)
        
        print(f"Model saved to {output_dir}/")
    
    def load_model(self, model_dir: str = "models"):
        """Load a previously trained model"""
        self.model_path = f"{model_dir}/donor_prediction_{self.model_type}.pkl"
        self.scaler_path = f"{model_dir}/donor_prediction_scaler.pkl"
        self.encoders_path = f"{model_dir}/donor_prediction_encoders.pkl"
        
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            self.label_encoders = joblib.load(self.encoders_path)
            print(f"Model loaded from {model_dir}/")
            return True
        except FileNotFoundError:
            print(f"Model files not found in {model_dir}/")
            return False
    
    def evaluate_model(self, test_df: pd.DataFrame) -> Dict:
        """
        Evaluate the model on test data
        
        Args:
            test_df: Test dataset with features and target
            
        Returns:
            Dictionary with evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        X_test = test_df[self.feature_columns]
        y_test = test_df[self.target_column]
        
        # Make predictions
        y_pred = self.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Calculate custom metrics
        availability_accuracy = np.mean((y_pred > 0.5) == (y_test > 0.5))
        
        results = {
            'mse': mse,
            'r2_score': r2,
            'availability_accuracy': availability_accuracy,
            'predictions_mean': y_pred.mean(),
            'actual_mean': y_test.mean(),
            'predictions_std': y_pred.std(),
            'actual_std': y_test.std()
        }
        
        return results

def train_and_evaluate_models(donors_df: pd.DataFrame, donations_df: pd.DataFrame):
    """
    Train and evaluate different model types
    
    Args:
        donors_df: Donor dataset
        donations_df: Historical donations dataset
    """
    print("Training and evaluating multiple model types...")
    
    models = ['random_forest', 'gradient_boosting', 'logistic']
    results = {}
    
    for model_type in models:
        print(f"\n{'='*50}")
        print(f"Training {model_type.upper()} model")
        print(f"{'='*50}")
        
        # Initialize model
        model = DonorPredictionModel(model_type=model_type)
        
        # Prepare features
        prepared_df = model.prepare_features(donors_df, donations_df)
        
        # Train model
        training_results = model.train(prepared_df)
        
        # Save model
        model.save_model()
        
        # Store results
        results[model_type] = training_results
    
    # Compare models
    print(f"\n{'='*60}")
    print("MODEL COMPARISON")
    print(f"{'='*60}")
    
    comparison_df = pd.DataFrame(results).T
    print(comparison_df[['model_type', 'r2_score', 'cv_mean', 'cv_std']].round(4))
    
    # Find best model
    best_model = comparison_df.loc[comparison_df['r2_score'].idxmax()]
    print(f"\nBest model: {best_model['model_type']} (R² = {best_model['r2_score']:.4f})")
    
    return results

if __name__ == "__main__":
    # Example usage
    print("Donor Prediction Model")
    print("=" * 50)
    
    # Load sample data (replace with your actual data paths)
    try:
        donors_df = pd.read_csv("data/donors.csv")
        donations_df = pd.read_csv("data/historical_donations.csv")
        
        # Train and evaluate models
        results = train_and_evaluate_models(donors_df, donations_df)
        
        # Save results
        with open("models/training_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print("\nTraining completed! Results saved to models/training_results.json")
        
    except FileNotFoundError:
        print("Data files not found. Please run the synthetic data generator first.")
        print("Run: python src/utils/syntheticDataGenerator.py")

