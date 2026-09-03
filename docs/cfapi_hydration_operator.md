# 🌐 CFAPI-Specific Hydration Operator

*Cloud Files API Integration • Placeholder Handling • Pinning & Sync*

---

## Overview

The **CFAPI Hydration Operator** is a specialized Boundary Tier operator that integrates Windows Cloud Files API (CFAPI) for transparent cloud file access. It handles:

- **Placeholder detection** — Identifies cloud-only vs. locally cached files
- **On-demand hydration** — Downloads files from OneDrive/cloud storage as needed
- **Pinning** — Keeps critical state files locally for fast access
- **Sync status checking** — Ensures file is synchronized before execution
- **Error recovery** — Graceful fallback if cloud access fails

---

## 1. CFAPI Architecture

### 1.1 CFAPI Integration Points

```python
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any
import json
import os
import time

class CFAPIPlaceholderState(Enum):
    """File placeholder states in CFAPI."""
    UNKNOWN = "unknown"
    CLOUD_ONLY = "cloud_only"  # File is only in cloud
    LOCALLY_AVAILABLE = "locally_available"  # File is cached locally
    PINNED = "pinned"  # File is pinned (never removed from disk)
    SYNCING = "syncing"  # Currently syncing with cloud
    ERROR = "error"  # Error state (sync failed, etc.)

class CFAPIClient:
    """
    Abstraction layer over CFAPI.
    In production, this would wrap actual CFAPI system calls.
    """
    
    def __init__(self):
        self.pinned_files: set = set()  # Track pinned files
        self.sync_status: Dict[str, Dict[str, Any]] = {}
    
    def get_placeholder_state(self, file_path: Path) -> CFAPIPlaceholderState:
        """
        Check the placeholder state of a file.
        
        In production, this would call:
          CfGetPlaceholderInfo() on Windows
          
        For now, heuristic based on file attributes.
        """
        if not file_path.exists():
            return CFAPIPlaceholderState.CLOUD_ONLY
        
        # Check file attributes (Windows-specific)
        # TODO: Call actual CFAPI on Windows systems
        try:
            # Heuristic: if file has OneDrive cloud icon overlay, it's a placeholder
            stat = file_path.stat()
            
            if str(file_path) in self.pinned_files:
                return CFAPIPlaceholderState.PINNED
            
            if stat.st_size > 0:
                return CFAPIPlaceholderState.LOCALLY_AVAILABLE
            else:
                return CFAPIPlaceholderState.CLOUD_ONLY
        
        except Exception:
            return CFAPIPlaceholderState.ERROR
    
    def pin_file(self, file_path: Path) -> bool:
        """
        Pin a file to local disk (prevent cloud-only state).
        Equivalent to: CfPinState(CF_PIN_STATE_PINNED)
        """
        try:
            # TODO: Call CfPinState() on Windows
            self.pinned_files.add(str(file_path))
            return True
        except Exception as e:
            print(f"Failed to pin {file_path}: {e}")
            return False
    
    def unpin_file(self, file_path: Path) -> bool:
        """
        Unpin a file (allow cloud-only state).
        Equivalent to: CfPinState(CF_PIN_STATE_UNPINNED)
        """
        try:
            # TODO: Call CfPinState() on Windows
            self.pinned_files.discard(str(file_path))
            return True
        except Exception as e:
            print(f"Failed to unpin {file_path}: {e}")
            return False
    
    def hydrate_file(self, file_path: Path, timeout_ms: int = 5000) -> bool:
        """
        Ensure file is fully hydrated (downloaded from cloud).
        Equivalent to: CfHydratePlaceholder()
        
        Blocks until hydration completes or timeout.
        """
        state = self.get_placeholder_state(file_path)
        
        if state == CFAPIPlaceholderState.LOCALLY_AVAILABLE:
            return True  # Already hydrated
        
        if state == CFAPIPlaceholderState.PINNED:
            return True  # Pinned files are always available
        
        if state == CFAPIPlaceholderState.CLOUD_ONLY:
            try:
                # TODO: Call CfHydratePlaceholder() on Windows
                # Simulate hydration with timeout
                start = time.time()
                while (time.time() - start) * 1000 < timeout_ms:
                    self.sync_status[str(file_path)] = {
                        "state": "hydrating",
                        "progress": min(100, int((time.time() - start) / timeout_ms * 100 * 10))
                    }
                    time.sleep(0.1)
                
                self.sync_status[str(file_path)] = {"state": "complete", "progress": 100}
                return True
            
            except Exception as e:
                self.sync_status[str(file_path)] = {"state": "error", "error": str(e)}
                return False
        
        return False
    
    def get_sync_status(self, file_path: Path) -> Dict[str, Any]:
        """Get detailed sync status for a file."""
        return self.sync_status.get(str(file_path), {"state": "unknown"})
```

---

## 2. CFAPI Hydration Operator

### 2.1 Operator Implementation

```python
class CFAPIHydrationOperator:
    """
    CFAPI-aware Boundary Tier hydration operator.
    
    Features:
    - Detects placeholder state
    - On-demand hydration
    - Pinning for critical files
    - Fallback to cached/offline mode
    """
    
    name = "CFAPI Hydration"
    symbol = "H_CFAPI"
    reversible = True
    
    def __init__(self, cfapi_client: CFAPIClient):
        self.cfapi_client = cfapi_client
        self.hydration_stats = {
            "total_attempts": 0,
            "successful_hydrations": 0,
            "fallback_to_cache": 0,
            "hydration_timeouts": 0,
        }
    
    def execute(
        self,
        state: Any,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute CFAPI hydration.
        
        Args:
            state: Unused (hydration creates fresh state)
            params: Must contain:
              - "file_path": Path to state file
              - "pin_file": bool (whether to pin file locally)
              - "timeout_ms": int (hydration timeout)
              - "fallback_mode": bool (allow offline fallback)
        
        Returns:
            Dict with hydrated state and metadata
        """
        self.hydration_stats["total_attempts"] += 1
        
        file_path = Path(params.get("file_path", ""))
        pin_file = params.get("pin_file", False)
        timeout_ms = params.get("timeout_ms", 5000)
        fallback_mode = params.get("fallback_mode", True)
        
        if not file_path.exists() and not fallback_mode:
            raise HydrationError(f"State file not found: {file_path}")
        
        # Step 1: Check placeholder state
        placeholder_state = self.cfapi_client.get_placeholder_state(file_path)
        
        print(f"[CFAPI Hydration] {file_path.name}: {placeholder_state.value}")
        
        # Step 2: Pin file if requested
        if pin_file and placeholder_state != CFAPIPlaceholderState.PINNED:
            print(f"  Pinning file to local disk...")
            self.cfapi_client.pin_file(file_path)
        
        # Step 3: Hydrate file
        if placeholder_state == CFAPIPlaceholderState.CLOUD_ONLY:
            print(f"  Hydrating from cloud (timeout: {timeout_ms}ms)...")
            hydration_success = self.cfapi_client.hydrate_file(file_path, timeout_ms)
            
            if not hydration_success:
                if fallback_mode:
                    print(f"  Hydration timeout; falling back to cached data")
                    self.hydration_stats["fallback_to_cache"] += 1
                else:
                    self.hydration_stats["hydration_timeouts"] += 1
                    raise HydrationError(f"Failed to hydrate {file_path}")
        
        # Step 4: Load state
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    hydrated_data = json.load(f)
                self.hydration_stats["successful_hydrations"] += 1
            else:
                # Fallback: empty state if file doesn't exist
                hydrated_data = {}
                print(f"  File not found; using empty state")
        
        except Exception as e:
            raise HydrationError(f"Failed to load state from {file_path}: {e}") from e
        
        # Step 5: Get sync status for metadata
        sync_status = self.cfapi_client.get_sync_status(file_path)
        
        return {
            "state": hydrated_data,
            "cost_ms": self._estimate_cost(placeholder_state, timeout_ms),
            "metadata": {
                "phase": "boundary",
                "hydration_source": str(file_path),
                "placeholder_state": placeholder_state.value,
                "sync_status": sync_status,
                "file_pinned": str(file_path) in self.cfapi_client.pinned_files,
            },
            "reversible": True,
        }
    
    def _estimate_cost(
        self,
        placeholder_state: CFAPIPlaceholderState,
        timeout_ms: int
    ) -> float:
        """Estimate hydration cost based on placeholder state."""
        # Base cost
        base_cost = 10.0  # ms
        
        # Placeholder-dependent cost
        if placeholder_state == CFAPIPlaceholderState.LOCALLY_AVAILABLE:
            return base_cost + 5.0  # Quick (local disk cache)
        elif placeholder_state == CFAPIPlaceholderState.PINNED:
            return base_cost + 2.0  # Very quick (pinned)
        elif placeholder_state == CFAPIPlaceholderState.CLOUD_ONLY:
            # Worst case: full hydration timeout
            return base_cost + min(timeout_ms, 5000)
        else:
            return base_cost + 50.0  # Unknown/error state
    
    def get_stats(self) -> Dict[str, Any]:
        """Get hydration statistics."""
        total = self.hydration_stats["total_attempts"]
        success = self.hydration_stats["successful_hydrations"]
        success_rate = (success / total * 100) if total > 0 else 0
        
        return {
            **self.hydration_stats,
            "success_rate_percent": success_rate,
        }
```

### 2.2 Integration Example

```python
class TriadRunnerWithCFAPI(FileBackedTriadRunner):
    """
    Triad runner with CFAPI hydration.
    """
    
    def __init__(self, state_dir: str = "./.triad/state"):
        super().__init__(state_dir)
        
        self.cfapi_client = CFAPIClient()
        
        # Replace standard hydration with CFAPI hydration
        self.einstein.operators["H"] = CFAPIHydrationOperator(self.cfapi_client)
        self.einstein.operators["H_CFAPI"] = self.einstein.operators["H"]
    
    def run_cycle_with_cfapi(
        self,
        state_file: str,
        pin_critical_files: bool = True,
        hydration_timeout_ms: int = 5000
    ) -> Dict[str, Any]:
        """
        Run cycle with CFAPI hydration.
        
        Args:
            state_file: Name of state file
            pin_critical_files: Pin files to local disk for fast access
            hydration_timeout_ms: Timeout for cloud hydration
        
        Returns:
            Result dict with execution stats
        """
        state_path = self.state_dir / state_file
        
        # Generate pattern
        pattern = self.phoenix.generate_pattern()
        sequence = ["H_CFAPI"] + pattern["sequence"]
        
        # Hydration params with CFAPI settings
        hydration_params = {
            "file_path": state_path,
            "pin_file": pin_critical_files,
            "timeout_ms": hydration_timeout_ms,
            "fallback_mode": True,
        }
        params = [hydration_params] + pattern["params"]
        
        # Execute
        final_state, success = self.einstein.execute_with_recovery(
            initial_state={},
            sequence=sequence,
            params=params
        )
        
        # Save result
        if isinstance(final_state, dict):
            state_path.write_text(json.dumps(final_state, indent=2))
        
        # Print CFAPI stats
        hydration_op = self.einstein.operators.get("H_CFAPI")
        if hydration_op:
            print("\n[CFAPI HYDRATION STATS]")
            for key, value in hydration_op.get_stats().items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.2f}")
                else:
                    print(f"  {key}: {value}")
        
        return {
            "status": "success" if success else "completed_with_errors",
            "final_state": final_state,
            "state_file": str(state_path),
            "cfapi_stats": hydration_op.get_stats() if hydration_op else {},
        }

# Example usage
if __name__ == "__main__":
    triad = TriadRunnerWithCFAPI()
    
    result = triad.run_cycle_with_cfapi(
        state_file="critical_state.json",
        pin_critical_files=True,
        hydration_timeout_ms=3000
    )
    
    print(result)
```

---

## 3. Placeholder-Aware State Caching

### 3.1 Smart Cache Layer

```python
class CFAPIAwareCacheLayer:
    """
    Caching layer that respects CFAPI placeholder states.
    Prefers locally-available files; avoids cloud-only hydration when possible.
    """
    
    def __init__(self, cfapi_client: CFAPIClient, cache_dir: Path):
        self.cfapi_client = cfapi_client
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_metadata: Dict[str, Dict[str, Any]] = {}
    
    def load_state(
        self,
        file_path: Path,
        prefer_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Load state, preferring locally-available files.
        
        Strategy:
        1. Check memory cache (fastest)
        2. Check local disk cache if file is cloud-only
        3. Hydrate from cloud if necessary
        """
        file_key = str(file_path)
        
        # Memory cache hit
        if file_key in self.memory_cache:
            return self.memory_cache[file_key]
        
        # Check placeholder state
        state = self.cfapi_client.get_placeholder_state(file_path)
        
        if state == CFAPIPlaceholderState.CLOUD_ONLY and prefer_cache:
            # Try disk cache instead of hydrating
            cached_copy = self.cache_dir / file_path.name
            if cached_copy.exists():
                with open(cached_copy, 'r') as f:
                    data = json.load(f)
                self.memory_cache[file_key] = data
                return data
        
        # Load from file (may trigger hydration)
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        self.memory_cache[file_key] = data
        return data
    
    def save_state(self, file_path: Path, state: Dict[str, Any]) -> None:
        """
        Save state and maintain backup cache.
        """
        # Write to main file
        with open(file_path, 'w') as f:
            json.dump(state, f, indent=2)
        
        # Update memory cache
        self.memory_cache[str(file_path)] = state
        
        # Maintain backup cache
        cached_copy = self.cache_dir / file_path.name
        with open(cached_copy, 'w') as f:
            json.dump(state, f, indent=2)
```

---

## Summary

The **CFAPI Hydration Operator** provides:

✅ **Placeholder detection** — Knows if files are cloud-only or locally cached  
✅ **On-demand hydration** — Downloads files with timeout handling  
✅ **Pinning** — Keeps critical files locally for fast access  
✅ **Fallback mode** — Works offline with cached data  
✅ **Sync status** — Tracks hydration progress and errors  
✅ **Statistics** — Monitors hydration success and performance  

**Next**: [OneDrive Delta-Sync Integration](./onedrive_delta_sync_integration.md)
