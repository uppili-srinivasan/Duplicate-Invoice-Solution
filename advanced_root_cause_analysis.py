# =========================================
# Step 5: Advanced Root Cause Analysis
# =========================================
def advanced_root_cause_analysis(row):
    """
    Advanced root cause analysis based on multiple factors:
    - Temporal patterns
    - User behavior
    - Application number patterns
    - Activity sequences
    """
    app_a, app_b = row['Application_A'], row['Application_B']
    time_diff = row['Time_Difference_Hours']
    same_user = row['Same_User']
    string_sim = row['String_Similarity']
    activity_sim = row['Activity_Similarity']
    
    # Rule 1: Manual re-entry by same user (typos, corrections)
    if same_user and time_diff <= 1.0 and string_sim >= 85:
        return "Manual re-entry by same user (likely typo/correction)"
    
    # Rule 2: Collaborative entry by different users
    elif not same_user and time_diff <= 2.0 and string_sim >= 80:
        return "Collaborative entry by multiple users"
    
    # Rule 3: System retry/retransmission
    elif (app_a.startswith('R') or app_b.startswith('R')) and time_diff >= 2.0:
        return "System retry/retransmission"
    
    # Rule 4: Data migration/import issues
    elif time_diff >= 24 and activity_sim >= 90:
        return "Data migration/import duplicate"
    
    # Rule 5: Process workflow duplication
    elif time_diff <= 0.5 and activity_sim >= 95:
        return "Process workflow duplication"
    
    # Rule 6: User training/testing
    elif string_sim >= 90 and time_diff <= 0.1:
        return "User training/testing scenario"
    
    else:
        return "Complex duplicate scenario requiring manual review"