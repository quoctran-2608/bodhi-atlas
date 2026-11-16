# Technology Assessment — MinerU

- **Mã / ưu tiên:** P45 / P0. **Ngày khảo sát:** 2026-11-16 (Asia/Ho_Chi_Minh).
- **Đối tượng:** [opendatalab/MinerU](https://github.com/opendatalab/MinerU), repository public, **không archived** tại lúc kiểm tra; nhánh mặc định `master`.
- **Bản phát hành đối chiếu:** **4.2.2**, tag `mineru-4.2.2-released` (13/11/2026), commit tag trỏ tới `0621ddbab8bf85294d6bac101c0a6def843195d8`. **Snapshot mã đọc:** `master` commit `f0497e0c6e9575fa553ce57cc9aa867906a00572` (13/11/2026). Hai SHA được ghi riêng, **không coi HEAD và tag đồng nhất**. [Release](https://github.com/opendatalab/MinerU/releases/tag/mineru-4.2.2-released) · [Commit HEAD](https://github.com/opendatalab/MinerU/commit/f0497e0c6e9575fa553ce57cc9aa867906a00572).
- **Phân loại đã thẩm định:** `component` — bộ phân tích tài liệu/OCR/nhận diện bố cục và thư viện tài liệu phụ trợ; **không** phải scholarly source-of-truth, thư viện witness hay bộ máy kiểm chứng dẫn chứng hoàn chỉnh. Phân loại này độc lập với nhãn của đề bài.
- **Analyst/phương pháp:** thẩm định kỹ thuật độc lập bằng đọc trực tiếp GitHub (PRD, risk register, corpus hiện hữu, repository tree, README, docs, release, license, mã thực thi, tests và issues), kiểm tài liệu các đối thủ. Không clone/khởi chạy MinerU hoặc tải model/corpus trong môi trường báo cáo. **Trạng thái thực nghiệm: NOT TESTED.**
- **Chú giải bằng chứng:** `[DOC]` văn bản của dự án; `[CODE]` mã đọc trực tiếp; `[ISSUE]` phản ánh/chẩn đoán từ issue, chưa khẳng định tái hiện; `[INFERRED]` phân tích có căn cứ; `[UNKNOWN]` chưa đủ nguồn; `[TESTED]` chỉ dành cho thử nghiệm tự chạy với log, không có trường hợp nào được dùng cho MinerU trong báo cáo này. Link mã `@HEAD` được ghim theo SHA kể trên.

## 1. Executive Decision

**Quyết định: `TRIAL ONLY` ở V1**, với **đích tiềm năng `USE AS COMPONENT`** sau POC. **Confidence: MED** cho kết luận về khả năng tái sử dụng giao diện và kiến trúc; **LOW** cho kết quả OCR đa ngữ/source fidelity vì chưa chạy corpus thực.

1. **V1 Core:** thí điểm MinerU **Flash** cho PDF có text và tài liệu định dạng hỗ trợ, **Basic** cho OCR offline, **Standard/Advanced** cho trang phức tạp được chọn. Tiếp nhận **Middle JSON + sidecar** vào adapter riêng; giữ PDF/EPUB/TEI gốc và `sha256` của BodhiAtlas làm thẩm quyền. Nếu chất lượng tốt, nâng thành thành phần ingest có điều kiện; không dùng Markdown làm hệ tọa độ nguồn duy nhất.
2. **V2:** lựa chọn dùng MinerU làm preprocessor sinh ứng viên đoạn/bố cục phục vụ học thuật/RAG, nhưng trích dẫn phải qua Source Reopen + Citation Verifier độc lập. Không thay thế hệ thống tra cứu và kiểm chứng sẵn có của `BuddhismDocuments-for-AI`.
3. **V3:** có thể dùng Router/API và quy trình phân tích tài liệu quy mô lớn **chỉ khi** khối lượng thực tế, chi phí, quyền dữ liệu và hoạt động có kiểm soát chứng minh được nhu cầu. Không chốt từ bây giờ.

**Ba rủi ro lớn nhất, không được bù bằng điểm benchmark tổng:**

- **R01/R04 — sai văn bản hoặc mất đường quay lại nguồn.** Middle JSON 2.0 có `page_idx`, bbox block và `continues_prev`, nhưng không mặc định có vị trí **từng ký tự** hoặc ID bất biến qua lần parse; OCR/VLM có thể làm sai phủ định, dấu phụ, chữ số, chữ ghép. Issue [#5705](https://github.com/opendatalab/MinerU/issues/5705), [#5517](https://github.com/opendatalab/MinerU/issues/5517), [#5465](https://github.com/opendatalab/MinerU/issues/5465) chỉ là tín hiệu để lập test, không phải bằng chứng lỗi vẫn có ở 4.2.2.
- **R07/R08 — nhầm tìm ứng viên với EXACT.** Doclib FTS5 hiện cắt text dài về **tối đa 30.000 ký tự (15.000 đầu + 15.000 cuối)**, dùng FTS token, mặc định tối đa **200** ứng viên nội bộ; không vét đủ các occurrence, không bảo toàn dấu câu như so khớp ký tự. **Không được dùng Doclib Search làm `CODE_ONLY_EXACT`.** [CODE: fts.py L73–90, L144–176](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/core/fts.py#L73-L90); [parse_execution_svc.py L475–491](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/services/parse_execution_svc.py#L475-L491).
- **R26/R27 — hợp đồng quyền và thay đổi hệ.** `LICENSE.md` là **MinerU Open Source License có điều khoản bổ sung**, không phải Apache 2.0 thuần; trọng số model/third-party và quyền văn bản/ảnh nguồn phải kiểm riêng. Doclib không phải kho catalog học thuật độc lập với parser; nếu lấy ID block hoặc chunk làm khóa chứng cứ sẽ dễ gãy sau reparse.

**Gate sơ bộ:** `SOURCE_FIDELITY=unknown`, `CODE_ONLY_EXACT=n/a` **khi xét đúng vai trò parser** (*fail nếu đề xuất Doclib thay máy tìm exact*), `MULTILINGUAL=unknown`, `OCR_COVERAGE=unknown`, `QUALITY_COVERAGE=unknown`, `RIGHTS_SECURITY=unknown` (cần threat model và kiểm license), `PORTABILITY=partial/conditional`. **Chưa đạt điều kiện ADOPT.**

**Nguồn quy chuẩn đã thực đọc:** [PRD V1.4](https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/PRD.md), [ACADEMIC_RISKS_AND_VERIFICATION](https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/ACADEMIC_RISKS_AND_VERIFICATION.md), [BuddhismDocuments-for-AI](https://github.com/quoctran-2608/BuddhismDocuments-for-AI) (README + manifest). PRD yêu cầu nguyên văn, file/ấn bản riêng, SHA-256, `EXACT/NORMALIZED/FUZZY/LEXICON`, vị trí nguồn xác minh được; risk register có G1–G6 và R01/R03/R04/R07/R09/R27. Tài sản hiện có đã có SQLite/FTS và resolver cho Bilara/CBETA/84000, nên **tránh xây trùng**.

## 2. Sources & Evidence Ledger

**Mốc đối chiếu code:** `H=f0497e0c6e9575fa553ce57cc9aa867906a00572` (master 13/11/2026); `T=0621ddbab8bf85294d6bac101c0a6def843195d8` (tag 4.2.2). Các path `github.com/.../blob/H/...` trong bảng là permalink thực đến SHA, không phải link động `master`. Tuyên bố hãng về chất lượng hoặc tốc độ **không** được gọi `[TESTED]`.

| claim_id | claim | Type | URL/file+line | version/SHA | note |
|---|---|---|---|---|---|
| M01 | Repo public, `master`, không archived; 4.2.2 phát hành 13/11 | `[DOC]` | [repo](https://github.com/opendatalab/MinerU), [release 4.2.2](https://github.com/opendatalab/MinerU/releases/tag/mineru-4.2.2-released) | H/T | Metadata và release chính thức |
| M02 | MinerU 4.x phân cấp `flash/basic/standard/advanced`, không còn xem pipeline/hybrid/vlm là tên tier | `[DOC][CODE]` | [tiers](https://opendatalab.github.io/MinerU/usage/tiers/), [types.py L87–105](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/types.py#L87-L105) | H | Không so các tier như bốn model khác nhau |
| M03 | PDF xử lý `auto/txt/ocr`, auto gọi classify; không đảm bảo `auto` luôn chọn đúng | `[CODE]` | [pdf/pipeline.py L44–62](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/backend/analysis/pdf/pipeline.py#L44-L62) | H | Cần thử text layer che/ẩn |
| M04 | API phân tích có PDF/EPUB/HTML/OFD/Office, `page_index_map` chỉ cho PDF | `[CODE]` | [backend/analyze.py L32–85, L144–151](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/backend/analyze.py#L32-L85) | H | Không suy ra EPUB CFI |
| M05 | Tầng schema và postprocess đến từ phụ thuộc DocVortex; `MiddleJson` re-export | `[CODE]` | [types.py L6–85](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/types.py#L6-L85), [document.py L5–23](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/backend/postprocess/document.py#L5-L23) | H | Phải pin cả `docvortex`, không chỉ MinerU |
| M06 | Middle JSON `docvortex.middle` schema 2.0, metadata producer, page index, block index và PDF bbox chuẩn hóa [0,1] | `[DOC]` | [current-medium.md L9–51](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/docs/next/middle-json/current-medium.md#L9-L51), [output format](https://opendatalab.github.io/MinerU/reference/output_files/) | H | PDF geometry extension có page width/height pt |
| M07 | `TextSpan` giữ text và style, không định nghĩa tọa độ/score từng ký tự trong giao diện InlineSpan | `[DOC]` | [current-medium.md L53–105](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/docs/next/middle-json/current-medium.md#L53-L105) | H | Không gọi bbox block là char-accurate |
| M08 | Chỉ top-level `text/ref_text/list/table` có `continues_prev`; có link khối tiếp trang nhưng không phải provenance bất biến | `[DOC]` | [current-medium.md L94–107](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/docs/next/middle-json/current-medium.md#L94-L107) | H | Kiểm tra nối đoạn khi export |
| M09 | CLI `mineru-kit parse` có `markdown/middle_json/zip`, `--ocr-mode`, tier; local mặc định Standard cho PDF | `[CODE]` | [kit/commands/parse.py L32–55, L87–106](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/kit/commands/parse.py#L32-L106) | H | `mineru parse --json` là **response** khác Middle JSON |
| M10 | `ParseResult.save()` lưu `middle_json.json`, `structured_content.json`, Markdown, images; JSON standalone chưa chứa image asset đầy đủ | `[DOC]` | [output_files](https://opendatalab.github.io/MinerU/reference/output_files/) | 4.x | Phải lưu ZIP/sidecars hoặc source crops |
| M11 | `doclib/locators.py` dùng `doc:<short_id>/tier:<tier>/page:<1-based>/block:<1-based>/char:<offset>` | `[CODE]` | [locators.py L10–61](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/locators.py#L10-L61) | H | Offset là cursor ở text đọc, không chứng minh bbox ký tự |
| M12 | Doclib sử dụng SHA-256 và SQLite FTS5, tách docs/files/parses | `[CODE]` | [001_init.sql L5–63, L93–106](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/migrations/001_init.sql#L5-L106) | H | Có giá trị cho cache nhưng không thay model work/edition |
| M13 | FTS lấy Markdown đã render rồi index, không trực tiếp index nguyên văn từng Span | `[CODE]` | [parse_execution_svc.py L234–247](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/services/parse_execution_svc.py#L234-L247) | H | Hiện diện biến đổi renderer, dấu câu/style |
| M14 | FTS cắt text giữa tài liệu >30k ký tự và chỉ giữ đầu/cuối | `[CODE]` | [fts.py L168–176](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/core/fts.py#L168-L176), [parse_execution_svc.py L475–491](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/services/parse_execution_svc.py#L475-L491) | H | **Blocker để dùng Doclib làm exact toàn văn** |
| M15 | FTS tokenization `jieba`, SQLite `unicode61`, MATCH xếp rank LIMIT 200; không phrase exact từng ký tự | `[CODE]` | [fts.py L23–34, L73–90, L144–165](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/core/fts.py#L23-L165), [search_svc.py L29–48](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/doclib/services/search_svc.py#L29-L48) | H | `total_count` của kết quả rút gọn, không phải exhaustive occurrences |
| M16 | `txt_spans_extract()` dùng char PDF gốc và fallback post-OCR trong một số tình huống | `[CODE]` | [text/native.py L74–98, L186–204](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/backend/analysis/pdf/text/native.py#L74-L204) | H | Không khẳng định always lossless |
| M17 | OCR giữ score nội bộ và có lọc text thấp confidence, khác trạng thái verification học thuật | `[CODE]` | [pdf/ocr.py L175–205](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/backend/analysis/pdf/ocr.py#L175-L205) | H | Không có CER thực đo từ score |
| M18 | Model 4.x Basic dùng PP-DocLayoutV2, PP-OCRv6 Small Rec, FormulaNet, table; Standard thêm VLM | `[CODE][DOC]` | [model/registry.py L23–57](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/model/registry.py#L23-L57), [model-assets](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/docs/next/model-assets.md#L54-L64) | H | Nhận dạng từng ngôn ngữ chưa thử |
| M19 | Tải/verify model và dùng source=`local`; khả năng offline có điều kiện | `[DOC]` | [Model Source](https://opendatalab.github.io/MinerU/usage/model_source/) | 4.x | Phải prefetch đủ weights; remote VLM là nhánh khác |
| M20 | Python 3.11–3.14, dependencies chính `docvortex`, ONNX, optional Torch/vLLM | `[CODE]` | [pyproject.toml L5–12, L40–112](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/pyproject.toml#L5-L112) | H | Không dùng hướng dẫn 2.x để cài 4.x |
| M21 | Code license thêm ngưỡng MAU/doanh thu và attribution dịch vụ online | `[DOC]` | [LICENSE.md L1–25](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/LICENSE.md#L1-L25) | H | Soát pháp lý riêng khỏi model và data |
| M22 | Test tồn tại cho locator, scan text routing, PDF footnote, CJK punctuation | `[CODE]` | [tests/locators](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/tests/unittest/test_doclib_locators.py), [tests/scan](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/tests/unittest/test_pdf_scan_text_routing.py), [tests/footnote](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/tests/unittest/test_pdf_footnote_layout.py) | H | Test files **không** phải `[TESTED]` của khảo sát |
| M23 | Có issue báo nhầm reading order, mất chữ số/ligature, ưu tiên nguồn PDF | `[ISSUE]` | [#5628](https://github.com/opendatalab/MinerU/issues/5628), [#5517](https://github.com/opendatalab/MinerU/issues/5517), [#5465](https://github.com/opendatalab/MinerU/issues/5465), [#5705](https://github.com/opendatalab/MinerU/issues/5705) | nhiều version | Phải xác minh lại 4.2.2, không coi issue = lỗi hiện hành |
| M24 | BodhiAtlas yêu cầu original file hash, edition/witness, source reopen; index không là chứng cứ | `[DOC]` | [PRD](https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/PRD.md#L227-L250), [Risks](https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/ACADEMIC_RISKS_AND_VERIFICATION.md#L18-L25) | PRD V1.4 | Quy tắc chặn lựa chọn engine |
| M25 | Repo corpus sẵn có 13 upstream pin; SQLite/FTS dẫn xuất, resolver Bilara/CBETA/84000 | `[DOC]` | [README L7–41](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/main/README.md#L7-L41), [manifest](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/main/manifest.json) | đọc 16/11 | Không đưa bản scan thay chứng tích TEI gốc |
| M26 | Chỉ thấy khả năng hỗ trợ OCR đa ngữ ở upstream; không có golden CER riêng Pāli/Tạng trong lần đọc này | `[UNKNOWN]` | [PaddleOCR model version/lang](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/OCR.en.md), [MinerU model registry](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/model/registry.py) | H | Không suy từ nhãn “109 languages” |

**Giới hạn phương pháp:** đã đọc trực tiếp ít nhất `backend/analyze.py`, `pdf/pipeline.py`, `pdf/ocr.py`, `pdf/text/native.py`, `postprocess/document.py`, `doclib/core/fts.py`, `doclib/services/search_svc.py`, `doclib/locators.py`, `doclib/services/parse_execution_svc.py`, `model/registry.py`, `kit/commands/parse.py`, schema SQL và một số test. **Chưa** audit hết 300+ test, mã của dependency `docvortex` hoặc các weight; không kiểm được hành vi thực bằng cách đọc code đơn lẻ.

## 3. Architecture & Data Flow

### Kiến trúc phần MinerU 4.x đã đối chiếu

```mermaid
flowchart TD
 A[PDF / scan / Office / EPUB / image / HTML] --> B[MinerU parser / CLI / SDK / API]
 B --> C{tier + parse_mode}
 C -->|Flash| D[DocVortex native reader / native PDF text]
 C -->|Basic| E[ONNX or Torch small models: layout OCR formula table]
 C -->|Standard/Advanced| F[Small models + VLM local/remote]
 D --> G[ModelJson analysis (internal)]
 E --> G
 F --> G
 G --> H[DocVortex deterministic postprocess]
 H --> I[MiddleJson v2.0: pages blocks bbox content]
 I --> J[Optional LLM-aided postprocess]
 J --> K[ParseResult renderers]
 K --> L[Markdown / structured content / Middle JSON / assets]
 K --> M[Optional Doclib: cache SQLite + FTS5 + cursors]
 L --> N[BodhiAtlas canonical extraction adapter]
 N --> O[Verified source map + independent original-file reopen]
 O --> P[Exact/normalized/lexicon indexes + research evidence]
```

**Trật tự phụ thuộc:** DocVortex sở hữu schema, parser native, hậu xử lý tất định và renderers; MinerU bổ sung mô hình OCR/layout/VLM, quản lý tier, CLI/API/Doclib ([architecture.md](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/docs/next/architecture.md#L6-L40)). Sơ đồ thể hiện đường đi khái niệm; tên **Flash/Basic/Standard/Advanced** là lựa chọn sản phẩm, `txt/ocr` là parse mode, ONNX/Torch và VLM engine là biến cấu hình độc lập. `ModelJson` không phải export tiêu chuẩn cho người dùng; `MiddleJson` mới là interface cần thử. Công đoạn hậu xử lý LLM **tùy chọn**, không được bật vô thức trong đường tạo nguồn tham chiếu.

**Ranh giới BodhiAtlas:** `[OriginalSource(work_id, edition_id, file_id, sha256)] → [ExtractionRun(version, config, model hashes)] → [PassageRevisions + source locator regions] → [independent verifier] → [FTS/exact/lexicon/search & citation cards]`. Bảng work/edition/witness, quyền nội dung, verification riêng text/location/meaning và note/claim memory **không lấy từ MinerU**. Corpus TEI/JSON/TMX đã có nên ưu tiên native upstream hơn OCR.

## 4. Feature Fit–Gap Matrix

*Quy ước:* `NATIVE` sẵn có trong scope MinerU, `CONFIG` cấu hình được, `EXTENSION` cần viết adapter, `EXTERNAL` do hệ khác làm, `MISSING` xác định thiếu, `UNKNOWN` chưa đủ chứng cứ, `N/A` ngoài nhiệm vụ parser. **N/A không bị trừ điểm**. “Mức công sức” là ước lượng định tính, chưa đo giờ công.

| ID | Capability | Status / vai trò chính | Bằng chứng | Gap và công việc BodhiAtlas | Công sức |
|---|---|---|---|---|---|
| C01 | Multi-format ingest | `NATIVE` cho PDF, ảnh, EPUB, DOCX, HTML...; `EXTERNAL` TEI/XML và Markdown gốc | M04, M09, [tiers](https://opendatalab.github.io/MinerU/usage/tiers/) | Adapter routing theo MIME + hash; TEI/Bilara/TMX direct parser, không ép sang PDF/OCR; Markdown lưu gốc và parse riêng | Medium |
| C02 | OCR/layout/reading order | `NATIVE` model-assisted; `CONFIG` 4 tier | M02–M03, M16–M18, M23 | Chạy fixtures cột/cước chú/Hán-Pāli/Tạng; kiểm thiếu phủ định, confidence và sequence | High |
| C03 | Canonical text/source map | `EXTENSION` (có Middle JSON/bbox nhưng canonical riêng) | M05–M08 | Chuyển block/span→passage + region; conversion page0→PDF page1; giữ config+revision và đối chiếu nguồn | High |
| C04 | Works/editions/witnesses | `EXTERNAL` | M12, M24–M25 | Catalog BodhiAtlas lưu work/translation/edition/witness/file riêng; SHA không nói tương đương bản | Medium |
| C05 | Exhaustive EXACT | `N/A` đối với parser; **Doclib FTS không đáp ứng** | M13–M15 | Exact engine code-only riêng, ALL occurrences + boundary crossing + byte/codepoint policy, không LIMIT 200 hay cắt giữa | High |
| C06 | Normalized multilingual search | `EXTERNAL` | M15, M24 | Side indices NFC/NFD, Việt bỏ dấu, Hán giản/phồn có rule, Wylie; không sửa text gốc | Medium–High |
| C07 | Fuzzy/near-duplicate/OCR errors | `EXTERNAL` | M23–M24 | Levenshtein/trigram candidate retrieval; audit diff; không gắn nhãn verified | Medium |
| C08 | Sense-aware lexicon | `EXTERNAL` | M24–M25 | Glossary theo nghĩa/ngôn ngữ/nguồn, không tự bắc cầu các từ dịch | High |
| C09 | Semantic/hybrid/RAG | `EXTERNAL`; Markdown là nguồn phục vụ RAG | M09–M10 | Định vị từ canonical passages, vector index tùy chọn sau code-only search | Medium |
| C10 | Verified citation card/source reopen | `EXTENSION` — chỉ có locator/geometry candidate | M06–M08, M11, M24 | Independent reopen file SHA/edition, compare text, PDF region multi-page, 3 trạng thái verify | High |
| C11 | Note/wiki/claim memory | `EXTERNAL` | M25 | Dùng hệ claim memory/corpus 2.0 hiện hữu; không gắn vào block index MinerU | Medium |
| C12 | API/MCP/export | `NATIVE` CLI/SDK/API/ZIP; MCP/docs cần test phiên triển khai | M09–M10, M20 | API auth, output version pin, packaging sidecars, contract error, rate limit; không giả định mỗi entrypoint xuất mọi format | Medium |
| C13 | Quality coverage + incremental | `EXTENSION` trên parser, cache `NATIVE` ở Doclib | M12–M14, M17 | Lưu page-level error, unreadable region, coverage %, drift/reindex; reload previous extraction khi fail | High |
| C14 | Auth/licensing/privacy/backup | `CONFIG` và `EXTERNAL` governance | M20–M21, M24 | Audit token/API, telemetry, third-party weights, permissions local-cloud, archive raw + restore; legal review | High |
| C15 | Operational simplicity + independent deploy | `CONFIG` (local Flash/Basic; multi-service optional) | M02, M19–M20 | Chạy version-pinned service nhỏ trước; pin model hashes; máy chủ VLM tăng complexity, giữ parser stateless | Medium–High |

**Gates không đánh đổi:** `SOURCE_FIDELITY` chưa pass; `CODE_ONLY_EXACT` là **N/A ở scope parser**, còn **fail với chức năng Doclib Search nếu đem thay search lõi**; `MULTILINGUAL` và `QUALITY_COVERAGE` chưa có đo trên corpus; `RIGHTS_SECURITY` cần audit; `PORTABILITY` chỉ đạt nếu BodhiAtlas sở hữu raw files, IDs, revisions và verified evidence riêng khỏi MinerU.

## 5. Deep Technical Findings

### 5.1. Pipeline, OCR, layout, reading order, bảng, công thức, ngôn ngữ

**[CODE/DOC]** MinerU 4.2.2 cung cấp tier `flash` (native reader/preview và OCR nhẹ theo loại tài liệu), `basic` (small models ONNX/Torch), `standard` (small models + VLM), `advanced` (cùng bộ model với standard nhưng inference nhiều hơn). Code có `doc_analyze`/`aio_doc_analyze` trong `mineru/backend/analyze.py`; `PDFDocument.classify()` quyết định `txt` hoặc `ocr` khi `auto` tại `backend/analysis/pdf/pipeline.py`; các bước `pdf/layout.py`, `ocr.py`, `text/native.py`, `formulas.py`, `tables.py`, `window.py` xử lý theo trang/window; `backend/postprocess/document.py` gọi DocVortex cho Middle JSON. Engine ONNX, Torch, llama.cpp, vLLM, LMDeploy/MLX có đường triển khai khác nhau; remote VLM không đồng nghĩa cloud tự gửi trong local mode. Không còn đồng nhất “pipeline/hybrid/vlm” của 3.x với API tier 4.x. Nguồn: M02–M05, M16–M20.

**[INFERRED]** Đọc các module cho thấy nhận diện layout và postprocess có thể sắp thứ tự đọc tốt hơn trích text thô trong PDF phức tạp, nhưng **không chứng minh** chính xác trên sách kinh/luận đa ngôn ngữ. Cần đo riêng order, thành phần bảng và footnote link.

### 5.2. JSON: IDs, pages, bbox, offsets, order, confidence

**[DOC/CODE]** Output `middle_json.json` dùng `schema: docvortex.middle`, `schema_version: "2.0"`, `metadata.producer.{name,version}`, `extensions.mineru.{tier,parse_mode}`, `pages[]` có **`page_idx` 0-based**, `blocks[]` có `index` và `type`, `content` thường là `InlineSpan[]`. PDF block ngoài cùng có **bbox `[0,1]`**, extension `docvortex_layout` có `page_idx`, `width_pt`, `height_pt` và thông tin xoay khi có. `text` span giữ string và style, nhưng public `InlineSpan` không quy định **char/glyph bbox**, confidence từng ký tự hay stable global block UUID. `page_idx + index` chỉ định vị một **bản parse**, không là ID lâu bền qua phiên bản. [current-medium](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/docs/next/middle-json/current-medium.md), [output specs](https://opendatalab.github.io/MinerU/reference/output_files/).

`doclib` có cursor `doc:shortid/tier:standard/page:1/block:3/char:0` — **char offset trong kết quả render**, không đảm bảo ánh xạ chính xác tới ảnh chữ gốc; nhận diện title/footnote/table được biểu diễn thành các block type, nhưng liên kết tham chiếu footnote→callout không thể coi sẵn sàng nếu chưa test. `--format middle_json` hoặc `zip` phù hợp thử nghiệm; `mineru parse --json` là response CLI khác kiểu, **không đem đọc như MiddleJson**. Giữ sidecars của images; JSON không đủ tự mang mọi ảnh.

### 5.3. PDF text vs scan; chọn route và giữ nguyên

- **[CODE]** `auto` dùng `PDFDocument.classify()`, `txt` ưu tiên PDF text layer và có post-OCR fallback cho span rỗng/không dùng được; `ocr` ép hướng OCR. [pipeline.py L44–62](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/backend/analysis/pdf/pipeline.py#L44-L62), [native.py L74–204](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/backend/analysis/pdf/text/native.py#L74-L204).
- **[INFERRED]** Có thể **bypass mô hình** với `--tier flash --ocr-mode txt` khi PDF text sạch; song không đồng nghĩa bảo toàn *byte-for-byte* Unicode gốc từ PDF, do ligature, encoding, khoảng trắng/reading order có thể biến đổi. Cần lưu text-layer baseline riêng (PDF words/rawdict) và so với output. Không chạy OCR lại bừa bãi trên text layer tốt; route theo **page/region** nếu classifier sai.
- **[ISSUE]** #5705 nêu chênh text layer với model và provenance; #5517 mất số trong mixed-font; #5465 ligature. Các issue là vật liệu tạo golden fixtures, **không phải xác nhận lỗi hiện tại**.

### 5.4. Ngôn ngữ và license model theo phiên bản

**[CODE]** Model registry của MinerU 4.x liệt kê `PP-DocLayoutV2`, `ch_PP-OCRv6_tiny_det`, `ch_PP-OCRv6_small_rec`, mô hình seal, công thức/bảng; không có “model riêng Tạng/Pāli” được chứng minh trong lần audit. [registry.py](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/mineru/model/registry.py#L23-L57). Upstream PaddleOCR nêu `vi` trong một số cấu hình PP-OCRv6, `pi` trong PP-OCRv5, **nhưng điều đó không xác nhận bundle cụ thể của MinerU 4.2.2 đạt CER nào**. Không thấy kiểm chứng kỹ thuật chữ Tạng Tibetan/Wylie trong output model MinerU đã đọc. [PaddleOCR language matrix](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/OCR.en.md).

Đối với **PDF có text sạch**, tiếng Việt/Pāli/Sanskrit/Hán/Tạng *có thể* đi theo Unicode text layer mà không cần OCR, với rủi ro map ký tự/ligature/combining marks. Với **scan**, tất cả phải test theo script và loại dấu: `anatta/anattā/anātman`, `dukkha/duḥkha`, `vô ngã/vo nga`, `無我`, `無常/无常`, Tạng Unicode và Wylie. Cần phân biệt model detector với recognizer và VLM, phiên bản/model hash; không công bố “109 ngôn ngữ nên hỗ trợ Tạng/Pāli”. **Kết luận multi-script: UNKNOWN cho gate chất lượng**.

### 5.5. Bảng, chú thích, nhiều cột, chữ nghiêng/subscript, reading order

**[CODE/DOC]** Middle JSON có `table`, `table_body`, caption/footnote, `page_footnote`, style `italic/superscript/subscript`, `continues_prev`; renderer có thể tạo table HTML, công thức LaTeX. Native spans có xử lý script role/ligature và box geometry; tests `test_pdf_footnote_layout.py`, `test_pdf_native_cjk_quote_span_edge.py`, `test_pdf_native_script_detection.py` thể hiện quan tâm regression. [current-medium L70–137](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/docs/next/middle-json/current-medium.md#L70-L137).

**Failure modes phải đo:** nhảy cột trái→phải sai thứ tự, đọc footnote lẫn body, dấu gọi footnote trôi, bảng bị nối ô/row-span sai, chữ phủ định/ni/不/無/མ་ mất, dấu Pāli bị bỏ, chữ italic bị chuyển sai emphasis, subscript/ligature mất chữ, đoạn nối across page bị đảo thứ tự, table cell/figure OCR sinh text ngoài trang. Issue [#5628](https://github.com/opendatalab/MinerU/issues/5628) mô tả title bị đặt sau body trong tier Basic; chưa xác nhận còn ở bản mới.

### 5.6. Crossing pages, chunking, footnotes

**[DOC]** `continues_prev` gắn ở top-level `text/ref_text/list/table`, có thể giữ trang gốc/bbox khi postprocess nối đoạn và bảng qua trang. **Không** đồng nghĩa có hệ thống “canonical paragraph across pages” hoặc stable graph từ marker gọi footnote sang nội dung footnote. Chuyển các block source thành `passage` của BodhiAtlas cần *join graph* riêng: `segments[{page_idx, block_index, bbox, char_range_in_extracted_text}]` và `next/prev` dựa trên evidence, không dùng một bbox giả cho đoạn 2 trang.

### 5.7. Máy chạy offline, tính năng VLM, tài nguyên

**[DOC]** Model source `local` dùng cache và báo thiếu nếu model chưa có; có lệnh `models download`, `verify`, `show`, có engine ONNX CPU ở Basic; Standard/Advanced với VLM đòi thêm hệ thống. 4.x đề xuất khoảng **16 GB RAM** khi triển khai cục bộ throughput cao và **8 GB VRAM chỉ là mức khởi đầu tham khảo, không bảo đảm**; CPU 4–11 logical cores tự đề nghị Basic, >=12 có thể Standard, GPU cho các tier cao tùy điều kiện; cần đo phần cứng thật. [tiers](https://opendatalab.github.io/MinerU/usage/tiers/) · [models](https://opendatalab.github.io/MinerU/usage/model_source/).

**[DOC/CODE]** Có `LLMAidedConfig` với postprocess enhancement tùy bật, và VLM cho inference. Bất kỳ text output từ VLM/LLM phải coi là **hypothesis of transcription**, không là *verified source*. Score OCR nội bộ không tương đương xác suất câu chữ/định vị đúng. Không thấy cơ chế independent double-pass verify image-to-text được chứng minh toàn diện trong dữ liệu đã đọc: `UNKNOWN`.

### 5.8. Chuyển JSON vào canonical passage và quản lý revision

**Đề xuất contract v0.1 — thiết kế BodhiAtlas, không phải schema có sẵn của MinerU:**

```json
{
  "file_id": "file:<uuid>",
  "source_sha256": "<64-lowercase-hex>",
  "work_id": "work:<uuid>",
  "edition_id": "edition:<uuid>",
  "witness_id": "witness:<uuid-or-null>",
  "extraction_run_id": "run:<uuid>",
  "parser": {"name": "MinerU", "version": "4.2.2", "commit": "<pinned-sha>", "docvortex": "<pinned-version>", "tier": "basic", "parse_mode": "ocr", "model_digests": []},
  "passage_id": "passage:<uuid>",
  "passage_revision": 1,
  "source_text": "<extracted-text-unverified>",
  "segments": [
    {"pdf_page_index_0": 12, "pdf_page_no_1": 13, "block_index": 4,
     "bbox_norm_xyxy": [0.12, 0.23, 0.85, 0.32],
     "pdf_geometry": {"width_pt": 595, "height_pt": 842, "rotation": 0},
     "char_start_in_passage": 0, "char_end_in_passage": 28}
  ],
  "printed_page": null,
  "quality": {"coverage_status": "OCR_UNCERTAIN", "ocr_score": null},
  "verification": {"text": "UNVERIFIED", "locator": "UNVERIFIED", "meaning": "NOT_ASSESSED"}
}
```

Ví dụ trên là **shape và số giả định minh họa contract**, **không phải trích từ file có thật, không được dùng làm citation card thực**. `passage_id` là khóa BodhiAtlas, không phát sinh bằng hash block/index. Lưu extraction-run manifest, output thô Middle JSON, `page_index_map`, model hashes, normalized canonical string và character diff. Khi chạy MinerU version/tier khác: **không update đè**, tạo revision mới; map old→new theo file SHA + text spans + vùng; nếu locator đổi/không khớp thì hạ `MISMATCH` và rollback phiên trích dẫn đã duyệt.

### 5.9. Thẩm định chỉ số, failure detection

Bảng đo phải song song Docling/Marker, không chỉ tin OmniDocBench do nhà phát triển công bố. Với nguồn scan: `CER/WER` theo Unicode code point và grapheme cluster; báo riêng dấu Pāli/Viet/Tạng, mất phủ định. Với layout: reading-order pairwise accuracy, footnote-callout linking, table cell accuracy, **locator success trên cả những vùng sai**, version-diff. Với retrieval: `EXACT_FULL_RECALL` trên **index của BodhiAtlas** chứ không gán cho MinerU; `FALSE_VERIFIED_CITATION` phải bằng 0 trong sample nghiệm thu verified. Tách benchmark parse và benchmark tìm kiếm.

### 5.10. Phần thiếu chắc chắn

Không có bằng chứng trong khảo sát cho: stable EPUB CFI/href từ Middle JSON; PDF printed-page inference đáng tin; calibrated confidence cho từng grapheme; tự động bắt mất phủ định; chuẩn hoá Hán giản/phồn, Wylie và lexicon theo nghĩa; so khớp chính xác xuyên block và vét mọi occurrence; policy bản quyền từng ấn bản; tự động gắn verification text/location/meaning. **Để `UNKNOWN` nếu là năng lực parser chưa chứng minh, `EXTERNAL/N/A` nếu nằm ngoài nhiệm vụ**.

## 6. Source Fidelity & Provenance

### Yêu cầu bất biến và đường kiểm chứng

- **Original:** BodhiAtlas lưu raw bytes bất biến, `file_id` + `sha256`, loại file, MIME, bản quyền, nguồn tiếp nhận, `work_id/edition_id/translation_id/witness_id`; đánh dấu mối quan hệ `translation_of`, `parallel_to`, `variant_of`, `commentary_on` nhưng không hòa làm một.
- **Extraction:** một `extraction_run` cho mỗi tập `MinerU version/commit + docvortex version + tier + parse_mode + model digests + config + input SHA`; giữ `middle_json.json` và ảnh sidecar, không chỉ MD. Mỗi segment lưu `page_idx` 0-based, `bbox` normalized, PDF geometry, rotation, order/index và char-offset trong canonical text. **Không suy ra vị trí glyph chính xác từ bbox block**.
- **Independent reopen:** khi người dùng chọn câu trích, tái kiểm hash file và edition; mở PDF page `page_idx+1`, vẽ lại bbox chuyển `[0,1]`→`point`, bảo đảm rotation; với nguồn không phải PDF cần path/href/CFI/canonical locator thật. Nạp lại vùng PDF/text layer hoặc xem ảnh crop; nếu OCR rủi ro, thẩm định người đọc trước khi verified. Trang in chỉ nhận khi có `printed_page_evidence`, không tính bù trang bìa bằng đoán.
- **Verification tách ba chiều:** `text_status` (`TEXT_MATCHED`, `OCR_NEEDS_REVIEW`, `MISMATCH`, ...), `locator_status` (`REOPEN_VERIFIED`, `REGION_AMBIGUOUS`, ...), `meaning_status` (`NOT_ASSESSED`, `ASSESSED`, ...). **`text+locator verified` không suy ra ý nghĩa, mức hỗ trợ lập luận hoặc sự kiện lịch sử đúng.**
- **Coverage:** ghi `READY/PARTIAL/OCR_UNCERTAIN/NOT_INDEXED/SOURCE_UNAVAILABLE`, lỗi theo trang, vùng rỗng, failed output, skipped/timeout; không kết luận “không có chứng cứ” khi phần giữa chỉ mục bị bỏ hoặc OCR chưa đủ tin cậy.

**Các cạm bẫy cụ thể:** (a) chuyển Markdown có thể gộp trang/cột và mất tọa độ; (b) `page_idx` khác trang sách in; (c) một đoạn across pages có nhiều box; (d) `block.index` có thể thay khi reading order/model update; (e) marker `...` trong FTS không phải văn bản đầy đủ; (f) trích *nguyên văn OCR* vẫn là bản trích xuất có rủi ro; (g) cùng SHA chỉ là cùng bytes, khác SHA chưa chắc khác tác phẩm; (h) output với JSON không kèm ảnh không đầy đủ nếu cần hiển thị crop; (i) Doclib cursor có `char_offset` trong kết quả nhưng không thay thế source coordinate system.

**Gates đề xuất dùng trong POC (mục tiêu chính sách, không phải số đo):** 100% **các citation được gắn `TEXT_AND_LOCATOR_VERIFIED`** phải tái mở đúng file+ấn bản+vị trí và đối chiếu đúng câu chữ; **0** trường hợp false verified trong golden set. Những phần thấp hơn vẫn có thể được hiển thị với nhãn *candidate / unverified*, không để mất dữ liệu.

## 7. Multilingual & Retrieval Behavior

| Trường hợp | MinerU 4.2.2 | Vai trò code-only BodhiAtlas | Mức bằng chứng |
|---|---|---|---|
| PDF Unicode text sạch: Việt, Pāli dấu phụ, Sanskrit, Hán, Tạng | Đọc text layer/native khi có; fidelity từng dấu chưa thử | Giữ raw Unicode, so codepoint/grapheme với text layer, version checksum | `[CODE]` path, chất lượng `UNKNOWN` |
| Scan tiếng Việt/Hán giản-phồn | Bundle PP-OCRv6/VLM và parser model-assisted | Golden CER/WER theo script, không tự chuẩn hóa thành “đúng” | `[CODE][DOC]`, POC `NOT TESTED` |
| Scan Pāli `ā ī ū ṅ ñ ṭ ḍ ṇ ḷ ṃ` / Sanskrit `ḥ ṛ` | Không có CER theo ngôn ngữ trong khảo sát | Benchmark diacritics, lexical false negatives | `UNKNOWN` |
| Scan chữ Tạng Unicode + Wylie | Không tìm thấy validation riêng trên model được dùng | Hỗ trợ transcript/glyph pipeline đã kiểm, Wylie bằng index phụ có rules | `UNKNOWN` |
| Hán `無常` ↔ `无常`, `無我` | Parser không phải bộ chuyển phồn-giản có căn cứ | `NORMALIZED` phụ có rule/version, hiển thị phép biến đổi; EXACT giữ phân biệt | `EXTERNAL` |
| Việt `vô ngã` ↔ `vo nga` | Không phải nhiệm vụ parser | Accent-insensitive index phụ, `NORMALIZED`, không đổi raw string | `EXTERNAL` |
| `anatta/anattā/anātman`, `dukkha/duḥkha` | OCR đọc chữ; không phải lexicon học thuật | Lexicon theo **sense**, ngôn ngữ, tác giả, nguồn; không khẳng định tương đương mọi ngữ cảnh | `EXTERNAL` |
| Cụm dài 200–300 ký tự, **5 lần cùng file**, vượt trang/block | Doclib MATCH không bảo đảm exact/exhaustive, FTS cắt giữa | Scan/index canonical complete text, trả cả 5 offsets + multi-page segments, independent reopen | `[CODE]` M13–M15 |
| FUZZY do lỗi OCR/lỗi dấu câu | Không có công cụ đúng vai trò được chứng minh | Candidate trigram/Levenshtein + diff + trạng thái unverified | `EXTERNAL` |
| LEXICON theo nghĩa; SEMANTIC/hybrid/RAG | MinerU cung cấp đầu vào cấu trúc, không là sense system | FTS/exact + glossary graph; embeddings optional, claims qua verifier | `EXTERNAL` |

**Phân biệt rõ hai phần của truy vấn phân tích:** “Trong các tài liệu tôi có, những tác giả nào phân biệt giữa vô thường và khổ? Họ lập luận như thế nào? Cho tôi vị trí chính xác trong sách.” **Code-only** tìm ứng viên theo `vô thường/khổ/anicca/dukkha/無常/...` trong phạm vi đã lập chỉ mục, mở từng nguồn/ấn bản và cung cấp vị trí. **Người/AI** đọc ngữ cảnh để đánh giá *tác giả có thực sự phân biệt không, lập luận là gì và có phản biện nào*, gắn nguồn và trạng thái semantic riêng; không cho MinerU tự tạo “trích dẫn chính xác”.

**Kết luận retrieval:** có FTS ứng viên trong Doclib nhưng đó là **bounded ranked candidate retrieval**, **không** là exhaustive exact; tìm kiếm chuẩn hóa/lexicon/semantic nên nằm trong BodhiAtlas đã có/hệ mở rộng. `NOT TESTED` cho mọi truy vấn trong corpus PDF benchmark vì chưa chạy MinerU.

## 8. Integration Options for BodhiAtlas

### Phương án A — Stateless MinerU parser, BodhiAtlas owns truth (**ưu tiên POC**)

**Input contract:** `{file_id, work_id, edition_id, witness_id, sha256, immutable_local_path, rights_policy, parser_profile, requested_pages}`. **Bộ điều phối:** tự kiểm hash, MIME/permission; với PDF sạch chạy Flash TXT baseline; scan chạy Basic hoặc Standard trên hàng đợi; TEI/Bilara/TMX đi native extractor, không qua MinerU. **Output contract:** `MiddleJson 2.0 + image assets + source PDF page geometry + error report + extraction_run_manifest`. Import chỉ khi validate schema/tier/producer, page order/coverage, bbox bounds và file SHA.

**Source-of-truth:** BodhiAtlas original blobs, work/edition/witness catalog, canonical passage revisions, verified cards. MinerU chỉ nắm parsed artifacts; service thay thế được. **IDs:** `extraction_run_id` bất biến, `passage_id` thuộc BodhiAtlas, `source_map` là danh sách vùng; không dùng `doclib short_id`/block index làm persistent citation. **Failure/rollback:** parse fail→giữ bản extraction được chấp nhận trước, báo `PARTIAL/UNKNOWN`, không cập nhật `verified`; drift→quarantine để re-verify. **Migration:** exporter JSON/sidecars tách khỏi MinerU; thay Docling/Marker vẫn tiếp diễn canonical source card. **Cost:** medium/high vì phải viết adapter + QA, đổi lại portability tốt nhất.

### Phương án B — Doclib để thử đọc/tìm ứng viên, canonical BodhiAtlas vẫn riêng

**Input:** local files + source paths; **output:** cached Middle JSON, snippets, Doclib content cursors, parser metadata. Dùng cho developer preview, đối chiếu layout hoặc xem parse nhanh; **không** dùng làm `EXACT`, không dùng FTS để chứng minh *không tìm thấy*, không dùng ID `doc:.../tier/...` làm citation lâu dài. Phải xử lý trùng hệ SQLite/catalog với BuddhismDocuments-for-AI và bug-prone reparse cache/tier. **Failure/rollback:** độc lập xóa/rebuild Doclib cache, canonical bản đã duyệt không đổi. **Cost:** setup thấp/medium cho demo; **high** nếu tích hợp sâu do dual stores và sai khác semantics. Chỉ nên chọn B nếu UX thử nghiệm mang giá trị rõ rệt.

### Phương án C — Selective fallback/baseline

Sử dụng native TEI/Bilara/84000 của kho hiện hữu; Docling/Marker làm đối chứng model parsing, PyMuPDF để baseline PDF text/bbox (kiểm luật license), PaddleOCR cho crop khó. MinerU chỉ xử lý tài liệu/trang đạt lợi ích rõ ràng qua POC. **Điểm mạnh:** tránh chi phí VLM toàn bộ tài liệu và giảm xác suất làm hỏng nguồn sạch. **Không** có đường duy nhất bắt buộc cho mọi format.

**Giao kèo bất biến chung:** raw file/hash và các proof-of-source **sống độc lập** với chunk, embedding, FTS, cache/parser; backup và test restore định kỳ.

## 9. Practical POC / Reproduction Plan

**Tình trạng:** tất cả POC dưới đây là **`NOT TESTED`**. Trong phiên này GitHub đã được đọc qua connector; runtime Python/container không có nguồn model/corpus thử và thử `git ls-remote https://github.com/opendatalab/MinerU.git HEAD` báo `Could not resolve host: github.com`. **Không** suy ra tốc độ, số CER, chi phí hay kết quả thành công nào từ lệnh mẫu. Khi thực chạy cần ghi `uname -a`, Python/OS, GPU/RAM/VRAM, `mineru version --json`, pip freeze, model digests, SHA của fixtures, stdout/stderr, duration và outputs.

**Chuẩn bị chung, chỉ là lệnh dự kiến (sau khi cấp quyền tải model và dữ liệu):**

```bash
# Chạy trên môi trường có mạng để chuẩn bị; PIN phiên bản & SHA nguồn riêng.
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install 'mineru==4.2.2'
mineru version --json
mineru-kit hardware info --json
mineru-kit models download --tier basic --small-backend onnx --source huggingface
mineru-kit models verify --tier basic --small-backend onnx
export MINERU_MODEL_SOURCE=local
export MINERU_TELEMETRY_DISABLED=1
# Test không gửi tài liệu sang remote; xác thực qua firewall/network capture.
```

**Fixtures:** không dùng bừa tài liệu bản quyền. Tạo 6 fixture PDF reproducible (3 born-digital, 3 scan từ tài liệu được quyền dùng): `digital_simple.pdf` (2 trang), `digital_2col_footnote.pdf`, `digital_cjk_pali.pdf`, `scan_plain.pdf`, `scan_cjk_viet.pdf`, `scan_pali_tibetan.pdf`; thêm `cross_page_5hits.pdf` và corpus `tei-native.xml`. Với mỗi trang: một `gold.jsonl` chứa `file_sha256`, `printed_page` nếu chứng minh được, `page_no`, text từng vùng, bbox theo PDF point, reading-order ranks, footnote linkage, 200–300 ký tự quote, 5 occurrence offsets. Annotate độc lập bởi 2 người, đo inter-annotator disagreements; lưu quyền và font nguồn.

| TC | Steps/commands (ví dụ, không phải log chạy thật) | Gold / metrics | Expected artifact & acceptance focus | Result |
|---|---|---|---|---|
| TC01 Text/scan x3 | `mineru-kit parse fixtures/digital_simple.pdf -o out/flash.json -f middle_json --tier flash --ocr-mode txt`; lặp 6 PDF với Basic | Gold text + 10 vùng PDF/page bbox; CER/WER; `SOURCE_REOPEN_SUCCESS` | 6 JSON và 10 overlay; không tự thêm printed page, box đúng orientation | `NOT TESTED` |
| TC02 Two-column/table/footnote/multilingual | `mineru-kit parse fixtures/digital_2col_footnote.pdf -o out/complex.zip -f zip --tier standard` | Reading-order pair correctness, footnote-callout link, cell accuracy, CER grapheme, lost negation | HTML table + block order + notes + source region; tất cả lỗi được gắn nhãn | `NOT TESTED` |
| TC03 Tier/mode paired test | Chạy cùng trang `--tier flash --ocr-mode txt` và `--tier basic --ocr-mode ocr`, rồi so JSON text/bbox/page_map | Text equality, normalized edit distance, OCR confusion, false substitutions | Diff theo khối/trang, provenance branch; route sạch không bị silent replace | `NOT TESTED` |
| TC04 Crossing pages + 5 occurrences | Parse `cross_page_5hits.pdf`; import canonical; chạy engine `EXACT` độc lập | `EXACT_FULL_RECALL=found/5`, `FALSE_VERIFIED_CITATION`, `SOURCE_REOPEN_SUCCESS` | 5 offsets đầy đủ, kể cả giữa file và across pages; citation card có nhiều regions | `NOT TESTED` |
| TC05 Air-gapped & resource | Prefetch model; chặn egress; `MINERU_MODEL_SOURCE=local mineru-kit parse fixtures/scan_plain.pdf -o out/offline.json -f middle_json --tier basic` | RSS/VRAM peak, page/sec, startup/latency, network destinations/bytes, OOM count | Tái lập hoàn toàn offline, thiếu model fail rõ, không gọi cloud | `NOT TESTED` |
| TC06 Version-diff and rollback | Chạy 4.2.2, chạy tiếp bản mới hơn trong env riêng khi có; diff canonical/JSON | Block ID churn, text drift, bbox IoU, source-map reopen, verified-card breakage | Extraction revision mới, auto-halt các mismatch, restore old record | `NOT TESTED` |
| TC07 Multilingual route + TEI bypass | Ảnh từng hệ script; song song native TEI/JSON upstream | Diacritic CER/word loss, Tibetan clusters, zh variant recall, source coverage | Parser chỉ trên scan; TEI nguyên bản không đổi, normalized match có nhãn | `NOT TESTED` |
| TC08 Long document Doclib FTS limitation | Tạo file >30.000 ký tự với sentinel ở giữa, 5 hits cùng file; bật Doclib rồi so exact raw scan | Recall ở giữa/đầu/cuối, `LIMIT 200`, punctuation/symbol match | Thấy giới hạn Doclib và bắt buộc chuyển sang exhaustive core; không coi `0 hits` là absent | `NOT TESTED` |

**Tạo gold và đo:** Lưu `gold.jsonl` kèm `sha256sum fixtures/*`; text-level CER/WER tính từ gold **không** tự dùng output MinerU làm gold. `SOURCE_REOPEN_SUCCESS = số trích dẫn được kiểm đúng file+vùng+text / tổng trích dẫn được kiểm`; `FALSE_VERIFIED_CITATION = số trích sai vẫn mang nhãn verified / tổng verified`; `EXACT_FULL_RECALL = số vị trí khớp thật tìm được / tất cả vị trí khớp thật trong index hoàn chỉnh`. Thử `anatta/anattā/anātman/vô ngã/vo nga/無我/無常/无常/dukkha/duḥkha`, Tạng/Wylie khi có gold. Đo thời gian parse/index riêng; POC ngang hàng với Docling và Marker trên **cùng file, cùng quyền, cùng hardware**.

**Pass criteria:** không có false verified; mọi card verified mở lại thành công; failures/uncertainties có coverage reports; không silent OCR rewrite sạch; các chỉ số CER/reading order do chủ dự án định ngưỡng *trước khi* xem kết quả (không đặt ngưỡng giả để hợp thức hóa kết quả). Nếu fail, chọn fallback parser hoặc human review; **không** nới gate do điểm tổng tốt.

## 10. Deployment, Security, Legal, Cost

### Dependencies/hardware/deployment

- **[CODE]** Python `>=3.11,<3.15`, `docvortex>=0.6.21,<0.7`, Pydantic, PyPDFium2, ONNXRuntime, PaddleOCR-related code, optional Torch/vLLM/LMDeploy. Không đồng nhất điều kiện cài core với tất cả engine extension ([pyproject](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/pyproject.toml#L5-L112)).
- **[DOC]** Flash TXT ít model; Basic ONNX có CPU pathway; Standard/Advanced với VLM cần phần cứng/tùy engine. Hướng dẫn chính thức gợi ý RAM 16 GB cho higher-throughput local, VRAM 8 GB chỉ là điểm khởi đầu, không phải yêu cầu bảo đảm. Để sizing thực tế `UNKNOWN` đến TC05 ([tiers](https://opendatalab.github.io/MinerU/usage/tiers/)).
- **[DOC]** `MINERU_MODEL_SOURCE=local` chỉ tái sử dụng model đã có và fail nếu thiếu; prefetch + hash trước khi airgap. Dùng `mineru-kit models verify`; container pin digest của app và models, không để `latest` âm thầm đổi nhận dạng ([Model Source](https://opendatalab.github.io/MinerU/usage/model_source/)).

### Code license, model weights, corpus rights

**Code:** [LICENSE.md](https://github.com/opendatalab/MinerU/blob/f0497e0c6e9575fa553ce57cc9aa867906a00572/LICENSE.md) quy định Apache 2.0 **cùng điều khoản bổ sung**: cần giấy phép thương mại riêng nếu cùng affiliates vượt **100 triệu MAU** *hoặc* **20 triệu USD doanh thu hàng tháng**, phải hiển thị ghi nhận MinerU khi cung cấp dịch vụ online cho bên thứ ba; không tuân thủ có điều khoản chấm dứt tự động. Đây là **mô tả điều khoản nguồn, không phải tư vấn pháp lý**; cần pháp chế kiểm những ràng buộc phân phối/sản phẩm thực tế.

**Weights:** model 4.x là các gói khác nhau, gồm `MinerU-4_models_onnx`, `MinerU-4_models_torch`, VLM `MinerU2.5-Pro-2605-1.2B`, GGUF/mmproj và upstream OCR/formula/table. [ModelScope bundle Torch](https://www.modelscope.ai/models/OpenDataLab/MinerU-4_models_torch) ghi Apache 2.0; [HF VLM card](https://huggingface.co/opendatalab/MinerU2.5-Pro-2605-1.2B) ghi Apache 2.0. **Không suy ra mọi weight/submodel/asset giống hệt license card**: cần inventory, file license và source manifest theo **version/hash** của weights thực dùng; cân nhắc điều kiện upstream và redistributions.

**Data/source:** repo BuddhismDocuments-for-AI public chứa pins, manifest và corpus upstream, **không tự làm mọi bản dịch/sách/ảnh trang thành public domain**. Tách quyền đọc nội bộ, xử lý cloud API, xuất snippet, in/redistribute ảnh trang, trích dẫn, quyền tác giả, quyền dữ liệu chú giải và hạn chế OCR bản sao. Lưu `rights_profile` theo file/edition và policy cấm upload cho nguồn restricted.

### Security/privacy/backups

- Local mode: disable telemetry trước start với `MINERU_TELEMETRY_DISABLED=1`; tài liệu 4.x nói telemetry chẩn đoán mặc định bật trong Doclib nhưng loại nội dung/tên/path, **chưa tự packet-capture chứng minh** ([quick start](https://opendatalab.github.io/MinerU/quick_start/)). Firewall/airgap là xác thực quan trọng, không chỉ tin biến môi trường.
- V1 API/Router/Doclib có security surface khác nhau; bind `127.0.0.1` mặc định demo, reverse proxy mTLS/token nếu dùng LAN, hạn chế upload/file paths, URL SSRF, rate limit, arbitrary downloads, logs/snapshots. 4.2.0 release nói có SSRF hardening và Doclib bearer tokens nhưng **không coi app auth đủ cho triển khai public**. [Release 4.2.0](https://github.com/opendatalab/MinerU/releases/tag/mineru-4.2.0-released).
- Pin model/data provenance; backups tách (1) raw immutable files + SHA list, (2) catalog work/edition/witness+rights, (3) canonical passages+verification/claims, (4) extraction runs+Middle JSON/assets; vector/Doclib FTS cache tái dựng được. Thử restore có xác minh lại citation.
- Giá API cloud, GPU/hour, storage/egress hiện **UNKNOWN**. Tính `TCO = pages × measured_ms_per_page × compute_rate + storage_original + JSON/images + QA_review_minutes × labor_rate + engineering + backup + GPU_idle`; chạy Basic CPU / Standard VLM local / cloud trong cùng định dạng fixture. Không cung cấp số tiền giả hoặc nhận số quảng cáo làm kết quả thực tế.

## 11. Comparison & Trade-offs

Các đối chứng chọn **đúng lớp parser/OCR**; không chấm họ về lexicon/citation verifier nếu ngoài vai trò. Tài liệu dự án là `[DOC]`, khả năng thực tế vẫn `NOT TESTED`.

| Công cụ | Tính chất cùng lớp | Ưu điểm cần kiểm | Trade-off/gap với BodhiAtlas | Source/rights |
|---|---|---|---|---|
| **MinerU 4.2.2** | Parser/layout/OCR/VLM + Middle JSON + Doclib phụ trợ | 4 tier, batch/API, bbox/page index, bảng/công thức và nguồn sidecar; native PDF+Office/EPUB | Cần canonical adapter, per-char/edition provenance, multilingual benchmark; Doclib FTS bị truncate | [docs](https://opendatalab.github.io/MinerU/reference/output_files/); custom code license |
| **Docling** | Parser tài liệu/structured DoclingDocument + layout/OCR | Đối chứng mạnh về structured document, provenance, offline | Cần đo PDF page/bbox/footnote, tính trung thành với nguồn; exact search ở hệ ngoài | [repo MIT](https://github.com/docling-project/docling), [docs](https://docling.ai/) |
| **Marker** | PDF/Office/EPUB→Markdown/JSON/tree + optional LLM | Cùng dạng output, có `--keep_chars` char boxes **cho digital PDFs** | Với VLM route, tài liệu nói chỉ block-level HTML; kiểm đủ sidecars và license weights (khác code) | [README](https://github.com/datalab-to/marker/blob/master/README.md) (code Apache 2.0; weights điều kiện riêng) |
| **PaddleOCR / PP-Structure** | OCR + layout/table model stack | Tùy chọn crop OCR/multilingual theo model cụ thể; Pāli/Viet xuất hiện ở một số model language tables | Không phải hệ canonical docs/edition/search; cần layout adapter, phiên bản OCR cụ thể và quality gold | [PaddleOCR language/model table](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/OCR.en.md) |
| **olmOCR** | VLM PDF image/text linearization | Đối chứng transcript nhiều cột/scan, Markdown | GPU/VLM, output cần alignment/source map độc lập; không là exact engine | [olmOCR repository](https://github.com/allenai/olmocr) (code Apache 2.0) |
| **PyMuPDF** | PDF native text/glyph/word geometry baseline | `rawdict` có char-level positions cho digital PDFs, tốt để so raw text vs OCR | Không tự sửa đọc hai cột/scan; OCR/model cần ghép thêm; AGPL/commercial license cần xét | [rawdict documentation](https://pymupdf.readthedocs.io/en/latest/faq/index.html), [license](https://pymupdf.io/) |

**Đề xuất trade study:** MinerU Basic/Standard vs Docling + Marker trên 6–8 PDF, thêm PyMuPDF text baseline, PaddleOCR trên crop lỗi; đối chiếu cùng OCR gold, vùng PDF, throughput/resource và quyền. `SOURCE_FIDELITY` phải pass trước khi cân điểm CER/layout tổng; ưu tiên engine rẻ/đơn giản nếu chất lượng tương đương. **Không xếp hạng chiến thắng khi chưa chạy.**

## 12. Decision Record for Master Synthesis

| Field | Value | Evidence/assumption |
|---|---|---|
| TARGET | MinerU | github.com/opendatalab/MinerU |
| CLASS | component | Parser/OCR + optional document library, không phải canonical academic platform |
| DATE / VERSION / COMMIT | 2026-11-16 / release **4.2.2** tag commit `0621ddbab8bf85294d6bac101c0a6def843195d8` / inspected master `f0497e0c6e9575fa553ce57cc9aa867906a00572` | Tag object và metadata GitHub; đã tách hai SHA |
| PRIMARY_ROLE | Document extraction/OCR/layout → Middle JSON/sidecars for BodhiAtlas | M03–M10 |
| BEST_FIT_V1_CORE | partial | Ingest source parser, không phải exact/catalog/verified citations |
| SOURCE_FIDELITY_GATE | unknown | Block page+bbox native nhưng chưa kiểm recovery trên fixture; không có verified glyph-by-glyph |
| CODE_ONLY_EXACT_GATE | n/a | Parser không đảm nhiệm. **Nếu đề xuất dùng Doclib FTS thay EXACT thì fail**, M14–M15 |
| MULTILINGUAL_GATE | unknown | Có engine OCR đa ngữ nhưng chưa CER Pāli/Tạng/Việt/Hán |
| OCR_COVERAGE_GATE | unknown | Model + error paths có, chưa test scan và missing regions |
| RIGHTS_SECURITY_GATE | unknown | Code license đã đọc, model sub-licenses/data permissions và network policy chưa audit đủ |
| INTEGRATION_COST | high | Canonical source map/revision/human QA/rights needed; estimate qualitative |
| MAINTENANCE_RISK | medium | Fast 4.x changes, DocVortex external, model compatibility/tiers; chưa benchmark ops |
| RECOMMENDATION | TRIAL | Tương đương `TRIAL ONLY`; chỉ thăng thành `COMPONENT` sau gates |
| CONFIDENCE | medium | MED kiến trúc, LOW fidelity/quality vì POC NOT TESTED |
| NEXT_POC | TC01–TC06 ưu tiên, thêm TC07–08 | Sử dụng cùng gold PDF, source reopen, compare Docling/Marker |

### 5 findings đưa vào master synthesis

1. `4.2.2` là release mới đã xác minh, tier 4.x khác tên backend cũ; kết luận từ báo cáo 2.x cần refresh. **[DOC/CODE]**
2. Middle JSON v2 có source pages, PDF normalized bbox và `continues_prev`; **chỉ đủ làm nguồn cho adapter**, không phải citation đã xác minh. **[DOC]**
3. Schema/reader/postprocess thuộc dependency DocVortex; cần pin và audit phụ thuộc. **[CODE]**
4. Doclib FTS dùng Markdown-derived text, truncated đầu/cuối 30k, ranked limit 200 — **không exhaustive exact**. **[CODE]**
5. BodhiAtlas đã có upstream pin/corpus/resolver; MinerU nên bổ trợ tài liệu PDF/scan mới, không ghi đè native TEI/JSON. **[DOC][INFERRED]**

### 5 blockers trước ADOPT

1. `SOURCE_REOPEN_SUCCESS` thực trên text PDF+scan chưa đo, nhất là page/bbox xuyên trang.
2. Không có gold CER/WER cho Việt/Hán/Pāli/Tạng; mô hình 4.x và diacritic fidelity chưa qua POC.
3. Thiếu map bền vững char↔glyph, link footnote-callout, trang in có chứng cứ; phải xây/kiểm độc lập.
4. Doclib Search **không** đáp ứng `EXACT_FULL_RECALL`; nếu tái sử dụng có nguy cơ trả false absence, phải chặn.
5. License weights/third-party + data rights + telemetry/offline/API permission và backup chưa nghiệm thu.

### 5 experiments ưu tiên

1. 3 digital + 3 scan với gold OCR, bbox và 10 test citations (TC01).
2. Multi-column/table/footnotes/CJK/Pāli/Tạng + phủ định/ligature (TC02/TC07).
3. Auto/text/ocr/tier paired-diff để bắt silent replacement of text layer (TC03).
4. Long query + 5 hits + crossing pages + source reopen, phân biệt FTS vs canonical exact (TC04/TC08).
5. Fully offline Basic/Standard selected, resource and version drift/rollback (TC05/TC06).

### 3 quyết định chờ chủ dự án

1. **Policy quyền:** tập PDF/scan mẫu nào được phép OCR nội bộ, ảnh trang nào bị cấm gửi cloud/redistribute? Xác nhận danh sách fixtures được quyền sử dụng.
2. **Ngưỡng accept:** định mức `CER/WER` theo ngôn ngữ và tiêu chí reading-order, chi phí GPU/CPU/mức công rà tay trước POC. Gate verified source (0 false verified) giữ bất biến.
3. **Kiến trúc đường dài:** ưu tiên A (stateless MinerU→canonical, đề xuất) hay B (tích hợp Doclib làm UI/candidate); có nhu cầu chạy VLM offline Standard từ V1 hay không?

## 13. Appendix

### A. Links/paths gốc và code đã khảo sát

- Target / release: <https://github.com/opendatalab/MinerU> · <https://github.com/opendatalab/MinerU/releases/tag/mineru-4.2.2-released> · [4.2.2 tag commit](https://github.com/opendatalab/MinerU/commit/0621ddbab8bf85294d6bac101c0a6def843195d8).
- Versioned code root: <https://github.com/opendatalab/MinerU/tree/f0497e0c6e9575fa553ce57cc9aa867906a00572>.
- Public docs: <https://opendatalab.github.io/MinerU/quick_start/> · <https://opendatalab.github.io/MinerU/usage/tiers/> · <https://opendatalab.github.io/MinerU/reference/output_files/> · <https://opendatalab.github.io/MinerU/usage/model_source/>.
- Data/schema/architecture: `docs/next/middle-json/current-medium.md`, `docs/next/middle-json/envelope.md`, `docs/next/architecture.md`, `mineru/types.py`, `mineru/backend/postprocess/document.py`, `mineru/integrations/docvortex.py`.
- Entrypoints: `pyproject.toml` scripts; `mineru/cli/main.py`, `mineru/kit/commands/parse.py`, `mineru/parser/base.py`, `mineru/backend/analyze.py`.
- Key modules: `mineru/backend/analysis/pdf/pipeline.py`, `ocr.py`, `layout.py`, `text/native.py`, `text/content.py`, `mineru/model/registry.py`, `mineru/doclib/core/fts.py`, `mineru/doclib/services/search_svc.py`, `mineru/doclib/services/parse_execution_svc.py`, `mineru/doclib/services/content_read_svc.py`, `mineru/doclib/locators.py`, `mineru/doclib/migrations/001_init.sql`.
- Tests seen: `tests/unittest/test_doclib_locators.py`, `test_pdf_scan_text_routing.py`, `test_pdf_footnote_layout.py`, `test_pdf_native_cjk_quote_span_edge.py`, `test_middle_json_validator.py`. **File tồn tại không đồng nghĩa đã tự chạy.**
- BodhiAtlas: <https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/PRD.md> (đã đọc toàn văn qua connector); <https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/ACADEMIC_RISKS_AND_VERIFICATION.md> (đã đọc toàn văn); <https://github.com/quoctran-2608/BuddhismDocuments-for-AI> (`README.md`, `manifest.json` đã đọc). PRD file blob SHA GitHub: `58d967c642d625180c436e1a6e6a75fa2e7070e3`; risk file blob SHA: `cdb642633f3dc3f7f83cb0e49a96abfebc9f132e` (đây là blob SHA, không phải repo commit SHA).
- Issues chỉ dùng làm POC risk signals: [#5705](https://github.com/opendatalab/MinerU/issues/5705), [#5517](https://github.com/opendatalab/MinerU/issues/5517), [#5628](https://github.com/opendatalab/MinerU/issues/5628), [#5465](https://github.com/opendatalab/MinerU/issues/5465). Với từng issue cần tra trạng thái hiện tại và tái hiện trên đúng release.

### B. Command checklist (chưa chạy)

```bash
# Kiểm version và model deployment
mineru version --json
mineru-kit hardware detect --json
mineru-kit hardware info --json
mineru-kit models show
mineru-kit models verify --tier basic --small-backend onnx

# Chạy text layer và OCR, xuất result có cấu trúc
mineru-kit parse fixtures/digital_simple.pdf -o out/text.json -f middle_json --tier flash --ocr-mode txt
mineru-kit parse fixtures/scan_plain.pdf -o out/scan.zip -f zip --tier basic --ocr-mode ocr

# Disable telemetry BEFORE process start; cho phép local-only và verify egress
export MINERU_TELEMETRY_DISABLED=1
export MINERU_MODEL_SOURCE=local
mineru-kit api-server --host 127.0.0.1 --port 8000 --tier basic

# Bộ đối chứng được cài trong env riêng, không dùng output MinerU làm đáp án chuẩn
sha256sum fixtures/* > gold/fixture_sha256.txt
```

### C. Giới hạn/những thứ *không* được xác minh

- **Không cài/chạy MinerU, không inference OCR/VLM**; không ghi `[TESTED]` cho pipeline; không có CER, WER, recall, latency, RAM/VRAM, giá thực tế, carbon hoặc false-citation measured. Thử `git ls-remote` trong sandbox không truy cập được GitHub do DNS; đọc code qua GitHub connector, không suy ra POC thất bại do dự án.
- **Chưa** đọc/audit dependency `docvortex` theo commit, thành phần mô hình ONNX/Torch, full `model registry` upstream weight licenses, mọi line tests, dịch vụ hosted/proprietary và quyền từng tác phẩm. Sơ đồ/document contract phần BodhiAtlas là **đề xuất**, không phải đang vận hành.
- **Không** xác nhận định vị EPUB CFI/href, page printed evidence, OCR confidence calibration theo ký tự, closure semantic, visual reading order, native Tibetan OCR hoặc all-positions exact như năng lực MinerU. Các tuyên bố tính năng nhanh/chính xác trong changelog/README không thay thế thực đo.
- **Không** đánh giá “không tìm thấy = không tồn tại”; chỉ phát biểu *không tìm thấy trong phần corpus thực sự đã kiểm* và giữ coverage/rights/source availability.
- **Bản quyền và pháp lý:** giấy phép code đọc được trực tiếp; quyền weights, model derivative và ảnh/biên dịch cần review trường hợp sử dụng, không suy từ repository public.

### D. Quy tắc tổng hợp máy và kết luận cuối

**Reusable:** OCR/layout nhận dạng nhiều khối, tiers local, Middle JSON v2 và PDF regions, DocVortex native parsing, CLI/SDK/API/ZIP, file-level SHA và parse cache hỗ trợ kỹ thuật. **BodhiAtlas phải bổ sung/duy trì:** immutable originals, catalog work/edition/witness, precise and revisioned source maps, Unicode exact + normalized/fuzzy/lexicon độc lập, QA coverage, independent citation reopen, semantic distinction, privacy/rights/backup và migration. **Evidence còn thiếu trước COMPONENT:** TC01–TC06 đầy đủ (khuyến nghị cả TC07–08), model-weights/license manifest, drift test và threat model.

**Final decision:** `TRIAL ONLY` (`RECOMMENDATION=TRIAL`); **không ADOPT làm platform** và **không thay CODE_ONLY_EXACT bằng Doclib Search**. Chuyển sang `USE AS COMPONENT` chỉ nếu các gate nguồn, OCR multilingual, coverage, privacy/rights và portability đều vượt kiểm thử độc lập, **không đánh đổi bằng một điểm benchmark tổng**.
