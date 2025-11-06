import os 
import sys 
from data_processing import DataPreprocessor
from visualization import MapVisualizer, StatisticsVisualizer

def create_output_directory():
    if not os.path.exists('output'):
        os.makedirs('output')
        print('Created Output Directory')

def main():
    print('='*60)
    print("INTERACTIVE GEOSPATIAL DATA VISUALIZATION DASHBOARD")
    print('='*60)

    create_output_directory()

    print('\n[1st Step] Loading Data..')
    preprocessor = DataPreprocessor('data/cities.csv')
    df = preprocessor.load_data()

    if df is None:
        print('Error: Could not load data.')
        return

    print("\n[Step 2] Exploring data...")
    preprocessor.explore_data()

    print("\n[Step 3] Cleaning data...")
    df = preprocessor.clean_data()
    preprocessor.get_summary()      
    
    # Step 4: Create interactive maps
    print("\n[Step 4] Creating interactive maps...")
    map_viz = MapVisualizer(df, output_dir='output')
    
    # Create basic markers map
    print("  - Creating markers map...")
    m1 = map_viz.create_base_map()
    m1 = map_viz.add_markers(m1, limit=200)
    map_viz.save_map(m1, 'markers_map.html')
    
    # Create marker cluster map
    print("  - Creating marker cluster map...")
    m2 = map_viz.create_marker_cluster_map()
    map_viz.save_map(m2, 'cluster_map.html')
    
    # Create heatmap
    print("  - Creating heatmap...")
    m3 = map_viz.create_heatmap()
    map_viz.save_map(m3, 'heatmap.html')
    
    # Create choropleth by country
    print("  - Creating choropleth map...")
    m4 = map_viz.create_choropleth_by_country()
    map_viz.save_map(m4, 'choropleth_map.html')
    
    # Step 5: Create statistical visualizations
    print("\n[Step 5] Creating statistical visualizations...")
    stats_viz = StatisticsVisualizer(df, output_dir='output')
    stats_viz.plot_all()
    
    # Step 6: Generate summary report
    print("\n[Step 6] Generating summary report...")
    print_summary_report(processor)
    
    print("\n" + "="*60)
    print("PROJECT COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nOutput files created in 'output' directory:")
    print("  - markers_map.html (Interactive map with individual markers)")
    print("  - cluster_map.html (Map with clustered markers)")
    print("  - heatmap.html (Heat distribution map)")
    print("  - choropleth_map.html (Country-level visualization)")
    print("  - latitude_distribution.png (Latitude histogram)")
    print("  - longitude_distribution.png (Longitude histogram)")
    print("  - top_countries.png (Bar chart of top countries)")
    print("  - lat_lng_scatter.png (Scatter plot visualization)")
    print("  - summary_statistics.png (Summary statistics table)")
    print("\nTo view the maps, open the HTML files in your web browser.")
    

def print_summary_report(processor):
    stats = processor.get_statistics()
    
    print("\n" + "-"*60)
    print("SUMMARY REPORT")
    print("-"*60)
    print(f"Total Cities Analyzed:        {stats['total_cities']:,}")
    print(f"Total Unique Countries:       {stats['unique_countries']}")
    print(f"Average Latitude:             {stats['avg_latitude']:.2f}°")
    print(f"Average Longitude:            {stats['avg_longitude']:.2f}°")
    print(f"Latitude Range:               {stats['lat_range'][0]:.2f}° to {stats['lat_range'][1]:.2f}°")
    print(f"Longitude Range:              {stats['lng_range'][0]:.2f}° to {stats['lng_range'][1]:.2f}°")
    print("-"*60)


if __name__ == "__main__":
    main()