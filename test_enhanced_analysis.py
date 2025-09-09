# =========================================
# Test Enhanced Analysis with Duplicate Type Organization
# =========================================
import pandas as pd
from datetime import datetime, timedelta
from create_mixed_duplicates import create_mixed_duplicates
from detect_duplicates_optimized import detect_duplicates_optimized
from run_complete_analysis import run_complete_analysis

def test_enhanced_analysis():
    """Test the enhanced analysis with duplicate type organization"""
    print("🧪 Testing Enhanced Analysis with Duplicate Type Organization")
    print("=" * 60)
    
    # Create sample data
    sample_data = pd.DataFrame({
        'application_id': [12345, 67890, 11111, 22222, 33333],
        'activity': ['A_SUBMITTED', 'A_SUBMITTED', 'A_SUBMITTED', 'A_SUBMITTED', 'A_SUBMITTED'],
        'user': ['User1', 'User2', 'User3', 'User4', 'User5'],
        'timestamp': [
            datetime.now(),
            datetime.now() + timedelta(hours=1),
            datetime.now() + timedelta(hours=2),
            datetime.now() + timedelta(hours=3),
            datetime.now() + timedelta(hours=4)
        ]
    })
    
    print(f"📊 Sample data: {len(sample_data)} records")
    
    # Add application_number to original data
    sample_data['application_number'] = sample_data['application_id'].astype(str)
    sample_data['duplicate_type'] = 'original'
    sample_data['variation_type'] = 'original'
    sample_data['original_application_id'] = sample_data['application_id']
    
    # Create mixed duplicates
    print("\n🔧 Creating mixed duplicates...")
    mixed_duplicates = create_mixed_duplicates(
        sample_data, 
        num_duplicates=12,  # Create 12 duplicates
        fuzzy_detectable_ratio=0.6  # 60% fuzzy-detectable
    )
    
    print(f"✅ Created {len(mixed_duplicates)} duplicate records")
    
    # Combine data
    combined_data = pd.concat([sample_data, mixed_duplicates], ignore_index=True)
    print(f"📊 Combined dataset: {len(combined_data)} records")
    
    # Run duplicate detection
    print("\n🔍 Running duplicate detection...")
    duplicate_pairs = detect_duplicates_optimized(
        combined_data, 
        threshold=80, 
        max_comparisons=1000
    )
    
    print(f"✅ Found {len(duplicate_pairs)} duplicate pairs")
    
    # Create dummy impact analysis (since we don't have the full impact analysis module)
    impact_df = pd.DataFrame({
        'Application_A': [f"App_{i}" for i in range(len(duplicate_pairs))],
        'Application_B': [f"App_{i+100}" for i in range(len(duplicate_pairs))],
        'Risk_Level': ['Medium'] * len(duplicate_pairs),
        'Potential_Financial_Impact': [1000] * len(duplicate_pairs),
        'Recommendation': ['Review and merge'] * len(duplicate_pairs)
    })
    
    # Run enhanced analysis
    print("\n🚀 Running enhanced analysis...")
    run_complete_analysis(duplicate_pairs, impact_df, mixed_duplicates)
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_enhanced_analysis()
