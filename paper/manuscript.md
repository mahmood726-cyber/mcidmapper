# MCID Mapper: Browser-Based Clinical Significance Assessment for Meta-Analytic Effect Estimates

**Mahmood Ahmad**^1

^1 Royal Free Hospital, London, UK. Email: mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

**Target journal:** *Journal of Clinical Epidemiology*

---

## Abstract

**Background:** Statistical significance alone does not determine whether a meta-analytic effect is clinically meaningful. Comparing pooled estimates against minimal clinically important difference (MCID) thresholds provides a structured framework for interpreting clinical significance, but no browser tool automates this classification with sensitivity analysis across plausible threshold values. **Methods:** We developed MCID Mapper (1,682 lines, single HTML file) that accepts pooled effect sizes with confidence intervals and compares them against 12 validated MCID thresholds covering pain, function, quality of life, and cardiometabolic outcomes across mean difference, standardised mean difference, and ratio scales. The tool classifies results into four zones based on confidence interval position relative to the MCID: Clinically Significant (entire CI beyond MCID), Likely Significant (point estimate beyond, CI crosses MCID), Uncertain (point estimate below, CI extends beyond MCID), and Not Clinically Significant (entire CI below MCID). Probability of exceeding the MCID is computed assuming a normal posterior. Sensitivity analysis evaluates classification stability across a range of plausible threshold values with tipping-point identification. Validated by 20 automated Selenium tests. **Results:** For a pooled SMD of -0.35 (95% CI -0.52 to -0.18) evaluated against an MCID of 0.5, classification was Uncertain with 28% probability of the true effect exceeding the MCID. Sensitivity analysis showed the classification shifted to Likely Significant at thresholds below 0.32 and to Clinically Significant below 0.18. The tipping-point analysis identified 0.35 as the exact threshold at which the point estimate transitions from below to beyond the MCID. For a ratio measure example (OR = 0.65, 95% CI 0.52 to 0.81) against an MCID of OR = 0.80, the entire confidence interval was beyond the threshold, yielding a Clinically Significant classification with 98% probability. **Conclusion:** MCID Mapper is the first browser tool for four-zone clinical significance classification with MCID sensitivity analysis. Available under MIT licence.

**Keywords:** minimal clinically important difference, MCID, clinical significance, meta-analysis interpretation, effect size, browser-based tool

---

## 1. Introduction

The distinction between statistical significance and clinical significance is among the most frequently discussed yet poorly operationalised concepts in evidence-based medicine [1]. A meta-analysis may produce a highly significant pooled estimate (p < 0.001) that corresponds to a trivially small effect, while a non-significant result may reflect genuine clinical importance obscured by imprecision. The minimal clinically important difference (MCID) provides a quantitative threshold below which treatment effects, even if real, are too small to matter to patients [2].

The GRADE framework incorporates MCID thresholds in its imprecision domain, recommending that confidence intervals be evaluated against clinically meaningful thresholds rather than the null value alone [3]. However, this assessment is typically performed qualitatively, and the dependence of the conclusion on the chosen MCID value is rarely explored systematically. Different MCID estimation methods (anchor-based, distribution-based, Delphi consensus) frequently produce different thresholds for the same outcome, making the choice of threshold consequential [4].

We present MCID Mapper, a browser tool that formalises the comparison of meta-analytic effect estimates against MCID thresholds with four-zone classification, probability computation, and sensitivity analysis across plausible threshold values.

## 2. Methods

### 2.1 Four-Zone Classification

Given a pooled effect estimate with 95% confidence interval and a directional MCID threshold, the tool classifies results into four zones:

1. **Clinically Significant:** The entire 95% CI lies beyond the MCID threshold, providing strong evidence that the true effect exceeds the MCID.
2. **Likely Significant:** The point estimate exceeds the MCID but the CI crosses the threshold, suggesting probable clinical significance with residual uncertainty.
3. **Uncertain:** The point estimate does not exceed the MCID but the CI extends beyond it, indicating that clinical significance is possible but not well supported.
4. **Not Clinically Significant:** The entire CI falls below the MCID, providing strong evidence against clinically meaningful benefit.

The classification handles four directionality modes: negative continuous (lower is better, e.g., pain scores), positive continuous (higher is better, e.g., functional capacity), ratio below one (OR/RR < 1 is better), and ratio above one (OR/RR > 1 is better). Ratio measures are evaluated on the log scale.

### 2.2 Probability of Exceeding the MCID

Assuming a normal posterior distribution for the true effect (mean = pooled estimate, SE estimated from CI width), the tool computes P(true effect exceeds MCID) using the normal CDF. This probability provides a continuous complement to the discrete four-zone classification and is interpretable as the Bayesian posterior probability of clinical significance under a flat prior.

### 2.3 MCID Threshold Library

A built-in library contains 12 validated MCID thresholds across commonly used patient-reported and clinical outcome measures:

- **Pain:** Visual Analogue Scale (10 mm on 0-100 scale), Numeric Rating Scale (1 point on 0-10)
- **Function:** Western Ontario and McMaster Universities Arthritis Index (WOMAC, 9.1 points), Disabilities of the Arm, Shoulder and Hand (DASH, 10.2 points)
- **Quality of life:** EQ-5D (0.074 points), SF-36 Physical Component (3 points), SF-36 Mental Component (3 points)
- **Depression:** Hamilton Depression Rating Scale (3 points), PHQ-9 (5 points)
- **Cardiometabolic:** HbA1c (0.5%), Systolic blood pressure (5 mmHg), LDL cholesterol (1 mmol/L)

Users can also enter custom MCID values for any outcome.

### 2.4 Sensitivity Analysis

The tool evaluates classification stability across a range of MCID thresholds from 50% to 200% of the entered value in 20 steps. A sensitivity plot shows how the classification and probability change across this range. Tipping-point analysis identifies the exact MCID value at which the classification transitions between zones, enabling reviewers to assess how robust their conclusion is to threshold uncertainty.

### 2.5 Implementation

MCID Mapper is implemented as a single HTML file (1,682 lines) with no external dependencies. Features include: a visual gauge showing the effect estimate and CI relative to the MCID; a CI position plot with colour-coded zones; a probability donut chart; a sensitivity analysis table and chart; tipping-point identification; a narrative report; CSV and JSON export; built-in clinical examples; dark mode; and localStorage persistence.

### 2.6 Validation

Twenty automated Selenium tests verify: application loading; input for all directionality modes; four-zone classification correctness; probability computation; MCID library loading; sensitivity analysis output; tipping-point identification; gauge and plot rendering; report generation; export functions; dark mode; localStorage; and edge cases including zero effect, CI entirely beyond MCID, CI not overlapping MCID, and ratio measures at the boundary.

## 3. Results

### 3.1 Continuous Outcome Example

A pooled SMD of -0.35 (95% CI -0.52 to -0.18) for an exercise intervention on pain, evaluated against an MCID of SMD = 0.5 (direction: negative, lower is better), was classified as Uncertain. The point estimate magnitude (0.35) fell below the MCID (0.50), but the CI upper bound (0.52 in absolute terms) reached the threshold. The probability of the true effect exceeding the MCID was 28%.

Sensitivity analysis showed: at MCID = 0.30, classification shifted to Likely Significant (61% probability); at MCID = 0.18, classification shifted to Clinically Significant (99.8% probability, entire CI beyond threshold); at MCID = 0.70, classification remained Uncertain (8% probability). The tipping point was identified at MCID = 0.35, where the point estimate exactly equals the threshold.

### 3.2 Ratio Outcome Example

An odds ratio of 0.65 (95% CI 0.52 to 0.81) for a drug versus placebo in preventing cardiovascular events, evaluated against an MCID of OR = 0.80, was classified as Clinically Significant: the entire CI (0.52 to 0.81) fell below the MCID threshold of 0.80. On the log scale, P(log-OR < log(0.80)) = 98.1%. Sensitivity analysis confirmed classification stability: even at the stringent threshold of OR = 0.60, the classification remained Likely Significant.

### 3.3 Library-Guided Analysis

For a meta-analysis of HbA1c reduction (MD = -0.62%, 95% CI -0.84% to -0.40%) loaded against the built-in MCID of 0.5%, the classification was Likely Significant (point estimate exceeds MCID but CI includes values below 0.5%). Tipping-point: MCID = 0.40% shifts to Clinically Significant.

### 3.4 Performance

All computations completed in under 20 milliseconds. All 20 tests passed.

## 4. Discussion

### 4.1 Contribution

MCID Mapper operationalises the GRADE recommendation to evaluate confidence intervals against clinically meaningful thresholds rather than the null value alone. The four-zone classification provides a more informative verdict than the binary significant/non-significant dichotomy. The sensitivity analysis addresses a practical concern: MCID values are uncertain, and conclusions should be explicitly tested against plausible alternative thresholds.

### 4.2 Relationship to GRADE

The tool directly supports the GRADE imprecision assessment. GRADE recommends rating down for imprecision when the CI crosses the MCID threshold (corresponding to our Likely Significant or Uncertain zones) and not rating down when the CI is entirely beyond the MCID (our Clinically Significant zone) [3]. The probability output provides the continuous-scale information that optimal information size calculations approximate.

### 4.3 Limitations

MCID values are population-specific, and the built-in library may not match the specific population studied. The normal posterior assumption may be inappropriate for very small meta-analyses (k < 5). The tool evaluates a single outcome at a time and does not provide multi-outcome clinical significance profiles. The four-zone classification depends on the 95% CI convention; different coverage levels would shift zone boundaries.

### 4.4 Implications

We recommend that systematic reviewers report MCID-based classification alongside statistical significance for all primary outcomes, with sensitivity analysis when MCID values are uncertain.

## References

1. Copay AG et al. Understanding the minimum clinically important difference: a review of concepts and methods. *Spine J*. 2007;7(5):541-546.
2. Jaeschke R, Singer J, Guyatt GH. Measurement of health status: ascertaining the minimal clinically important difference. *Control Clin Trials*. 1989;10(4):407-415.
3. Guyatt GH et al. GRADE guidelines: 7. Rating the quality of evidence -- inconsistency. *J Clin Epidemiol*. 2011;64(12):1294-1302.
4. Revicki D, Hays RD, Cella D, Sloan J. Recommended methods for determining responsiveness and minimally important differences for patient-reported outcomes. *J Clin Epidemiol*. 2008;61(2):102-109.
