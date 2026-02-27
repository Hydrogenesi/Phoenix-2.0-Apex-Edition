# Phase 1 Script Usage

## Overview

The `run-phase-1.sh` script is the canonical Phase 1 execution script for Phoenix 2.0 Apex Edition. It automates the complete Phase 1 workflow, including environment preparation, validation, and Ceremonies layer establishment.

## What It Does

1. **Prepares the environment** - Checks current directory, branch, and git status
2. **Validates structure and prerequisites** - Verifies all required directories and files exist
3. **Runs Phase 1 checks** - Confirms git repository and remote configuration
4. **Creates Phase 1 branch** - Works on the current branch (already created by automation)
5. **Stages Ceremonies README artifact** - Creates `Ceremonies/README.md` if not present
6. **Commits changes** - Commits the Ceremonies layer with descriptive message
7. **Prints PR URL** - Provides the URL and instructions for creating the PR

## Usage

Simply run the script from the repository root:

```bash
./run-phase-1.sh
```

## Requirements

- Git repository with origin remote configured
- Required directories: Phoenix, Hydrogenesi, TheThird, Atlases, Universal-Laws
- Required files: README.md, LICENSE
- Bash shell

## Idempotency

The script is idempotent and can be run multiple times safely:
- If Ceremonies directory exists, it will be reused
- If Ceremonies/README.md exists, it will not be overwritten
- If changes are already committed, no new commit will be created

## Output

The script provides:
- Colored status messages for each step
- ✓ Success indicators for completed steps
- ℹ Info indicators for skipped steps
- ✗ Error indicators for failures
- PR URL with suggested title and body

## After Running

1. Open the provided PR URL in your browser
2. Use the suggested PR title and body
3. Create the Pull Request
4. Report back: "Phase 1 PR created"

## Example Output

```
═══════════════════════════════════════════════════════════
    Phoenix 2.0 Apex Edition — Phase 1 Canonical Script
═══════════════════════════════════════════════════════════

Step 1: Preparing the environment...
✓ Environment prepared

Step 2: Validating structure and prerequisites...
✓ Structure and prerequisites validated

[... additional steps ...]

═══════════════════════════════════════════════════════════
✓ Phase 1 Script Execution Complete
═══════════════════════════════════════════════════════════

Next Steps:
1. Create PR at: https://github.com/Hydrogenesi/Phoenix-2.0-Apex-Edition/compare/copilot/run-phase-1-script?expand=1
```

## Troubleshooting

### Script fails at structure validation
- Ensure you're running from the repository root
- Verify all required directories exist

### Script fails at git checks
- Ensure you're in a git repository
- Verify origin remote is configured with `git remote -v`

### No changes to commit
- This is normal if Ceremonies/README.md was already committed
- The script is idempotent and safe to re-run

## Integration

This script is part of the Phoenix 2.0 Apex Edition Phase 1 initiative to establish the Ceremonies layer - the ritual and invocation framework that makes the Triadic architecture practical and actionable.
