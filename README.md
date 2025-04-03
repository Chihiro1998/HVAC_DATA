# HVAC Final Project Check In

**Authors**: Weiqi (Vicky) Dong, Yuchen (Olivia) Kuang  
**Date**: 2025-04-03

---
## Project Goal
Simulate the core intelligence of Elipsa’s HVAC  tool — identifying rooftop-terminal unit (RTU–VAV) system structure and diagnosing inefficiencies or abnormal performance using data.

---
## Data Overview

### Primary Dataset: `HVAC_NewData`

- **RTUs**:  
  Files like `RTU_1.csv`, `RTU_2.csv`, `RTU_3.csv` represent rooftop units.
  - Key fields: `SuplAirTemp`, `HtgPct`, `SuplFanSpd`

- **VAVs**:  
  Files like `A.csv` to `ZZ.csv` represent terminal units.
  - Key fields: `DschAirTemp`, `HtgPct`, `AirFlow`, `RmTemp`, `ClgPct`, etc.

> ⚠️ The `HVAC` folder (zone-level data) is excluded per company clarification — it's outdated, lacks mapping, and is not recommended for main analysis.
---

## 1. RTU Activity Status

### Goal

Determine which RTUs are active and serving loads.

### Approach

- Analyzed:
- `SuplAirTemp` trends
  ![image](https://github.com/user-attachments/assets/50c41ab0-13cd-46ca-9a18-66d3ec8b9ced)
- `HtgPct` heating percentage
  ![image](https://github.com/user-attachments/assets/85c1eecb-8fac-4ab6-a239-94cb55f3552e)
- `SuplFanSpd` fan output
  ![image](https://github.com/user-attachments/assets/2cc4a97c-fb2d-4fa2-aa57-f7b41fa20288)

### Result

| RTU   | Active? | Notes                             |
|-------|---------|-----------------------------------|
| RTU_1 | ✅ Yes  | Heating/Cooling cycles visible     |
| RTU_2 | ✅ Yes  | Actively modulating temperature    |
| RTU_3 | ❌ No   | Mostly inactive, excluded from mapping |

---

## 2. RTU–VAV Connection Mapping

### What we want to know:

Which RTU serves each VAV?

---

### Version 1 – Simple Matching (Baseline)

- Matched `DschAirTemp` (VAV) ↔ `SuplAirTemp` (RTU)
- Metrics:
  - Pearson correlation
  - Mean Squared Error (MSE)

---

### Version 2 – Enhanced Matching (Improved)

Added new VAV–RTU signals:
- `HtgPct` (heating behavior similarity)
- `AirFlow` vs `HtgPct` (response linkage)

### Composite Scoring Formula:
```python
CombinedScore = Corr_Temp - MSE_Temp + Corr_HtgPct + Corr_AirFlow_HtgPct
```

| Using Metric         | Meaning                                          |
|----------------------|--------------------------------------------------|
| `Corr_Temp`          | Correlation between discharge air & supply air  |
| `MSE_Temp`           | Dsch-Supl temperature mismatch (penalty)        |
| `Corr_HtgPct`        | Synchronized heating activation                 |
| `Corr_AirFlow_HtgPct`| Terminal airflow responding to RTU heating      |


> This version achieved 100% connection resolution across 47+ VAVs.


### RTU VAVS Connections Result Visualization:
Sankey:
![image](https://github.com/user-attachments/assets/69c2ac76-0550-4c33-a867-c5cb511c9781)

Network:
![image](https://github.com/user-attachments/assets/1261198c-3a35-4959-a3b6-230e2444b23c)

---

## 3. Todo List

| To-Do Task                                                        | Why It Matters                                                                 |
|-------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Perform spatial visualization based on RTU-VAV connection table   | Helps simulate Eclipse’s interface and visually interpret the HVAC system structure     |
| Compare first version vs enhanced version of connection analysis  | Justifies why the enhanced metric approach is more accurate and informative             |
| Develop zone-level energy models using HVAC + weather data        | Enables external driver analysis and supports accurate energy consumption prediction     |
| Conduct fault or anomaly detection based on VAV-RTU interactions  | Identifies unusual behavior (e.g., under-performing zones or unresponsive systems)       |
| Integrate findings into a complete diagnostics and control report | Prepares final documentation that mimics real-world HVAC analytics and decision support  |
| Build final dashboard or presentation visualizations              | Delivers a user-facing summary of insights to stakeholders or technical reviewers        |
