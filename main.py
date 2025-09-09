import pm4py
import pandas as pd
from rapidfuzz import fuzz, process
from datetime import timedelta
from create_mixed_duplicates import create_mixed_duplicates, analyze_duplicate_detectability
from detect_duplicates_optimized import detect_duplicates_optimized
from advanced_root_cause_analysis import advanced_root_cause_analysis
from analyze_duplicate_impact import analyze_duplicate_impact
from run_complete_analysis import run_complete_analysis

xes_file = "data/BPI_Challenge_2012.xes"  

log = pm4py.read_xes(xes_file)
df = pm4py.convert_to_dataframe(log)

# Keep only activities related to the loan application (those starting with "A_")
application_df = df[df['concept:name'].str.startswith("A_", na=False)].copy()

# Keep only relevant fields
application_df = application_df[['case:concept:name', 'concept:name', 'org:resource', 'time:timestamp']]
application_df = application_df.rename(columns={
    'case:concept:name': 'application_id',
    'concept:name': 'activity',
    'org:resource': 'user',
    'time:timestamp': 'timestamp'
})

# Create mixed duplicates (fuzzy-detectable and non-fuzzy-detectable)
print("🔧 Creating mixed duplicates...")
print("   - 60% fuzzy-detectable (typos, character variations)")
print("   - 40% non-fuzzy-detectable (semantic duplicates)")
mixed_duplicates = create_mixed_duplicates(application_df, num_duplicates=20, fuzzy_detectable_ratio=0.6)

# Add metadata to original data
application_df['application_number'] = application_df['application_id'].astype(str)
application_df['duplicate_type'] = 'original'
application_df['variation_type'] = 'original'
application_df['original_application_id'] = application_df['application_id']

# Combine original and duplicate data
combined_apps = pd.concat([application_df, mixed_duplicates], ignore_index=True)

# Detect duplicates with optimized analysis
duplicate_pairs = detect_duplicates_optimized(combined_apps, threshold=80, max_comparisons=5000)

# Analyze detection effectiveness
print("\n📈 Analyzing detection effectiveness...")
detection_analysis = analyze_duplicate_detectability(mixed_duplicates, duplicate_pairs)

# Apply advanced root cause analysis
duplicate_pairs['Root_Cause'] = duplicate_pairs.apply(advanced_root_cause_analysis, axis=1)

# Perform impact analysis
impact_df = analyze_duplicate_impact(combined_apps, duplicate_pairs)

# Run the complete analysis
print("🚀 Running Complete Duplicate Analysis...")
run_complete_analysis(duplicate_pairs, impact_df, mixed_duplicates)

# Show mixed duplicate analysis results
print(f"\n📊 Mixed Duplicate Analysis Summary:")
print(f"   • Total duplicates created: {len(mixed_duplicates)}")
print(f"   • Fuzzy-detectable: {detection_analysis['total_fuzzy_duplicates']} "
      f"({detection_analysis['fuzzy_detection_rate']:.1%} detected)")
print(f"   • Non-fuzzy-detectable: {detection_analysis['total_non_fuzzy_duplicates']} "
      f"({detection_analysis['non_fuzzy_detection_rate']:.1%} detected)")
print(f"   • Total duplicate pairs found: {len(duplicate_pairs)}")