# Technology Assessment — Dharmamitra / DharmaNexus ecosystem

**Mã:** P41 · **Ngày khảo sát:** 2026-11-16 (Asia/Ho_Chi_Minh) · **Phân loại:** `ecosystem` — phối hợp dịch vụ nghiên cứu, giao diện liên văn bản, corpus phân đoạn, mô hình NLP, từ điển và dataset song hành; **không phải một repository phần mềm nguồn mở đồng nhất**.  
**Địa chỉ chính:** https://github.com/dharmamitra · https://dharmamitra.github.io/dharmamitra-guides/ · https://dharmamitra.org/ · https://dharmamitra.org/db  
**Mốc phiên bản:** web UI tự công bố `v1.51.1-2-g91d74bff`, cập nhật 2026-11-12; đây **không phải** commit của backend. Các SHA *repo cụ thể* tại bảng inventory và Evidence Ledger.  
**Analyst:** thẩm định kỹ thuật độc lập cho BodhiAtlas; đọc PRD V1.4, sổ rủi ro, tài sản sẵn có, tài liệu chính thức, repository metadata/tree/README, các file code và dữ liệu mẫu qua GitHub connector, đối chiếu website/Hugging Face. **Không chạy API thật, không benchmark corpus, không clone/checksum toàn bộ dữ liệu.**  
**Quy ước bằng chứng:** `[DOC]` tuyên bố của tác giả/tài liệu; `[CODE]` đã đọc nội dung code/schema/sample record; `[ISSUE]` trạng thái issue/PR được xem; `[TESTED]` phép đo do cuộc khảo sát tự chạy; `[INFERRED]` suy luận có điều kiện; `[UNKNOWN]` thiếu chứng cứ. Khi `NOT TESTED` nghĩa là **không có kết quả chạy thực nghiệm**; các thống kê sản phẩm là số tự công bố, không là số đo độc lập.

## 1. Executive Decision

**Quyết định: `USE AS COMPONENT` — có điều kiện về giấy phép, với chế độ mặc định chỉ tham chiếu học thuật ngoài hệ thống. Không `ADOPT` toàn bộ làm V1 Core.**  
**Confidence:** `MED` cho phân loại kiến trúc và cơ hội tái sử dụng; `LOW` cho hành vi API live, tính đủ/chính xác corpus, quyền tái phân phối trên từng record và thời gian/chi phí vận hành chưa thử.

- **V1:** ưu tiên sử dụng dữ liệu upstream trực tiếp đã được cấp phép, hoặc corpora công khai được kiểm quyền theo từng tác phẩm; có thể lấy **catalog/segment ID** của Pāli, Sanskrit, Chinese làm crosswalk hoặc nguồn tham khảo. Không thay thế bộ nạp PDF/EPUB/DOCX, OCR được kiểm, kho file SHA-256, verified citation/source map, và exhaustive `EXACT` code-only của BodhiAtlas. Xây engine gốc V1 trong local stack; không dùng API Dharmamitra để “populate” giao diện BodhiAtlas khi chưa có giấy phép riêng.
- **V2:** thí điểm MITRA-lexicon để gợi ý nghĩa, bản dịch và dẫn chứng ở mức *candidate*; có thể dùng `mitra-bo-zh-tagger` và ByT5 ở tầng phân đoạn/phân tích **phái sinh**, không ghi đè văn bản gốc; crosswalk đến kho nguồn bất biến là điều kiện tiên quyết.
- **V3:** sau quyền sử dụng/POC và giao diện duyệt học thuật, mới cân nhắc song hành liên ngữ từ MITRA-parallel v3, mô hình MT/embeddings, hoặc service adapter ngoài; AI diễn giải không cấp quyền trích dẫn đã xác minh.

**Ba rủi ro chặn quyết định:** (1) **điều khoản API** chính thức cấm dùng API/DharmaNexus database API để populate ứng dụng bên thứ ba, presentation layers hay staging environments nếu chưa được trao đổi/cấp quyền; (2) **đúng bản văn khác đúng ấn bản/file gốc**: segment/corpus ID và tự động alignment chưa chứng minh PDF page+bbox/EPUB CFI/độc lập verifier; (3) **quyền và chất lượng không đồng nhất**: code MIT, weights, bản dịch, metadata AI, corpora VRI/CBETA/GRETIL, lexicon có `CC BY-NC-ND`, `CC BY-SA`, prosopography `CC BY-NC-SA` và quyền riêng của upstream.

**Gate, không dùng điểm tổng để vượt qua:** `SOURCE_FIDELITY=UNKNOWN` cho re-open về file gốc của BodhiAtlas (`N/A` nếu chỉ xét vai trò candidate scholarly reference); `CODE_ONLY_EXACT=N/A` đối với lexicon/corpus song hành, **không có bằng chứng ecosystem đạt exhaustive EXACT**; `MULTILINGUAL=UNKNOWN` cho tập test riêng BodhiAtlas (có khả năng đa ngôn ngữ `[DOC]` nhưng chưa đo); `QUALITY_COVERAGE=UNKNOWN`; `RIGHTS_SECURITY=UNKNOWN` và **không được triển khai API tích hợp khi chưa được phép**; `PORTABILITY=PARTIAL/UNKNOWN` tùy phương thức tự quản corpus và ID mapping.

## 2. Sources & Evidence Ledger

**Snapshot đã mở:** PRD V1.4 và sổ rủi ro trong `quoctran-2608/bodhi-atlas`; `BuddhismDocuments-for-AI`; hướng dẫn DharmaNexus chính thức; repo metadata/tree + README/schema/code dưới đây; website đang công bố; mô tả model Hugging Face. Đã liệt kê issue/PR của một số repo nhưng **không** kết luận mức độ sửa bug theo số issue. SHA trong bảng là **head commit** của default branch vào 2026-11-16, còn link `blob/.../` trỏ tại SHA đó để đọc lại. Website là dynamic version, không có backend SHA công khai được xác nhận.

| claim_id | claim | Loại | URL/file+line hoặc permalink | version/SHA | Ghi chú / giới hạn |
|---|---|---|---|---|---|
| P41-E01 | PRD bắt buộc local exact, từng vị trí, provenance và multimode search | `[DOC]` | https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/PRD.md | blob `58d967c642d625180c436e1a6e6a75fa2e7070e3` | Đã đọc nội dung qua connector; phiên bản PRD V1.4 |
| P41-E02 | Sổ rủi ro tách trạng thái nguồn, trích dẫn, diễn giải; cấm gộp các tầng | `[DOC]` | https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/ACADEMIC_RISKS_AND_VERIFICATION.md | blob `cdb642633f3dc3f7f83cb0e49a96abfebc9f132e` | Ngày tài liệu 2026-11-15 |
| P41-E03 | Repo tài sản hiện có có 13 upstream pin, SQLite/FTS, CLI verification và hạn chế nghiệm thu V2 | `[DOC]` | https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/main/README.md | blob `fd237c107445bc2a4f6f5999c8b66a8380335cfe` | Số test do repo báo cáo, KHÔNG test P41 |
| P41-E04 | DharmaNexus là công cụ corpus/intertextuality bốn ngôn ngữ và kế tiếp BuddhaNexus | `[DOC]` | https://dharmamitra.github.io/dharmamitra-guides/dharmanexus/ | Web, 2026-11-16 | Tài liệu mô tả, không chứng minh backend open-source |
| P41-E05 | DharmaNexus không có engine search riêng mà dựa MITRA Search | `[DOC]` | https://dharmamitra.github.io/dharmamitra-guides/dharmanexus/#for-buddhanexus-users | Web | Các guide có câu “currently” có thể cũ |
| P41-E06 | ToS cấm dùng API để populate ứng dụng third-party/presentation/staging; mời liên hệ xin phép | `[DOC]` | https://dharmamitra.github.io/dharmamitra-guides/dharmanexus/#terms-of-service | Web, các dòng 141–146 | Đây là blocker pháp lý rõ nhất |
| P41-E07 | Website `/db` công bố bốn ngôn ngữ và version UI tháng 11/2026 | `[DOC]` | https://dharmamitra.org/db | `v1.51.1-2-g91d74bff` | Không đồng nghĩa server/source commit |
| P41-E08 | Sanskrit repo là corpus từ GRETIL, DSBC, Muktabodha, ilx_skt; có per-text attribution | `[DOC]` | https://github.com/dharmamitra/dharmanexus-sanskrit/blob/aec80af58c2bbd18477553f350bf067ed7807ea7/README.md | `aec80af5…` | Không có quyền chung cho mọi record |
| P41-E09 | Sanskrit metadata có `filename`, `filenr`, `uniformtitle`, author role và source | `[CODE]` | https://github.com/dharmamitra/dharmanexus-sanskrit/blob/aec80af58c2bbd18477553f350bf067ed7807ea7/metadata/SA_GK19_Mayūra_Sūryaśataka_Quackenbos_1917-metadata.json | `aec80af5…` | Đọc một mẫu, không đảm bảo mọi record đồng nhất |
| P41-E10 | Prosopography Sanskrit là bản nháp LLM, chưa specialist verify; license CC BY-NC-SA | `[DOC]` | https://github.com/dharmamitra/dharmanexus-sanskrit/blob/aec80af58c2bbd18477553f350bf067ed7807ea7/prosopography/README.md | `aec80af5…` | Quyết định thư mục/dị bản phải review |
| P41-E11 | Pāli sample có segmentnr, original, analyzed, folio, SuttaCentral link | `[CODE]` | https://github.com/dharmamitra/dharmanexus-pali/blob/74e0f1a70476cfa7c45e5ca1335ac3ed0d5c1fe8/segments/PA_an_1.json | `74e0f1a…` | `folio` không mặc định là trang PDF |
| P41-E12 | Pāli README ghi VRI và SuttaCentral; tác giả hạn chế non-commercial | `[DOC]` | https://github.com/dharmamitra/dharmanexus-pali/blob/74e0f1a70476cfa7c45e5ca1335ac3ed0d5c1fe8/README.md | `74e0f1a…` | Original PD không xóa quyền data packaging |
| P41-E13 | Pāli raw_metadata có *AI-generated Overview* và danh sách parallels tự động | `[CODE]` | https://github.com/dharmamitra/dharmanexus-pali/blob/74e0f1a70476cfa7c45e5ca1335ac3ed0d5c1fe8/metadata/PA_an_1-metadata.json | `74e0f1a…` | Tuyệt đối không coi đoạn tóm tắt như nguồn nguyên cấp |
| P41-E14 | Chinese repo chứa Taishō/Zokuzōkyō/Kanripo, cấp juan, Bunkankun AI summary | `[DOC]` | https://github.com/dharmamitra/dharmanexus-chinese/blob/aa362ea779a9238260cdd84a8f1d6384e8407437/README.md | `aa362ea…` | Guide cũ nói thiếu X; repo hiện mô tả có X: không tự kết luận độ phủ live |
| P41-E15 | MITRA-parallel `v3/` current Oct 2026 với 1,690,655 alignment records theo README | `[DOC]` | https://github.com/dharmamitra/mitra-parallel/blob/0a770d98283b826134da0d8ec4d75259350faaa0/README.md | `0a770d9…` | Nhà phát hành công bố; không đo độc lập |
| P41-E16 | v3 có 3 cặp SA–BO, SA–ZH, BO–ZH, 6 hướng, vecalign + post-corrector | `[DOC]` | https://github.com/dharmamitra/mitra-parallel/blob/0a770d98283b826134da0d8ec4d75259350faaa0/v3/README.md | `0a770d9…` | P42 đánh giá chi tiết chất lượng benchmark |
| P41-E17 | MITRA-lexicon v1.1 lưu mỗi sense với attestations ID, offsets, quality flags | `[DOC]` | https://github.com/dharmamitra/dharmamitra-lexicon/blob/f61c572930cca49fe7654ffda1555c3937e5bf3a/README.md | `f61c572…` | Dữ liệu sinh từ aligner, không tự là nghĩa đúng |
| P41-E18 | Lexicon code MIT, các release data có CC BY-SA hoặc BY-NC-ND tùy pack | `[DOC]` | https://github.com/dharmamitra/dharmamitra-lexicon/blob/f61c572930cca49fe7654ffda1555c3937e5bf3a/LICENSE.md | `f61c572…` | Rights trong source sentences vẫn giữ nguyên |
| P41-E19 | Quy trình tái tạo lexicon dùng absolute build paths, external scripts, teacher Gemini, vLLM | `[CODE]` | https://github.com/dharmamitra/dharmamitra-lexicon/blob/f61c572930cca49fe7654ffda1555c3937e5bf3a/code/README.md | `f61c572…` | Reproduce full end-to-end chưa chứng minh |
| P41-E20 | Normalization Wylie xóa particles và gộp verb lemmas; forms riêng | `[CODE]` | https://github.com/dharmamitra/dharmamitra-lexicon/blob/f61c572930cca49fe7654ffda1555c3937e5bf3a/code/pipeline/5-build/tib_norm.py | `f61c572…` | Không thể coi normalized form là nguyên văn đảo ngược |
| P41-E21 | CLI agent script công khai route `/matches/`, `/menudata/`, `/table-view/table/` | `[CODE]` | https://github.com/dharmamitra/dharmamitra-claude-code-agent/blob/63a39fe679575751a7a95358801257ba2fb92726/scripts/nexus.sh | `63a39fe…` | Client chứng minh shape code, không chứng minh API SLA/ToS |
| P41-E22 | Table API paging 100 rows/page; script nhắc dùng `--all` | `[CODE]` | https://github.com/dharmamitra/dharmamitra-claude-code-agent/blob/63a39fe679575751a7a95358801257ba2fb92726/scripts/nexus.sh | `63a39fe…` | Bỏ phân trang có thể báo âm tính giả |
| P41-E23 | Search client cho `regular`, `semantic`, `semantic_only` và `src_link` | `[CODE]` | https://github.com/dharmamitra/dharmamitra-claude-code-agent/blob/63a39fe679575751a7a95358801257ba2fb92726/scripts/primary-search.sh | `63a39fe…` | `regular` KHÔNG chứng minh exhaustive char-exact |
| P41-E24 | Cache corpus local từ API là index danh mục, không phải local toàn văn | `[CODE]` | https://github.com/dharmamitra/dharmamitra-claude-code-agent/blob/63a39fe679575751a7a95358801257ba2fb92726/scripts/build-corpus-index.py | `63a39fe…` | Giấy phép API vẫn áp dụng lúc tạo cache |
| P41-E25 | Tagger BO/ZH là Python package MIT, HF weights cần kiểm license riêng | `[CODE]` | https://github.com/dharmamitra/mitra-bo-zh-tagger/blob/b678dbe73c3113021aedf164b04cb94eb6b54f84/pyproject.toml | `b678dbe…` | `torch`, `transformers`, `pyewts`, `accelerate`; model lớn |
| P41-E26 | Tagger docs nêu round-trip validation, Trung văn bỏ dấu câu đầu vào rồi dự đoán lại | `[DOC]` | https://github.com/dharmamitra/mitra-bo-zh-tagger/blob/b678dbe73c3113021aedf164b04cb94eb6b54f84/README.md | `b678dbe…` | Source fidelity cần giữ nguyên trước xử lý |
| P41-E27 | Repo ByT5 cung cấp inference scripts, training/data chưa hoàn chỉnh theo README | `[DOC]` | https://github.com/dharmamitra/byt5-sanskrit-analyzers/blob/3f25e158e862b029d6cd7bd20653f903c466635f/README.md | `3f25e15…` | Không đồng nhất inference open với toàn bộ pipeline open |
| P41-E28 | Claude-agent issue #3 là đề xuất optional offline fojin-cli, chưa phải tích hợp hiện hành | `[ISSUE]` | https://github.com/dharmamitra/dharmamitra-claude-code-agent/issues/3 | Trạng thái `open` khi khảo sát | Issue là ý định/trao đổi, không phải test hay feature release |
| P41-E29 | Gốc `/db` mô tả khác guide cũ tại tính năng X, OCR/phiên bản; cần live contract validation | `[INFERRED]` | https://dharmamitra.org/db ; https://github.com/dharmamitra/dharmanexus-chinese | Web 2026-11-12 / repo 2026-10-13 | Tài liệu khác thời điểm, không kết luận bug |
| P41-E30 | Không xác minh được public server/backend source và toàn bộ Tibetan dump qua link của guide | `[UNKNOWN]` | https://dharmamitra.github.io/dharmamitra-guides/dharmanexus/ (liên kết Tibetan GitHub); https://github.com/dharmamitra/dharmanexus-tibetan | 2026-11-16 | Link đích trả 404 trong lần mở; có thể đổi tên/mất quyền, chưa được chứng minh redirect |

### Inventory repo/sản phẩm theo vai trò

| Component | Đơn vị sở hữu/chủ quản quan sát | Repo/site, branch `HEAD` khảo sát | Loại; mức trưởng thành quan sát | Quyền đã biết / trạng thái |
|---|---|---|---|---|
| DharmaNexus web/DB/intertextuality | Dharmamitra consortium | https://dharmamitra.org/db; UI `v1.51.1-2-g91d74bff` | Hosted app/service đang cập nhật | Server code/DB dump tổng thể `UNKNOWN`; ToS chặn third-party populate |
| MITRA Search, Translate, Deep Research, OCR | Dharmamitra | https://dharmamitra.org/; https://dharmamitra.github.io/dharmamitra-guides/ | Hosted services; tài liệu công khai | Chưa chứng minh self-host của từng service; API rights riêng |
| DharmaNexus Sanskrit | Dharmamitra | https://github.com/dharmamitra/dharmanexus-sanskrit · `master` `aec80af58c2bbd18477553f350bf067ed7807ea7` | Corpus + metadata + processing utilities, active/not archived | Hỗn hợp license từng upstream, prosopography NC-SA |
| DharmaNexus Pāli | Dharmamitra | https://github.com/dharmamitra/dharmanexus-pali · `main` `74e0f1a70476cfa7c45e5ca1335ac3ed0d5c1fe8` | Corpus segmented; active/not archived | README hạn chế dùng noncommercial, attribution VRI |
| DharmaNexus Chinese | Dharmamitra | https://github.com/dharmamitra/dharmanexus-chinese · `master` `aa362ea779a9238260cdd84a8f1d6384e8407437` | Corpus + AI metadata; active/not archived | Bunkankun summaries CC BY-SA, CBETA/upstream xem riêng |
| DharmaNexus Tibetan | Dharmamitra? | Link guide đến `dharmanexus-tibetan` 404 | `UNKNOWN`, không suy thành chưa tồn tại | Chưa xác nhận dump/commit/license |
| MITRA-parallel (P42) | Dharmamitra | https://github.com/dharmamitra/mitra-parallel · `main` `0a770d98283b826134da0d8ec4d75259350faaa0` | Dataset `v3` current, v1/v2 archived in directory | License toàn v3 cần xác nhận ở record/upstream; không phải engine OCR/search |
| MITRA-lexicon | Dharmamitra | https://github.com/dharmamitra/dharmamitra-lexicon · `main` `f61c572930cca49fe7654ffda1555c3937e5bf3a` | Artifact + scripts/eval và release v1.1, active | MIT code; các pack CC BY-SA/NC-ND riêng |
| BO/ZH tagger | Dharmamitra | https://github.com/dharmamitra/mitra-bo-zh-tagger · `master` `b678dbe73c3113021aedf164b04cb94eb6b54f84` | Python NLP component, 9B model bên ngoài | MIT code, weight card cần khóa revision/license |
| ByT5 Sanskrit analyzers | Dharmamitra | https://github.com/dharmamitra/byt5-sanskrit-analyzers · `main` `3f25e158e862b029d6cd7bd20653f903c466635f` | Inference code thành phần; repo last push 2024 | Training/data toàn phần chưa xuất bản theo README |
| Claude Code agent starterpack | Dharmamitra | https://github.com/dharmamitra/dharmamitra-claude-code-agent · `main` `63a39fe679575751a7a95358801257ba2fb92726` | Public **API clients/workflow prompts**, không phải server | No key claim không miễn ToS; hosted/cloud calls |
| MITRA-parallel HTML | Dharmamitra | https://github.com/dharmamitra/mitra-parallel-html · `main` `fcda3f1dac7fa3d89955e13b58f029a9e2145301` | Static browser cho TSV cũ | Build paths liên quan v1, cần update nếu dùng v3 |
| StarDict dictionaries | Dharmamitra | https://github.com/dharmamitra/dharmamitra-stardict-dictionaries · `main` `5e704d14e757f3d5709e141346ee3d2464e2fddb` | README, link tới dữ liệu StarDict; khác MITRA-lexicon v1.1 | Rights/bản cập nhật pack chưa kiểm, không có server source |

**Mức “active”:** chỉ xác nhận repository *không bị archived* và ngày commit gần đây ở một số repo; không suy đoán SLA, số người duy trì, mức bao phủ thực tế. GitHub stars/release latest của site **không** dùng làm tiêu chí. Các HEAD có thể đổi sau snapshot; clone phải `git checkout <full SHA>`.

## 3. Architecture & Data Flow

Đây là sơ đồ **lineage/phụ thuộc** từ tài liệu và code client; phần server có dấu `?` là không kiểm được source backend. Không giả định MITRA-parallel *tạo ra toàn bộ* matches live của DharmaNexus.

```mermaid
flowchart TB
  A[Upstream text editions: Bilara/VRI, GRETIL/DSBC/Muktabodha, CBETA, ACIP/Tsadra] --> B[Segmented DharmaNexus corpora: PA/SA/ZH/BO]
  B --> C[DharmaNexus DB / intertextuality hosted backend ?]
  B --> D[MITRA Search hosted index ?]
  D --> E[/api-search/primary/ - search candidate]
  C --> F[/api-db/menudata/matches/table-view/]
  G[Embeddings + cross-language mining pipeline] --> H[MITRA-parallel v3 dataset]
  B --> G
  H --> I[MITRA-lexicon aligner / sense+attestation mining]
  I --> J[Versioned lexicon NDJSON releases]
  K[ByT5 Sanskrit; BO/ZH tagger; MT weights] --> D
  K --> I
  E --> L[Public web/agent CLIENTS]
  F --> L
  J --> M[Optional offline lexicon adapter, RIGHTS GATE]
  B --> N[Optional local corpus adapter, per-record rights gate]
  N --> O[BodhiAtlas corpus registry + immutable raw files + hashes]
  M --> P[Candidate lexicon/parallel suggestions]
  O --> Q[Local exact/normalized/fuzzy + independent verifier]
  P --> Q
  Q --> R[Verified citation card + coverage manifest]
  L -. Not allowed to populate third-party app without authorization .-> R
```

**Điểm đứt chủ yếu:** Web và agent client công khai **không chứng minh** API server, search backend, provenance resolver và khôi phục DB đều có source code để self-host. Dữ liệu phát hành riêng/thuộc nhiều upstream; bản `v3` của P42 chứa các cặp aligned mined, không chứa bản PDF/scan và không mang trọn nhãn witness/edition từ thư viện cá nhân.

## 4. Feature Fit–Gap Matrix

Trạng thái là **từng vai trò tái sử dụng hợp pháp** của P41, **không** phải điểm chấm toàn sản phẩm. `N/A` không là điểm trừ. `NATIVE` chỉ nói có tại component được mô tả; không tự động qua gate của BodhiAtlas. Công sức: `S/M/L` ước tính định tính theo công việc, **chưa đo giờ**. Mỗi dòng nêu căn cứ ngắn (tra E## ở ledger), gap và phương án.

| Mã | Năng lực | Status | Evidence / vai trò thực | Công sức | Gap BodhiAtlas, công việc bù |
|---|---|---|---|---|---|
| C01 | Multi-format ingest PDF/EPUB/DOCX/MD/TEI | `N/A` | P41-E08/E11/E14: đây là corpus segmented có sẵn, không phải pipeline thu nhận sách bất kỳ | S (kết nối), L (Core) | BodhiAtlas tự xây ingest/format detector và versioning; dùng Docling/OCR adapters khác |
| C02 | OCR/layout/reading order | `EXTERNAL` | Dharmamitra có hosted OCR `[DOC]`, không chứng minh bbox/layout source map tương thích; E04 | L | OCR sang raw scan và từng bbox độc lập; không dùng bản dịch model chứng minh câu chữ |
| C03 | Canonical text/source map | `EXTENSION` | E09/E11/E14: original + segment ID + folio/url xuất hiện ở mẫu | L | Map corpus IDs đến edition, file SHA, page+bbox/CFI; PDF witness absent |
| C04 | Works/editions/witnesses | `EXTENSION` | E09/E10: metadata work/author/source; upstream khác nhau | L | Crosswalk work vs edition vs translation vs witness; ID versioning/attribution_review |
| C05 | Exhaustive EXACT code-only | `N/A` | E05/E23: hosted search `regular` != exact mọi occurrence | L cho BodhiAtlas | Implement local byte/codepoint substring scan and occurrence offsets; audit 5 repeats/300 chars |
| C06 | Multilingual normalized search | `EXTENSION` | E20/E23/E26: ByT5, BO/ZH analyzer, Wylie and search filters | M–L | Vietnamese dấu, Han variant mapping, reversible display mapping, query-by-script gold suite |
| C07 | Fuzzy/near-duplicate/OCR errors | `CONFIG` | E04/E16: text similarity/mined parallels có sẵn, không phải sửa lỗi OCR nguồn cá nhân | M–L | Fuzzy index riêng, OCR confidence/error manifest, fail highlights |
| C08 | Sense-aware lexicon | `NATIVE` (lexicon artifact) | E17/E18/E19: headword→senses→attestations/offsets | M | License pack, calibrate false senses/negative examples; provenance crosswalk/pinning |
| C09 | Semantic/hybrid/RAG | `EXTERNAL` | E05/E23: MITRA Search, Qwen/embedding/Claude workflow; không phải native local BodhiAtlas | M–L | Optional engine; never source of citation; permission & private data gate |
| C10 | Verified citation card/source reopen | `EXTENSION` | E11/E17/E21: segment and sentence offsets `src_link`; **chưa có independent verifier** | L | Verify file SHA/version, raw chars, position+context, page/bbox, 3-state validation |
| C11 | Note/wiki/claim memory | `N/A` | P41 không có bằng chứng sản phẩm claim store/Second Brain vững và export | L cho V1/V2 | Dùng tài sản BodhiAtlas/BuddhismDocuments-for-AI, tránh khóa vào agent output |
| C12 | API/MCP/export | `EXTERNAL` | E21–E24: hosted HTTP APIs + script client, table spreadsheet xuất được; MCP server `UNKNOWN` | M nếu permitted, L nếu custom | **ToS hard blocker** trước khi dùng app API; có thể import local data hợp pháp; MCP wrapper không giải quyết quyền |
| C13 | Quality coverage/incremental | `EXTENSION` | E10/E13/E16: QC filters và metadata cảnh báo có, repo ngày cập nhật khác nhau | L | Local coverage manifest per-work per-page, OCR errors, tombstones, refresh delta checksum |
| C14 | Auth/licensing/privacy/backup | `UNKNOWN` | E06/E12/E18: quyền phân tách; agent claim unkeyed ≠ được tích hợp | L | ACL source license, secret/key policy, private-file no upload, snapshots và restore drill |
| C15 | Operational simplicity/independent deploy | `UNKNOWN` | E19/E24/E27: client/scripts open; server source thiếu; lexicon build paths ngoài | L | Self-host chỉ ở vài adapter/models; không chốt platform; CI pin deps & reproducible builds |

**Cổng V1 thất bại nếu:** service chỉ trả top-k mà không liệt kê mọi vị trí; source map không quay lại file gốc đúng edition; API bị dùng trái ToS; thiếu coverage manifest; normalized/token semantics bị gọi `EXACT`; ép user gửi file riêng tư lên cloud.

## 5. Deep Technical Findings

### 5.1. Hệ sinh thái gồm những lớp nào? (Câu hỏi 1)

**Bốn nhóm tách rời:** (a) web apps hosted (`DharmaNexus / MITRA Search / Translate / OCR / Deep Research`), (b) corpora được phân đoạn (`dharmanexus-sanskrit`, `-pali`, `-chinese`; Tibetan dump chưa xác nhận theo link), (c) artifacts/model nghiên cứu (`MITRA-parallel v3`, `MITRA-lexicon v1.1`, tagger/ByT5/MT weights), (d) client/research workflow (`dharmamitra-claude-code-agent`, MITRA-parallel-html, StarDict). Chỉ các lớp (b/c/d) có tài sản công khai cụ thể như inventory. Không đồng nhất quyền đọc GitHub với quyền sử dụng mọi nội dung.

### 5.2. DharmaNexus và BuddhaNexus cũ (Câu hỏi 2)

Tài liệu chính thức gọi DharmaNexus là tiếp nối của BuddhaNexus ở phần khảo sát song hành, thay đổi giao diện/thuật toán và thay engine search bằng MITRA Search. Website có nút “classic DharmaNexus”. BuddhaNexus repo/tài liệu cũ là **historical reference**, không được dùng làm API/schema production hiện hành. Migration cấp database, mapping IDs, redirect link cũ và trạng thái archived của **từng** repo chưa được chứng minh trong cùng snapshot; công bố `UNKNOWN`. Để di trú: export danh mục `old_id`, `new_id`, `edition_id`, `segment_span`, `redirect_evidence`, `text_hash`, `verification_status`, rồi thử 100 liên kết ngẫu nhiên và 10 ca đổi đoạn; không tự chuyển tên theo heuristic.

### 5.3. Matching symbolic, n-gram, embeddings, model và offline (Câu hỏi 3)

- `[DOC]` MITRA-parallel v3 dùng kNN margin scoring với biểu diễn vector để khai thác anchor, chuỗi span đơn điệu, `vecalign` và model post-correction; *không phải* literal exact cross-lingual. DharmaNexus bản cũ và dịch vụ web còn có thuật toán similarity/score, nhưng không kiểm được source server hiện tại nên không tự gán từng API result cho một thuật toán.
- `[DOC]` guide nói Tibetan special substitution stemmer; ByT5 Sanskrit/Pāli segmentation và Chinese Elasticsearch analyzers; search có sentence/paragraph embeddings. `semantic` là candidate retrieval, chưa chứng minh đồng nghĩa hoặc evidence certainty.
- **Offline/code-only thực sự:** repo `mitra-parallel` static NDJSON và MITRA-lexicon static NDJSON, nếu được phép và tải bản release phù hợp, có thể lọc JSON bằng code. `mitra-bo-zh-tagger`/ByT5 có inference local sau khi có weights/phần cứng và kiểm giấy phép. **Tự tái chạy full v3 mining pipeline hoặc tự host API backend**: `UNKNOWN` vì code server/pipeline/weights/dữ liệu cần thiết chưa xác minh đủ. No network == không live service; cache menu của agent không biến toàn bộ database thành offline.

### 5.4. Source/work/witness/segment IDs và mở lại nguồn (Câu hỏi 4)

- Pāli record mẫu `[CODE]`: `segmentnr = PA_an_1:1.0.1`, `original = Aṅguttara Nikāya 1`, `analyzed = aṅguttara nikāya `, `folio = "1"`, `suttacentral_link = https://suttacentral.net/an1.1-10/pli/ms#an1.1_0.1`. **Dẫn được đến segment công bố**; không có file PDF SHA hay bbox trong record này.
- Sanskrit metadata mẫu: `filename = SA_GK19_Mayūra_Sūryaśataka_Quackenbos_1917`, work label `Sūryaśataka`, author `Mayūra`, `source = G. P. Quackenbos…1917` và note có chỉnh sandhi; **đó là record corpus**, chưa đủ chứng minh ảnh trang của bản in này.
- Chinese `ZH_T*` có thể map sang CBETA Taishō; `/metadata` và `segments` tổ chức theo juan; metadata được nối Bunkankun không phải lời giải thích lịch sử chuyên gia đã duyệt.
- `MITRA-parallel v3` giữ `root_segnr`, `par_segnr` và text; MITRA-lexicon `ex[].id`, `ex[].tgt_segnr` (tùy pair) và char `start/end`. Need `locator_crosswalk` mapping các upstream IDs đến immutable `bodhi_file_id`, `edition_id`, anchor in raw source, rồi **đọc lại**. Giữ `source_segment_id` là external identifier, không dùng làm `bodhi_file_id`.

### 5.5. Dịch thuật AI, citation và align (Câu hỏi 5)

**Ba loại bằng chứng:** (i) `translation_generated`: model sinh ra để đọc hiểu, **không** phải bản dịch có bản quyền tác giả như một witness độc lập; (ii) `candidate_alignment`: một tương ứng máy tìm giữa đoạn/term, có thể mang score/quality signals, **không** là `VERIFIED_PARALLEL`; (iii) `verified_citation`: văn bản nguyên bản tại edition/file được mở và match về ký tự/vị trí, **không** suy ra nghĩa. V3 nói có post-corrector và decontamination; đây là quy trình QC theo tác giả, **không chứng nhận từng cặp đúng nghĩa**. Bộ negative examples xuyên truyền thống và lỗi đổi phủ định được đánh giá riêng `NOT TESTED`.

### 5.6. Kênh truy cập, API và bền URI (Câu hỏi 6)

`/api-db/menudata/?language={sa|bo|zh|pa}` (`GET`), `/api-db/matches/` (`POST`), `/api-db/table-view/table/` (`POST`, phân trang); `/api-search/primary/` (`POST`), đã quan sát **trong mã client** chứ chưa gọi thử. Đường clone/download: `dharmanexus-{pali,sanskrit,chinese}`, `mitra-parallel/v3/*.ndjson.gz`, GitHub release MITRA-lexicon v1.1 `*.ndjson.zst` + `SHA256SUMS.txt`, Python tagger package, HF model cards. URL `src_link` từ API cần kiểm độ bền/redirect sau phiên bản. `UNVERIFIED`: API schema live, rate limits, auth, service uptime, TOS riêng từng endpoint, max page/version, status codes, pagination exhaustion. **Không dùng API để populate BodhiAtlas cho tới khi có chấp thuận bằng văn bản.**

### 5.7. Unicode/phiên tự/normalization trong Tibetan và Sanskrit (Câu hỏi 7)

`mitra-lexicon` mô tả Tibetan dictionary keys dùng **Wylie**; `tib_norm.strip_particles()` xóa trailing particles và `verb_root()` gộp động từ (khi có map); bản gốc/indices phải được giữ tách. `mine_direction.py` dùng `pyewts` để đổi Wylie thành Tibetan Unicode khi đưa vào model, tức encoding conversion tại ranh giới. Cần kiểm Unicode NFC/NFD, tsheg/shad, combining marks, Wylie escape/round-trip, homographs, Sanskrit sandhi/lemma, chữ Hán phồn/giản và lossless source-offset maps. Tagger mô tả một số kiểm reconstruction nhưng chính model có thể **thay dấu câu Hán**, không được dùng output để thay nguyên văn. License code MIT ≠ model weights/data; HF weight license phải khóa revision và legal review.

### 5.8. Open-source hay external service? (Câu hỏi 8)

Không có căn cứ gọi **toàn hệ sinh thái là open-source hoàn chỉnh có thể self-host**: chỉ xác minh được các repo corpus, artifact, inference, utility và agent *client*. Không tìm thấy bằng chứng công khai đủ của server source và complete dump cho toàn web stack; Tibetan download link chính thức đang không mở qua lần thử web. Treat API/web as **external scholarly reference**; không dùng danh nghĩa open-source để né điều khoản truy cập.

### 5.9. Ranh giới P41 và P42 (Câu hỏi 9)

P41 xét **hệ sinh thái/quan hệ phụ thuộc, source fidelity, API/rights, tích hợp ứng dụng và glossary/segmentation**. P42 đánh giá **dataset MITRA-parallel v3 như artifact độc lập**: cặp align, schema, sampling, licenses, duplicate/decontam, precision/recall, negative controls. P41 chỉ trích các thông tin cần lập bản đồ: v3 current, 3 cặp ngôn ngữ, được dùng upstream bởi lexicon, không tự cấp độ tin cậy trích dẫn. Không trộn số record của v1/v2/v3 hay cho rằng v3 gồm Pāli.

### 5.10. Chiến lược tích hợp (Câu hỏi 10)

Ba kiến trúc cụ thể ở mục 8. Nguyên tắc: **BodhiAtlas sở hữu IDs, raw assets, license decisions, verified claims, coverage; component bên ngoài chỉ thêm candidate**. Mọi đường API chỉ được kích hoạt sau rights gate; phương án an toàn mặc định là link ngoài thủ công hoặc local artifact có license rõ. Nếu nguồn ngoài đổi hoặc chết: giữ nội dung có quyền được lưu + hash và tái tạo index nội bộ; nếu không có quyền cache, ngắt adapter và vẫn cho local exact.

## 6. Source Fidelity & Provenance

**Không đánh đồng bốn vật:** `work` (tác phẩm học thuật) ≠ `edition/witness` (bản văn xác định) ≠ `source_file` (byte/file bất biến) ≠ `segment` (đơn vị kỹ thuật ở corpus). Một match across text families chỉ là `parallel_candidate` trước khi người thẩm định gán `translation_of`, `parallel_to`, `quotation_of`, `variant_of` và lý do.

**Citation card contract đề xuất** — *schema BodhiAtlas phải xây*, không tuyên bố P41 đang xuất đúng schema này:

```json
{
  "work_id": "BA-WORK-...",
  "edition_id": "BA-EDITION-...",
  "witness_id": "BA-WITNESS-...",
  "file_id": "BA-FILE-...",
  "file_sha256": "<computed_from_immutable_raw_bytes>",
  "external_source": {"provider": "dharmanexus", "repo_commit": "<pinned_sha>", "segmentnr": "PA_an_1:1.0.1", "uri": "<checked_upstream_uri>"},
  "author": null, "translator": null, "source_role": "original_or_translation_or_commentary_unknown",
  "quote_original": "<raw_substring_only>",
  "work_section": null,
  "locator": {"kind": "pdf_bbox_or_epub_cfi_or_tei_xpath_or_corpus_segment", "pdf_page": null, "printed_page": null, "bbox": null, "epub_cfi": null, "href": null},
  "match_type": "EXACT_OR_NORMALIZED_OR_FUZZY_OR_LEXICON_OR_SEMANTIC",
  "index_coverage": "READY_OR_PARTIAL_OR_NOT_INDEXED_OR_UNAVAILABLE",
  "ocr_status": "NOT_APPLICABLE_OR_UNCERTAIN_OR_REVIEWED",
  "validation": {"text": "UNVERIFIED", "position": "UNVERIFIED", "meaning": "NOT_ASSESSED"},
  "claim_scope": "<which_editions_were_searched>",
  "rights": {"source_license": "UNKNOWN", "permission": "UNREVIEWED"}
}
```

**Bảng đối chiếu ví dụ — không phải citation đã verified:**

| Cấp | Record đã thấy | Có thể chứng minh | Không được tuyên bố |
|---|---|---|---|
| Corpus segment Pāli | `PA_an_1:1.0.1` với `original`/SuttaCentral URL | Link khái niệm tới text segment upstream trong một repo pinned | Đây là vị trí bbox PDF của một bản in bất kỳ |
| Sanskrit metadata | `SA_GK19_Mayūra_..._1917` + bibliographical source | Tên nguồn/ấn bản mô tả do repo ghi | Toàn văn đã đối chiếu scan Quackenbos 1917 |
| Lexicon attestation | `id` + `target` + `start/end` | Khoảng ký tự trong chuỗi target do lexicon phát hành | Sense đúng, target là bản dịch có bản quyền được dùng tự do, offset trỏ PDF |
| Parallel v3 | `root_segnr/par_segnr`, `score` | Máy đã đưa một quan hệ align candidate | Đây là hai witness đồng nhất về giáo lý/lịch sử |

**Verifier bắt buộc độc lập:** nhận `(file_sha256, extraction_version, segment/offset, raw_quote)`, đọc lại raw/extracted text, so chữ và context (chữ phủ định/ngoặc/footnotes), so locator đến page image/EPUB/TEI và edition, trả text/position/meaning **ba trạng thái riêng**. Trạng thái `verified_text` chỉ khi quote khớp đúng version; `verified_position` chỉ khi mở lại được đúng raw asset/edition/locator; `meaning=NOT_ASSESSED` cho tới người duyệt. Nếu source chỉ metadata hoặc ở bên ngoài không giữ được snapshot có quyền, báo `EXTERNAL_REFERENCE_ONLY/UNVERIFIABLE`. Không suy ra trang in từ folio/segment.

## 7. Multilingual & Retrieval Behavior

| Phương thức | P41 thực sự hỗ trợ phần nào | Hành vi phải bổ sung trong BodhiAtlas |
|---|---|---|
| `EXACT` | `N/A` như chức năng core P41; `regular` search API không có bằng chứng exhaustive | Tất cả occurrence trong indexed immutable extraction, boundary/page/cột, case sensitive, query dài 200–300 ký tự, >=5 lần/file, code-only |
| `NORMALIZED` | `EXTENSION`: ByT5 segmentation, Wylie/Unicode, Chinese analyzers, stemmer, metadata fold | Tách Unicode display vs search-key, NFC, diacritic fold, Vietnamese ambiguity, OpenCC Han variant crosswalk, reversible offset map, track transformation |
| `FUZZY` | `CONFIG/EXTERNAL`: intertextuality, char/lexical/semantic similarities theo docs | Fuzzy threshold, comparison diff, negation penalty, OCR-error profiles; không dán verified badge |
| `LEXICON` | `NATIVE` tại MITRA-lexicon releases, sense/attestation counts, IDs/offsets | Duyệt nghĩa/giới hạn truyền thống, phân biệt quote/excerpts/license; chọn pack được phép |
| `SEMANTIC`/hybrid/RAG | `EXTERNAL`: MITRA Search, agent workflows, pretrained MT/embeddings | Candidate retrieval optional, không viết quote hay đổi result ID bằng LLM |

**Cụm test bắt buộc:** `anatta` / `anattā` / `anātman` / `vô ngã` / `vo nga` / `無我` phải được trả **theo phân loại quan hệ** (orthographic variant, transliteration, translation-specific term, near sense, unsupported) chứ không gộp một literal search. `無常` ↔ `无常`: normalized mode (không phải exact), và trường hợp glyph biến thể; `dukkha` / `duḥkha`: khác hệ Pāli/Sanskrit, không ép bằng nhau. Tibetan Unicode↔Wylie cần round-trip và báo trường hợp không tái tạo; `མི་` phủ định không được rơi khỏi context. Vietnamese `vo nga` có thể nhập nhằng nên chỉ là ứng viên normalized với chú giải. Với câu *“Trong các tài liệu tôi có, những tác giả nào phân biệt giữa vô thường và khổ? Họ lập luận như thế nào? Cho tôi vị trí chính xác trong sách”*: code tìm các vị trí và candidate đoạn từ `vô thường`, `khổ`, `anicca`, `dukkha`, `無常`, `苦` rồi báo đã tìm ở tác giả/edition nào; **diễn giải ai phân biệt và cách lập luận** đòi đọc ngữ cảnh/AI/người và thẩm định, không có giao thức exact nào tự chứng minh câu hỏi nghị luận.

**Specific gaps theo ngôn ngữ:**

- **Việt:** Không tìm được bằng chứng MITRA-lexicon cung cấp map Việt–Pāli/Hán/Sanskrit native; BodhiAtlas cần tự xây bảng nghĩa có người duyệt.
- **Hán:** Chinese corpus/analyzer tồn tại, nhưng `ZH_T*`, `ZH_X*` trong repo không bảo đảm tất cả bản live đã ingest; CBETA Simplified/Traditional chuyển đổi phải có offset mapping.
- **Tạng:** script Wylie rõ ở lexicon, tài liệu guide nói stemmer; full Tibetan corpus dump link hiện `UNKNOWN`, Unicode roundtrip và query coverage chưa đo.
- **Pāli:** segments Bilara/VRI và analyzed fields, nhưng MITRA-parallel **v3 không gồm Pāli**. Cấm suy diễn mọi công cụ P41 đều bao phủ cả 4 language pairs.
- **Sanskrit:** metadata/segmentation/ByT5/models; morphology/sandhi có thể giúp candidate, không tạo mặt chữ/phiên bản được xác minh.

## 8. Integration Options for BodhiAtlas

### Option A — External scholarly reference, **mặc định V1 an toàn**

**Input:** người dùng đã chọn `work/segment` hoặc tên tác phẩm; **output:** link ngoài tới web/app để **con người** tham khảo, metadata link/provenance `EXTERNAL_REFERENCE_ONLY`, không tự nạp text/nhân bản API. **Source of truth:** raw file và nguồn trong BodhiAtlas, không phải kết quả web. **IDs:** lưu `provider, external_id, accessed_at, url, link_status`, không coi external ID là file ID. **Rollback:** tắt shortcut/link khi 404/dịch vụ đổi, local citation unaffected. **Auth/privacy:** không truyền sách cá nhân hoặc user notes tới bên ngoài. **License:** quyền vào website/browse theo ToS; không gọi API để populate ứng dụng.

### Option B — Ingest static authorized artifacts, **ưu tiên cho V2**

**Input:** pinned repo commit + release asset checksum + record-level license/permission; `segments/*.json`, `metadata/*.json`, MITRA-lexicon `*.ndjson.zst`, MITRA-parallel `v3/*.ndjson.gz` khi được phép. **Adapter:** validate schema + UTF-8, unique external IDs, parse originals + analyzed separately; map upstream record to `work/edition/witness/file` **chỉ khi có chứng cứ**; provenance, imported_at, license_decision và `source_hash`. **Output:** `external_segment`, `lexicon_candidate`, `parallel_candidate` records liên kết `bodhi_source_file` sau khi source reopen thành công. **Source of truth:** imported raw asset pinned byte/hash + upstream publication; local candidate graph không thay verifier. **Migration:** schema_version, SHA pin, mappings old/new, duplicate/conflict logs; rescan diff on new import. **Rollback:** snapshot SQLite/catalog và tách candidate tables; khi license bị thu hồi, unpublish affected record và giữ audit metadata hợp lệ. **Failure:** malformed JSON, missing segment, unknown rights -> quarantine; báo `PARTIAL/UNAVAILABLE`, không âm thầm skip.

### Option C — Authorized read-only hosted API adapter, **conditional V3 / không được phép mặc định**

**Precondition:** văn bản chấp thuận cụ thể từ Dharmamitra về third-party populate, retention, rate limits, screenshots/quotes, redistribution, privacy và revocation. **Input:** `segmentnr` + collection filters, requests `matches/table` hoặc search query `primary`; **output:** ephemeral `candidate` + external `src_link`, `timestamp, query, pagination_complete, provider_version`. **Do not** persist API-derived corpus at scale nếu hợp đồng không cho phép; **do not** upload private text mặc định. **Rollbacks:** feature flag off, queue flush, cache TTL/retention theo hợp đồng, offline local engine vẫn hoạt động. **Security:** auth/key vault nếu server yêu cầu, request budget, circuit breaker, audit access, retry/backoff, response schema pin và complete pagination. **Không đồng nhất client shell script với sản phẩm backend tự host.**

**Bản hợp đồng giao tiếp nội bộ (đề xuất):**

```text
CandidateRequest { query, mode, work_scope, languages, source_permissions, requested_limit }
CandidateResult { provider, provider_version, external_segment_ids[],
                  texts_or_null, relation_type='candidate', rank_or_score,
                  corpus_scope, license_status, pagination_complete, source_links[],
                  provenance_snapshot, verification='UNVERIFIED' }
VerifiedCitation { bodhi_file_sha256, work_id, edition_id, witness_id,
                   quoted_bytes_and_text, raw_locator, verifier_log,
                   text_status, position_status, meaning_status }
```

**Portability:** mọi claims, IDs, raw-file hashes, authority tables, correction history nằm ngoài vector chunk store. Thay P41/provider/version chỉ làm mất candidates, không làm mất citation card đã kiểm hoặc local search.

## 9. Practical POC / Reproduction Plan

**Tình trạng thực tế:** **TOÀN BỘ TC01–TC06 `NOT TESTED`** về runtime/API/độ chính xác. Cuộc khảo sát chỉ **đọc** code/README/record mẫu, không chạy benchmark, không đo recall/CER/latency/cost, không tải corpus lớn và không truy cập API để populate app vì hạn chế ToS. Dưới đây là **test plan tái lập**, không phải dữ liệu kết quả. Chỉ chạy với file có quyền và môi trường tách biệt, không tự gọi hosted API khi chưa được phép.

| Test | Fixture & setup có thể tái lập | Lệnh/steps dự kiến (không phải log đã chạy) | Gold/expected output | Metric và failure gate | Kết quả |
|---|---|---|---|---|---|
| **TC01** inventory + snapshot | 11 repo ở inventory, pin SHA và schema sample `PA_an_1`, Sanskrit Quackenbos, Chinese metadata | `git clone <URL>; git -C repo checkout <SHA>; find repo -maxdepth 2 -type f`; record README/LICENSE/tag/tree; for API `UNKNOWN` | Inventory phân biệt web app, client, corpus, model, API, no-licence; mỗi record có SHA/license status | coverage inventory, number UNKNOWN; không giả tag | **NOT TESTED** (runtime); source inspection `[CODE]` |
| **TC02** source reopen SA–ZH hoặc SA–BO | 1 pair thực sau khi chọn từ `v3/sa-zh_matches.ndjson.gz`, 2 source segmented text pinned; ấn bản scan có quyền nếu có | `gzip -dc v3/sa-zh_matches.ndjson.gz | head -n 1` (pipe may emit benign broken pipe); parse `root_segnr/par_segnr`, locate source by `segmentnr`, compare raw string; open edition page via authorized URI | Gold người nghiên cứu tự ghi: hai nguyên văn, đúng ID, link edition; trang PDF nullable khi không có chứng cứ | `SOURCE_REOPEN_SUCCESS` + số bước reopen + mismatch count; no guessed page | **NOT TESTED** |
| **TC03** false semantic/cross-tradition | ≥30 gold positive + ≥30 negative: từ đồng âm, `無我`/`我`, phủ định Tạng, analogy vs quotation, translated near-sense; gold reviewed independently | Run authorized offline similarity/lexicon search on same fixtures; compare candidate ranking và expose `VERIFIED` flag; double review | False pair must stay `candidate`, no `VERIFIED` without verifier and human; context displays negation | `FALSE_VERIFIED_CITATION` target **0**, P@k/R@k measured later, disagreement reviewed | **NOT TESTED** |
| **TC04** API/export + citation adapter | Local *recorded/stub responses* modeled after `examples/nexus-matches.json`, `PA_an_1.json`, plus license grant before any real calls | `python adapter.py --fixture fixtures/authorized.json`; **only with written grant:** `./scripts/nexus.sh matches --file ...` / `table ... --all` | Candidate card contains upstream IDs, src_link, score type, `EXTERNAL/UNVERIFIED`, rights; pagination complete | schema validation, failed pages, missing rights; response without source hash not verified | **NOT TESTED** |
| **TC05** missing source/revision/OCR scope | Local 3 docs: one fully indexed text, one missing page, one source changed SHA, one corrupt OCR character; two editions of same work | Rebuild index manifest, simulate source deletion/tamper; compare checksum, query missing term; re-open stale citation | `SOURCE_UNAVAILABLE`/`PARTIAL`, excludes unverifiable claims, unchanged source stays searchable; no false global absence | `ERROR_COVERAGE` + `SOURCE_REOPEN_SUCCESS`; gate fail on silent omission | **NOT TESTED** |
| **TC06** options trade comparison | 1 shared authorized text; (A) external scholarly link, (B) static dataset import; privacy test with private file never leaves local | Execute both workflows, log outbound requests (must be none for option B); export JSON IDs and restore snapshot | External-only shows link not claim; local artifact reopens raw source if same edition; rollback retains local exact | permission compliance, restore success, id drift, cost of integration | **NOT TESTED** |
| **TC07** Unicode + exact regression | Synthetic 2-page, 2-column, 5 repeats of 250-character quotation; `anatta/anattā/anātman`, `vô ngã/vo nga`, `無常/无常`, Unicode Tạng/Wylie, mixed line breaks | Local `pytest tests/test_exact_unicode.py`; run exact scan on immutable extraction, run transform-aware variants separately | `EXACT` 5/5 offsets for literal text and zero nonliteral; normalized hits explain transform; no page guessed | `EXACT_FULL_RECALL=5/5` required **as acceptance target**, not measured result; 0 duplicate/missing offsets | **NOT TESTED** |
| **TC08** licensed lexicon offline and upstream alignment | Download release *legally* from lexicon v1.1, verify `SHA256SUMS.txt`; sample 10 headwords and 10 ambiguous senses; choose `sa-en-by-sa` subset if license fits | `sha256sum -c SHA256SUMS.txt` after pulling correct assets; `zstd -d --long=27 FILE.zst`; parse `senses[].ex[].start/end` | Every excerpt offset roundtrips against `target`; source ID resolves or marked unresolved; all licenses recorded | offset success, unresolvable ID rate, human sense precision; unsupported `unknown` state not silently dropped | **NOT TESTED** |

**Acceptance measurement definitions:**

- `EXACT_FULL_RECALL`: (# manually gold occurrences returned at exact raw offsets) / (# gold occurrences in **indexed/accessible** scope), including duplicates/long excerpts; target 1.0 on deterministic fixture, **chưa đo**.
- `FALSE_VERIFIED_CITATION`: count machine-derived or incorrect-page quotes labeled `TEXT_AND_LOCATOR_VERIFIED` without source check; acceptance **0 on gold**, **chưa đo**.
- `SOURCE_REOPEN_SUCCESS`: count verified citations whose immutable input+locator reopen and byte/text checks succeed / audited citations; **chưa đo**.
- `P@k/R@k`: same-language and cross-language **candidate** recall vs human gold; not citation precision. `CER/WER` only for OCR on ground-truth page images, no valid number from these repo samples. `QUALITY_COVERAGE`: files/pages present, skipped, corrupt, OCR-uncertain; `FTS_index_latency` and `integration_person-days` measured only after POC on specified machine/volume.

**Gợi ý fixture manifest:** `fixtures/manifest.json` gồm `fixture_id`, `source_sha256`, `edition_id`, `query`, `expected_occurrences[{start,end,page_or_null}]`, `expected_candidate_relation`, `gold_reviewer`, `license`, `scope`, `negative_reason`. `gold` không là output của model. Lệnh thiết lập demo cấp repo chỉ mang tính kế hoạch; không sinh ra log giả.

## 10. Deployment, Security, Legal, Cost

**Hệ thống/phụ thuộc:** (1) corpora JSON/NDJSON có thể xử lý offline sau khi pin file/checksum và được quyền; (2) `mitra-bo-zh-tagger` yêu cầu Python >=3.10, PyTorch >=2.2, Transformers >=4.57, pyewts, accelerate; model 9B bfloat16 tài liệu nêu khoảng 18 GB weights, GPU khoảng 19 GB VRAM (Apple Silicon unified memory >=24 GB; đó là ước lượng tác giả, **không** phải test tại đây); (3) ByT5 Sanskrit inference/weights riêng; (4) MITRA-lexicon tái tạo full đòi vLLM, CUDA/HF checkpoints, teacher model API, external training framework và một số corpus/từ điển chưa phân phối; bản artifact static tiết kiệm phức tạp hơn nhiều; (5) hosted Dharmamitra API phụ thuộc network, ToS, upstream service và có thể có quota không công bố.

**Bảng quyền tách lớp:**

| Đối tượng | Quyền/bằng chứng đã thấy | Quyết định an toàn trước permission review |
|---|---|---|
| Lexicon `code/` | MIT, `LICENSE.md` | Có thể đọc/điều chỉnh code giữ notices; không kéo theo quyền corpus |
| Lexicon `sa-en` full và gold/teacher | CC BY-NC-ND 4.0 | Không hợp pháp mặc định cho thương mại/derivative redistribution; hỏi pháp lý |
| Lexicon `sa-en-by-sa`, `sa-bo`, `sa-zh`, `zh-bo` | CC BY-SA 4.0 theo repo v1.1 | Tôn trọng share-alike/attribution, rights source sentences, chọn packaging mode |
| Prosopography Sanskrit | CC BY-NC-SA 4.0 + draft machine-generated | Chỉ internal review/NC use hợp lệ; không nhập dữ kiện như historical truth |
| Pāli segmented corpus | README ghi original PD nhưng file giới hạn non-commercial và attribution VRI | Giữ separate legal fields, xét trước import/publish |
| Chinese corpus / AI summaries | CBETA/Kanripo upstream, Ask Bunkankun summary CC BY-SA | Per-text source licenses/edition; không cấp phép toàn Chinese repo theo suy đoán |
| MITRA-parallel v3 | Mô tả dataset và guide dùng CC BY-SA nhưng **v3 root/README chưa cấp đầy đủ cho từng source** | `UNKNOWN` theo từng record/redistribution cho đến license manifest được xác nhận |
| BO/ZH tagger | package code MIT; weights tải từ HF | Check **exact model revision/card** và downstream derivative rights riêng |
| Hosted API/DharmaNexus DB | ToS chính thức cấm populate third-party | **Không tích hợp/populate** trước khi được Dharmamitra cấp quyền văn bản |
| Private scans, PDFs, unpublished translations | Quyền thuộc chủ sở hữu, không suy từ repo | `LOCAL_ONLY` mặc định; cloud/AI opt-in granular; không gửi tới tools ngoài |

**Bảo mật tối thiểu:** private/public input separation; permission matrix `LOCAL_ONLY/EXTERNAL_API_ALLOWED/GENAI_ALLOWED`; read-only connector, allowlisted hosts, no automatic mass scraping; log provider URL/method without secret text; redaction; retries with budgets; no unlimited agent actions; immutable backup + SHA manifest; restore dry run; source license purge on revocation; export vendor-neutral JSON/SQLite; audit record of scholar corrections. API auth “không cần key” theo agent README **không có nghĩa** API được tích hợp hay có authorization model cho dữ liệu cá nhân.

**Chi phí — assumptions, không phải đo:** static import tiêu thụ disk cho corpus + indices + backup (chi phí tăng theo bytes thực tế); local 9B tagger cần GPU/memory như tác giả báo; rebuild full lexicon có GPU/API teacher rất đáng kể và path dependencies; hosted API có rủi ro giá/limit/điều khoản đổi, không đủ chứng cứ để định lượng. `COST=UNKNOWN` đến khi chọn dataset subset, đo size, request counts, hardware, và số công duyệt. Đừng tạo bảng USD/tháng bịa đặt.

## 11. Comparison & Trade-offs

So sánh **cùng vai trò** trước, không dùng stars và không ép corpus thành search engine. `N/A` khi ngoài trách nhiệm sản phẩm. `BuddhismDocuments-for-AI` là tài sản của BodhiAtlas, không là đối thủ cùng phạm vi web.

| Lớp và ứng viên | Mạnh ở đâu / bằng chứng | Yếu ở đâu đối với V1 Core | Quyết định |
|---|---|---|---|
| **Dharmamitra/DharmaNexus** ecosystem | Đa ngôn ngữ, intertextuality, segmented texts, lexicon có attestation và model NLP; có repository artifacts và client API | Không biết whole server/self-host, third-party API ToS, thiếu book-to-PDF source map, exact exhaustive không chứng minh | **COMPONENT** chỉ artifact/licensed data, external links |
| **BuddhaNexus legacy** | Hệ tiền nhiệm intertextuality, thích hợp khảo cứu lịch sử thuật toán/đối chiếu | Không dùng mặc định như live backend; migration ID/DB chưa xác minh; code cũ không tự tạo rights | Historical/legacy only; kiểm redirect nếu cần |
| **FoJin** (platform/search) | Repository giới thiệu một stack end-to-end gồm FastAPI/Postgres/Elasticsearch/vector, giao diện tra cứu corpus | Claims README cần kiểm code, benchmark và legal; không mặc định đáp ứng local immutable proof/EPUB locator/exact | Alternative **TRIAL ONLY**, so P41 không là cùng lớp engine |
| **SuttaCentral Bilara** (primary corpus/segments) | Segments JSON/root/translation/notes và URL có ID ổn định là nguồn upstream phù hợp | Không phải OCR sách tùy ý, không bảo đảm tự động map tới các ấn bản người dùng | **Preferred upstream** khi có quyền, crosswalk `SuttaCentral_ID` |
| **BuddhismDocuments-for-AI** (tài sản hiện có) | Repo báo pin 13 upstream; local SQLite FTS, search/context/provenance/evidence/Quick; có luật kiểm chứng | Chưa tự khẳng định full V1 PDF/EPUB/OCR, Windows toàn suite và Research semantic approvals; số test do repo tự công bố | **Reuse existing local base**, P41 chỉ bổ sung sau gate |

**Tradeoffs:** P41 lợi về học thuật liên truyền thống và candidate/lexicon; SuttaCentral/Bilara mạnh ở provenance primary segments; FoJin là nền tảng ứng dụng cần kiểm thực tế; tài sản sẵn có phù hợp việc quản lý pins/source. **Không có lựa chọn một sản phẩm bao trùm cả nguồn, engine exact và verified citation** từ bằng chứng đang có.

## 12. Decision Record for Master Synthesis

**Bảng chuẩn giữ nguyên field names:**

| Field | Value | Evidence/assumption |
|---|---|---|
| TARGET | Dharmamitra / DharmaNexus ecosystem | P41-E04/E07, inventory |
| CLASS | ecosystem | Nhiều loại repo, service, model, corpus; không một platform OSS đồng nhất |
| DATE / VERSION / COMMIT | 2026-11-16; UI `v1.51.1-2-g91d74bff`; repo pinned SHA tại §2 | UI version không phải backend commit |
| PRIMARY_ROLE | Multilingual scholarly corpus reference + intertextuality/lexicon candidate provider | P41-E04/E05/E16/E17 |
| BEST_FIT_V1_CORE | partial | Hữu ích cho crosswalk/candidate; không thay exact/ingest/source verifier |
| SOURCE_FIDELITY_GATE | unknown | Một số segment IDs/URLs có, không chứng minh source reopen PDF/bbox của BodhiAtlas |
| CODE_ONLY_EXACT_GATE | n/a | P41 không đảm nhiệm exhaustive exact Core; tự xây local engine |
| MULTILINGUAL_GATE | unknown | Đa ngôn ngữ theo docs; bộ gold Việt/Hán/Tạng/Pāli/Sanskrit chưa thực đo |
| OCR_COVERAGE_GATE | n/a | Corpus/lexicon không có vai trò OCR; hosted OCR riêng chưa source-map POC |
| RIGHTS_SECURITY_GATE | unknown | API ToS chặn third-party populate, licensing theo từng pack; quyền cụ thể chưa quyết |
| INTEGRATION_COST | high | Crosswalk rights/edition/source map/verifier, chưa đo person-days |
| MAINTENANCE_RISK | high | Hosted API/version/rights/data heterogeneity; dependency offline pipeline |
| RECOMMENDATION | COMPONENT | `USE AS COMPONENT` theo §1, cấp quyền từng artifact, no unauthorized API |
| CONFIDENCE | medium | Cao với tồn tại source/docs, thấp ở runtime/full corpus legal+accuracy |
| NEXT_POC | TC02+TC03+TC05 offline corpus/citation gates; TC08 licensed lexicon; API chỉ sau grant | Bộ gold độc lập, nguồn gốc pinned, log + rollback theo §9 |

**5 findings trọng yếu:**
1. DharmaNexus và MITRA Search là hai vai trò tách: DB/intertextuality vs search candidate (`[DOC]` E05).
2. Static corpora Sanskrit/Pāli/Chinese có segment và metadata thật; không là byte-identical file thư viện BodhiAtlas (`[CODE]` E09/E11/E14).
3. MITRA-parallel v3 mới hơn v2, có 3 cặp xuyên ngôn ngữ và không gồm Pāli (`[DOC]` E15/E16).
4. MITRA-lexicon có dữ liệu nghĩa/dẫn chứng/offset hữu ích nhưng quality và rights inherited không thể bỏ (`[DOC/CODE]` E17–E20).
5. Clause ToS chính thức chặn third-party API populate dù agent công khai endpoint (`[DOC]` E06 và `[CODE]` E21).

**5 blockers:** (B1) API authorization; (B2) unknown complete edition-to-file-bbox source mapping; (B3) uneven attribution/license/derivatives, especially full sa-en, Pāli and prosopography; (B4) no independent gold/negative OCR/language benchmark; (B5) backend self-host and Tibetan full data dump not proven.

**5 experiments ưu tiên:** (X1) licensed source ID→raw reopened citation 2 pairs; (X2) error/negative cases with explicit no-verified flag; (X3) Vietnamese–Han–Tibetan–Pāli–Sanskrit normalization+5 occurrences; (X4) import one CC BY-SA compatible lexicon pack with checksums/provenance; (X5) update/missing-source/restore test + paging/filter validation **chỉ dùng offline stub hoặc API grant**.

**3 quyết định chờ chủ dự án:** (D1) BodhiAtlas có định hướng sử dụng dữ liệu bên ngoài trong public/commercial product không (để xác định legal mode và NC/SA derivatives)? (D2) có liên hệ Dharmamitra xin cấp quyền cụ thể cho API/retention/reuse hay chỉ dùng external scholarly link? (D3) phạm vi V1 đối chiếu liên ngữ: chỉ nhập upstream được phép, hay cần bilingual lexicon/datasets ngay (đổi chi phí POC và ưu tiên)?

**Tóm tắt hành động:** kế thừa artifacts có kiểm quyền + thuật toán phân đoạn/word-alignment hỗ trợ; tự xây những thứ mang tính bất biến học thuật của BodhiAtlas: registry work/edition/witness, file checksum, OCR/parser/source map, exhaustive exact search, multilingual normalized/fuzzy code-only, coverage manifest, rights ACL, independent citation verifier, claim/reviewer workflow; trước quyết định triển khai cần POC và giấy phép thật.

## 13. Appendix

### A. Nguồn chính thức và đường dẫn cố định

- BodhiAtlas PRD V1.4: https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/PRD.md (`blob SHA 58d967c642d625180c436e1a6e6a75fa2e7070e3`).
- BodhiAtlas risk and verification: https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/ACADEMIC_RISKS_AND_VERIFICATION.md (`blob SHA cdb642633f3dc3f7f83cb0e49a96abfebc9f132e`).
- Existing corpus research: https://github.com/quoctran-2608/BuddhismDocuments-for-AI (README pinned blob SHA ở E03).
- Official ecosystem site and guide: https://dharmamitra.org/ ; https://dharmamitra.org/db ; https://dharmamitra.github.io/dharmamitra-guides/dharmanexus/ ; https://dharmamitra.github.io/dharmamitra-guides/ .
- Sanskrit corpus: https://github.com/dharmamitra/dharmanexus-sanskrit/tree/aec80af58c2bbd18477553f350bf067ed7807ea7 .
- Pāli corpus: https://github.com/dharmamitra/dharmanexus-pali/tree/74e0f1a70476cfa7c45e5ca1335ac3ed0d5c1fe8 .
- Chinese corpus: https://github.com/dharmamitra/dharmanexus-chinese/tree/aa362ea779a9238260cdd84a8f1d6384e8407437 .
- MITRA-parallel v3: https://github.com/dharmamitra/mitra-parallel/tree/0a770d98283b826134da0d8ec4d75259350faaa0/v3 .
- MITRA-lexicon v1.1: https://github.com/dharmamitra/dharmamitra-lexicon/tree/f61c572930cca49fe7654ffda1555c3937e5bf3a ; release https://github.com/dharmamitra/dharmamitra-lexicon/releases/tag/v1.1 .
- BO/ZH tagger: https://github.com/dharmamitra/mitra-bo-zh-tagger/tree/b678dbe73c3113021aedf164b04cb94eb6b54f84 ; model https://huggingface.co/buddhist-nlp/mitra-bo-zh-tagger .
- ByT5 Sanskrit: https://github.com/dharmamitra/byt5-sanskrit-analyzers/tree/3f25e158e862b029d6cd7bd20653f903c466635f ; https://huggingface.co/buddhist-nlp/byt5-sanskrit .
- Agent API client: https://github.com/dharmamitra/dharmamitra-claude-code-agent/tree/63a39fe679575751a7a95358801257ba2fb92726 .
- Legacy and comparators: https://github.com/BuddhaNexus ; https://github.com/xr843/fojin ; https://github.com/suttacentral/bilara-data ; https://github.com/quoctran-2608/BuddhismDocuments-for-AI .

### B. File paths và lệnh điều tra tái lập (không phải lệnh đã chạy)

```bash
# Snapshot: thay mỗi URL/SHA theo inventory; không dùng HEAD trôi nổi cho nghiên cứu.
git clone https://github.com/dharmamitra/mitra-parallel.git
git -C mitra-parallel checkout 0a770d98283b826134da0d8ec4d75259350faaa0
sed -n '1,100p' mitra-parallel/v3/README.md

# Chỉ nếu rights/size cho phép:
# gzip -dc mitra-parallel/v3/sa-zh_matches.ndjson.gz | head -n 1

# Static lexicon: verify sum trên toàn bộ release asset tương ứng.
# sha256sum -c SHA256SUMS.txt
# zstd -d --long=27 mitra-lexicon-sa-bo.sa2bo.ndjson.zst

# Không gọi /api-db hay /api-search để populate BodhiAtlas khi chưa có quyền.
# Agent clients for contract reading only: scripts/nexus.sh, scripts/primary-search.sh
```

**Files lõi đã đọc:** `dharmanexus-sanskrit/{README.md,convert_to_json.py,metadata/SA_GK19_Mayūra_Sūryaśataka_Quackenbos_1917-metadata.json,prosopography/README.md}`; `dharmanexus-pali/{README.md,segments/PA_an_1.json,metadata/PA_an_1-metadata.json}`; `dharmanexus-chinese/README.md`; `mitra-parallel/{README.md,v2/README.md,v3/README.md}`; `dharmamitra-lexicon/{README.md,LICENSE.md,code/README.md,code/pipeline/4-mining/mine_direction.py,code/pipeline/5-build/{tib_norm.py,build_sabo_bidict.py}}`; `dharmamitra-claude-code-agent/{README.md,scripts/{nexus.sh,primary-search.sh,build-corpus-index.py},examples/{nexus-matches.json,primary-search-regular.json}}`; `mitra-bo-zh-tagger/{README.md,pyproject.toml}`; `byt5-sanskrit-analyzers/README.md`; `mitra-parallel-html/{README.md,build.py}`. Đã xem repo trees và một số issue/PR, không có clone repo/full tests/benchmark.

### C. Thiếu quyền tiếp cận / chưa xác minh và ảnh hưởng

1. **Đọc được** PRD V1.4 và `ACADEMIC_RISKS_AND_VERIFICATION.md` qua GitHub connector; có thể truy cập đủ yêu cầu để đối chiếu, không phải tự suy diễn.
2. **Chưa được phép/không thử** hosted APIs, authenticated/admin endpoints, quota/rate-limit, request data thực và OpenAI/Claude/Gemini translation cost. Agent public endpoint docs không thay ToS.
3. **Chưa có** kiểm kê full rights/manifest của mọi bản dịch, ảnh trang, Pāli VRI packaged data, Chinese CBETA, Sanskrit upstream, model weights revisions. Cần license ledger per record.
4. **Tibetan corpora:** guide trỏ repo nhưng lượt mở không cho source/Tibetan corpus hoàn chỉnh; ghi `UNKNOWN`, không gán repo SHA giả hoặc kết luận repo đã xóa.
5. **Server source & data dump all services:** không xác minh. Không khẳng định có source hoặc app độc lập deploy.
6. **Current MITRA-parallel:** dùng v3 từ GitHub head 2026-10-16, phân biệt v2/v1; những crawler còn hiển thị v2 là nguồn cũ, không dùng để xác định newest.
7. **No TESTED claims:** không chạy real-life exact/fuzzy/multilingual/latency/source-reopen, không có gold chuyên gia hoặc OCR page images; số tự công bố của dự án được giữ nhãn `[DOC]`.
8. **Tính thời gian:** snapshot tại 2026-11-16; tên endpoint/corpus và giấy phép phải đối chiếu lại trước khi đưa vào hợp đồng hoặc sản phẩm public.

**Kết luận cuối:** Dharmamitra/DharmaNexus có giá trị rõ trong **tham khảo liên văn bản và khai thác dữ liệu từ vựng/ngôn ngữ**, nhưng không chứng minh có thể kế thừa nguyên khối làm hệ thống thư viện kiểm chứng trích dẫn của BodhiAtlas. Quyết định an toàn là **component chọn lọc, có quyền sử dụng và verifier độc lập**, đồng thời giữ local code-only search và provenance làm nguồn thẩm quyền V1.
