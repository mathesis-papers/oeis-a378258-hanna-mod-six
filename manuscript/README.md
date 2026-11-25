# Proof of the modulo-six and parity conjectures in OEIS A378258, Comments

The note proves both conjectures in Paul D. Hanna's [OEIS A378258, Comments](https://oeis.org/A378258), posed on 3 December 2024. Odd coefficients occur exactly at powers of two. Every even-indexed coefficient is divisible by three, with residue three modulo six at powers of two and zero otherwise. The normalized rational solution exists, is unique and has integer coefficients.

## Companion results

Write `C=x+C^2`, `J=A-A^2` and `c_n=[x^n]C`. Every coefficient of `B` or `J` beyond degree one is even. The odd coefficients of `A^2` occur exactly at indices 2, 4, 8, ... . For every `n>=2`, the coefficient of `B composed with B` is `-4c_n`, while that of `J composed with J` is `4*5^(n-2)c_n`. Both have dyadic valuation `s_2(n)+1`, where `s_2` counts binary ones.

The proof also treats every integer `t`, with `q=1+4t` replacing 5. If `M=abs(2t+1)`, then every even-indexed coefficient is `M` modulo `2M` at powers of two and zero otherwise. The case `t=0` gives the Catalan series.

## Files and build

- `note.tex`: complete proofs, a source-coverage table and checked scientific references.
- `note.pdf`: typeset note, supplied separately from the source archive.
- `verify.py`: two exact coefficient constructions and finite checks.
- `verification.json`: deterministic checker output.
- `coverage.json`: exact claim, source and declaration mapping.
- `metadata.json`: stable identity, revision, problem identifiers, creators and license.

Build with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, run `pdflatex note.tex` twice. The bibliography is embedded; no BibTeX database is required. The checker uses Python 3.10 or later and its standard library:

```sh
python3 verify.py > verification.json
```

Its exact arithmetic covers degree 80 for A378258, all six identities, every displayed sequence and companion-series coefficient, both compositional-square valuations, and the first negative coefficient at index 58. For nine integer parameters `t=-3,...,5`, both constructions and all generalized identities agree through degree 24, including the composite modulus `M=9`. These finite checks accompany the all-degree written proofs.

## Formal statements and attribution

At scientific revision `01b573fd9b691a4be3a8b0ecbb41b3311eda19b5`, [`HannaA378258ModSix.result`](https://github.com/the-omega-institute/trureturing/blob/01b573fd9b691a4be3a8b0ecbb41b3311eda19b5/D5/S1/Recurrence/Invariants/HannaA378258ModSix.lean) states existence and the modulo-six exclusion for every normalized rational solution at every degree greater than one. [`HannaA378258SquareRootParity.result`](https://github.com/the-omega-institute/trureturing/blob/01b573fd9b691a4be3a8b0ecbb41b3311eda19b5/D5/S1/Recurrence/Invariants/HannaA378258SquareRootParity.lean) states existence, integrality and the power-of-two parity criterion at every positive degree. Both are in namespace `D5.S1.Recurrence.Invariants` followed by the filename stem. `IsGF` is exactly the normalized source system. The additional congruences, companion results and parameter family have written proofs; the two exported statements concern `q=5`.

An earlier parity argument appears in [hilbert-clavius, 25 October 2026, item 5](https://www.openwitness.net/p/10125). The Catalan valuation is classical: [Deutsch and Sagan, arXiv:math/0407326v1, Theorem 2.1](https://arxiv.org/abs/math/0407326v1).

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0 (Creative Commons Attribution 4.0 International).
