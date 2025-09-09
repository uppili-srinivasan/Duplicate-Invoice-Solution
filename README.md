# Duplicate-Invoice-Solution
AI-powered duplicate invoice detection enriched with process mining to uncover root causes and prevent financial leakage.

## 📌 Project Description
This project enhances traditional **duplicate invoice detection** by linking it to **process mining insights** using Purchase-to-Pay (P2P) event logs from the [4TU Data Centre (BPI Challenge)](https://data.4tu.nl/).

**Key Features:**
- **Mixed Duplicate Generation**: Creates realistic duplicates (fuzzy-detectable + non-fuzzy-detectable)
- **Fuzzy Matching Detection**: Detects typos, character variations, and similar strings
- **Process Mining Integration**: Correlates duplicates with end-to-end process traces
- **Root Cause Analysis**: Identifies why duplicates happen (manual entry, workflow deviations)
- **Comprehensive Visualization**: Single dashboard with detection insights and type breakdown

## 🎯 Duplicate Types

### 🔍 Fuzzy-Detectable Duplicates (60%)
- **Character Substitution**: `12345` → `12346` (typos)
- **Insertion/Deletion**: `12345` → `123456` or `1234`
- **Transposition**: `12345` → `12435`

### 🎯 Non-Fuzzy-Detectable Duplicates (40%)
- **Semantic Variations**: `12345` → `APP00012345` (different format)
- **System Variations**: `12345` → `WEB00012345` (different interface)
- **Format Variations**: `12345` → `SYS00012345` (system-specific)

## ⚙️ Quick Start

### 1) Setup
```bash
git clone https://github.com/uppili-srinivasan/Duplicate-Invoice-Solution.git
cd Duplicate-Invoice-Solution
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 2) Run Analysis
```bash
# Complete analysis with mixed duplicates
python main.py

# Demo with examples
python demo_mixed_duplicates.py

# Quick test
python test_mixed_duplicates.py
```

## 📊 Expected Results
- **Fuzzy-detectable**: 80-95% detection rate
- **Non-fuzzy-detectable**: 0-20% detection rate
- **Overall**: 50-70% detection rate
- **Output**: CSV files with duplicate types + comprehensive visualization

## 🔧 Core Files
- `main.py` - Complete analysis pipeline
- `create_mixed_duplicates.py` - Mixed duplicate generation
- `detect_duplicates_optimized.py` - Fuzzy matching detection
- `run_complete_analysis.py` - Enhanced analysis with type organization
- `demo_mixed_duplicates.py` - Demonstration script

## 📈 Output
- **CSV Files**: `output/duplicates_by_type.csv` (all duplicates with types)
- **Visualization**: Single dashboard with 4 subplots showing detection insights
- **Examples**: `df.head()` samples for each duplicate type

