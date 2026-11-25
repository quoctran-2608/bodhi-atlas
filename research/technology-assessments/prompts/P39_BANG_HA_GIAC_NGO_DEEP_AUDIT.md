# P39-R2 — PROMPT NGHIÊN CỨU ĐỘC LẬP TOÀN DIỆN: `Bang-ha-giac-ngo` → BodhiAtlas V1 Core

**Loại tài liệu:** Prompt giao việc cho một AI/chat nghiên cứu kỹ thuật độc lập. **Không phải báo cáo thẩm định, không phải kết luận đã chạy POC.**

**Đầu ra bắt buộc:** một file Markdown duy nhất mang tên `REPORT_39_BANG_HA_GIAC_NGO_INDEPENDENT_REVIEW.md` (không ghi đè báo cáo P39 cũ); nội dung tiếng Việt, 13 mục như chỉ định bên dưới, Evidence Ledger có permalink commit/dòng, Fit–Gap C01–C15, ít nhất 18 test case/POC có điều kiện và quyết định kiến trúc có khả năng bị bác bỏ bằng thực nghiệm.

**Mục đích cuối cùng:** quyết định khách quan, tiết kiệm công sức và token AI nhất cho BodhiAtlas: (A) chọn Bang-ha framework làm lõi, (B) chọn BCR làm lõi, (C) tự xây **lõi chứng cứ tối thiểu** rồi kế thừa, (D) chọn `book-memex` làm lõi, (E) lấy nền tảng nghiên cứu/AI hiện hữu làm lõi, hoặc (F) chỉ dùng Bang-ha như corpus/connector/component. Có thể đề xuất phương án G nếu chứng minh tốt hơn. **Không mặc định bất kỳ phương án nào thắng**, kể cả ý tưởng LEGO/plugin hay Minimal Core mà các nghiên cứu trước đang ưu tiên.

---

## 0. VAI TRÒ, ĐẦU VÀO VÀ QUY TẮC NGHIÊN CỨU

Bạn là hội đồng thẩm định kỹ thuật độc lập trong một AI: kiến trúc sư hệ thống, kỹ sư tìm kiếm, chuyên gia preservation/provenance, kiểm thử phần mềm, an ninh/giấy phép, và người phản biện chi phí vận hành. Không đóng vai quảng bá repo. Nhiệm vụ là **tìm phương án ít phức tạp nhất thỏa các điều kiện nghiệm thu học thuật**, không phải chọn repo nhiều tính năng nhất.

### Các nguồn bắt buộc phải trực tiếp đọc

1. **Repository chính để thẩm định:** `https://github.com/quoctran-2608/Bang-ha-giac-ngo` và bản đối chiếu/đường dẫn được chủ dự án cung cấp `https://github.com/quocgempro361/Bang-ha-giac-ngo`. Có thể cả hai **private**. Kiểm qua kết nối GitHub được ủy quyền, `get_repo`, cây Git và các file thực; **404 khi không có quyền không chứng minh repo không tồn tại**. Xác nhận hai repo giống/khác nhau theo SHA commit hoặc hash Git blob; không mặc nhiên coi chúng là hai mirror đồng nhất chỉ vì cùng tên hoặc README.
2. **Tài liệu yêu cầu bắt buộc:** `https://github.com/quoctran-2608/bodhi-atlas/blob/main/docs/PRD.md` (V1.4), `docs/V1_CORE_FOUNDATION.md`, `docs/ACADEMIC_RISKS_AND_VERIFICATION.md`. Dùng đúng nội dung được mở trực tiếp ở SHA ghim. PRD và G1–G6 là tiêu chuẩn đánh giá, **không tự hạ tiêu chuẩn để giúp repo qua cửa**.
3. **Báo cáo đã có:** `https://github.com/quoctran-2608/bodhi-atlas/blob/main/research/technology-assessments/REPORT_39_BANG_HA_GIAC_NGO.md`. Đọc để biết *giả thuyết, manh mối, rủi ro* của P39, nhưng **không dùng kết luận P39 làm kết luận của bạn**. Kiểm mã nguồn độc lập; ghi nếu khác vì repo đổi commit.
4. **Đối chứng khi cần:** `BuddhismDocuments-for-AI` (P03), `book-memex` (P57), `Open Notebook` (P56), Docling (P12), SQLite FTS5 (P20), và mã nguồn thực của các repo tương ứng nếu đánh giá lợi thế cạnh tranh. Các báo cáo đối chứng là tư liệu tham khảo, không phải bằng chứng POC đã chạy trong nghiên cứu này.
5. **Upstream corpus nếu cần thiết và hợp pháp:** SuttaCentral Bilara, CBETA, TEI, OpenPecha, 84000/BDRC tùy xuất xứ từng dữ liệu. Xác nhận provenance và quyền **theo nguồn/ấn bản**; không suy rằng mọi bản dịch Việt được phép tái phát hành.

**Quy tắc nếu không được truy cập:** Nếu GitHub connector không có quyền vào repo private, báo `ACCESS_BLOCKED`, liệt kê chính xác nguồn/đường dẫn cần truy cập và yêu cầu bản ZIP hoặc quyền được cấp. Chỉ phân tích phần có thể truy cập; **không bịa kết quả từ README, báo cáo cũ hoặc trí nhớ**. Nếu dữ liệu sản xuất trên ổ `D:/E:` không được cung cấp thì đánh dấu `UNAVAILABLE`, không suy đoán rằng build có thể tái lập.

**Về reproducibility:** Ghim SHA của các repo và phiên bản phụ thuộc, tách `main HEAD` khỏi bản release/tag/branch; lưu mã, dòng, log kiểm thử, môi trường, tập fixture, script và config **không chứa secrets/đoạn dài có bản quyền**. Phân biệt `[CODE]` đã đọc code, `[DOC]` tài liệu, `[TESTED]` tự chạy upstream, `[TESTED-ISOLATED]` tự tái tạo thuật toán/schema không chạy upstream, `[ISSUE]` báo cáo sự cố, `[PLAN]` roadmap, `[INFERRED]` suy luận từ code và `[UNKNOWN]` chưa đủ bằng chứng. `TESTED` chỉ có khi nêu lệnh, đầu vào, phiên bản, kết quả, log và tái hiện được. Ghi mức `HIGH/MED/LOW` theo độ tin cậy bằng chứng. **Không nhầm file count với số kinh độc lập, hay code có mặt với production đã nghiệm thu.**

**Bảo vệ dữ liệu:** Repo có thể private, chứa dữ liệu dịch thuật có quyền. Không đăng nội dung gốc ra public gist/CI, không upload corpus lên dịch vụ AI/OCR bên ngoài, không công bố mật khẩu/đường dẫn nội bộ. Dùng fixture tự tạo có quyền hợp lệ. Mọi thay đổi code, DB, thư mục nguồn chỉ trong sandbox/snapshot có quyền, không chạy build/repair trên chỉ mục sản xuất. Nếu license mã nguồn chưa rõ thì không tự chép code qua repo khác; đánh giá điều kiện cần trước.

---

## 1. CÁC CÂU HỎI QUYẾT ĐỊNH CẦN TRẢ LỜI

Bạn bắt buộc trả lời rõ, có phản chứng cho từng câu:

1. `Bang-ha-giac-ngo` thực chất là **kho dữ liệu**, **corpus framework**, **sản phẩm tra cứu**, hay **nền tảng chứng cứ học thuật hoàn chỉnh**? Phân lớp rõ, đừng đánh đồng corpus nhiều với phần mềm production tốt.
2. Có thể lấy nguyên `tools/local_corpus_framework` làm **BodhiAtlas V1 Core** không? Bao nhiêu thành phần cần thay vì nhu cầu sách cá nhân PDF/EPUB/DOCX, nguồn bất biến, ấn bản và Citation Checker?
3. Nếu lấy Bang-ha-led, có phải duy trì các phụ thuộc dữ liệu ngoài Git `D:/E:` hay có thể **clean clone → build** bằng corpus và manifest có quyền? Có portable config, staging, restore?
4. `sources/passages/translations` có đúng **Work–Expression–Edition–Witness–SourceFile–ExtractionRevision–SourceSpan** hay chỉ có vài cột gần giống? Khi đổi bản dịch/ấn bản/reparse, dẫn chứng cũ có bị trỏ sai?
5. `EXACT` có **liệt kê đầy đủ mọi occurrence + offsets** trên phạm vi đã xử lý, kể cả đoạn lặp và câu vượt ranh giới record không, hay chỉ trả record/page được tìm thấy?
6. Bilara JSON pointer, TEI XPath/page marker, Hán HTML anchor và EPUB/DOCX xuất bản có định vị thực sự mở lại đúng **từng câu** trong đúng version không? CFI PDF page/bbox có hay không?
7. **Sổ cái Claim–Evidence–Contradiction** có fail-closed đúng G2/G3 không? Các nhãn `VERIFIED`, `SUPPORTED`, `T1` do đâu sinh, có cấp tự động sai không? Đây là bài kiểm tra hard gate.
8. Source provenance, permission, source URL và quyền tác giả/dịch giả có đủ để dùng trên cloud, xuất bản hoặc chia sẻ không? Private repo **không** đồng nghĩa có quyền tái phân phối.
9. Có thể tái dùng an toàn **module nhỏ** nào thay vì fork cả repo: parser, schema pattern, publishing/rollback, bộ tra cứu, UI, resolver, ontology, indexer, QA?
10. Nếu buộc chọn một phương án làm nền mã chủ đạo, **Bang-ha-led vs BCR-led vs Minimal Core vs book-memex-led**, phương án nào giảm *tổng* số module sửa, dữ liệu nhân bản, số dịch vụ, token AI, chi phí nâng cấp và khả năng sai dẫn chứng? Nêu **bằng chứng hoặc giả định** cho chi phí, không phát minh nhân-ngày/LOC.
11. Có cần plugin framework tổng quát hay chỉ `Ports & Adapters` theo 2–3 hợp đồng hẹp? Việc phát hành/rebuild và source verifier có cần “plugin” hay nên ở core bất biến?
12. **Điều kiện cụ thể nào khiến bạn đảo ngược kết luận ban đầu?** Đặt tiêu chí falsifiable trước khi xếp hạng.

---

## 2. CÁC VỊ TRÍ MÃ NGUỒN PHẢI ƯU TIÊN ĐỌC

Đọc trực tiếp *tối thiểu 25–35 file thực sự có trong tree* bao gồm ít nhất 8 file Python core, 4 file test/incident/QA, 3 file nguồn mẫu và 3 file định hướng/quyền. Dưới đây là **candidate paths đã xuất hiện ở snapshot cũ**, phải kiểm tồn tại tại SHA mới trước khi dùng, không tự tuyên bố chưa từng thay đổi:

### Core data, adapter, retrieval, QA, publication

- `tools/local_corpus_framework/README.md`, `SPEC.md`, `local-framework-reference.md`.
- `tools/local_corpus_framework/corpus/common.py`: schema, hash, normalized text, source registry, phiên bản, đường file.
- `tools/local_corpus_framework/corpus/adapters.py`: parse Bilara, HTML/TEI, nguồn khác, locator/line/xpath và xử lý lỗi.
- `tools/local_corpus_framework/corpus/build.py`: ingest, manifest, QA, coverage, errors, transaction, file idempotence.
- `tools/local_corpus_framework/corpus/cli.py`: search, federated search, get passage/source/context/citation, pagination, FTS, EXACT.
- `tools/local_corpus_framework/corpus/publication.py`: staging, activation, snapshot, checksums, rollback.
- `tools/local_corpus_framework/corpus/ontology.py`, `ontology.json`, `build_parallels.py`: thuật ngữ song ngữ và kinh song hành; phân biệt rule-based expansion vs verified scholarship.
- `tools/local_corpus_framework/index_corpus.py`, `manage_index.py`, `publish_mvp.py`, `test_framework.py`, `validate_contribution.py`.
- `tools/local_corpus_framework/build_vietnamese_canon.py`, `build_cbeta_fts.py`, `build_tibetan.py` (và build script khác nếu thuộc luồng sản xuất).

### Giao diện, MCP, sổ cái học thuật, an ninh

- `tools/local_corpus_ui/server.py`, `static/app.js`, `static/index.html`, `test_ui.py`, `TEST_REPORT.md`.
- `tools/scholarly_ledger.py`, `tools/test_scholarly_ledger.py`, kiểm `ledgers/scholarly_ledgers.sqlite` **chỉ trong bản copy, không ghi vào nguồn**.
- `tools/ebt_mcp_server.py`, `tools/generate_multiview_app.py` và các đường HTTP/Parquet/MCP/cloud nếu thật sự liên quan.
- `docs/ROADMAP_2.0_OPEN_HERITAGE_CORPUS.md`, `docs/SPECIFICATION_2.0_OPEN_HERITAGE_CORPUS.md`, `docs/TIEN_DO_DU_AN.md`.
- `incidents/2026-09-24-source-quarantine.json`, `incidents/2026-09-24-phase-4-claim-correction.md`, `incidents/2026-09-24-safe-index-publication.md`, `incidents/2026-09-25-judaism-build-oom-storage-incident.md`, `docs/incidents/*`.

### Corpus và sản phẩm đọc (mẫu bắt buộc)

- Bilara Pāli JSON: kiểm file có thật trong `01_NIKAYA/MN_Trung-Bo/pli_root/` hoặc thư mục tương đương; ví dụ ở P39 là `mn1_root-pli-ms.json`, và định danh câu như `mn1:1.1`.
- Việt HTML: `01_NIKAYA/MN_Trung-Bo/vi/mn1.html` (kiểm anchor và văn bản thực), ít nhất một nguồn `SN`/`AN` khác.
- Hán Āgama: `02_AGAMA/DA_Truong-A-ham/lzh_root/da1.html` và bản Việt `vi/da1.html`; đối chiếu page/line anchor, dịch giả và link nguyên văn.
- Vinaya: ít nhất một source `03_VINAYA_LUAT-TANG/*` và đối chứng chú thích/biên giới đoạn.
- TEI/CBETA hoặc XML source nếu nằm trong snapshot và quyền cho phép; nếu file lớn bị chặn đọc, ghi rõ không kiểm nội dung, chỉ tree không đủ.
- `SACH_DOC_NGUOI_DUNG/`: ít nhất một EPUB và một DOCX xuất từ corpus, đối chiếu chúng với nguồn upstream. **Đừng coi sách được xuất ra là chứng nhân văn bản độc lập hoặc locator học thuật đã được kiểm.**

### Bản quyền và vận hành

- README phần provenance/license, `.gitignore` / manifest / source-registry, đối chiếu xem có top-level LICENSE hay không, phân tích license cho code, dữ liệu Pāli, Hán, bản dịch Việt, file EPUB/DOCX phát sinh, dịch vụ cloud, model/OCR.
- Xác minh tài liệu chỉ có trên `D:/E:` bằng cách liệt kê dependency/hướng khôi phục; nếu không được cung cấp thì **không khẳng định có thể tái tạo production index**.

### Đọc đối chứng (có ghim commit, không copy kết luận)

- `BuddhismDocuments-for-AI`: `tools/corpus_research/verification.py`, `source_resolvers.py`, `retrieval.py`, schema và tests; kiểm khả năng tái dùng trực tiếp `source_reader`/evidence gate thay vì viết mới.
- `book-memex`: `db/models.py`, `services/import_service.py`, search/reader; xem nó có *thật sự* tốt hơn cho personal PDF/EPUB không.
- `Open Notebook`: `content-core` chỉ là parser wrapper, không ngầm có source locator/citation; xem nhu cầu workspace V2, không cộng điểm UI/RAG vào G2.

**Sau khi đọc:** đính bảng inventory tất cả file đã mở, SHA, path, chức năng, và **điều chưa kiểm**. Nếu một file không tồn tại thì chứng minh bằng tree/API, không giả vờ đã đọc. Kiểm README claim với *effective code path*, tránh đưa kế hoạch roadmap thành tính năng hiện tại.

---

## 3. MA TRẬN FIT–GAP CHUẨN C01–C15 (BẮT BUỘC)

Chấm từng tiêu chí bằng `NATIVE | CONFIG | EXTENSION | EXTERNAL | MISSING | UNKNOWN`, kèm `GATE PASS / GATE FAIL (measured) / NOT DEMONSTRATED`, bằng chứng commit/dòng, độ tin cậy, rủi ro, phương pháp POC, effort `L/M/H/VH` **chỉ là ước tính**. Không dùng điểm trung bình để bù một hard gate thất bại.

| Mã | Năng lực BodhiAtlas | Câu hỏi áp dụng riêng cho Bang-ha |
|---|---|---|
| **C01** | Universal Document Ingestion | Corpus Bilara/TEI/HTML có adapter; PDF, EPUB, DOCX, Markdown ngoài corpus có đường import tổng quát không? |
| **C02** | OCR / layout / reading order | Có OCR nội tại hay cần Docling/engine ngoài? Missing page, 2 cột, footnote và chữ Hán/Nôm có báo lỗi? |
| **C03** | Canonical Text & Source Map | Original byte hash, structured text, reversible normalization, locator, extraction revision, mapping tới file gốc? |
| **C04** | Work–Expression–Edition–Witness–File | Nhiều bản dịch, ấn bản, dị bản và file bản sao có ID/quan hệ tách đúng? |
| **C05** | Exhaustive EXACT code-only | Liệt kê **mọi occurrence + offsets** toàn phạm vi, không top-K/record-only/chunk miss, có oracle? |
| **C06** | Normalized multilingual retrieval | Pāli ā/ṭ/ṃ, tiếng Việt có/không dấu, `đ/d`, Hán giản/phồn, CJK 1–2 ký tự, Tạng/Wylie, NFC/NFD, map ngược offsets? |
| **C07** | Fuzzy / OCR-tolerant retrieval | Đã có edit-distance/character ngram thật hay chỉ FTS/ontology; nhãn match mode chuẩn? |
| **C08** | Sense-aware lexicon | Lexeme/sense/nguồn chứng/attestation/quan hệ nghĩa, reviewer; không tự đồng nhất `anatta` với mọi cách dịch? |
| **C09** | Semantic/RAG (optional) | Có dùng LLM trong đường bắt buộc không; có thể tắt hẳn; chi phí model/embedding là bao nhiêu? |
| **C10** | Verified citation + reopen | Giữ file SHA, edition, exact quote, passage/page/bbox/CFI/TEI locator và independent verifier; `VERIFIED` do ai cấp? |
| **C11** | Wiki / notes / claims | Claim–Evidence–Contradiction gate có fail-closed, bằng chứng phản chứng và người duyệt không? |
| **C12** | REST/MCP/export interoperability | API read-only, provenance/status, quyền truy cập và dữ liệu xuất có giữ được trích dẫn? |
| **C13** | Coverage, incremental rebuild, QA | Stage/atomic publish/rollback; missing source, error, quarantined record, OCR gaps; rebuild deterministic? |
| **C14** | Rights/security/privacy/backup | Quyền từng bản dịch, cấu hình private/cloud, CORS/auth, file path traversal, offline mode, backup/restore? |
| **C15** | Operability/portability/TCO | Clean clone/cold rebuild, Windows-only D:/E: dependency, RAM/disk, số dịch vụ, migration, maintenance, token AI? |

**Kết luận từng hàng phải nêu tác động với quyết định kiến trúc**: ADOPT / USE AS COMPONENT / TRIAL ONLY / REJECT; không biến `NATIVE` thành `G1 PASS` nếu chưa kiểm thật.

---

## 4. 12 NHÓM GIẢ THUYẾT CẦN PHẢN BIỆN KHÔNG THIÊN LỆCH

H01. `Bang-ha` chứa code framework cốt lõi có thể chạy portable từ clean clone; **bằng chứng phản bác** là thiếu registry/DB ngoài Git, hard-coded drive paths hoặc build phụ thuộc nội dung không có.

H02. Schema passages+sources+translations đã đủ identity học thuật; phản bác nếu edition dùng string/ID không scope theo bản dịch, không có extraction revision, identity nguồn có thể đổi khi rebuild.

H03. `exact` trong CLI tương đương exhaustive EXACT; phản bác bằng một record có 5 occurrences, queries 1–2 Hán tự, câu đi qua ranh giới hoặc phép tìm phân trang/top limit.

H04. JSON pointer/HTML line/TEI XPath cho phép mở đúng **từng nguyên văn và bối cảnh** sau reindex; phản bác bằng anchor trôi hoặc không thể đối chiếu raw file SHA.

H05. SuttaCentral Pāli ↔ bản dịch Việt hoặc Āgama Hán ↔ Việt có mapping đoạn **được kiểm**; phản bác bằng ví dụ một đoạn không tương ứng 1:1 hoặc anchor `sc`/line không xác lập equivalence.

H06. Ontology và parallel lookup đủ đáng tin để gọi là cross-language scholarly mapping; kiểm provenance *từng sense/edge*, không coi bảng thuật ngữ hoặc heuristic là verified relation.

H07. Publication stage/activate/rollback an toàn khi build hỏng giữa chừng; kiểm fail injection, old reader session, corruption, checksum và restore.

H08. QA của repo chứng minh độ bao phủ toàn bộ corpus; đối chiếu sample-only QA, quarantined sources, invalid locators, XML có blob nhưng chưa đọc, historic tests vs HEAD.

H09. Sổ cái `EvidenceRecord` không tự tạo `VERIFIED` khi thiếu source; thử mặc định và câu `SUPPORTED` dựa trên evidence chưa kiểm, bypass, fake SHA/locator.

H10. Class T1–T5 là kết quả đánh giá nguồn thực; kiểm nguồn giá trị `T1` và code default, policy review, xem có auto-assign tất cả không.

H11. Có thể cho public-cloud REST/MCP an toàn; kiểm auth, CORS, quyền theo file/user, đường dẫn ngoài sandbox, network egress tự tải Parquet/corpus, denial-of-service; không cố khai thác hệ thống production.

H12. Fork Bang-ha-led rẻ hơn Minimal Core/BCR-led; so sánh **số tầng phải sửa** (schema, parser, locator, search, verifier, UI, export, rights, backup), không dùng lượng corpus sẵn có làm lý do quyết định codebase nếu dữ liệu có thể import qua connector.

Mỗi giả thuyết cần `CONFIRMED | REFUTED | PARTIAL | UNKNOWN` và đường mã/dòng + test/log/điều kiện đảo kết luận.

---

## 5. POC/GOLD TEST — ÍT NHẤT 18 TÌNH HUỐNG, ƯU TIÊN CA CÓ KHẢ NĂNG BÁC BỎ

**Không cần chạy toàn bộ nếu thiếu quyền hoặc môi trường**, nhưng thiết kế đủ cụ thể để AI khác/lập trình viên thực hiện ngay. Tách `EXECUTED` và `PLAN`; có input fixture, expected, actual nếu đã chạy, metrics, log/artifact đường dẫn, severity khi fail. Không lấy `test_ui.py` hoặc `TEST_REPORT.md` làm test pass ở phiên này.

| ID | Phép thử | Điều kiện thành công / điều phải phát hiện |
|---|---|---|
| **TC01** | Clean checkout & reproducible bootstrap | Clone SHA mới trên Linux sạch/Windows, build sandbox không đòi DB ẩn D:/E: hoặc khai báo chính xác phần phụ thuộc không có |
| **TC02** | Registry + rights + file SHA | Manifest/chains đúng source/version/hash, quyền từng bản dịch/ấn bản không bị lấy quyền từ repo cha |
| **TC03** | Bilara parse + `mn1:1.1` raw reopen | Giữ đúng JSON pointer và văn bản theo nguồn Pāli, không biến normalize thành raw |
| **TC04** | Hán/Việt `da1` anchors & version | Đúng bản Hán/Việt, Taishō line/HTML anchor; không gọi hai bản đồng nhất tự động |
| **TC05** | TEI/XML roundtrip | XPath/IDs/page markers trỏ lại đúng node; malformed XML bị quarantine, không báo READY |
| **TC06** | EXACT 5 occurrence trong 1 record | Trả 5 offsets theo oracle trong `canonical text`, kể cả overlapping nếu query quy định cho phép |
| **TC07** | CJK 1 ký tự và 2 ký tự | Không âm thầm drop vì trigram/tokenizer, báo rõ EXACT vs FTS candidate |
| **TC08** | Unicode multi-mode | `anatta`/`anattā`, `dhamma`, `vô ngã`/`vo nga`, NFC/NFD, `đ/d`, giản/phồn, Tạng/Wylie; map vị trí normalized đúng về raw |
| **TC09** | Query qua ranh giới passage/chunk | Kiểm liệu có false negative hoặc bị cắt; khai báo scope chính xác và mọi occurrence được phép |
| **TC10** | Hai ấn bản khác nhau, có chữ phủ định | Search hit, get-source và citation bắt đúng `edition_id`, file hash và câu `không` khác biệt |
| **TC11** | Ingest sách ngoài corpus | PDF text, PDF scan, EPUB, DOCX hợp pháp; giữ source identity, mọi page/CFI có precision status; fail được phân loại |
| **TC12** | OCR mất chữ phủ định/missing page | Không cấp VERIFIED; đánh dấu OCR_NEEDS_REVIEW/PARTIAL; không âm thầm tạo nghĩa trái |
| **TC13** | Rebuild index không đổi source | Tái chạy cùng inputs/build profile → deterministic artifact hoặc có giải thích khác biệt; source/file SHA giữ đúng |
| **TC14** | Fault injection publication & rollback | Crash trước/giữa activation; reader vẫn thấy snapshot hợp lệ, rollback còn nguyên citation cũ |
| **TC15** | Ledger `VERIFIED` defaults | Tạo EvidenceRecord thiếu file hash/locator/raw check: hệ thống bắt buộc từ chối VERIFIED; nếu không, ghi P0 failure |
| **TC16** | Ledger `SUPPORTED` / bypass | Một evidence UNREVIEWED hoặc REJECTED, claim phủ định; hỗ trợ claim chỉ khi policy G3 thực sự qua verifier và review |
| **TC17** | Parallel/ontology false equivalence | Một cặp Pāli–Hán–Việt có khác biệt đoạn/nghĩa: hệ thống không tự cấp scholarly equivalent/SUPPORTS |
| **TC18** | Coverage + quarantine regression | Tài liệu thiếu file, lỗi parser, HTML đa dòng, nguồn XML lớn; status/report thể hiện chính xác scope và thất bại |
| **TC19** | REST/MCP/offline security | Loopback vs LAN, quyền user/host, CORS không thay auth, SQL/file access, egress no-cloud; không công bố dữ liệu private |
| **TC20** | Backup/restore, metadata migration, rights | Trên máy sạch, restore index + raw + manifest + ledger + evidence, mọi locator/citation đối chiếu được |
| **TC21** | Scalability under bounded budget | p50/p95 latency, RAM peak, SSD/disk, record count, cold/warm rebuild, backup time; đo trên fixture và phần corpus được phép |
| **TC22** | A/B architecture cost comparison | Thử *cùng một vertical slice* bằng Bang-ha-led/BCR-led/minimal core: số file phải sửa, LOC delta, deps, service count, debug token, gate outcomes, upstream merge friction |

**Gold oracle tối thiểu:** fixture do nhóm tự viết 2 ấn bản có một chữ phủ định khác nhau; 1 đoạn có 5 lần lặp, 1 câu vượt ranh giới; Pāli có/không dấu, tiếng Việt NFC/NFD và Hán ký ngắn; 1 EPUB/PDF scan giả lập có locator và missing page đã biết. Dữ liệu chính trong repo chỉ dùng để kiểm đường nguồn nếu quyền cho phép. Không dùng OCR hay LLM tự sinh *gold answer* mà không kiểm lại bằng mắt/source.

**Chỉ số nghiệm thu:** `exact_occurrence_recall=1.0` và `exact_precision=1.0` **trên declared indexed scope và golden text**; `wrong_file_or_edition_count=0`; `false_verified_count=0` trong adversarial gold; 100% source hashes đúng; locator reopen rõ precision (page-only không giả thành bbox/character); report đầy đủ missing/partial. Các ngưỡng là yêu cầu/đề xuất policy, không phải số đã đo. Nếu sample không đại diện, báo scope. Với `UNKNOWN/NOT TESTED`, không ghi `PASS`.

**Thứ tự chi phí thấp nhất:** TC01 → TC03 → TC06 → TC10 → TC15/TC16 → TC14 → TC11 → TC22; chỉ mở rộng khi một lựa chọn vẫn sống sót sau gate P0. Nếu đầu tiên đã fail cần đánh giá *mức sửa để đạt* chứ không bỏ mặc năng lực tái sử dụng khác.

---

## 6. ĐÁNH GIÁ LỰA CHỌN KIẾN TRÚC MÀ KHÔNG CÓ THÀNH KIẾN

So sánh ít nhất các phương án dưới đây. Dùng **cùng golden fixtures, quyền dữ liệu và G1–G6**. Lập hai bảng xếp hạng riêng: (i) *Fastest useful demo* và (ii) *Lowest total cost/risk to compliant V1*. Nếu chưa đo, đặt rõ `QUALITATIVE ESTIMATE`, không gọi là benchmark.

- **A — Bang-ha-led:** port/localize `local_corpus_framework` làm authoritative BodhiAtlas core; bổ sung books, OCR, source map, exact offsets, verification, rights, web UI.
- **B — BCR-led:** mở rộng BCR corpus/verifier thành kho thư viện đa định dạng; Bang-ha là corpus connector, không nhập nguyên database.
- **C — Minimal BodhiAtlas Evidence Core:** một SQLite/Postgres catalog nhỏ + object store + versioned extraction/source map + exhaustive EXACT + verifier; tận dụng parser và các module thật sự cần.
- **D — book-memex-led:** sử dụng book library/reader/FTS rồi thêm provenance & scholarly identity; so đo thay đổi thực sự ở importer/search/reader.
- **E — Open Notebook/RAGFlow-first:** lấy notebook/RAG platform làm core; chỉ chọn nếu chứng minh được G1/G2 và tổng vận hành rẻ hơn, không dùng roadmap chưa ra mắt để tăng điểm.
- **F — Bang-ha as component/connector:** giữ nguyên repo/corpus, dùng one-way import hoặc read-only adapter tới BodhiAtlas authority; cân chi phí sync, kiểm source quyền và locators.
- **G — Bang-ha corpus foundation + BCR verification reused, without general-purpose framework:** nếu tin rằng hybrid này thắng, phải chứng minh không kéo hai DB cùng quyền ghi, không nhân đôi source ID và không làm vỡ G2.

**Bảng trade-off tối thiểu:** nguồn dữ liệu authoritative; schemas phải sửa; code/module thực sự tái dùng; duplication; lock-in; hard gates; CPU/RAM/storage; cloud/offline; token AI/debug; upgrade/rebase; model provider dependencies; license; khả năng chuyển đổi công nghệ. Phân biệt **cost of first demo** vs **cost to trustworthy V1**.

**Quy tắc đảo quyết định:** Nếu Bang-ha làm thư viện tổng quát với một patch nhỏ đã đo, không mất source fidelity và rebase dễ → ưu tiên `TRIAL AS CORE` trước. Nếu sửa nhiều lớp hoặc đòi private D/E data khó triển khai → chỉ dùng corpus/parts. Nếu BCR resolver đã đạt G2 tốt và dạng source phù hợp → BCR-led có thể thắng. Nếu Minimal Core phình thành framework/plugin/microservices → C mất lợi thế. **Không được chọn C chỉ vì các báo cáo khác đang chọn C.**

---

## 7. RỦI RO HỌC THUẬT VÀ PHÁP LÝ: PHÂN TÍCH BẮT BUỘC

- **Phân biệt rõ:** match raw/extracted string → locator check → textual citation verified → semantic support → scholarly claim/publish approval. Không có một boolean `verified` cho tất cả.
- **Sơ đồ chain of custody:** Original bytes + rights + SHA256 → source/edition/witness → extraction revision (tool/model/profile) → canonical/normalized text + reversible map → passage span → search occurrence → independent checker → reviewer → Evidence Card. Từng đường data code có hay chưa?
- **Potential red flags từng kiểm ở P39 (chưa phải kết quả phiên mới):** `review_state='VERIFIED'` mặc định; `SUPPORTED` dựa trên evidence chưa `REJECTED`; `bypass_evidence_check`; `instr` chỉ tìm record; `T1` gán mặc định; source URL hardcoded owner cũ; QA sampling; unsafe MCP/web default; quyền bản dịch Việt chưa toàn diện; release rollback chưa test. Phải mở code HEAD mới xác nhận/refute.
- **Rủi ro provenance dịch thuật:** Việt dịch ở HTML, bản sách DOCX/EPUB tạo ra, Taishō line, Bilara ID, SuttaCentral root có thể không 1:1. Tránh gọi `parallel` là bản tương đương được chứng minh khi chỉ có heuristic alignment.
- **Rights matrix:** `code license | corpus source license | Vietnamese translation rights | derived EPUB/DOCX | cloud processing rights | redistribution | attribution | modification | commercial/public access`; `UNKNOWN` thực sự là chưa được phép mặc định.
- **Security:** private repository access, API authentication, per-source ACL, network egress, downloaded Parquet/corpus, safe SQL/paths, no published raw private documents. Xác định cloud deployment profile khác offline personal research. Không thử exploit tác động ngoài sandbox.
- **Incident evidence:** so roadmap/tuyên bố hoàn tất với reports lỗi/quarantine và code hiện tại; nêu điểm đã sửa, chưa sửa hoặc không đủ chứng cứ; không phủ định tất cả dự án chỉ vì từng có sự cố.

---

## 8. CẤU TRÚC BÁO CÁO ĐẦU RA BẮT BUỘC — ĐÚNG 13 PHẦN

**Tên duy nhất:** `REPORT_39_BANG_HA_GIAC_NGO_INDEPENDENT_REVIEW.md`, đặt đề xuất dưới `research/technology-assessments/`. Báo cáo P39 cũ phải được giữ nguyên để đối chiếu lịch sử.

1. **Executive Decision** — Một quyết định rõ `ADOPT | TRIAL AS CORE | USE AS COMPONENT | TRIAL ONLY | REJECT`, với confidence và điều kiện đảo quyết định. Nêu một kiến trúc ưu tiên, không đề xuất “cứ ghép hết repo”.
2. **Sources & Evidence Ledger** — snapshot repos/SHAs/quyền, link file+dòng, ít nhất 25 nguồn code được kiểm, các phát hiện quan trọng có claim ID, nhãn bằng chứng và phản chứng.
3. **Architecture & Data Flow** — sơ đồ corpus→parser→source registry→SQLite→FTS→CLI/UI/MCP, dependencies ngoài Git, ownership state, luồng thay parser/build; sơ đồ hiện trạng tách sơ đồ đề xuất.
4. **Feature Fit–Gap Matrix C01–C15** — đủ 15 tiêu chí, G1–G6, status, code proof, cost, hard blockers, next test; không tổng điểm che fail.
5. **Deep Technical Findings A–G** — A corpus vs app vs framework; B schema/identity/revision; C ingest/QA/publishing; D multilingual+EXACT/normalization; E locator/verification/ledger; F API/UI/MCP/cloud/security; G reuse/maturity/maintenance; kèm kiểm 12 giả thuyết H01–H12.
6. **Source Fidelity & Provenance** — chain of custody, minh họa 2 ấn bản/1 chữ phủ định, OCR thiếu từ, rights & reviewer status; đề xuất verifier fail-closed (ghi là proposal nếu chưa làm).
7. **Multilingual & Retrieval Behavior** — oracle codepoint, Pāli/Việt/Hán/Tạng modes, CJK/trigram/FTS, unknown coverage, 100% recall trong scope test và giới hạn ngoài scope.
8. **Integration & Reuse Options** — so A–G, chọn component/file nào thật sự nên port, cái nào không nên fork, DB/API ownership, provenance contract tối thiểu và migration/rollback.
9. **Practical POC / Reproduction Plan TC01–TC22** — bảng input/expected/actual/status, chạy/không chạy, script và test logs; test đã có trong repo ≠ test tự chạy; chỉ số và STOP criteria.
10. **Deployment, Security, Legal & Cost** — private access, D/E vs portable, filesystem, license, translator rights, API/MCP auth, backup/restore; TCO assumptions vs measured.
11. **Comparison & Trade-offs** — ít nhất 2 bảng xếp hạng demo nhanh và compliant V1 ít rủi ro/TCO nhất, cùng 3 điều kiện đảo quyết định.
12. **Decision Record for Master Synthesis** — bảng máy đọc: TARGET, CLASS, OWNER, SNAPSHOT, ACCESS, LICENSE, PRIMARY_ROLE, BEST_FIT_V1/V2, C01-C15, G1-G6, SOURCE_FIDELITY, EXACT_GATE, MULTILINGUAL, QUALITY, SECURITY, EFFORT, MAINTENANCE_RISK, RECOMMENDATION, CONFIDENCE, NEXT_POC, TOP_5_STRENGTHS/BLOCKERS/EXPERIMENTS. Có thể thêm JSON không chứa private data.
13. **Appendix** — inventory file+SHA, commands/logs, build dependency map, manifest quyền, discrepancy với P39 cũ, “đã kiểm/không kiểm”, nơi cần quyền/fixture bổ sung; glossary EXACT/NORMALIZED/VERIFIED/SUPPORTS và bibliography.

**Tiêu chí chất lượng của báo cáo:**

- Các kết luận quyết định phải **tự đứng được** dù người đọc chưa đọc báo cáo P39 trước; dẫn nguồn rõ.
- Dùng permalink tới commit + dòng với nhận định kỹ thuật; ghi snapshot nếu GitHub private chỉ chủ tài khoản mở được.
- Mọi con số (file, records, nguồn có quyền, WER, pass rate, giờ công, token, TCO) phải gắn `MEASURED | ESTIMATED | UNKNOWN`, có mẫu số và phạm vi.
- Không nói `VERIFIED` khi mới match code/raw text OCR, không nói `EXACT COMPLETE` khi trả record-level hoặc có top-K.
- Không trích nguyên văn corpus dài hoặc mang dữ liệu riêng tư vào báo cáo public. Dùng ví dụ tự tạo cho test adversarial.
- Không coi bug trong P39 là bug hiện tại nếu không đối chiếu HEAD mới; phân biệt fix đã có/bug chưa test.
- Đưa ra **lựa chọn kỹ thuật cụ thể, có thể bác bỏ**, không kết thúc bằng câu “tùy nhu cầu” chung chung.

---

## 9. QUY TRÌNH THỰC HIỆN TIẾT KIỆM TOKEN VÀ CÔNG SỨC

1. Ghim SHA, thống kê source tree, xác minh private/repo mirror, mở tài liệu bắt buộc **một lần**, tạo Evidence Ledger sơ bộ.
2. Đọc **đường mã end-to-end** cho `search → get-passage → citation → source reopen`, cùng một đường `ingest → build → publish → rollback`; chỉ đọc sâu file nào thuộc đường quan trọng.
3. Tạo ma trận kiểm H01–H12 để **bác bỏ sớm** những giả thuyết đắt tiền. Có thể dừng thử fork nếu schema/editor verification buộc sửa 6+ tầng mà vẫn chưa có lời giải; nhưng tiếp tục nhận diện module có thể tái sử dụng.
4. Tạo golden fixtures hợp pháp nhỏ và **test độc lập** trước; không xây cloud/frontend/RAG/graph chỉ để kiểm đúng citation.
5. Chạy/báo TC01/03/06/10/15/16/14 trước. Nếu môi trường thiếu deps/quyền, cung cấp command reproducible và đánh `NOT RUN`; **không chờ thêm giờ hoặc bịa log**.
6. Đánh giá A–G bằng cùng yêu cầu và công thực đo. Phân biệt **công từ góc độ hệ thống** với công phụ trội riêng của `Bang-ha`.
7. Xuất file Markdown duy nhất. Nếu có code POC, log phụ trợ chỉ là artifact tùy chọn, nhưng **báo cáo chính vẫn là một file** và chứa tổng kết đủ để ra quyết định.

---

## 10. YÊU CẦU CUỐI CÙNG ĐỐI VỚI AI NGHIÊN CỨU

Hãy triển khai nghiên cứu theo prompt này **ngay trong phiên** với quyền và công cụ hiện có. Không hỏi lại điều đã nằm trong tài liệu, không giới hạn ở README, không phản ánh định kiến từ lựa chọn trước. Nếu không có quyền hoặc không chạy được một phần, nói rõ những gì bạn đã kiểm, những gì **chưa kiểm**, đưa ra kết luận **có điều kiện** và chỉ ra phép thử nào thực sự có thể đổi kết luận.

**Câu trả lời cuối của báo cáo phải là câu trả lời dứt khoát và cân bằng:**

> “Nếu tôi phải xây BodhiAtlas V1 cho một nhóm nhỏ với ngân sách token/nhân lực hữu hạn, có nên **lấy Bang-ha làm lõi**, **lấy BCR làm lõi**, **tự xây lõi chứng cứ hẹp**, hoặc **chỉ kế thừa một số module của Bang-ha**? Tôi chọn [một hướng] vì [bằng chứng & rủi ro], với [ngưỡng đảo quyết định] và [ba phép thử quyết định đầu tiên].”

**Đầu ra:** tạo và cung cấp tệp tải `REPORT_39_BANG_HA_GIAC_NGO_INDEPENDENT_REVIEW.md` hoàn chỉnh (13 phần). Không ghi đè `REPORT_39_BANG_HA_GIAC_NGO.md` hiện hữu. Khi không thể tạo file, xuất toàn bộ Markdown đầy đủ để người dùng lưu, nói rõ giới hạn công cụ.
