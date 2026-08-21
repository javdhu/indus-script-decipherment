# Source manifest

Snapshot used for the analysis (2026-08-09). `scripts/fetch_inputs.sh` fetches
the three Git sources at these commits; the PLOS data is committed.

| Source | Local path | Revision / checksum | Use |
|---|---|---|---|
| Todd Olsen Indus corpus, [toddcolsen/indus_script](https://github.com/toddcolsen/indus_script) | `vendor/toddcolsen-indus-script` (fetched) | `52a6fdb5fa235bca1b78ef8856a4ba54714d37fb` | Mahadevan-numbered IDF-80/M77-derived lines and metadata. No declared licence: fetched, never committed. |
| Glossa-Lab, [BitConcepts/glossa-lab](https://github.com/BitConcepts/glossa-lab) | `vendor/glossa-lab` (fetched) | `40812fc54470d5508b47af5fabcea7ccf044036c` | Adversarial audit of 2026 anchor table |
| mayig CISI digitization, [mayig/indus-valley-script-corpus](https://github.com/mayig/indus-valley-script-corpus) | `vendor/mayig-indus-valley-script-corpus` (fetched) | `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb` | Independent Parpola corpus, feature dictionary, and orientation control |
| PLOS Wells supporting data, S2 of Ashraf & Sinha 2018 ([doi:10.1371/journal.pone.0190735.s010](https://doi.org/10.1371/journal.pone.0190735.s010)) | `vendor/plos-wells-s2-data/` (committed, CC BY 4.0) | S2 ZIP SHA-256 `7b5e7d5243ef34fe3a5990be879c02f24664bf8b07fe427b2942e6611005f688`; extracted `25_Undeciphered(Indus).csv` SHA-256 `140a61e57dfaccd15867d9a00141f180a38080141b0ad18bb4262c782024f186`, `Keylist_Udeciphered_Indus.pdf` SHA-256 `4fd9e70aabf035b3da018fa3d3abfbd074718254f3004624dad976fd7336af61` | CC BY Wells-numbered 1,837-line sequence corpus and sign key; independent positional replication |
| Ross, *Reading the Indus Valley Script* (preprint, March 2026) | not included (no licence) | MD5 of the copy audited `6d6348ebdba94f63172bffd6b88935ad` | Adversarial audit of a claimed complete reading (`research/candidate_model_audit.md`) |

External scholarly sources and direct URLs are listed in
`research/primary_sources.md`.
