# =========================================
# Enhanced Analysis with Duplicate Type Organization and Visualization
# =========================================
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from tabulate import tabulate
import os

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

def organize_duplicates_by_type(duplicate_pairs, mixed_duplicates):
    """
    Organize duplicates into separate dataframes by type and detection status
    """
    print("🔧 Organizing duplicates by type and detection status...")
    
    # Get all unique application numbers from detected pairs
    detected_apps = set()
    for _, row in duplicate_pairs.iterrows():
        detected_apps.add(str(row['Application_A']))
        detected_apps.add(str(row['Application_B']))
    
    # Separate mixed_duplicates by type and detection status
    fuzzy_detectable = mixed_duplicates[mixed_duplicates['duplicate_type'] == 'fuzzy_detectable'].copy()
    non_fuzzy_detectable = mixed_duplicates[mixed_duplicates['duplicate_type'] == 'non_fuzzy_detectable'].copy()
    
    # Add detection status
    fuzzy_detectable['was_detected'] = fuzzy_detectable['application_number'].astype(str).isin(detected_apps)
    non_fuzzy_detectable['was_detected'] = non_fuzzy_detectable['application_number'].astype(str).isin(detected_apps)
    
    # Create separate dataframes
    fuzzy_detected = fuzzy_detectable[fuzzy_detectable['was_detected']].copy()
    fuzzy_not_detected = fuzzy_detectable[~fuzzy_detectable['was_detected']].copy()
    non_fuzzy_detected = non_fuzzy_detectable[non_fuzzy_detectable['was_detected']].copy()
    non_fuzzy_not_detected = non_fuzzy_detectable[~non_fuzzy_detectable['was_detected']].copy()
    
    # Create summary dataframe
    summary_data = {
        'Type': ['Fuzzy-Detectable', 'Fuzzy-Detectable', 'Non-Fuzzy-Detectable', 'Non-Fuzzy-Detectable'],
        'Detection_Status': ['Detected', 'Not Detected', 'Detected', 'Not Detected'],
        'Count': [len(fuzzy_detected), len(fuzzy_not_detected), len(non_fuzzy_detected), len(non_fuzzy_not_detected)],
        'Percentage': [
            len(fuzzy_detected) / len(fuzzy_detectable) * 100 if len(fuzzy_detectable) > 0 else 0,
            len(fuzzy_not_detected) / len(fuzzy_detectable) * 100 if len(fuzzy_detectable) > 0 else 0,
            len(non_fuzzy_detected) / len(non_fuzzy_detectable) * 100 if len(non_fuzzy_detectable) > 0 else 0,
            len(non_fuzzy_not_detected) / len(non_fuzzy_detectable) * 100 if len(non_fuzzy_detectable) > 0 else 0
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    
    return {
        'fuzzy_detected': fuzzy_detected,
        'fuzzy_not_detected': fuzzy_not_detected,
        'non_fuzzy_detected': non_fuzzy_detected,
        'non_fuzzy_not_detected': non_fuzzy_not_detected,
        'summary': summary_df,
        'all_duplicates': mixed_duplicates
    }

def display_duplicate_examples(organized_duplicates):
    """
    Display examples of each duplicate type using df.head()
    """
    print("\n" + "=" * 80)
    print("📋 DUPLICATE EXAMPLES BY TYPE")
    print("=" * 80)
    
    # Fuzzy-detectable detected
    if len(organized_duplicates['fuzzy_detected']) > 0:
        print(f"\n✅ FUZZY-DETECTABLE DUPLICATES (DETECTED) - {len(organized_duplicates['fuzzy_detected'])} total:")
        print("Sample records:")
        display_cols = ['application_number', 'original_application_id', 'variation_type', 'user', 'timestamp']
        available_cols = [col for col in display_cols if col in organized_duplicates['fuzzy_detected'].columns]
        print(organized_duplicates['fuzzy_detected'][available_cols].head().to_string(index=False))
    
    # Fuzzy-detectable not detected
    if len(organized_duplicates['fuzzy_not_detected']) > 0:
        print(f"\n❌ FUZZY-DETECTABLE DUPLICATES (NOT DETECTED) - {len(organized_duplicates['fuzzy_not_detected'])} total:")
        print("Sample records:")
        display_cols = ['application_number', 'original_application_id', 'variation_type', 'user', 'timestamp']
        available_cols = [col for col in display_cols if col in organized_duplicates['fuzzy_not_detected'].columns]
        print(organized_duplicates['fuzzy_not_detected'][available_cols].head().to_string(index=False))
    
    # Non-fuzzy-detectable detected
    if len(organized_duplicates['non_fuzzy_detected']) > 0:
        print(f"\n✅ NON-FUZZY-DETECTABLE DUPLICATES (DETECTED) - {len(organized_duplicates['non_fuzzy_detected'])} total:")
        print("Sample records:")
        display_cols = ['application_number', 'original_application_id', 'variation_type', 'user', 'timestamp']
        available_cols = [col for col in display_cols if col in organized_duplicates['non_fuzzy_detected'].columns]
        print(organized_duplicates['non_fuzzy_detected'][available_cols].head().to_string(index=False))
    
    # Non-fuzzy-detectable not detected
    if len(organized_duplicates['non_fuzzy_not_detected']) > 0:
        print(f"\n❌ NON-FUZZY-DETECTABLE DUPLICATES (NOT DETECTED) - {len(organized_duplicates['non_fuzzy_not_detected'])} total:")
        print("Sample records:")
        display_cols = ['application_number', 'original_application_id', 'variation_type', 'user', 'timestamp']
        available_cols = [col for col in display_cols if col in organized_duplicates['non_fuzzy_not_detected'].columns]
        print(organized_duplicates['non_fuzzy_not_detected'][available_cols].head().to_string(index=False))

def save_duplicates_to_csv(organized_duplicates, output_dir="output"):
    """
    Save all duplicate types to a single CSV file with type information
    """
    print(f"\n💾 Saving duplicates to CSV...")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Combine all duplicates with type information
    all_duplicates_with_type = []
    
    # Add fuzzy detected
    if len(organized_duplicates['fuzzy_detected']) > 0:
        df = organized_duplicates['fuzzy_detected'].copy()
        df['duplicate_category'] = 'Fuzzy-Detectable'
        df['detection_status'] = 'Detected'
        all_duplicates_with_type.append(df)
    
    # Add fuzzy not detected
    if len(organized_duplicates['fuzzy_not_detected']) > 0:
        df = organized_duplicates['fuzzy_not_detected'].copy()
        df['duplicate_category'] = 'Fuzzy-Detectable'
        df['detection_status'] = 'Not Detected'
        all_duplicates_with_type.append(df)
    
    # Add non-fuzzy detected
    if len(organized_duplicates['non_fuzzy_detected']) > 0:
        df = organized_duplicates['non_fuzzy_detected'].copy()
        df['duplicate_category'] = 'Non-Fuzzy-Detectable'
        df['detection_status'] = 'Detected'
        all_duplicates_with_type.append(df)
    
    # Add non-fuzzy not detected
    if len(organized_duplicates['non_fuzzy_not_detected']) > 0:
        df = organized_duplicates['non_fuzzy_not_detected'].copy()
        df['duplicate_category'] = 'Non-Fuzzy-Detectable'
        df['detection_status'] = 'Not Detected'
        all_duplicates_with_type.append(df)
    
    # Combine and save
    if all_duplicates_with_type:
        combined_df = pd.concat(all_duplicates_with_type, ignore_index=True)
        csv_path = os.path.join(output_dir, "duplicates_by_type.csv")
        combined_df.to_csv(csv_path, index=False)
        print(f"✅ Saved {len(combined_df)} duplicate records to {csv_path}")
        
        # Also save summary
        summary_path = os.path.join(output_dir, "duplicate_summary.csv")
        organized_duplicates['summary'].to_csv(summary_path, index=False)
        print(f"✅ Saved summary to {summary_path}")
    else:
        print("⚠️ No duplicates to save")

def create_comprehensive_visualization(organized_duplicates, duplicate_pairs):
    """
    Create a single comprehensive visualization showing duplicate types and detection insights
    """
    print(f"\n📊 Creating comprehensive visualization...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Duplicate Detection Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Duplicate Type Distribution (Stacked Bar Chart)
    summary = organized_duplicates['summary']
    
    # Prepare data for stacked bar chart
    fuzzy_detected = summary[(summary['Type'] == 'Fuzzy-Detectable') & (summary['Detection_Status'] == 'Detected')]['Count'].iloc[0] if len(summary[(summary['Type'] == 'Fuzzy-Detectable') & (summary['Detection_Status'] == 'Detected')]) > 0 else 0
    fuzzy_not_detected = summary[(summary['Type'] == 'Fuzzy-Detectable') & (summary['Detection_Status'] == 'Not Detected')]['Count'].iloc[0] if len(summary[(summary['Type'] == 'Fuzzy-Detectable') & (summary['Detection_Status'] == 'Not Detected')]) > 0 else 0
    non_fuzzy_detected = summary[(summary['Type'] == 'Non-Fuzzy-Detectable') & (summary['Detection_Status'] == 'Detected')]['Count'].iloc[0] if len(summary[(summary['Type'] == 'Non-Fuzzy-Detectable') & (summary['Detection_Status'] == 'Detected')]) > 0 else 0
    non_fuzzy_not_detected = summary[(summary['Type'] == 'Non-Fuzzy-Detectable') & (summary['Detection_Status'] == 'Not Detected')]['Count'].iloc[0] if len(summary[(summary['Type'] == 'Non-Fuzzy-Detectable') & (summary['Detection_Status'] == 'Not Detected')]) > 0 else 0
    
    types = ['Fuzzy-Detectable', 'Non-Fuzzy-Detectable']
    detected_counts = [fuzzy_detected, non_fuzzy_detected]
    not_detected_counts = [fuzzy_not_detected, non_fuzzy_not_detected]
    
    x = np.arange(len(types))
    width = 0.6
    
    bars1 = axes[0, 0].bar(x, detected_counts, width, label='Detected', color='lightgreen', alpha=0.8)
    bars2 = axes[0, 0].bar(x, not_detected_counts, width, bottom=detected_counts, label='Not Detected', color='lightcoral', alpha=0.8)
    
    axes[0, 0].set_xlabel('Duplicate Type')
    axes[0, 0].set_ylabel('Number of Duplicates')
    axes[0, 0].set_title('Duplicate Detection by Type', fontweight='bold')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(types)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, (det, not_det) in enumerate(zip(detected_counts, not_detected_counts)):
        if det > 0:
            axes[0, 0].text(i, det/2, str(det), ha='center', va='center', fontweight='bold')
        if not_det > 0:
            axes[0, 0].text(i, det + not_det/2, str(not_det), ha='center', va='center', fontweight='bold')
    
    # 2. Detection Rate Comparison (Bar Chart)
    fuzzy_total = fuzzy_detected + fuzzy_not_detected
    non_fuzzy_total = non_fuzzy_detected + non_fuzzy_not_detected
    
    fuzzy_rate = (fuzzy_detected / fuzzy_total * 100) if fuzzy_total > 0 else 0
    non_fuzzy_rate = (non_fuzzy_detected / non_fuzzy_total * 100) if non_fuzzy_total > 0 else 0
    
    rates = [fuzzy_rate, non_fuzzy_rate]
    colors = ['skyblue', 'lightcoral']
    
    bars = axes[0, 1].bar(types, rates, color=colors, alpha=0.8)
    axes[0, 1].set_ylabel('Detection Rate (%)')
    axes[0, 1].set_title('Detection Rate by Duplicate Type', fontweight='bold')
    axes[0, 1].set_ylim(0, 100)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Add value labels
    for bar, rate in zip(bars, rates):
        axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                       f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 3. Duplicate Pairs Analysis (if available)
    if len(duplicate_pairs) > 0:
        # Similarity distribution
        axes[1, 0].hist(duplicate_pairs['String_Similarity'], bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        axes[1, 0].axvline(duplicate_pairs['String_Similarity'].mean(), color='red', linestyle='--', 
                           label=f'Mean: {duplicate_pairs["String_Similarity"].mean():.1f}%')
        axes[1, 0].set_xlabel('String Similarity (%)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Detected Pairs: Similarity Distribution', fontweight='bold')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
    else:
        axes[1, 0].text(0.5, 0.5, 'No Duplicate Pairs\nDetected', ha='center', va='center', 
                       transform=axes[1, 0].transAxes, fontsize=12)
        axes[1, 0].set_title('Detected Pairs: Similarity Distribution', fontweight='bold')
    
    # 4. Summary Statistics (Text-based visualization)
    axes[1, 1].axis('off')
    
    # Calculate statistics
    total_duplicates = len(organized_duplicates['all_duplicates'])
    total_detected = fuzzy_detected + non_fuzzy_detected
    total_not_detected = fuzzy_not_detected + non_fuzzy_not_detected
    overall_detection_rate = (total_detected / total_duplicates * 100) if total_duplicates > 0 else 0
    
    stats_text = f"""
DUPLICATE DETECTION SUMMARY

📊 Total Duplicates Created: {total_duplicates}
✅ Total Detected: {total_detected} ({overall_detection_rate:.1f}%)
❌ Total Not Detected: {total_not_detected} ({100-overall_detection_rate:.1f}%)

🔍 By Type:
• Fuzzy-Detectable: {fuzzy_total} total
  - Detected: {fuzzy_detected} ({fuzzy_rate:.1f}%)
  - Not Detected: {fuzzy_not_detected} ({100-fuzzy_rate:.1f}%)

• Non-Fuzzy-Detectable: {non_fuzzy_total} total
  - Detected: {non_fuzzy_detected} ({non_fuzzy_rate:.1f}%)
  - Not Detected: {non_fuzzy_not_detected} ({100-non_fuzzy_rate:.1f}%)

🎯 Key Insights:
• Fuzzy matching works well for typo-based duplicates
• Semantic duplicates are harder to detect
• Overall detection rate: {overall_detection_rate:.1f}%
"""
    
    axes[1, 1].text(0.05, 0.95, stats_text, transform=axes[1, 1].transAxes, 
                    fontsize=10, verticalalignment='top', fontfamily='monospace',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    plt.tight_layout()
    plt.show()

def display_detailed_summary(organized_duplicates, duplicate_pairs):
    """
    Display detailed summary statistics
    """
    print("\n" + "=" * 80)
    print("📊 DETAILED DUPLICATE ANALYSIS SUMMARY")
    print("=" * 80)
    
    summary = organized_duplicates['summary']
    
    print(f"\n🔢 TOTAL COUNTS:")
    print(f"   • Total Duplicates Created: {len(organized_duplicates['all_duplicates'])}")
    print(f"   • Total Duplicate Pairs Found: {len(duplicate_pairs)}")
    
    print(f"\n📈 DETECTION BREAKDOWN:")
    for _, row in summary.iterrows():
        print(f"   • {row['Type']} ({row['Detection_Status']}): {row['Count']} ({row['Percentage']:.1f}%)")
    
    # Calculate overall rates
    total_duplicates = len(organized_duplicates['all_duplicates'])
    total_detected = summary[summary['Detection_Status'] == 'Detected']['Count'].sum()
    overall_rate = (total_detected / total_duplicates * 100) if total_duplicates > 0 else 0
    
    print(f"\n🎯 OVERALL DETECTION RATE: {overall_rate:.1f}%")
    
    if len(duplicate_pairs) > 0:
        print(f"\n⏱️  TEMPORAL PATTERNS:")
        print(f"   • Average time between duplicates: {duplicate_pairs['Time_Difference_Hours'].mean():.1f} hours")
        print(f"   • Median time between duplicates: {duplicate_pairs['Time_Difference_Hours'].median():.1f} hours")
        print(f"   • Fastest duplicate: {duplicate_pairs['Time_Difference_Hours'].min():.2f} hours")
        print(f"   • Slowest duplicate: {duplicate_pairs['Time_Difference_Hours'].max():.1f} hours")

def run_complete_analysis(duplicate_pairs, impact_df, mixed_duplicates=None):
    """
    Run the complete analysis with duplicate type organization and visualization
    """
    print("🚀 Running Enhanced Duplicate Analysis...")
    
    if mixed_duplicates is None:
        print("⚠️ No mixed_duplicates provided. Using basic analysis.")
        # Fallback to original analysis
        display_basic_results(duplicate_pairs, impact_df)
        return
    
    # Organize duplicates by type
    organized_duplicates = organize_duplicates_by_type(duplicate_pairs, mixed_duplicates)
    
    # Display examples
    display_duplicate_examples(organized_duplicates)
    
    # Save to CSV
    save_duplicates_to_csv(organized_duplicates)
    
    # Create comprehensive visualization
    create_comprehensive_visualization(organized_duplicates, duplicate_pairs)
    
    # Display detailed summary
    display_detailed_summary(organized_duplicates, duplicate_pairs)
    
    print("\n✅ Enhanced analysis completed!")

def display_basic_results(duplicate_pairs, impact_df):
    """
    Fallback basic results display when mixed_duplicates is not available
    """
    print("=" * 80)
    print("DUPLICATE DETECTION RESULTS SUMMARY")
    print("=" * 80)
    
    print(f"\n📊 SUMMARY STATISTICS:")
    print(f"   • Total Duplicate Pairs Found: {len(duplicate_pairs)}")
    if len(duplicate_pairs) > 0:
        print(f"   • Average String Similarity: {duplicate_pairs['String_Similarity'].mean():.1f}%")
        print(f"   • Average Time Difference: {duplicate_pairs['Time_Difference_Hours'].mean():.1f} hours")
    
    if len(impact_df) > 0:
        print(f"   • Total Impact Analysis Records: {len(impact_df)}")