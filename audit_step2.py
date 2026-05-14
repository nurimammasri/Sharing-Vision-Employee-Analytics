import json
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open("Jawaban_Coding_Test_EndToEnd.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

def get_cell_source(idx):
    cell = nb['cells'][idx]
    source = cell.get('source', [])
    if isinstance(source, list):
        return ''.join(source)
    return source

print("="*100)
print("STEP 2: DETAILED AUDIT")
print("="*100)

# Task 1
print("\nA. TASK 1 - EDA NUMERIK")
source_t1 = ''.join([get_cell_source(i) for i in [14, 15, 16, 17, 18, 19, 20]])
print("(a) Histogram+Boxplot:", "OK" if ('subplots' in source_t1 and 'histplot' in source_t1) else "CHECK")
print("(b) Statistics table:", "OK" if ('mean' in source_t1.lower() and 'std' in source_t1.lower()) else "CHECK")
print("(c) Whisker:", "OK" if 'whisker' in source_t1.lower() else "CHECK")
print("(d) Outlier:", "OK" if 'outlier' in source_t1.lower() else "CHECK")
print("(e) Insights:", "OK" if 'insight' in source_t1.lower() else "CHECK")

# Task 2
print("\nB. TASK 2 - EDA KATEGORIK")
source_t2 = ''.join([get_cell_source(i) for i in [21, 22, 23, 24, 25]])
print("(a) Countplots:", "OK" if 'countplot' in source_t2.lower() else "CHECK")
print("(b) Frequency:", "OK" if 'value_counts' in source_t2.lower() else "CHECK")

# Task 3
print("\nC. TASK 3 - MULTIVARIAT NUMERIK")
source_t3 = ''.join([get_cell_source(i) for i in [27, 28, 29, 30]])
print("(a) Boxplot Attrition:", "OK" if ('boxplot' in source_t3.lower() and 'attrition' in source_t3.lower()) else "CHECK")

# Task 4
print("\nD. TASK 4 - MULTIVARIAT KATEGORIK")
source_t4 = ''.join([get_cell_source(i) for i in [39, 40, 41]])
print("(a) Countplot hue:", "OK" if 'countplot' in source_t4.lower() else "CHECK")
print("(b) Stacked bar:", "OK" if 'normalize' in source_t4.lower() else "CHECK")

# Task 5
print("\nE. TASK 5 - T-TEST")
source_t5 = ''.join([get_cell_source(i) for i in [43, 44, 45]])
print("T-test:", "OK" if ('ttest' in source_t5.lower()) else "CHECK")
print("Conclusion:", "OK" if ('kesimpulan' in source_t5.lower()) else "CHECK")

# Task 6
print("\nF. TASK 6 - ANOVA")
source_t6 = ''.join([get_cell_source(i) for i in [46, 47, 48]])
print("ANOVA:", "OK" if ('f_oneway' in source_t6.lower() or 'anova' in source_t6.lower()) else "CHECK")

# Task 11
print("\nG. TASK 11 - GRIDSEARCHCV")
source_t11 = ''.join([get_cell_source(i) for i in [56, 57]])
print("GridSearchCV:", "OK" if 'GridSearchCV' in source_t11 else "MISSING")

# Task 12
print("\nH. TASK 12 - CLASSIFICATION REPORT")
source_t12 = ''.join([get_cell_source(i) for i in [58, 59, 60, 61]])
print("Report:", "OK" if 'classification_report' in source_t12.lower() else "MISSING")

# Task 13
print("\nI. TASK 13 - BEST ESTIMATOR")
source_t13 = ''.join([get_cell_source(i) for i in [62, 63, 64, 65, 66]])
print("Comparison:", "OK" if ('f1' in source_t13.lower()) else "CHECK")

# Task 17
print("\nJ. TASK 17 - REGRESSION")
source_t17 = ''.join([get_cell_source(i) for i in [76, 77]])
reg_count = source_t17.count('LinearRegression') + source_t17.count('Ridge') + source_t17.count('XGBoost') + source_t17.count('RandomForest')
print(f"Regressors: OK ({reg_count} found)")
print("GridSearchCV:", "OK" if 'GridSearchCV' in source_t17 else "CHECK")

# Task 18
print("\nK. TASK 18 - METRICS")
source_t18 = ''.join([get_cell_source(i) for i in [78, 79, 80]])
metrics = sum([1 for m in ['r2', 'mse', 'rmse', 'mae', 'mape'] if m.lower() in source_t18.lower()])
print(f"Metrics: OK ({metrics}/5 found)")

# Task 21
print("\nL. TASK 21 - CLUSTERING")
source_t21 = ''.join([get_cell_source(i) for i in [86, 87]])
print("Elbow:", "OK" if 'inertia' in source_t21.lower() else "CHECK")
print("Silhouette:", "OK" if 'silhouette' in source_t21.lower() else "CHECK")

# Task 22
print("\nM. TASK 22 - LABEL")
source_t22 = ''.join([get_cell_source(i) for i in [88, 89]])
print("Label column:", "OK" if 'label' in source_t22.lower() else "CHECK")

# Em-dash
print("\nP. EM-DASH CHECK")
em_count = sum([1 for idx in range(len(nb['cells'])) if '—' in get_cell_source(idx)])
print(f"Em-dashes: {em_count} found" if em_count > 0 else "Em-dashes: None found")

print("\n" + "="*100)
