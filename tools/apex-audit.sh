#!/bin/bash
# apex-audit.sh — Apex Engine Audit Script
# Version 1.0
# Part of Phoenix 2.0 — Apex Edition

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
total_checks=0
passed_checks=0
failed_checks=0

# Output functions
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║        Apex Engine Audit — Eight-Engine Validator      ║${NC}"
    echo -e "${BLUE}║              Phoenix 2.0 — Apex Edition                ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    echo -e "${YELLOW}▶ $1${NC}"
}

check_pass() {
    echo -e "  ${GREEN}✓${NC} $1"
    ((passed_checks++))
    ((total_checks++))
}

check_fail() {
    echo -e "  ${RED}✗${NC} $1"
    ((failed_checks++))
    ((total_checks++))
}

# Check if file exists
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        check_pass "$description"
        return 0
    else
        check_fail "$description (file not found: $file)"
        return 1
    fi
}

# Check if string exists in file
check_content() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if [ ! -f "$file" ]; then
        check_fail "$description (file not found)"
        return 1
    fi
    
    if grep -q "$pattern" "$file"; then
        check_pass "$description"
        return 0
    else
        check_fail "$description (pattern not found)"
        return 1
    fi
}

# Main audit execution
print_header

# ============================================================
# PHASE 1: Ascent Phase (Phoenix) — 4 Engines
# ============================================================
print_section "Phase 1: Ascent Phase (Phoenix) — 4 Engines"

echo ""
echo "  Engine 1/8: FLQG₁ — First-Level Quantum Geometry"
check_file "Phoenix/apex-engine/engines/FLQG1.md" "FLQG₁ documentation exists"
check_content "Phoenix/apex-engine/engines/FLQG1.md" "FLQG₁" "FLQG₁ symbol notation present"
check_content "Phoenix/apex-engine/engines/FLQG1.md" "substrate" "Substrate mechanics documented"

echo ""
echo "  Engine 2/8: FLQG₂ — Second-Level Quantum Geometry"
check_file "Phoenix/apex-engine/engines/FLQG2.md" "FLQG₂ documentation exists"
check_content "Phoenix/apex-engine/engines/FLQG2.md" "FLQG₂" "FLQG₂ symbol notation present"
check_content "Phoenix/apex-engine/engines/FLQG2.md" "harmonic" "Harmonic mechanics documented"

echo ""
echo "  Engine 3/8: Reproduction Engine (ℜ)"
check_file "Phoenix/apex-engine/engines/reproduction-engine.md" "Reproduction Engine documentation exists"
check_content "Phoenix/apex-engine/engines/reproduction-engine.md" "ℜ" "ℜ symbol notation present"
check_content "Phoenix/apex-engine/engines/reproduction-engine.md" "replication" "Replication mechanics documented"

echo ""
echo "  Engine 4/8: Relativity Engine (ℛ)"
check_file "Phoenix/apex-engine/engines/relativity-engine.md" "Relativity Engine documentation exists"
check_content "Phoenix/apex-engine/engines/relativity-engine.md" "ℛ" "ℛ symbol notation present"
check_content "Phoenix/apex-engine/engines/relativity-engine.md" "relativity" "Relativity mechanics documented"

# ============================================================
# PHASE 2: Flight Phase (Hydrogenesi) — 3 Theories
# ============================================================
echo ""
print_section "Phase 2: Flight Phase (Hydrogenesi) — 3 Theories"

echo ""
echo "  Engine 5/8: TOR₁ — Theory of Recursion Level 1"
check_file "Hydrogenesi/apex-engine/theories/TOR1.md" "TOR₁ documentation exists"
check_content "Hydrogenesi/apex-engine/theories/TOR1.md" "TOR₁" "TOR₁ symbol notation present"
check_content "Hydrogenesi/apex-engine/theories/TOR1.md" "recursion" "Recursion mechanics documented"

echo ""
echo "  Engine 6/8: TOR₂ — Theory of Recursion Level 2"
check_file "Hydrogenesi/apex-engine/theories/TOR2.md" "TOR₂ documentation exists"
check_content "Hydrogenesi/apex-engine/theories/TOR2.md" "TOR₂" "TOR₂ symbol notation present"
check_content "Hydrogenesi/apex-engine/theories/TOR2.md" "meta-recursion" "Meta-recursion mechanics documented"

echo ""
echo "  Engine 7/8: TOR₃ — Theory of Recursion Level 3"
check_file "Hydrogenesi/apex-engine/theories/TOR3.md" "TOR₃ documentation exists"
check_content "Hydrogenesi/apex-engine/theories/TOR3.md" "TOR₃" "TOR₃ symbol notation present"
check_content "Hydrogenesi/apex-engine/theories/TOR3.md" "convergent" "Convergent recursion documented"

# ============================================================
# PHASE 3: Return Phase (The Third) — 1 Theory
# ============================================================
echo ""
print_section "Phase 3: Return Phase (The Third) — 1 Theory"

echo ""
echo "  Engine 8/8: TOE — Theory of Everything"
check_file "TheThird/apex-engine/TOE.md" "TOE documentation exists"
check_content "TheThird/apex-engine/TOE.md" "TOE" "TOE acronym present"
check_content "TheThird/apex-engine/TOE.md" "integration" "Integration mechanics documented"
check_content "TheThird/apex-engine/TOE.md" "apex" "Apex convergence documented"

# ============================================================
# INTEGRATION CHECKS
# ============================================================
echo ""
print_section "Integration Validation"

echo ""
echo "  Cross-Engine References"
check_file "Phoenix/apex-engine/README.md" "Phoenix Apex Engine README exists"
check_file "Hydrogenesi/apex-engine/README.md" "Hydrogenesi Apex Engine README exists"
check_file "TheThird/apex-engine/README.md" "The Third Apex Engine README exists"

echo ""
echo "  Master Index"
check_file "Atlases/ApexEngineIndex.md" "Apex Engine Index exists"
check_content "Atlases/ApexEngineIndex.md" "FLQG₁" "Index references FLQG₁"
check_content "Atlases/ApexEngineIndex.md" "FLQG₂" "Index references FLQG₂"
check_content "Atlases/ApexEngineIndex.md" "TOR₁" "Index references TOR₁"
check_content "Atlases/ApexEngineIndex.md" "TOR₂" "Index references TOR₂"
check_content "Atlases/ApexEngineIndex.md" "TOR₃" "Index references TOR₃"
check_content "Atlases/ApexEngineIndex.md" "TOE" "Index references TOE"

echo ""
echo "  Cycle Mapping"
check_file "Phoenix/apex-engine/cycle-mapping.md" "Cycle mapping documentation exists"

# ============================================================
# DOCUMENTATION COMPLETENESS
# ============================================================
echo ""
print_section "Documentation Completeness"

echo ""
echo "  Audit Schema"
check_file "docs/apex/apex-engine-audit-schema.md" "Audit schema exists"
check_file "docs/apex/apex-audit-quickstart.md" "Audit quickstart exists"

# ============================================================
# RESULTS SUMMARY
# ============================================================
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""
echo "Audit Results:"
echo "  Total Checks:  $total_checks"
echo -e "  Passed:        ${GREEN}$passed_checks${NC}"
echo -e "  Failed:        ${RED}$failed_checks${NC}"
echo ""

# Calculate percentage
if [ $total_checks -gt 0 ]; then
    percentage=$((passed_checks * 100 / total_checks))
    echo "  Success Rate:  $percentage%"
    echo ""
    
    if [ $failed_checks -eq 0 ]; then
        echo -e "${GREEN}✓ AUDIT PASSED${NC} — All engines validated"
        echo ""
        exit 0
    elif [ $percentage -ge 95 ]; then
        echo -e "${YELLOW}⚠ AUDIT PASSED WITH WARNINGS${NC} — Minor issues detected"
        echo ""
        exit 0
    elif [ $percentage -ge 85 ]; then
        echo -e "${YELLOW}⚠ AUDIT INCOMPLETE${NC} — Significant gaps detected"
        echo ""
        exit 1
    else
        echo -e "${RED}✗ AUDIT FAILED${NC} — Major issues detected"
        echo ""
        exit 1
    fi
else
    echo -e "${RED}✗ AUDIT ERROR${NC} — No checks executed"
    echo ""
    exit 1
fi
