"""Visualization utilities."""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class Plotter:
    """Handles visualization tasks."""
    
    def __init__(self, output_dir: str = "visualizations"):
        """
        Initialize plotter.
        
        Args:
            output_dir: Directory to save plots
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"Plotter initialized with output directory: {output_dir}")
    
    def plot_time_series(self, df: pd.DataFrame, column: str, title: str = None, save: bool = True) -> None:
        """
        Plot time series data.
        
        Args:
            df: Input dataframe with datetime index
            column: Column to plot
            title: Plot title
            save: Whether to save the plot
        """
        logger.info(f"Plotting time series for {column}")
        
        plt.figure(figsize=(14, 6))
        plt.plot(df.index, df[column], linewidth=1)
        plt.title(title or f"Time Series - {column}")
        plt.xlabel("Date")
        plt.ylabel(column)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save:
            path = self.output_dir / f"time_series_{column}.png"
            plt.savefig(path, dpi=100)
            logger.info(f"Plot saved to {path}")
        
        plt.close()
    
    def plot_distribution(self, df: pd.DataFrame, column: str, title: str = None, save: bool = True) -> None:
        """
        Plot distribution of a variable.
        
        Args:
            df: Input dataframe
            column: Column to plot
            title: Plot title
            save: Whether to save the plot
        """
        logger.info(f"Plotting distribution for {column}")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(df[column], bins=50, edgecolor='black')
        axes[0].set_title(f"Histogram - {column}")
        axes[0].set_xlabel(column)
        axes[0].set_ylabel("Frequency")
        
        # Box plot
        axes[1].boxplot(df[column])
        axes[1].set_title(f"Box Plot - {column}")
        axes[1].set_ylabel(column)
        
        plt.tight_layout()
        
        if save:
            path = self.output_dir / f"distribution_{column}.png"
            plt.savefig(path, dpi=100)
            logger.info(f"Plot saved to {path}")
        
        plt.close()
    
    def plot_correlation_matrix(self, df: pd.DataFrame, title: str = None, save: bool = True) -> None:
        """
        Plot correlation matrix heatmap.
        
        Args:
            df: Input dataframe (numeric columns only)
            title: Plot title
            save: Whether to save the plot
        """
        logger.info("Plotting correlation matrix")
        
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        corr_matrix = numeric_df.corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title(title or "Correlation Matrix")
        plt.tight_layout()
        
        if save:
            path = self.output_dir / "correlation_matrix.png"
            plt.savefig(path, dpi=100)
            logger.info(f"Plot saved to {path}")
        
        plt.close()
    
    def plot_predictions_vs_actual(self, y_actual: np.ndarray, y_pred: np.ndarray, 
                                    title: str = None, save: bool = True) -> None:
        """
        Plot actual vs predicted values.
        
        Args:
            y_actual: Actual values
            y_pred: Predicted values
            title: Plot title
            save: Whether to save the plot
        """
        logger.info("Plotting predictions vs actual")
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(y_actual[:200], label='Actual', alpha=0.7)
        plt.plot(y_pred[:200], label='Predicted', alpha=0.7)
        plt.title("Actual vs Predicted (First 200 samples)")
        plt.legend()
        plt.xlabel("Sample Index")
        plt.ylabel("Value")
        
        plt.subplot(1, 2, 2)
        plt.scatter(y_actual, y_pred, alpha=0.5)
        plt.plot([y_actual.min(), y_actual.max()], [y_actual.min(), y_actual.max()], 'r--', lw=2)
        plt.xlabel("Actual")
        plt.ylabel("Predicted")
        plt.title("Predicted vs Actual Scatter")
        
        plt.tight_layout()
        
        if save:
            path = self.output_dir / "predictions_vs_actual.png"
            plt.savefig(path, dpi=100)
            logger.info(f"Plot saved to {path}")
        
        plt.close()
