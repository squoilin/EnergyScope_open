# PyOptInterface Model - Performance Optimization Strategy

**Date**: October 25, 2025

## Current Performance

```
Data loading:       0.15s (  0.2%)
Model building:    40.44s ( 43.3%)  ← BOTTLENECK
Solving:           52.88s ( 56.6%)
TOTAL:             93.49s
```

**Model Statistics:**
- Variables: ~675,638
- F: 108, F_t: 39,168, Storage vars: 622,200
- Model size: ~1.1M constraints

**Comparison with AMPL:**
- AMPL solve time: ~40s (just solving)
- PyOptInterface total time: ~93s (building + solving)

## Performance Bottleneck Analysis

### 1. Model Building (40.4s - 43.3% of time)

**Root Causes:**
1. **Nested loops**: Many constraints use triple/quadruple nested loops over (LAYERS × HOURS × TYPICAL_DAYS)
   - Example: End-uses calculation, Layer balance, Storage constraints
   - Creates hundreds of thousands of individual constraint additions

2. **Individual constraint additions**: Each `model.add_linear_constraint()` call has overhead
   - With ~1.1M constraints, even small per-call overhead accumulates
   - PyOptInterface is fast, but still slower than bulk operations

3. **Expression building**: Complex expressions with many sum() operations
   - Example: Layer balance sums over all technologies and storage
   - Each expression object creation has overhead

### 2. Solving Time (52.9s - 56.6% of time)

**Analysis:**
- Gurobi solving time is reasonable for model size
- 1.1M constraints, 675K variables is a large model
- AMPL takes ~40s, PyOptInterface ~53s (25% slower, acceptable)

## Optimization Strategies

### Strategy 1: Reduce Constraint Count ⭐⭐⭐ (High Priority)

**Problem:** 1.1M constraints vs AMPL's ~487K (2.25x more)

**Investigation needed:**
```python
# Count constraints by type to identify bloat
constraint_counts = {
    'end_uses': len(LAYERS) * len(HOURS) * len(TYPICAL_DAYS),  # ~8,640
    'layer_balance': len(LAYERS) * len(HOURS) * len(TYPICAL_DAYS),  # ~8,640
    'hourly_cf': len(ALL_TECH) * len(HOURS) * len(TYPICAL_DAYS),  # ~311,040
    'storage_level': len(STORAGE_TECH) * len(PERIODS),  # ~210,000
    'storage_compatibility': len(STORAGE_TECH) * len(LAYERS) * len(HOURS) * len(TYPICAL_DAYS) * 2,  # ~1,036,800
}
```

**Action:** The storage layer compatibility constraints (Eq. 2.17-2.18) are likely the culprit.
- Current: Adding constraints even when coefficient is 0
- Fix: Only add constraints where `ceil(eff) - 1 != 0` (i.e., when eff == 0)

**Expected Impact:** Could reduce from 1.1M to ~500K constraints, cutting build time in half.

### Strategy 2: Use Batch Constraint Addition ⭐⭐ (Medium Priority)

According to [PyOptInterface documentation](https://metab0t.github.io/PyOptInterface/), batch operations are faster.

**Current approach:**
```python
for j in STORAGE_TECH:
    for l in LAYERS:
        for h in HOURS:
            for td in TYPICAL_DAYS:
                model.add_linear_constraint(...)  # Individual calls
```

**Optimized approach:**
```python
# Collect all constraints first, then add in batch
constraints = []
for j in STORAGE_TECH:
    for l in LAYERS:
        if storage_eff_in.get((j, l), 0) == 0:  # Only where needed
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    constraints.append(Storage_in[j, l, h, td] == 0)

# Add all at once (if PyOptInterface supports batch addition)
# Otherwise, at least we've pre-filtered
```

**Expected Impact:** 10-20% reduction in build time.

### Strategy 3: Pre-compute Sums and Expressions ⭐⭐ (Medium Priority)

**Problem:** Repeated computation of same expressions

**Example optimization:**
```python
# BEFORE (slow):
for l in LAYERS:
    for h in HOURS:
        for td in TYPICAL_DAYS:
            balance_expr = sum(
                layers_in_out.get((entity, l), 0) * F_t[entity, h, td]
                for entity in (RESOURCES + TECH_NOSTORAGE)
            )
            # ...

# AFTER (faster):
# Pre-filter entities by layer
entities_by_layer = {}
for l in LAYERS:
    entities_by_layer[l] = [
        e for e in (RESOURCES + TECH_NOSTORAGE) 
        if layers_in_out.get((e, l), 0) != 0
    ]

# Then use in loop
for l in LAYERS:
    entities = entities_by_layer[l]  # Much smaller list
    for h in HOURS:
        for td in TYPICAL_DAYS:
            balance_expr = sum(
                layers_in_out[(e, l)] * F_t[e, h, td]
                for e in entities  # Pre-filtered
            )
```

**Expected Impact:** 5-10% reduction in build time.

### Strategy 4: Optimize Storage Compatibility Constraints ⭐⭐⭐ (High Priority - Easy Win)

**Current code:**
```python
for j in STORAGE_TECH:
    for l in LAYERS:
        eff_in = storage_eff_in.get((j, l), 0)
        coef_in = math.ceil(eff_in) - 1
        if coef_in != 0:  # Only when eff=0
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    model.add_linear_constraint(Storage_in[j, l, h, td] * coef_in == 0)
```

**Problem:** When `coef_in == -1` (eff=0), this adds: `Storage_in * (-1) == 0` which is just `Storage_in == 0`

**Better approach:**
```python
for j in STORAGE_TECH:
    for l in LAYERS:
        eff_in = storage_eff_in.get((j, l), 0)
        if eff_in == 0:  # Direct check
            for h in HOURS:
                for td in TYPICAL_DAYS:
                    model.add_linear_constraint(Storage_in[j, l, h, td] == 0)
```

Or even better - **don't create the variables at all** if efficiency is 0:
```python
# During variable creation:
Storage_in = {
    (s, l, h, td): model.add_variable(lb=0, name=f"Storage_in_{s}_{l}_{h}_{td}")
    for s in STORAGE_TECH 
    for l in LAYERS 
    if storage_eff_in.get((s, l), 0) > 0  # Only create if compatible
    for h in HOURS 
    for td in TYPICAL_DAYS
}
```

**Expected Impact:** 
- Eliminates ~500K unnecessary constraints
- Reduces variables by ~300K
- Could reduce build time by 40-50%

### Strategy 5: Parallel Model Building ⭐ (Low Priority, Complex)

PyOptInterface may support parallel constraint addition (check docs).

**Approach:**
- Build constraint groups in parallel threads
- Requires careful handling of shared model object

**Expected Impact:** 20-30% reduction if supported.

### Strategy 6: Use Gurobi's Model.update() Less Frequently ⭐ (Low Priority)

Check if PyOptInterface calls Gurobi's `update()` after each constraint.

**Expected Impact:** Minimal, likely already optimized.

## Recommended Implementation Plan

### Phase 1: Quick Wins (Target: 30-40% improvement)

1. ✅ **Add timing measurement** (DONE)
   - Identify bottlenecks

2. **Optimize storage compatibility constraints**
   ```python
   # Only create storage variables where efficiency > 0
   # Eliminates ~500K constraints and ~300K variables
   ```
   - Expected: Build time 40s → 20-25s
   - Effort: 1-2 hours

3. **Pre-filter entities by layer**
   ```python
   # Filter once, use many times
   ```
   - Expected: Build time → 15-20s
   - Effort: 2-3 hours

### Phase 2: Medium Improvements (Target: additional 10-15%)

4. **Optimize nested loops**
   - Use list comprehensions instead of explicit loops where possible
   - Pre-compute commonly used values
   - Expected: Build time → 12-17s
   - Effort: 3-4 hours

5. **Check for redundant constraints**
   - Analyze constraint count by type
   - Compare with AMPL's constraint count
   - Expected: Variable
   - Effort: 2-3 hours

### Phase 3: Advanced Optimizations (Target: additional 5-10%)

6. **Profile with cProfile**
   ```python
   import cProfile
   cProfile.run('build_and_run_full_model()', sort='cumtime')
   ```
   - Identify hotspots
   - Expected: Various small improvements
   - Effort: 4-6 hours

7. **Consider Gurobi parameters**
   ```python
   model.set_raw_parameter("Threads", 8)  # Use more threads
   model.set_raw_parameter("Method", 3)   # Try concurrent method
   ```
   - Expected: Solve time 53s → 40-45s
   - Effort: 1 hour

## Expected Final Performance

**Current:**
```
Building: 40.4s
Solving:  52.9s
Total:    93.5s
```

**After Phase 1 (realistic):**
```
Building: 15-20s  (↓60%)
Solving:  52.9s
Total:    68-73s  (↓25%)
```

**After All Phases (optimistic):**
```
Building: 10-15s  (↓75%)
Solving:  40-45s  (↓20%)
Total:    50-60s  (↓45%)
```

**Comparison to AMPL:**
- AMPL: ~40s (solving only, building is in C++)
- PyOptInterface target: ~50-60s (building + solving in Python)
- Acceptable performance for a pure Python implementation

## References

- [PyOptInterface Documentation](https://metab0t.github.io/PyOptInterface/)
- [Gurobi Performance Tips](https://www.gurobi.com/documentation/current/refman/performance_tips.html)
- Model implementation: `scripts/pyoptinterface_full_model.py`

---

**Next Steps:**
1. Implement Phase 1 optimizations
2. Measure improvement
3. Profile with cProfile
4. Decide if Phase 2/3 are needed

*Document created: October 25, 2025*

