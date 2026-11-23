# REPORT 56 — Independent Technical Assessment: Open Notebook / BodhiAtlas

**Ngày kiểm tra:** 23/11/2026 (Asia/Ho_Chi_Minh)  
**Đối tượng:** [`lfnovo/open-notebook`](https://github.com/lfnovo/open-notebook) và thư viện/tích hợp liên quan  
**Phạm vi quyết định:** BodhiAtlas V1.4, *V1 Core Foundation*, *Academic Risks & Verification*, đối chiếu A–E  
**Phương pháp:** truy cập GitHub trực tiếp qua API/kết nối được ủy quyền; xác minh SHA, đọc nội dung code, migration, docs, test nguồn và repo đối chứng. **Chưa clone/chạy Open Notebook, SurrealDB, Docling hoặc POC BodhiAtlas trên fixture thực tế**. Mọi chỉ số runtime: **NOT TESTED**.  
**Tính chất:** đánh giá độc lập theo snapshot cố định, không dựa vào kết luận các báo cáo P01–P55. Các báo cáo này chỉ hỗ trợ định vị nguồn để đối chiếu độc lập.

**Quy ước bằng chứng:** `[CODE]` mã/hàm/schema đã đọc ở commit ghim; `[DOC]` tài liệu chính thức hoặc PRD; `[ISSUE]` báo cáo lỗi/issue (không có nghĩa đã tái hiện); `[PLAN]` thảo luận/roadmap chưa phát hành; `[INFERRED]` hệ quả kiến trúc được suy luận từ nguồn; `[UNKNOWN]` chưa đủ chứng cứ; `[TESTED]` chỉ khi đã thực thi thao tác được mô tả và có đầu ra. Trong báo cáo **không có tuyên bố `[TESTED]` đối với phần mềm đang thẩm định**; test source hoặc CI tự mô tả không phải kết quả do người lập báo cáo thực hiện. “Không thấy trong code/schema đã đọc” không có nghĩa chứng minh tuyệt đối toàn bộ ecosystem không tồn tại tính năng.

---

## 1. Executive Decision

**Quyết định cho toàn bộ Open Notebook: `TRIAL ONLY` — KHÔNG chọn `Open Notebook-first` làm system of record hoặc lõi chứng cứ V1.** **Lựa chọn kiến trúc ưu tiên: `D — BodhiAtlas Minimal Core`**, lấy file gốc + catalog scholarly + canonical extraction/source map + exhaustive code-only search + verifier làm thẩm quyền; chỉ cân nhắc `lfnovo/content-core` như thư viện parser/route **sau POC** (`USE AS COMPONENT`, có điều kiện), và triển khai Open Notebook như **Research Workspace riêng, tùy chọn ở V2/V3**, kết nối qua REST bằng bản sao phiếu chứng cứ, không làm thẩm quyền cho `VERIFIED`.

**Confidence:** **HIGH** rằng Open Notebook `main` được kiểm tra **không native** đáp ứng G1/G2/G3 và contract exhaustive EXACT theo PRD; **MED** rằng D có tổng chi phí đạt chuẩn thấp nhất vì không có benchmark end-to-end hay ước lượng nhân lực đã đo; **LOW–MED** về chi phí duy trì deployment lâu dài trên phần cứng mục tiêu chưa biết. `TRIAL ONLY` không phủ nhận tiện ích sản phẩm: UI notebooks, chat, notes, insight, REST, model choice và background processing là những chức năng **có code**.

**Vấn đề quyết định không thể bù bằng điểm trung bình:**

1. **G1 — bất biến nguồn và coverage:** schema `Source` chỉ có `asset`, `title`, `topics`, `full_text`, `command`, thời gian; ingestion ghi `extraction.content` vào `full_text`, không lưu extraction revision, work/edition/witness, locator theo trang/CFI, page coverage hoặc hash bytes nguồn thành các trường riêng. Đáng chú ý cài đặt mặc định còn **xóa file upload sau xử lý** theo `auto_delete_files="yes"`. Xem [Source schema](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L450-L461), [save_source](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L349-L383), [settings](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/content_settings.py#L8-L21). `[CODE]`
2. **G2 — citation kiểm độc lập:** citation được model chọn ID `source/note/insight`, trỏ **toàn bộ item**, không có page/offset/bbox/CFI hoặc independent quote/locator verifier. Dù endpoint tải file gốc tồn tại **nếu upload chưa bị xóa**, khả năng tải file không đồng nghĩa reader reopen đúng trang và highlight đúng chữ. [Citation guide](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/3-USER-GUIDE/citations.md#L7-L40), [file download](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/routers/sources.py#L1042-L1075). `[DOC][CODE]`
3. **C05 — không phải exhaustive EXACT:** SurrealDB `fn::text_search` dùng English-stemmed BM25, GROUP BY và `LIMIT`; API trả item results, không mọi occurrence với character offsets. Khi lỗi highlight position overflow, Python `text_search` **fallback sang vector** nhưng `search_type` vẫn lấy từ request. Một biến đổi semantic âm thầm như vậy **không được gắn EXACT**. [Analyzer](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/1.surrealql#L64-L72), [effective search migration 26](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/26.surrealql#L111-L192), [fallback](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L898-L949). `[CODE]`
4. **G3 — trust boundary:** Ask là LLM strategy → vector top-10/nhánh → LLM answer/nhánh → LLM final. Không thấy bộ kiểm claim-support hoặc human scholarly approval trong các luồng đã đọc. Không được coi câu trả lời có citation ID là chứng cứ đã kiểm. [Ask graph](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/ask.py#L65-L203). `[CODE]`
5. **Operability:** 2 Compose services mặc định nhưng thực chất ít nhất 4 vai trò chạy: SurrealDB, FastAPI, worker, Next.js; thêm checkpoint SQLite và uploads volume. V1 cần ít loại state authoritative hơn, không phải tái thiết trên SurrealDB. [Architecture](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/7-DEVELOPMENT/architecture.md#L12-L34), [Compose](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docker-compose.yml#L1-L66). `[CODE][DOC]`

**CURRENT (đã chứng minh ở HEAD):** App đa notebook/source, notes/insights/chat/Ask, text BM25, vector tùy model, REST, file download có điều kiện, parser qua `content-core`, model via `esperanto`, worker, basic password; có cải tiến an toàn URL và scope. **ROADMAP, không được tính vào điểm V1:** #1315 định hướng search–evidence–provenance standalone, span-level validated citation và MCP read-only local; maintainer nói rõ *direction, not commitment; no dates*, chưa thấy package `evidence-core` công bố qua tìm kiếm tên repo trong tổ chức `lfnovo` và chưa thấy Open Notebook phụ thuộc package như vậy. Tình trạng chính xác ở mọi tổ chức/tên khác là **UNKNOWN**, không khẳng định chứng minh không tồn tại trên toàn GitHub. [Discussion #1315](https://github.com/lfnovo/open-notebook/discussions/1315), [Vision](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/VISION.md#L49-L75). `[PLAN][UNKNOWN]`

**Điều kiện đảo quyết định:** (i) upstream ship/release evidence schema có source identity/hash/edition/locator/coverage, verifier fail-closed thực, (ii) POC-2 đạt exhaustive EXACT không phụ thuộc embedding và không fallback semantic trong tất cả tình huống adversarial, (iii) POC-3 đạt G2 raw-reopen và G3 state separation, (iv) POC-5 chứng minh migration/restore và chi phí vận hành so với D có lợi. Nếu một trong bốn thiếu, giữ D. Không nâng hạng bằng demo đẹp hoặc ROADMAP.

---

## 2. Sources & Evidence Ledger

### 2.1. Snapshot được kiểm tra

| Đối tượng | Owner / branch | SHA/phiên bản đã truy vấn | Phạm vi nguồn đã kiểm | Trạng thái |
|---|---|---|---|---|
| Open Notebook | `lfnovo`, `main` | HEAD `0c1e7abbd77411057d8feef02fc4588ec9a556d6`, 18/11/2026; package `1.15.1`; frontend package `0.1.0`; MIT | metadata repo, recursive tree, code, docs, migration, một số tests | **ACCESS OK / CODE READ** |
| Stable release | `lfnovo/open-notebook` | `v1.15.1`, công bố 04/11/2026; tag commit `5e285b7a2e435895c4ee99ad7e4b8d2af64c3239` | GitHub release API và Git ref | **ACCESS OK / NOT DEPLOYED** |
| Content Core | `lfnovo/content-core`, `main` | `b8452534bfd85ac6048ac8f028a219638aef0a8c`, 08/11/2026; `2.3.0`, MIT | source `src/`, parser, model, tests | **ACCESS OK / CODE READ** |
| Esperanto | `lfnovo/esperanto`, `main` | `343e0a9f874cb9a4339f2bc21817add4c296daa6`, 03/10/2026; `2.28.0`, MIT | `README`, `pyproject`, `LICENSE` | **ACCESS OK / LIMITED REVIEW** |
| Surreal Commands | `lfnovo/surreal-commands`, `main` | `2abbdd7f4581b9f3514669721cb949f536cc2a87`, 31/01/2026 | README/queue contract | **ACCESS OK / LIMITED REVIEW** |
| MCP community | `Epochal-dev/open-notebook-mcp`, `main` | `a2cddbf65cba8c4c8de7be16566781b7612a9545`, 22/12/2025 | README/API/remote transport | **ACCESS OK / THIRD-PARTY** |
| BodhiAtlas | `quocgempro361/bodhi-atlas`, `main` | `aa874008ff4c6a6e9d66e6fee34c55e0370d6820`, 16/11/2026 | PRD 398 dòng, V1 Core 249 dòng, Risk handbook 239 dòng | **ACCESS OK / DOC READ** |
| Bang-ha | `quoctran-2608/Bang-ha-giac-ngo`, private `main` | `4345737ae16638b19226ea1b11007e6ffa4faf62`, 27/09/2026 | code `tools/local_corpus_framework`/ledger; yêu cầu quyền riêng tư để người khác mở permalink | **ACCESS OK VIA AUTHORIZED CONNECTION** |
| BCR | `quoctran-2608/BuddhismDocuments-for-AI`, `main` | `dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410`, 05/11/2026 | model/retrieval/verification/resolver | **ACCESS OK / CODE READ** |

Các SHA trên chỉ nhận diện commit, không phải hash SHA-256 của file PDF do người dùng nhập; Git blob SHA và package release cũng không thay thế chứng cứ quyền đối với nội dung sách. **Ngày truy cập toàn bộ: 23/11/2026**. Stable và HEAD là hai snapshot **khác nhau**: commit của tag phải dùng khi POC release; không thể dẫn `main` để khẳng định hành vi release hoàn toàn đồng nhất. `[CODE][DOC]`

### 2.2. Ledger truy vết claim quan trọng

Tiền tố permalink: `ON` = commit HEAD Open Notebook; `CC` = content-core; `BA` = BodhiAtlas. Đường dẫn trong bảng là liên kết pin SHA có line, không phải liên kết `main` động.

| ID | Luận điểm / giới hạn | Loại | Permalink/source snapshot | Chưa kiểm / phản chứng |
|---|---|---|---|---|
| E01 | HEAD/release độc lập; pyproject 1.15.1 | `[CODE][DOC]` | [HEAD](https://github.com/lfnovo/open-notebook/commit/0c1e7abbd77411057d8feef02fc4588ec9a556d6), [release](https://github.com/lfnovo/open-notebook/releases/tag/v1.15.1), [pyproject L2–4](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/pyproject.toml#L2-L4) | Chưa chạy image release |
| E02 | 4 runtime roles, Surreal v2 + checkpoint SQLite | `[CODE][DOC]` | [architecture L12–34](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/7-DEVELOPMENT/architecture.md#L12-L34), [supervisord L12–49](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/supervisord.conf#L12-L49) | Runtime topology chưa chạy |
| E03 | Source schema thiếu identity scholarly/map/coverage | `[CODE]` | [domain L335–343, L450–461](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L335-L461), [migration 1 L2–26](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/1.surrealql#L2-L26) | Không loại trừ dữ liệu tùy biến ngoại lai bên ngoài schema |
| E04 | `Source.full_text = extraction.content`; không lưu structured extraction metadata | `[CODE]` | [source graph L313–383](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L313-L383) | Kiểm thử re-ingest chưa chạy |
| E05 | Upload auto-delete **mặc định yes**; code thực sự unlink khi yêu cầu | `[CODE]` | [settings L16–21](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/content_settings.py#L16-L21), [unlink L334–344](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L334-L344) | Cần xác minh UI/form map setting thành delete_source trên từng luồng |
| E06 | Có raw-file download **nếu còn file** | `[CODE]` | [sources router L1042–1075](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/routers/sources.py#L1042-L1075) | Chưa kiểm HTTP/stream/reader; không có page highlight ở đây |
| E07 | Citation LLM trỏ whole item, không page/section/highlight | `[DOC][CODE]` | [citations L7–40](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/3-USER-GUIDE/citations.md#L7-L40), [UI parser L34–55](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/frontend/src/lib/utils/source-references.tsx#L34-L55), [prompt L35–55](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/prompts/source_chat/system.jinja#L35-L55) | Không có adversarial citation runtime |
| E08 | BM25/English stemming, không phải raw string offsets | `[CODE]` | [analyzer L64–72](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/1.surrealql#L64-L72) | Chưa đo tokenizer Unicode trên Surreal v2 |
| E09 | Effective text search GROUP BY, LIMIT, không trả all occurrences | `[CODE]` | [migration 26 L111–192](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/26.surrealql#L111-L192) | Không chứng minh mọi query trả thiếu; hợp đồng exhaustive không có |
| E10 | Text highlight-error fallback vector | `[CODE]` | [notebook.py L898–949](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L898-L949) | Tần suất bug chưa đo; chỉ nhánh lỗi RuntimeError liên quan overflow |
| E11 | API `total_count = len(results)` sau LIMIT, echo `search_type` request | `[CODE]` | [search.py L25–61](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/routers/search.py#L25-L61), [limit max1000](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/models.py#L67-L81) | POC kiểm count/overflow chưa chạy |
| E12 | Ask strategy LLM → vector top10/nhánh → LLM → final LLM | `[CODE]` | [ask.py L47–52, L65–203](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/ask.py#L47-L203) | Thực tế token và số term vượt 5 chưa đo |
| E13 | Chunk embedding chỉ có source/order/content/embedding | `[CODE]` | [embedding command L313–416](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/commands/embedding_commands.py#L313-L416), [migration1 L16–20](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/1.surrealql#L16-L20) | Không có offset/span locator bất biến trong records này |
| E14 | `content-core` ExtractionOutput là content string + small metadata | `[CODE]` | [state.py L22–29](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/common/state.py#L22-L29) | Có thể nhúng Docling JSON trong string nếu cấu hình |
| E15 | Docling optional export JSON/HTML/MD, không typed source map | `[CODE]` | [docling.py L101–145](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/processors/document/docling.py#L101-L145) | Không đã test output JSON trên layout thật |
| E16 | Simple PDF pdfplumber gom text, whitespace/hyphen cleanup | `[CODE]` | [pdf.py L151–185](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/processors/document/pdf.py#L151-L185), [test source](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/tests/unit/test_pdf_extraction.py#L12-L38) | Không có WER/CER, bbox, printed pages |
| E17 | EPUB fast-ebook thành markdown, không expose CFI/spine trong output | `[CODE]` | [epub.py L14–27](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/processors/document/epub.py#L14-L27) | Có thể viết adapter EPUB ngoài thư viện |
| E18 | Notes REST, notebook/source CRUD có sẵn | `[CODE]` | [notes.py L17–118](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/routers/notes.py#L17-L118), [sources endpoints](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/routers/sources.py#L870-L1075) | Roundtrip metadata thuần văn bản chưa kiểm |
| E19 | Một shared password, no RBAC/ACL; CORS default phụ thuộc cấu hình | `[CODE][DOC]` | [security L1–7, L75–115, L169–217](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/5-CONFIGURATION/security.md#L1-L217), [main.py L83–114](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/main.py#L83-L114) | Pentest/deployment chưa làm |
| E20 | Compose root:root fallback, app password trống, encryption placeholder, 8502+5055 published | `[CODE]` | [compose L1–66](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docker-compose.yml#L1-L66) | Không phải cấu hình khuyến nghị LAN/VPS |
| E21 | SSRF/path guards hiện hữu; không thể đánh đồng “không có” với “đã pentest an toàn” | `[CODE]` | [source.py L175–193](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L175-L193), [url validation](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/utils/url_validation.py#L43-L165) | Redirect/DNS-rebind adversarial test chưa chạy |
| E22 | PRD đòi all occurrences và exact source mapping | `[DOC]` | [PRD L107–119](https://github.com/quocgempro361/bodhi-atlas/blob/aa874008ff4c6a6e9d66e6fee34c55e0370d6820/docs/PRD.md#L107-L119), [L227–250](https://github.com/quocgempro361/bodhi-atlas/blob/aa874008ff4c6a6e9d66e6fee34c55e0370d6820/docs/PRD.md#L227-L250) | PRD là hợp đồng, chưa là code đã nghiệm thu |
| E23 | G1–G6: coverage, verified quote, scholarly support riêng | `[DOC]` | [Academic Risks L90–100, L154–165](https://github.com/quocgempro361/bodhi-atlas/blob/aa874008ff4c6a6e9d66e6fee34c55e0370d6820/docs/ACADEMIC_RISKS_AND_VERIFICATION.md#L90-L165) | Gate phải chứng minh POC |
| E24 | BCR có pinned source quote verifier và source resolvers, không phải PDF/EPUB general | `[CODE]` | [verification.py L1–57, L129–153](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/verification.py#L1-L153), [resolvers.py](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/source_resolvers.py#L1-L65) | Không đo trên sách mới |
| E25 | Bang-ha có SQLite passage/edition/file SHA/locator nhưng giới hạn personal books, occurrence | `[CODE]` | [common.py L87–115](https://github.com/quoctran-2608/Bang-ha-giac-ngo/blob/4345737ae16638b19226ea1b11007e6ffa4faf62/tools/local_corpus_framework/corpus/common.py#L87-L115), [cli.py L109–130](https://github.com/quoctran-2608/Bang-ha-giac-ngo/blob/4345737ae16638b19226ea1b11007e6ffa4faf62/tools/local_corpus_framework/corpus/cli.py#L109-L130) | Repo private; quyền corpus riêng cần kiểm |
| E26 | Bang-ha ledger mặc định `review_state='VERIFIED'` là rủi ro trust | `[CODE]` | [scholarly_ledger.py L127–152](https://github.com/quoctran-2608/Bang-ha-giac-ngo/blob/4345737ae16638b19226ea1b11007e6ffa4faf62/tools/scholarly_ledger.py#L127-L152) | Không đánh đồng với BCR verifier chuẩn hơn |
| E27 | Evidence core độc lập là hướng thiết kế, chưa có release/package xác minh | `[PLAN][UNKNOWN]` | [discussion #1315](https://github.com/lfnovo/open-notebook/discussions/1315), [VISION L49–75](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/VISION.md#L49-L75) | Tìm `evidence-core` trong repo owner `lfnovo`: không thấy; không chứng minh không có tên khác |
| E28 | Tests nguồn có mock Ask/docling, không phải benchmark thật | `[CODE]` | [ON test Ask](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/tests/test_ask_graph.py#L46-L110), [CC mock Docling](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/tests/unit/test_docling_extraction.py#L29-L80) | **NOT TESTED** trong nghiên cứu này |
| E29 | Source URL hardening cải thiện ở release 1.15.1 | `[DOC]` | [release notes v1.15.1](https://github.com/lfnovo/open-notebook/releases/tag/v1.15.1) | Không chứng nhận chống SSRF tuyệt đối |
| E30 | `Content Core` MIT, `Esperanto` MIT; model/book rights riêng | `[CODE]` | [CC LICENSE](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/LICENSE), [Esperanto LICENSE](https://github.com/lfnovo/esperanto/blob/343e0a9f874cb9a4339f2bc21817add4c296daa6/LICENSE), [ON LICENSE](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/LICENSE) | Transitive licenses, model terms, rights mỗi sách: **UNKNOWN / NOT AUDITED COMPLETELY** |

**Độ tin cậy ledger:** E03/E04/E07/E08/E09/E10/E12/E13/E14/E15/E16/E17/E18/E19/E20/E24–E26 là quan sát code; kết luận “không đạt G1/G2/C05” là **đánh giá compliance từ code**, không phải tuyên bố đã chạy test thất bại. Những khía cạnh vẫn `UNKNOWN`: lỗi thực tế và tỷ lệ lỗi OCR, latency/RAM/storage, enterprise hardening, hiệu quả CJK tokenizers từng cấu hình, khả năng restore, full dependency license/SBOM, pass rate 50 query, tương thích REST adapter qua phiên bản nâng cấp.

---

## 3. Architecture & Data Flow

### 3.1. Sơ đồ luồng dữ liệu được xác lập từ code

```text
Browser / Next.js 16 (:8502)
    |  /api/*  (proxy / cross-origin)
    v
FastAPI (:5055) -- shared bearer password / CORS / upload-size guards
    | POST sources (multipart or JSON), notes, notebooks, search, Ask
    |
    +-- save upload -> /app/data/uploads/  [CÓ THỂ BỊ XÓA]
    |       |
    |       v
    |  Source(asset.file_path / asset.url)   [SurrealDB record]
    |       |
    |       +-- process_source job -> SurrealDB commands queue
    |                               |
    |                          surreal-commands worker
    |                               |
    |                          content_core.extract_content
    |                           |             |
    |                        simple        Docling optional
    |                     PDF/EPUB/...      OCR/layout/MD/HTML/JSON string
    |                           \             /
    |                            ExtractionOutput(content, title, metadata)
    |                                      |
    |                            source.full_text = content
    |                                      |
    |                                SurrealDB source
    |                                      |
    |                           (optional) embed_source
    |                                      |
    |                     chunk_text -> Esperanto/embed model
    |                                      |
    |                     source_embedding(order, content, embedding)
    |
    +-- POST /search -> Surreal fn::text_search (BM25) OR vector_search
    |                  |--- text highlight error -> VECTOR fallback!
    |                  +--- grouped/top LIMIT, not occurrence-level offsets
    |
    +-- POST /search/ask -> LLM strategy -> vector top10 per term
    |                       -> LLM partials -> LLM final + model-chosen item IDs
    |
    +-- notebooks / notes / insights (SurrealDB records, relation edges)
    +-- chat / source-chat -> LangGraph checkpoints (separate SQLite file)
    +-- file download -> uploaded bytes ONLY if still present

External state / dependencies:
 - SurrealDB v2/RocksDB (data, jobs, BM25 and vectors)
 - Next.js + FastAPI + worker under supervisord (three processes in app image)
 - SQLite LangGraph checkpoint, filesystem uploads, optional model caches
 - Optional provider HTTP, OCR/VLM, web extraction services
```

**Phần sống độc lập:** `content-core` có `extract_content` API không đòi Next/SurrealDB; Esperanto là client/provider abstraction; một vài thuật toán chunking có thể được trích nhưng phải xét license và phụ thuộc. **Phần không thể “import như thư viện” một cách rẻ:** `Source`, `Note`, search function và worker gắn Surreal record IDs, schema migration, functions, API, LangGraph; lấy toàn bộ module domain mà không chạy SurrealDB không tương đương reusable library. `[CODE]` [Source graph](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L196-L383), [SQL migration](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/26.surrealql#L20-L192).

### 3.2. Service/process, persisted state, failure modes

| Thành phần | Trách nhiệm | Trạng thái cần bảo vệ | Failure mode đặc thù |
|---|---|---|---|
| Next.js | notebooks/search/chat/source viewing | Client/browser localStorage auth | API khác origin, mất session; không là evidence authority |
| FastAPI | CRUD, upload, Search, Ask, sync orchestration, auth | Không nên authoritative ngoài DB/storage | 5xx khi DB/search, fallback không đúng semantics, upload error |
| Worker / surreal-commands | source extraction, embedding, insight, podcast | queue/job status trong SurrealDB | worker ngưng ⇒ nguồn vẫn pending; retry, race with delete, partial chunk cleanup |
| SurrealDB v2 + RocksDB | source, note, notebook, relation, BM25, vector, queue | **App state có lock-in** | conflict, migration, backup consistency; Surreal v3 chỉ planned |
| SQLite checkpoint | chat/source-chat checkpoint | history không cùng kho với SurrealDB | mất hội thoại khi chỉ backup database |
| `uploads/` | bytes uploaded có điều kiện | file có thể bị delete | không thể reopen/so SHA nếu hết bytes |
| Local/remote models | embeddings, Ask/chat, transformations, podcast | weights/cache, secrets, request logs | thiếu embedding ⇒ vector/Ask không chạy; egress/chi phí |

**Tính năng code-only thực sự:** quản lý metadata basic, nạp text/PDF text/EPUB/DOCX bằng parser không cần LLM (không đồng nghĩa OCR tốt), notebook/notes CRUD và `text_search` trong đường bình thường. Nhưng `Note.save()` tự enqueue embedding dù có thể không cấu hình embedding; `Ask`, vector, generative chat/insight, STT/TTS phụ thuộc model. **Một endpoint trả `type=text` không bảo đảm đường thực thi không gọi embedding khi fallback overflow.** `[CODE]` [Note.save](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L768-L801), [Search](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L898-L949).

### 3.3. Điểm mất thông tin và khóa dữ liệu

- `Source` giữ `asset` dưới dạng path/URL và `full_text`; `SourceEmbedding` có `order` nhưng **không** offset gốc / page / revision. Re-embed xóa record cũ và tạo chunk mới, không có contract giữ ID/locator chunk. Khi xóa `Source`, mã xóa embeddings/insights và file upload còn tồn tại; ở đối tượng research, đây không phải bản ghi chứng cứ bất biến. `[CODE]` [embedding command](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/commands/embedding_commands.py#L313-L416), [Source.delete](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L694-L752).
- REST có thể GET notebooks/sources/notes, download originals còn tồn tại, nhưng chưa thấy **định dạng export toàn bộ data + graph edges + source IDs + checkpoint + source maps** đạt migration/roundtrip. `docs/citations.md` nói không có export/share citations. **Không dùng REST CRUD thành bằng chứng export/migrate lossless**. Migration 1–28 là SurrealQL app-state; path khác không thể tự đọc nếu không chuyển schema, edges, job state và authored notes.
- Các text source web/URL có thể thay đổi/mất truy cập; không có file immutable authority chỉ từ URL. Duplicate `content_hash` dùng SHA256 của nội dung đã co khoảng trắng để so trùng **text**, khác với SHA256 của raw original file. `[CODE]` [sources.py L190–195](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/routers/sources.py#L190-L195).

---

## 4. Feature Fit–Gap Matrix C01–C15

**Scope chấm:** *Open Notebook toàn bộ ở HEAD* nếu dùng thẳng cho BodhiAtlas V1, **không cộng điểm** cho Docling/BCR/Bang-ha khi chúng chưa tích hợp vào data contract. `NATIVE` = có code đúng chức năng mô tả, **không** hàm ý đã nghiệm thu. `CONFIG` = cấu hình bật năng lực, `EXTENSION` = có nền để sửa, `EXTERNAL` = BodhiAtlas tự sở hữu, `MISSING` = không có năng lực yêu cầu trong core đã xem, `UNKNOWN` = chưa đủ bằng chứng. Effort định tính `L/M/H/VH`, không phải person-days. `P0` = gate production, `P1` = quan trọng, `P2` = tương lai.

| ID | Năng lực | Trạng thái ON | Bằng chứng | Khoảng trống, rủi ro & công bổ sung | Ưu tiên |
|---|---|---|---|---|---|
| **C01** | Multi-format ingest | **NATIVE** (có giới hạn) | `[CODE]` E04,E14–E17 | PDF/EPUB/DOCX/HTML qua library; TEI không có parser scholarly chuyên dụng trong default pipeline; link là nguồn biến động. **H** cho manifest/format profiles, raw authority. | **V1/P0** |
| **C02** | OCR/layout/reading order | **CONFIG** | `[CODE][DOC]` E15,E16; guide engine | Docling/OCR opt-in; không đo hai cột, footnote, Hán/Nôm/Pāli/Tạng, CER/region. `simple` làm phẳng. **H**, thử theo profile; fail → PARTIAL. | **V1/P0** |
| **C03** | Canonical text & source map | **MISSING** trong core | `[CODE]` E03,E04,E13–E17 | Không immutable extraction revision, raw-to-text mapping/page/bbox/CFI; JSON Docling ở `content` không đủ. **VH**, phải tạo canonical + map ngoài. | **V1/P0 — G1/G2** |
| **C04** | Work/Edition/Witness model | **MISSING** | `[CODE]` E03 | Không tách work/translation/edition/witness/rights/file SHA và các quan hệ; topics/title không thay thế. **H–VH** catalog scholarly ngoài. | **V1/P0** |
| **C05** | Exhaustive EXACT | **MISSING** | `[CODE]` E08–E11 | BM25/LIMIT/English stemming, item topK, không char occurrences; vector fallback phá contract. **H**, viết deterministic exhaustive engine + post-verification. | **V1/P0 — no false EXACT** |
| **C06** | Normalized multilingual | **EXTENSION** | `[CODE][DOC]` E08; English snowball | Không thấy hệ derived indices reversible Pāli/Việt/đ,Hán giản-phồn,Tạng/Wylie. **H**, per-script normalizers + offset maps. | **V1/P0–P1** |
| **C07** | Fuzzy retrieval | **EXTENSION** | `[CODE]` BM25/vector ≠ edit distance fuzzy | Cần typo/OCR candidate edit distance/char n-gram + diff/false positives; chưa measured. **M–H**. | **V1/P1** |
| **C08** | Sense-aware lexicon | **MISSING** | `[CODE]` E03; `[DOC]` PRD §2.4 | Không lexeme/sense/attestation/reviewer, không tự đồng nhất bản dịch. **H**, lexicon riêng. | **V1/P1**, mở rộng V2 |
| **C09** | Semantic/RAG | **NATIVE** | `[CODE]` E12,E13 | Vector, Ask, Chat có code, phụ thuộc models; top10/nhánh mất context, citation LLM. **L** nếu research workspace, **H** nếu ghép evidence gate. | **V2/V3 optional** |
| **C10** | Verified citation/reopen | **MISSING** đối với *verified* | `[DOC][CODE]` E05–E07 | Có item-pointer & download **nếu file còn** nhưng không độc lập verify SHA/edition/page/CFI/quote. **VH**, verifier + resolver + review workflow. | **V1/P0 — G2** |
| **C11** | Wiki/notes/claims | **NATIVE** notes; **EXTENSION** scholarly claims | `[CODE]` E18; notes/insight | Notebook/notes/insights không có audited claim support, reviewer/counterevidence/revisions theo gate. **M–H** ngoại vi. | **V1/P1** ghi chú, V2 claims UI |
| **C12** | APIs/MCP/export | **NATIVE** REST; **EXTERNAL** MCP/verified export | `[CODE]` E18, [MCP community](https://github.com/Epochal-dev/open-notebook-mcp/blob/a2cddbf65cba8c4c8de7be16566781b7612a9545/README.md#L1-L15) | REST CRUD có; MCP third-party không được coi upstream/ACL; no citation export/share, full migration unknown. **M–H** adapter/export. | **V1/P1** API, **V2** workspace |
| **C13** | Coverage/incremental | **MISSING** scholarly coverage | `[CODE]` E03,E05,E13 | Có command status và re-embed, nhưng không manifest missing pages, OCR coverage, extraction version/immutable rebuild. **H** quality pipeline. | **V1/P0 — G1** |
| **C14** | Auth/privacy/license/backup | **CONFIG** basic; **EXTERNAL** source ACL | `[CODE][DOC]` E19–E21,E30 | Password chung, localStorage, API port, secrets, no source-level roles; rights & restore per file chưa chứng minh. **H** vận hành/hardening hoặc isolate. | **V1/P0** |
| **C15** | Operability/portability | **NATIVE** deploy; **EXTENSION** portable V1 | `[CODE][DOC]` E01,E02,E20 | 2 Compose services/4 process roles, Surreal migrations, SQLite checkpoints, image tag floating. Không phải drop-in replace. **M–VH** migration/upgrade. | **V1/P0** |

**Hard-gate verdict hiện tại:** G1 **NOT DEMONSTRATED / code gap**; G2 **NOT DEMONSTRATED / code gap**; G3 **NOT DEMONSTRATED / code gap**; G4 external rights **NOT TESTED**; G5 scholarly sense **code gap**; G6 publish **NOT DEMONSTRATED**. `C05 exhaustive EXACT`: **code gap**. Bảng trên không được diễn giải như đã chạy một test và thấy FAIL thực nghiệm; chỉ cho thấy **không thể cấp PASS theo bằng chứng hiện có**.

---
## 5. Deep Technical Findings

### A. Open Notebook là app, thư viện, dịch vụ hay roadmap?

**App đã có mã:** Next.js frontend → FastAPI/routers → SurrealDB/domain, worker `surreal-commands`, LangGraph workflows, Esperanto model abstraction; multi notebook, notes, search, Ask, source upload, transformations/insights và podcast. `api/routers` chứa các router sources/notebooks/notes/search/chat/insights/transformations/config/credentials; hướng API-first là thật. Có sự khác nhau giữa **quyền dùng ứng dụng** và **khả năng trích một package như library**: code `Source`, `Note`, `Search` phụ thuộc RecordID, SurrealQL, command queue và schema, nên dùng từ “chỉ import vài module” sẽ đánh giá thấp công tích hợp. [Architecture](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/7-DEVELOPMENT/architecture.md#L36-L107). `[CODE][DOC]`

**Thư viện đã tách:** `content-core` chạy trích xuất độc lập, `esperanto` chọn provider; `surreal-commands` có thể dùng độc lập nhưng kéo SurrealDB; không phải “framework plugin” cần viết lại. [Content Core API](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/extraction.py#L50-L97), [Esperanto README](https://github.com/lfnovo/esperanto/blob/343e0a9f874cb9a4339f2bc21817add4c296daa6/README.md#L9-L25), [Surreal Commands README](https://github.com/lfnovo/surreal-commands/blob/2abbdd7f4581b9f3514669721cb949f536cc2a87/README.md#L1-L25). `[CODE][DOC]`

**Dịch vụ độc lập:** triển khai Open Notebook bên ngoài lõi BodhiAtlas là khả thi trên mặt hợp đồng REST hiện hữu; dùng `POST /api/notes`, `GET /api/notes`, `GET /api/sources`, `POST /api/search` để phục vụ nghiên cứu. Tuy nhiên việc đồng bộ citation authority phải là **một chiều, BodhiAtlas → workspace**, không chia sẻ một bảng Surreal `source` làm catalog chuẩn. Việc Open Notebook có endpoint `GET /sources/{id}/download` là điểm cộng hạn chế, nhưng mặc định auto-delete upload và thiếu Work/Edition khiến nó chưa là canonical document reader. `[CODE]`

**Kế hoạch, không phải feature:** discussion #1315 đề xuất standalone Search–Evidence–Provenance component và local MCP read-only; thảo luận mô tả evidence knowing provenance/position/validity, tương phản mạnh với code hiện tại. Việc một maintainer thừa nhận chưa đạt trích dẫn passage-level là **bằng chứng phản biện** cho nhận định “có citation = verified”. Dự án ở trạng thái direction/exploration không có ETA; chưa tìm thấy `evidence-core` ở danh sách repo tên khớp owner `lfnovo` hoặc dependency tương ứng ở `pyproject`. Chưa có artifact/release/test evidence-core độc lập được xác minh ở snapshot này. **Không dùng vNext để chọn kiến trúc V1**. [#1315](https://github.com/lfnovo/open-notebook/discussions/1315), [Vision](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/VISION.md#L49-L75). `[PLAN][UNKNOWN]`

### B. File gốc, hai ấn bản và citation — điểm then chốt

`Source.asset` chỉ `file_path/url`; `Source.full_text` là string; `source_embedding` chỉ `source, order, content, embedding`. Không có các trường bất biến **`file_sha256`, `work_id`, `expression_id`, `edition_id`, `witness_id`, `translator_id`, `extraction_run_id`, `source_span`, `pdf_page_index`, `printed_page_label`, `bbox`, `EPUB href/CFI`, `TEI XPath`, `OCR page_coverage`** trong các model/migration cốt lõi đã xem. Không hợp lệ lấy `title`, `topics` hoặc `order` để suy ra các trường này. [Domain](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L335-L461), [migration1](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/1.surrealql#L2-L26). `[CODE]`

**Quan sát dễ bị bỏ qua:** `src/content_core/processors/document/docling.py` cho xuất JSON của `DoclingDocument` như string `ExtractionOutput.content`; mặc định là Markdown, và Open Notebook ghi **nguyên string** vào full_text, không parse `doc.prov` thành bảng `SourceSpan`. Do đó “Docling upstream có bbox” không chứng minh “Open Notebook đã lưu và index bbox” hay “citation UI có highlight đúng tọa độ”. Nếu cấu hình JSON mà vẫn đưa vào FTS/embedding như text thường, việc tìm kiếm còn có thể bị nhiễu JSON keys/escaping; đây là **[INFERRED] cần test**, không phải benchmark. [Docling wrapper](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/processors/document/docling.py#L129-L145), [save_source](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L349-L383).

**Raw reopening: nhận định cân bằng.** Open Notebook **có** endpoint download raw uploaded file, tránh kết luận sai rằng không thể lấy file trong mọi tình huống. Tuy nhiên nó chỉ `FileResponse` đường dẫn nếu file còn; không có hàm chứng thực hash bytes độc lập, bắt đúng ấn bản, PDF printed page offset, EPUB CFI, char-range hay source citation verifier. Mặc định setting `auto_delete_files=yes` làm nguy cơ mất file cao; nút download chỉ phản hồi khi file còn. Cần POC kiểm UI sử dụng flag trên cả upload async/sync, tránh suy diễn mặc định trên mọi request API. `[CODE]` E05–E07.

**Citation UI** parse string kiểu `[source:abc]`, `[note:def]`, `[insight:ghi]`, biến chúng thành clickable reference, không tự gọi resolver mở file gốc/so quote. Câu chỉ dẫn `prompts/source_chat/system.jinja` bảo model không bịa ID không phải enforcement (một model có thể làm sai prompt). Citation đúng ID nhưng sai edition/negation vẫn có thể được hiển thị như liên kết. `docs/citations.md` nói minh bạch: model chọn citation, đôi lúc sai, người dùng phải tự kiểm. Đây là một cơ chế **navigation hint** chứ không phải G2 `TEXT_AND_LOCATOR_VERIFIED`. `[CODE][DOC]` E07.

### C. Search / Ask / Chat và hợp đồng code-only EXACT

1. **Search:** `POST /api/search` chọn `type=text|vector`. Text đi `fn::text_search`; migration cuối cùng xác định hành vi là `26.surrealql` (migration 27/28 không sửa function). Query qua analyzer `blank,class,camel,punct`, `snowball(english),lowercase`, tính BM25, GROUP BY item và ORDER score rồi `LIMIT`. Kết quả gần với “item/record có liên quan”, không phải toàn bộ substring occurrences. `total_count` = độ dài mảng kết quả sau LIMIT, **không là corpus total**. `[CODE]` E08–E11.
2. **Ngữ nghĩa exact:** matching token/stem có thể bỏ hoặc thêm biến thể; English stemming làm thay đổi loại khớp; kết quả không chứa `start/end` offset chuẩn. Một item chứa cùng câu 200 lần vẫn có thể là một row; query 1 Hán tự và substring giữa token không có bảo đảm recall. Search chunk phục vụ ranking khác với search cả `full_text`: không thể suy ra ứng viên đọc ở một trong hai là exhaustive. `[INFERRED]` từ analyzer/schema/`LIMIT`; hành vi Unicode thật **NOT TESTED**.
3. **Fallback ảnh hưởng integrity:** trong `text_search`, nếu `RuntimeError` liên quan highlight byte overflow, code **cố chạy vector_search**. Nếu không có embedding model, lỗi được bọc 5xx. Nếu có, semantic result được trả mà API dùng `search_type` từ request (text) thay vì observed execution mode; UI không đủ để phân biệt. Lưu ý **không phải mọi lỗi text đều fallback**: điều kiện cụ thể là error substring overflow; những RuntimeError khác bị lỗi. POC phải chủ động tạo đa byte/large content tái hiện hoặc chứng minh không xảy ra. `[CODE]` E10,E11.
4. **Ask:** graph chiến lược gọi LLM một lần, n search terms do model đề xuất (prompt nói tối đa 5, không có validator cứng `max_length=5` ở `Strategy.searches`), mỗi nhánh vector search `results=10`, một LLM answer nếu có results, rồi LLM final. Trong trường hợp model tuân prompt và có 5 nhánh có dữ liệu: **tối đa 7 lời gọi LLM suy ra từ code** (1+5+1); nếu strategy trả nhiều hơn 5, không bảo đảm bound này, và nếu nhánh empty có ít calls hơn. `ASK_MAX_TOKENS=8192` là **ngân sách output mỗi stage**, không phải token đã sử dụng/chi phí dự kiến. Bất kỳ nguồn nằm ngoài vector top10 hay không embedded sẽ bị bỏ qua; citations cuối do model tạo. `[CODE]` E12, [test Ask mock](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/tests/test_ask_graph.py#L46-L110).
5. **Chat:** notebook/source-chat dùng LangGraph checkpoint SQLite, xây context từ notes/insights/source theo lựa chọn; LLM tạo đáp án, không tự tương đương `EXACT` query. `get_context(short|long)` có id/title/insights/full_text tùy mode; nếu context dài bị giới hạn/truncate hoặc source ở “insights only”, một đoạn có thể vắng mặt. Không dùng Chat để kết luận tài liệu không có từ hay một claim đã được kiểm. `[CODE][DOC]` [Source.get_context](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L524-L544), [Search guide](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/3-USER-GUIDE/search.md#L46-L75).

**Consequence:** code-only Text Search bình thường có thể chạy không cần LLM/embedding, đó là một tính năng thật; **không đáp ứng “code-only exhaustive EXACT” của BodhiAtlas**. Nên cấm đặt nhãn `EXACT` cho response `/api/search` kể cả khi query tình cờ đúng; nhãn `RETRIEVAL_CANDIDATE_TEXT` hoặc “FTS text hit” chính xác hơn.

### D. Ingestion: Direct Docling, Content Core wrapper hay full Open Notebook?

| Engine / cách dùng | Có trong code | Dữ liệu trả về | Vấn đề V1 |
|---|---|---|---|
| **Content Core `simple` PDF** | `pdfplumber` rồi `clean_pdf_text()` | một string, có thể ghép bảng thành Markdown | Rủi ro đọc sai 2 cột, mất pages/bbox, gộp dấu gạch nối, mất raw character evidence |
| **Content Core `simple` EPUB** | `fast_ebook.read_epub(...).to_markdown()` | string | mất original href/spine/CFI và xref qua `ExtractionOutput` |
| **Content Core DOCX** | `python-docx`/Markdown | string/heading/table | không phải source map byte/paragraph immutable; footnotes cần kiểm riêng |
| **Content Core URL** | URL processor auto, Jina/Firecrawl/Crawl4AI/simple, YouTube | text + metadata tùy path | nguồn biến động, remote service/JS/SSRF/rights, không snapshot immutable tự động |
| **Content Core Docling** | optional `DocumentConverter`; OCR/formula/vision flags | `export_to_markdown`, `export_to_html`, hoặc `export_to_json` thành **string** | JSON có thể giữ metadata upstream nhưng wrapper không cho typed page/bbox/CFI API và ON không lưu thành source map riêng |
| **Direct Docling** | **ngoài Open Notebook**, converter trả `DoclingDocument` | nếu giữ `result.document`/JSON có thể duy trì cấu trúc và PDF provenance tốt hơn | vẫn phải kiểm map char-level/printed page/EPUB locator; không tự cho VERIFIED |
| **Full Open Notebook ingest** | `extract_content` + `Source` + embeddings | `source.full_text` và chunk vectors | thêm Surreal/worker/frontend mà không tăng bất biến nguồn đủ V1 |

**Điểm có lợi của wrapper:** một Python API `extract_content` unified, cấu hình engine/URL/media và errors; có thể tận dụng V1 **chỉ cho extraction nhanh và tài liệu không rủi ro cao**, đồng thời chạy Direct Docling cho PDF khó. Nhưng nếu điều kiện V1 là phải có **một source map tài liệu có cấu trúc duy nhất** thì lập tức **không dùng string wrapper làm dữ liệu có thẩm quyền**; dùng `DoclingDocument` direct (với serialized JSON artifact) hoặc parser theo định dạng gốc, sinh `SourceSpan` rồi map toàn vẹn. Không tự viết wrapper trừ khi POC chứng minh reuse tiết kiệm file/code. `[CODE]` [Content Core routing](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/extraction.py#L142-L300), [Docling](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/processors/document/docling.py#L101-L145).

**OCR/QA:** mã cho thấy toggles tồn tại và Docling OCR chạy nếu optional dependency được cài; **không có số đo CER/WER, character-level locator accuracy, layout page coverage, confidence threshold hay hiệu năng** trên PDF chữ, PDF scan 2 cột, Hán/Nôm/Pāli có dấu, EPUB, DOCX, HTML/TEI thuộc BodhiAtlas. Không được suy chất lượng Hán/Tạng từ “Docling supports OCR”. Với `content-core` simple PDF còn có test source xác nhận `ﬁ→fi`, `word-\nbreak→wordbreak`, co whitespace — đây là biến đổi text, không phù hợp dùng làm **bản nguyên văn nguyên trạng** nếu không có mapping có kiểm. `[CODE]` [test PDF](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/tests/unit/test_pdf_extraction.py#L12-L38).

**Engine fallback:** `content-core` khi `document_engine=docling` mà runtime không có thì raise cấu hình; `auto` route sang simple nếu Docling unavailable, còn Open Notebook `_usable_engine` có thể đổi engine không còn runtime sang `auto` để ingestion tiếp tục. Điều này hữu ích về UX nhưng bắt buộc phải ghi **engine thực tế + version + model + pipeline flags + output checksum** vào extraction revision; không được để một file bị xử lý bằng parser khác rồi tự giữ trạng thái `READY` như cũ. `[CODE]` [routing](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/extraction.py#L142-L179), [graph engine](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L79-L98).

### E. Notebook, ghi chú, insights và tiết kiệm code/token

**Năng lực reuse thật:** tạo nhiều notebook, một source có quan hệ `reference` tới nhiều notebook, notes có `artifact` edge, Source Insight theo transformation, notes CRUD, download original khi còn, giới hạn context short/long, Search/Ask qua API, external `open-notebook-mcp` bridge bên thứ ba. App phù hợp cho nhà nghiên cứu muốn quản lý câu hỏi, ghi chú và hỏi đáp trên tài liệu, không phải xây UI từ đầu. [domain notebook](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L36-L107), [notes](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/routers/notes.py#L17-L118). `[CODE]`

**Chi phí ẩn nếu chọn làm core:** sửa Source schema/Surreal migrations, parser pipeline, chunk offsets, search API, all-corpus EXACT, viewer, citation UI, OCR QA, edition/work identities, permission and review state; mỗi upstream release có thể đụng Graph/Surreal/Next; phải backfill bản `source.full_text` vốn mất provenance. Reuse UI chỉ đáng giá nếu nhu cầu workspace research lớn và **không bắt tích hợp trực tiếp vào V1 code-only**. Lợi thế token là giảm thời gian xây UI ở demo, **không phải giảm token runtime**: Ask/Chat chủ động gọi model; `content-core` simple và deterministic search không gọi LLM. Không có đo token/tiền/tốc độ; kết luận chỉ là [INFERRED].

**Evidence Card integration** có thể thử `POST /api/notes` với `note_type=human`, `title` do caller chọn và `content` chứa **JSON envelope/Markdown có đường dẫn** đến BodhiAtlas. Đây là phép **chiếu dữ liệu 1 chiều**: BodhiAtlas giữ file hash/locator/review state có thẩm quyền; Open Notebook chỉ giữ bản hiển thị có thể xóa. `source_id` của Open Notebook là ID Surreal **không thể** thay thế canonical `file_id`, không được dùng để suy ra ấn bản. `Note.save()` tự gửi `embed_note` worker khi có nội dung; cần thử khi embedding chưa cấu hình, hạn chế egress/budget và không mặc nhiên hứa “notes hoàn toàn không tạo job”.

### F. Evidence Core roadmap và đánh giá khả năng thay BCR verifier

Discussion #1315 (05/09/2026, maintainer) nêu việc chia search/research bằng một **evidence contract** chứa content, origin, original/derived/authored, vị trí trong file và citation do code validate; còn gọi thiết kế **standalone MIT component**. Đây là định hướng nhất quán với G1–G3 nhưng bản thân discussion ghi *not commitment/no dates*. Source Open Notebook HEAD vẫn dùng model-selected item IDs và Surreal BM25 chunk search, không có function/source schema chứng minh contract mới đã triển khai. Search repo owner `lfnovo` cho tên `evidence-core` ngày truy cập cho **0 match**; đây là bằng chứng **NOT LOCATED**, không phải exhaustive internet proof; có thể tên/package khác hoặc PR chưa release, vì thế trạng thái release/interface/tests `UNKNOWN`. `[PLAN][CODE][UNKNOWN]` [#1315](https://github.com/lfnovo/open-notebook/discussions/1315).

**Quy tắc thay thế BCR verifier:** không thay dù roadmap có tiêu đề phù hợp; cần kiểm package/version, API `verify(source bytes SHA, edition, span locator, quote)`, expected statuses, adversarial false-verified, source-reader trust boundary, errors fail-closed, source-mapping cross-format, export/rebuild stability, review ownership, production test. BCR `verification.py` hiện đã có code keyed pinned source và `source_reader` độc lập cho một số corpus, vì vậy thay bằng ý tưởng chưa phát hành là bước lùi ở những nguồn đã hỗ trợ. `[CODE]` [BCR verification](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/verification.py#L1-L57).

### G. Security, deploy, license, upgrade, resource boundaries

**Thay đổi tích cực phải ghi nhận:** `source.py` tái kiểm URL ở extraction worker và path upload containment; source URL validation kiểm IP nguy hiểm và có cơ chế target pin ở một số luồng, release v1.15.1 gọi là security release với URL hardening. Do đó không đánh giá sai rằng “Open Notebook hoàn toàn không có chống SSRF”. Nhưng phải thử redirect hop/HTTP client cụ thể, DNS rebinding, provider endpoint, remote Docling vision và network egress; đọc code không thay penetration test. `[CODE][DOC]` [source.py L175–193](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L175-L193), [release](https://github.com/lfnovo/open-notebook/releases/tag/v1.15.1).

**Rủi ro kiến trúc:** basic shared-password là ranh giới toàn app; không có source-level ACL/RBAC. Khi không set `OPEN_NOTEBOOK_PASSWORD`, auth disabled; khi set, CORS mặc định wildcard nếu không hạn chế. Với password unset, bản hiện tại **không mặc nhiên CORS `*`**, thay vào đó có same-host/localhost policy; không lặp lại nhận xét cũ sai thời điểm. Password nằm trong localStorage UI. Compose mặc định database `root:root`, app password trống, encryption placeholder; image `v1-latest` floating. **Không deploy nguyên Compose mặc định lên LAN/VPS**. `[CODE][DOC]` [security](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/5-CONFIGURATION/security.md#L144-L217), [main CORS](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/main.py#L83-L114).

**Offline:** Esperanto hỗ trợ Ollama, OpenAI-compatible và Transformers; Docling local có thể chạy không cloud cho extraction (tùy OCR/model/image flags). Có thể dựng profile local-only trên mặt code; **offline hoàn toàn chưa được chứng minh** cho tổng thể Open Notebook + URL lookup + provider creds + telemetry/dependency downloads + model assets. Muốn tuyên bố offline phải chạy POC network-denied và inspect outbound connections. `license MIT` của ON/Content Core/Esperanto **không** cấp quyền cho bytes sách, bản dịch, OCR/VLM weights, nền tảng model hoặc quyền đưa nội dung lên provider. POC G4 và data-egress bắt buộc.

**Backup/upgrade:** `docker-compose` mounts `./surreal_data`, `./notebook_data`; cần backup consistent cả DB, SQLite checkpoints, uploads nếu giữ, provider encryption secret và model/pipeline config; restore có chạy migration phiên bản ghim rồi đối chiếu hash, graph edges, verified evidence references. Surreal v3 và thay worker/Celery chỉ nêu ở VISION/horizon, **[PLAN]** không phải chức năng có sẵn. Backups/restore và upgrade across stable→main **NOT TESTED**. [Vision](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/VISION.md#L49-L75), [security backups](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/5-CONFIGURATION/security.md#L188-L217).

---

## 6. Source Fidelity & Provenance

### 6.1. Failure trace: `raw → extract → text → chunk → result → cite → reopen`

| Giai đoạn | Dữ liệu ON thực có | Bất biến BodhiAtlas yêu cầu | Mất/giả trust tại đâu? |
|---|---|---|---|
| `RAW` | uploaded file path/URL; file bytes có thể bị xóa | immutable file bytes + SHA256 + rights + work/edition/witness | **Tại ingress:** thiếu data model/file hash/persistent-retention gate; URL mutable |
| `EXTRACT` | `ExtractionOutput(content,title,...,metadata)` | per-file extraction version, per-page/region coverage, engine/model/pipeline hash | **Tại interface:** metadata chỉ generic; Docling JSON có thể đóng vào string |
| `TEXT` | `source.full_text = extraction.content` | canonical exact extracted text + structure roles + source map | **Tại save_source:** không persist structural mapper/extraction metadata |
| `CHUNK` | `source_embedding(order,content,embedding)` | offsets sang canonical text, extraction revision, no loss from chunking | **Tại embed_source:** không start/end, overlap và splitter không làm source locator |
| `RESULT` | Surreal text/vector ranked items, top LIMIT, highlight strings | all EXACT occurrences with offsets, manifest scope and result type | **Tại fn::text_search:** group/LIMIT/truncation; fallback vector trên một lỗi |
| `CITE` | model-selected `source:...` / note / insight | quote + file hash + edition + locator + independently checked status | **Tại LLM/UI:** link item, không chứng nhận quote hay semantic support |
| `REOPEN` | `GET /sources/{id}/download` nếu tồn tại bytes | mở đúng PDF file page + printed label/bbox hoặc EPUB CFI, so context | **Tại download:** không xác định đúng span, không đảm bảo giữ file |

**Bất biến đề xuất (không gán là code ON):**

```text
Work(work_id) --has_expression--> Expression(expression_id, language, translator)
 Expression --has_edition--> Edition(edition_id, imprint, date, pagination_system)
 Edition --has_witness--> Witness(witness_id, provenance, variant_role)
 Edition/Witness --has_file--> File(file_id, sha256_bytes, mime, bytes_uri, rights_policy)
 File --has_extraction--> Extraction(extraction_id, engine_version, content_sha256,
                                     status, page_manifest, extraction_config)
 Extraction --has_span--> SourceSpan(span_id, canonical_start, canonical_end,
                                    structure_role, PDF_page_index/printed_page/bbox
                                    OR EPUB_spine_href/CFI OR HTML/TEI_xpath,
                                    locator_quality)
 SourceSpan --derives--> SearchIndex (regenerable, untrusted candidates)
 EvidenceCard(evidence_id, quote, work_id, edition_id, file_id, file_sha256,
              extraction_id, span_id, verification_status, reviewed_by, reviewed_at,
              claim_relation_status, rights_status)
```

**Ba trạng thái tách:**
- `ingest_state` = `READY | PARTIAL | OCR_UNCERTAIN | NOT_INDEXED | SOURCE_UNAVAILABLE`;
- `technical_citation_state` = `CANDIDATE | TEXT_ONLY | TEXT_AND_LOCATOR_VERIFIED | OCR_NEEDS_REVIEW | MISMATCH | UNVERIFIABLE | REJECTED` (muốn dùng `VERIFIED` alias chỉ khi đạt `TEXT_AND_LOCATOR_VERIFIED`);
- `claim_relation_state` = `NOT_ASSESSED | SUPPORTS | PARTIAL | CONTRARY | DISPUTED | INSUFFICIENT`.

**Quyền cấp verified:** chỉ trusted BodhiAtlas code verifier đọc *file bytes* theo `file_id/SHA`, dùng source-specific locator resolver từ parser trusted và đối chiếu quote/context rồi **human reviewer khi OCR/layout/semantic có rủi ro**, được phép nâng `technical_citation_state`. LLM, external workspace và search ranking **không có quyền** nâng bất kỳ trạng thái nào; *technical verified* không tự suy ra `SUPPORTS`. `claim_relation_state` có thể được gợi ý bởi AI nhưng hội đồng/người nghiên cứu phải duyệt kết luận học thuật quan trọng. Theo [Risk G2/G3](https://github.com/quocgempro361/bodhi-atlas/blob/aa874008ff4c6a6e9d66e6fee34c55e0370d6820/docs/ACADEMIC_RISKS_AND_VERIFICATION.md#L154-L165). `[DOC][INFERRED: design]`

### 6.2. Ví dụ adversarial giả định — **không phải POC đã chạy**

Giả định *Edition E1*: PDF `sha256=A`, trang PDF 7, trang in “5”, câu **“Tác giả không chấp nhận giả thuyết X.”**; *Edition E2*: PDF `sha256=B`, trang PDF 9, trang in “7”, câu **“Tác giả chấp nhận giả thuyết X.”**; scan E2 bị OCR sai, tự thêm “không”. Cả hai có title “Bài khảo luận X”. `[HYPOTHETICAL / NOT TESTED]`

- Với Open Notebook, Search có thể trả cả hai item; item citation `source:...` không đủ chứng minh câu thuộc E1 hay E2, không có page/bbox; nếu original đã auto-delete thì reader không còn bytes để so.
- BodhiAtlas phải **không gộp theo title**, dùng `file_sha256` E1/E2, `edition_id`, `extraction_revision`, `pdf_page_index`, `printed_page_label`, `bbox`, `quote`. E2 OCR chứa từ “không” nhưng ảnh gốc không có ⇒ `OCR_NEEDS_REVIEW` hoặc `MISMATCH`, tuyệt đối không `TEXT_AND_LOCATOR_VERIFIED`. Một citation AI bịa `source:X` nhưng ID không tồn tại phải thành `REJECTED`/`UNVERIFIABLE`, không được hiển thị như VERIFIED.
- Khi file PDF thiếu trang 7, tra cứu 0 kết quả không cho phát biểu “không có câu”; trạng thái phạm vi `PARTIAL/MISSING_PAGE`. Khi hai đoạn cùng quote giống nhau trong một file, verifier cần locator cụ thể và xử lý ambiguity, không chọn tùy tiện occurrence đầu tiên.

**Phép kiểm fail-closed đề xuất:** `verify_card(card)` đọc canonical `file_id` từ catalog trusted, đọc bytes immutable, xác nhận SHA256, xác nhận edition/witness, tìm locator trong bản extraction được ghim, đối chiếu sequence Unicode nguyên trạng + ngữ cảnh, kiểm coverage/loc_quality và nếu OCR rủi ro thì yêu cầu visual/human review. Mọi lỗi I/O/hash/locator/ambiguous/partial trả nhãn không verified **kèm lý do**, không fallback vector search/AI. `citation.open_uri` sinh từ source-specific resolver có thể bị thu hồi nếu quyền không cho chia sẻ; lưu audit trail. **Chưa implement/test ở đây.**

---

## 7. Multilingual & Retrieval Behavior

**Phân loại bảng:** `PREDICTED` = suy ra từ FTS analyzer/code, không phải kết quả thực thi; `REQUIRED` = truth của fixture/lý thuyết contract (với canonical text do fixture cung cấp); `MEASURED` = không có vì chưa chạy Open Notebook. EXACT được định nghĩa trước thí nghiệm: *match chuỗi codepoint nguyên trạng trong canonical extracted text*; nếu muốn `NFC` tương đương phải trả loại `NORMALIZED`, không đổi tên chế độ. Chọn rõ case, whitespace, line-break, grapheme và page-boundary policy, bởi raw PDF bytes ≠ extracted text.

| Test ID | Query / dữ liệu chuẩn chứa | EXACT bắt buộc | NORMALIZED/FUZZY/LEXICON được tách | Dự báo từ code ON (`NOT TESTED`) |
|---|---|---|---|---|
| U01 | `anatta` vs `anattā` | `anatta` chỉ khớp nguyên chuỗi tương ứng; `ā` không tự bằng `a` | diacritic-folded về một nhóm có metadata phép chuyển | English snowball/lowercase không chứng minh Pāli fold, thiếu reversibility |
| U02 | `nibbāna` vs `nibbana`, `duḥkha` vs `duhkha` | phân biệt dấu phụ | index phụ có map char offsets | FTS token relevance khác normalized recall |
| U03 | `vô thường` vs `vo thuong` | khác | VI tone-fold + reversible span; ambiguous candidate | analyzer English không chứng minh strip diacritics |
| U04 | `đạo` vs `dao` và `đ` vs `d` | khác | map rõ `đ→d` riêng, không giả NFD đã làm | Unicode NFD không chuyển `đ` thành `d`; nên không thể dựa vào strip combining |
| U05 | `Á` (NFD) vs `Á` (NFC) | khác dãy codepoint | `NORMALIZED_NFC`, mapping tới gốc | FTS index/case rules không cấp exact mode identity |
| U06 | `無常` vs `无常` | khác | Chinese simp/trad mapping qua canonical relation, có ambiguity | Không có code simp/trad index verified trong paths đã đọc |
| U07 | `無` một chữ; `常` trong chuỗi liền nhau | tất cả substring theo index scope | CJK tokenizer/char n-gram candidate | `blank,class,camel,punct`/BM25 không đủ chứng minh 1 Han char/substring recall |
| U08 | Hán 2 chữ `無常` trong đoạn liền không khoảng cách | tất cả start/end | variant search tách | FTS item topK không phải tất cả occurrences |
| U09 | Tạng Unicode / Wylie, query 1 token | EXACT script gốc | Wylie→Tibetan chỉ nếu quy tắc có, nghĩa qua sense | không thấy Wylie scholarly module cốt lõi |
| U10 | `anattā` lặp 10 lần trong 1 source | **10 offsets** | ranking candidate có thể gộp source | FTS GROUP BY ra 1 item, API `total_count=1` không là 10 |
| U11 | `not true` / `true` với từ phủ định và OCR thiếu “not” | phân biệt context/role; OCR mismatch fail G2 | fuzzy chỉ ứng viên có diff | text ranking/AI citation không verify phủ định |
| U12 | cụm dài vượt 400-token chunk hoặc qua ranh trang | EXACT full canonical string nếu liên tục theo policy | context candidate cho phép search | embedding topK/chunk không bảo đảm; full_text FTS cũng không trả offsets |
| U13 | punctuation và xuống dòng | exact theo policy đã định | whitespace-normalized riêng | analyzer punctuation không giữ semantics exact |
| U14 | phrase trong HTML/TEI DOM splits | original DOM text position, struct role | normalize chỉ nếu có stable map | full-text flatten mất XPath/role |
| U15 | file thiếu trang, query không có match | `NO_MATCH_IN_INDEXED_SCOPE` + `PARTIAL` | không suy ra claim absence | API count=0 không báo coverage |
| U16 | một query có >1000 matching items | cursor/page across all items + all positions | paging deterministic | SearchRequest limit max 1000, count len(results) |
| U17 | query trigram `ana` ở giữa token | cần substring match theo exact contract | spell candidates | English token match không bảo đảm infix |
| U18 | mixed Hán/Pāli/Việt chứa NFD + superscript footnote | cần offset map chính xác và role | index riêng, mapping reversible | processor string có thể mất font/footnote/run boundaries |

**Điều gì chắc bằng code:** search API có limit default 100/max1000; `fn::text_search` chỉ trả item-level và `LIMIT`; analyzer có English snowball; fallback vector trong một nhánh lỗi; Ask always uses vector top10/term. **Điều chưa biết bằng measured:** tokenization SurrealDB v2 đối với Han 1–2 ký tự và `đ`, search::highlight behavior multi-byte, percentage false positives, 50-query recall, 2-column OCR CER, word boundaries, across-chunk recall sau re-index. Một kết luận về chính xác Unicode phải xuất ra **số đếm / offsets / false-positive log** của fixture, không suy từ tên analyzer. `[CODE][UNKNOWN]`

**Hợp đồng tìm kiếm khuyến nghị cho V1 (independent engine, chưa implement):**

```json
{
  "query": "anattā",
  "requested_mode": "EXACT",
  "executed_mode": "EXACT_CODEPOINT",
  "scope": {"extraction_ids": ["ext:1"], "coverage": "PARTIAL"},
  "total_occurrences": 3,
  "occurrences": [
    {
      "file_id": "file:1", "edition_id": "edition:1", "extraction_id": "ext:1",
      "canonical_start": 15, "canonical_end": 21,
      "match_kind": "EXACT", "source_span_ids": ["span:2"],
      "technical_citation_state": "CANDIDATE"
    }
  ],
  "next_cursor": null,
  "complete_within_indexed_scope": true,
  "warnings": ["One PDF page not extracted; scope is partial"]
}
```

*Ví dụ schema minh họa, **không phải JSON đã trả từ Open Notebook**. `total_occurrences` phải đúng cả khi phân trang, có thể tính riêng hoặc streaming count; nếu timeout phải trả `complete=false`, không khai đã tìm hết. `start/end` half-open theo codepoint canonical, không được dùng như byte offsets PDF hoặc CFI.*

---

## 8. Integration Options for BodhiAtlas

**Một bài toán chung để so sánh, không “chấm điểm vì feature”:** nhập khoảng 50–100 tài liệu thử có file gốc/edition/witness, scan 2 cột, PDF chữ, EPUB, DOCX, HTML/TEI; giữ raw SHA, canonical text/source map/page manifest; tra 50+ exact/normalized/fuzzy queries trả *tất cả* occurrence và vị trí; verify technical citations độc lập; no LLM path; tùy chọn research notes và model. Không giả có kết quả POC.

### 8.1. Năm phương án nguyên vẹn, phần phải tự viết và state ownership

| PA | Core authority & state | Phải tự phát triển còn lại | Vận hành / duplication / lock-in / rollback | Đánh giá |
|---|---|---|---|---|
| **A — Open Notebook-first** | SurrealDB `source/full_text/embedding`, filesystem/SQLite trong ON | `File/Work/Edition/Witness`, revision/source map/coverage, verifier, EXACT engine, lexicon, evidence reader, claim gates; sửa API/UI/schema | 2 Compose services nhưng 4 process roles, DB+SQLite+files; heavy ON fork/upstream merges, migration Surreal lock-in; rollback phải export entire source/edge/notes & reconstruct origins | **Không khuyến nghị V1**; UI demo nhanh nhất khi không phải compliant |
| **B — Bang-ha-led** | SQLite FTS/passage catalog pinned, source SHA/edition/locator có sẵn trong code | ingest general PDF/EPUB, OCR/revision/page-bbox/CFI, exhaustive char occurrence offsets, rights/reviewer QA, UI upload | SQLite có thể là single DB, corpus build tooling phức tạp/corpus-specific, source provenance theo từng adapter; rollback export SQLite/manifest; private repo governance | Cạnh tranh cho canonical corpora, không mặc nhiên tốt cho thư viện sách tùy ý |
| **C — BCR-led** | SQLite/pinned sources & trusted `source_reader`; quote verification ở schema BCR | books personal file store, PDF/EPUB parser/locator & page map, ingestion version/coverage, independent all-occurrence exact, general UI/catalog | có research/verification code mạnh; hạn chế format/source corpus, cần refactor adapters; rollback giữ pinned raw/locators | Phù hợp trích dẫn corpora pinned; **ứng viên kỹ thuật** cho verifier module |
| **D — BodhiAtlas Minimal Core** | file gốc immutable + một catalog/SQLite, versioned extraction/source spans, deterministic exact & verifier; ON không authoritative | core schemas/API, trusted validators, source-specific parser integration, minimal UI; notes UI có thể tạm đơn giản | ít state authoritative; **1 DB/core+file store** ở cấu hình nhỏ, optional ON thêm state sau; rollback không phụ thuộc ON; adapter tháo được | **Ưu tiên compliant V1** có điều kiện POC proof |
| **E — Selective Reuse** | Chỉ `content-core` parser và/hoặc Esperanto provider; **không có data/search authority** | gần như toàn bộ catalog, EXACT, provenance, UI, verifier, API như D; nếu không xây core thì không thể đạt V1 | parser dep/local-only, không Surreal/Next/worker bắt buộc; rất dễ bỏ wrapper; nhưng là **thành phần**, không phải full V1 architecture | Tốt cho extraction thử nhanh; không độc lập thay D |

**Đối chứng RAGFlow / Docling:** RAGFlow định hướng RAG/chunk/document QA, có UI và workflow nhưng không tự chứng minh bất biến file/edition/map/verified citation của BodhiAtlas; chưa audit HEAD RAGFlow trong phạm vi P56 nên mọi đánh giá chi tiết về code hiện tại **UNKNOWN**. Direct Docling là lựa chọn extractor có quyền truy cập intermediate `DoclingDocument` giàu hơn wrapper, nhưng không có catalog/search/claim verifier. Cả hai phải qua cùng POC G1–G6. Không lấy kết luận báo cáo P01/P12 làm số điểm được chứng minh ở đây.

**G1–G6 và tính tháo lắp:** A có UI lợi nhưng gần như mọi G1–G6 cần sửa; B/C có nguồn/locator hoặc verifier đáng tái dùng nhưng cần hỗ trợ đa dạng input; D có tự viết core song schema được chốt bởi PRD, dễ đưa mọi parser qua *một* contract; E không có chỗ chứa bất biến. Xếp hạng “số thư viện ít” khác “ít code core”, nên D chỉ thắng nếu POC chứng minh module/schema tối thiểu không phình thành framework tùy tiện.

### 8.2. Đường ranh D + optional ON (đề nghị)

```text
[Canonical BodhiAtlas Authority]
  raw object store(file SHA) ---- catalog SQLite/Postgres (Work/Edition/Right)
        |                                  |
  parser/direct Docling                 extract runs/source map/coverage
        |                                  |
        +-----------> canonical text <----+
                       |           |
                 EXACT code   source locator/verifier  ---> EvidenceCard signed by gate
                       |                              |
                  core REST/MCP                        |
                       |                              |
                minimal reader UI                      |
                                                       v
                 [Projection adapter, optional V2]
                  read verified card from core API -> POST /api/notes
                               |                              |
                         Open Notebook workspace (Surreal, Next, worker)
                         **display-only, no authority to verify**
```

**Adapter tối thiểu là một định dạng và hai thao tác, không plugin framework**: (a) `GET /v1/evidence/{id}` từ BodhiAtlas với bearer/service identity quyền read-only; (b) `POST /api/notes` của ON với `note_type="human"`, caller-provided `title`, `content` là envelope Markdown/JSON có canonical URL. Option (c) `GET /api/notes/{id}` đối chiếu roundtrip và ghi map `external_note_id` ở một bảng **projection** riêng; không đặt khóa ngoại authoritative tới Surreal record ID. Adapter ước tính chạm **3–5 file thuộc BodhiAtlas** (`contracts/evidence_card`, `integration/open_notebook_client`, `integration/projector`, `mapping store`, integration tests); **[INFERRED] phạm vi thiết kế**, không phải số file đã sửa, không phải ngày công. Nếu POC chứng minh REST không ổn định hoặc projection không đáng tiền, **bỏ toàn bộ adapter** và core vẫn chạy đủ. Không tự viết sync hai chiều / plugin framework/embedding bridge ở V1.

**Payload v1 minh họa (projection, không phải schema hiện hữu của ON):**

```json
{
  "schema": "bodhiatlas.evidence_card.v1",
  "evidence_id": "ev:0009",
  "canonical_url": "https://bodhiatlas.local/v1/evidence/ev:0009",
  "file_id": "file:0003",
  "file_sha256": "<64-hex-from-trusted-catalog>",
  "work_id": "work:0001",
  "edition_id": "edition:0002",
  "witness_id": "witness:0002",
  "extraction_id": "ext:0004",
  "locator": {"kind": "pdf", "pdf_page_index": 7, "printed_page": "5", "bbox": null},
  "quote": "Tác giả không chấp nhận giả thuyết X.",
  "technical_citation_state": "TEXT_AND_LOCATOR_VERIFIED",
  "claim_relation_state": "NOT_ASSESSED",
  "coverage_state": "READY",
  "rights_policy": "private-no-external-llm",
  "reviewer_id": "trusted-reviewer-id",
  "verified_at": "<timestamp from verified gate>"
}
```

Trong triển khai, `file_sha256` phải là hash thật từ file, `verified_at` không nhận từ prompt/LLM và URI phải có auth (không tự mở public). Tại ON note chỉ ghi “projection of verified BodhiAtlas card” và link; khi thông tin bản gốc thay đổi/thu hồi, adapter đánh dấu stale/xóa projection; **không** dùng deleted ON note để xóa raw BodhiAtlas. Một On source ID chỉ là cross-reference ở projection. **Bảo mật nguồn:** không copy full text hoặc raw PDF sang Open Notebook nếu quyền sách/proxy/model egress chưa qua G4; với dữ liệu cấm external LLM chỉ gửi metadata/quote đã được phép hoặc không projection.

### 8.3. Chuyển dữ liệu và rollback

| Phương án | Xuất/rollback cần tối thiểu | Có thể tháo mà không mất canonical evidence? |
|---|---|---|
| A | dump Surreal schema+edges, jobs, notes, raw upload còn tồn tại, SQLite chat, parse/restore into new schema; khó dựng locator vốn không lưu | **Không đảm bảo** |
| B | export SQLite raw tables, source manifest hashes, adapter native locators, re-index FTS | Có điều kiện, nếu format/rights không corpus-locked |
| C | export pinned corpus, contracts, evidence records, reader/resolver, reproducible index | Có điều kiện, PDF/EPUB cần external mapping |
| D | raw originals + manifest SHA, SQLite/Postgres dumps, canonical extraction versions/source spans, gold tests | **Có theo thiết kế**, vẫn phải test restore |
| E | bỏ package parser, re-run extraction từ immutable originals; preserve downstream schema | **Có theo thiết kế**, phải kiểm map stability |

**Cost caution:** không bịa person-days, VND, RAM, latency. Complexity tương đối: A code adaptation **VH**, operations **H**, model/token **H khi Ask**; B/C adaptation **H**, operations **L–M**, model token **L nếu code-only**; D core code **H**, ops **L–M**, model token **0 cho deterministic path**; E parser code **L**, product code **VH nếu đứng riêng**. Các phân hạng không là benchmark và chịu thay đổi theo kỹ năng đội phát triển, tình trạng quyền kho và lượng sách thực.

---
## 9. Practical POC / Reproduction Plan

**Trạng thái tại ngày nghiên cứu:** POC-0..POC-5 **NOT TESTED**; không có bản cài Open Notebook/SurrealDB/Docling, không cài dependencies từ GitHub trong sandbox này. Mã và migration đã đọc trực tiếp trên GitHub, không có khả năng suy từ việc đọc mã rằng API đang chạy. Các lệnh phía dưới là **kế hoạch có thể chạy**, không phải shell transcript hay kết quả đã thu được. Điểm quan trọng: ghi tách **stable release** `v1.15.1` (SHA tag `5e285b7...`) và **main** `0c1e7...`; không chạy với `v1-latest` floating rồi coi là pinned snapshot. Chạy trên private/test environment, không nhập sách chưa rõ quyền vào cloud/provider.

### 9.1. Chuẩn bị fixture & cấu trúc log — áp dụng mọi POC

Đề nghị dùng bộ dữ liệu **được phép sử dụng** gồm 12–20 file nhỏ nhưng có gold truth: (1) 3 PDF text có page labels offset, footnote, negation; (2) 2 scanned PDF, trong đó 1 PDF hai cột, 1 PDF thiếu trang; (3) 2 edition title giống nhau khác “không”; (4) 2 EPUB có spine/anchor và đoạn lặp; (5) DOCX có heading/footnote/table; (6) HTML/TEI với XPath, inline note; (7) corpus plain UTF-8 NFC/NFD tiếng Việt, Pāli, 1–2 Hán tự, Han variants, Tạng/Wylie; (8) nguồn website đã lưu snapshot và checksum, không fetch nội dung động chưa được phép. **Người nghiên cứu tự tạo/đính fixture có quyền, không dùng source có bản quyền ngoài kiểm soát.**

```text
p56_poc/
  fixtures/raw/               # PDFs/EPUB/DOCX/HTML/TEI -- immutable during run
  fixtures/gold_sources.jsonl # file_id, edition_id, expected_sha256, rights, page labels
  fixtures/gold_pages.jsonl   # file_id, page_idx, printed_label, OCR/layout expected
  fixtures/gold_queries.jsonl # >=50 queries: query, mode, scope, [(file_id,offsets)]
  fixtures/gold_cards.jsonl   # positive/negative quote + correct locator/edition
  snapshots/release/          # frozen config, image digest, schema migrations, env-redacted
  snapshots/main/
  outputs/raw_extract/{engine}/
  outputs/search/{mode}/
  outputs/verification/
  outputs/metrics.jsonl
  outputs/manifest.json       # hash, code SHAs, library versions, model versions, rights
  outputs/logs-redacted/      # PII/secrets omitted
```

**Metrics bắt buộc:** input SHA256 (bytes), extractor name/version/pipeline config, output content SHA256, pages total/extracted/missing/low confidence, `char_count`, ground truth exact occurrences, `TP/FP/FN` char offsets, normalized transform mapping, `% verified citation false acceptance` (phải là 0 trong adversarial set), unknown/partial rate, `returned_count`, `true_total_occurrences`, `time_ms` p50/p95, max RSS MiB, disk bytes (raw/DB/SQLite/cache), remote calls, model/provider ID, prompt/completion tokens đo từ usage, HTTP status/errors. Không lấy billing estimate thay runtime usage.

### POC-0 — Deploy pinned stable và main theo 2 môi trường tách biệt

**Chuẩn bị:** Docker+Compose, Git (internet truy cập GitHub), Python+uv, bộ biến bí mật nội bộ, ổ lưu trữ, mô hình local nếu đo Ask, nguồn được phép. Pin **`v1.15.1` tag** và **`main` commit `0c1e7...`**; Docker image pin digest đọc từ registry sau khi resolve (không bịa digest). `OPEN_NOTEBOOK_PASSWORD`, `OPEN_NOTEBOOK_ENCRYPTION_KEY`, `SURREAL_USER/PASSWORD` tự cấp không dùng mẫu, bind 5055/8502 vào loopback hoặc reverse proxy private, không bật cloud providers. Dùng hai compose projects/volumes riêng, không trộn migrations.

```bash
# LỆNH DỰ KIẾN -- chưa chạy; chỉ trên máy được phép truy cập mạng/registry
mkdir -p p56_poc/snapshots/{release,main}
git clone https://github.com/lfnovo/open-notebook.git p56_poc/on-release
git -C p56_poc/on-release checkout 5e285b7a2e435895c4ee99ad7e4b8d2af64c3239
git clone https://github.com/lfnovo/open-notebook.git p56_poc/on-main
git -C p56_poc/on-main checkout 0c1e7abbd77411057d8feef02fc4588ec9a556d6
# Configure unique secrets, tagged/sha-pinned app image or build from the checked-out commit.
# docker compose -p p56_release -f <PINNED_COMPOSE> up -d --build
# curl --fail http://127.0.0.1:5055/openapi.json > snapshots/release/openapi.json
# docker compose -p p56_release ps
# docker compose -p p56_release logs --no-color > outputs/logs-redacted/release.log
```

**PASS:** UI/REST, SurrealDB, worker/command pipeline đều health/functional; no default secrets, machine reachable only authorized; pinned image/commit captured; no remote egress unauthorized; 1 harmless fixture note/source round-trip. **FAIL:** password absent exposed, worker cannot read model/settings/queue, version drift, no files after service restart, raw source accidentally sent ngoài. **Không cho phép:** kết luận POC-0 chứng minh G2/EXACT.

### POC-1 — Extractor parity và source preservation

**Đối chứng cùng file bytes (sha256 trùng):** `content-core` `simple`, `auto`, `docling` optional, Open Notebook full ingest với embed=false, **Direct Docling** lấy `DocumentConverter.convert(path).document` và xuất JSON **cùng config OCR**. Engine/context/flags phải log đúng để so apple-to-apple. Kế hoạch script sau dùng API library, không có bảo đảm CLI upstream đúng version nếu chưa install; pin version từ `uv.lock`/`pyproject`, chạy thử `python -m` ở môi trường thực.

```python
# p56_poc/scripts/extract_content_core.py -- ví dụ POC, CHƯA CHẠY
import asyncio, hashlib, json, sys
from pathlib import Path
from content_core import ContentCoreConfig, extract_content

async def run(path, engine):
    data = Path(path).read_bytes()
    result = await extract_content(file_path=path,
        config=ContentCoreConfig(document_engine=engine))
    print(json.dumps({
        'file': path, 'sha256_bytes': hashlib.sha256(data).hexdigest(),
        'engine': engine, 'content_sha256': hashlib.sha256(result.content.encode()).hexdigest(),
        'content': result.content, 'metadata': result.metadata,
    }, ensure_ascii=False))

asyncio.run(run(sys.argv[1], sys.argv[2]))
```

**Direct Docling sketch (chưa chạy):**

```python
from docling.document_converter import DocumentConverter
result = DocumentConverter().convert('/path/to/permitted.pdf')
with open('direct_docling.json', 'w', encoding='utf-8') as fh:
    fh.write(result.document.export_to_json())
# Save result.document, page/element provenance and compare source-specific offsets.
```

**PASS:** công khai manifest per page/structure, không còn missing/unreadable trang bị giấu, hash original stable, letter `không`/`not`/Pāli dấu và footnote đúng hoặc có `OCR_UNCERTAIN`, source locators hợp lệ. **FAIL:** silently drop trang/negation/footnote, mất original không cảnh báo, engine fallback đổi mà không record revision. Chỉ riêng Open Notebook/Content Core mặc định không có native source map nên **không cấp PASS G1** nếu thiếu external layer; kết luận về chất lượng OCR phải dựa gold. Metrics: CER/WER thủ công trên khu vực khó, page coverage, bbox IoU (khi có ground truth), order-error count, time/RSS/storage. Stage Direct Docling có thể làm tốt hơn hoặc tốn nhiều hơn; chưa biết.

### POC-2 — Exhaustive EXACT, >=50 gold queries

**Truthset:** ít nhất **50 query** phân tầng: 8 Pāli dấu vs không; 8 Việt dấu/bỏ dấu và `đ/d`; 8 Han 1–2 chars và giản/phồn; 4 Unicode NFC/NFD; 4 Tibetan/Wylie; 4 repeat 10+ occurrences; 4 query qua chunk/page; 4 phủ định; 4 long phrase/footnote; 2 no-results/partial, tổng **50**. *Chọn truy vấn có ground truth exact codepoint offsets độc lập được người kiểm*. Ghi mọi offset cho mọi file trong scope; không chỉ score/topK. Với công cụ nền, text canonical do fixture xác định trước.

```python
# Reference truth builder trên canonical text UTF-8 đã ghim; CHƯA CHẠY
# Find all overlapping occurrences in Python's Unicode codepoint offsets.
def occurrences_exact(text: str, needle: str):
    assert needle
    found, start = [], 0
    while True:
        i = text.find(needle, start)
        if i == -1:
            return found
        found.append([i, i + len(needle)])
        start = i + 1

# NOTE: trim, casefold, NFC, whitespace fold, Han variants, d/đ
# must be separate NORMALIZED modes with offset-map proof, not EXACT.
```

**CLI/API planned:** `POST /api/search` body `{"query":"anattā","type":"text","limit":1000,"search_sources":true,"search_notes":false}`; record `total_count`, returned IDs, text results. Không thể “pagination offsets” qua `limit` nếu API không có offset/cursor, vì vậy **kỳ vọng Open Notebook native không đạt exhaustive V1 contract** theo code; vẫn chạy để định lượng mức gap. Trong BodhiAtlas engine so `set(file_id,canonical_start,canonical_end)` với gold, kiểm `recall=1.000`, `precision=1.000` cho EXACT trong indexed scope đã declared, `false_EXACT=0`, duplicates xử lý theo occurrence, `complete=true` chỉ khi không partial/timeouts. **Không lấy 50 query “top1 found source” làm PASS.** Test thêm `search::highlight` lỗi 4-byte/large string xem có fallback vector hay không; kiểm `executed_mode` được trả/ghi nhận trung thực, tạo failure injection nếu phù hợp ở môi trường test, không dùng prod.

### POC-3 — Citation adversarial / reopen original

Tạo E1/E2 cùng title, khác negation và printed page; một bản OCR bỏ/đổi `không`, một source thiếu page, một citation AI bịa ID, một valid quote nhưng sai file SHA, một quote trùng 2 nơi, một citation chỉ xuất hiện trong notes/insight phái sinh. Đưa từng case vào giao diện Search/Ask và `/sources/{id}/download`; capture pointer UI và raw reopening. So đúng **2 thông số**: (a) ON native tạo pointer cấp gì, (b) BodhiAtlas verifier có thể bác false verified khi đọc raw bytes và locator không. **PASS G2** nếu cả positive valid đúng file/edition/page/span pass, tất cả negative **không** được `VERIFIED`, OCR khó phải `NEEDS_REVIEW`, missing original phải `UNVERIFIABLE`, hash mismatch `REJECTED`, scholarly conclusion vẫn `NOT_ASSESSED`. G3 chỉ pass khi review claim/context/counterevidence đầy đủ; một “citation present” chưa đủ.

### POC-4 — Read-only-from-core Evidence Card projection qua REST

**Trình tự thực nghiệm:** (1) BodhiAtlas authority cấp card đã verify (không tự sinh nhãn trong adapter), (2) `GET /v1/evidence/ev:test` qua service account read-only; (3) serialize Markdown note gồm schema v1, evidence_id, file SHA/edition/locator/quote/status và canonical deep-link; (4) `POST /api/notes` `note_type="human"` + title có sẵn (tránh title LLM generation); (5) `GET /api/notes/{id}` so content byte/text & trạng thái; (6) delete ON note/source ở test workspace xem có xóa dữ liệu BodhiAtlas hay không; (7) backup/restore ON và export text note; (8) nâng version ON có giữ mapping không. **Không push raw book** nếu rights không cho.

```bash
# Ví dụ yêu cầu HTTP tới ON của riêng bạn, CHƯA CHẠY.
# Thay PASSWORD bằng secret từ environment; không lưu vào logs/scripts.
curl --fail-with-body -sS \
  -H "Authorization: Bearer ${OPEN_NOTEBOOK_PASSWORD}" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Verified Evidence ev:test (projection)","note_type":"human", "content":"BodhiAtlas: ev:test\nCitation: TEXT_AND_LOCATOR_VERIFIED\nCanonical URL: https://bodhiatlas.local/v1/evidence/ev:test"}' \
  http://127.0.0.1:5055/api/notes
```

**PASS:** no authority drift, note ID map roundtrip, canonical link resolves with permissions, ON delete does not delete BodhiAtlas, recoverable export, no unwanted model/provider egress (test network capture). **FAIL:** remote note hiển thị sai tình trạng, tự phong verified, raw file không cho phép bị upload, adapter phải chỉnh ON source/migrations hoặc hóa thành sync hai chiều. Nếu PASS chỉ mở V2 Workspace, không thay V1 core.

### POC-5 — Swap, disable LLM, backup/restore, nâng cấp và cost

**Ma trận:** 2 source processing engine (`simple`, Docling) × embedding `never/always` × local-only vs configured model × pinned stable/main; test notes write, text FTS, vector, Ask, upload-retention yes/no, start/stop worker, schema upgrade, backup/restore. Đo `num_services`, `num_processes`, `num_databases`, `num_modified_files`, `num_copied_sources`, actual process max RSS, disk bytes per source/embedding, p50/p95 ingest/search latency, token from provider usage and outbound bytes/domain, restore time/error rate. Use `docker stats --no-stream`, `/usr/bin/time -v`, process supervisor list, disk `du -sb`, a protected network/egress monitor. `docker compose ... exec` chỉ sau khi confirm service name/health; tag/digest pin được ghi snapshot.

**PASS for D:** code-only EXACT/search/verifier vẫn phục vụ khi LLM/embedding completely unavailable, hash/locator/coverage survives rebuild, backups restore all authoritative data, ON can be removed without changing BodhiAtlas core; licensing & rights policy enforced. **PASS for ON as optional workspace:** restores notes/source state, no leaks, no surprise cloud model usage, repeatable updates. **FAIL:** fallback semantic in code-only contract, silently wrong restored ID, missed source coverage, encrypted secrets mất sau restore, data unavailable if worker/provider offline. Không báo KPI khi chưa chạy.

### 9.2. Decision thresholds và log mẫu phân biệt expected/measured

| Gate | Ngưỡng nghiệm thu bắt buộc (đề xuất policy, không phải observed) | Kết quả hiện tại |
|---|---|---|
| G1 source/coverage | `file_sha256` đúng 100%; mỗi trang trong scope có `READY/PARTIAL/ERROR`, engine/extract revision không thiếu; không silently drop negation | **NOT TESTED** |
| G2 technical citation | 100% positive gold đúng raw-file/edition/locator, **0 false VERIFIED** ở adversarial negative; OCR uncertain không automatically verified | **NOT TESTED** |
| G3 scholarly claim | model cannot promote `SUPPORTS`; reviewer/counterevidence mandatory cho claims trọng yếu; phản chứng giữ độc lập | **NOT TESTED** |
| C05 exhaustive EXACT | `precision=1`, `recall=1` **all occurrence offsets** trên full indexed scope, report partial/timeout; no semantic fallback mislabeled EXACT | **NOT TESTED** |
| C06 multilingual | expected normalized links với map vị trí, 0 falsely labeled EXACT; Han/Pāli/Việt/Tạng cases có gold-defined scope | **NOT TESTED** |
| G4/G6 rights/security/publish | no unauthorized provider egress, secret hardening, policy per original, publication review trail | **NOT TESTED** |
| Operability | after restore SHA/content/edition/locator unchanged and all verified links pass or explicitly stale; no ghost vector DB authority | **NOT TESTED** |

```json
{
  "record_type": "p56_poc_result_example_only",
  "poc": "POC-2",
  "repository_sha": "0c1e7abbd77411057d8feef02fc4588ec9a556d6",
  "fixture_id": "U10",
  "status": "NOT_TESTED",
  "expected_occurrences": "value must come from human gold fixture",
  "observed_occurrences": null,
  "latency_ms": null,
  "peak_rss_mib": null,
  "token_usage": null,
  "notes": "This is a proposed logging schema, NOT an executed test output"
}
```

**Chú ý an toàn khi thực thi:** chỉ log file_id/SHA và non-sensitive fixture, redacted request/response; không lưu passwords, bearer tokens, full copyrighted excerpts vào public CI; không gọi cloud OCR/LLM cho tư liệu chưa được phép. Không làm POC bằng corpus kinh sách thương mại khi chưa chứng minh quyền.

---
## 10. Deployment, Security, Legal, Cost

### 10.1. Triển khai tối thiểu an toàn: profile `sandbox-only` / `private LAN` / `VPS`

**Không sử dụng Compose mẫu trực tiếp trên VPS/LAN.** GitHub Compose đã kiểm có `surrealdb` và `open_notebook`, app ports `8502:8502` và `5055:5055`, password app rỗng theo default, Surreal credentials `root:root`, encryption key public fallback `change-me-to-a-secret-string`, image tag `v1-latest` không pin digest. `./notebook_data` và `./surreal_data` là volumes persistence. Đọc trực tiếp [Docker compose](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docker-compose.yml#L1-L66). `[CODE]`

| Profile | Quy định | Quyết định |
|---|---|---|
| **POC private workstation** | pin tag/commit/digest, generated secrets, port bind `127.0.0.1`, no external content without rights, `NO_PROXY` internal, no telemetry/provider ngoài, mount volumes snapshot | **Cho phép thử** nếu có người quản trị và fixture hợp lệ |
| **Private LAN single researcher** | HTTPS reverse proxy/auth network boundary, non-default passwords, CORS exact origins, firewall 5055/DB, local-only model if book policy demands, backups tested | **Chỉ xem xét V2 Workspace**; shared password không phù hợp source ACL đa người |
| **Public VPS / multi-user** | per-user identity/RBAC/source ACL, audit access, secrets management, rate limit, quota/upload scanning, SSRF+egress filtering, encrypted backups, vulnerability management | **Không phê duyệt với auth hiện tại** làm core tài liệu học thuật nhiều người |
| **Air-gapped/offline** | pinned offline image+wheel+weights, no DNS/network routes, local OCR/LLM if any, proof all requests are on host, start up after network denied | **HYPOTHESIS**, cần POC-5; không tuyên bố “offline hoàn toàn” chỉ vì hỗ trợ Ollama |

**Auth model thực:** `PasswordAuthMiddleware` chỉ so shared bearer secret, bypass nếu không set `OPEN_NOTEBOOK_PASSWORD`; docs chính thức cảnh báo single-user-first, chưa RBAC. CORS no-password same-host/localhost theo `api/main.py` mới; với password set thì default wildcard nếu không cấu hình cụ thể, vì vậy luôn set `CORS_ORIGINS=https://your-private-origin` và kiểm browser credential flow. `SameHostCORSMiddleware` **không phải auth** và không chống DNS rebinding hoàn toàn. Password lưu phía browser theo docs làm máy tính người dùng/extension có thể là điểm yếu. Reverse proxy phải không ghi Authorization vào access logs. `[CODE][DOC]` [auth](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/auth.py#L12-L81), [CORS](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/main.py#L83-L114), [security](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/5-CONFIGURATION/security.md).

### 10.2. Threat model theo asset / adversary / control

| Asset cần bảo vệ | Mối đe dọa | Control hiện thấy | Khoảng trống/hành động bắt buộc |
|---|---|---|---|
| Raw copyrighted PDFs/EPUBs | leak qua upload/web/LLM provider; tự delete file | path containment, opt upload retention; source pipeline URL guard | rights flags + deny outbound by default; immutable encrypted raw authority ở BodhiAtlas, ON chỉ projection |
| Provider/API keys | default encryption key và browser password exposure | env key/Fernet, optional Docker secrets, password compare-time guard | rotate secrets, no sample key, TLS, secrets manager và restore secret test |
| URLs/metadata endpoints | SSRF to cloud metadata/LAN, redirects/DNS rebinding | URL validation worker+API, Content Core patched security release | attack tests redirect chain, DNS pin per client, network allowlist/deny, no full SSRF guarantee |
| Search & citation | LLM hallucinates ID/quote, false `EXACT` | prompts instruct citations, Search BM25, UI link parser | independent verifier/candidate status, no implicit semantic fallback, audit exact scope |
| SurrealDB/queue | unauthorized DB access/worker injection, migration conflicts | DB credential, schemafull for many tables, source delete retries | private DB bind, no public 8000, least privilege, inventory endpoints, migration backup & restore |
| File upload / model resource | oversized file, malicious PDF/HTML, memory exhaustion | upload body size middleware and file support preflight | file magic MIME checks, AV/sandbox optional, timeout CPU/RAM, quotas, OCR model isolation |
| Evidence reviewer status | model or workflow escalates candidate to VERIFIED | **không có gate này trong ON** | BodhiAtlas signed/audited review event with source-scoped permissions |
| Search/Ask outputs | prompt injection từ source web/HTML/TEI | app relies on prompt/model for research | treat source text as untrusted data, never execute model instructions in documents, citations must be code-checked |
| Backup & restores | lost originals, corrupt schema, missing SQLite state | Docker volumes, DB migration scripts | restore drill with bytes hash + source IDs + edges + checkpoint and authorization |

**Supply chain / dependencies:** HEAD `pyproject.toml` có các dependency `content-core`, `esperanto`, Surreal Python client, LangGraph; Docling extras kéo ML stack lớn, frontend Next/React. Không có báo cáo audit tất cả transitive license/CVEs, lockfile provenance, SBOM hay Docker digest trong nghiên cứu này: `UNKNOWN`. Ràng buộc lock version, release feed và scan vulnerability trước production; không kết luận “an toàn” dựa MIT. Open Notebook release v1.15.1 là security release và phần nào sửa lỗi; nhưng issue/changelog không thay pentest. `[CODE][DOC]` [pyproject](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/pyproject.toml), [frontend deps](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/frontend/package.json#L45-L54), [release](https://github.com/lfnovo/open-notebook/releases/tag/v1.15.1).

### 10.3. Quyền: ma trận chính sách trước khi xử lý

**MIT code license ≠ quyền xử lý/phổ biến sách hoặc quyền xuất PDF/quote lên provider.** Ít nhất phải phân 4 lớp: license mã nguồn ON/CC/Esperanto; license từng package/transitive; quyền file/bản dịch/scan/catalog/metadata được nhập; điều khoản model weights/API/host provider (training/retention/region). Tác phẩm có thể public domain nhưng **ấn bản/bản dịch/chú giải cụ thể** còn có quyền riêng. OCR có thể tạo derivative; uploading model provider là một hành vi xử lý truyền dữ liệu, không suy từ quyền local reading. Chưa audit từng nguồn: **UNKNOWN**.

| Chính sách ví dụ | Ingest nội bộ | Embeddings cloud | Remote OCR/vision | Export publish | V1 response |
|---|---|---|---|---|---|
| `public-domain-verified` | được theo license | chỉ sau consent/model terms | chỉ sau đánh giá provider | theo quy định attribution/edition | cho phép theo giấy phép cụ thể |
| `personal-private-licensed` | phụ thuộc giấy phép/tư cách | **mặc định không** | **mặc định không** | **mặc định không** | code-only, local OCR/LLM nếu được phép |
| `restricted-academic` | whitelist người dùng/dữ liệu | deny mặc định | deny mặc định | cần duyệt legal | local encrypted, no ON public server |
| `unknown-rights` | quarantine metadata, không cloud | deny | deny | deny | `RIGHTS_UNKNOWN` và human check |

### 10.4. Cost model không giả benchmark

**Chi phí một nghiên cứu** = `C_ingest + C_OCR + C_emb + C_retrieval + C_Ask + C_storage + C_backup + C_maintenance + C_compliance`. Với code-only default BodhiAtlas, `C_Ask=0`, `C_emb=0` trên đường đó; OCR có thể dùng local CPU/GPU hoặc provider nhưng vẫn tốn tài nguyên. Với Open Notebook Ask, chi phí tạo sinh có ít nhất strategy+final calls, tối đa theo fan-out thực; vector embedding query cũng tốn latency/provider calls và source embedding jobs; `OPEN_NOTEBOOK_CHUNK_SIZE` mặc định 400 tokens/overlap ~15%, nên số chunks phụ thuộc text/format. `ASK_MAX_TOKENS=8192` là **max output token config** mỗi call, không phải usage invoice. `[CODE]` [Ask](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/ask.py#L23-L27), [chunking](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/utils/chunking.py#L9-L24).

**Không báo giá theo VND, person-day, RAM, token hay p95** nếu chưa đo trên máy, input, provider, quota và profile lưu trữ. Định tính: ON app thường đắt vận hành hơn core SQLite nhỏ do có thêm server/frontend/worker/Surreal/SQLite/caches, nhưng nếu nhóm ưu tiên UI ghi chú/Ask thì tiết kiệm UI có thể bù chi phí; chỉ POC-5 mới trả lời. **Chi phí thay thế vendor** đáng chú ý hơn lần install đầu: ON authoritative source metadata thiếu nên migration sang core đúng PRD có nguy cơ buộc re-ingest mất source reference history; D authoritative immutable raw+catalog cho phép thay parser/index/LLM mà không thay chứng cứ gốc.

### 10.5. Upgrade / backup / legal checklist trước production

- Pin SHA và image digest, lock Python/JS deps, ghi namespace/database/schema migration number, không dùng `v1-latest` như pinned release.
- Backup đồng bộ Surreal state, queue, SQLite checkpoints, retained `uploads`, app config và encryption key; lưu bản backup encrypted, thử restore trên máy sạch trước bất kỳ upgrade nào.
- Trong restore, so nguồn/work/edition identifiers, SHA bytes, article notes, edge relationships, citation links, verified cards và false-verification count; `file_path` phải xử lý đổi mount root.
- Test source delete/retry khi embedding đang chạy và original file retained/unretained, có audit event và retention policy; API delete source không được xóa raw BodhiAtlas authoritative.
- Network isolate có egress allowlist; local OCR/LLM model được phép; không log full text private hoặc token; cùng lúc kiểm lại CORS/origin/bearer auth.
- Kiểm third-party licenses của `Docling` runtime, OCR models, `tesseract` nếu dùng, frontend/JS deps và mọi model weights trước xuất bản.

---

## 11. Comparison & Trade-offs

### 11.1. Technology landscape — cùng một tiêu chuẩn G1–G6

| Stack/Repo | Bằng chứng trực tiếp P56 | Điểm mạnh được chứng minh trong code | Giới hạn đối với BodhiAtlas V1 | Kết luận sử dụng |
|---|---|---|---|---|
| **Open Notebook** | sâu: domain, source graph, search/Ask, API, migrations, UI citations, auth/tests | UI research phong phú, REST, multiple notebooks, notes/insights, search BM25+vector, local/remote provider plumbing | không work/edition/map/coverage; no exhaustive EXACT; citation item-level; extra state | Workspace optional trial, không system of record |
| **Content Core** | sâu: `ExtractionOutput`, extract route, PDF/EPUB/Docling, tests | unified extraction, parser selection, library API độc lập, MIT | flatten string; parser metadata không typed map; Docling JSON chưa thành scholarly locator | Reuse **có điều kiện** ở ingestion; Direct Docling khi cần map |
| **Direct Docling** | wrapper trực tiếp + API code sử dụng; không audit toàn repo upstream ở P56 | có `DocumentConverter` và `DoclingDocument` (qua code wrapper) cho export structured JSON | không tự là corpus/search/verified citation; thực tế OCR/layout chưa đo | extractor candidate bên dưới BodhiAtlas adapter |
| **Bang-ha local corpus framework** | code private trực tiếp: schema SQLite, adapters, cli, ledger | source hash, work/edition/locator, passages, canonical corpus adapters, FTS | source-specific, personal PDF/EPUB/OCR/source map chưa native; ledger review default verified risk | Candidate reuse passage/catalog, không chọn whole core không POC |
| **BCR** | code public: model/retrieval/verification/source readers | pinned source code verifier, typed quote status, original-text source reader, CJK and normalized candidates | corpora pinned, PDF/EPUB page+bbox/CFI và generic ingest phải tự viết | Candidate reuse verifier conventions/contracts; giữ quyền nguồn BodhiAtlas |
| **RAGFlow** | đọc PRD/assessment navigation; **không audit HEAD trực tiếp trong P56** | app RAG scope theo vị trí trên thị trường/phạm vi tool; **chưa code-verify** trong P56 | G1/G2/C05 **UNKNOWN trong đánh giá này**, không thể cấp native compliance | Research/Ask comparison only; cần thẩm định riêng P01 bằng commit hiện thời |
| **SQLite FTS5/trigram baseline** | code Bang-ha/BCR và PRD; không đo engine isolated P20 trong P56 | simple offline index, candidate search và cursor khi tự thiết kế | FTS query không tự cho every occurrence/character offsets; phải xác minh trên canonical string và coverage | kỹ thuật index ứng viên cho D, không là EXACT verifier đơn độc |
| **Esperanto** | README/pyproject/license | abstraction local/remote LLM/embedding/STT, MIT | không giải quyết G1–G3 hay code-only search | hoãn V2; không cần cho V1 deterministic core |
| **Surreal Commands** | README + ON call sites | durable async queue on Surreal | kéo SurrealDB và worker; không tự tạo evidence provenance | chỉ dùng khi chạy ON workspace, không dùng cho D minimal |
| **Community MCP `Epochal-dev`** | README | bridge API ON→MCP, transports stdio/HTTP | third-party, auth theo ON bearer, không kiểm nguồn độc lập | không dùng remote with private source trước hardening |

**Cảnh báo công bằng:** “Open Notebook nhiều feature” có giá trị thực khi mục tiêu là research workspace tương tác; “BCR có verifier” có giá trị thực khi source pinned mà reader hiểu; “Bang-ha có edition” có giá trị thực khi corpus format/locator đã biết; “Direct Docling” phù hợp PDF layout tốt hơn text flatten về khả năng truy nguyên. Nhưng không phương án nào được cấp PASS vì chỉ số đo quality absent. Đây là so sánh G1–G6 theo **sự tương thích code** và phạm vi phải xây, không tuyên bố performance winner.

### 11.2. Xếp hạng riêng #1 — `FASTEST USEFUL DEMO`

**Định nghĩa demo:** một nhà nghiên cứu có thể nhập tài liệu được phép, tạo notebook, tìm văn bản/câu hỏi, ghi chú và xem lại kết quả **không gắn nhãn verified**, chưa đáp ứng G1–G6. Xếp hạng định tính, đo thực tế **NOT TESTED**; thay đổi nếu demo chỉ yêu cầu corpus search offline.

| Hạng giả thuyết | Phương án | Lý do | Điều kiện thay đổi |
|---|---|---|---|
| **1** | **A — Open Notebook-first (demo only)** | UI+API+workflows hoàn chỉnh đã có, có thể demo notebooks/search/chat/notes nhanh hơn xây UI mới | deploy engine/DB/model phải thành công; nếu no-cloud/offline yếu, mất lợi thế |
| **2** | **B — Bang-ha-led** | SQLite passage search/corpus pipeline đã có, demo code-only corpus nhanh nếu dữ liệu sẵn | nếu demo PDF/EPUB cá nhân, adapter mới kéo chậm |
| **3** | **C — BCR-led** | pinned corpus retrieval/quote verifier có code, hợp demo văn bản chuẩn | nếu cần UI đẹp hay nhập sách mới, phải xây nhiều |
| **4** | **D — Minimal Core** | phải tạo skeleton catalog/search/reader API ban đầu; sau đó demo trustworthy hơn | có bootstrap template hoặc team quen SQLite/Docling thì có thể vượt B/C |
| **5** | **E — Selective Reuse đứng riêng** | parser/provider library không tạo product UI/notes/search; demo chỉ extraction thì E có thể là **hạng 1** | demo định nghĩa *extract text only* thì đổi rank, không so “app demo” với “parser demo” |

**Không diễn giải bảng này là “A nhanh nhất compliant V1”.** Demo chứng minh product UX, không chứng minh provenance, verified citation hoặc exhaustive exact.

### 11.3. Xếp hạng riêng #2 — `SAFEST / LOWEST TOTAL COST TO COMPLIANT V1`

**Định nghĩa:** đầy đủ hard-gate G1/G2/G3/G4/G5/G6 khi áp dụng, no false EXACT, source map/coverage, code-only, quyền nguồn/restore, tổng coupling và migration thấp. Tất cả là **candidate architectures chưa PASS POC**.

| Hạng giả thuyết | Phương án | Lý do chọn / caveat |
|---|---|---|
| **1 — ưu tiên** | **D — BodhiAtlas Minimal Core** | thiết kế authority đúng PRD từ đầu, giữ original SHA và map trước indexing, deterministic exact, dễ thay Docling/SQLite/LLM; cần chứng minh không over-engineer bằng POC |
| **2** | **C — BCR-led** | có trusted code verifier/pinned sources và review states; dùng kỹ thuật BCR nhưng mở rộng PDF/EPUB là **H–VH** và có thể phá pinned corpus simplicity |
| **3** | **B — Bang-ha-led** | catalog/passages SHA/edition và locators đáng reuse; framework nhiều corpus adapters, SQLite state phù hợp; generic books/coverage/strict reviewer semantics vẫn thiếu, repo private governance |
| **4** | **E — Selective Reuse as stand-alone** | chi phí vận hành engine thấp và dễ tháo nhưng **không phải một V1 đầy đủ**; chỉ có cơ hội thắng khi **gộp E vào D**, vì còn phải xây toàn core |
| **5** | **A — Open Notebook-first** | muốn compliant phải sửa dữ liệu + Search/Ask + verifier/UI + schema/ACL, duy trì 4 vai trò runtime, khó giữ upstream; lock-in lớn nhất đối với authoritative data |

**Sensitivity / phản biện:** Nếu đội đã có BCR trusted verifier fully adapted PDF/EPUB, phương án C có thể vượt D nhờ reuse; nếu Bang-ha có general book loader + source maps mới đã hoàn thiện, B có thể vượt C; nếu ON upstream shipping evidence-core và all-occurrences API audited, A cần chấm lại; nếu D scope nở thành custom framework nhiều service, D mất lợi thế. Vị trí #2/#3 phụ thuộc POC, không coi là định luật. Không được lấy `mean score` để vượt hard-gate fail.

### 11.4. Decision table đối nghịch: lợi ích UI so với ảnh hưởng scholarly trust

| Câu hỏi phản biện | A/ON mạnh ở đâu? | Vì sao không đủ chọn làm V1? | Cách giữ lợi ích mà không hy sinh gate |
|---|---|---|---|
| “Một app đã viết xong, sao không fork?” | notebook/chat/notes/search UI có sẵn | domain/source schema và migration không chứa source map; fork broad change | dùng app nguyên trạng, ON chỉ research projection ở V2 |
| “Docling có bbox, ON cũng dùng Docling” | parser optional thực dùng Docling | `ExtractionOutput.content` string và `save_source` không persist bbox→cite | dùng Direct Docling JSON/DoclingDocument vào BodhiAtlas canonical extractor |
| “Text Search không cần AI” | text BM25 bình thường không gọi model | không exhaustive, English stemming, top LIMIT và overflow fallback vector | own deterministic exact index+verification, gọi ON text search cho khám phá tùy chọn |
| “Có citation click được” | source/note/insight ID link | ID không page/CFI/quote/hash/edition/coverage | BodhiAtlas `EvidenceCard` canonical deep-link, verified status chỉ từ trusted code |
| “LLM local thì hoàn toàn offline” | Esperanto hỗ trợ Ollama/local, Docling local | API/web fetch/remote enrichment/cache/telemetry chưa network-denied tested | chạy POC-5 deny egress, tắt models cho code-only, enforce rights policy |
| “Chỉ cần thêm custom fields” | Surreal flexible `asset`, REST note content | thêm JSON field không đồng nghĩa all pipeline/FTS/Ask/UI/worker giữ metadata và verify | làm schema chuyên biệt độc lập, adapter projection nhỏ và reversible |

---

## 12. Decision Record for Master Synthesis

### 12.1. Bản ghi chuẩn, có thể trích máy đọc

**Đối tượng của bản ghi là _toàn bộ ứng dụng_ `lfnovo/open-notebook` tại HEAD đã ghim, không phải riêng `content-core` hoặc đề xuất Evidence Core.** Trường `RECOMMENDATION` phân biệt quyết định về sản phẩm này với lựa chọn kiến trúc D ở cấp BodhiAtlas; `TRIAL ONLY` không có nghĩa loại bỏ mọi thư viện con. `NOT TESTED` là trạng thái kết quả POC, không phải bằng chứng thất bại thực nghiệm.

| FIELD | VALUE | EVIDENCE / INTERPRETATION |
|---|---|---|
| `TARGET` | `lfnovo/open-notebook` | [Repository](https://github.com/lfnovo/open-notebook) |
| `CLASS` | `Research Workspace / self-hosted notebook and AI research application` | `[CODE][DOC]` [architecture](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/7-DEVELOPMENT/architecture.md#L12-L34) |
| `DATE` | `2026-11-23` | Ngày truy cập và kiểm tra bằng chứng, múi giờ `Asia/Ho_Chi_Minh` |
| `VERSION/COMMIT` | `HEAD main=0c1e7abbd77411057d8feef02fc4588ec9a556d6; package=1.15.1; frontend=0.1.0; release=v1.15.1@5e285b7a2e435895c4ee99ad7e4b8d2af64c3239` | `[CODE]` HEAD khác stable; `main` có thay đổi chưa được khẳng định là phát hành ổn định |
| `LICENSE` | `MIT (Open Notebook); MIT (content-core, esperanto); other transitive/data/model terms UNKNOWN` | `[CODE]` LICENSE của ba repo; **không** cấp phép nội dung sách/ảnh/OCR weights |
| `ACCESS_STATUS` | `PUBLIC_REPOS_READ; BANG_HA_PRIVATE_AUTHORIZED_READ; RUNTIME_NOT_TESTED` | Repo chính, CC, Esperanto, Surreal Commands, MCP, BodhiAtlas và BCR đã đọc; Bang-ha cần quyền mở permalink; không clone/deploy |
| `PRIMARY_ROLE` | `OPTIONAL_RESEARCH_WORKSPACE` | Notes/insights/chat/API tồn tại nhưng không là scholarly authority |
| `BEST_FIT_V1` | `NOT_AS_CORE; optional selective content-core evaluation under D` | Chỉ cân nhắc component extractor sau POC-1; thẩm quyền G1/G2/G3 ở BodhiAtlas |
| `BEST_FIT_V2_V3` | `ISOLATED_WORKSPACE_VIA_REST; possible esperanto as AI provider abstraction` | Giữ note projection và canonical evidence URL, không đồng bộ hai chiều state verified |
| `SOURCE_FIDELITY_GATE` | `NOT_DEMONSTRATED; G1/C03/C04/C13 CODE_GAPS` | `Source` schema, flattened extraction và auto-delete có điều kiện; thiếu scholarly source map/coverage |
| `CODE_ONLY_EXACT_GATE` | `NOT_MET_BY_NATIVE_SEARCH_CONTRACT; C05 CODE_GAP; POC_NOT_TESTED` | Surreal BM25 item limit, `total_count=len(results)`, no occurrence offsets, fallback sang vector khi highlight overflow |
| `MULTILINGUAL_GATE` | `NOT_DEMONSTRATED; C06/C07/C08 EXTENSIONS_OR_MISSING` | English stem analyzer, không có bộ query transform + reversible offset map/verified lexicon theo PRD |
| `QUALITY_COVERAGE_GATE` | `NOT_DEMONSTRATED; per-page/OCR/partial manifest missing in reviewed core` | Chưa đo CER/WER, 2-column order, missing-page detection, G1–G2 |
| `RIGHTS_SECURITY_GATE` | `CONDITIONAL; BASIC_PASSWORD; SOURCE_ACL_AND_RIGHTS_EXTERNAL; SECURITY_POC_NOT_TESTED` | Auth chung và Docker defaults cần hardening; network guards có code; quyền tác phẩm riêng |
| `INTEGRATION_COST` | `A=HIGH_TO_VERY_HIGH; D_WITH_OPTIONAL_ON=LOW_TO_MEDIUM_BOUNDARY_ONLY; MEASURED_UNKNOWN` | Fork/app schema rộng hơn một note REST projection; không gán nhân-ngày khi chưa benchmark |
| `MAINTENANCE_RISK` | `HIGH_AS_V1_AUTHORITY; MEDIUM_AS_ISOLATED_OPTIONAL_WORKSPACE` | SurrealQL 1–28, worker, FastAPI/Next.js, SQLite checkpoints, upstream version churn; vNext roadmap chưa là code |
| `RECOMMENDATION` | `TRIAL ONLY (whole Open Notebook); USE AS COMPONENT only for content-core after POC; PREFERRED_BODHIATLAS_ARCHITECTURE=D` | Quyết định có điều kiện, không `ADOPT` app làm V1 |
| `CONFIDENCE` | `HIGH(native hard-gate gaps); MED(architecture D cost ranking); LOW-MED(runtime economics)` | Bằng chứng code mạnh, thiếu benchmark runtime; thứ hạng chi phí mang tính giả thuyết |
| `NEXT_POC` | `POC-1,POC-2,POC-3 first; POC-0,POC-4,POC-5 to validate optional workspace` | Gate thứ tự: source → exact → citation; nếu không qua thì không commit production |

**Dạng JSON tiện đưa vào master inventory** (giá trị status là kết quả thẩm định, **không** phải test-run report):

```json
{
  "target": "lfnovo/open-notebook",
  "class": "research-workspace-application",
  "date": "2026-11-23",
  "snapshot": {
    "default_branch": "main",
    "head_commit": "0c1e7abbd77411057d8feef02fc4588ec9a556d6",
    "package_version": "1.15.1",
    "stable_release": "v1.15.1",
    "stable_commit": "5e285b7a2e435895c4ee99ad7e4b8d2af64c3239"
  },
  "license": "MIT; dependencies, book rights and model licenses require separate audit",
  "access_status": "CODE_READ_NOT_EXECUTED",
  "primary_role": "OPTIONAL_RESEARCH_WORKSPACE",
  "source_fidelity_gate": "NOT_DEMONSTRATED",
  "code_only_exact_gate": "NATIVE_CONTRACT_GAP",
  "multilingual_gate": "NOT_DEMONSTRATED",
  "quality_coverage_gate": "NOT_DEMONSTRATED",
  "rights_security_gate": "CONDITIONAL_NOT_TESTED",
  "recommended_bodhiatlas_architecture": "D_MINIMAL_CORE",
  "whole_application_recommendation": "TRIAL_ONLY",
  "component_recommendation": "CONTENT_CORE_POC_THEN_CONDITIONAL_USE",
  "confidence": {"native_gap": "HIGH", "architecture_cost_ranking": "MED", "runtime_economics": "LOW_MED"},
  "next_poc": ["POC-1", "POC-2", "POC-3", "POC-0", "POC-4", "POC-5"],
  "performance_measured": false,
  "github_source_verified": true,
  "runtime_not_tested": true
}
```

### 12.2. Top 5 findings — các điểm có tác động lớn nhất

1. **[CODE] Mất chuỗi truy nguyên ở ranh ingestion.** `extract_content` trả `ExtractionOutput.content`; `save_source` lưu chuỗi đó thành `full_text`; schema chunk chỉ lưu `source/order/content/embedding`. Bất kể Docling upstream có provenance, đường mặc định này không biến nó thành Work/Edition/Page/CFI được kiểm. [source.py L313–383](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/graphs/source.py#L313-L383), [CC state.py L22–29](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/common/state.py#L22-L29).
2. **[CODE] Text Search chạy khi không có LLM ở đường thường, nhưng không là exhaustive EXACT.** English stemming/BM25, giới hạn item, không trả every occurrence; fallback vector khi lỗi highlight phải được chặn khỏi contract exact. [migration 26](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/database/migrations/26.surrealql#L111-L192), [notebook.py L898–949](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/open_notebook/domain/notebook.py#L898-L949).
3. **[DOC][CODE] Citation là navigational pointer do LLM chọn**, không phải phiếu G2 kiểm câu chữ/locator/ấn bản; raw download có điều kiện là lợi thế nhỏ nhưng không chứng minh reopen theo đoạn. [citations.md](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/3-USER-GUIDE/citations.md#L7-L40), [source references UI](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/frontend/src/lib/utils/source-references.tsx#L34-L55).
4. **[CODE] Ưu điểm tái dùng có ranh giới rõ:** `content-core` là library extractor độc lập; Open Notebook REST notes/CRUD là integration point; `esperanto` phục vụ model portability nhưng không giúp G1–G3. [CC extraction](https://github.com/lfnovo/content-core/blob/b8452534bfd85ac6048ac8f028a219638aef0a8c/src/content_core/extraction.py#L50-L97), [notes REST](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/api/routers/notes.py#L55-L118).
5. **[PLAN] Roadmap nhìn nhận đúng lỗ hổng evidence**, nhưng chưa thể coi là implementation/release/compliant V1; chi phí fork hiện tại không thể bù bằng lời hứa Evidence Core. [Discussion #1315](https://github.com/lfnovo/open-notebook/discussions/1315), [VISION Horizon](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/VISION.md#L49-L75).

### 12.3. Top 5 blockers — giữ nguyên ưu tiên P0 trước tính năng phụ

1. **P0/G1/G2:** không có immutable original-file SHA256 cùng scholarly identity, extraction revision và source-span locator có thể mở lại trong schema/lưu đồ mặc định; upload file còn có thể auto-delete.
2. **P0/C05:** không có all-occurrences, all-offsets post-verification trên canonical extracted text; thiếu hard separation `EXACT` vs `NORMALIZED` vs `SEMANTIC` và scope-completeness semantics.
3. **P0/G2/G3:** thiếu code-verifier trusted độc lập; claim support không có reviewer/contradiction/dependency provenance, “citation exists” không cấp `SUPPORTS`.
4. **P0/C13/C14:** không có page/region OCR coverage + `PARTIAL` theo scholarly contract; quyền dùng file, cloud egress, user roles/review authority và reproducible restore vẫn phải triển khai/kiểm thử.
5. **P1–P0/C06/C08/C15:** đa ngôn ngữ có dấu và Wylie, sense-level lexicon, cùng upgrade/migration giữa SurrealDB/SQLite/upload records sẽ làm fork app trở nên rộng; thiếu benchmark đo chi phí thực.

### 12.4. Top 5 experiments — tính phản chứng và thứ tự ra quyết định

| Priority | Experiment | Phép đo quyết định | Nếu không đạt |
|---|---|---|---|
| 1 | **POC-1** — same input: CC `simple/docling` / direct Docling / ON, PDF scan + EPUB | hash raw, per-page missing/negation/footnote, structural locator, OCR uncertainty; không tự điền missing | bỏ CC wrapper cho format có yêu cầu source map mạnh; dùng direct parser/Docling adapter; giữ G1 fail closed |
| 2 | **POC-2** — >=50 gold query, raw codepoint offsets | exact precision/recall **1.0** trong scope declared, tất cả hit và `false_EXACT=0`; no silent semantic fallback | không cho ON Search làm V1 `EXACT`; dùng BodhiAtlas deterministic index + verifier |
| 3 | **POC-3** — negation/edition/OCR/spoofed citation | `0` false VERIFIED; positive reopen đúng file SHA/edition/locator; G3 review tách biệt | cấm cấp G2 bằng item citation; thiết kế resolver riêng trước khi research publish |
| 4 | **POC-4** — 1-way Evidence Card → ON note REST | round-trip ID/link/status, quyền, deletion isolation, no unnecessary AI egress | không kết nối workspace ở V2; giữ ON ngoài boundary |
| 5 | **POC-5** kết hợp **POC-0** — restore/swap/cost/release parity | config pinned, measured RAM/p95/token/storage, restore raw + graph/checkpoint, không drift authority | không cho production; nâng version tách sandbox, giảm service hoặc bỏ ON |

**Một câu kiến trúc đề xuất:** **BodhiAtlas V1 dùng Minimal Core (D) làm _sole authority_ cho file gốc, Work/Edition/Witness, extraction/source-map/coverage, exhaustive code-only retrieval và G1–G6 evidence gates; tái dùng Content Core/Direct Docling theo profile đã thử, giữ Open Notebook độc lập như workspace V2 chỉ nhận bản chiếu read-only hoặc note một chiều qua REST, không trao quyền tạo/xác nhận citation.**

---

## 13. Appendix

### 13.1. Snapshot pin và liên kết tra cứu lại

| Mục | Đường dẫn cố định/địa chỉ | Ghi chú xác minh |
|---|---|---|
| Open Notebook HEAD | [`0c1e7abb`](https://github.com/lfnovo/open-notebook/commit/0c1e7abbd77411057d8feef02fc4588ec9a556d6) | `main`, 18/11/2026; đã đọc code tại SHA này |
| Open Notebook stable | [`v1.15.1`](https://github.com/lfnovo/open-notebook/releases/tag/v1.15.1) và [tag commit](https://github.com/lfnovo/open-notebook/commit/5e285b7a2e435895c4ee99ad7e4b8d2af64c3239) | published 04/11/2026; chưa deploy; không trộn với HEAD |
| Open Notebook tree | [GitHub tree tại SHA](https://github.com/lfnovo/open-notebook/tree/0c1e7abbd77411057d8feef02fc4588ec9a556d6) | GitHub API recursive tree đã đọc; không có nghĩa đã mở mọi file |
| Content Core | [`b8452534`](https://github.com/lfnovo/content-core/commit/b8452534bfd85ac6048ac8f028a219638aef0a8c) | 08/11/2026; pyproject `2.3.0`, MIT |
| Esperanto | [`343e0a9f`](https://github.com/lfnovo/esperanto/commit/343e0a9f874cb9a4339f2bc21817add4c296daa6) | 03/10/2026; `2.28.0`, MIT |
| Surreal Commands | [`2abbdd7f`](https://github.com/lfnovo/surreal-commands/commit/2abbdd7f4581b9f3514669721cb949f536cc2a87) | 31/01/2026; queue integration qua README và ON call sites |
| Community MCP | [`a2cddbf6`](https://github.com/Epochal-dev/open-notebook-mcp/commit/a2cddbf65cba8c4c8de7be16566781b7612a9545) | 22/12/2025; bên thứ ba, chưa kiểm runtime |
| BodhiAtlas docs | [`aa874008`](https://github.com/quocgempro361/bodhi-atlas/commit/aa874008ff4c6a6e9d66e6fee34c55e0370d6820) | PRD V1.4, Foundation, Academic Risks; authority về yêu cầu |
| Bang-ha private | [`4345737a`](https://github.com/quoctran-2608/Bang-ha-giac-ngo/commit/4345737ae16638b19226ea1b11007e6ffa4faf62) | đọc bằng kết nối có quyền; người khác có thể bị 404 |
| BCR | [`dfdd3cbb`](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/commit/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410) | code `model/retrieval/verification/source_resolvers` đã đọc |

**Tính mới:** GitHub Compare API tại thời điểm truy cập trả `main` đi trước `v1.15.1` **180 commits**, thay đổi **232 files**. Đây là số liệu thay đổi trong metadata API, **không phải** benchmark hoặc cam kết 180 thay đổi đều liên quan evidence. Để lặp lại, truy cập [compare pinned release → main](https://github.com/lfnovo/open-notebook/compare/v1.15.1...0c1e7abbd77411057d8feef02fc4588ec9a556d6); số sẽ khác nếu so với `main` động về sau.

### 13.2. Code inventory đã đọc và vì sao quan trọng

Danh mục dưới đây chỉ ghi file đã **mở nội dung thực tế** tại commit tương ứng, không coi tất cả blob trong tree là đã audit. Nhóm mã Open Notebook đã mở vượt tối thiểu 15 file cốt lõi, có cả migration tạo bảng và migration effective search:

| Nhóm | File đã mở tại pinned snapshot | Cơ chế đã xác nhận |
|---|---|---|
| Packaging/runtime | `pyproject.toml`, `frontend/package.json`, `docker-compose.yml`, `supervisord.conf`, `open_notebook/config.py` | dependencies/version, Next/React, DB worker startup, SQLite checkpoint, uploads |
| Docs architecture/product | `VISION.md`, `docs/7-DEVELOPMENT/architecture.md`, `docs/3-USER-GUIDE/citations.md`, `docs/3-USER-GUIDE/search.md`, `docs/3-USER-GUIDE/content-processing-engines.md`, `docs/5-CONFIGURATION/security.md`, `LICENSE` | scope, citations known limitations, config/rights and deployment |
| Domain & source | `open_notebook/domain/notebook.py`, `open_notebook/domain/content_settings.py`, `open_notebook/graphs/source.py`, `open_notebook/utils/chunking.py` | Source/Note/schema, file deletion, extraction flatten, chunking |
| Search & research | `api/routers/search.py`, `open_notebook/graphs/ask.py`, `frontend/src/lib/utils/source-references.tsx`, `prompts/source_chat/system.jinja` | Text/Vector/Ask semantics, UI citation ID grammar |
| API/security | `api/routers/sources.py`, `api/routers/notes.py`, `api/routers/notebooks.py`, `api/models.py`, `api/main.py`, `api/auth.py`, `api/cors.py`, `open_notebook/utils/url_validation.py` | CRUD/download, shared password, CORS, SSRF guards, request limits |
| Worker | `commands/embedding_commands.py`, `commands/source_commands.py` | async execution/retry, embeddings cleanup and source processing |
| DB migrations | `open_notebook/database/migrations/{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28}.surrealql` | inspected definition and search/SQL signatures; full text details sâu nhất ở 1, 3, 4, 9, 24, 25, 26, 28 |
| Tests (source only) | `tests/test_ask_graph.py`, `tests/test_content_core_integration.py` | mocked behavior and code assertions; **not executed** |
| Content Core code | `src/content_core/common/state.py`, `src/content_core/common/types.py`, `src/content_core/extraction.py`, `src/content_core/processors/document/{pdf,epub,docx,docling}.py`, `src/content_core/models.py`, `pyproject.toml`, `LICENSE`, `README.md` | actual library surface, format routes, output type, optional Docling |
| Content Core tests | `tests/unit/test_{pdf,epub,docling}_extraction.py` | test specifications; **not executed** |
| Adjacent repos | Esperanto `README.md`, `pyproject.toml`, `LICENSE`; Surreal Commands `README.md`; Community MCP `README.md` | limited code-depth; không suy diễn runtime |
| BodhiAtlas | `docs/PRD.md`, `docs/V1_CORE_FOUNDATION.md`, `docs/ACADEMIC_RISKS_AND_VERIFICATION.md`; báo cáo P01/P03/P12/P20/P39 được mở như **context only** | nguồn yêu cầu G1–G6, PRD C01–C15, comparator hypotheses |
| BCR | `tools/corpus_research/{model,retrieval,verification,source_resolvers}.py` | scoped evidence verifier vs corpus search; không chạy tests |
| Bang-ha | `tools/local_corpus_framework/corpus/{common,adapters,cli}.py`, `tools/scholarly_ledger.py` | catalog/hash/locator và reviewer-default risk; không chạy trên corpora |

**Giới hạn kiểm kê:** đã mở nhiều file/migration hơn hẳn 15, nhưng không claim codebase được audit 100%. Câu “không có” trong phần kết luận được giới hạn ở **chức năng/schema mặc định được gọi theo luồng đã đọc**, không phải phủ nhận mọi plugin tùy biến hay fork bên ngoài. Chưa lấy Docker image digest, chưa audit `uv.lock`/`package-lock` toàn bộ, transitive dependency SBOM, GPU OCR models hay supply-chain CVE database.

### 13.3. Issue, discussion, release và tài liệu phản chứng

| Nguồn | Loại | Ý nghĩa — không phóng đại |
|---|---|---|
| [Discussion #1315 — Evidence-Centered Research](https://github.com/lfnovo/open-notebook/discussions/1315) | `[PLAN]` | Maintainer nói hướng evidence/provenance, citation exact passage, không timeline; không phải code shipped |
| [Issue #294 — citations](https://github.com/lfnovo/open-notebook/issues/294) | `[ISSUE]` / được dẫn trong #1315 | Dấu hiệu nhu cầu citation đáng tin; không phải benchmark false citation |
| [Issue #648 — highlight overflow](https://github.com/lfnovo/open-notebook/issues/648) | `[ISSUE]` + `[CODE]` fallback | Nhánh xử lý tồn tại trong domain; chưa tái hiện tần suất/đầu vào |
| [Issue #1431 — ranked search](https://github.com/lfnovo/open-notebook/issues/1431) | `[ISSUE]` / comments migration 26 | Có bản sửa GROUP/ORDER; không nhầm thành fix all-occurrences |
| [Issue #1505 — grouping/limit](https://github.com/lfnovo/open-notebook/issues/1505) | `[ISSUE]` / comments migration 26 | Query sửa order/limit, nhưng contract vẫn top-K |
| [Issue #1602 — Node upgrade](https://github.com/lfnovo/open-notebook/issues/1602) | `[ISSUE]` | Mốc vận hành/upstream dependency, cần theo dõi upgrade khi triển khai, không phải lỗ hổng đã khai thác |
| [Open Notebook v1.15.1 security release](https://github.com/lfnovo/open-notebook/releases/tag/v1.15.1) | `[DOC]` release notes | URL/path guard và content-core floor; lời maintainer về kiểm suite/image không biến thành POC của báo cáo |
| [Content Core v2.3.0 release](https://github.com/lfnovo/content-core/releases/tag/v2.3.0) | `[DOC]` release notes | Docling vision remote options; phải kiểm cloud egress theo quyền |
| [Vision Horizon](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/VISION.md#L49-L75) | `[DOC][PLAN]` | V-next migration / MCP ambitions = future only |
| [Open Notebook CITATIONS guide](https://github.com/lfnovo/open-notebook/blob/0c1e7abbd77411057d8feef02fc4588ec9a556d6/docs/3-USER-GUIDE/citations.md#L7-L49) | `[DOC]` | Dẫn rõ citations don't carry page/section/highlight và no citations export |

**Cảnh báo kiểm chứng phụ:** Các issue trong bảng được dùng làm **tín hiệu/bối cảnh**; nơi đánh giá chính dựa trên logic code ở các permalink đã ghim. Trạng thái đóng/mở, root cause cuối cùng và bug frequency của các issue chưa được audit độc lập đầy đủ trong P56.

### 13.4. Reproduction commands, expected logs và bằng chứng thực nghiệm

Các lệnh dưới đây **là kế hoạch**, chưa thực thi. Trên máy thử nghiệm có quyền Docker/GitHub, mạng, dung lượng model thích hợp, dùng tài liệu synthetic/public-domain được cấp phép và **tách môi trường release/HEAD**:

```bash
# NOT EXECUTED: script outline, first pin sources; do not run on a production host.
git clone https://github.com/lfnovo/open-notebook.git
cd open-notebook
git checkout --detach 5e285b7a2e435895c4ee99ad7e4b8d2af64c3239
git rev-parse HEAD
# → expected: 5e285b7a2e435895c4ee99ad7e4b8d2af64c3239
# Copy sample env to a local ignored .env; replace all placeholders and root passwords.
# Do not publish ports beyond localhost. Use separate project/volumes for HEAD.
# docker compose -p on_p56_release up -d --build
# curl --fail http://127.0.0.1:5055/openapi.json > ../on-p56-release-openapi.json

# Independently inspect HEAD in a separate clean worktree:
git worktree add ../open-notebook-p56-head 0c1e7abbd77411057d8feef02fc4588ec9a556d6
# docker compose -p on_p56_head -f ../open-notebook-p56-head/docker-compose.yml up -d --build
# Restrict port binds and volumes before running either Compose stack.

# In a separate, licensed private fixture environment:
# python -m pytest tests/test_ask_graph.py tests/test_content_core_integration.py -q
# curl -sS -X POST http://127.0.0.1:5055/api/search \
#   -H "Authorization: Bearer ${OPEN_NOTEBOOK_PASSWORD}" \
#   -H "Content-Type: application/json" \
#   -d '{"query":"anattā","type":"text","limit":1000}'
```

**Không có measured output.** Trong đoạn lệnh, mọi dòng bắt đầu `# → expected:` là *dự đoán* từ Git ref, không phải stdout của terminal. Không có `pytest PASSED` hoặc Docker `healthy` được báo từ thí nghiệm P56. GitHub release notes/test fixtures chỉ chứng minh rằng mã/tests/tuyên bố tồn tại. Các POC cụ thể, runnable script và ngưỡng PASS/FAIL nằm ở §9.

**Bộ sản phẩm đầu ra bắt buộc khi team chạy POC:** `environment.json` (OS, Python, Docker, CPU/GPU, RAM, engine, models, locked versions), `fixture_manifest.jsonl` (rights, bytes SHA, edition/locator truth, pages), `extraction_runs.jsonl`, `search_runs.jsonl`, `citation_verification_runs.jsonl`, `network_egress.jsonl` và `restore_report.json`; mỗi run có `commit_sha`, `run_id`, `timestamp`, `scope`, `warnings`, `observed`, `expected`, `pass_fail` cùng redaction policy. Chỉ khi các tệp này có kết quả thao tác thực mới được đổi nhãn `[UNKNOWN]/NOT TESTED` thành `[TESTED]`.

### 13.5. Caveats, phạm vi không biết và glossary

**Không thể xác nhận trong nghiên cứu này:** độ nhạy OCR Hán/Tạng/Nôm trên PDF hai cột; CER/WER/latency/RAM/SSD/ingest throughput; sự tương đương release image với HEAD; app stability dưới nhiều user; đầy đủ rights/third-party license/weights; mức độ an toàn SSRF trong adversarial network; correctness tại runtime của SurrealDB-specific functions và migrations; khả năng xuất toàn bộ data/migrate lossless; data-leak qua provider bất kỳ; retention/audit trail; năng lực future Evidence Core sau snapshot. Mọi điểm này là **UNKNOWN hoặc NOT TESTED**, không phải ngầm định PASS hay FAIL.

| Thuật ngữ | Nghĩa dùng trong báo cáo |
|---|---|
| **Raw original / immutable source** | bytes file đầu vào giữ nguyên, gắn SHA-256 và rights; không phải text trích xuất hay URL sống |
| **Canonical extracted text** | bản text với revision/coverage liên kết một file/edition; **không tự bảo đảm** đúng ảnh nếu OCR chưa kiểm |
| **Source Map / locator** | phép ánh xạ span text về file + trang PDF/trang in/bbox, EPUB href+spine+CFI, DOCX path, TEI/HTML ID/XPath khi xác minh được |
| **Work / Edition / Witness** | thực thể thư mục và chứng bản phân biệt; không nhập vì trùng tên hoặc hash text |
| **EXACT** | ký tự gốc theo match contract đã công bố, tìm mọi occurrence trong scope có coverage đã khai; không phải `BM25` hoặc `SEARCH MATCH` nói chung |
| **NORMALIZED** | match sau biến đổi Unicode/dấu/chữ viết, có raw offset map; phải ghi rõ phép biến đổi |
| **FUZZY / LEXICON / SEMANTIC** | gần chữ/OCR, bằng nghĩa thuật ngữ đã chứng thực, hoặc vector tương đồng; không được nâng thành EXACT hay claim support |
| **G1–G6** | ingest, citation, claim, external evidence, lexicon và publish gates theo BodhiAtlas Academic Risks |
| **Evidence Card** | đối tượng trích dẫn kỹ thuật riêng với claim: quote/context, file SHA, edition, locator, coverage, reviewer/state |
| **Scholarly review** | human governance thẩm định ngữ cảnh và mức hỗ trợ luận điểm; không suy từ technical quote VERIFIED |
| **Fail-closed** | thiếu file/locator/quyền/coverage thì trả `UNVERIFIABLE/PARTIAL/UNKNOWN` thay vì tự phong verified hoặc “không có chứng cứ” |
| **Projection** | sao chép **ít metadata đã cho phép**, một chiều, vào ON note/workspace; có canonical link tới BodhiAtlas, không chuyển authority |
| **HEAD/release** | commit phát triển và bản đóng gói công bố khác nhau; không dùng trạng thái branch `main` động thay pinned artifact |

### 13.6. Kết luận triển khai một người / token hữu hạn

**Nếu phải tự triển khai BodhiAtlas bằng nguồn lực và token hữu hạn, tôi sẽ không fork Open Notebook làm lõi: tôi giữ một Minimal Core (D) để lưu file gốc có SHA-256, phân biệt Work/Edition/Witness, bản trích xuất/locator/coverage có phiên bản, tìm code-only exhaustive và xác minh câu trích bằng nguồn độc lập; chỉ thử tái dùng `content-core` ở nơi chứng minh được chất lượng và không mất source map, dùng Direct Docling hoặc parser chuyên biệt ở định dạng khó, hoãn `esperanto` đến khi thật sự bật AI Research, và chỉ chạy Open Notebook nguyên trạng như Research Workspace V2 qua bản chiếu REST nếu POC-4 cho thấy không rò quyền hoặc làm trôi trạng thái. Tôi bỏ native Search/Ask/citation của Open Notebook khỏi đường quyết định `EXACT/VERIFIED` vì BM25 top-K, semantic fallback và item-level citation không đạt hợp đồng BodhiAtlas. Trước khi commit production tôi bắt buộc chạy POC-1 ingestion/coverage, POC-2 ≥50 truy vấn all-occurrence Unicode, POC-3 two-edition/OCR/negation/source-reopen, cùng restore/rights/egress tests POC-5; nếu một hard gate G1/G2/G3/C05 thất bại, dừng triển khai chức năng chứng cứ, không che bằng kết quả AI hoặc demo UI.**
