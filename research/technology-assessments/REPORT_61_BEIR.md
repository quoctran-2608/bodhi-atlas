# REPORT 61 — BEIR: thẩm định độc lập công cụ QA truy xuất cho BodhiAtlas

**Ngày:** 25/11/2026 (Asia/Ho_Chi_Minh) · **Đối tượng:** [beir-cellar/beir](https://github.com/beir-cellar/beir) · **Phạm vi:** dev/QA benchmark Information Retrieval, không phải search engine production. **Trạng thái:** audit tĩnh có ghim commit, POC cô lập có oracle và log; chưa chạy BEIR/backend native. Không sửa repository, không tải corpus/model. Báo cáo này là quyết định đầu tư QA, không nghiệm thu V1.

## 1. Executive Decision

**Khuyến nghị chính: `DEFER` dependency BEIR trong V1; chọn D — harness nhỏ Python/SQLite cho Track A, áp dụng ngay quy ước dữ liệu/đánh giá của E (methodology).** Khi có ranked discovery thực sự cần so sánh, thử C (backend độc lập nhẹ) và B (BEIR evaluator-only) trên cùng Track B; chỉ chọn một nếu qua parity và giảm chi phí bảo trì. Không fork BEIR; không dùng full suite A mặc định. Confidence **HIGH** về phân biệt hợp đồng EXACT/qrels và logic evaluator tại SHA; **MED** về ưu tiên D; **LOW** về tổng chi phí thực tế trước POC native.

BEIR có ích thật: nhận corpus/query/qrels tùy chọn, dùng metric IR phổ biến, có abstraction cho retriever/reranker và export run. Một evaluator có sẵn có thể tiết kiệm công viết lại các metric phức tạp khi sản phẩm cần ranked retrieval. Không cần bác bỏ evaluator chỉ vì dataset khác domain. Nhưng **một benchmark tài liệu không chứng nhận mọi lần xuất hiện trong một tài liệu, càng không chứng nhận câu trích từ đúng file/ấn bản/trang**. Bộ gold Track A vẫn bắt buộc dù chọn B hoặc C.

**Ba blocker trước khi dùng BEIR làm chuẩn QA:**

1. `[CODE]` `evaluate()` chỉ chia theo `len(scores)` từ backend, không kiểm đủ query universe; custom MRR chia theo qrels. BM25 và runfile có đường làm mất query rỗng. Issue #222 báo cùng vấn đề; chưa tái hiện với backend native. Phải báo đủ zero-hit, missing, error và no-positive; không im lặng bỏ mẫu.
2. `[CODE]` loader dùng dict theo `_id`, giữ text/title nhưng không giữ source map; mặc định loại query/doc cùng ID **và mutate results**. Một corpus ID không thể biểu diễn đủ identity/offset/coverage; cần preflight và sidecar BodhiAtlas.
3. `[CODE]` full package yêu cầu `sentence-transformers`, `datasets`, `pytrec-eval-terrier` dù evaluator tĩnh không dùng model; sandbox không có BEIR/pytrec_eval/ir_measures và không clone được qua DNS. Quyền dữ liệu/model phải kiểm riêng. Chưa đo chi phí native, chưa có gold Phật học do reviewer duyệt.

**Ba POC quyết định:** (i) TC01/02/03/05/15 — cài offline pinned B/C, parity với oracle và kiểm mẫu số; (ii) TC06/07/09/10/13 — adapter read-only trên BCR/SQLite, all-offset, coverage, wrong-edition, false VERIFIED; (iii) TC08/11/12/14 — bộ gold đa ngôn ngữ frozen, so candidate/rerank và reproducibility. Đừng bắt đầu POC iii bằng tải toàn suite.

| Mức | Điều có thể nói |
|---|---|
| Demo nhanh nhất đã làm | Python stdlib + SQLite fixture: metric, offset, adapter cô lập chạy thành công. |
| Đủ tiêu chuẩn QA | Chưa: cần chạy TC native, source resolver độc lập, corpus thật hợp quyền. |
| Production | Không đề xuất service BEIR. Không có chứng nhận G1–G6, latency, recall domain hay TCO. |

## 2. Sources & Evidence Ledger

### 2.1 Snapshot và truy cập

| Nguồn | Snapshot / trạng thái |
|---|---|
| BEIR GitHub | Public, không archived, default `main`; latest commit từ GitHub connector: [`ef83d29307061c65d04b035b4f4e7c18bd8374af`](https://github.com/beir-cellar/beir/commit/ef83d29307061c65d04b035b4f4e7c18bd8374af), 16/10/2025 06:38:02 UTC, merge #203 sửa import API. Đây là snapshot được truy cập, không phải wheel. |
| Tag | `v2.2.0` resolve qua GitHub commit API thành [`6ef8c9097ebfb203ad360bd64e0cfb93e64f4a44`](https://github.com/beir-cellar/beir/commit/6ef8c9097ebfb203ad360bd64e0cfb93e64f4a44). HEAD pyproject cũng ghi 2.2.0. Đã đọc lại evaluator L68–122 ở tag: cùng logic chính. Không xác minh mọi diff, trang release GitHub bị chặn; trạng thái formal stable release GitHub UNKNOWN. |
| PyPI | [beir 2.2.0](https://pypi.org/project/beir/2.2.0/) là bản mới nhất quan sát từ trang project, upload 04/06/2025, Python >=3.9, classifier Beta; wheel 77.4 kB, sdist 64.0 kB theo metadata, không tính dependencies. Chưa tải hoặc kiểm hash thực tế. Wheel SHA-256 công bố `46fe4d0a3a6e719090eabc0d1f8aa0c51c6c1379639e6381de5b49e445ab36d1`; sdist `3bef26652cf9fa209190c3b3b9e9ff684343d66cf39ec637998a6a57e523f786`. Không có provenance attestation theo PyPI. |
| BodhiAtlas | Public, không archived, `main` [`c5dfe50613dfd492407bf1db1061c1cfc9d30e8e`](https://github.com/quoctran-2608/bodhi-atlas/commit/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e), 25/11/2026 11:26:47 UTC. 5 file nền lấy qua connector; trích các đoạn liên quan. |
| Runtime | Git CLI tới cả BEIR/BodhiAtlas lỗi DNS; GitHub connector đọc thành công. Không có checkout, package BEIR hoặc backend native. Không bypass bằng tải mạng không được duyệt. |

**Quy ước:** `[DOC]` văn bản/metadata đã đọc; `[CODE]` nội dung mã đã lấy; `[TESTED]` upstream/integration thật đã chạy (0 ca); `[TESTED-ISOLATED]` fixture Python/SQL tự viết; `[ISSUE]` bên khác báo, không tự tái hiện native; `[PLAN]` chưa chạy; `[INFERRED]` suy luận có tiền đề; `[UNKNOWN]` chưa xác minh; `[CONFLICT]` khác biệt contract/version. NATIVE không đồng nghĩa PASS. Các đường dẫn dưới đây dùng commit đầy đủ; không dùng HEAD động để gán bằng chứng.

### 2.2 Ledger

| ID | Loại | Claim / bằng chứng có thể truy lại | Giới hạn |
|---|---|---|---|
| E01 | DOC | [PRD V1.4 L105–121, L213–254](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/PRD.md#L105-L121), tìm nguyên văn, match labels và provenance; [L227–254](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/PRD.md#L227-L254) | yêu cầu, không phải implementation |
| E02 | DOC | [V1 Foundation L51–109](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/V1_CORE_FOUNDATION.md#L51-L109), [L130–160](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/V1_CORE_FOUNDATION.md#L130-L160) | nguồn, chỉ mục dẫn xuất, evidence |
| E03 | DOC | [Academic Risks G1–G6 L154–165](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/ACADEMIC_RISKS_AND_VERIFICATION.md#L154-L165), [T01–T16 L169–190](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/ACADEMIC_RISKS_AND_VERIFICATION.md#L169-L190) | không thể thay reviewer bằng IR |
| E04 | CODE | [pyproject L1–13, L37–62](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/pyproject.toml#L37-L62): 3 direct deps không pin, extras TF/ES/PEFT/LLM2Vec/FAISS/dev | số transitive và cài thực UNKNOWN |
| E05 | CODE/DOC | [LICENSE](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/LICENSE) Apache-2.0; [README disclaimer L389–397](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/README.md#L389-L397) quyền dataset riêng | không cấp quyền corpus |
| E06 | CODE | [data_loader.py L13–91](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/datasets/data_loader.py#L13-L91) load split, filter query bằng qrels, cache mutable | chưa chạy loader |
| E07 | CODE | [data_loader.py L104–134](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/datasets/data_loader.py#L104-L134) UTF-8, dict overwrite, TSV bỏ header | missing/orphan/duplicates không validate ở đây |
| E08 | CODE | [evaluation.py L14–31](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/evaluation.py#L14-L31) top_k=max K và `retrieve` delegate | evaluate tĩnh khác retrieval |
| E09 | CODE | [evaluation.py L68–85](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/evaluation.py#L68-L85) ignore_identical_ids mặc định true, pop in-place | cần deepcopy, namespace |
| E10 | CODE | [evaluation.py L91–122](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/evaluation.py#L91-L122) metric strings, scores, len(scores), round 5 decimals | backend tie/undefined chưa chạy |
| E11 | CODE | [tag evaluator L68–122](https://github.com/beir-cellar/beir/blob/6ef8c9097ebfb203ad360bd64e0cfb93e64f4a44/beir/retrieval/evaluation.py#L68-L122) cùng logic E09–10 | không xác nhận wheel bytes |
| E12 | CODE | [custom_metrics.py L6–34](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/custom_metrics.py#L6-L34) MRR rel>0, tie insertion order, chia len(qrels) | khác mẫu số |
| E13 | CODE | [custom_metrics.py L37–93](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/custom_metrics.py#L37-L93) R_cap chia min(R,k), hole dùng tập doc judged toàn bộ | zero division nếu R=0; hole không phải per-query Judged |
| E14 | CODE | [custom_metrics.py L96–126](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/custom_metrics.py#L96-L126) accuracy hit-any, len(qrels) | không phải citation accuracy |
| E15 | CODE | [dense exact L40–126](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/search/dense/exact_search.py#L40-L126) embedding score + top-k heap, skip self IDs | không literal; single-query hazard L102 |
| E16 | CODE | [dense exact L128–251](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/search/dense/exact_search.py#L128-L251) reuse filenames, FAISS file path | stale cache và metric parity chưa chạy |
| E17 | CODE | [FAISS L21–45](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/search/dense/faiss_index.py#L21-L45) IndexFlatIP, batch search | khác cosine nếu vector không chuẩn hóa |
| E18 | CODE | [dense util L77–97](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/search/dense/util.py#L77-L97) pickle load/save | không đọc pickle không tin cậy |
| E19 | CODE | [BM25 L49–87](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/search/lexical/bm25_search.py#L49-L87) ES delete/create, zero-hit thiếu key, skip self | không kết nối ES thật |
| E20 | CODE | [util L58–103](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/util.py#L58-L103) HTTP stream, extractall, cache theo path | không thấy checksum/timeout/quota ở đường này |
| E21 | CODE | [util L106–155](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/util.py#L106-L155) JSONL/TSV, runfile thiếu hàng zero-hit | round-trip không bảo toàn query universe |
| E22 | CODE | [SentenceBERT L16–54, L89–113](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/retrieval/models/sentence_bert.py#L16-L54) model load và max length; [Rerank L15–49](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/beir/reranking/rerank.py#L15-L49) chỉ rescore candidate | không có recall guarantee |
| E23 | DOC | [README L340–358](https://github.com/beir-cellar/beir/blob/ef83d29307061c65d04b035b4f4e7c18bd8374af/README.md#L340-L358), dataset URLs/splits/checksum | chưa tải hoặc kiểm quyền từng bộ |
| E24 | ISSUE | [BEIR #222, 25/09/2026](https://github.com/beir-cellar/beir/issues/222), thiếu key → giảm denominator, báo tái hiện bằng stand-in | bên khác báo; không phải runtime của báo cáo này |
| E25 | DOC | [Thakur et al. 2021, abstract NeurIPS](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html), 18 dataset, 10 hệ thống theo nghiên cứu gốc; [arXiv 2104.08663](https://arxiv.org/abs/2104.08663) | đọc abstract/metadata, chưa đọc toàn PDF; không ngoại suy |
| E26 | DOC | [ir_measures measures](https://ir-measur.es/en/latest/measures.html), [getting-started](https://github.com/terrierteam/ir_measures/blob/main/docs/getting-started.rst), Judged, parameterization | docs động, backend/version chưa ghim, chưa parity |
| E27 | CODE | [BCR retrieval.py L268–347](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/retrieval.py#L268-L347) FTS LIMIT, CJK ngắn có cảnh báo | đọc lại đúng SHA P03, không phải HEAD mới |
| E28 | CODE | [BCR evidence_gate L223–342](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/verification.py#L223-L342) host-controlled independent source reader, compare identity/ranges | chưa test resolver; không thay SHA256 file sách |
| E29 | TESTED-ISOLATED | §9/§13: hand oracle 8 queries, 12 records, qrels graded, metric matches; dropping missing raises macro; same ID, tie examples | không native backend; synthetic policy riêng |
| E30 | TESTED-ISOLATED | §9/§13: SQLite read-only export logic, 8 occurrences; top-1 giữ 5, overlap/Unicode | fixture in-memory, không production source map |
| E31 | UNKNOWN | Native package/trec_eval, real gold, resource/TCO, source rights, tests tree | phải chốt trước nâng quyết định |
| E32 | DOC | [Research README L316–337](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/README.md#L316-L337), [template](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_TEMPLATE.md) | quy tắc synthesis, không làm bằng chứng code |

### 2.3 Đối chứng BodhiAtlas đã mở tại SHA c5dfe506…

Đã yêu cầu nội dung L1–65 của từng báo cáo dưới đây (tập trung executive/snapshot, không tuyên bố đã đọc toàn văn các báo cáo dài). Đối chứng chỉ giúp chọn phép thử; không sao chép kết luận hoặc kết quả đo cũ.

| Báo cáo | Manh mối và cách kiểm |
|---|---|
| [P20](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_20_SQLITE_FTS5_TRIGRAM.md#L1-L65) | FTS candidate ≠ exhaustive offsets; TC06 tự kiểm với SQLite/raw scan. |
| [P03](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_03_BUDDHISMDOCUMENTS_FOR_AI.md#L1-L65) và [BCR Evidence Engine](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_BCR_EVIDENCE_ENGINE.md#L1-L65) | có retriever/gate A, đọc lại E27–28; không cần đổi schema authoritative để thử xuất ranked run. |
| [P39-R2](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_39_BANG_HA_GIAC_NGO_INDEPENDENT_REVIEW.md#L1-L65) và [P57](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_57_BOOK_MEMEX.md#L1-L65) | wrong edition và false VERIFIED phải đếm riêng; chưa kiểm lại mã Bang-ha/book-memex trong P61. |
| [P01](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_01_RAGFLOW.md#L1-L65), [P02](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_02_QMD_TOBI_QMD.md#L1-L65), [P56](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_56_OPEN_NOTEBOOK.md#L1-L65) | các ứng viên ranked có thể so cùng qrels; không đánh giá lại engine hay áp dụng số benchmark của họ. |
| P59 | `REPORT_59_HAYSTACK.md` tại snapshot trả 404; không dự đoán kết quả P59. Không khẳng định file không tồn tại ở nhánh/path khác. |

## 3. Architecture & Data Flow

### 3.1 Hiện trạng BEIR (E06–E22)

```text
corpus.jsonl {_id,title,text,...}      queries.jsonl {_id,text,...}
                 |                         |
                 +---- GenericDataLoader --+-- qrels/{split}.tsv
                              |                  (query-id,corpus-id,score)
           corpus[id]={title,text}, queries[id]=text, qrels[qid][did]=int
                              |
                EvaluateRetrieval.retrieve -> BaseSearch.search
                     |                   |                    |
            lexical BM25 ES       dense similarity       custom adapter
                     +-------------------+--------------------+
                                 results[qid][did]=score
                                      | optional Rerank
                                      v
                          EvaluateRetrieval.evaluate (static)
                                      | pytrec_eval.RelevanceEvaluator
                                      v
                 per-query backend scores -> aggregate rounded dictionaries
                 custom metric path -> MRR, R_cap, Hole, Accuracy
                 util.save_runfile / save_results -> files
```

Đường metric không đòi gọi `retrieve`, không cần search server/model về mặt logic. Import `beir` đi qua logging handler (`tqdm`); evaluator import base/custom/pytrec_eval, không thấy import torch trực tiếp trong ba file này. Tuy nhiên installation metadata full package vẫn kéo ba dependency lớn. Không suy `pip install --no-deps` là deployment được hỗ trợ; phải lock và kiểm import sạch.

### 3.2 Đề xuất (không phải code đã triển khai)

```text
BodhiAtlas immutable raw store + catalog + versioned extraction/source map
                     |             |
             candidate engine      | read-only independent oracle/reopen
                /  |  \            |         |
           EXACT  ranked   error/coverage    Track A: occurrence + identity + G2
             |      |             |           |
             +------+-------------+-----------+--> QA report (no production write)
                    |
           versioned projection + query universe + frozen qrels B
                    |
             candidate stage / rerank stage separately
                    |
         optional evaluator backend (B or C) --> per-query B metrics + Judged
```

**Ownership:** catalog nắm raw bytes, SHA-256, Work/Expression/Edition/Witness/File, extraction revision, source map, permissions; retriever nắm derived index và result events; reviewer nắm gold, qrels, source/claim review. Evaluator chỉ đọc snapshot đã được phép, xuất artifacts tái tạo được. QA không cấp `VERIFIED`, không ghi đè catalog, không đồng bộ hai DB hai chiều, không dùng result ID làm canonical identity. Một process CLI/CI tách môi trường dev là đủ, không đề xuất service mới.

## 4. Fit–Gap C01–C15

Scope = năng lực QA IR, không đánh giá BEIR như hệ thống thư viện. Effort L/M/H/VH là phần công việc BodhiAtlas để đạt mục tiêu tương ứng, định tính chưa đo; N/A không bị trừ điểm. V1/V2/V3 chỉ giai đoạn đề xuất.

| ID | Yêu cầu | Trạng thái theo vai trò | Evidence | Còn thiếu / owner | Effort | Gate | Test / pha |
|---|---|---|---|---|---|---|---|
| C01 | Multi-format ingest | N/A | E06–07: JSONL/TSV benchmark | Parser/catalog của core | H | G1 | T01, TC09 V1 |
| C02 | OCR/layout/reading order | N/A | E06, E15 | OCR QA riêng CER/WER/layout và coverage | H | G1/G2 | T01, TC09 V1 |
| C03 | Canonical text & source map | EXTERNAL | E07, E21 | core cung cấp revision/locator, sidecar | H | G1/G2 | TC07/10/13 V1 |
| C04 | Work/Edition/Witness | EXTERNAL | E07 dict | authority cấp ID và provenance | H | G2/G3 | TC07/14 V1 |
| C05 | Exhaustive EXACT | EXTERNAL; MISSING nếu dùng BEIR thay oracle | E15/E29–30 | Track A độc lập, mọi offset | M/H | G1/G2 | TC06/07 V1 |
| C06 | Normalized multilingual | EXTENSION (đo ranked theo strata) | E07/E25 | core normalization version, reviewer | M | G2/G5 | TC08 V1–2 |
| C07 | Fuzzy retrieval | EXTENSION | E08/E10 | adapter candidates + gold typo; không tự sửa quote | M | G2 | TC11 V1–2 |
| C08 | Sense-aware lexicon | EXTERNAL | E07/E10 | typed judgment, sense/evidence reviewer | H | G5 | TC12/T05 V1–2 |
| C09 | Semantic/RAG | NATIVE cho IR metric, không RAG factuality | E08/15/22 | model pin, judgment, cost và verifier | M/H | G3 | TC11/12/16 V2–3 |
| C10 | Verified citation/reopen | EXTERNAL | E02/28/30 | source reader độc lập, hard gate negatives | H | G2 | TC10/T13 V1 |
| C11 | Wiki/notes/claims | N/A | E10 | G3/G6 review, không lấy qrels làm claim | H | G3/G6 | T08/T14/T15 V2–3 |
| C12 | APIs/MCP/export | NATIVE export run; EXTENSION adapter | E08/21 | validate IDs, manifest, không cần MCP riêng | L/M | G2 | TC13 V1 |
| C13 | Coverage/incremental | EXTENSION đo query coverage; EXTERNAL source coverage | E06/10/16/19 | events, failed pages, stale, pinned manifest | M | G1/G2 | TC03/09/14 V1 |
| C14 | Auth/privacy/license/backup | EXTERNAL | E05/20 | read scope, SBOM, consent, rights, backup | M/H | G4/G6 | TC01/16, T16 V1 |
| C15 | Operability/portability | CONFIG/UNKNOWN | E04/10/24 | offline wheelhouse, lock, parity/CI/rollback | M | mọi gate liên quan | TC01/15 V1–2 |

### G1–G6 (tách role ứng viên và nghiệm thu toàn hệ thống)

| Gate | BEIR trực tiếp | BodhiAtlas QA cần chứng minh | Trạng thái tổng thể tại P61 |
|---|---|---|---|
| G1 Ingest | N/A; chỉ loader benchmark | inventory trang/format/failed/coverage, T01/T10 | NOT DEMONSTRATED |
| G2 Citation | N/A; nếu lấy nDCG làm verifier là CODE GAP contract | exact offsets, independent reopen, wrong edition=0, false VERIFIED=0 | NOT DEMONSTRATED |
| G3 Claim | N/A | reviewer ngữ cảnh, phủ định/ngoại lệ, T06–09/T15 | NOT DEMONSTRATED |
| G4 External | N/A; code license không cấp quyền dữ liệu | quyền từng corpus, access scope, egress | NOT DEMONSTRATED |
| G5 Lexicon | N/A; relevance typed ngoài qrels | tách sense, dẫn chứng, reviewer | NOT DEMONSTRATED |
| G6 Publish | N/A | G2/G3 và consistency/rights; no automatic publish | NOT DEMONSTRATED |

Không có PASS production. Có CODE GAP cho *chính vai trò QA* ở missing-query/coverage (E10/E19/E21); không coi đó là FAIL native đã đo. Năng lực tính metric common có code; không đồng nghĩa mọi quy ước đúng với nhu cầu BodhiAtlas.

## 5. Deep Technical Findings

### 5.1 Loader, schema và split

`GenericDataLoader.load(split)` gán `qrels/<split>.tsv`, check file tồn tại và extension; đọc corpus UTF-8 JSONL, chỉ giữ title/text, query text, parse score int. `load_custom` tương tự. Không có validator schema đầy đủ trong đường đã đọc (E06–07).

- Duplicate corpus/query ID ghi đè bản trước; qrel cùng `(qid,did)` ghi đè score. Missing `_id` thành key None; qrels đọc ID string còn JSONL `_id` có thể số. Missing title/text có thể None, ảnh hưởng dense nối chuỗi. Đừng coerce sang string sau khi đã collapse. Orphan qrel doc không được đối chiếu corpus ở loader; qrel query không có text gây KeyError khi filter. Blank/malformed rows, header rỗng, file corpus rỗng (log ví dụ `[0]`), query rỗng có thể error; chưa chạy native.
- Query không có qrel bị lọc khỏi query universe, kể cả no-judgment. `self.qrels` không clear giữa các lần load; `self.queries` bị thu hẹp. Dùng instance mới mỗi split, tách manifest universe, assert split disjoint theo policy, không dựa vào cache mutable. Không mặc định tất cả split disjoint ở document/work level: corpus có thể shared theo protocol; leakage cần kiểm theo query, source group và model training.
- Preflight: nonempty string IDs, strict UTF-8/JSON object, no duplicate IDs/rows, known doc/query refs, int grade 0..3 theo rubric, explicit no-judgment event, finite scores, K>0, manifest checksum. Không log toàn văn private: loader log sample doc/query. Read-only approved export, giữ metadata bên ngoài.

### 5.2 Metric semantics và các phản ví dụ

E10 gọi pytrec_eval với `ndcg_cut`, `map_cut`, `recall`, `P` và comma-separated cutoffs. `pytrec-eval-terrier` là tên distribution tại HEAD, `pytrec_eval` là module import; không đánh đồng với wheel pytrec_eval khác. Kết quả chỉ trả aggregate 4 dict (round 5 số lẻ), không trả per-query/count. Log 4 chữ số. Với strict QA, gọi backend per-query hoặc wrapper trả counts; khóa convention và version. Backend thật chưa cài nên không khẳng định parity C implementation.

**Convention oracle cô lập:** `R=|{d: grade>0}|`; tại K, P=hit/K (không chia số hit trả về), recall=hit/R, AP@K=sum precision tại các vị trí relevant/min(R,K), MRR=1/rank hit đầu tiên; nDCG linear gain `DCG=sum grade_i/log2(i+1)`, IDCG sắp grade giảm dần. Các backend có thể dùng gain exp2 hoặc AP denominator khác; đây là convention đề xuất, đối chiếu trực tiếp native trước khi gọi là BEIR parity. Zero positive: nDCG/AP/Recall/MRR undefined (null), P=0; báo count và tách strata. Qid có judged positive mà missing/no-hit phải hiện thành zero (và trạng thái phân biệt). Timeout/no access/stale không phải successful no-hit; policy report run incomplete, không silently zero-fill rồi pass. Unjudged được tính gain 0 *cho metric theo judgment hiện có*, không thành negative học thuật; báo per-query Judged@K và retrieved judged fraction.

TC02 ví dụ q1 grade d1=3,d2=1,d4=0; ranking d2,d12(unjudged),d1; K=3: DCG=1+3/2=2.5; IDCG=3+1/log2(3); nDCG=0.68853; AP=(1+2/3)/2=0.83333; R=1; P=2/3; MRR=1. Backend actual null. Truy vấn q8 chỉ trả một trong hai relevant: P@3=1/3, Recall=1/2, AP=1/2. q4 có judged zero nhưng không positive: null convention riêng, không trộn macro tùy tiện.

**Denominator:** E10 chỉ cộng `scores.keys()`; nếu scores rỗng, chia 0. E12–14 chia `len(qrels)`. E24 mô tả backend trả giao tập run/qrels, empty dict vẫn có điểm zero; native build chưa chạy nên đây là `[ISSUE]` + `[INFERRED]` phù hợp code, không tuyên bố TESTED. E19 BM25 gán `self.results[qid]` trong loop hits; không hit không key. E21 `save_runfile` chỉ dòng hit, rank cột ghi 0, `load_runfile` chỉ tạo query có dòng; empty run biến mất. Một đường serialize có thể đổi điểm. Dùng explicit query events sidecar và wrapper preseed empty results **chỉ cho successful zero-hit/missing judged qid theo chính sách đánh giá**, cấm coi failed như successful; report both strict and backend conventional values nếu cần so paper.

**Identity:** mặc định `ignore_identical_ids=True` lọc cả qid/did bằng nhau (E09) và thay đổi input dict. Dùng separate namespace `q:` và `p:`, `ignore_identical_ids=False`, copy run; một bài self-retrieval legit không bị loại. DRES/ES tự loại self trước evaluator, flag không phục hồi được. `evaluate_custom` gọi sau evaluate có thể dùng run đã bị mutate. Kiểm trường hợp qrels rỗng, extra result qid: MRR/recall_cap/accuracy index qrels[qid] có thể KeyError; R_cap zero positives có thể chia 0, hole dùng judged docs toàn corpus, không phải judged per query. E13.

**Tie:** custom sorted score-only ổn định theo insertion order, backend trec tie chưa xác minh; nếu rank boundary có ties, lưu raw score và policy (score desc, ID asc hoặc rank đã cung cấp), báo best/worst sensitivity và check permutation. Không tùy tiện thêm epsilon làm đảo genuine scores. Không dùng rounded score cho quyết định close call. Runfile export top_k, ties có thể bị cắt khác policy. Repeated runs fixed seeds/thread/hardware nếu có model.

### 5.3 Dense “exact”, lexical, reranker

E15: DRES encode toàn queries, sort corpus length, chunk mặc định 50.000, score cos/dot matrix, NaN→-1, torch.topk(top_k+1), heap giữ top_k, skip ID giống nhau. Đây là exhaustive **vector similarity** trong scope embeddings đã encode, không scan text, có score/candidate cap. `[CODE]` L102 dùng `len(cos_scores[1])` chỉ số query thứ hai; nếu chỉ 1 query và corpus nonempty có nguy cơ IndexError (không chạy, TC01 phụ). Nếu embeddings truncate text theo max length thì even exhaustive vector không bảo đảm đoạn cuối được nhìn. Chi phí score theo Q×D×dimension, bộ nhớ matrix Q×chunk, heap Q×K; chưa đo RAM/GPU. Không chọn đường này để chạy metric thuần.

File path E16–18: cache tái dùng theo filename tồn tại và `overwrite=False`, không thấy hash/config/rights validation trong đường này. `glob` shard có thể lẫn stale; `search_from_files` tham số score_function mặc định dot, FAISS FlatIP; không thấy normalize trong đường add này. Cosine parity phải đo, K>docs có thể trả sentinel -1 và map Python negative index (suy luận nếu backend trả -1, test native cần thiết). Pickle chỉ file trusted, không expose upload. E19 ES init có delete/create index: chỉ disposable dev index, tuyệt đối không production. Rerank E22 chỉ xếp lại top candidates; đo candidate recall trước và sau, không suy reranker phục hồi passage chưa được đưa vào.

### 5.4 Datasets / paper / rights / external validity

Paper abstract NeurIPS 2021 (E25) mô tả heterogeneous zero-shot trên 18 bộ và các họ retriever. README hiện quảng bá 17 preprocessed datasets; khác scope/phiên bản, không gọi đây là bug; leaderboard và research paper không đồng nhất distribution. Không áp dụng mean score công bố cho domain Phật học. Repo code Apache-2.0, data/model rights độc lập, README disclaimer explicit. Các ví dụ đọc được: SciFact train/test, SCIDOCS test, FEVER train/dev/test, Quora dev/test, DBPedia dev/test, ArguAna test. URL dạng `https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/<dataset>.zip`; bảng README có MD5-style digest (SciFact `5f7d1de60b170fc8027bb7898e2efca1`, SCIDOCS `38121350fc3a4d2f48850f6aff52e4a9`). Không tải, không kiểm digest bytes; downloader E20 không tự verify checksum. Dataset revision, terms và domain-language coverage thực tế UNKNOWN.

| Dataset/asset | Split theo README đọc | Quyền / quyết định |
|---|---|---|
| SciFact | train/test | chưa đọc điều khoản gốc; ứng viên subset TC16 khi xác minh bài/abstract license; không mặc định cho redistribute |
| SCIDOCS | test | chưa xác minh data license và paper rights, defer |
| FEVER | train/dev/test | chưa xác minh nguồn evidence Wikipedia và điều khoản annotation, defer |
| Quora / DBPedia | dev/test | chưa xác minh terms của câu hỏi/DBpedia và attribution, defer |
| ArguAna / Touche / CQADupstack / Climate-FEVER | test | từng nguồn và quyền thương mại/chia sẻ chưa kiểm, defer |
| Bộ khác, multilingual datasets, leaderboard, weights | chưa kiểm đầy đủ | UNKNOWN; không lấy license repo thay các terms này |

Paper gốc mới đọc abstract/metadata, chưa audit full PDF; wiki multilingual và terms từng bộ chưa mở đầy đủ. Không có bằng chứng benchmark đại diện Pāli, Việt, Hán cổ, Tạng/Wylie, Sanskrit, văn bản song hành, OCR scan hay quyền dùng sách; ngay cả domain-general model tốt vẫn có thể sai negation/edition. Không loại package evaluator chỉ vì training data khác: input own corpus hợp lệ là đủ để đánh giá IR, nếu metric contract đúng.

### 5.5 Giả thuyết H01–H12

| H | Kết quả hiện tại | Evidence/giới hạn | Stop / flip criteria |
|---|---|---|---|
| H01 package nhẹ, không model/server | một phần: evaluate không gọi model; full install nặng về direct deps | E04/08/10, native UNKNOWN | B chỉ nếu offline import + lock/deps/cost qua TC01; C thắng nếu B kéo gánh thừa |
| H02 qrels đủ mọi outcome | bác bỏ contract | E07/E30; doc relevance không chứa multiplicity/locator | chỉ dùng Track B; không flip bằng đổi chunk ID mà mất identity |
| H03 metric mọi edge đúng | UNKNOWN native; code hazard | E10/12/13, TC02 cô lập | parity mọi expected với tolerance và conventions cố định, không cherry-pick |
| H04 missing/unjudged không làm đẹp | không đảm bảo, counterexample cô lập | E10/19/21/24/E29 | wrapper báo count và missing/error, reject nếu aggregate silently drop |
| H05 IDs ổn định qua edition/reindex | không tự bảo đảm | E07/16 | sidecar unique, frozen revision, old ID resolves or STALE TC14 |
| H06 dense exact = literal | bác bỏ | E15/17 | không dùng vector để cấp EXACT dù k=N |
| H07 public scores dự báo Phật học | chưa có chứng cứ | E25, không có gold thật | domain-held-out paired effect + strata; vẫn không thay Track A |
| H08 đo OCR/citation G2 trực tiếp | bác bỏ về role | E07/10 vs E03 | external oracle + source reopen, không dùng nDCG làm G2 |
| H09 gold tự từ engine/AI vẫn độc lập | bác bỏ nếu cùng output là oracle | thiết kế E29/30 | human independently annotate; AI chỉ gợi ý, audit blinded/adjudication |
| H10 adapter BCR/SQLite không đổi authority | khả thi theo fixture; BCR native chưa chạy | E27–30 | TC13 snapshot export read-only, no dual DB, fail nếu mapping mất edition |
| H11 evaluator nhỏ rẻ hơn full suite | plausible, chưa đo | E04/E26 | lock + integration diff, CI time/RSS + reviewer cost thực tế; choose least compliant cost |
| H12 BEIR tăng reproducibility/decision value hơn tiny harness | conditional | E21/E25/26, E29 | ranked feature thật + standard external comparisons + parity/maintenance savings; nếu không defer |

## 6. Source Fidelity & Provenance

BEIR không sở hữu file gốc hay citation locator. Corpus ID chỉ là khóa projection. Qrel positive có thể là passage nói về một câu mà không chứa chính xác câu, có thể là bản dịch sai, có thể một bản photocopy khác trang. Không nâng relevance thành TEXT_ONLY/VERIFIED/SUPPORTS. [E01–03, E07].

**Track A** oracle ngoài engine: (file_id, edition_id, extraction_revision, start, end), codepoint Python Unicode half-open, cùng immutable canonical revision; lưu SHA256 raw và canonical bytes, offset mapping về raw/source page hoặc fragment. Phân biệt PDF physical index và printed page; bbox/range hoặc EPUB spine/href/CFI/TEI XPath/segment ID tùy parser. Nếu chỉ cấp page/block thì hiển thị granularity thật. Canonical text có thể OCR sai; EXACT vào canonical không là xác minh ảnh scan. Không sửa normalized trở lại raw. Query scope gồm corpus, ngôn ngữ, edition, filters, text layer, revision, join segment policy, rights. Cross-segment chỉ tìm nếu liên tiếp theo source map và boundary rule công bố; không nối hai sách hoặc hai cột sai reading order. Overlap phải enumerate cả hai start.

**Metric bắt buộc:** set P=TP/(TP+FP), R=TP/(TP+FN) trên key, duplicate count riêng trước set; scope gold P/R=1, zero wrong file/edition/locator và false VERIFIED trên negatives; empty gold/empty results báo true negative riêng không tự đặt P/R=1; partial coverage không cấp COMPLETE. Tách page/character coverage (expected vs extracted vs indexed vs searched) và errors/timeouts, truncated counts, stale IDs, denied rights. Không dùng qrels recall document thay occurrence recall: fixture d1 có 5 hits trong một doc, 3 doc khác có thêm 3 hits; top1 chọn d1 có thể relevant tuyệt đối ở rank1 nhưng recall occurrence=5/8. Có thể mọi doc đều retrieved mà mỗi doc trả một offset, vẫn mất 4 trong d1.

**G2 independent checker:** nhận expected identity/range từ authoritative catalog, mở file raw đúng SHA/revision bằng đường không dùng index results, xác định range theo source map, đối chiếu literal và context, xác minh locator/phạm vi đọc, OCR risk chuyển người rà. Nếu SHA mismatch, locator invalid, edition khác dù quote giống, source unavailable: REJECTED/UNVERIFIED hoặc STALE, không VERIFIED. G2 không đồng nghĩa G3: câu trích đúng có thể được tác giả bác ngay sau đó. BCR evidence_gate tại E28 là candidate đáng kiểm trước khi tự xây toàn gate, nhưng scope Git-pinned corpus không chứng minh universal file/edition/PDF.

**Định danh Track B:** passage_id stable trong extraction revision (ví dụ opaque ID từ catalog hoặc hash namespace + file + edition + revision + segment/range; không chỉ hash text vì hai edition trùng câu). Frozen map `passage_id -> file_id,edition_id,revision,start,end,language,source_locator,canonical_sha256,access_scope`. Không reassign old ID sau reindex; changed segmentation new IDs, map explicitly or STALE. Test hold-out giữ snapshot; cùng source group không tách bản dịch gần trùng giữa tuning/test nếu đánh giá generalization. Không yêu cầu BEIR loader giữ metadata, vì owner core phải giữ sidecar.

## 7. Multilingual & Retrieval Behavior

BEIR measure tính theo IDs, nên language-agnostic ở tầng metric; model/tokenizer/retrieval mới có năng lực cụ thể. Loader UTF-8 không chứng minh Unicode correctness, dấu Pāli, Hán ngắn, Wylie conversion hay lexical sense. Tách nhóm test và label; cùng qrels grade không mang phép chuyển đổi.

| Stratum | Track A / retrieval | Track B judgment | Ca bắt buộc |
|---|---|---|---|
| Pāli/Sanskrit Latin | NFC vs NFD giữ raw, NORMALIZED nếu chuyển; diacritics fold versioned | relevance grade có lý do, lemma ≠ exact | TC08 `anattā` vs decomposed, anatta |
| Việt | `đ` không tự biến thành `d` ở EXACT; dấu có thể phân nghĩa | reviewer kiểm từ đồng dạng/khác nghĩa | TC08 `đạo`/`dao`, `vo thuong` |
| Hán | literal 1–2 chars, CJK short fallback; giản/phồn không exact | grade theo context, đối chiếu dị thể | TC08 `無常`/`无常`/`常` |
| Tạng/Wylie | script/transliteration version riêng, không sửa quote | reviewer duyệt spelling/meaning, typed relation | TC08/T04 chưa chạy |
| OCR noisy/format | raw scan coverage, negation missing, boundary | fuzzy discovery vs exact text | TC09/10/11 |
| Lexicon/cross-language | sense_id và relationship type bên ngoài | relevant translation không chứng minh equivalence | TC12/T05–07 |

TC08 fixture chứng minh khác raw NFC/NFD, normalize NFC equality, khác `đạo`/`dao`, Hán `常` offset 1 và giản/phồn khác literal. Không thử Tibetan tokenization/Wylie conversion, không đánh giá engine ranking theo language. Gold thật phải có strata language×format×query type (literal, normalization, fuzzy, lexicon, semantic), không aggregate che low-resource. Macro per-query/per-language, micro occurrence theo scope; paired difference same queries; khi mẫu nhỏ báo counts, không CI giả chính xác. Với đủ mẫu, bootstrap paired query/source groups theo strata, báo interval và effect size, không coi correlated translations độc lập.

## 8. Integration Options

| Option | Thành phần / owner | Lợi ích | Chi phí/rủi ro (định tính) | Stop / rollback |
|---|---|---|---|---|
| A full suite | BEIR + datasets + models + wrappers; dev only | so leaderboard, reproduce research | H/VH; rights, egress, dependencies, GPU/ES tùy engine; không tăng G2 | stop nếu không có external comparison requirement; xóa dev env, keep gold |
| B evaluator-only | BEIR static evaluate, own projection/qrels | familiar API/format, metrics & custom helpers | M; 3 declared deps full package, denominator/mutation wrapper | nếu parity/import/cost kém C, bỏ dependency và giữ run format |
| C lightweight backend | `pytrec-eval-terrier` trực tiếp hoặc `ir_measures` pinned + wrapper | per-query metrics, tránh model stack; `Judged` tiện | L/M dự kiến; native wheel availability, metric parameter drift, backend selection | nếu dependency/ABI khó hoặc parity fail, D; không dùng nhiều backend production |
| D tiny harness | Track A Python/SQLite set diffs, explicit query status; minimal B metrics nếu cần | đơn giản nhất cho V1 code-only, control hard gates, no extra runtime dependency | L cho fixture, M/H cho full gold/reopen; nguy cơ tự viết metric sai nếu mở rộng | khi ranked metrics/standard compare phức tạp, add C/B dev-only, giữ Track A |
| E methodology only | spec/gold format chưa code evaluator | zero dep, chuẩn bị schema | L ban đầu, manual repetition, không đủ regression V1 | dùng kết hợp D ngay; không defer Track A |

**Đề xuất module hẹp** (`tests/gold/track_a`, `tests/gold/track_b`, `qa/export.py`, `qa/occurrence_check.py`, `qa/run_manifest.py`, optional `qa/ranked_metrics.py`). Tên module là đề xuất chưa tồn tại, không commit. Input read-only catalog and search API; export only approved text, preferably qrels/run IDs only cho metric evaluator (không cần corpus text cho evaluate). Không dựng API/MCP/queue riêng. Adapter gọi BCR `search()` cho ranked discovery hoặc SQLite projection; mapping ổn định theo core, không thay BCR source pins hay ép BCR schema thành BEIR. Tách run states: COMPLETE/PARTIAL/FAILED/DENIED và judgment state; report fail closed nếu missing manifest, qid orphan, duplicate, stale. Khi thay engine, chạy fixture và held-out cùng snapshot rồi giữ raw/run config để tái lập. Rollback chỉ tắt QA backend hoặc pin lại venv; không migration authoritative DB. Nếu D không đạt hiệu năng all-offset, tối ưu candidate generator với proof coverage, không cắt K rồi gắn COMPLETE.

**Chia sẻ P58/P59/P60/P61:** một versioned gold registry độc lập (Track A raw fixtures + occurrence/negative/reopen oracle; Track B query IDs, rubric, grades, typed judgment), runner adapters riêng. Freeze fixtures bằng SHA256, cùng split, cùng expected, mỗi tool ghi result manifest; không đổi qrels vì engine trả khác. Khi reviewer sửa gold, new revision + rationale + rerun mọi tool; không dùng kết luận P59 chưa có. Đảm bảo cùng rights, không đẩy text hạn chế vào repo public. Gold nhỏ synthetic chạy CI; domain gold local permissioned, reviewer blind/adjudication. Không dùng LLM judge làm nguồn duy nhất.

## 9. Practical POC & Reproduction Plan

### 9.1 Điều kiện thực thi và oracle

Fixture tự tạo: 12 passages, 8 queries, 2 edition A/B, graded qrels (0,1,3), no-hit, missing key, no-positive, ties, unjudged, identical ID. Không trích sách, không có claim học thuật thật. Oracle B lập bằng tính tay trước implementation (linear gain, grade>0, K=3, tie ID asc, undefined no-positive); oracle A literal `x` với offsets liệt kê tay. Fixture và log/script đầy đủ §13; checksum trên canonical JSON UTF-8 sort_keys=True separators=(',',':'), không phải checksum dataset upstream. Test chỉ là minh họa regression harness, không có reviewer thứ hai, không đủ domain gold. Test SQLite in-memory không đọc BCR DB. Script không network, không model. Python 3.13.5, SQLite 3.46.1, Linux x86_64 glibc 2.41, AMD EPYC 9V74 (5 logical CPUs thấy được, cgroup quota 4 CPU), cgroup RAM 4 GiB, GPU không dùng/không probe. `beir`, `pytrec_eval`, `ir_measures` không có, `torch`, `tqdm`, `rapidfuzz` có spec nhưng không import/chạy. Không có lock native, nên không tự cài package online. Lệnh đã chạy: `python /tmp/p61/poc.py > /tmp/p61/log.txt 2>&1` (exit 0). Reproduce bằng lưu script §13 thành `poc.py`, chạy `python poc.py`.

### 9.2 Kết quả per-query (TESTED-ISOLATED)

| qid | nDCG@3 | AP@3 | R@3 | P@3 | MRR@3 | Trạng thái |
|---|---:|---:|---:|---:|---:|---|
| q1 | .68853 | .83333 | 1 | .66667 | 1 | graded, 1 unjudged |
| q2 | 0 | 0 | 0 | 0 | 0 | missing run key |
| q3 | 0 | 0 | 0 | 0 | 0 | explicit empty |
| q4 | null | null | null | 0 | null | judged 0, no positive |
| q5 | 1 | 1 | 1 | .33333 | 1 | tie id asc |
| d1 | 1 | 1 | 1 | .33333 | 1 | same query/doc ID allowed |
| q7 | .63093 | .5 | 1 | .33333 | .5 | unjudged first |
| q8 | .61315 | .5 | .5 | .33333 | 1 | one hit, two relevant |
| Macro defined (7 or 8 qids) | .56180 | .54762 | .64286 | .25000 | .64286 | all declared, null excluded per metric |
| Macro bỏ q2 (6 or 7 qids) | .65543 | .63889 | .75000 | .28571 | .75000 | minh họa inflation, không phải BEIR output |

K=3 đã chọn trước; nDCG difference .09363 khi loại một missing query. Đây là demonstration trên fixture giả lập chính sách aggregation, không ước lượng mức inflation thực. q5 alternate tie ordering tại K=1 làm nDCG/R/AP/P/MRR từ 1 xuống 0; script dùng score đảo thứ tự để kiểm hai possible rankings, chưa chạy native exact ties. Judgment coverage cần report per qid: q1 2/3 retrieved judged, q7 1/2, q5 2/2; K denominator nếu `Judged@K` là 2/3, 1/3, 2/3 tương ứng; các quy ước không được trộn. 8 query declared, 7 run keys, 1 missing q2, 1 explicit empty q3, 1 no-positive q4, 6 nonempty run (7 keys gồm q3 empty và 6 nonempty); no qid extra. Không có timeout/no access trong fixture. Ties/ID mutation chỉ mô phỏng.

Track A expected 8 tuples, actual 8, FP=0/FN=0, P=R=1. Top1 projection d1 giữ 5/8, FN=3, P=1/R=.625. Overlap `aaaa`/`aa` offsets 0–2,1–3,2–4; `ab`+`cd`/`bc` offset 1–3 theo declared concatenation. Không có real locator, raw PDF reopen hay verifier trong script nên wrong-edition/false VERIFIED production = null, không được ghi 0. Gold key gắn edition A/B cho fixture nhưng chưa kiểm thử attack quote từ edition khác. Không đo p50/p95/RSS/disk/CI time, không extrapolate.

### 9.3 TC01–TC16: expected / actual / status / next action

| TC | Expected & independent acceptance | Actual / evidence | Status và phép tiếp theo |
|---|---|---|---|
| TC01 pin install/import offline | clean venv, exact version lock, no model/server/download; smoke single qid | package specs absent; DNS failure; native actual=null | BLOCKED/NOT TESTED; stage approved wheelhouse, offline install B/C, import and network deny; test DRES single-query only if chosen |
| TC02 graded/binary metrics | q1 expected values §9.2 and AP cap variants, linear/exp gains explicitly chosen | Python actual matches all 8 per-query hand values | PASS ISOLATED; native actual=null; compare backend raw and rounded tolerance |
| TC03 missing/no hits/no positives | all 8 declared; distinguish missing/empty/null; extra qid errors; no silent filtering | all vs dropped macro §9.2, no native | PASS ISOLATED policy; BEIR risk E10/E24; run empty/all-missing/unknown qid and check backend counts |
| TC04 unjudged/graded/ties | q1/q7 unjudged count; two tie permutations, deterministic or sensitivity | q7 unjudged=1, tie alternative values 1 vs 0 | PARTIAL ISOLATED; repeat native same-score/order permutations and round-trip |
| TC05 duplicate/same ID | reject duplicate before dict; same ID legit retained with false flag; input immutable | dict overwrite emulated, self pop changes 1→0 in copy | COUNTEREXAMPLE ISOLATED; actual loader/eval null; native duplicate TSV/JSONL and compare original run |
| TC06 multi-occurrence/top_k | 8 exact offsets independently, top1 cannot COMPLETE | 8 full; 5 top1; FN3 | PASS ISOLATED; native BCR/SQLite adapter actual=null, full-scope raw scan vs candidate union |
| TC07 boundary/overlap/two editions negation | overlapping 3, contiguous crossing 1; no join across editions; wrong edition=0 | overlap/boundary matches; two editions fixture but no reopen/negation test | PARTIAL ISOLATED; run edition A affirms/B denies, independent page/range reopen |
| TC08 multilingual | raw NFC/NFD distinct, normalized label, Việt đ/d distinct, Hán short literal, Tibetan/Wylie scoped | Python Unicode assertions, no tokenizer/normalization engine, Wylie untested | PARTIAL ISOLATED; core label/map and reviewer gold required |
| TC09 missing OCR/stale/timeout/denied | manifest partial/error not no-result; no COMPLETE | actual=null | PLAN P0; mock failed page and stale source pin, inject timeout/rights denial; oracle expected coverage table |
| TC10 wrong SHA/locator/spoof/negation | independent opener fails all negatives; false VERIFIED=0 | actual=null | PLAN P0; BCR gate/resolver and PDF source reader fixture, T01/T02/T15 |
| TC11 candidate vs reranker/fuzzy | same qrels, candidate recall separate from final nDCG; typo expected passage | actual=null | PLAN V1 if fuzzy, V2 if semantic; run BCR/SQLite then RapidFuzz bounded on same candidates, no model required initially |
| TC12 cross-language/translation dependence | typed grade/sense/group, no implied equivalence or SUPPORTS | actual=null | PLAN reviewer; two senses and one countertranslation, independent reviewers |
| TC13 BCR/SQLite export | 12 IDs, valid refs, snapshot checksum; no second DB, same metric | SQLite fixture export 12, mapping digest, equality | PASS ISOLATED; native BCR query + core passage map, ACL and source pins test |
| TC14 frozen dev/test/reindex | separate split manifest; changed rev new IDs or STALE, old reopen correct | actual=null | PLAN P0 for old IDs; version migration dry run, no test tuning |
| TC15 BEIR vs backend vs hand | parity on fixed conventions; measure deps/install/CI/maintenance | hand vs local Python passes; BEIR/C actual=null | PARTIAL ISOLATED; compare B/C per-query to independent expected (not compare two implementations sharing same backend as independent truth) |
| TC16 lawful public subset | license and bytes pinned, same metrics; domain-vs-general comparison | actual=null; no downloads | PLAN optional V2; skip until rights and ranked question, no extrapolation |

Summary: 0 `[TESTED]`; four full isolated-scope PASS rows TC02/03/06/13; TC04/07/08/15 partial isolated; TC05 isolated counterexample; TC01 blocked native; TC09/10/11/12/14/16 planned. All native/integration actuals null. No hidden PASS for TC03 upstream. TC02 POC only AP where R<=K; additional hand case R>K distinguishes denominator min(R,K) vs R (R=4,K=2, 2 hits: AP_cut=1 vs .5). For qrels no-positive define policy before parity, report native convention separately.

### 9.4 Native reproduction (PLAN, chưa chạy)

1. Trên máy có quyền tải dependency: lấy wheel/sdist từ PyPI, kiểm published SHA256, lấy commit/tag và hash artifacts; build wheelhouse + hash lock từng OS/ABI (Python 3.11/3.12 là ứng viên do metadata, không đảm bảo). Security scan SBOM/dependency license. Không dùng `pip install --no-deps` như shortcut nếu import không đủ deps. Môi trường B và C riêng; direct deps B=3 theo pyproject; C `pytrec-eval-terrier` direct một package do chọn, hoặc `ir_measures` + provider pinned, số transitive chưa biết. Không cài cả hai vào runtime sản phẩm.
2. Sandbox offline CI: `python -m venv .venv`; `.venv/bin/python -m pip install --no-index --find-links /approved/wheelhouse --require-hashes -r requirements.lock`; `python -m pip freeze --all`; deny egress ở OS/network namespace; `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1` defense-in-depth, không dùng làm bằng chứng no-network. Log CPU/RAM/OS, versions, import walltime, peak RSS, disk, install error. `requirements.lock` phải được tạo và duyệt trước, hiện chưa có.
3. Lưu fixture §13, script export qrels/run/queries JSONL và corpus JSONL + sidecar; tạo expected hand values, check valid refs/duplicates. Pseudocode kiểm BEIR và backend (chưa chạy):

```python
from copy import deepcopy
from beir.retrieval.evaluation import EvaluateRetrieval
import pytrec_eval
# qrels, run, expected từ fixture đã freeze; k_values=[1,3]
assert set(run) <= set(qrels)
raw = deepcopy(run)
metrics = EvaluateRetrieval.evaluate(qrels, deepcopy(raw), [1,3], ignore_identical_ids=False)
backend = pytrec_eval.RelevanceEvaluator(qrels, {'ndcg_cut.1,3','map_cut.1,3','recall.1,3','P.1,3'})
perq_raw = backend.evaluate(deepcopy(raw))
complete = {q: deepcopy(raw.get(q, {})) for q in qrels} # only fixture missing/no-hit, not error
perq_complete = backend.evaluate(complete)
print(sorted(set(qrels)-set(perq_raw)), sorted(perq_complete))
# assert per-query values vs hand under agreed conventions; report native zero-positive separately
# compare same ID default vs False on fresh copies, assert input untouched in wrapper
# ir_measures option: use nDCG@3/AP@3/R@3/P@3/RR@3/Judged@3 with explicit provider/gain policy
```

4. Native test matrix: empty qrels/run, only missing query, explicit empty query, no positive graded zero, extra qid/doc, duplicate IDs preflight, score NaN/Inf, K larger hits, R>K AP denominator, ties insertion order/permutations, run save/load with sidecar, loader repeated split instance vs new instance. For agreed same convention use absolute tolerance <=1e-5 on aggregate rounded BEIR, compare unrounded backend with <=1e-9 where feasible; mismatched conventions must be explained, never adjust oracle to fit. Metric threshold for Track B chosen per feature (non-inferiority on held-out paired baseline and candidate recall requirement agreed in advance; no universal nDCG target). Track A P/R=1 on declared complete gold scope, zero wrong edition/locator/false VERIFIED, no silent truncation; partial explicitly not pass complete.
5. Apply only if rights: BCR pinned fixture/local SQLite; independently label before engine runs, source reopening, failed page injection, source hash, stale rev. POC gold domain requires permissioned scans and texts, not supplied; obtain explicit rights + reviewer time. Compare paired candidate generator and reranker with fixed K (proposed K=10/50 after reviewer agrees), candidate recall on max candidate window, rank nDCG/MRR/P/Recall and per-query judgments. Use no LLM judge alone. Assess CI cold/warm runs separately, repeated wall/RSS p50/p95 with sample counts, disk, module diff LOC, resolved deps count, setup/upgrade/rollback attempts, human review hours and external cost if any. Current measured_cost=null.

### 9.5 Manifest và sample event (PLAN schema; ví dụ synthetic, không giả native result)

```json
{"run_id":"p61-isolated-v1","engine":"python-sqlite-fixture","engine_version":"Python 3.13.5 / SQLite 3.46.1","source_pin":"synthetic-v1","extraction_revision":"r1","index_revision":"memory-v1","corpus_sha256":"5ce45bc1734cc0a5ef967a492df7a040a95b05249cef5c54dbbef6f49ddcc5dd","queries_sha256":"a62eae64bb9ffd4c6571f661fd0d6d266537bdabdc6b23d1d12084dbc4769183","qrels_sha256":"94763964a16af6447d9c18258b9d31994cf98c864277ddf723432e1eac280489","oracle_a_sha256":"d462cc4416a5263aa86c8f6201f6722b3dc78680bfb74d9a6e35dbb63f8b4bee","oracle_b_sha256":"89097e0c539f238f902acc13b204c380637a1302783b4489778f59d37e2a1309","mode":"RANKED_FIXTURE","filter_scope":"12 synthetic records","top_k":3,"normalization":"none","score_policy":"linear gain, rel>0","tie_policy":"score desc/id asc","declared_query_count":8,"run_key_count":7,"missing_query_ids":["q2"],"zero_hit_count":1,"no_positive_ids":["q4"],"excluded_reason":{"q4":"undefined for nDCG/AP/R/MRR; counted for P"},"judgment_coverage":"per-query report; see section 9.2","native_beir_actual":null}
```

```jsonl
{"qid":"q2","state":"MISSING_RUN_KEY","expected":{"recall@3":0},"actual_isolated":{"recall@3":0},"actual_beir":null,"judged_positive_count":1}
{"qid":"q3","state":"SUCCESS_ZERO_HIT","expected":{"recall@3":0},"actual_isolated":{"recall@3":0},"actual_beir":null}
{"qid":"q4","state":"NO_POSITIVE_JUDGMENT","expected":{"ndcg@3":null},"actual_isolated":{"ndcg@3":null},"actual_beir":null}
{"qid":"literal-x","track":"A","scope":"all 12 synthetic records","expected_count":8,"actual_isolated_count":8,"actual_top1_count":5,"fn_top1":3,"coverage":"fixture text only","wrong_edition_native":null,"false_verified_native":null}
```

Manifest final implementation also records run hash, raw bytes SHA/revisions per source, ACL, qrel rubric version, reviewer IDs pseudonymous, judgment uncertainty, index/parser/model/dependency lock digests, retrieval error events, excluded IDs/reasons, per language/format counts and resource measurements. Example is illustrative schema with measured isolated counts, not production log. For held-out store artifacts immutable separately from tuning set.

### 9.6 Sổ tay T01–T16 mapping

| T | Relation to TC and owner | Status |
|---|---|---|
| T01 scan two-column negation | TC09/10 OCR + verifier | PLAN |
| T02 two editions printed/pdf page | TC07/10 source map | PLAN (fixture editions only) |
| T03 Việt/Hán variants | TC08 normalization | PARTIAL isolated |
| T04 Tibetan/Wylie | TC08 | PLAN |
| T05 two senses | TC12 reviewer | PLAN |
| T06 parallel texts differing | TC12 reviewer + witness | PLAN |
| T07 correlated translations | TC12 source group | PLAN |
| T08 universal claim exception | TC10/12 G3 reviewer | PLAN |
| T09 manuscript vs historical date | G3 human separate gold | PLAN/N/A BEIR |
| T10 missing PDF page no-hit | TC09 coverage | PLAN |
| T11 DOI/abstract only | G4 access record, TC16 rights | PLAN |
| T12 prompt injection in external text | G4 read-only + untrusted content, no agent for evaluator | PLAN |
| T13 index rebuild chunk ID | TC14 old mapping | PLAN |
| T14 cross-chapter contradiction | G6 consistency review | PLAN/N/A BEIR |
| T15 quote followed by refutation | TC10/12 G3 context | PLAN |
| T16 limited copyright | TC01/16 rights and egress | PLAN |

## 10. Deployment, Security, Legal, Cost

**Deployment:** local/offline dev CLI/CI, no always-on service, no embedding model or Elasticsearch for metrics. With B/C metric-only, pass IDs/scores/qrels not text where possible. Export subset under ACL; do not grant benchmark runner write access to source store, index or published evidence. No corpus in public CI/logs. Full suite wrappers may call model downloads or external APIs; explicitly disable unless separately approved. No private content submitted to public/cloud. Separate dev lock from app runtime. Backup gold, qrels, manifests, raw run and mapping with access control, restore drill verifies hashes and old IDs; caches and embeddings rebuildable, never authority.

**Code rights:** Apache-2.0 permits commercial use/modification/distribution subject to license terms, preservation of notices/license and applicable NOTICE/modified-file requirements; patent license/termination and warranty disclaimer apply. LICENSE header read and repo metadata confirm; full legal review, NOTICE at root returned 404, other third-party notices and dependency licenses not audited. No blanket restriction on cloud from code license alone, but check every dependency, dataset/model/provider terms and private corpus agreement separately. Beta classifier, no attestation on wheel, use verified source + hash locked artifacts and SBOM. Not legal approval to redistribute BEIR corpus. Model weights and remote APIs not required for evaluator and not assessed. Commercial/cloud data use UNKNOWN until reviewed. No external publication from this report.

**Downloader & file security (E20):** `requests.get(stream=True)` lacks visible timeout, `raise_for_status`, content checksum/size limits; writes path before successful validation, reuses zip and dir by existence. Not evidence of exploit, but avoid helper for untrusted ZIP. Stage download to tmp, validate trusted URL and TLS/allowlist, content length and SHA256 with trusted manifest (README MD5 only integrity hint, not security), enforce max archive/uncompressed bytes/count, reject traversal/absolute/symlink paths as appropriate, extract to isolated temp, atomic rename only after validated. JSONL/TSV strict size/rows/int bounds, no NaN scores, cap memory, avoid XML/ZIP parsing for metric-only. XML if later imported handled in dedicated parser with entity/DTD protections and resource quotas. E18 pickle deserialization unsafe for untrusted data, never load external cache. ES deletion risk E19; isolated namespace/no production credentials. E06 logging text leaks, configure redaction and export only necessary fields. No source pin changes, no writes to GitHub.

| Cost dimension | D baseline | B evaluator-only | C minimal backend | A full suite |
|---|---|---|---|---|
| Direct new dependency count | 0 stdlib for tested fixture | 3 declared deps (full install) + package | proposed 1 backend package or wrapper+provider; resolved unknown | same base + selected extras/models |
| Runtime services needed for metrics | 0 | 0 by code | 0 expected | depends retriever (ES etc), not required for pure metric |
| Install/import CI cost | stdlib fixture ran, time not measured | UNKNOWN | UNKNOWN | UNKNOWN |
| Gold annotation/reviewer | required | required | required | required, domain rights plus external dataset |
| Maintenance | small Track A contract; avoid reimplement complex B | adapter + denominator/identity policy + pins | provider convention + ABI + pins | larger stack/version churn, model/data rights |
| Monetary cost | unknown; no paid API used | unknown | unknown | unknown |

TCO compare actual lock resolution, setup friction, diff churn, failed upgrade/rollback and CI costs, plus annotation/adjudication hours (likely important regardless evaluator). No person-days inferred from file count, no actual latency or dollar estimates. D appears lowest incremental V1 cost because hard gates must be built anyway; not proof overall cheapest if ranked evaluation complex. If native backend installation requires compiler/new environment unsupported target ABI, evaluate isolated dev runner rather than change V1 runtime. No security vulnerability scan run; rights gate NOT DEMONSTRATED.

## 11. Comparison & Trade-offs

Compare **QA** alternatives, not search engines versus OCR. `pytrec_eval` as module can be used directly from `pytrec-eval-terrier` distribution pinned, preserving per-query output instead of BEIR aggregate. `ir_measures` offers standardized metric names/parameters, `Judged@K`, perquery and aggregate interface ([docs](https://ir-measur.es/en/latest/), [measures](https://ir-measur.es/en/latest/measures.html)); different providers may differ tie/gain/undefined and bugs, e.g. [issue #83](https://github.com/terrierteam/ir_measures/issues/83) reports provider mapping issue, not reproduced and may not apply to future version. Neither direct backend nor ir_measures installed; no claim of actual parity or lower measured TCO. If backend common, agreement B/C not independent truth; hand fixture and alternate implementation required. A tiny Python ranked evaluator is transparent but risky when AP variants, bpref, graded gains, incomplete judgments and tie policies expand; prefer mature backend if it saves maintenance after tests.

| Requirement | Best current candidate | Why / counterargument |
|---|---|---|
| Fastest useful demo V1 | D | actually ran stdlib fixture; no install. If team already has locked BEIR env, B could be fastest ranked demo; not measured. |
| Lowest compliant total cost V1 | D + methodology E (conditional) | Track A must exist independent of B/C/A; no ranked dependency before need. Human gold cost shared. |
| Ranked regression with standard metrics | C first, B comparison | per-query and smaller intended dependency surface; B convenience if integration/maintenance measurably better. |
| Published model leaderboard reproduction | A in isolated research env | external comparability when explicit requirement; not V1 hard gate, no automatic domain generalization. |
| Citation/coverage | Track A + independent verifier | no ranked metric replaces hard gate. BCR Gate A candidate; not adjudicated as entire architecture in P61. |

**Flip thresholds:** choose B over C/D only if all P0 metric cases parity, wrapper exposes query counts/errors/no mutation, install offline and license pass, measured integration/maintenance savings over C/D at same scope. Choose C if B forces unnecessary model/dataset transitive deps or extra adapter and C passes parity with less burden. Keep D for V1 if no ranked feature requiring reusable standard metric; adding ranked feature with multiple retrievers, held-out regressions and published comparisons triggers TC15, not arbitrary number of repos. Choose A only when same lawful dataset/model versions and zero-shot external comparison justify extra stack; stop if external dataset rights uncertain or cannot reproduce. Downgrade any if qids drop, tie policy silently differs, incorrect source mapping or test tuning contamination; no score trade-off overrides G2. No final decision on Bang-ha vs BCR vs new authority implied by this report; it evaluates QA tool regardless engine.

## 12. Decision Record for Master Synthesis

| Field | Value |
|---|---|
| target / class | beir-cellar/beir / IR benchmark and evaluator dev tool |
| snapshot | main ef83d293…; tag v2.2.0 6ef8c909…; PyPI 2.2.0 observed |
| license/access | code Apache-2.0; data/model rights UNKNOWN; GitHub read OK, native runtime BLOCKED |
| primary_role | ranked discovery QA, not authority or search engine |
| best_fit_v1 | D Track A + E format/methodology; no BEIR dependency |
| best_fit_v2_v3 | C/B dev-only conditional, A only research reproduction |
| source_fidelity_gate/exact_gate | N/A direct; external Track A NOT DEMONSTRATED production |
| multilingual_gate | UNKNOWN engine/domain; isolated Unicode only |
| coverage_gate | CODE GAP query universe; external source coverage NOT DEMONSTRATED |
| rights_security_gate | NOT DEMONSTRATED |
| integration_cost/maintenance_risk | L for D fixture, M/H full gold+reopen; B M qualitative; risk of denominator/version churn |
| recommendation/confidence | DEFER dependency, MED; HIGH static distinction; LOW actual TCO |
| tests_executed | 0 native; 4 isolated full-scope PASS, 4 partial isolated, 1 isolated counterexample |
| measured_cost | null |
| next_poc | TC01/02/03/05/15 parity when ranked; TC06/07/09/10/13/14 V1 hard gates |

```json
{
  "target": "beir-cellar/beir",
  "class": "IR_BENCHMARK_DEV_QA",
  "snapshot": {"branch":"main","head":"ef83d29307061c65d04b035b4f4e7c18bd8374af","head_date_utc":"2025-10-16T06:38:02Z","tag":"v2.2.0","tag_commit":"6ef8c9097ebfb203ad360bd64e0cfb93e64f4a44","package_version_observed":"2.2.0","bodhiatlas":"c5dfe50613dfd492407bf1db1061c1cfc9d30e8e"},
  "license": {"code":"Apache-2.0","dataset":"UNKNOWN_PER_DATASET","model":"UNKNOWN_NOT_REQUIRED"},
  "access_status": "GITHUB_READ_OK_NATIVE_RUNTIME_BLOCKED",
  "primary_role": "Ranked retrieval benchmark methodology or dev-only evaluator",
  "best_fit_v1": "D: Python/SQLite Track A plus E methodology; defer BEIR dependency",
  "best_fit_v2_v3": "C or B dev-only after parity and cost POC; A only for lawful external reproducibility",
  "source_fidelity_gate": "N/A_DIRECT_EXTERNAL_NOT_DEMONSTRATED",
  "exact_gate": "N/A_DIRECT_TRACK_A_REQUIRED_NOT_DEMONSTRATED_PRODUCTION",
  "multilingual_gate": "UNKNOWN_DOMAIN_ISOLATED_UNICODE_ONLY",
  "coverage_gate": "CODE_GAP_QUERY_DENOMINATOR_EXTERNAL_SOURCE_COVERAGE_NOT_DEMONSTRATED",
  "rights_security_gate": "NOT_DEMONSTRATED",
  "integration_cost": "QUALITATIVE_D_LOW_FIXTURE_B_MEDIUM_FULL_GOLD_MEDIUM_HIGH",
  "maintenance_risk": "MEDIUM_IF_BEIR_ADDED; query denominator, dependency drift, identity mapping",
  "recommendation": "DEFER",
  "confidence": "MEDIUM",
  "tests_executed": {"upstream":0,"isolated_pass":["TC02","TC03","TC06","TC13"],"isolated_partial":["TC04","TC07","TC08","TC15"],"isolated_counterexample":["TC05"],"blocked":["TC01"],"planned":["TC09","TC10","TC11","TC12","TC14","TC16"]},
  "measured_cost": null,
  "next_poc": {"v1_hard_gates":["TC06","TC07","TC09","TC10","TC13","TC14"],"ranked_backend_if_needed":["TC01","TC02","TC03","TC05","TC15"],"domain_review":["TC08","TC11","TC12"],"optional_public":["TC16"]}
}
```

**Top 5 strengths:** (1) standard corpus/query/qrels and run format; (2) evaluator static API permits custom runs; (3) established metric backend rather than implementing all IR math; (4) separate retriever/reranker can benchmark common input; (5) heterogeneous research protocol and citations for external comparisons. **Top 5 blockers:** (1) denominator/missing query discrepancy; (2) duplicate/identical ID mutation and loader split cache; (3) qrels lacks occurrence/source fidelity contract; (4) package dependency and native wheel/ABI costs not verified; (5) no domain gold/rights/production performance evidence. Raise to USE AS COMPONENT for dev only if ranked use case and TC15 pass with lower measured TCO; lower to REJECT for QA backend if cannot preserve query universe or parity without invasive fork. Methodology remains useful regardless dependency decision.

## 13. Appendix

### 13.1 Inventory và mức truy cập

19 upstream files successfully retrieved at pinned HEAD (9 initial + 10 follow-up; enumerated below), plus evaluator at tag. Các file dài ở lượt sau được đọc qua excerpts/hàm liên quan, không tuyên bố audit từng dòng. 404 ở guessed test path không chứng minh repo không có test. Full recursive tree chưa được lấy qua connector; path thực tế được xác nhận qua fetch_file (file retrieval), không bịa test. Test native NOT RUN.

| # | File tại HEAD ef83d293… | Đoạn đã kiểm / role |
|---|---|---|
| 1 | README.md | usage, datasets, rights disclaimer L340–397 |
| 2 | pyproject.toml | version, dependency, extras L1–62 |
| 3 | LICENSE | Apache-2.0 header; rights summary, full license review pending |
| 4 | beir/__init__.py | L1–7 import logging |
| 5 | beir/logging.py | handler functions, tqdm |
| 6 | beir/datasets/data_loader.py | L13–134 load/split/duplicates |
| 7 | beir/util.py | L16–185 scoring/download/export |
| 8 | beir/retrieval/evaluation.py | L14–147 delegate + metrics |
| 9 | beir/retrieval/custom_metrics.py | L6–126 MRR/R_cap/Hole/Accuracy |
| 10 | beir/retrieval/search/base.py | L6–38 interface |
| 11 | beir/retrieval/search/__init__.py | BaseSearch export |
| 12 | beir/retrieval/search/dense/__init__.py | exports exact/FAISS variants |
| 13 | beir/retrieval/search/dense/exact_search.py | L25–251 embeddings/cache/heap |
| 14 | beir/retrieval/search/dense/util.py | L11–97 score/pickle |
| 15 | beir/retrieval/search/dense/faiss_index.py | FlatIP/batch/other variants excerpts |
| 16 | beir/retrieval/search/lexical/bm25_search.py | init/search/index excerpts |
| 17 | beir/retrieval/models/sentence_bert.py | model load/encode excerpts |
| 18 | beir/reranking/rerank.py | rerank top-K and predict |
| 19 | examples/retrieval/evaluation/dense/evaluate_sbert.py | entry imports/model/rank excerpts |

All 19 paths resolve at HEAD. `tests/test_evaluation.py` and `NOTICE` 404; tests tree web request blocked. Tag evaluator same method read L68–122. BodhiAtlas 5 foundational docs and 8 named historical reports excerpts read, P59 path 404; BCR two files excerpted at historical pin. Links §2. No source repo writes.

### 13.2 Raw logs (redacted, actual)

```text
$ git ls-remote https://github.com/beir-cellar/beir.git HEAD
fatal: unable to access 'https://github.com/beir-cellar/beir.git/': Could not resolve host: github.com
$ git ls-remote https://github.com/quoctran-2608/bodhi-atlas.git HEAD
fatal: unable to access 'https://github.com/quoctran-2608/bodhi-atlas.git/': Could not resolve host: github.com
$ python /tmp/p61/poc.py > /tmp/p61/log.txt 2>&1
```

Actual stdout/stderr combined (no secrets, synthetic only):

```text
corpus 5ce45bc1734cc0a5ef967a492df7a040a95b05249cef5c54dbbef6f49ddcc5dd
queries a62eae64bb9ffd4c6571f661fd0d6d266537bdabdc6b23d1d12084dbc4769183
qrels 94763964a16af6447d9c18258b9d31994cf98c864277ddf723432e1eac280489
run 412bfd38166c3f344c9976a9401adc42cb0040e3243c76a203b2729e55a93a4b
oracleB 89097e0c539f238f902acc13b204c380637a1302783b4489778f59d37e2a1309
metrics {"q1": [0.68853, 0.83333, 1.0, 0.66667, 1.0], "q2": [0.0, 0.0, 0.0, 0.0, 0], "q3": [0.0, 0.0, 0.0, 0.0, 0], "q4": [null, null, null, 0.0, null], "q5": [1.0, 1.0, 1.0, 0.33333, 1.0], "d1": [1.0, 1.0, 1.0, 0.33333, 1.0], "q7": [0.63093, 0.5, 1.0, 0.33333, 0.5], "q8": [0.61315, 0.5, 0.5, 0.33333, 1.0]}
macro_defined [0.5618, 0.54762, 0.64286, 0.25, 0.64286]
macro_missing_dropped [0.65543, 0.63889, 0.75, 0.28571, 0.75]
tie_asc_desc_at1 [1.0, 1.0, 1.0, 1.0, 1.0] [0.0, 0.0, 0.0, 0.0, 0]
per_query_unjudged 1
same_id_before_after 1 0
oracleA d462cc4416a5263aa86c8f6201f6722b3dc78680bfb74d9a6e35dbb63f8b4bee
exact 8 top1 5 FN 3 P/R 1.0 0.625
overlap_boundary OK (declared concatenation)
unicode NFC/NFD + CJK literal OK; Wylie not evaluated
adapter 12 snapshot 1cfa47847f3d1a1908045ccb3c6c2fd702fde926b72c92ff69c62185f347e3ef metrics unchanged True
env 3.13.5 3.46.1 Linux-6.18.57-x86_64-with-glibc2.41
installed {'beir': False, 'pytrec_eval': False, 'ir_measures': False, 'torch': True, 'tqdm': True, 'sentence_transformers': False, 'datasets': False, 'rapidfuzz': True}
PASS isolated assertions
```

### 13.3 Script tái lập đã chạy (TESTED-ISOLATED; không phải mã BEIR)

Copy code block sau thành `poc.py` rồi chạy Python. Dùng only stdlib, SQLite memory. Expected literal offsets và qrels định trước. q1 oracle ratio được gán công thức tính tay trước hàm metrics, không lấy output của evaluator làm expected. Các fixture có qid tiếng Anh mô tả edge cases chứ không phải truy vấn domain thật; `d6`–`d12` kiểm Unicode riêng. Không dùng làm training data hay chứng minh claim. Script output digest là content checksum của fixture, không phải SHA256 file sách. 

```python
import json, hashlib, math, sqlite3, unicodedata as u, platform, importlib.util
from statistics import mean
# Entire fixture synthetic; no religious claims about real sources.
docs={'d1':'x x x x x','d2':'x','d3':'x','d4':'not x','d5':'aaaa','d6':'anattā','d7':'anatta\u0304','d8':'đạo','d9':'dao','d10':'無常','d11':'无常','d12':'བོད bod'}
queries={'q1':'rank graded','q2':'missing','q3':'no hits','q4':'no positive','q5':'tie','d1':'self ID','q7':'unjudged','q8':'K larger than hits'}
qrels={'q1':{'d1':3,'d2':1,'d4':0},'q2':{'d3':1},'q3':{'d4':1},'q4':{'d5':0},'q5':{'d6':1,'d7':0},'d1':{'d1':1},'q7':{'d8':1},'q8':{'d10':1,'d11':1}}
run={'q1':{'d2':3,'d12':2,'d1':1},'q3':{},'q4':{'d5':1},'q5':{'d7':1,'d6':1},'d1':{'d1':1},'q7':{'d9':2,'d8':1},'q8':{'d10':1}}
# Frozen hand oracle before implementation; linear gain, binary rel>0, k=3, tie id asc.
expected={'q1': [0.68853, 0.83333, 1., 0.66667, 1.], 'q2':[0.,0.,0.,0.,0.], 'q3':[0.,0.,0.,0.,0.], 'q4':[None,None,None,0.,None], 'q5':[1.,1.,1.,0.33333,1.], 'd1':[1.,1.,1.,0.33333,1.], 'q7':[0.63093,0.5,1.,0.33333,0.5], 'q8':[0.61315,0.5,0.5,0.33333,1.]}
# q1: DCG=1+3/2=2.5; IDCG=3+1/log2(3); exact ratio below.
expected['q1'][0]=round(2.5/(3+1/math.log2(3)),5)
def digest(obj):return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
for name,obj in [('corpus',docs),('queries',queries),('qrels',qrels),('run',run),('oracleB',expected)]:print(name,digest(obj))
def metrics(rel, scores, k=3):
 hits=sorted(scores,key=lambda d:(-scores[d],d))[:k]; R=sum(v>0 for v in rel.values()); gains=[rel.get(d,0) for d in hits]; dcg=lambda g:sum(v/math.log2(i+2) for i,v in enumerate(g)); ideal=dcg(sorted(rel.values(),reverse=True)[:k]); pos=[i+1 for i,v in enumerate(gains) if v>0]; n=len(pos)
 vals=[dcg(gains)/ideal if ideal else None, sum(j/r for j,r in enumerate(pos,1))/min(R,k) if R else None,n/R if R else None,n/k,1/pos[0] if pos else (0 if R else None)]
 return [round(x,5) if x is not None else None for x in vals]
actual={q:metrics(rel,run.get(q,{})) for q,rel in qrels.items()}; print('metrics',json.dumps(actual));assert actual==expected
print('macro_defined', [round(mean(v[i] for v in actual.values() if v[i] is not None),5) for i in range(5)])
print('macro_missing_dropped', [round(mean(v[i] for q,v in actual.items() if q in run and v[i] is not None),5) for i in range(5)])
print('tie_asc_desc_at1',metrics(qrels['q5'],{'d6':2,'d7':1},1),metrics(qrels['q5'],{'d6':1,'d7':2},1)); print('per_query_unjudged',sum(d not in qrels['q7'] for d in run['q7']))
# Emulate only the observed dict overwrite and self filtering, not upstream import.
assert dict([('d1','old'),('d1','new')])=={'d1':'new'}; copy={q:dict(r) for q,r in run.items()};copy['d1'].pop('d1'); print('same_id_before_after',len(run['d1']),len(copy['d1']))
# Independent hand-annotated offsets, code point [start,end), one edition per file.
gold={('d1','A','r1',i,i+1) for i in (0,2,4,6,8)}|{('d2','A','r1',0,1),('d3','B','r1',0,1),('d4','B','r1',4,5)}
print('oracleA',digest(sorted(gold)))
con=sqlite3.connect(':memory:');con.execute('create table passage(id primary key, edition, rev, text)');con.executemany('insert into passage values(?,?,?,?)',[(d,'B' if d in ('d3','d4') else 'A','r1',t) for d,t in docs.items()])
def find(t,q):return [(i,i+len(q)) for i in range(len(t)) if t.startswith(q,i)]
actualA={(d,e,r,a,b) for d,e,r,t in con.execute('select * from passage') for a,b in find(t,'x')};assert actualA==gold
trunc={v for v in actualA if v[0]=='d1'};print('exact',len(actualA),'top1',len(trunc),'FN',len(gold-trunc),'P/R',1.,len(trunc)/len(gold))
assert find('aaaa','aa')==[(0,2),(1,3),(2,4)];assert find('ab'+'cd','bc')==[(1,3)]; print('overlap_boundary OK (declared concatenation)')
assert docs['d6']!=docs['d7'] and u.normalize('NFC',docs['d6'])==u.normalize('NFC',docs['d7']);assert docs['d8']!=docs['d9'];assert find(docs['d10'],'常')==[(1,2)];assert docs['d10']!=docs['d11'];print('unicode NFC/NFD + CJK literal OK; Wylie not evaluated')
# Adapter is read-only export from same fixture authority; stable key includes rev and edition.
mapping={d:(e,r,t) for d,e,r,t in con.execute('select * from passage')};export={d:{'title':'','text':t} for d,(e,r,t) in mapping.items()};assert set(export)==set(docs);assert all(d in export for rel in qrels.values() for d in rel);print('adapter',len(export),'snapshot',digest(mapping),'metrics unchanged',actual=={q:metrics(rel,run.get(q,{})) for q,rel in qrels.items()})
print('env',platform.python_version(),sqlite3.sqlite_version,platform.platform()); print('installed', {p:bool(importlib.util.find_spec(p)) for p in ['beir','pytrec_eval','ir_measures','torch','tqdm','sentence_transformers','datasets','rapidfuzz']})
print('PASS isolated assertions')
```

### 13.4 Bibliography / câu hỏi mở

- Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., Gurevych, I. (2021). *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models*. NeurIPS Datasets & Benchmarks. [Proceedings abstract](https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html), [arXiv](https://arxiv.org/abs/2104.08663). Abstract/metadata accessed; full paper not audited.
- Kamalloo et al. (2024). *Resources for Brewing BEIR: Reproducible Reference Models and an Official Leaderboard*, SIGIR. [DOI](https://doi.org/10.1145/3626772.3657862), citation from README; full paper not independently audited.
- [BEIR repository pinned](https://github.com/beir-cellar/beir/tree/ef83d29307061c65d04b035b4f4e7c18bd8374af), [PyPI](https://pypi.org/project/beir/), [issue #222](https://github.com/beir-cellar/beir/issues/222), [ir_measures docs](https://ir-measur.es/en/latest/). Backend source web open blocked; actual backend behavior remains native POC, not inferred as verified.
- [BodhiAtlas pinned docs and research](https://github.com/quoctran-2608/bodhi-atlas/tree/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e), links and ranges §2.

**Open questions / limitations:** Which ranked features actually need evaluation in V1? Which source snapshots and rights are available for private domain gold? Native pytrec backend versions/tie/gain/empty dict behavior? Can BCR resolver pass independent source opening across general book formats? How much reviewer time and CI resource cost? Does tag wheel differ from pinned source? Tests tree, release page, multilingual wiki and per-dataset terms, model license, full paper and native runtime remain incomplete. Only excerpts of older reports used, no new audit of all previous engines. No result from P59 presumed. No old P61 report supplied or found in the requested inventory; this report independently adds query-universe, self-ID and metric convention checks rather than reusing prior conclusions. Scope decision chosen without extra guidance: K=3, linear gain, undefined no-positive, codepoint offsets and synthetic data; these are explicit test conventions, not normative PRD changes. Track A required for EXACT/G2; whether D remains optimal after real benchmark is conditional.

**Self-check:** 13 sections, C01–C15, H01–H12, TC01–TC16, G1–G6 and T01–T16 mapping present; pinned code + evidence ledger; 0 upstream/integration runs; isolated output and reproduction script included; explicit blockers, rights unknown and rollback criteria. Full audit of test tree, native parity, public dataset terms and domain gold not completed; report is usable for master synthesis as conditional decision, not qualification for production. One deliverable Markdown, no repository changes.
