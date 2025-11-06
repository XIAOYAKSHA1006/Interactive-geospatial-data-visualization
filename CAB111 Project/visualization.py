import folium
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from folium.plugins import HeatMap, MarkerCluster

class MapVisualizer:
    
    def __init__(self, df, output_dir='output'):
        self.df = df
        self.output_dir = output_dir
        
    def create_base_map(self, location=None, zoom_start=4, tiles='OpenStreetMap'):
        if location is None:
            # Center on world average
            location = [self.df['lat'].mean(), self.df['lng'].mean()]
            
        m = folium.Map(
            location=location,
            zoom_start=zoom_start,
            tiles=tiles,
            control_scale=True
        )    
        return m
        
    def add_markers(self, m, limit=100):
        data = self.df.head(limit)
        
        for idx, row in data.iterrows():
            popup_text = f"<b>{row['city']}</b><br>Country: {row['country']}"
            
            folium.Marker(
                location=[row['lat'], row['lng']],
                popup=popup_text,
                tooltip=row['city'],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
            
        print(f"Added {min(len(data), limit)} markers to map")
        return m
        
    def create_marker_cluster_map(self, location=None, zoom_start=4):
        m = self.create_base_map(location, zoom_start)
        
        # Add marker cluster
        marker_cluster = MarkerCluster().add_to(m)
        
        for idx, row in self.df.iterrows():
            folium.Marker(
                location=[row['lat'], row['lng']],
                popup=f"{row['city']}, {row['country']}",
                icon=folium.Icon(color='green')
            ).add_to(marker_cluster)
            
        print(f"Created marker cluster map with {len(self.df)} markers")
        return m
        
    def create_heatmap(self, location=None, zoom_start=4):
        m = self.create_base_map(location, zoom_start)
        
        # Prepare data for heatmap
        heat_data = [[row['lat'], row['lng']] for idx, row in self.df.iterrows()]
        
        # Add heatmap layer
        HeatMap(heat_data, radius=15, blur=25, max_zoom=1).add_to(m)
        
        print(f"Created heatmap with {len(heat_data)} data points")
        return m
        
    def create_choropleth_by_country(self):
        # Count cities per country
        country_counts = self.df['country'].value_counts().reset_index()
        country_counts.columns = ['country', 'city_count']
        
        # Create base map
        m = folium.Map(
            location=[20, 0],
            zoom_start=2,
            tiles='CartoDB positron'
        )
        
        # Add country markers with size based on city count
        for idx, row in country_counts.head(50).iterrows():
            country_data = self.df[self.df['country'] == row['country']]
            if len(country_data) > 0:
                avg_lat = country_data['lat'].mean()
                avg_lng = country_data['lng'].mean()
                
                # Scale radius based on number of cities
                radius = int(np.sqrt(row['city_count']) * 2)
                
                folium.CircleMarker(
                    location=[avg_lat, avg_lng],
                    radius=radius,
                    popup=f"{row['country']}: {row['city_count']} cities",
                    color='blue',
                    fill=True,
                    fillColor='blue',
                    fillOpacity=0.6
                ).add_to(m)
                
        print("Created choropleth map by country")
        return m
        
    def save_map(self, m, filename):
        filepath = f"{self.output_dir}/{filename}"
        m.save(filepath)
        print(f"Map saved to: {filepath}")
        

class StatisticsVisualizer:
    def __init__(self, df, output_dir='output'):
        self.df = df
        self.output_dir = output_dir
        sns.set_style("whitegrid")
        
    def plot_latitude_distribution(self):
        plt.figure(figsize=(12, 6))
        sns.histplot(data=self.df, x='lat', kde=True, bins=50)
        plt.title('Distribution of Cities by Latitude', fontsize=16, fontweight='bold')
        plt.xlabel('Latitude', fontsize=12)
        plt.ylabel('Number of Cities', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/latitude_distribution.png", dpi=300)
        print("Saved: latitude_distribution.png")
        plt.close()
        
    def plot_longitude_distribution(self):
        plt.figure(figsize=(12, 6))
        sns.histplot(data=self.df, x='lng', kde=True, bins=50)
        plt.title('Distribution of Cities by Longitude', fontsize=16, fontweight='bold')
        plt.xlabel('Longitude', fontsize=12)
        plt.ylabel('Number of Cities', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/longitude_distribution.png", dpi=300)
        print("Saved: longitude_distribution.png")
        plt.close()
        
    def plot_top_countries(self, n=10):
        top_countries = self.df['country'].value_counts().head(n)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis')
        plt.title(f'Top {n} Countries by Number of Cities', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Cities', fontsize=12)
        plt.ylabel('Country', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/top_countries.png", dpi=300)
        print(f"Saved: top_countries.png")
        plt.close()
        
    def plot_lat_lng_scatter(self, sample_size=1000):
        sample = self.df.sample(n=min(sample_size, len(self.df)))
        
        plt.figure(figsize=(14, 8))
        sns.scatterplot(data=sample, x='lng', y='lat', alpha=0.5, s=30)
        plt.title('Geographic Distribution of Cities (Latitude vs Longitude)', fontsize=16, fontweight='bold')
        plt.xlabel('Longitude', fontsize=12)
        plt.ylabel('Latitude', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/lat_lng_scatter.png", dpi=300)
        print("Saved: lat_lng_scatter.png")
        plt.close()
        
    def plot_summary_statistics(self):
        stats = {
            'Total Cities': len(self.df),
            'Unique Countries': self.df['country'].nunique(),
            'Avg Latitude': self.df['lat'].mean(),
            'Avg Longitude': self.df['lng'].mean(),
        }
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        
        # Create table
        table_data = [[k, f"{v:.2f}"] if isinstance(v, float) else [k, str(v)] 
                      for k, v in stats.items()]
        
        table = ax.table(cellText=table_data, 
                        colLabels=['Metric', 'Value'],
                        cellLoc='center',
                        loc='center',
                        colWidths=[0.5, 0.3])
        
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2)
        
        plt.title('Summary Statistics', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/summary_statistics.png", dpi=300, bbox_inches='tight')
        print("Saved: summary_statistics.png")
        plt.close()
        
    def plot_all(self):
        print("Generating statistical visualizations...")
        self.plot_latitude_distribution()
        self.plot_longitude_distribution()
        self.plot_top_countries()
        self.plot_lat_lng_scatter()
        self.plot_summary_statistics()
        print("All plots generated successfully!")