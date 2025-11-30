# /forge:sync - Documentation Synchronization

## Usage

```
/forge:sync {PRD_ID}
/forge:sync {PRD_ID} --mode auto
/forge:sync all
```

## Description

Synchronizes implementation progress with documentation. Generates or updates:
- README updates
- API documentation
- Architecture diagrams
- Test reports
- CHANGELOG entries

## Workflow

### 1. Analyze Implementation

```
Analyzing implementation for {PRD_ID}...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scanning:
   ├── Source files in src/
   ├── Test files in tests/
   ├── PRD document
   └── Progress checkpoint

Implementation Summary:
   ├── Files created: 12
   ├── Functions: 45
   ├── Classes: 8
   └── Test coverage: 85%
```

### 2. Generate Documentation

```
Generating documentation...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/5] README.md
      └── Added: Features, Installation, Usage sections

[2/5] API Documentation
      └── Generated: docs/api/

[3/5] Architecture Diagrams
      └── Updated: .forge/design/{PRD_ID}/

[4/5] Test Report
      └── Generated: .forge/reports/{PRD_ID}-test-report.md

[5/5] CHANGELOG
      └── Added: New entries for {PRD_ID}
```

### 3. Sync Complete

```
Documentation sync complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated Files:
   ├── README.md (updated)
   ├── docs/api/endpoints.md
   ├── docs/api/models.md
   ├── .forge/design/{PRD_ID}/DESIGN.md
   ├── .forge/reports/{PRD_ID}-test-report.md
   └── CHANGELOG.md (updated)

Next Steps:
   1. Review generated documentation
   2. Commit changes: git add . && git commit -m "docs: sync {PRD_ID}"
   3. Create PR (if using team mode)
```

## Options

- `--mode {auto|manual|review}`: Sync mode
  - `auto`: Generate all documentation automatically
  - `manual`: Prompt for each section
  - `review`: Generate drafts for review (default)
- `--include {sections}`: Specific sections to sync (comma-separated)
- `--exclude {sections}`: Sections to skip
- `--format {md|html|both}`: Output format (default: md)

## Documentation Sections

| Section | Description | Default |
|---------|-------------|---------|
| `readme` | Project README | Yes |
| `api` | API reference documentation | Yes |
| `diagrams` | Architecture diagrams | Yes |
| `tests` | Test reports and coverage | Yes |
| `changelog` | Version changelog | Yes |
| `contributing` | Contribution guide | No |
| `deployment` | Deployment guide | No |

## Output Structure

```
project/
├── README.md                    # Updated
├── CHANGELOG.md                 # Updated
├── docs/
│   ├── api/
│   │   ├── endpoints.md
│   │   ├── models.md
│   │   └── authentication.md
│   ├── architecture.md
│   └── deployment.md
└── .forge/
    ├── design/{PRD_ID}/
    │   ├── DESIGN.md           # Design documentation
    │   └── diagrams/           # PlantUML files
    └── reports/
        └── {PRD_ID}-test-report.md
```

## Examples

### Sync specific PRD
```
/forge:sync CHAT-001
```

### Sync all PRDs
```
/forge:sync all
```

### Auto mode (no prompts)
```
/forge:sync CHAT-001 --mode auto
```

### Include only specific sections
```
/forge:sync CHAT-001 --include readme,api,changelog
```

## Integration with Git

When `git_strategy` is configured:

- **manual mode**: Documents generated, manual commit required
- **personal mode**: Auto-commit after sync
- **team mode**: Auto-commit + create PR draft

## Related Commands

- `/forge:build` - Implementation (run before sync)
- `/forge:verify` - Verification (run before sync)
- `/forge:design` - Generate diagrams only
