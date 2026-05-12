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
- [ ] **#55** [L170-179] Synthetic benchmark says "based on the example" but uses different variable conventions
- [ ] **#56** [L192-194] Depth parameter $l$ introduced with no construction — reader cannot reproduce
- [ ] **#33** [L187 vs L197] Width parameter inconsistently called $n$ then $k$
- [ ] **#57** [L239] Section labeled `sec:eval:hardware` but titled "Circuit equivalence Benchmarks"; "equivalence" should be capitalized
- [ ] **#27** [L253] "sub-circuits" vs "subcircuits"
- [ ] **#18** [L284-285] Sentence fragment / comma splice
- [ ] **#58** [L289-291] AIGER is a file format, not a synonym for AIG
- [ ] **#59** [L296-297] Lost the "before deduplication" detail
- [ ] **#60** [L298-299] Lost justification for picking 12 instances
- [ ] **#19** [L328] "on most workloads,." — stray comma
- [ ] **#39** [L313] Caption missing terminal period
- [ ] **#38** [L308 vs L42] `fig:circuit:parent` (singular) vs `fig:random:parents` (plural)
- [ ] **#61** [L344-345] Em-dash style inconsistent with rest of paper
- [ ] **#34** [L379] "MST-LIB" → "SMT-LIB" (commented text)

## sections/6-discussion.tex

- [ ] **#62** [L12] `\as{give a number here}` TODO
- [ ] **#63** [L56] Backtracking section is empty
- [x] **#26** [L33] Fixed (see §5 entry)
- [ ] **#20** [L36] "which the would add" → "they"
- [ ] **#21** [L37] "wer unioning" → "were"
- [x] **#22** [L41] Fixed (see §5 entry)
- [ ] **#23** [L42] "where we you have add the merges" → "you have to add"
- [ ] **#24** [L67] "as done by the Z3 SMT solver does" — drop one redundancy
- [x] **#30** [L73] "E-node" — paper uses "e-node" elsewhere (now: drop e-prefix entirely)
- [ ] **#64** [L69-76] "Incremental Update" paragraph appears twice
- [ ] **#25** [L73] Unfinished sentence
- [ ] **#68** No Conclusion section

## Cross-cutting

- [x] **#28** "Parlay-Lib" / "parlaylib" / "ParlayLib" — standardized on `\textsc{ParlayLib}`
- [ ] **#32** "hashcons" / "hash-cons" / "hash cons" — pick one
- [ ] **#69** Stale figure labels referenced from prose
- [ ] **NEW** Drop e-graph / e-node / e-class terminology — use "data structure" / "term" or "node" / "equivalence class" or "congruence class"
