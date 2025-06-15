# OCR Analysis System - README

## 🚀 Workflow Overview

1. **PDF Upload**

   * A PDF document is uploaded via API along with its `doc_type`.

2. **Job Creation**

   * A new `Job` entry is created to track the analysis process.

3. **Asynchronous OCR Analysis**

   * A Celery task (`analyze_pdf_task`) is triggered in the background.
   * This task handles reading, analyzing, and storing the OCR results.

4. **OCR Simulation**

   * The PDF is parsed using PyMuPDF (`fitz`) to extract text spans.
   * Each span is analyzed for its font style, size, position, and content.

5. **Classification**

   * Text is classified as either:

     * `template` (pre-filled text by the organization)
     * `user` (user-filled text in a form)
   * This is done by comparing each span’s font and size with expected baselines for the given `doc_type`.

6. **Outlier Detection**

   * For user-entered fields, two types of inconsistencies are detected:

     * **Font Outliers**: Font/style combinations that appear rarely in the document.
     * **Position Outliers**: Numeric fields that are misaligned compared to others.

7. **Result Storage**

   * All OCR results are stored in the database, along with `meta` information and flags for detected inconsistencies.
   * The job status is marked as `COMPLETED` or `FAILED` based on the outcome.

---

## 🔎 How Inconsistencies Are Detected

### 1. **Template vs User Classification**

Each text span in the PDF is checked for:

* Font name
* Font size
* Tolerance margin

If both font and size match any of the baseline values defined for that form type (within allowed tolerance), it's considered a **template** field.

Otherwise, it's marked as a **user-entered** field — these are the fields we focus on for inconsistency detection.

---

### 2. **Font Outlier Detection**

For user-entered fields:

* The combination of font + size is recorded for all entries.
* A frequency distribution is calculated.
* If any font+size pair is used very rarely (below a set threshold, like 10%), it's flagged as an **outlier**.

This helps detect inconsistent entries where users used different styles or sizes unintentionally.

---

### 3. **Position Outlier Detection**

Among user-entered fields that are numeric (e.g., salary, tax amount):

* The left x-coordinate (`x0`) of each field is collected.
* A median `x0` is calculated.
* If any field deviates too far from this median (beyond a fixed pixel tolerance), it's flagged.

This catches formatting or alignment issues (e.g., misaligned number columns).
