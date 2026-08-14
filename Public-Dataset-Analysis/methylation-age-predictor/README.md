# $\text{Age Predictor via DNA methylation}$

> **Database Info**
> 
> The database used is based on the research conducted by the Department of Forensic Medicine at Seoul National University.
> <br> You can check original database here: `https://forensicdna.snu.ac.kr/portal/guideline`

---

## $\text{✨ Key Points}$

- **Linear Regression model:**
  - **5 CpG methylation markers**: `ELOVL2`, `FHL2`, `KLF14`, `MIR29B2C`, and `TRIM59` alongside with 3 body fluid types (blood, saliva, buccal swab).
  - **One-hot encoding**: Categorical variables (Body Fluid Type, Genetic Analyzer) were processed via one-hot encoding.
- **Model Validation:**
  - **5-Fold Cross Validation combined with Train/Test Split**: Verified performance stability (Mean R² = 0.887, Std = 0.010, MAE = ±3.78 years).
  - **Residual Plot**: Examined linearity assumptions and age-specific error patterns.
- **Data Visualisation:**
  - **Boxplot**: Visualised marker distribution comparisons (Boxplot) and marker value differences by body fluid type.
  - **Correlation Heatmap**: Assessed marker-age correlations using a heatmap.

---

## $\text{🛠️ Tech Stack}$
- **Data Handling:** pandas, sklearn, numpy
- **Data Visualisation:** Matplotlib, Seaborn

---

## $\text{📂 Project Structure}$
`methylation-age-predictor/`
<br>├── `main.py  # Main code`
<br>├── `MethylationDB-SNaPShot-BloodSalivaBuccalcells.csv           # Database for training`
<br>└── `README.md              # Documentation and system manual`

---

## $\text{🚀 Future Roadmap}$
- **Non-linear Model Comparison:** Polynomial Regression / Random Forest will be employed for comparison. (possibility that certain markers do not show linear correlation with age)
- **Web Interface:** Plan to make website (using Streamlit etc.) that presents age estiamtion with CpG marker input.

---

## $\text{🎨 Figure Examples}$
<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/241d5357-b6a9-42c2-9237-3d34657aa5e2" />
<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/d312edeb-0b7f-4b94-b89a-c25d3b6f771a" />
<img width="640" height="608" alt="Image" src="https://github.com/user-attachments/assets/59c3a17f-bcf1-4275-ba9c-7c1f09483fa7" />
<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/69e5efd2-6480-4ef1-b220-e7fe95e9dcb6" />

