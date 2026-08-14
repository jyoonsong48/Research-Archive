# The database used is based on the research conducted by the Department of Forensic Medicine at Seoul National University.
# URL: https://forensicdna.snu.ac.kr/portal/guideline

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, KFold, cross_val_score
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

# font
plt.rcParams["text.usetex"] = False
plt.rcParams["font.family"] = "serif"

# database
df = pd.read_csv("MethylationDB-SNaPShot-BloodSalivaBuccalcells.csv")

# database check
"""
print(df.head())    
print(df.shape) 
print(df.isnull().sum()) 
print(df["Genetic analyzer"].unique())
print(df["Body Fluid Type"].unique())
"""
# lists
markers = ["ELOVL2", "FHL2", "KLF14", "MRI29B2C", "TRIM59"]
#body_fluid = ["Blood", "Buccal Swab", "Saliva"]
#genetic_analyser = ["3130", "3500", "SeqStudio"]

# ---------------  x, y separation (test/train separation) --------------- 
one_hot_encode_1 = pd.get_dummies(df, columns = ["Genetic analyzer"], prefix = "Genetic Analyzer", drop_first=True) # one hot encoding
one_hot_encode_2 = pd.get_dummies(one_hot_encode_1, columns= ["Body Fluid Type"], prefix= "Body Fluid Type", drop_first=True)
x = one_hot_encode_2.drop("Age", axis = 1)
y = df["Age"].values

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=1214 # my fav youtubers bday...
)

# ---------------  machine learning (train) --------------- 
model = LinearRegression()
model.fit(x_train, y_train)

# ---------------  cross check (train+test, for stable performance estimation) --------------- 
kfold = KFold(n_splits=5, shuffle=True, random_state=1214)
scores = cross_val_score(model, x, y, cv=kfold)

# --------------- evaluating --------------- 
train_r2 = model.score(x_train, y_train)
test_r2 = model.score(x_test, y_test)
print(f"Train R²: {train_r2:.3f}, Test R²: {test_r2:.3f}") # train vs. test
print(round(scores.mean(), 3)) # averg. of R^2
print(round(scores.std(), 3)) # SD


coef_df = pd.DataFrame({"feature": x.columns, "coefficient": model.coef_}).sort_values("coefficient")

# 1. Markers
marker_df = coef_df[coef_df['feature'].isin(markers)]

# 2. Tools
analyzer_df = coef_df[coef_df['feature'].str.contains('Genetic Analyzer')]

# 3. Body fluids
fluid_df = coef_df[coef_df['feature'].str.contains('Body Fluid Type')]

# combine
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

bars0 = axes[0].barh(marker_df['feature'], marker_df['coefficient'], color = "teal", alpha = 0.3, height=0.4)
axes[0].set_title('Markers')

bars1 = axes[1].barh(analyzer_df['feature'], analyzer_df['coefficient'], color = "slateblue", alpha = 0.3, height=0.3)
axes[1].set_title('Genetic Analyzer')

bars2 = axes[2].barh(fluid_df['feature'], fluid_df['coefficient'], color = "salmon", alpha = 0.3, height=0.3)
axes[2].set_title('Body Fluid Type')

for ax, bars in zip(axes, [bars0, bars1, bars2]):
    for rect in bars:
        width = rect.get_width()
        y_center = rect.get_y() + rect.get_height()/2.0
        
        if width >= 0:
            ax.text(width, y_center, f'{width:.1f}',
                     ha='right', va='center', size=9)
        else:
            ax.text(width, y_center, f'{width:.1f}',
                     ha='left', va='center', size=9)

plt.tight_layout()
plt.suptitle("Feature Coefficients")
plt.figtext(0, 0, "Genetic Analzer Standard: 3130, Body Fluid Type Standard: Blood")
plt.show()

#  --------------- Prediction (test) --------------- 
y_pred = model.predict(x_test)

# ---------------  RMSE, MAE --------------- 
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
print(rmse, mae)

# ---------------  Actual vs est. --------------- 
plt.scatter(y_test, y_pred, color = "teal", alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual Age')
plt.ylabel('Estimated Age')
plt.title('Actual vs Estimation (Test Set)')
plt.show()

# --------------- Distribution --------------- 
df[['ELOVL2', 'FHL2', 'KLF14', 'MRI29B2C', 'TRIM59']].plot(kind='box')
plt.title("Distribution by Markers")
plt.show()

for m in markers:
    df.boxplot(column=m, by='Body Fluid Type', color = "teal")
    plt.suptitle('')
    plt.title(f"Distribution by {m} & Body Fluid Type")
    plt.show()

# --------------- Heatmap --------------- 
numeric_cols = ['Age', 'ELOVL2', 'FHL2', 'KLF14', 'MRI29B2C', 'TRIM59']
corr = df[numeric_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.set_context("notebook")
sns.heatmap(
    corr, 
    mask=mask, 
    annot=True, 
    cmap='seismic', 
    center=0, 
    square=True
)
plt.title("Correlation Matrix (Lower Triangle)")
plt.show()

# --------------- Residual plot --------------- 
residuals = y_test - y_pred
plt.scatter(y_pred, residuals, color = "teal", alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Age')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()