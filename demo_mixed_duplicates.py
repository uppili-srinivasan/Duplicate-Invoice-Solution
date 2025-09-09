# =========================================
# Demo: Mixed Duplicate Generation and Analysis
# =========================================
import pm4py
import pandas as pd
from create_mixed_duplicates import create_mixed_duplicates, analyze_duplicate_detectability
from detect_duplicates_optimized import detect_duplicates_optimized

def run_mixed_duplicate_demo():
    """
    Demonstrate the mixed duplicate generation and analysis
    """
    print("🚀 Mixed Duplicate Generation Demo")
    print("=" * 50)
    
    # Load the original data
    print("📁 Loading original data...")
    xes_file = "data/BPI_Challenge_2012.xes"
    log = pm4py.read_xes(xes_file)
    df = pm4py.convert_to_dataframe(log)
    
    # Keep only activities related to the loan application
    application_df = df[df['concept:name'].str.startswith("A_", na=False)].copy()
    application_df = application_df[['case:concept:name', 'concept:name', 'org:resource', 'time:timestamp']]
    application_df = application_df.rename(columns={
        'case:concept:name': 'application_id',
        'concept:name': 'activity',
        'org:resource': 'user',
        'time:timestamp': 'timestamp'
    })
    
    # Add application_number to original data
    application_df['application_number'] = application_df['application_id'].astype(str)
    application_df['duplicate_type'] = 'original'
    application_df['variation_type'] = 'original'
    application_df['original_application_id'] = application_df['application_id']
    
    print(f"✅ Loaded {len(application_df)} original application records")
    
    # Create mixed duplicates
    print("\n🔧 Creating mixed duplicates...")
    print("   - 60% fuzzy-detectable (typos, character variations)")
    print("   - 40% non-fuzzy-detectable (semantic duplicates)")
    
    mixed_duplicates = create_mixed_duplicates(
        application_df, 
        num_duplicates=30,  # Create 30 duplicate applications
        fuzzy_detectable_ratio=0.6  # 60% fuzzy-detectable, 40% non-fuzzy-detectable
    )
    
    print(f"✅ Created {len(mixed_duplicates)} duplicate records")
    
    # Show breakdown by type
    fuzzy_count = len(mixed_duplicates[mixed_duplicates['duplicate_type'] == 'fuzzy_detectable'])
    non_fuzzy_count = len(mixed_duplicates[mixed_duplicates['duplicate_type'] == 'non_fuzzy_detectable'])
    
    print(f"   📊 Breakdown:")
    print(f"      - Fuzzy-detectable: {fuzzy_count} records")
    print(f"      - Non-fuzzy-detectable: {non_fuzzy_count} records")
    
    # Combine original and duplicate data
    print("\n🔗 Combining original and duplicate data...")
    combined_data = pd.concat([application_df, mixed_duplicates], ignore_index=True)
    print(f"✅ Total dataset: {len(combined_data)} records")
    
    # Run duplicate detection
    print("\n🔍 Running fuzzy matching duplicate detection...")
    detection_results = detect_duplicates_optimized(
        combined_data, 
        threshold=80,  # 80% similarity threshold
        max_comparisons=10000
    )
    
    print(f"✅ Found {len(detection_results)} duplicate pairs")
    
    # Analyze detection effectiveness
    print("\n📈 Analyzing detection effectiveness...")
    analysis_results = analyze_duplicate_detectability(mixed_duplicates, detection_results)
    
    # Show detailed results
    print("\n📋 Detailed Results:")
    print(f"   Fuzzy-detectable duplicates:")
    print(f"      - Total created: {analysis_results['total_fuzzy_duplicates']}")
    print(f"      - Detected: {analysis_results['detected_fuzzy']}")
    print(f"      - Detection rate: {analysis_results['fuzzy_detection_rate']:.1%}")
    
    print(f"   Non-fuzzy-detectable duplicates:")
    print(f"      - Total created: {analysis_results['total_non_fuzzy_duplicates']}")
    print(f"      - Detected: {analysis_results['detected_non_fuzzy']}")
    print(f"      - Detection rate: {analysis_results['non_fuzzy_detection_rate']:.1%}")
    
    # Show examples of each type
    print("\n🔍 Examples of created duplicates:")
    
    # Show fuzzy-detectable examples
    fuzzy_examples = mixed_duplicates[mixed_duplicates['duplicate_type'] == 'fuzzy_detectable'].head(3)
    print("\n   Fuzzy-detectable examples:")
    for _, row in fuzzy_examples.iterrows():
        original_id = row['original_application_id']
        duplicate_id = row['application_number']
        variation_type = row['variation_type']
        detected = "✅ DETECTED" if row['was_detected'] else "❌ NOT DETECTED"
        print(f"      {original_id} → {duplicate_id} ({variation_type}) {detected}")
    
    # Show non-fuzzy-detectable examples
    non_fuzzy_examples = mixed_duplicates[mixed_duplicates['duplicate_type'] == 'non_fuzzy_detectable'].head(3)
    print("\n   Non-fuzzy-detectable examples:")
    for _, row in non_fuzzy_examples.iterrows():
        original_id = row['original_application_id']
        duplicate_id = row['application_number']
        variation_type = row['variation_type']
        detected = "✅ DETECTED" if row['was_detected'] else "❌ NOT DETECTED"
        print(f"      {original_id} → {duplicate_id} ({variation_type}) {detected}")
    
    # Show detected pairs
    if len(detection_results) > 0:
        print(f"\n🎯 Sample detected duplicate pairs:")
        for i, (_, row) in enumerate(detection_results.head(3).iterrows()):
            print(f"      {i+1}. {row['Application_A']} ↔ {row['Application_B']} "
                  f"(similarity: {row['String_Similarity']:.1f}%)")
    
    # Summary insights
    print(f"\n💡 Key Insights:")
    print(f"   • Fuzzy matching successfully detects most typo-based duplicates")
    print(f"   • Semantic duplicates (different formats) are harder to detect")
    print(f"   • Mixed approach provides realistic duplicate scenarios")
    print(f"   • Detection rate varies significantly by duplicate type")
    
    return {
        'original_data': application_df,
        'mixed_duplicates': mixed_duplicates,
        'combined_data': combined_data,
        'detection_results': detection_results,
        'analysis_results': analysis_results
    }

if __name__ == "__main__":
    results = run_mixed_duplicate_demo()
    print("\n🎉 Demo completed successfully!")
