# Bản đồ nghiên cứu công nghệ BodhiAtlas

**Phiên bản trang tổng quan:** 1.0 · **Ngày lập/cập nhật:** 16/11/2026 (Asia/Ho_Chi_Minh)  
**Số báo cáo:** 9 · **Trạng thái:** Đang nghiên cứu, **chưa chốt công nghệ**  
**Căn cứ đánh giá:** [PRD v1.4](../../docs/PRD.md) · [Định hướng V1 Core](../../docs/V1_CORE_FOUNDATION.md) · [Sổ tay kiểm chứng học thuật](../../docs/ACADEMIC_RISKS_AND_VERIFICATION.md)

> **Đọc trong 30 giây:** Không có báo cáo nào chứng minh một công nghệ đơn lẻ đã đáp ứng trọn V1 Core. BodhiAtlas cần **file gốc + định danh ấn bản + văn bản có cấu trúc/bản đồ nguồn + tìm kiếm bằng code + kiểm chứng độc lập**. Các công cụ bên dưới có thể đóng góp vào **từng năng lực**, không tự thay thế nền tảng đó.

## 1. Tổng quan 9 nghiên cứu — đọc nhanh và mở chi tiết

**Cách đọc:** Tầng 1–5 theo [sơ đồ kiến trúc khái niệm](../../docs/assets/bodhiatlas-5-layer-model.svg). Các tầng ghi trong bảng chỉ là **vị trí có thể đóng góp**, không phải quyết định tích hợp. Nhấn vào **tên công nghệ** để xem toàn bộ báo cáo gốc, bằng chứng, giới hạn và đề xuất kiểm thử.

| Nghiên cứu | Vị trí trong mô hình | **Giá trị cụ thể cho BodhiAtlas** | **Giới hạn quan trọng** |
|---|---|---|---|
| **P05 — [Zotero](REPORT_05_ZOTERO.md)** | **T1** · Thư mục | Quản lý tác giả, DOI/ISBN, tài liệu tham khảo, ghi chú và trích dẫn; có thể đồng bộ metadata | Không phải kho nguồn gốc/ấn bản học thuật và bộ định vị mọi câu trích; chưa POC |
| **P06 — [Calibre](REPORT_06_CALIBRE.md)** | **T1** · Ebook | Quản lý, đọc, chuyển đổi PDF/EPUB/DOCX; hỗ trợ thư viện ebook thuận tiện | Tìm toàn văn và chức năng đọc không tự bảo đảm đúng trang/vùng chữ, OCR coverage hay ấn bản; chưa POC |
| **P12 — [Docling](REPORT_12_DOCLING.md)** | **T2** · Tiêu hóa | Trích xuất PDF/scan, EPUB, DOCX, Markdown; xử lý cấu trúc, có provenance trang/bbox ở các đường PDF | Độ đúng OCR/reading order và định vị EPUB CFI chưa được thử đạt chuẩn BodhiAtlas; chưa POC |
| **P03 — [BuddhismDocuments-for-AI](REPORT_03_BUDDHISMDOCUMENTS_FOR_AI.md)** | **T3** · Corpus và chứng cứ | Có nguồn Phật học được ghim phiên bản, quan hệ corpus, tra cứu từ vựng, một số resolver kiểm chứng trích dẫn | Không nạp mọi PDF/EPUB/DOCX; chưa bảo đảm EXACT vét hết và locator cho mọi định dạng; chưa tái chạy test độc lập |
| **P20 — [SQLite FTS5 / trigram](REPORT_20_SQLITE_FTS5_TRIGRAM.md)** | **T3** · Chỉ mục | Nền tìm kiếm lexical bằng code, hỗ trợ token/phrase, CJK và ứng viên chuỗi con, nhẹ và có thể tạo lại | Không tự xác minh file/trang; phải hậu kiểm EXACT, xử lý truy vấn Hán ngắn. **Có POC fixture tổng hợp, chưa thử corpus thật** |
| **P39 — [Bang-ha-giac-ngo](REPORT_39_BANG_HA_GIAC_NGO.md)** | **T1–T3**, có mở rộng | Kho kinh Pāli–Hán–Việt, parser, corpus định danh đoạn, framework SQLite FTS5, giao diện và sổ cái nghiên cứu — có thành phần đáng thử tái sử dụng | **Repo nguồn PRIVATE.** Báo cáo công khai; quyền dữ liệu, locator, tra cứu vét hết và cơ chế `VERIFIED/SUPPORTED` còn là chốt chặn. **TRIAL ONLY**, chưa chạy lại độc lập |
| **P02 — [QMD (tobi/qmd)](REPORT_02_QMD_TOBI_QMD.md)** | **T4A** · Retrieval mở rộng | Tìm ứng viên nhanh trong nội dung Markdown bằng BM25; có hybrid/vector và giao tiếp với AI | Kết quả/chunk không phải tất cả vị trí nguyên văn, không giữ PDF bbox/EPUB CFI; chưa POC |
| **P01 — [RAGFlow](REPORT_01_RAGFLOW.md)** | **T2, T4A** · RAG | Nạp/chia đoạn, tìm kiếm hybrid, cung cấp ngữ cảnh cho AI, wiki/biên soạn tri thức tùy chọn | Citation gắn chunk chưa tương đương xác minh nguồn, ấn bản và mọi occurrence; chưa POC |
| **P04 — [Karpathy LLM Wiki / Second Brain](REPORT_04_KARPATHY_LLM_WIKI_SECOND_BRAIN_PATTERN.md)** | **T4B** · Tích lũy | Ý tưởng lưu wiki, ghi chú, liên kết và tri thức nghiên cứu để sử dụng lại lâu dài | Đây là **mẫu tư duy/idea file**, không phải sản phẩm có thể cài sẵn; ghi chú AI không trở thành chứng cứ đã duyệt; chưa POC |

**Tầng 5 — Giao diện nghiên cứu:** chưa có báo cáo chuyên biệt chứng minh một giải pháp đã đáp ứng trọn **phiếu truy nguyên nguồn** của BodhiAtlas. Giao diện đọc/tìm của các sản phẩm có thể là thành phần tham khảo, không thay cho Citation Checker.

**Khuyến nghị trong các báo cáo:** P01–P06, P12 và P20 đề xuất **USE AS COMPONENT** trong vai trò tương ứng; P39 đề xuất **TRIAL ONLY**. Đó là **ý kiến nghiên cứu**, không phải đã chọn để triển khai hay được nghiệm thu.

## 2. Những kết luận đã rõ và những việc chưa được chứng minh

- **Có thể khảo sát để tái sử dụng:** quản lý thư mục/ebook (Zotero, Calibre); trích xuất (Docling); tra cứu mã nguồn và corpus (SQLite FTS5, BuddhismDocuments-for-AI, một phần Bang-ha-giac-ngo); retrieval nâng cao (QMD, RAGFlow); ghi chú tích lũy (Second Brain).
- **Không được coi là đã giải quyết:** nguyên văn bất biến; ánh xạ chắc chắn tới trang in/PDF bbox/EPUB CFI; EXACT trả đủ mọi lần xuất hiện; chất lượng OCR đa ngữ; nghĩa thuật ngữ được kiểm chứng; đánh giá nguồn hỗ trợ hay phản bác luận điểm.
- **Chưa có cơ sở chọn stack cuối cùng:** nhiều báo cáo dựa trên đọc mã và tài liệu, **không có POC end-to-end trên kho sách thật của BodhiAtlas**. Kết quả `TESTED` của P20 chỉ áp dụng cho fixture/phiên bản đã chạy được báo cáo mô tả.

**Quy trình ra quyết định:** xác định năng lực cần đạt → chọn đúng nhóm ứng viên → chạy POC với nguồn/phiên bản đã ghim và bộ thử độc lập → rà quality gates **G1–G6** → ghi quyết định riêng có người phê duyệt. Không biến điểm tìm kiếm cao hoặc lời giải thích thuyết phục thành chứng cứ học thuật.

## 3. Cách đọc và cập nhật các hồ sơ

- **Xem chi tiết:** nhấn tên trong bảng, đọc phần *Executive Decision*, *Sources & Evidence Ledger*, *Feature Fit–Gap*, *POC plan* và *Open Questions* của từng báo cáo.
- **Bổ sung nghiên cứu mới:** dùng [mẫu báo cáo](REPORT_TEMPLATE.md), giữ mã `Pxx` và tên gốc, ghi **ngày khảo sát, phiên bản/tag/commit, phạm vi đọc, trạng thái kiểm thử**; sau đó thêm một dòng vào bảng.
- **Chuẩn chứng cứ:** `DOC` = đã đọc tài liệu; `CODE` = đã đọc mã; `TESTED` = tự chạy có log; `ISSUE` = lỗi do bên khác báo; `INFERRED` = suy luận có căn cứ; `UNKNOWN` = chưa xác minh. Không tự nâng mức `CODE` thành `TESTED`.
- **Lịch sử nghiên cứu:** không ghi đè âm thầm kết luận cũ. Khi có POC hoặc phiên bản mới, ghi rõ ngày, khác biệt và căn cứ; Git giữ lịch sử của bản trước.

### Ghi chú về nguồn riêng tư P39

Repo [`quoctran-2608/Bang-ha-giac-ngo`](https://github.com/quoctran-2608/Bang-ha-giac-ngo) là **PRIVATE** tại thời điểm khảo sát 16/11/2026; các liên kết mã nguồn trong P39 có thể chỉ mở được với người được cấp quyền. **Chính báo cáo P39 đặt trong `bodhi-atlas` công khai nên báo cáo này là PUBLIC**, theo yêu cầu công bố của chủ dự án. Nhãn `PRIVATE` chỉ mô tả quyền truy cập **repo nguồn**, không bảo mật nội dung báo cáo.

> **Nguyên tắc chung:** Thư mục này là **hồ sơ thẩm định**, không phải danh sách công nghệ đã được phê duyệt. Công nghệ được đánh giá theo chứng cứ và vai trò thực tế, luôn đặt yêu cầu nguồn gốc và kiểm chứng học thuật của BodhiAtlas lên trước.
