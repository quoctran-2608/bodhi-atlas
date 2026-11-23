# BodhiAtlas — Bản đồ nghiên cứu công nghệ và nguồn dữ liệu

> **Mục đích:** Giúp người đọc hiểu nhanh **mỗi công nghệ/repository là gì, giải quyết phần nào của BodhiAtlas, giới hạn đáng kiểm tra ở đâu** và tìm đúng báo cáo để đọc sâu. Đây là tài liệu dẫn đường phục vụ lựa chọn kiến trúc, **không phải bảng xếp hạng hoặc quyết định chọn stack**.
>
> **Ngày cập nhật:** 23/11/2026 (Asia/Ho_Chi_Minh) · **56 đề tài** · **25 báo cáo đã có trên GitHub** · **31 đề tài chưa có báo cáo tại đường dẫn này**.
>
> **Trạng thái biên soạn:** Bản tổng quan dựa trên danh mục P01–P55 cùng P57 và yêu cầu BodhiAtlas V1.4. **Đã đối chiếu sự tồn tại của tệp báo cáo và đường dẫn nội bộ với nhánh `main` ngày 23/11/2026**, nhưng chưa thẩm định lại toàn bộ phát hiện trong từng báo cáo; phần tóm tắt nhằm dẫn đường, không thay cho kết quả thực nghiệm. Mục chưa có báo cáo được ghi rõ thay vì tạo liên kết hỏng.

## BodhiAtlas đang tìm lời giải cho điều gì?

BodhiAtlas không phải chỉ là “chat với PDF”. Đích đến là một thư viện nghiên cứu có thể **nạp PDF/EPUB/DOCX/Markdown và corpus học thuật; giữ file gốc bất biến; trích xuất có cấu trúc, có trạng thái OCR; tìm nguyên văn/biến thể bằng code; mở lại đúng trang/đoạn/ấn bản; và trình bày phiếu truy nguyên nguồn**. RAG, wiki và AI Research là lớp hỗ trợ tìm nguồn, tích lũy tri thức và phân tích; không được thay thế bằng chứng gốc.

**Tách bốn điều:**

- **Quản lý tài liệu:** Sách nào, ấn bản nào, file nào, quyền truy cập gì?
- **Tiêu hóa tài liệu:** Văn bản nào đã đọc được, mức tin cậy ra sao, tọa độ nguồn ở đâu?
- **Tìm và xác minh:** Chuỗi chữ/thuật ngữ/đoạn nào khớp, kiểu khớp gì, có mở lại đúng nguồn không?
- **Phân tích và tích lũy:** Tác giả lập luận thế nào, có phản chứng không, nhận định nào đã được người nghiên cứu xác nhận?

Một công cụ có thể bao phủ nhiều tầng; vì vậy **56 mục bên dưới không phải 56 thành phần phải cài**.

## Chọn đọc theo vấn đề

| Nếu bạn muốn... | Hãy xem trước |
|---|---|
| Nạp sách và OCR tự động | P44 Paperless-ngx, P01 RAGFlow; P12 Docling, P45 MinerU, P46 Marker, P53 Xberg/Kreuzberg |
| Tìm `anatta`/`anattā` và biến thể chính xác không LLM | P20 SQLite FTS5, P21 OpenSearch, P22 PostgreSQL; P43 DPD, P31 OpenCC, P32 pyewts |
| Tìm đoạn rồi **mở lại đúng vị trí gốc** | P13 PyMuPDF, P34 IIIF, P35 Mirador, P36 EPUB CFI, P33 TEI |
| Kế thừa corpus Phật học đã số hóa | P03 BuddhismDocuments, P40 FoJin, P41 Dharmamitra, P26 Bilara, P28 CBETA, P29 84000, P51 BDRC |
| Đối chiếu song hành/dị bản, phân biệt nguồn | P27 sc-data, P42 MITRA, P48 CollateX, P49 passim, P33 TEI |
| Quản lý sách, tác giả, trích dẫn, xuất bản | P05 Zotero, P06 Calibre, P07 Islandora, P08 Omeka S, P10 InvenioRDM, P11 DSpace; **P57 book-memex** (thư viện eBook và reader) |
| Thêm RAG, semantic search, Second Brain | P01 RAGFlow, P02 QMD, P04 LLM Wiki, P54 Open WebUI |

## Cách đọc bằng chứng trong các báo cáo

- **`[DOC]`**: Nhà phát triển công bố; **`[CODE]`**: Đã thấy trong mã nguồn; **`[TESTED]`**: Đã chạy kiểm nghiệm trên đối tượng thực có log; **`[TESTED-ISOLATED]`**: Đã chạy phép thử cô lập/mô phỏng, không phải kiểm thử upstream; **`[INFERRED]`**: Suy luận; **`[UNKNOWN]`**: Chưa rõ. `TESTED` không được gán chỉ vì repo có file test.
- Phân biệt `EXACT` (đúng chuỗi nguyên văn), `NORMALIZED`, `FUZZY`, `LEXICON`, `SEMANTIC`. **Điểm gần nghĩa không chứng minh một nhận định đúng**.
- Khi đọc một kết quả, luôn hỏi: đã có **file ID, ấn bản, checksum, trang/đoạn và cách đối chiếu** chưa? OCR/chunk/RAG có thể bỏ sót hoặc thêm sai chữ.
- Đánh giá giấy phép riêng cho **mã nguồn, model và corpus/ảnh/bản dịch**. Repo mở không đồng nghĩa toàn bộ nội dung được phép tái phân phối.
- Mỗi mục trong danh mục sau chỉ là **ứng viên/tài nguyên tham khảo**; chỉ chọn sau khi có kiểm thử với corpus BodhiAtlas.

## Danh mục 56 đề tài

Các nhóm xếp theo **vai trò sử dụng**, không phải xếp hạng tốt–xấu. Một số mục là phương pháp/chuẩn hoặc bộ dữ liệu, không phải ứng dụng có thể cài độc lập.

### 01. Nền tảng tra cứu, RAG và Second Brain

Nhóm có thể giải quyết đồng thời nhiều chức năng. Cần phân biệt nền tảng tìm kiếm/AI với hệ thống kiểm chứng học thuật.

**P01 · [RAGFlow](https://github.com/infiniflow/ragflow)** · [Đọc báo cáo](REPORT_01_RAGFLOW.md)  
**Là gì:** Nền tảng RAG tích hợp: tiếp nhận tài liệu, chia đoạn, truy xuất và hỏi đáp, có các cơ chế tạo tri thức phái sinh.  
**BodhiAtlas cần kiểm:** Thử làm “bộ tiêu hóa + tìm nguồn ứng viên”; kiểm tra khả năng giữ nguyên văn, trang và khả năng tắt LLM.

**P02 · [QMD (tobi/qmd)](https://github.com/tobi/qmd)** · [Đọc báo cáo](REPORT_02_QMD_TOBI_QMD.md)  
**Là gì:** Máy tìm kiếm tài liệu cục bộ kết hợp truy vấn từ khóa, vector và xếp hạng; có đường tích hợp cho AI.  
**BodhiAtlas cần kiểm:** Thử tầng retrieval gọn nhẹ; không mặc định BM25/phrase search là tìm đúng mọi vị trí ký tự.

**P03 · [BuddhismDocuments-for-AI](https://github.com/quoctran-2608/BuddhismDocuments-for-AI)** · [Đọc báo cáo](REPORT_03_BUDDHISMDOCUMENTS_FOR_AI.md)  
**Là gì:** Công cụ corpus Phật học và truy nguyên chứng cứ do chủ dự án phát triển, gồm nguồn được ghim phiên bản và truy vấn chuyên ngành.  
**BodhiAtlas cần kiểm:** Ưu tiên kiểm kê phần đã có thể kế thừa; phân biệt test phần mềm với thẩm định học thuật.

**P04 · [Karpathy LLM Wiki / Second Brain pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** · [Đọc báo cáo](REPORT_04_KARPATHY_LLM_WIKI_SECOND_BRAIN_PATTERN.md)  
**Là gì:** Phương pháp “LLM Wiki/Second Brain”: dùng AI duy trì các trang kiến thức liên kết và tích lũy theo thời gian; không phải một search engine hoàn chỉnh.  
**BodhiAtlas cần kiểm:** Nghiên cứu lớp ghi chú phái sinh; tuyệt đối không dùng wiki do AI viết thay nguyên văn nguồn.

**P40 · [FoJin](https://github.com/xr843/fojin)** · [Đọc báo cáo](REPORT_40_FOJIN.md)  
**Là gì:** Ứng viên nền tảng Phật học tích hợp corpus đa ngôn ngữ, tìm kiếm, RAG và kiểm tra câu trích theo công bố.  
**BodhiAtlas cần kiểm:** Cần thẩm định sâu endpoint xác minh, nguồn dữ liệu, khả năng thêm sách và độ tin cậy học thuật.

**P41 · [Dharmamitra / DharmaNexus ecosystem](https://github.com/dharmamitra)** · [Đọc báo cáo](REPORT_41_DHARMAMITRA_DHARMANEXUS.md)  
**Là gì:** Hệ sinh thái xử lý và nghiên cứu văn bản Phật học nhiều ngôn ngữ, bao gồm công cụ và dữ liệu.  
**BodhiAtlas cần kiểm:** Xem xét sử dụng module/corpus chuyên ngành thay tự xây; so với FoJin và BuddhismDocuments.

**P54 · [Open WebUI Knowledge](https://github.com/open-webui/open-webui)** · *Chưa có báo cáo trong repo*  
**Là gì:** Giao diện tương tác AI có chức năng knowledge và truy vấn tài liệu.  
**BodhiAtlas cần kiểm:** Ứng viên UI/AI layer; không được trao nhiệm vụ xác thực trích dẫn học thuật cho chatbot.


### 02. Quản lý thư viện, tư liệu và quy trình số hóa

Nhóm quản lý “sách nào, ấn bản nào, file nào, quyền nào”; không mặc nhiên giải quyết tìm EXACT theo ký tự.

**P05 · [Zotero](https://github.com/zotero/zotero)** · [Đọc báo cáo](REPORT_05_ZOTERO.md)  
**Là gì:** Phần mềm quản lý tài liệu tham khảo, trích dẫn, metadata và thư viện nghiên cứu.  
**BodhiAtlas cần kiểm:** Ứng viên quản lý tác giả/ấn bản và xuất danh mục; cần adapter nối tới kho nội dung đã đánh chỉ mục.

**P06 · [Calibre](https://github.com/kovidgoyal/calibre)** · [Đọc báo cáo](REPORT_06_CALIBRE.md)  
**Là gì:** Phần mềm quản lý, đọc và chuyển đổi ebook, đặc biệt hữu ích khi có nhiều EPUB.  
**BodhiAtlas cần kiểm:** Ứng viên quản lý sách cá nhân và chuyển định dạng; kiểm tra khả năng quản trị học thuật, định danh và API.

**P07 · [Islandora](https://github.com/Islandora/islandora)** · *Chưa có báo cáo trong repo*  
**Là gì:** Nền tảng thư viện số trên hệ sinh thái Drupal, thiên về bộ sưu tập, tư liệu số và khả năng hiển thị.  
**BodhiAtlas cần kiểm:** Xem xét thay cụm quản lý tư liệu và viewer; cân nhắc công sức vận hành, cấu hình và tích hợp.

**P08 · [Omeka S](https://github.com/omeka/omeka-s)** · *Chưa có báo cáo trong repo*  
**Là gì:** Nền tảng xuất bản bộ sưu tập có cấu trúc metadata và quan hệ giữa các tài nguyên.  
**BodhiAtlas cần kiểm:** Phù hợp cho hiện vật, ảnh, tư liệu liên ngành; chưa mặc định giải được exact search trong sách.

**P09 · [Goobi workflow](https://github.com/intranda/goobi-workflow)** · *Chưa có báo cáo trong repo*  
**Là gì:** Hệ thống điều phối quy trình số hóa, OCR, metadata, kiểm soát chất lượng và xuất bản tài liệu.  
**BodhiAtlas cần kiểm:** Thử làm pipeline số hóa quy mô lớn; cân đối độ phức tạp với nhu cầu của một nhóm nghiên cứu nhỏ.

**P10 · [InvenioRDM](https://inveniordm.docs.cern.ch/)** · *Chưa có báo cáo trong repo*  
**Là gì:** Hệ thống kho dữ liệu nghiên cứu, quản lý record, file, metadata và quyền truy cập.  
**BodhiAtlas cần kiểm:** Ứng viên kho lâu dài; cần kiểm tra mức độ tùy biến cho sách nhiều ấn bản và text-level provenance.

**P11 · [DSpace](https://github.com/DSpace/DSpace)** · *Chưa có báo cáo trong repo*  
**Là gì:** Nền tảng kho lưu trữ học thuật và tổ chức số, mạnh về metadata, phát hành và chính sách truy cập.  
**BodhiAtlas cần kiểm:** Thử làm backend quản lý tư liệu; kiểm tra giới hạn về tìm kiếm đa ngôn ngữ ở cấp đoạn.

**P44 · [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)** · [Đọc báo cáo](REPORT_44_PAPERLESS_NGX.md)  
**Là gì:** Phần mềm lưu trữ, OCR, gắn metadata và tìm kiếm tài liệu có giao diện web.  
**BodhiAtlas cần kiểm:** Ứng viên thay cụm quản lý file và ingest; cần kiểm thư viện EPUB, ấn bản và source locator.


**P57 · [book-memex](https://github.com/queelius/book-memex)** · [Đọc báo cáo](REPORT_57_BOOK_MEMEX.md) · [Mã và log thử nghiệm cô lập](reproduction/P57/README.md)  
**Là gì:** Thư viện ebook cá nhân có quản lý file SHA-256, đọc PDF/EPUB, tìm kiếm SQLite FTS5, ghi chú và cổng REST/MCP, không bắt buộc sử dụng LLM.  
**Giá trị với BodhiAtlas:** `USE AS COMPONENT` **có điều kiện** — tham khảo mô hình lưu file theo hash, FTS candidate, registry extractor và giao diện reader; báo cáo **ưu tiên phương án D — Minimal BodhiAtlas Evidence Core**, không fork cả repo làm lõi nguồn có thẩm quyền.  
**Giới hạn cần kiểm:** Chưa có hợp đồng đầy đủ về ấn bản/file/revision, exhaustive EXACT, locator chính xác và citation verifier độc lập. Có 30 mục chứng cứ, Fit–Gap C01–C15, POC cô lập SQLite/PDF và kế hoạch TC01–TC15; **upstream tests và POC tích hợp chưa chạy**. Kiến trúc đề xuất có thể đảo nếu kiểm nghiệm thực chứng minh phương án khác đạt G1/G2 với rủi ro/chi phí thấp hơn.

### 03. Tiêu hóa tài liệu, OCR và bố cục

Nhóm biến file thành văn bản cấu trúc. Thước đo là fidelity, thứ tự đọc, source map và báo lỗi — không chỉ chất lượng Markdown đẹp.

**P12 · [Docling](https://github.com/docling-project/docling)** · [Đọc báo cáo](REPORT_12_DOCLING.md)  
**Là gì:** Công cụ phân tích cấu trúc tài liệu và chuyển đổi nhiều định dạng sang dữ liệu có tổ chức.  
**BodhiAtlas cần kiểm:** Benchmark vị trí trang, thứ tự đọc, bảng/cước chú và PDF có nhiều cột trước khi chọn.

**P13 · [PyMuPDF](https://github.com/pymupdf/PyMuPDF)** · *Chưa có báo cáo trong repo*  
**Là gì:** Thư viện làm việc với PDF: trích xuất chữ, hình học trang và vùng chữ; có khả năng hiển thị/xử lý PDF.  
**BodhiAtlas cần kiểm:** Ứng viên source map cho PDF văn bản; OCR hoặc bố cục scan vẫn phải được xử lý riêng.

**P14 · [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF)** · *Chưa có báo cáo trong repo*  
**Là gì:** Pipeline bổ sung OCR text layer cho PDF scan và giữ PDF có thể tìm kiếm.  
**BodhiAtlas cần kiểm:** Thử cho nhánh PDF scan; phân biệt lớp chữ OCR với câu chữ đã được kiểm chứng.

**P15 · [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** · *Chưa có báo cáo trong repo*  
**Là gì:** OCR engine lâu đời, hỗ trợ nhiều ngôn ngữ qua mô hình huấn luyện.  
**BodhiAtlas cần kiểm:** Đối chứng chi phí thấp cho scan phổ thông; kiểm riêng Hán/Tạng, chữ cổ và dấu phụ.

**P16 · [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)** · *Chưa có báo cáo trong repo*  
**Là gì:** Bộ công cụ OCR và phân tích cấu trúc tài liệu dựa trên mô hình học máy.  
**BodhiAtlas cần kiểm:** Thử khi scan/bảng/bố cục phức tạp; so CER, đọc đúng thứ tự cột và chi phí chạy.

**P17 · [Surya OCR](https://github.com/datalab-to/surya)** · *Chưa có báo cáo trong repo*  
**Là gì:** Công cụ OCR, phát hiện bố cục và thứ tự đọc cho trang tài liệu.  
**BodhiAtlas cần kiểm:** Đặt cạnh Docling/PaddleOCR trong benchmark cùng trang; chú ý license của model và bbox.

**P18 · [Apache Tika](https://github.com/apache/tika)** · *Chưa có báo cáo trong repo*  
**Là gì:** Thư viện phát hiện định dạng, trích văn bản và metadata từ nhiều loại file.  
**BodhiAtlas cần kiểm:** Ứng viên “cổng vào” cho ingest; không coi output văn bản tuyến tính là source map đủ chính xác.

**P19 · [eScriptorium](https://escriptorium.eu/)** · *Chưa có báo cáo trong repo*  
**Là gì:** Nền tảng làm việc với bản thảo và tài liệu lịch sử, hỗ trợ nhận dạng chữ và hiệu đính có người tham gia.  
**BodhiAtlas cần kiểm:** Phù hợp tư liệu cổ khó OCR; cân nhắc khi nguồn cần huấn luyện/biên tập chứ không phải ingest đại trà.

**P45 · [MinerU](https://github.com/opendatalab/MinerU)** · [Đọc báo cáo](REPORT_45_MINERU.md)  
**Là gì:** Công cụ đọc/khôi phục cấu trúc PDF phức tạp để tạo Markdown/JSON và dữ liệu cho RAG.  
**BodhiAtlas cần kiểm:** Benchmark trên scan sách Phật học; đặc biệt lỗi xuống dòng, cột, cước chú và tọa độ chữ.

**P46 · [Marker (datalab-to/marker)](https://github.com/datalab-to/marker)** · [Đọc báo cáo](REPORT_46_MARKER_DATALAB.md)  
**Là gì:** Bộ chuyển đổi tài liệu thành Markdown/JSON/chunk cho tìm kiếm và AI.  
**BodhiAtlas cần kiểm:** So với Docling/MinerU về độ trung thực chữ, cấu trúc và mức mất thông tin trang.

**P47 · [GROBID](https://github.com/grobidOrg/grobid)** · [Đọc báo cáo](REPORT_47_GROBID.md)  
**Là gì:** Công cụ trích xuất cấu trúc bài nghiên cứu, metadata, trích dẫn và tài liệu tham khảo sang định dạng học thuật.  
**BodhiAtlas cần kiểm:** Rất phù hợp bài báo; cần kiểm hiệu quả trên sách/kinh dài và nguồn không theo layout học thuật hiện đại.

**P52 · [olmOCR](https://github.com/allenai/olmocr)** · [Đọc báo cáo](REPORT_52_OLMOCR.md)  
**Là gì:** OCR hướng đến tài liệu phức tạp, đi kèm phương pháp đánh giá đầu ra.  
**BodhiAtlas cần kiểm:** Đối chứng trong benchmark parser/OCR; chú ý tính trung thực với chữ nguồn và chi phí compute.

**P53 · [Xberg / Kreuzberg (xberg-io)](https://github.com/xberg-io/xberg)** · [Đọc báo cáo](REPORT_53_XBERG_KREUZBERG.md)  
**Là gì:** Framework thống nhất trích xuất nội dung từ nhiều định dạng, mở rộng bằng bộ xử lý khác.  
**BodhiAtlas cần kiểm:** Ứng viên ingest ít thành phần; kiểm giữ layout và source map chứ không chỉ có text.


### 04. Tìm kiếm code-only và search engine

Nhóm tạo chỉ mục, tìm ứng viên và tìm gần đúng. Cần thêm bộ xác minh nguyên văn độc lập với engine.

**P20 · [SQLite FTS5 / trigram](https://www.sqlite.org/fts5.html)** · [Đọc báo cáo](REPORT_20_SQLITE_FTS5_TRIGRAM.md)  
**Là gì:** Công cụ full-text bên trong SQLite, có các tokenizer và lựa chọn trigram.  
**BodhiAtlas cần kiểm:** Ứng viên code-only tối giản; cần thử chuỗi dài, chữ Hán ngắn, nhiều lần xuất hiện và offset chính xác.

**P21 · [OpenSearch](https://github.com/opensearch-project/OpenSearch)** · *Chưa có báo cáo trong repo*  
**Là gì:** Search engine phục vụ index lớn, nhiều analyzer, truy vấn từ khóa và mở rộng retrieval.  
**BodhiAtlas cần kiểm:** Ứng viên cho corpus lớn đa ngôn ngữ; đối chiếu lợi ích với chi phí triển khai/duy trì.

**P22 · [PostgreSQL FTS + pg_trgm](https://www.postgresql.org/docs/current/textsearch.html)** · *Chưa có báo cáo trong repo*  
**Là gì:** Tìm kiếm toàn văn PostgreSQL kết hợp mở rộng trigram cho so khớp chuỗi gần đúng.  
**BodhiAtlas cần kiểm:** Thử mô hình một database + search trước khi bổ sung dịch vụ riêng.

**P23 · [Meilisearch](https://github.com/meilisearch/meilisearch)** · *Chưa có báo cáo trong repo*  
**Là gì:** Search engine hướng đến trải nghiệm tìm kiếm đơn giản và có dung sai lỗi gõ.  
**BodhiAtlas cần kiểm:** Thử độ dễ dùng và fuzzy; kiểm nghiêm ngặt semantics EXACT, Unicode và vị trí nguồn.

**P24 · [Typesense](https://github.com/typesense/typesense)** · *Chưa có báo cáo trong repo*  
**Là gì:** Search engine thiết kế để tìm nhanh với bộ lọc và typo tolerance.  
**BodhiAtlas cần kiểm:** So sánh cùng Meilisearch/OpenSearch; không suy từ tốc độ UI sang khả năng xác minh trích dẫn.


### 05. Corpus, từ điển và tài nguyên Phật học

Nhóm cung cấp dữ liệu và quan hệ đã có. “Có văn bản điện tử” không có nghĩa được phép phân phối tự do hoặc mọi liên kết đều đã xác minh.

**P25 · [SuttaCentral Bilara application](https://github.com/suttacentral/bilara)** · *Chưa có báo cáo trong repo*  
**Là gì:** Ứng dụng phục vụ biên dịch và biên tập văn bản Phật học theo các đoạn có định danh.  
**BodhiAtlas cần kiểm:** Nghiên cứu cách thiết kế quy trình dịch thuật/định danh; phân biệt ứng dụng với kho dữ liệu Bilara.

**P26 · [SuttaCentral bilara-data](https://github.com/suttacentral/bilara-data)** · *Chưa có báo cáo trong repo*  
**Là gì:** Kho corpus nguyên văn, dịch thuật và ghi chú có khóa đoạn ổn định của hệ sinh thái SuttaCentral.  
**BodhiAtlas cần kiểm:** Nguồn có thể nhập thẳng thành corpus cấu trúc; kiểm giấy phép và ánh xạ đoạn–ấn bản.

**P27 · [SuttaCentral sc-data](https://github.com/suttacentral/sc-data)** · *Chưa có báo cáo trong repo*  
**Là gì:** Kho metadata, cấu trúc kinh và các quan hệ văn bản trong hệ sinh thái SuttaCentral.  
**BodhiAtlas cần kiểm:** Ứng viên đồ thị quan hệ kinh song hành; phải bảo toàn nguồn xác nhận và trạng thái quan hệ.

**P28 · [CBETA XML P5](https://github.com/cbeta-org/xml-p5)** · *Chưa có báo cáo trong repo*  
**Là gì:** Kho kinh điển Hán dạng XML/TEI P5, có cấu trúc phù hợp tra cứu văn bản.  
**BodhiAtlas cần kiểm:** Ưu tiên tận dụng văn bản điện tử thay OCR lại; kiểm định danh, dị bản và điều kiện dùng dữ liệu.

**P29 · [84000 Tibetan corpus / data-tei](https://github.com/84000/data-tei)** · *Chưa có báo cáo trong repo*  
**Là gì:** Nguồn corpus và bản dịch Tạng từ hệ sinh thái 84000, có những đầu ra cấu trúc.  
**BodhiAtlas cần kiểm:** Ứng viên phục vụ tìm Tạng và đối chiếu dịch; kiểm mức mở dữ liệu, quyền và granularity.

**P30 · [OpenPecha ecosystem](https://github.com/OpenPecha)** · *Chưa có báo cáo trong repo*  
**Là gì:** Hệ sinh thái quản lý văn bản Tạng và các tầng dữ liệu có cấu trúc.  
**BodhiAtlas cần kiểm:** Nghiên cứu mô hình chữ Tạng, bản chép, căn chỉnh và nguồn gốc, không coi là ứng dụng all-in-one.

**P39 · [Bang-ha-giac-ngo](https://github.com/quoctran-2608/Bang-ha-giac-ngo)** · [Đọc báo cáo](REPORT_39_BANG_HA_GIAC_NGO.md)  
**Là gì:** Repository do chủ dự án cung cấp; vai trò thực tế cần được xác minh từ nội dung repo.  
**BodhiAtlas cần kiểm:** Không phân loại hoặc suy đoán chức năng khi chưa đọc được source và giấy phép.

**P42 · [MITRA-parallel](https://github.com/dharmamitra/mitra-parallel)** · [Đọc báo cáo](REPORT_42_MITRA_PARALLEL.md)  
**Là gì:** Dataset các cặp đoạn văn Phật học được căn chỉnh qua ngôn ngữ.  
**BodhiAtlas cần kiểm:** Nguồn ứng viên cho tra cứu song hành; quan hệ do thuật toán gợi ý không mặc nhiên đã duyệt.

**P43 · [Digital Pāḷi Dictionary (DPD)](https://github.com/digitalpalidictionary/dpd-db)** · [Đọc báo cáo](REPORT_43_DIGITAL_PALI_DICTIONARY_DPD.md)  
**Là gì:** Từ điển Pāli dạng dữ liệu, với thông tin mục từ và hình thái ngôn ngữ.  
**BodhiAtlas cần kiểm:** Rất đáng thử cho anatta/anattā và dạng biến tố bằng code; kiểm nghĩa, license, API và độ phủ.

**P51 · [BDRC / BUDA archive and data ecosystem](https://github.com/buda-base)** · [Đọc báo cáo](REPORT_51_BUDA_BDRC.md)  
**Là gì:** Hệ sinh thái tư liệu Phật học, metadata, ảnh bản thảo và định danh nguồn.  
**BodhiAtlas cần kiểm:** Ưu tiên khảo sát tài nguyên và khả năng truy nguyên; tách quyền sử dụng data/ảnh và code.

**P55 · [BuddhaNexus legacy](https://github.com/BuddhaNexus)** · [Đọc báo cáo](REPORT_55_BUDDHANEXUS_LEGACY.md)  
**Là gì:** Dự án tiền nhiệm nghiên cứu các đoạn song hành/tái sử dụng trong văn bản Phật học.  
**BodhiAtlas cần kiểm:** Đáng học phương pháp và dữ liệu lịch sử; cần phân biệt legacy với hệ sinh thái kế nhiệm.


### 06. Ngôn ngữ, phê bình văn bản và định vị học thuật

Nhóm chuẩn/công cụ chuyên biệt cho chuyển tự, dị bản, ghi chú và mở đúng vị trí nguồn.

**P31 · [OpenCC](https://github.com/BYVoid/OpenCC)** · *Chưa có báo cáo trong repo*  
**Là gì:** Công cụ đổi Hán giản thể/phồn thể và một số biến thể chính tả theo cấu hình.  
**BodhiAtlas cần kiểm:** Bổ sung normalized index; cần tránh chuyển đổi nhiều-một khiến thuật ngữ bị đồng nhất sai.

**P32 · [pyewts / Tibetan Wylie transliteration](https://pypi.org/project/pyewts/)** · *Chưa có báo cáo trong repo*  
**Là gì:** Thư viện chuyển tự giữa chữ Tạng Unicode và Wylie theo quy tắc.  
**BodhiAtlas cần kiểm:** Bổ sung kênh tra cứu phiên tự; không giải quyết tự động ngữ nghĩa hay OCR Tạng.

**P33 · [TEI P5 / Critical Apparatus](https://tei-c.org/release/doc/tei-p5-doc/en/html/)** · *Chưa có báo cáo trong repo*  
**Là gì:** Bộ chuẩn mô hình hóa văn bản học thuật, nhân chứng và chú giải dị bản.  
**BodhiAtlas cần kiểm:** Dùng làm tham chiếu cho schema và nhập/xuất, tránh áp cả chuẩn vào mọi nguồn khi chưa cần.

**P34 · [IIIF specifications](https://iiif.io/api/presentation/3.0/)** · *Chưa có báo cáo trong repo*  
**Là gì:** Bộ chuẩn phân phối, biểu diễn và chú giải ảnh tư liệu số.  
**BodhiAtlas cần kiểm:** Đáng nghiên cứu để trỏ trích dẫn về ảnh trang/vùng ảnh khi có máy chủ IIIF.

**P35 · [Mirador IIIF viewer](https://github.com/ProjectMirador/mirador)** · *Chưa có báo cáo trong repo*  
**Là gì:** Trình xem ảnh theo chuẩn IIIF, hỗ trợ điều hướng và chú giải tư liệu số.  
**BodhiAtlas cần kiểm:** Ứng viên viewer trang scan/bản thảo; phụ thuộc metadata và manifest ảnh được chuẩn hóa.

**P36 · [EPUB CFI / EPUB 3 locator](https://www.w3.org/TR/epubcfi-11/)** · *Chưa có báo cáo trong repo*  
**Là gì:** Quy tắc định vị điểm/đoạn trong tài liệu EPUB; đây là chuẩn, không phải ứng dụng.  
**BodhiAtlas cần kiểm:** Cần cho phiếu truy nguyên EPUB và khả năng mở lại vị trí khi hiển thị.

**P48 · [CollateX](https://github.com/interedition/collatex)** · [Đọc báo cáo](REPORT_48_COLLATEX.md)  
**Là gì:** Công cụ đối chiếu nhiều phiên bản văn bản và hiển thị khác biệt.  
**BodhiAtlas cần kiểm:** Ứng viên cho nghiên cứu dị bản; không thay thế người quyết định quan hệ song hành.

**P49 · [passim](https://github.com/dasmiq/passim)** · [Đọc báo cáo](REPORT_49_PASSIM.md)  
**Là gì:** Thuật toán/công cụ phát hiện đoạn được trích dẫn lại hoặc tái sử dụng giữa nhiều văn bản.  
**BodhiAtlas cần kiểm:** Ứng viên tìm đoạn gần giống và nguồn gián tiếp; cần kiểm ngôn ngữ, độ dài, false positive.

**P50 · [INCEpTION](https://github.com/eclipse-inception/inception)** · [Đọc báo cáo](REPORT_50_INCEPTION_ANNOTATION.md)  
**Là gì:** Nền tảng gắn nhãn corpus và xét duyệt annotation với người tham gia.  
**BodhiAtlas cần kiểm:** Tạo bộ gold set về nghĩa thuật ngữ, quan hệ và chứng cứ; có thể cần ở giai đoạn học thuật.


### 07. Hạ tầng lưu trữ và kết nối AI

Nhóm triển khai bảo toàn file gốc và mở API/MCP; không phải bộ máy hiểu nghĩa hay xác nhận trích dẫn.

**P37 · [S3-compatible Object Storage](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html)** · *Chưa có báo cáo trong repo*  
**Là gì:** Họ giao thức lưu object như S3, phục vụ file bất biến, sao lưu và phân phối nội dung.  
**BodhiAtlas cần kiểm:** Ứng viên hạ tầng tài liệu gốc; không nhầm object storage với catalog/quan hệ học thuật.

**P38 · [Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification)** · *Chưa có báo cáo trong repo*  
**Là gì:** Chuẩn kết nối công cụ và ngữ cảnh cho các AI client.  
**BodhiAtlas cần kiểm:** Kết nối cùng kho tra cứu cho nhiều AI; cần chặn truy cập vượt quyền và không lẫn quyền đọc file.

---

## Cách ra quyết định sau khi đọc báo cáo

1. **Đối chiếu năng lực, không so repo bằng số sao.** Một platform đầy đủ không mặc nhiên tốt hơn các công cụ chuyên biệt nếu không giữ được source map.
2. **Đánh giá theo ba chiến lược:** *(A)* kế thừa nền tảng lớn, *(B)* ghép vài nền tảng có API rõ, *(C)* tự xây lõi mỏng dựa trên thư viện có sẵn.
3. **Chạy cùng corpus mẫu:** PDF sạch/scan, EPUB, DOCX, văn bản Hán, Pāli, Tạng, bài nghiên cứu có cước chú, nhiều ấn bản và ví dụ OCR lỗi. Tìm chuỗi ngắn, câu dài, nhiều vị trí, lỗi một ký tự và câu không tồn tại.
4. **Đặt cổng không được đánh đổi:** `SOURCE_FIDELITY`, `CODE_ONLY_EXACT`, `QUALITY_COVERAGE`, `RIGHTS_SECURITY`, `PORTABILITY`. Nếu không vượt qua cổng bắt buộc, phần mềm nhiều tính năng hơn cũng không thể thay thế lõi học thuật.
5. **Ghi quyết định có thể đảo ngược:** Mỗi lựa chọn phải có phiên bản kiểm thử, tiêu chí đạt/chưa đạt, chi phí tích hợp, phương án thay thế và những điểm chưa biết.

## Các khoảng trống cần tiếp tục kiểm tra

Danh mục hiện tại có nhiều ứng viên OCR/search/corpus. Sáu hướng dưới đây là **đề xuất khảo sát ngoài bộ P01–P55**, chưa phải báo cáo đã hoàn tất và chưa phải quyết định lựa chọn:

| Công nghệ | Khoảng trống nó giúp xem xét | Ưu tiên khảo sát |
|---|---|---|
| [PDF.js](https://github.com/mozilla/pdf.js) | Viewer PDF trong browser, mở trang và đánh dấu câu trích trên bản gốc | Rất cao |
| [Readium Web](https://github.com/readium/web) | Bộ công cụ trình đọc EPUB trên web, cần kiểm tra locator/CFI | Rất cao |
| [Unstructured](https://github.com/Unstructured-IO/unstructured) | Pipeline tiền xử lý nhiều định dạng, so sánh với Docling/MinerU/Marker | Cao |
| [Haystack](https://github.com/deepset-ai/haystack) | Framework pipeline retrieval/RAG có thể cấu hình thay vì phụ thuộc platform tích hợp | Trung bình–cao |
| [OCR-D](https://github.com/OCR-D) | Công cụ và chuẩn luồng OCR với chú trọng ground truth/đánh giá tài liệu lịch sử | Theo nhu cầu bản thảo cổ |
| [BEIR](https://github.com/beir-cellar/beir) | Framework benchmark information retrieval; tham khảo cách tổ chức đánh giá trên bộ truy vấn chuẩn | Theo nhu cầu benchmark |

**Lưu ý:** BEIR không thay thế bộ câu trích chuẩn riêng của BodhiAtlas; một hệ thống đứng đầu benchmark truy xuất vẫn có thể trả sai vị trí/trang khi sử dụng thực tế.

## Quản trị tài liệu

- **Nguồn chuẩn nghiệp vụ:** [`../../docs/PRD.md`](../../docs/PRD.md).
- **Nguồn chuẩn rủi ro học thuật:** [`../../docs/ACADEMIC_RISKS_AND_VERIFICATION.md`](../../docs/ACADEMIC_RISKS_AND_VERIFICATION.md).
- **Nội dung báo cáo chuyên sâu là bằng chứng để chọn giải pháp, không phải quyết định triển khai.** Khi repo upstream thay đổi, giữ ngày nghiên cứu, tag/commit và đánh dấu đánh giá đã cũ.
- **Bảo toàn lịch sử:** Không xóa báo cáo chỉ vì kết luận đã thay đổi; thêm quyết định kiến trúc/biên bản benchmark riêng sau này.
