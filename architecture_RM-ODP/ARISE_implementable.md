# ARISE Implementable View (RM-ODP)

## Technical viewpoint with implementation guidance

### Repo to Component Mapping
- UI: `src/ui/app.py` (+ assets)
- Core Pipeline: `src/core/{datasets.py, models.py, pipeline.py}`
- Reporting: `src/core/reporting.py`
- API: `src/api/app.py` (FastAPI, optional)
- Docs: `architecture_RM-ODP/*`
- Tests: `tests/*`

### Runtime Stack and Versions
- Python 3.11+
- Streamlit, pandas, numpy, scikit‑learn, reportlab, FastAPI, uvicorn

### Configuration
- `.env` (example in `.env.example`): `DATA_ROOT`, endpoints for external APIs.
- `requirements.txt` pinned versions; Docker reproducibility.

### Execution
- Windows: `./run.ps1`
- macOS/Linux/WSL: `./run.sh`
- API (optional): `uvicorn src.api.app:app --reload`

### Data Contract (enforced)
- Input CSV columns: `name,type,dose,pulse_hours,target_genes`.
- Output adds: `Rejuvenation,SafetyRisk,Confidence,Composite`.

### Extending Models (Replace Toy Scorers)
- Create `src/core/advanced_models.py` with trained predictors.
- Wire into `pipeline.score_dataframe` behind a feature flag (e.g., `USE_ADVANCED=1`).
- Add uncertainty with conformal prediction or ensembles; surface in report.

### Lineage and Reproducibility
- Inject `{data_version, model_version, parameters, commit_sha}` into report footer and CSV metadata.
- Persist run manifests under `reports/` for audit.

### Observability
- Minimal: structured logs around ingest, scoring, report build.
- Later: metrics (latency, throughput), tracing (OpenTelemetry), error aggregation.

### Security Controls
- Do not persist uploads by default; scrub temp files.
- Validate content types and schema; limit file sizes.

### CI/CD (MVP)
- GitHub Actions: lint, tests, artifact upload (PDF/CSV sample).
- Container build for reproducible runs.

### Deployment Options
```mermaid
graph LR
  Dev[Local Dev (Docker Compose)] --> Pilot[Single VM + Docker]
  Pilot --> K8s[Kubernetes + Ingress]
```

### Testing Strategy
- Unit: datasets, models, pipeline, reporting.
- Property tests: ranking monotonicity and determinism under fixed seed.
- Golden tests: snapshot PDF metadata fields.

### Performance and Sizing (Starter)
- Target: 2k candidates < 5s on laptop; scale via vectorization/multiprocessing.
- Profile with `cProfile` and pandas eval; iterate hot spots.

### Migration Plan
- Introduce advanced models behind flags; keep toy models for demo.
- Add persistence and artifact store in a backward‑compatible manner.

### Example API Calls
- Health: `GET /health`
- Score: `POST /score` with CSV (returns top‑K JSON)

### Risk Log (Selected)
- Misinterpretation of scores → disclaimers, clear axes, validation plan in reports.
- Data licensing → track dataset licenses; enforce allowed use.
