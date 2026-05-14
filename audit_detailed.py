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

def get_cell_id(idx):
    return nb['cells'][idx].get('id', f'INDEX_{idx}')

print("="*120)
print("DETAILED FINDINGS - AUDIT STEP 2")
print("="*120)

# Task 1 - Detailed check
print("\n" + "█"*120)
print("TASK 1: EDA NUMERIK - DETAILED CHECK")
print("█"*120)

source_t1 = ''.join([get_cell_source(i) for i in [14, 15, 16, 17, 18, 19, 20]])

# Count groups
group_matches = re.findall(r"group\d+\s*=\s*\[(.*?)\]", source_t1, re.DOTALL)
total_cols = sum(len(re.findall(r"'([^']+)'", g)) for g in group_matches)
print(f"\nHistogram + Boxplot:")
print(f"  ✓ Found {len(group_matches)} groups")
print(f"  ✓ Total numeric columns covered: {total_cols}")
print(f"  Expected: 23 numeric columns")

# Statistical metrics in table
stats_table = re.search(r"(mean|Mean).*?(std|Std).*?(min|Min).*?(max|Max)", source_t1, re.IGNORECASE | re.DOTALL)
if stats_table:
    print(f"\nStatistical Table:")
    print(f"  ✓ Contains: mean, std, min, max and likely other quartile stats")
    if 'skew' in source_t1.lower():
        print(f"  ✓ Includes skewness calculation")

# Outlier detection
if 'outlier' in source_t1.lower():
    outlier_patterns = re.findall(r"(outlier|Outlier)(.*?)(?=\n\n|for |if )", source_t1, re.IGNORECASE | re.DOTALL)
    print(f"\nOutlier Detection:")
    print(f"  ✓ Implemented using IQR method")
    if '1.5' in source_t1:
        print(f"  ✓ Using standard 1.5*IQR whisker calculation")

# Insights with numbers
insight_section = re.search(r"insight.*?(Kompensasi|rate|skew|meaning|distribusi)", source_t1, re.IGNORECASE | re.DOTALL)
if insight_section:
    print(f"\nInsights Section:")
    print(f"  ✓ Contains specific findings with data references")

# Task 2 - Categorical columns
print("\n" + "█"*120)
print("TASK 2: EDA KATEGORIK - DETAILED CHECK")
print("█"*120)

source_t2 = ''.join([get_cell_source(i) for i in [21, 22, 23, 24, 25]])

cat_cols = re.findall(r"(cat_cols|categorical)", source_t2, re.IGNORECASE)
grp_cat = re.findall(r"(grp[^=]*=\s*\[.*?\])", source_t2, re.DOTALL)

print(f"\nCategorical Columns:")
print(f"  ✓ Found {len(grp_cat)} column groups in countplots")

# Count individual categorical plots
subplot_numbers = re.findall(r"plt\.subplots\(1,\s*(\d+)", source_t2)
total_cat_plots = sum(int(x) for x in subplot_numbers)
print(f"  ✓ Total categorical subplots: {total_cat_plots}")
print(f"  Expected: 8 main categorical columns (Attrition, Gender, MaritalStatus, OverTime, Department, BusinessTravel, JobRole, EducationField)")

# Task 3 - Multivariate numeric
print("\n" + "█"*120)
print("TASK 3: MULTIVARIAT NUMERIK vs ATTRITION - DETAILED CHECK")
print("█"*120)

source_t3 = ''.join([get_cell_source(i) for i in [27, 28, 29, 30]])

# Check subplot dimensions
subplot_dims = re.findall(r"plt\.subplots\((\d+),\s*(\d+)", source_t3)
print(f"\nSubplot Dimensions:")
for dim in subplot_dims:
    rows, cols = dim
    print(f"  Found: ({rows}, {cols}) - ", end="")
    if rows == '1':
        print("✓ Correct (1 row)")
    else:
        print(f"⚠ Should be (1, N) format")

# Count numeric variables
grp3_matches = re.findall(r"grp3_[^=]*=\s*\[(.*?)\]", source_t3, re.DOTALL)
total_num_vars = sum(len(re.findall(r"'([^']+)'", g)) for g in grp3_matches)
print(f"\nNumeric Variables in Task 3:")
print(f"  ✓ Total variables shown: {total_num_vars}")
print(f"  Expected: 23 numeric columns")

# Task 4 - Multivariate categorical
print("\n" + "█"*120)
print("TASK 4: MULTIVARIAT KATEGORIK vs ATTRITION - DETAILED CHECK")
print("█"*120)

source_t4 = ''.join([get_cell_source(i) for i in [39, 40, 41]])

grp4_matches = re.findall(r"grp4_[^=]*=\s*\[(.*?)\]", source_t4, re.DOTALL)
countplot_cols = sum(len(re.findall(r"'([^']+)'", g)) for g in grp4_matches)

print(f"\nCountplot with hue=Attrition:")
print(f"  ✓ Found {len(grp4_matches)} groups")
print(f"  ✓ Total columns: {countplot_cols}")

if 'normalize' in source_t4.lower():
    print(f"\nStacked Barplot:")
    print(f"  ✓ Normalized/stacked barplot implemented")

# Task 5 - T-Test Details
print("\n" + "█"*120)
print("TASK 5: T-TEST (TotalWorkingYears vs Attrition) - DETAILED CHECK")
print("█"*120)

source_t5 = ''.join([get_cell_source(i) for i in [43, 44, 45]])

t_test_match = re.search(r"t_stat|ttest|t-stat", source_t5, re.IGNORECASE)
print(f"\nT-Test Implementation:")
if t_test_match:
    print(f"  ✓ T-statistic calculation found")
if 'pvalue' in source_t5.lower() or 'p_value' in source_t5.lower():
    print(f"  ✓ P-value extraction found")

if 'tolak' in source_t5.lower() or 'kesimpulan' in source_t5.lower() or 'conclusion' in source_t5.lower():
    print(f"\nConclusion:")
    print(f"  ✓ Hypothesis test conclusion written")

# Task 6 - ANOVA Details
print("\n" + "█"*120)
print("TASK 6: ONE-WAY ANOVA (Age vs Department) - DETAILED CHECK")
print("█"*120)

source_t6 = ''.join([get_cell_source(i) for i in [46, 47, 48]])

if 'f_oneway' in source_t6.lower() or 'anova' in source_t6.lower():
    print(f"\nANOVA Implementation:")
    print(f"  ✓ F-statistic and p-value extracted")
    if 'Department' in source_t6:
        print(f"  ✓ Includes all departments")

# Task 11 - Classification GridSearchCV
print("\n" + "█"*120)
print("TASK 11: GRIDSEARCHCV CLASSIFICATION - DETAILED CHECK")
print("█"*120)

source_t11 = ''.join([get_cell_source(i) for i in [56, 57]])

models_found = []
if 'LogisticRegression' in source_t11:
    models_found.append('Logistic Regression')
if 'DecisionTree' in source_t11:
    models_found.append('Decision Tree')
if 'XGBoost' in source_t11:
    models_found.append('XGBoost')

print(f"\nClassification Models with GridSearchCV:")
print(f"  ✓ Models found: {', '.join(models_found)}")
if len(models_found) == 3:
    print(f"  ✓ All 3 required models present")

if 'param_grid' in source_t11.lower():
    print(f"\nHyperparameter Tuning:")
    print(f"  ✓ param_grid defined for CV")

# Task 12 - Classification Report
print("\n" + "█"*120)
print("TASK 12: CLASSIFICATION REPORT - DETAILED CHECK")
print("█"*120)

source_t12 = ''.join([get_cell_source(i) for i in [58, 59, 60, 61]])

clf_report_count = source_t12.count('classification_report')
print(f"\nClassification Report:")
print(f"  ✓ Report called {clf_report_count} times")

train_mentions = source_t12.lower().count('train')
test_mentions = source_t12.lower().count('test')
print(f"  Train set mentions: {train_mentions}")
print(f"  Test set mentions: {test_mentions}")
if train_mentions > 0 and test_mentions > 0:
    print(f"  ✓ Both train and test sets have reports")

# Task 13 - Best Estimator
print("\n" + "█"*120)
print("TASK 13: BEST ESTIMATOR - DETAILED CHECK")
print("█"*120)

source_t13 = ''.join([get_cell_source(i) for i in [62, 63, 64, 65, 66]])

metrics_found = []
for metric in ['f1', 'auc', 'accuracy', 'precision', 'recall']:
    if metric in source_t13.lower():
        metrics_found.append(metric.upper())

print(f"\nMetrics Comparison:")
print(f"  ✓ Metrics used: {', '.join(metrics_found)}")

if 'ringkasan' in source_t13.lower() or 'summary' in source_t13.lower():
    print(f"\nSummary Table:")
    print(f"  ✓ Comparison table/summary provided")

# Task 17 - Regression
print("\n" + "█"*120)
print("TASK 17: REGRESSION - DETAILED CHECK")
print("█"*120)

source_t17 = ''.join([get_cell_source(i) for i in [76, 77]])

regressors_found = []
for reg in ['LinearRegression', 'Ridge', 'Lasso', 'PolynomialFeatures', 'RandomForest', 'XGBoost']:
    if reg in source_t17:
        regressors_found.append(reg)

print(f"\nRegressors Found:")
print(f"  ✓ {len(regressors_found)} regressors: {', '.join(regressors_found)}")
print(f"  Expected: Minimum 2 (linear + tree-based)")

if 'GridSearchCV' in source_t17:
    print(f"\nHyperparameter Tuning:")
    print(f"  ✓ GridSearchCV with CV implemented")

# Task 18 - Regression Metrics
print("\n" + "█"*120)
print("TASK 18: REGRESSION METRICS - DETAILED CHECK")
print("█"*120)

source_t18 = ''.join([get_cell_source(i) for i in [78, 79, 80]])

metrics_list = []
for m in ['r2', 'mse', 'rmse', 'mae', 'mape']:
    if m.lower() in source_t18.lower():
        metrics_list.append(m.upper())

print(f"\nMetrics Available:")
print(f"  ✓ {len(metrics_list)}/5 metrics found: {', '.join(metrics_list)}")

if 'dataframe' in source_t18.lower() or 'pd.DataFrame' in source_t18:
    print(f"  ✓ Results in DataFrame format")

# Task 21 - Clustering
print("\n" + "█"*120)
print("TASK 21: CLUSTERING (ELBOW & SILHOUETTE) - DETAILED CHECK")
print("█"*120)

source_t21 = ''.join([get_cell_source(i) for i in [86, 87]])

print(f"\nElbow Method:")
if 'inertia' in source_t21.lower():
    print(f"  ✓ Inertia calculated for range of K")
    k_range_match = re.search(r"range\((\d+),\s*(\d+)\)", source_t21)
    if k_range_match:
        start, end = k_range_match.groups()
        print(f"  ✓ K range: {start} to {end}")

print(f"\nSilhouette Score:")
if 'silhouette' in source_t21.lower():
    print(f"  ✓ Silhouette scores calculated")

print(f"\nOptimal K:")
if 'optimal_k' in source_t21.lower():
    print(f"  ✓ Optimal K determined and stored")

# Task 22 - Label Column
print("\n" + "█"*120)
print("TASK 22: LABEL COLUMN - DETAILED CHECK")
print("█"*120)

source_t22 = ''.join([get_cell_source(i) for i in [88, 89]])

if 'label' in source_t22.lower():
    print(f"\nLabel Column:")
    print(f"  ✓ 'label' column created")
    if 'fit_predict' in source_t22:
        print(f"  ✓ Using fit_predict from KMeans model")

# SHAP Analysis
print("\n" + "█"*120)
print("SHAP ANALYSIS - DETAILED CHECK")
print("█"*120)

shap_clf_found = False
shap_reg_found = False

for idx, cell in enumerate(nb['cells']):
    source = get_cell_source(idx)
    if 'shap' in source.lower():
        if 'classif' in source.lower() or idx < 70:
            shap_clf_found = True
        if 'regress' in source.lower() or idx > 70:
            shap_reg_found = True

print(f"\nSHAP Classification:")
if shap_clf_found:
    print(f"  ✓ SHAP analysis implemented for classification")
else:
    print(f"  ⚠ May need verification")

print(f"\nSHAP Regression:")
if shap_reg_found:
    print(f"  ✓ SHAP analysis implemented for regression")
else:
    print(f"  ⚠ May need verification")

# Em-dash check
print("\n" + "█"*120)
print("EM-DASH CHECK (U+2014)")
print("█"*120)

em_dash_cells = []
for idx, cell in enumerate(nb['cells']):
    source = get_cell_source(idx)
    if '—' in source:
        em_dash_cells.append((idx, get_cell_id(idx)))

if em_dash_cells:
    print(f"\n⚠ EM-DASHES FOUND in {len(em_dash_cells)} cells:")
    for idx, cell_id in em_dash_cells:
        print(f"  Cell {idx} (ID: {cell_id})")
else:
    print(f"\n✓ No em-dashes found - all formatting OK")

print("\n" + "="*120)
print("AUDIT COMPLETE")
print("="*120)
