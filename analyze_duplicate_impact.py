# =========================================
# Step 6: Duplicate Impact Analysis and Recommendations
# =========================================
import pandas as pd

def analyze_duplicate_impact(df, duplicate_pairs):
    """
    Analyze the business impact of duplicates and provide recommendations
    """
    impact_analysis = []
    
    for idx, row in duplicate_pairs.iterrows():
        app_a, app_b = row['Application_A'], row['Application_B']
        root_cause = row['Root_Cause']
        
        # Get application amounts (if available in original data)
        amount_a = df[df['application_number'] == app_a]['case:AMOUNT_REQ'].iloc[0] if 'case:AMOUNT_REQ' in df.columns else 0
        amount_b = df[df['application_number'] == app_b]['case:AMOUNT_REQ'].iloc[0] if 'case:AMOUNT_REQ' in df.columns else 0
        
        # Calculate risk level
        if root_cause in ["Manual re-entry by same user", "User training/testing scenario"]:
            risk_level = "Low"
            recommendation = "Implement input validation and auto-save features"
        elif root_cause in ["Collaborative entry by multiple users", "Process workflow duplication"]:
            risk_level = "Medium"
            recommendation = "Implement real-time duplicate checking and user coordination"
        elif root_cause in ["System retry/retransmission", "Data migration/import duplicate"]:
            risk_level = "High"
            recommendation = "Review system integration and data migration processes"
        else:
            risk_level = "Critical"
            recommendation = "Immediate manual review and process audit required"
        
        impact_analysis.append({
            'Application_A': app_a,
            'Application_B': app_b,
            'Root_Cause': root_cause,
            'Risk_Level': risk_level,
            'Potential_Financial_Impact': max(amount_a, amount_b),
            'Recommendation': recommendation,
            'Time_Difference_Hours': row['Time_Difference_Hours']
        })
    
    return pd.DataFrame(impact_analysis)