# ARISE Implementable View (RM-ODP)

## Technical viewpoint with implementation guidance

### Core Components
- Streamlit UI: `src/ui/app.py`
- Pipeline: `src/core/{datasets.py,models.py,pipeline.py}`
- Reporting: `src/core/reporting.py`
- Optional API: `src/api/`

### Run
- Windows: `./run.ps1`
- Unix: `./run.sh`

### Data Contract
CSV columns required: `name,type,dose,pulse_hours,target_genes`.

### Composite Score
`Composite = 0.55*Rejuvenation + 0.30*(100 - SafetyRisk) + 0.15*Confidence`

### Upgrades
- Replace toy scorers with trained models
- Add uncertainty estimation and calibration
- Persist lineage: data_version, model_version, parameters, commit_sha
