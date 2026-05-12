# Proofreading Issues

Tracking all issues found in the paper. Mark with `[x]` when fixed.

## paper.tex / preamble

None.

## sections/1-intro.tex

- [x] **#1** [L28] "is a important" → "an important"
- [x] **#65** Add explicit contributions list at end of intro
- [x] **#41** [L101] Cite consistency for P-completeness — use `unification` (Kanellakis-Revesz) for the CC-specific result; `p-complete` (Greenlaw-Hoover-Ruzzo) for the P-completeness definition
- [x] **#40** [L73-77] Algorithm sketch crammed primitives (`flat_map`, `filter`) before they're introduced — defer to §3
- [x] **#2** [L66] "our algorithms replaces" → "replace" (fixed as part of #40)
- [x] **#3** [L83] "keeps track of parents list" → rewrote the paragraph; also dropped stale "step (ii)" reference

## sections/2-background.tex

- [x] **#4** [L7] "two terms that that have" → "two terms with"
- [x] **#42** [L65] $Q$ wording inconsistency — rewrote paragraph to consistently frame $Q$ as the best-cost member of $P$'s equivalence class
- [x] **#5** [L65] "to $P$.After" → fixed as part of #42 rewrite
- [x] **#6** [L111] "i.e.the" → "i.e.\ the"
- [x] **#37** [L77] Changed `equation*` → `equation` so `\autoref{ex:formula}` resolves
- [x] **#8** [L172] "arbritrary" → "arbitrary-forking" (also added hyphen)
- [x] **#9** [L174-175] Fixed subject/verb agreement; tightened sentence
- [x] **#28** [L180] Standardized on `\textsc{ParlayLib}` everywhere
- [x] **#7** [L155] Dropped extra "in"
- [x] **#66** [L211] Skipping — related work is contextualized inline throughout the paper

## sections/3-algorithm.tex

- [x] **#43** [L8] Added `\cite{nieuwenhuis-oliveras-cc}`
- [x] **#10** [L22-23] Rewrote sentence; also replaced "operand" with "child"/"children" everywhere for consistency
- [x] **#11** [L36] "and merged" → "are merged"
- [x] **#31** Standardized on "union-find" (lowercase, hyphenated); kept title-case in subsection heading
- [x] **#44** [L103] Kept all as `\subsection`s; rewrote intro paragraph to flag that next subsections describe the building blocks
- [x] **#70** Renamed pseudocode functions to `\parentalgo` / `\filteralgo`, captions and subsection titles now use the macros
- [x] **#12** [L178] Dropped extra "that"
- [x] **#45** [L188] Dropped Level1 footnote; standardized on `\textsc{Congruent}`
- [x] **#13** Fixed both "maintaing" → "maintaining"
- [x] **#46** §4 deleted entirely; §3's "Implementation Details" stays as-is (former §4 content intentionally dropped)
- [x] **#47** Fixed: ParlayLib parallel bucketing is advantageous for *large* buckets, not the small ones in our workloads
- [x] **#15** Fixed "Heterogenous"/"hetergenous" → "heterogeneous"
- [x] **#14** Fixed "sotring" → "storing"

## sections/4-implementation.tex (deleted)

- [x] **#48** §4 deleted entirely
- [x] **#49** §4 deleted (the broken-ref fix had already been applied prior)
- [x] **#16** §4 deleted (no other "tantamout" in paper)
- [x] **#67** §4 deleted entirely

## sections/5-evaluation.tex

- [x] **#36** No longer in file
- [x] **#17** [L26] "an" → "a"
- [x] **#52** [L120] Fixed: now `\autoref{fig:random}`, "shows the speedup"
- [x] **#35** [L120] Resolved (now references the parent figure label)
- [x] **#53** [L120-126] Fixed run-on sentence, "32-XL" → `\texttt{32xl}`, dropped misleading "only"
- [x] **#50** Filled in equality-generation procedure (x-y pairs, $n_{\text{merges}}$ random equalities)
- [x] **#51** `\as{}` note already removed
- [x] **#29, #54** Standardized on `n_{\text{compound}}`; clarified that total leaves = 2 × $n_{\text{leaves}}$; reconciled prose/caption on equality pairs (x-y); fixed "appliction" typo
- [x] **#26** Fixed all three "parallization"/"parallize" → "parallelization"/"parallelize"
- [x] **#37** [L176] `\autoref{ex:formula}` resolves now that equation is numbered
- [x] **#55** Tightened tie-in to example (now "generalizes the structure of"); construction is now self-contained
- [x] **#56** Added explicit three-layer construction (leaves, $f$-layer, $g$-tree) with parameters $k$ and $l$ — fully reproducible
- [x] **#33** Standardized on $k$ throughout construction and analysis
- [x] **#57** Capitalized "Equivalence"; renamed label to `sec:eval:circuit` (matches existing reference)
- [x] **#27** Standardized on "subcircuits"
- [x] **#18** Removed comma splice; added "on them"
- [x] **#58** Renamed AIGER → "And-Inverter Graph"; removed undefined "ABC-optimized"
- [ ] **#59** [L296-297] Lost the "before deduplication" detail (skipped per user)
- [ ] **#60** [L298-299] Lost justification for picking 12 instances (skipped per user)
- [x] **#19** Removed stray comma
- [x] **#39** Added missing terminal periods on two captions
- [x] **#38** Standardized on `fig:*:parents` (plural)
- [x] **#61** All active em-dashes already converted to `---` during prior edits; remaining `—` are in commented-out blocks
- [x] **#34** Fixed "MST-LIB" → "SMT-LIB" (also fixed "into and" → "into an")

## sections/6-discussion.tex

- [x] **#62** Filled in $27\times$ self-speedup for \filteralgo on `32xl`
- [ ] **#63** [L56] Backtracking section empty — deferred (Zak to fill in)
- [x] **#26** [L33] Fixed (see §5 entry)
- [x] **#20** [L36] "the" → "they"
- [x] **#21** [L37] "wer" → "were"
- [x] **#22** [L41] Fixed (see §5 entry)
- [x] **#23** Fixed garbled "where we you have add" → "where you have to add"
- [x] **#24** Removed "done by" redundancy
- [x] **#30** [L73] "E-node" — paper uses "e-node" elsewhere (now: drop e-prefix entirely)
- [x] **#64** Merged duplicate Incremental Update paragraphs into one coherent paragraph
- [x] **#25** Fixed (resolved as part of #64 merge)
- [x] **#68** Added `7-conclusion.tex`; wired into `paper.tex`

## Cross-cutting

- [x] **#28** "Parlay-Lib" / "parlaylib" / "ParlayLib" — standardized on `\textsc{ParlayLib}`
- [x] **#32** All active hashcons references already gone; remaining are in commented-out related work
- [x] **#69** All figure label references resolve cleanly in latest build
- [x] **NEW** Dropped "e-node"/"e-class" terminology paper-wide (replaced with "term" / "equivalence class"); kept "e-graph" reference in §2.1 per your request

---

## Second-pass issues (read-through round 2)

### Round 2 — paper.tex / abstract

- [x] **#71** [paper.tex:113] Fixed verb agreement; reframed loop description to fit both algorithms; added one sentence noting they differ in re-examination strategy
- [x] **#72** Keeping as-is; backtracking will be filled in later (tracked in #63)
- [x] **#73** Removed commented abstract drafts in paper.tex; also removed the older mirrored block at top of 1-intro.tex

### Round 2 — sections/1-intro.tex

- [x] **#74** Restructured: split the chain of inferences into two clauses ("$a=c$ follows by transitivity, and then $f(a)=f(c)$ follows by congruence, contradicting the disequality"); dropped the undefined "parent terms" scare-quotes
- [x] **#75** Intro now cites `\cite{uf}` (Alistarh et al.) to match §3.3
- [x] **#76** Joined orphan sentence to the preceding paragraph
- [x] **#77** Resolved by user dropping the "$27\times$" parenthetical from the contribution
- [x] **#78** Resolved by same removal; no inconsistent framing remains in intro
- [x] **#79** Keeping bare (current state) — all four tool names (egg/egglog/Z3/cvc5) use the same plain style, which is internally consistent

### Round 2 — sections/2-background.tex

- [x] **#80** Standardized on "data structure" (two words); fixed both §2 occurrences. §4 occurrence will be handled with #121
- [x] **#81** Named the definition `[Terms]`
- [x] **#82** Added "with" between "$f \in F$" and "$\text{arity}(f) = k$"; added comma after the form
- [x] **#83** Kept $f(x)$ notation per user; switched articles to indefinite ("a child"/"a parent") and added "compound term" framing
- [x] **#84** Reworded to "consider the following formula given to an SMT solver"
- [x] **#85** Re-read; the definition introduces "$k$-step congruent" as shorthand for "congruent after $k$ rounds", then uses the shorthand. Fine as-is
- [x] **#86** Introduced symbol `D` for congruence depth in the prior definition; reused it as the summation upper bound in the width definition. Tightened wording.
- [x] **#87** Renamed `sec:alg` → `sec:algorithm` in commented blocks
- [x] **#88** Capitalized "Algorithms"; also fixed "Congruence closure" → "Congruence Closure" in §2.1 for the same reason
- [x] **#89** Pluralized all four "our algorithm" references in §2 (L116, L136, L178, L200)
- [x] **#90** Named the definition `[P-completeness]`
- [x] **#91** Fixed split infinitive: "to not be" → "not to be"
- [x] **#92** False alarm — acronym IS expanded on first use ("Multi-Process Random-Access Machine (MP-RAM)")
- [x] **#93** Lifted the parenthetical into a comma-bracketed clause; "manifests" replaces "shows up"
- [x] **#94** Standardized to `\autoref` in §2 (two occurrences); §4's `Figure~\ref` will be handled as #130

### Round 2 — sections/3-algorithm.tex

- [x] **#95** Reworded to drop "a-priori"; also corrected the inaccurate claim that the union-find "maintains" the input equalities (it has to add them via Union)
- [x] **#96** Updated pseudocode to "Insert all non-leaf terms" so it matches the prose
- [x] **#97** Resolved: prose was already plural; the singular heading was the issue (fixed by #98)
- [x] **#98** Pluralized heading: "Other Sequential Algorithm" → "Other Sequential Algorithms"
- [x] **#99** "then" → "than"
- [x] **#100** Expanded §3.4 with the semisort signature (no total order across hashes) and complexity ($O(n)$ work, $O(\log n)$ span on average)
- [x] **#101** Fixed "Intially" → "Initially"
- [x] **#102** Merged the duplicate `\autoref{alg:bsp}` references into one
- [x] **#103** Fixed subject/verb: "each ... is congruent" (also dropped "pointwise" per user)
- [x] **#104** Added the same initial-union ParFor block to `\filteralgo` so both algorithms match
- [x] **#105** Defined both `GroupBy` (equivalence-relation form) and `GroupByKey` (key-value form) in §3.4
- [x] **#106** Reworded: "achieves the same effect without keeping these parent lists"
- [ ] **#107** [L264] `\mathit{dirty} \gets [\textbf{false} \mid 0 \leq i < n]` — what is $n$? Never defined in the pseudocode scope
- [ ] **#108** [L292] "for terms of arities **1,2,3 and 4**" — missing space after comma
- [x] **#109** Replaced "fairly high overhead" with the concrete reason: "expensive due to frequent allocations"

### Round 2 — sections/4-evaluation.tex

- [ ] **#110** [L4, L8, L11, L13] RQs say "parallel congruence closure **algorithm**" (singular) — paper has two; should be plural throughout
- [ ] **#111** [L23] "a set of benchmarks on a set of circuit equivalence benchmarks" — "a set of ... on a set of" reads awkwardly; simplify
- [ ] **#112** [L26] "Amazon Web **Service**" → "Amazon Web Services" (the product is plural)
- [ ] **#113** [L28] "Ubuntu 26.04 LTS" — 26.04 is not a real Ubuntu version (LTS goes 22.04, 24.04, 26.04 hypothetically). Confirm the actual OS version
- [ ] **#114** [L29] "compiled using g++15.2.0" — odd formatting; standard is "GCC 15.2" or "g++ 15.2.0"
- [ ] **#115** [L37-52] Random-benchmarks figure references aren't tied to the prose discussion at L123-129 — could add `\autoref{fig:random:parents}` and `\autoref{fig:random:filter}` to make the discussion concrete
- [ ] **#116** [L85] `\begin{table}[t]` — uses `[t]` while other floats use `[!tb]`; minor consistency thing
- [ ] **#117** [L106] Table caption starts with "Synthetic workload parameters." but this is the *random* workload table, not synthetic. Mismatch
- [ ] **#118** [L107] "Each workload is a random binary-tree DAG" — "binary tree" suggests arity 2 but the prose says "function symbols, each of arity 2" — OK consistent. But "binary-tree DAG" is unusual phrasing (a DAG is not a tree); consider "DAG with binary internal nodes"
- [ ] **#119** [L131-135] "\filteralgo starts from a much better baseline" — what baseline? Reads ambiguously (sequential? T=1?). Specify
- [ ] **#120** [L138-141] "we can achieve **superlinear speedups**" — claim made but no specific numbers given; back with a figure reference or specific data point
- [ ] **#121** [L139] "the \filteralgo has less datastructures" — drop "the" (article shouldn't precede `\filteralgo` since the macro starts with "Filter"); also "datastructures" → "data structures"; also "less" → "fewer" (countable)
- [ ] **#122** [L212] "cube width $k$" — but the synthetic section never calls $k$ "cube width" — it's just the width. Either define "cube width" or use "width $k$"
- [ ] **#123** [L226] "Similar to the random workloads, our **algorithm achieves**" — singular but should be "our algorithms achieve"
- [ ] **#124** [L231-234] "\filteralgo (and respectively \parentalgo) achieves" — change "respectively" parenthetical style to match line 126's "resp." which is cleaner
- [ ] **#125** [L234] "and only $26.4\times$ ($17.0\times$) on 192 threads" — "only" is misleading (this is a *positive* result, not a let-down); drop "only"
- [ ] **#126** [L286-292] "In this section, we evaluate on a set of benchmarks checking the equivalence of two circuits." — sentence repeats "benchmarks" from the section opener at L22-23; tighten
- [ ] **#127** [L294] "given to a SAT solver" → "given to **an** SAT solver" (acronym, "ess-ay-tee" starts with vowel sound)
- [ ] **#128** [L308-314] Methodology paragraph for circuit benchmarks: "we instrument Kissat's gate extractor to dump every candidate gate (AND/XOR/ITE). We evaluate our congruence closure implementations on these gates." Two short sentences could be merged
- [ ] **#129** [L341-348] "the single-core baseline of \filteralgo varies dramatically across files: on the 22 files we measured" — but the prose at L313 said "twelve hardest instances". Mismatch: 12 vs 22 files
- [ ] **#130** [L350] `Figure~\ref{fig:gates_vs_min_dirty_fraction}` — uses `\ref` not `\autoref` like the rest of the paper
- [ ] **#131** [L360] "wastes work proportional to the entire term set" — "term set" undefined as a concept; previous text uses "live e-nodes / terms" (we renamed). Just use "live terms"

### Round 2 — sections/5-discussion.tex

- [ ] **#132** [L9] RQ1 answer: "Our parallel congruence closure **algorithm achieves**" — singular; should be plural
- [ ] **#133** [L13] "begin to plateau" — singular subject "We" wants "begin"; OK. But this sentence is now somewhat clumsy; the parenthetical "(\filteralgo on \texttt{32xl} ... baseline)" is a lot to read mid-sentence
- [ ] **#134** [L17] RQ2: "More rounds of congruence closure **does** not have" — subject "more rounds" is plural; "do not have"
- [ ] **#135** [L18] RQ3: "Our **algorithm provides**" — singular; should be plural
- [ ] **#136** [L56-57] Backtracking section still has `\as{}` TODO — deferred per earlier decision (already tracked as #63)
- [ ] **#137** [L59] "produce \emph{proofs}(i.e." — missing space between `\emph{proofs}` and `(i.e.`
- [ ] **#138** [L62-63] "it is necessary to justify correctness and it is used to produce conflict clauses in SMT solvers" — two clauses using "it" with different referents; restructure

### Round 2 — sections/6-conclusion.tex

- [ ] **#139** [L5] "two parallel congruence closure algorithms built on a bulk-synchronous design over a lock-free concurrent union-find" — "built ... over" reads oddly; "built on a bulk-synchronous design **that operates over** a lock-free concurrent union-find" reads better

### Round 2 — sections/7-acks.tex

- [ ] **#140** [L4] "We did not use generative AI for writing beyond standard grammar, formatting, and editing." — this contradicts the work we did: I did substantive structural/wording rewrites. If the disclosure should be accurate, mention that AI was used for proofreading/editorial revisions but not for generating new ideas/results
