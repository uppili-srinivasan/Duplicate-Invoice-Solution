# =========================================
# Quick Test: Mixed Duplicate Generation
# =========================================
import pandas as pd
from datetime import datetime, timedelta
from create_mixed_duplicates import create_mixed_duplicates, create_typo_variation, create_semantic_variation

def test_mixed_duplicates():
    """Quick test of the mixed duplicate generation functionality"""
    print("🧪 Testing Mixed Duplicate Generation")
    print("=" * 40)
    
    # Create sample data
    sample_data = pd.DataFrame({
        'application_id': [12345, 67890, 11111],
        'activity': ['A_SUBMITTED', 'A_SUBMITTED', 'A_SUBMITTED'],
        'user': ['User1', 'User2', 'User3'],
        'timestamp': [
            datetime.now(),
            datetime.now() + timedelta(hours=1),
            datetime.now() + timedelta(hours=2)
        ]
    })
    
    print(f"📊 Sample data: {len(sample_data)} records")
    print("   Application IDs:", sample_data['application_id'].tolist())
    
    # Test individual variation functions
    print("\n🔧 Testing variation functions:")
    
    # Test typo variation
    test_num = "12345"
    typo_variation = create_typo_variation(test_num)
    print(f"   Typo variation: {test_num} → {typo_variation}")
    
    # Test semantic variation
    semantic_variation = create_semantic_variation(test_num)
    print(f"   Semantic variation: {test_num} → {semantic_variation}")
    
    # Test mixed duplicate generation
    print("\n🎯 Testing mixed duplicate generation:")
    mixed_duplicates = create_mixed_duplicates(
        sample_data, 
        num_duplicates=6,  # Small number for testing
        fuzzy_detectable_ratio=0.5  # 50/50 split
    )
    
    print(f"✅ Generated {len(mixed_duplicates)} duplicate records")
    
    # Show breakdown
    fuzzy_count = len(mixed_duplicates[mixed_duplicates['duplicate_type'] == 'fuzzy_detectable'])
    non_fuzzy_count = len(mixed_duplicates[mixed_duplicates['duplicate_type'] == 'non_fuzzy_detectable'])
    
    print(f"   📊 Breakdown:")
    print(f"      - Fuzzy-detectable: {fuzzy_count}")
    print(f"      - Non-fuzzy-detectable: {non_fuzzy_count}")
    
    # Show examples
    print(f"\n🔍 Examples:")
    for _, row in mixed_duplicates.head(3).iterrows():
        original_id = row['original_application_id']
        duplicate_id = row['application_number']
        dup_type = row['duplicate_type']
        variation = row['variation_type']
        print(f"      {original_id} → {duplicate_id} ({dup_type}, {variation})")
    
    print("\n✅ Test completed successfully!")
    return mixed_duplicates

if __name__ == "__main__":
    test_mixed_duplicates()
