# ARISE Logical View (RM-ODP)

## Computational and Engineering (Logical level)

### Services (logical)
- Ingest: dataset normalization and QC
- Simulate: candidate generation and prediction
- Score: composite ranking with uncertainty
- Report: PDF/CSV with clinician notes
- Audit: lineage and reproducibility metadata

### Interfaces
- UI → Pipeline: `run_simulation(n, seed, csv_file)`
- Pipeline → Reporting: `make_pdf_report(df, top_k)`

### Workflows (MVP)
1. Load demo or uploaded CSV
2. Score rows with toy models
3. Rank by composite
4. Render PDF/CSV and present downloads
