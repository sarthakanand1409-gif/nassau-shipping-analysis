### 1. Introduction
**Background:** Nassau Candy Distributor operates as a national distributor across 5 factories...

**Problem:** Despite rich order/shipment data, logistics decisions are made without route-level efficiency intelligence...

**Objectives:**
- Identify consistently efficient routes
- Detect routes with frequent delays
- Map geographic bottlenecks
- Compare ship mode performance

### 2. Data & Methodology
**Dataset:** 10,194 shipment records, 18 fields, [date range]

**Methodology:**
- Data cleaning: validated dates, removed invalid lead times
- Feature engineering: lead time, route IDs, factory mapping, profit margin
- KPI computation: 7 route-level metrics
- Geographic analysis: state-level aggregation with bottleneck flagging

### 3. Exploratory Findings
- Lead time distribution: [insert numbers]
- Volume by region: [insert breakdown]
- Time trend: [observation]
- (Embed images saved on Day 6)

### 4. KPI Results
[Insert table from Day 5]
- Top 10 most efficient routes (table)
- Bottom 10 least efficient routes (table)

### 5. Geographic Bottlenecks
- Critical bottleneck states: [list]
- Pacific region underserved by Sugar Shack? [analyze]
- Top 5 high-volume + slow states

### 6. Ship Mode Tradeoffs
- Same Day vs Standard: [comparison]
- Cost-time tradeoffs: [observation]

### 7. Recommendations
1. **Distribution hub:** Open Pacific hub to reduce Sugar Shack reach
2. **Ship mode policy:** Upgrade orders > $X to faster mode for bottleneck states
3. **Carrier audit:** Investigate states with >2× avg lead time
4. **Capacity planning:** Pre-position inventory in Q4 for high-volume states

### 8. Conclusion
This analysis transforms raw order and shipment data into route-level operational intelligence,
giving Nassau Candy Distributor data-driven leverage to improve logistics performance,
reduce delays, and enhance nationwide delivery reliability.

### Appendix
- Dataset schema (full)
- Factory coordinates
- Full KPI tables
- Charts and visualizations