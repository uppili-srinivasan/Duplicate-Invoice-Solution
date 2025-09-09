# =========================================
# Enhanced Duplicate Generation: Mixed Types
# =========================================
import random
import pandas as pd
from datetime import timedelta
import string

def create_mixed_duplicates(df, num_duplicates=20, fuzzy_detectable_ratio=0.6):
    """
    Create a mixture of duplicates:
    1. Fuzzy-detectable duplicates (typos, character variations, similar strings)
    2. Non-fuzzy-detectable duplicates (semantic duplicates, different representations)
    
    Args:
        df: Original dataframe
        num_duplicates: Total number of duplicate applications to create
        fuzzy_detectable_ratio: Ratio of fuzzy-detectable vs non-fuzzy-detectable duplicates
    
    Returns:
        DataFrame with mixed duplicates and metadata
    """
    duplicates = []
    
    # Calculate split
    num_fuzzy_detectable = int(num_duplicates * fuzzy_detectable_ratio)
    num_non_fuzzy_detectable = num_duplicates - num_fuzzy_detectable
    
    # Get unique applications to duplicate
    unique_apps = df['application_id'].unique()
    apps_to_duplicate = random.sample(list(unique_apps), min(num_duplicates, len(unique_apps)))
    
    print(f"Creating {num_fuzzy_detectable} fuzzy-detectable and {num_non_fuzzy_detectable} non-fuzzy-detectable duplicates")
    
    # Create fuzzy-detectable duplicates
    fuzzy_apps = apps_to_duplicate[:num_fuzzy_detectable]
    for app_id in fuzzy_apps:
        original_app = df[df['application_id'] == app_id].copy()
        
        # Create 2-3 fuzzy-detectable variations
        for variation_type in range(1, 4):
            dup_app = original_app.copy()
            base_num = str(app_id)
            
            if variation_type == 1:
                # Type 1: Character substitution (typos)
                new_num = create_typo_variation(base_num)
                dup_app['application_id'] = new_num
                dup_app['application_number'] = new_num
                
                # Slight time variation
                time_offset = timedelta(minutes=random.randint(5, 30))
                dup_app['timestamp'] = dup_app['timestamp'] + time_offset
                
            elif variation_type == 2:
                # Type 2: Character insertion/deletion
                new_num = create_insertion_deletion_variation(base_num)
                dup_app['application_id'] = new_num
                dup_app['application_number'] = new_num
                
                # Different user, similar time
                available_users = df['user'].dropna().unique()
                dup_app['user'] = random.choice([u for u in available_users if u != dup_app['user'].iloc[0]])
                time_offset = timedelta(minutes=random.randint(10, 60))
                dup_app['timestamp'] = dup_app['timestamp'] + time_offset
                
            else:
                # Type 3: Character transposition
                new_num = create_transposition_variation(base_num)
                dup_app['application_id'] = new_num
                dup_app['application_number'] = new_num
                
                # Same user, later time
                time_offset = timedelta(hours=random.randint(1, 3))
                dup_app['timestamp'] = dup_app['timestamp'] + time_offset
            
            # Add metadata
            dup_app['duplicate_type'] = 'fuzzy_detectable'
            dup_app['variation_type'] = f'fuzzy_{variation_type}'
            dup_app['original_application_id'] = app_id
            duplicates.append(dup_app)
    
    # Create non-fuzzy-detectable duplicates
    non_fuzzy_apps = apps_to_duplicate[num_fuzzy_detectable:num_fuzzy_detectable + num_non_fuzzy_detectable]
    for app_id in non_fuzzy_apps:
        original_app = df[df['application_id'] == app_id].copy()
        
        # Create 2-3 non-fuzzy-detectable variations
        for variation_type in range(1, 4):
            dup_app = original_app.copy()
            base_num = str(app_id)
            
            if variation_type == 1:
                # Type 1: Completely different number format (semantic duplicate)
                new_num = create_semantic_variation(base_num)
                dup_app['application_id'] = new_num
                dup_app['application_number'] = new_num
                
                # Different user, different time
                available_users = df['user'].dropna().unique()
                dup_app['user'] = random.choice([u for u in available_users if u != dup_app['user'].iloc[0]])
                time_offset = timedelta(hours=random.randint(2, 8))
                dup_app['timestamp'] = dup_app['timestamp'] + time_offset
                
            elif variation_type == 2:
                # Type 2: Different encoding/format (same logical application)
                new_num = create_format_variation(base_num)
                dup_app['application_id'] = new_num
                dup_app['application_number'] = new_num
                
                # Same user, much later (system retry with different format)
                time_offset = timedelta(days=random.randint(1, 3))
                dup_app['timestamp'] = dup_app['timestamp'] + time_offset
                
            else:
                # Type 3: Different system/interface entry (same business case)
                new_num = create_system_variation(base_num)
                dup_app['application_id'] = new_num
                dup_app['application_number'] = new_num
                
                # Different user, similar business time
                available_users = df['user'].dropna().unique()
                dup_app['user'] = random.choice([u for u in available_users if u != dup_app['user'].iloc[0]])
                time_offset = timedelta(hours=random.randint(1, 6))
                dup_app['timestamp'] = dup_app['timestamp'] + time_offset
            
            # Add metadata
            dup_app['duplicate_type'] = 'non_fuzzy_detectable'
            dup_app['variation_type'] = f'non_fuzzy_{variation_type}'
            dup_app['original_application_id'] = app_id
            duplicates.append(dup_app)
    
    return pd.concat(duplicates, ignore_index=True)

def create_typo_variation(base_num):
    """Create typo variations that are fuzzy-detectable"""
    if len(base_num) < 3:
        return base_num
    
    # Randomly substitute one character
    pos = random.randint(0, len(base_num) - 1)
    if base_num[pos].isdigit():
        # Replace digit with another digit
        new_digit = str((int(base_num[pos]) + random.randint(1, 9)) % 10)
        return base_num[:pos] + new_digit + base_num[pos+1:]
    else:
        # Replace letter with similar letter
        similar_chars = {
            'a': 'e', 'e': 'a', 'i': 'o', 'o': 'i', 'u': 'o',
            'b': 'd', 'd': 'b', 'p': 'q', 'q': 'p',
            'n': 'm', 'm': 'n', 'w': 'v', 'v': 'w'
        }
        char = base_num[pos].lower()
        if char in similar_chars:
            replacement = similar_chars[char]
            if base_num[pos].isupper():
                replacement = replacement.upper()
            return base_num[:pos] + replacement + base_num[pos+1:]
        else:
            return base_num

def create_insertion_deletion_variation(base_num):
    """Create insertion/deletion variations that are fuzzy-detectable"""
    if len(base_num) < 2:
        return base_num
    
    operation = random.choice(['insert', 'delete'])
    
    if operation == 'insert' and len(base_num) < 10:
        # Insert a character
        pos = random.randint(0, len(base_num))
        char = random.choice(string.digits + string.ascii_letters)
        return base_num[:pos] + char + base_num[pos:]
    else:
        # Delete a character
        pos = random.randint(0, len(base_num) - 1)
        return base_num[:pos] + base_num[pos+1:]

def create_transposition_variation(base_num):
    """Create transposition variations that are fuzzy-detectable"""
    if len(base_num) < 2:
        return base_num
    
    # Swap two adjacent characters
    pos = random.randint(0, len(base_num) - 2)
    chars = list(base_num)
    chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
    return ''.join(chars)

def create_semantic_variation(base_num):
    """Create semantic variations that are NOT fuzzy-detectable"""
    # Convert to completely different format but same logical meaning
    if base_num.isdigit():
        # Convert number to different base or format
        num = int(base_num)
        # Create a different representation (e.g., add prefix, different encoding)
        return f"APP{num:06d}"  # Different format
    else:
        # For non-numeric, create a different encoding
        return f"REQ{hash(base_num) % 100000:05d}"

def create_format_variation(base_num):
    """Create format variations that are NOT fuzzy-detectable"""
    # Different system format but same application
    if base_num.isdigit():
        num = int(base_num)
        # Different system encoding
        return f"SYS{num:08d}"
    else:
        # Different format
        return f"REF{hash(base_num) % 10000:04d}"

def create_system_variation(base_num):
    """Create system variations that are NOT fuzzy-detectable"""
    # Different system/interface entry
    if base_num.isdigit():
        num = int(base_num)
        # Different system prefix
        return f"WEB{num:07d}"
    else:
        # Different system encoding
        return f"MOB{hash(base_num) % 1000:03d}"

def analyze_duplicate_detectability(duplicates_df, detection_results):
    """
    Analyze which duplicates were detected vs not detected
    """
    # Add detection status to duplicates
    duplicates_df['was_detected'] = False
    duplicates_df['detection_method'] = 'none'
    
    # Check which duplicates were detected
    for _, row in detection_results.iterrows():
        app_a = str(row['Application_A'])
        app_b = str(row['Application_B'])
        
        # Mark as detected
        duplicates_df.loc[duplicates_df['application_number'] == app_a, 'was_detected'] = True
        duplicates_df.loc[duplicates_df['application_number'] == app_b, 'was_detected'] = True
        duplicates_df.loc[duplicates_df['application_number'] == app_a, 'detection_method'] = 'fuzzy_matching'
        duplicates_df.loc[duplicates_df['application_number'] == app_b, 'detection_method'] = 'fuzzy_matching'
    
    # Analyze detection rates
    fuzzy_detectable = duplicates_df[duplicates_df['duplicate_type'] == 'fuzzy_detectable']
    non_fuzzy_detectable = duplicates_df[duplicates_df['duplicate_type'] == 'non_fuzzy_detectable']
    
    fuzzy_detection_rate = fuzzy_detectable['was_detected'].mean() if len(fuzzy_detectable) > 0 else 0
    non_fuzzy_detection_rate = non_fuzzy_detectable['was_detected'].mean() if len(non_fuzzy_detectable) > 0 else 0
    
    print(f"\n📊 Duplicate Detection Analysis:")
    print(f"Fuzzy-detectable duplicates: {len(fuzzy_detectable)} total, {fuzzy_detection_rate:.1%} detected")
    print(f"Non-fuzzy-detectable duplicates: {len(non_fuzzy_detectable)} total, {non_fuzzy_detection_rate:.1%} detected")
    
    return {
        'fuzzy_detection_rate': fuzzy_detection_rate,
        'non_fuzzy_detection_rate': non_fuzzy_detection_rate,
        'total_fuzzy_duplicates': len(fuzzy_detectable),
        'total_non_fuzzy_duplicates': len(non_fuzzy_detectable),
        'detected_fuzzy': fuzzy_detectable['was_detected'].sum(),
        'detected_non_fuzzy': non_fuzzy_detectable['was_detected'].sum()
    }

if __name__ == "__main__":
    # Example usage
    print("🔧 Mixed Duplicate Generator")
    print("This module creates both fuzzy-detectable and non-fuzzy-detectable duplicates")
