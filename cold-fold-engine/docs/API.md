# API reference

Generated from the package docstrings (`cold_fold_engine` 7.1.0).


## `OriginNucleus()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `DivisionAttempt()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`partition(self, state: 'EngineState') -> 'tuple[int, int, int]'`**: Return (target_groups, group_size, residue) without changing state.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `StalledFold()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `HingeBand()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `VacuumDynamo()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `CrestGenesis()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `StarGenesis()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `GalaxyGenesis()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `MasterPlate()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `CosmogenicEngine(pipeline: 'tuple[Plate, ...] | None' = None, tension_cap: 'int | None' = None, bus: 'Any' = None) -> 'None'`

Ordered pipeline runner with a tension governor.


- **`governor_trip(self, state: 'EngineState') -> 'str | None'`**: Return a trip reason if the state violates a governor bound.

- **`pass_once(self, state: 'EngineState') -> 'tuple[EngineState, list[PlateResult], str | None]'`**: Run every plate once, in order. Returns (state, results, halt_reason).

- **`run(self, max_passes: 'int' = 8, state: 'EngineState | None' = None) -> 'Trace'`**: Run passes until the state seals, stops advancing, or halts.

- **`run_to_completion(self, state: 'EngineState | None' = None) -> 'dict[str, Any]'`**: Dict-returning form matching the original stub API.



## `Runtime(perturbations: 'tuple[Perturbation, ...]' = (), engine: 'CosmogenicEngine | None' = None, state: 'EngineState | None' = None) -> 'None'`

Plate-at-a-time driver with a perturbation schedule.


- **`reset(self) -> 'None'`**

- **`run(self, max_steps: 'int' = 120) -> 'Trace'`**: Advance up to `max_steps` plate executions.



## `Perturbation(step: 'int', kind: 'str', magnitude: 'int' = 0) -> None`

A scheduled, deterministic external nudge.

Perturbations are the only source of non-monotonic change in a run. They
are declared up front with fixed step indices and magnitudes -- there is no
randomness anywhere in the engine, which is what makes the trace digest
reproducible.


- **`apply(self, state: 'EngineState') -> 'tuple[EngineState, str]'`**

- **`to_dict(self) -> 'dict[str, Any]'`**



## `DEFAULT_SCENARIO`

Constant: `(Perturbation(step=40, kind='tension', magnitude=6), Perturbation(step=60, kind='unseal', magnitude=0), Perturbation(step=95, kind='tension', magnitude=200))`


## `ColdFoldV7(pipeline: 'tuple[Plate, ...] | None' = None, tension_cap: 'int | None' = None, bus: 'Any' = None) -> 'None'`

Ordered pipeline runner with a tension governor.


- **`governor_trip(self, state: 'EngineState') -> 'str | None'`**: Return a trip reason if the state violates a governor bound.

- **`pass_once(self, state: 'EngineState') -> 'tuple[EngineState, list[PlateResult], str | None]'`**: Run every plate once, in order. Returns (state, results, halt_reason).

- **`run(self, max_passes: 'int' = 8, state: 'EngineState | None' = None) -> 'Trace'`**: Run passes until the state seals, stops advancing, or halts.

- **`run_to_completion(self, state: 'EngineState | None' = None) -> 'dict[str, Any]'`**: Dict-returning form matching the original stub API.



## `default_pipeline() -> 'tuple[Plate, ...]'`

Plates in dependency order.

Note this is NOT ascending plate number: VacuumDynamo (4) must run after
HingeBand (3) but before CrestGenesis (5), and the 71/72/74 engine-set
plates run last. Execution order is set by data dependency.


## `Plate()`

A single named stage in the pipeline.

Subclasses set `number` and `label` and override `apply`. Override `check`
to declare preconditions and `verify` to declare postconditions.


- **`apply(self, state: 'EngineState') -> 'EngineState'`**: Pure transition. Must not mutate `state`.

- **`as_record(self, index: 'int', result: 'PlateResult') -> 'StepRecord'`**

- **`check(self, state: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of unmet preconditions. Empty tuple = runnable.

- **`narrate(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Human-readable summary of what changed. Derived, never authoritative.

- **`run(self, state: 'EngineState') -> 'PlateResult'`**: Execute the plate against `state`, returning a real outcome.

- **`run_to_completion(self, state: 'EngineState | None' = None) -> 'PlateResult'`**: Compatibility alias for the original stub API.

- **`verify(self, before: 'EngineState', after: 'EngineState') -> 'tuple[str, ...]'`**: Return descriptions of violated postconditions. Empty tuple = valid.



## `PlateResult(plate: 'int', label: 'str', status: 'Status', state_before: 'EngineState', state_after: 'EngineState', reasons: 'tuple[str, ...]' = (), history: 'tuple[str, ...]' = ()) -> None`

Outcome of one plate execution.


- **`to_dict(self) -> 'dict[str, Any]'`**



## `EngineState(tension: 'int' = 0, band: 'int' = 0, echo: 'int' = 1, nodes: 'int' = 127, folded: 'bool' = False, stalled: 'bool' = False, sealed: 'bool' = False) -> None`

Immutable engine state.

Frozen so that stages cannot mutate shared state by accident; every stage
returns a new state via `EngineState.evolve`. This is what makes replay and
the determinism digest meaningful.


- **`evolve(self, **changes: 'Any') -> 'EngineState'`**: Return a new state with `changes` applied, clamped to legal ranges.

- **`to_dict(self) -> 'dict[str, Any]'`**



## `EngineError`

Raised on a structural misuse of the engine (not a modelled failure).




## `Status(*values)`

Terminal status of a plate or cycle step.

A stage that cannot fail cannot inform. BLOCKED and FAILED are real,
reachable outcomes -- see `Plate.check`.




## `StepRecord(index: 'int', source: 'str', status: 'Status', state: 'EngineState', notes: 'tuple[str, ...]' = ()) -> None`

One recorded transition.


- **`to_dict(self) -> 'dict[str, Any]'`**



## `Trace(records: 'list[StepRecord]' = <factory>) -> None`

An ordered list of StepRecords, plus a content digest.

`len(trace)` is the number of recorded steps, so the launcher idiom
`print('steps', len(tr))` works as written in coldfold.ps1.


- **`append(self, record: 'StepRecord') -> 'None'`**

- **`digest(self) -> 'str'`**: SHA-256 over the canonical JSON form of the trace.

- **`statuses(self) -> 'dict[str, int]'`**

- **`to_dict(self) -> 'dict[str, Any]'`**



## `CYCLES`

Registry: relativistic, collapse, demo


## `SUBSTRATE_NODES`

Constant: `127`


## `ECHO_BANDS`

Constant: `(1, 2, 3, 4, 5, 6, 7, 8, 9)`


## `CANON_THRESHOLD`

Constant: `3`


## `OCTAVE_LADDER`

Constant: `(('HA-0', 'Substrate'), ('HA-1', 'Spark'), ('HA-2', 'Vector'), ('HA-3', 'Frame'), ('HA-4', 'Harmonic'), ('HA-5', 'Operator'), ('HA-6', 'Engine'), ('HA-7', 'Crown'), ('HA-8', 'Apex'))`


## `MAX_BAND`

Constant: `8`
