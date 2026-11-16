# Danh mục nghiên cứu và thẩm định công nghệ

**Ngày lập danh mục:** 16/11/2026  
**Đợt nhập ban đầu:** Các báo cáo có ngày khảo sát 16/11/2026  
**Trạng thái:** Tập hợp hồ sơ nghiên cứu; **chưa phải danh mục công nghệ đã chọn**  
**Tài liệu đối chiếu:** [PRD v1.4](../../docs/PRD.md) · [V1 Core Foundation](../../docs/V1_CORE_FOUNDATION.md) · [Rủi ro và kiểm chứng học thuật](../../docs/ACADEMIC_RISKS_AND_VERIFICATION.md)

## 1. Danh mục báo cáo đã lưu

Mã **P** được **giữ nguyên theo mã trong báo cáo gốc**, không đánh số lại; các khoảng trống trong dãy mã không hàm ý đã thất lạc tài liệu.

| Mã | Đối tượng | Vai trò được khảo sát trong BodhiAtlas | Khuyến nghị *trong báo cáo* | Tình trạng thực nghiệm ghi nhận |
|---|---|---|---|---|
| **P01** | [RAGFlow](REPORT_01_RAGFLOW.md) | Nạp/chia đoạn, RAG và truy xuất nâng cao tùy chọn | USE AS COMPONENT | Chưa chạy POC trong báo cáo |
| **P02** | [QMD (tobi/qmd)](REPORT_02_QMD_TOBI_QMD.md) | Tìm nguồn ứng viên, lexical/hybrid/semantic | USE AS COMPONENT | Chưa chạy POC trong báo cáo |
| **P03** | [BuddhismDocuments-for-AI](REPORT_03_BUDDHISMDOCUMENTS_FOR_AI.md) | Corpus Phật học có cấu trúc, retrieval và kiểm chứng nguồn | USE AS COMPONENT | Chưa tái chạy test độc lập trong báo cáo |
| **P04** | [Karpathy LLM Wiki / Second Brain pattern](REPORT_04_KARPATHY_LLM_WIKI_SECOND_BRAIN_PATTERN.md) | Mô hình tích lũy ghi chú/tri thức, không phải phần mềm hoàn chỉnh | USE AS COMPONENT (pattern) | Chưa chạy pipeline thực nghiệm |
| **P05** | [Zotero](REPORT_05_ZOTERO.md) | Quản trị thư mục và trích dẫn, công cụ kết nối | USE AS COMPONENT | Chưa chạy POC trong báo cáo |
| **P06** | [Calibre](REPORT_06_CALIBRE.md) | Quản lý, chuyển đổi và đọc ebook | USE AS COMPONENT | Chưa chạy POC trong báo cáo |
| **P12** | [Docling](REPORT_12_DOCLING.md) | Trích xuất/OCR, cấu trúc và vị trí tài liệu | USE AS COMPONENT | Chưa chạy POC trong báo cáo |
| **P20** | [SQLite FTS5 / trigram](REPORT_20_SQLITE_FTS5_TRIGRAM.md) | Chỉ mục tìm kiếm bằng code | USE AS COMPONENT | Có thử nghiệm trên *fixture tổng hợp*; chưa nghiệm thu corpus thật |

**Lưu ý:** Các kết luận trên được tóm lược từ chính báo cáo đính kèm, không phải kết quả đối chiếu lại phiên bản mới ở thời điểm mở danh mục. `USE AS COMPONENT` **không đồng nghĩa đã được tích hợp hay phê duyệt**. Các báo cáo nhận diện năng lực, rủi ro và khoảng trống trong **đúng vai trò** của từng đối tượng; không nên dùng bảng này để chấm điểm xếp hạng tổng thể.

## 2. Cách sử dụng các nghiên cứu

- **Muốn hiểu ứng viên:** mở báo cáo, đọc *Executive Decision*, phạm vi chứng cứ và giới hạn trước khi xem phần đề xuất.
- **Muốn so sánh:** so trong cùng một nhiệm vụ (ví dụ ingest/provenance hoặc deterministic retrieval); không coi người quản lý thư mục là đối thủ trực tiếp của OCR/parser.
- **Muốn chọn công nghệ:** chỉ sau khi tạo bộ kiểm thử dùng chung, ghi rõ bản chạy, corpus, log, kết quả âm tính giả/dương tính giả, chi phí, quyền sử dụng và cổng G1–G6.
- **Muốn nghiên cứu thêm:** dùng [mẫu báo cáo](REPORT_TEMPLATE.md), ghi mã mới và bổ sung dòng vào danh mục; không sửa kết luận của bài cũ để tạo vẻ đồng thuận.

## 3. Chuẩn chứng cứ và mức quyết định

| Nhãn | Ý nghĩa |
|---|---|
| `DOC` | Tài liệu, mô tả, hướng dẫn hoặc thông tin phát hành đã đọc |
| `CODE` | Mã nguồn/schema/test *đã đọc*, không nhất thiết đã chạy |
| `TESTED` | Người thẩm định *tự chạy*, lưu môi trường, dữ liệu, log và kết quả |
| `ISSUE` | Báo cáo lỗi/hồ sơ sự cố; không mặc định đã tái hiện |
| `INFERRED` | Suy luận có chỉ rõ bằng chứng và điều kiện |
| `UNKNOWN` | Chưa tiếp cận hoặc chưa chứng minh được |

**Tách 3 việc:** (1) báo cáo *đề xuất*; (2) thí nghiệm *chứng minh trong phạm vi nào*; (3) nhóm dự án *quyết định* có sử dụng hay không. Một `TESTED` với dữ liệu giả lập không tương đương nghiệm thu corpus Phật học thực tế.

## 4. Quy tắc duy trì

1. **Giữ nguyên file gốc và mã P**, cùng các dẫn chiếu ghim commit/phiên bản có sẵn.
2. Thêm báo cáo theo tên `REPORT_<MÃ>_<TÊN>.md`; ngày khảo sát nằm ngay đầu báo cáo.
3. Khi có kết quả POC mới, ghi riêng ngày, môi trường, đầu vào, log, sai số, giới hạn và phiên bản; không gọi lại bằng chứng `DOC` thành `TESTED`.
4. Nếu đánh giá thay đổi, nêu **điều gì thay đổi** và lý do; giữ lịch sử Git.
5. **Không công khai** các báo cáo chứa tài liệu private hoặc chi tiết không được phép phát hành. Để ở kho riêng có quyền truy cập phù hợp.

**Mục đích của kho nghiên cứu:** hỗ trợ lựa chọn cẩn trọng dựa trên chứng cứ, không chốt sớm một sản phẩm rồi diễn giải các dữ kiện theo kết luận có trước.
