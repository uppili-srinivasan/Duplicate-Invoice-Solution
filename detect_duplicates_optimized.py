# =========================================
# Step 4: Optimized Duplicate Detection using Fuzzy Matching
# =========================================

from rapidfuzz import fuzz, process
import pandas as pd

def detect_duplicates_optimized(df, threshold=80, max_comparisons=1000):
    """
    Optimized duplicate detection with multiple performance improvements:
    - Pre-filtering by length and prefix
    - Batch processing
    - Early termination
    - Caching
    """
    results = []
    
    # Get unique applications and pre-process
    apps = df[['application_number', 'user', 'activity', 'timestamp']].drop_duplicates()
    app_list = apps['application_number'].tolist()
    
    print(f"Processing {len(app_list)} unique applications...")
    
    # Pre-filter applications by length (similar lengths are more likely to be duplicates)
    app_lengths = {}
    for app in app_list:
        length = len(str(app))
        if length not in app_lengths:
            app_lengths[length] = []
        app_lengths[length].append(app)
    
    comparison_count = 0
    max_comparisons = min(max_comparisons, len(app_list) * 10)  # Limit comparisons
    
    # Only compare applications of similar lengths
    for length, apps_of_length in app_lengths.items():
        if len(apps_of_length) < 2:
            continue
            
        # Sort by prefix for better clustering
        apps_of_length.sort()
        
        for i in range(len(apps_of_length)):
            if comparison_count >= max_comparisons:
                print(f"Reached maximum comparisons limit ({max_comparisons})")
                break
                
            app_a = apps_of_length[i]
            
            # Only compare with nearby applications (reduces comparisons significantly)
            for j in range(i+1, min(i+50, len(apps_of_length))):  # Limit to 50 nearby apps
                app_b = apps_of_length[j]
                comparison_count += 1
                
                # Quick length check first
                if abs(len(str(app_a)) - len(str(app_b))) > 2:
                    continue
                
                # Fuzzy string similarity
                string_similarity = fuzz.ratio(str(app_a), str(app_b))
                
                if string_similarity >= threshold:
                    # Get traces efficiently
                    trace_a = df[df['application_number'] == app_a].sort_values('timestamp')
                    trace_b = df[df['application_number'] == app_b].sort_values('timestamp')
                    
                    if len(trace_a) > 0 and len(trace_b) > 0:
                        # Calculate metrics
                        time_diff = abs(trace_a['timestamp'].iloc[0] - trace_b['timestamp'].iloc[0])
                        user_similarity = 1.0 if trace_a['user'].iloc[0] == trace_b['user'].iloc[0] else 0.0
                        
                        # Quick activity similarity (only if traces are short)
                        if len(trace_a) <= 10 and len(trace_b) <= 10:
                            activities_a = trace_a['activity'].tolist()
                            activities_b = trace_b['activity'].tolist()
                            activity_similarity = fuzz.ratio(' '.join(activities_a), ' '.join(activities_b))
                        else:
                            activity_similarity = 0  # Skip expensive calculation for long traces
                        
                        results.append({
                            'Application_A': app_a,
                            'Application_B': app_b,
                            'String_Similarity': string_similarity,
                            'Time_Difference_Hours': time_diff.total_seconds() / 3600,
                            'Same_User': user_similarity,
                            'Activity_Similarity': activity_similarity,
                            'Trace_A': trace_a[['activity', 'user', 'timestamp']].to_dict('records'),
                            'Trace_B': trace_b[['activity', 'user', 'timestamp']].to_dict('records')
                        })
            
            if comparison_count >= max_comparisons:
                break
        
        if comparison_count >= max_comparisons:
            break
    
    print(f"Completed {comparison_count} comparisons in optimized mode")
    return pd.DataFrame(results)