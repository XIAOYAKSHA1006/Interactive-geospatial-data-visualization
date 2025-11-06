import pandas as pd 
import numpy as np

class DataPreprocessor:
    def __init__(self, filepath):
        filepath = pd.read_csv(r"C:\Users\shubh\OneDrive\Desktop\College Projects\CAB111 Project\Dataset\worldcities.csv")
        self.filepath = filepath
        self.df = None
    
    def load_data(self):
        try:    
            self.df = self.filepath
            print(f"Data Uploaded Successfully: {self.df.shape}")
            return self.df
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return None

    def explore_data(self):
        if self.df is None:
            print("No data Loaded")
            return
        
        print("\n=== Data Exploration ===")
        print(f"Dataset Shape: {self.df.shape}")
        print(f"\nColumn Names:\n{self.df.columns.tolist()}")
        print(f"\nFirst 5 Rows:\n{self.df.head()}")
        print(f"\nData Types:\n{self.df.dtypes}")
        print(f"\nMissing Values:\n{self.df.isnull().sum()}")
        print(f"\nBasic Statistics:\n{self.df.describe()}")

    def clean_data(self):
        if self.df is None:
            print("No Data Loaded")
            return
        
        self.df = self.df.dropna(subset=['lat','lng'])
        self.df = self.df.reset_index(drop=True) 
        print(f"Data is cleaned. New shape: {self.df.shape}")
        return self.df

    def get_statistics(self):
        if self.df is None:
            return None

        stats = {
            'total_cities': len(self.df),
            'unique_countries': self.df['country'].nunique() if 'country' in self.df.columns else 0,
            'avg_latitude': self.df['lat'].mean(),
            'avg_longitude': self.df['lng'].mean(),
            'lat_range': (self.df['lat'].min(), self.df['lat'].max()),
            'lng_range': (self.df['lng'].min(), self.df['lng'].max()),
        }   
        return stats
    
    def get_top_cities(self, n=10, sort_by='population'):
        if self.df is None:
            return None
        if sort_by in self.df.columns:
            return self.df.nlargest(n, sortby)
        else:
            return self.df.head(n)

    def filter_by_countries(self, country_name):
        if self.df is None:
            return None
        return self.df[self.df['country'].str.lower() == country_name.lower()]

    def get_summary(self):
        stats = self.get_statistics()
        print("\n===Data Summary ===")       
        for key,value in stats.items():
            print(f"{key}: {value}")