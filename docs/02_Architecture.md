
## 2. `docs/system_architecture_diagram.md`

```markdown
# TrailVision System Architecture Diagram


                         Project TrailVision
┌──────────────────────────────────────────────────────────────┐
│                         Desktop App                          │
│                    app/main.py - future GUI                   │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                         Services Layer                       │
│                                                              │
│   VideoService        AnalysisService        DatabaseService │
│   - metadata          - motion metrics       - rides         │
│   - conversion        - optical flow         - videos        │
│   - file paths        - highlights           - metrics       │
└───────────────┬──────────────────────┬───────────────────────┘
                │                      │
                ▼                      ▼
┌──────────────────────────┐   ┌───────────────────────────────┐
│       Vision Layer       │   │          Models Layer          │
│                          │   │                               │
│   motion.py              │   │   Ride                        │
│   optical_flow.py        │   │   Video                       │
│   highlights.py          │   │   Future: Metric, Highlight   │
└───────────────┬──────────┘   └───────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
│                                                              │
│   DuckDB                                                     │
│   database/trailvision.duckdb                                │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                    Analytics / Reporting                     │
│                                                              │
│   dbt models - planned                                       │
│   Power BI dashboard - planned                               │
└──────────────────────────────────────────────────────────────┘