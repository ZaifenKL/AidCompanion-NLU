# Dataset Validation Report

**Date:** 2026-09-16 13:28
**Language:** ES
**Hierarchy:** H1

## Summary
- Total duplicates: **66**
- Total corrupted lines: **0**
- Dataset Status: **NEEDS FIXES**

---

## TRAIN
- Total examples: 920
- Duplicates: 60
- Corrupted lines: 0

### Category Distribution
| Category | Count | Histogram |
|----------|-------|-----------|
| other | 293 | ██████████████████ |
| medical_emergency | 311 | ███████████████████ |
| survival | 316 | ████████████████████ |

## Balance Analysis

### TRAIN
- Largest category: **survival** (316)
- Smallest category: **other** (293)
- Ratio largest/smallest: **1.08**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### VAL
- Largest category: **other** (70)
- Smallest category: **survival** (58)
- Ratio largest/smallest: **1.21**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### TEST
- Largest category: **survival** (71)
- Smallest category: **other** (62)
- Ratio largest/smallest: **1.15**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### Text Length Analysis
- Average length: 11.31 tokens
- Min length: 2 tokens
- Max length: 26 tokens

---

## VAL
- Total examples: 197
- Duplicates: 2
- Corrupted lines: 0

### Category Distribution
| Category | Count | Histogram |
|----------|-------|-----------|
| survival | 58 | ████████████████ |
| medical_emergency | 69 | ███████████████████ |
| other | 70 | ████████████████████ |

## Balance Analysis

### TRAIN
- Largest category: **survival** (316)
- Smallest category: **other** (293)
- Ratio largest/smallest: **1.08**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### VAL
- Largest category: **other** (70)
- Smallest category: **survival** (58)
- Ratio largest/smallest: **1.21**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### TEST
- Largest category: **survival** (71)
- Smallest category: **other** (62)
- Ratio largest/smallest: **1.15**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### Text Length Analysis
- Average length: 11.31 tokens
- Min length: 2 tokens
- Max length: 26 tokens

---

## TEST
- Total examples: 198
- Duplicates: 4
- Corrupted lines: 0

### Category Distribution
| Category | Count | Histogram |
|----------|-------|-----------|
| other | 62 | █████████████████ |
| medical_emergency | 65 | ██████████████████ |
| survival | 71 | ████████████████████ |

## Balance Analysis

### TRAIN
- Largest category: **survival** (316)
- Smallest category: **other** (293)
- Ratio largest/smallest: **1.08**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### VAL
- Largest category: **other** (70)
- Smallest category: **survival** (58)
- Ratio largest/smallest: **1.21**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### TEST
- Largest category: **survival** (71)
- Smallest category: **other** (62)
- Ratio largest/smallest: **1.15**
- Balance status: **🟢 Good balance**

- Balance looks good.

---

### Text Length Analysis
- Average length: 11.31 tokens
- Min length: 2 tokens
- Max length: 26 tokens

---

## Warnings
- No category distribution warnings.

---

## Recommendations
- Remove or review 66 duplicated examples.

---

## Final Status
**NEEDS FIXES**
