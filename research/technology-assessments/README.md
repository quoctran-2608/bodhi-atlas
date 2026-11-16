# Bản đồ 24 nghiên cứu công nghệ — BodhiAtlas

**Phiên bản trang tổng quan:** 1.2  
**Ngày lập:** 16/11/2026 · **Cập nhật:** 16/11/2026 (Asia/Ho_Chi_Minh)  
**Số báo cáo:** **24** · **Tệp POC tham khảo:** **1** · **Trạng thái:** Đang thẩm định; **chưa chốt công nghệ**  
**Đối chiếu:** [PRD v1.4](../../docs/PRD.md) · [Định hướng V1 Core](../../docs/V1_CORE_FOUNDATION.md) · [Sổ tay kiểm chứng học thuật](../../docs/ACADEMIC_RISKS_AND_VERIFICATION.md)

> **Đọc nhanh:** BodhiAtlas V1 Core cần **file/ấn bản gốc → tiêu hóa và định vị → tra cứu bằng code → kiểm chứng độc lập → phiếu truy nguyên nguồn**. **Không có báo cáo nào hiện chứng minh một công cụ đơn lẻ hoàn thành tất cả công việc này.** Các báo cáo là bằng chứng để quyết định thận trọng, không phải stack đã chọn.

## 1. Danh mục tra cứu nhanh theo chức năng

**Cách đọc bảng:** Tên màu xanh dẫn vào **báo cáo đầy đủ**. Cột **Giá trị** nói công cụ có ích cho BodhiAtlas ở đâu; cột **Giới hạn** nêu điều **không được hiểu lầm**. Các tầng T1–T4 tham chiếu [sơ đồ khái niệm 5 tầng](../../docs/assets/bodhiatlas-5-layer-model.svg), **không** khẳng định đây là thành phần đã tích hợp.

### A. Quản lý nguồn và thư viện — Tầng 1

| Nghiên cứu | Giá trị cho BodhiAtlas | Giới hạn cần nhớ |
|---|---|---|
| **P05 · [Zotero](REPORT_05_ZOTERO.md)** | Biên mục sách/bài báo, tác giả, DOI/ISBN, ghi chú và tài liệu tham khảo; có thể nối metadata | Không phải bộ định danh mọi ấn bản/vị trí trích dẫn; chưa POC |
| **P06 · [Calibre](REPORT_06_CALIBRE.md)** | Quản lý và chuyển đổi ebook, đọc EPUB và tổ chức thư viện | Khả năng đọc/tìm toàn văn không thay source map hoặc kiểm chứng trang |
| **P44 · [Paperless-ngx](REPORT_44_PAPERLESS_NGX.md)** | Hệ quản lý tài liệu, nạp PDF, OCR, phân loại, workflow, API và quyền người dùng | Chỉ đáng thử làm DMS phụ trợ; không tự quản ấn bản học thuật hay tìm hết mọi lần xuất hiện EXACT |
| **P51 · [BDRC / BUDA](REPORT_51_BUDA_BDRC.md)** | Nguồn thư mục Phật học, nhận diện tác phẩm–ấn bản, scan/IIIF, RDF metadata và đường mở lại ảnh trang | **Không phải engine OCR hoặc tìm EXACT của BodhiAtlas**; quyền truy cập/tải ảnh và e-text phải kiểm theo từng mục; số liệu thử HTTP chỉ chứng minh phản hồi mẫu |

### B. Tiêu hóa tài liệu, OCR và cấu trúc — Tầng 2

| Nghiên cứu | Giá trị cho BodhiAtlas | Giới hạn cần nhớ |
|---|---|---|
| **P12 · [Docling](REPORT_12_DOCLING.md)** | Trích xuất nội dung và cấu trúc từ PDF, EPUB, DOCX; một hướng khảo sát source map/định vị | Cần thử chất lượng theo từng định dạng, OCR và locator gốc; chưa nghiệm thu |
| **P45 · [MinerU](REPORT_45_MINERU.md)** | OCR, nhận diện bố cục/tài liệu phức tạp; Middle JSON và metadata trang/block làm đầu vào adapter | Đầu ra không mặc nhiên là nguyên văn đã xác minh; FTS của Doclib không đủ EXACT vét hết; giấy phép cần rà |
| **P46 · [Marker (Datalab)](REPORT_46_MARKER_DATALAB.md)** | Chuyển PDF thành JSON/HTML/chunks, OCR và nhận diện bảng/bố cục | Locator chủ yếu cấp block; EPUB/DOCX qua PDF trung gian; **license model** cần kiểm riêng |
| **P47 · [GROBID](REPORT_47_GROBID.md)** | Trích cấu trúc **bài báo PDF học thuật** thành TEI: tác giả, mục, chú thích, references, DOI và tọa độ | Không phải OCR/ingest đa định dạng; chưa chứng minh độ đúng trên sách kinh, Hán/Pāli/Tạng |
| **P52 · [olmOCR](REPORT_52_OLMOCR.md)** | Ứng viên OCR bổ trợ cho trang PDF/scan khó, có văn bản và ánh xạ ký tự sang **trang PDF** trong Dolma JSONL | **Không có bbox từng từ/câu** và không chứng thực chữ do VLM tạo; chưa chạy POC trên sách Phật học |
| **P53 · [Xberg / Kreuzberg](REPORT_53_XBERG_KREUZBERG.md)** | Bộ trích xuất đa định dạng PDF, EPUB, DOCX, Markdown/XML; cấu trúc, trang, cảnh báo và OCR tùy cấu hình | Source map, EPUB CFI, tính đủ/đúng OCR còn cần thử; không đưa REST công khai khi chưa có xác thực |

### C. Tra cứu bằng code, corpus và chứng cứ — Tầng 3

| Nghiên cứu | Giá trị cho BodhiAtlas | Giới hạn cần nhớ |
|---|---|---|
| **P20 · [SQLite FTS5 / trigram](REPORT_20_SQLITE_FTS5_TRIGRAM.md)** | Chỉ mục lexical, tìm chuỗi/từ khóa/ứng viên bằng code với dữ liệu có cấu trúc | FTS chưa đồng nghĩa exact từng ký tự; phải hậu kiểm nguyên văn, vị trí; POC đã chạy trên **fixture tổng hợp** |
| **P03 · [BuddhismDocuments-for-AI](REPORT_03_BUDDHISMDOCUMENTS_FOR_AI.md)** | Corpus kinh điển được ghim phiên bản, tìm nguồn và bộ resolver xác minh một số loại dẫn chứng | Chưa nạp sách bất kỳ và thiếu locator PDF/EPUB phổ quát; chưa kiểm thử độc lập ở báo cáo |
| **P39 · [Bang-ha-giac-ngo](REPORT_39_BANG_HA_GIAC_NGO.md)** | Kho kinh Pāli–Hán–Việt, parser, index SQLite và thiết kế ledger/đối chiếu có thể thử kế thừa | **Repo nguồn PRIVATE; báo cáo này PUBLIC**. Rights, chính xác locator và verified claim chưa đạt gate; chỉ TRIAL ONLY |
| **P40 · [FoJin](REPORT_40_FOJIN.md)** | Nền tảng Phật học, tra cứu kinh, URN, tác phẩm/bản song hành và giao diện đối chiếu; có thể nối read-only | `exact/verbatim` qua chuẩn hóa/shortlist **không** là EXACT nguyên ký tự/vét hết của BodhiAtlas; chưa POC |

### D. Thuật ngữ và quan hệ đa ngôn ngữ — Tầng 3 / các lớp bổ trợ

| Nghiên cứu | Giá trị cho BodhiAtlas | Giới hạn cần nhớ |
|---|---|---|
| **P41 · [Dharmamitra / DharmaNexus](REPORT_41_DHARMAMITRA_DHARMANEXUS.md)** | Hệ sinh thái nguồn/segment, tìm song hành Sanskrit–Pāli–Hán–Tạng, từ điển và NLP; cung cấp đối chiếu tham khảo | Không phải một repo duy nhất; **ToS hạn chế dùng API để điền dữ liệu ứng dụng khác** khi chưa có phép; bản quyền từng nguồn khác nhau |
| **P42 · [MITRA-parallel](REPORT_42_MITRA_PARALLEL.md)** · [POC mẫu](POC_42_MITRA_PARALLEL.py) | Dữ liệu **ứng viên căn chỉnh** các đoạn Sanskrit–Tạng–Hán; có thể tạo PassageLink để người nghiên cứu duyệt | `score` không phải xác suất đúng; chưa xác minh từng mối liên hệ với bản gốc. **POC chỉ chạy trên dữ liệu giả lập**, không phải thử dataset thực |
| **P43 · [Digital Pāḷi Dictionary (DPD)](REPORT_43_DIGITAL_PALI_DICTIONARY_DPD.md)** | Từ điển Pāli, mục từ, biến tố, gốc từ, gợi ý phân tích hợp từ; hữu ích cho LEXICON có kiểm soát | Quyền **CC BY-NC-SA** và nội dung chưa hoàn thiện phải đánh giá; không tự có sense ID học thuật hoặc locator của sách người dùng |
| **P55 · [BuddhaNexus legacy](REPORT_55_BUDDHANEXUS_LEGACY.md)** | Nghiên cứu lịch sử phương pháp tìm đoạn song hành Pāli–Sanskrit–Tạng–Hán, các bộ segment và dữ liệu căn chỉnh cũ | **Backend legacy đã archived, không đề xuất làm platform V1**; ID/segment cũ chưa chứng minh tương thích DharmaNexus; dữ liệu, quyền và backend cần kiểm |

### E. Truy xuất mở rộng, RAG và Second Brain — Tầng 4A/4B

| Nghiên cứu | Giá trị cho BodhiAtlas | Giới hạn cần nhớ |
|---|---|---|
| **P02 · [QMD](REPORT_02_QMD_TOBI_QMD.md)** | Bộ tìm ứng viên local trên Markdown, BM25, hybrid/vector, SDK/MCP | Trả document/chunk, không phải mọi occurrence và trang/bbox/CFI đã xác minh |
| **P01 · [RAGFlow](REPORT_01_RAGFLOW.md)** | Pipeline ingest/chunk, hybrid/semantic retrieval, RAG và wiki/tri thức được tổng hợp tùy chọn | Citation theo chunk/similarity không tự chứng minh đúng nguyên văn, ấn bản và định vị |
| **P04 · [Karpathy LLM Wiki / Second Brain pattern](REPORT_04_KARPATHY_LLM_WIKI_SECOND_BRAIN_PATTERN.md)** | Mẫu thiết kế ghi chú, wiki, quan hệ/nhận định tích lũy và tái sử dụng tri thức | **Pattern**, không phải sản phẩm plug-and-play; kiến thức AI sinh ra vẫn phải kiểm chứng |

### F. So sánh dị bản, phát hiện văn bản tương đồng và biên tập có người duyệt — Lớp nghiên cứu bổ trợ

| Nghiên cứu | Giá trị cho BodhiAtlas | Giới hạn cần nhớ |
|---|---|---|
| **P48 · [CollateX](REPORT_48_COLLATEX.md)** | Căn chỉnh **nhiều nhân chứng của cùng đoạn văn**; tạo bảng sai khác, gợi ý bộ máy chú thích dị bản (critical apparatus) | Không tìm kiếm toàn kho hay tự chứng minh bản văn tương đương; cần thử lỗi alignment/transposition và giữ locator gốc |
| **P49 · [passim](REPORT_49_PASSIM.md)** | Phát hiện **đoạn tái sử dụng/tương đồng** trên corpus lớn; xuất cặp span và vị trí ứng viên để kiểm tra | Bộ lọc n-gram có thể bỏ văn bản lặp, Hán ngắn; chạy Spark, không phải EXACT toàn vị trí hay bằng chứng ảnh hưởng lịch sử |
| **P50 · [INCEpTION](REPORT_50_INCEPTION_ANNOTATION.md)** | Công cụ **gắn nhãn học thuật có người duyệt**: annotation span/relation, phân công, đối chiếu bất đồng và xuất CAS | Hướng **V2 curation**, không thay V1 Core; CAS offset/ID và nhãn curator cần đối chiếu nguồn/ấn bản trước khi phê duyệt |

**Tầng 5 — Giao diện nghiên cứu:** các công cụ như BUDA, INCEpTION và FoJin có UI hữu ích để học hỏi, nhưng **chưa có nghiên cứu chứng minh giao diện phiếu truy nguyên nguồn hoàn chỉnh**, mở đúng ấn bản và phân biệt kiểm chứng câu chữ/vị trí/luận điểm theo PRD BodhiAtlas.

**Mã nghiên cứu:** giữ nguyên mã P của từng báo cáo. **P54 chưa được cung cấp trong đợt này**; khoảng trống mã không đồng nghĩa tài liệu bị thất lạc.

## 2. Kết luận thẩm định: có tiềm năng, chưa phê duyệt

| Nhóm đề xuất trong từng báo cáo | Các mã | Ý nghĩa |
|---|---|---|
| **USE AS COMPONENT** *(kể cả pattern/thành phần có điều kiện)* | P01, P02, P03, P04, P05, P06, P12, P20, P40, P41, P46, P47, **P51** | Có năng lực đáng xem xét **trong đúng vai trò**; không là quyết định triển khai |
| **TRIAL ONLY** | P39, P42, P43, P44, P45, **P48, P49, P50, P52, P53, P55** | Còn rào cản về quyền, nguồn/locator, chất lượng hoặc POC; chỉ thử có kiểm soát |

**Đọc nhãn cho đúng:** `DOC` = đã đọc tài liệu; `CODE` = đã đọc mã; `TESTED` = tự chạy có log và phạm vi rõ; `ISSUE` = báo cáo ngoài chưa tái hiện; `INFERRED` = suy luận có căn cứ; `UNKNOWN` = chưa xác minh. Chỉ đánh giá theo **đúng vai trò của ứng viên**: không trừ điểm GROBID vì thiếu quản lý ebook, hoặc trừ DPD vì không OCR.

**Điểm chưa được chứng minh cho V1 Core:** ingest đầy đủ nhiều định dạng; OCR và bản đồ lỗi theo trang; đúng từng ấn bản/nguồn bất biến; `EXACT` vét mọi vị trí; tra cứu Hán giản/phồn và Pāli/Sanskrit dấu phụ; mở lại đúng vị trí PDF/EPUB; và phân biệt xác minh câu chữ, định vị với mức hỗ trợ của lập luận.

**Giới hạn thực nghiệm:** P42 có tệp POC Python **3 fixture tổng hợp**, không có dữ liệu MITRA v3 thực, không kiểm chứng nguồn hoặc chất lượng alignment. P20 có phép thử fixture tổng hợp trong báo cáo riêng. P51 có một số lần **đọc phản hồi HTTP mẫu** (RDF/IIIF), không phải kiểm định toàn corpus, dữ liệu thô hoặc triển khai Java. **P48–P50, P52–P53, P55 chưa chạy POC thực nghiệm** theo các báo cáo. Những mục ghi `NOT TESTED` chỉ là thẩm định mã/tài liệu; file test của một dự án không phải `[TESTED]` của cuộc khảo sát.

## 3. Cách đi tiếp và quản lý nghiên cứu

1. **Mở báo cáo:** nhấn tên công nghệ phía trên; đọc *Executive Decision*, *Evidence Ledger*, *Fit–Gap*, *POC plan* và *Open Questions* trước khi so sánh.
2. **Thử theo đúng nhiệm vụ:** Docling, MinerU, Marker và Xberg có thể so trên **bộ ingest/OCR đa định dạng**, còn GROBID nên có benchmark riêng cho bài báo; olmOCR cần thử riêng các trang scan khó. CollateX so trên đoạn/witness đã xác định, passim trên corpus tìm đoạn tương đồng, INCEpTION trên luồng annotation/curation. Dùng gold set và cổng kiểm nguồn phù hợp từng vai trò, không xếp hạng sai phạm vi.
3. **Ra quyết định sau POC:** lưu phiên bản/commit, corpus, môi trường, chi phí, lỗi và các cổng G1–G6; ghi quyết định riêng có người chịu trách nhiệm, **không sửa ngược báo cáo cũ cho hợp kết luận mới**.
4. **Bổ sung hồ sơ:** theo [mẫu nghiên cứu](REPORT_TEMPLATE.md); giữ nguyên mã P, ngày khảo sát, nguồn ghim commit và nội dung gốc. Có thể đặt script/fixture minh họa cạnh báo cáo khi có liên kết rõ.

### Quyền riêng tư và bản quyền

- Repo nguồn **P39 Bang-ha-giac-ngo là PRIVATE** theo khảo sát; **bản báo cáo P39 đã đưa vào BodhiAtlas PUBLIC** theo yêu cầu chủ dự án. Nhãn PRIVATE không bảo vệ bản sao báo cáo công khai. Link vào repo nguồn có thể yêu cầu quyền truy cập.
- Các ứng viên như Dharmamitra/DharmaNexus, DPD, MinerU, Marker, CollateX, passim và BUDA/BDRC có điều khoản **API, dữ liệu, license code/model/weights** khác nhau. Thẩm định quyền riêng cho từng cách dùng; không coi một repo công khai là cho phép tự do sao chép toàn bộ dữ liệu.

> **Nguyên tắc xuyên suốt:** nghiên cứu độc lập → thử nghiệm tái lập → đối chiếu [PRD](../../docs/PRD.md) và quality gates → **quyết định triển khai riêng**. Không gộp khả năng tìm *ứng viên* với năng lực *kiểm chứng trích dẫn học thuật*.
