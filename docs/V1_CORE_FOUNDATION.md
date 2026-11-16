# ĐỊNH HƯỚNG THIẾT KẾ NỀN TẢNG BODHIATLAS V1 CORE

**Tên tiếng Anh:** BodhiAtlas V1 Core — Source-Grounded Knowledge Retrieval  
**Phiên bản tài liệu:** 1.0  
**Ngày lập:** 16/11/2026  
**Ngày cập nhật:** 16/11/2026  
**Trạng thái:** Định hướng thiết kế — chưa chốt kiến trúc triển khai hoặc công nghệ cụ thể  
**Phạm vi:** Năng lực nền tảng của V1 Core; không phải tài liệu chọn công nghệ hoặc kế hoạch triển khai

> **Tuyên bố cốt lõi:** BodhiAtlas V1 Core biến tài liệu đa định dạng thành một kho văn bản có cấu trúc, có thể tìm kiếm và truy nguyên về tài liệu gốc. **Tìm đúng nguồn, đúng nguyên văn và đúng vị trí bằng code** là năng lực nền tảng. Second Brain, RAG và AI Research có thể được bổ sung nhưng không thay thế việc kiểm chứng nguồn.

## 1. Vai trò của tài liệu và định nghĩa V1 Core

### 1.1. Tài liệu này giải quyết điều gì?

- **[PRD v1.4](PRD.md):** quy định sản phẩm phải làm được gì và các tiêu chí nghiệm thu.
- **Tài liệu này:** diễn giải các lớp năng lực cần phối hợp như thế nào để hình thành một lõi tra cứu có thể kiểm chứng, không phụ thuộc LLM tạo sinh.
- **[Sổ tay rủi ro và kiểm chứng học thuật v1.0](ACADEMIC_RISKS_AND_VERIFICATION.md):** chỉ ra các sai sót cần ngăn ngừa, trạng thái kiểm chứng và các cổng chất lượng trước khi dùng chứng cứ để công bố.

Tài liệu này **không thay thế, mở rộng hoặc hạ thấp yêu cầu PRD v1.4**. Các đề xuất về cách mô hình hóa được sử dụng làm cơ sở nghiên cứu và thử nghiệm; khi có xung đột, đối chiếu PRD và cập nhật có kiểm soát.

### 1.2. V1 Core là gì — và không phải là gì?

**Định nghĩa đề xuất:** *Source-Grounded Knowledge Retrieval* — lõi xử lý tài liệu, lưu dấu nguồn, lập chỉ mục, tìm kiếm đa ngôn ngữ và xuất kết quả có thể đối chiếu độc lập với bản gốc.

BodhiAtlas **không chỉ là** phần mềm chứa sách, kho tóm tắt, Second Brain, hay RAG. Một hệ RAG thông thường có thể trả lời câu hỏi nhưng chưa chắc bảo toàn được chính xác ấn bản, trang, đoạn, ngữ cảnh và mức độ tin cậy của nguồn.

**Ưu tiên trong PRD:**
1. Tìm đúng nguồn, kiểm chứng được.
2. Nạp và xử lý tài liệu tự động, liên tục.
3. Đơn giản, tiết kiệm, mở rộng lâu dài và độc lập với nhà cung cấp AI.

## 2. Mô hình nền tảng: từ file gốc đến chứng cứ truy nguyên

Luồng khái niệm:

```text
KHO TÀI LIỆU GỐC
PDF · EPUB · DOCX · Markdown · các định dạng được hỗ trợ
File gốc, hash, tác phẩm, ngôn ngữ, bản dịch và ấn bản
                        |
                        v
NẠP VÀ TIÊU HÓA TÀI LIỆU
Trích xuất/OCR -> nhận diện cấu trúc -> ghi nhận lỗi/độ bao phủ
                        |
                        v
VĂN BẢN TRÍCH XUẤT CÓ CẤU TRÚC + BẢN ĐỒ NGUỒN
Định danh, phiên bản xử lý, chương/mục/đoạn,
ánh xạ về trang/vùng chữ/vị trí trong file gốc
                        |
           +------------+-------------+
           |            |             |
           v            v             v
  CHỈ MỤC CHÍNH XÁC  TỪ ĐIỂN/QUAN HỆ  CHỈ MỤC NGỮ NGHĨA
  & GẦN ĐÚNG         ĐÃ XÁC MINH      (mở rộng tùy chọn)
           |            |             |
           +------------+-------------+
                        |
                        v
          TÌM ỨNG VIÊN + KIỂM CHỨNG ĐỘC LẬP
                        |
                        v
             PHIẾU TRUY NGUYÊN NGUỒN
           Nguyên văn · Vị trí · Trạng thái
                        |
                        v
       NGHIÊN CỨU / GHI CHÚ / AI RESEARCH (nếu bật)
```

**Ba nguyên tắc không được phá vỡ:**

1. **File gốc là đối tượng đối chiếu cuối cùng.** Mỗi tác phẩm, ấn bản/bản dịch và file có danh tính riêng. Hash kiểm tra trùng byte, không tự khẳng định hai ấn bản là một.
2. **Văn bản trích xuất có cấu trúc không thay thế bản gốc.** Mỗi bản trích xuất gắn với file/ấn bản và phiên bản xử lý; lỗi OCR, trang thiếu và vùng không đọc được phải được lưu/hiển thị.
3. **Chỉ mục và chunk là dẫn xuất có thể tạo lại.** Chuẩn hóa, bỏ dấu, chuyển tự, embeddings hay chia chunk không được sửa nguyên văn hoặc trở thành địa chỉ dẫn chứng học thuật duy nhất. Khi tái lập chỉ mục, dẫn chứng cũ phải tiếp tục mở đúng chỗ hoặc báo cần kiểm lại.

### 2.1. Các đơn vị dữ liệu cần phân biệt

| Đơn vị | Chức năng |
|---|---|
| **Tác phẩm** | Nhận diện một tác phẩm ở mức khái niệm/thư mục. |
| **Bản dịch / ấn bản / dị bản** | Phân biệt các hình thức văn bản có nội dung hoặc cách đánh số trang khác nhau. |
| **File nguồn** | Đối tượng lưu trữ thực tế, có định danh, định dạng và hash. |
| **Bản trích xuất** | Văn bản/cấu trúc được xử lý từ file cụ thể, có phiên bản và chất lượng xử lý. |
| **Đơn vị văn bản** | Chương, mục, đoạn, chú thích hoặc vùng văn bản có thể dẫn chiếu. |
| **Source Map / Locator** | Ánh xạ đơn vị văn bản về đúng vị trí có thể mở lại trong file nguồn. |
| **Chỉ mục tra cứu** | Cấu trúc phục vụ tìm ứng viên; có thể tái tạo từ dữ liệu đã lưu. |
| **Chứng cứ / ghi chú nghiên cứu** | Trích dẫn, nhận định và quan hệ đã được gắn nguồn, trạng thái, người duyệt khi thích hợp. |

## 3. Năm năng lực nền tảng của V1 Core

### 3.1. Universal Document Ingestion — Nạp và xử lý tài liệu

- Nhận PDF văn bản, PDF scan, EPUB, DOCX và Markdown; hỗ trợ mở rộng thêm định dạng.
- Lưu file gốc và metadata; phát hiện file trùng, phiên bản mới và ngôn ngữ khi có thể.
- Trích xuất văn bản; OCR khi cần; nhận diện chương, mục, đoạn, chú thích, bảng, cột và trang trong phạm vi khả năng thực tế.
- Ghi rõ **độ bao phủ**, trang/vùng lỗi, phần không đọc được, tình trạng `READY`, `PARTIAL`, `OCR_UNCERTAIN` hoặc tương đương.
- Chỉ lập chỉ mục phần có thể truy xuất; không tuyên bố đã đọc hết một tài liệu khi mới xử lý một phần.

“Tiêu hóa” ở V1 Core chủ yếu là **biến tài liệu thành dữ liệu tìm được và kiểm tra được**, không bắt buộc AI tóm tắt/diễn giải toàn bộ sách lúc nhập.

### 3.2. Structure & Source Mapping — Giữ cấu trúc và vị trí gốc

- Bảo toàn văn bản trích xuất theo từng file/ấn bản; giữ ranh giới đoạn, nội dung chính và chú thích khi có thể.
- Có đường quay lại đúng file, trang/vùng chữ hoặc đoạn gốc, không chỉ quay lại tên sách.
- PDF: phân biệt **trang PDF** với **trang in**; lưu tọa độ/vùng chữ khi xác định đáng tin cậy.
- EPUB: lưu tài nguyên/đoạn trong cấu trúc EPUB; dùng EPUB CFI nếu tạo và đối chiếu được.
- DOCX/Markdown: lưu đường dẫn cấu trúc, định danh đoạn và phiên bản file; không xem số dòng có thể thay đổi là định danh bất biến.
- Vị trí tự động suy ra phải có trạng thái kiểm chứng, đặc biệt khi OCR, nhiều cột hoặc tái trích xuất.

### 3.3. Deterministic Search — Tra cứu bằng code

Lõi tra cứu phải có khả năng tìm mà **không cần LLM tạo sinh**:

- **`EXACT`:** khớp chuỗi nguyên văn.
- **`NORMALIZED`:** khớp sau chuẩn hóa rõ ràng, ví dụ bỏ dấu hoặc chuyển đổi chữ viết có quy tắc.
- **`FUZZY`:** tìm gần đúng về chữ, cấu trúc hoặc lỗi OCR.
- **`LEXICON`:** mở rộng theo từ điển và quan hệ thuật ngữ đã xác minh.
- **`SEMANTIC`:** tùy chọn khi cần tìm tương đồng ngữ nghĩa; không được gắn nhãn `EXACT` hoặc ngầm coi như chứng minh luận điểm.

Đặc biệt phải xử lý trong phạm vi dữ liệu và công cụ được hỗ trợ: tiếng Việt có/không dấu; Hán giản/phồn, cụm Hán văn; Pāli/Sanskrit Latin có/không dấu phụ; và mở rộng dần sang chữ Tạng/Wylie, các ngôn ngữ khác theo PRD.

**Hai bước độc lập:** (a) bộ tìm kiếm thu thập và xếp hạng *nguồn ứng viên*; (b) bộ kiểm chứng đọc lại văn bản/định vị đã lưu để đối chiếu chính xác, ghi giới hạn và tình trạng. Điểm xếp hạng **không phải** xác suất luận điểm đúng.

### 3.4. Terminology-Aware Retrieval — Tra theo từng nghĩa

- Mục từ đa nghĩa phải tách **từng nghĩa**, mỗi nghĩa có văn cảnh và chứng cứ riêng.
- Quan hệ Pāli–Sanskrit–Hán–Tạng–Việt–Anh phải nêu loại quan hệ, nguồn xác nhận, phạm vi và truyền thống khi thích hợp.
- Không xem từ gần nghĩa hoặc từ dịch tương ứng là đồng nghĩa hoàn toàn trong mọi hoàn cảnh; không suy ra tương đương bằng liên kết bắc cầu vô hạn.
- Kết quả có thể nhóm theo tác phẩm, tác giả, ấn bản, ngôn ngữ và nghĩa, trong phạm vi metadata đã có.

### 3.5. Evidence Presentation — Phiếu truy nguyên nguồn

Mỗi kết quả có giá trị sử dụng học thuật cần thể hiện đủ để người dùng **mở và tự kiểm tra**, thay vì chỉ xem câu trả lời tạo sinh:

- Tác phẩm, tác giả, ngôn ngữ, dịch giả/ấn bản và file xác định.
- Nguyên văn, ngữ cảnh, chương/mục/đoạn, số trang hoặc định vị phù hợp định dạng.
- Định danh file, hash, loại khớp, phạm vi đã tìm và tình trạng OCR/chỉ mục.
- Trạng thái kiểm tra câu chữ/vị trí tách riêng khỏi nhận định về **ý nghĩa của chứng cứ**.
- Ghi chú, phân tích của người nghiên cứu hoặc AI **đặt riêng khỏi nguyên văn** và có trạng thái thẩm định.

## 4. Ranh giới giữa Code-only, Second Brain, RAG và AI Research

| Năng lực | Code-only (mặc định) | Lớp mở rộng / AI Research |
|---|---|---|
| Nạp, OCR, cấu trúc và chỉ mục | Xử lý, ghi lỗi, giữ provenance | Có thể hỗ trợ trường hợp khó nhưng không che lỗi |
| Tìm `anatta`, `anattā` hoặc thuật ngữ có quan hệ | Tìm chính xác, chuẩn hóa, từ điển có nguồn | Semantic search giúp mở rộng ứng viên |
| Tìm câu trích, ấn bản, trang/đoạn | Đối chiếu kỹ thuật, trả vị trí và trạng thái | AI không tự xác nhận vị trí |
| Tìm tác giả cùng bàn về hai khái niệm | Tìm đoạn đồng xuất hiện, cấu trúc liên quan, quan hệ đã được biên tập | AI/người nghiên cứu xác định họ có *thực sự phân biệt* hay không |
| Giải thích và so sánh lập luận phức tạp | Chỉ xuất thông tin/quan hệ đã lưu và nguồn ứng viên | Đánh giá ngữ cảnh, phản chứng, giới hạn; cần người duyệt các kết luận quan trọng |

**Second Brain** ở đây là **lớp tích lũy tri thức có kiểm chứng**: ghi chú, luận điểm, quan hệ giữa tác giả–nhận định–đoạn chứng cứ–nguồn, người xác nhận và lịch sử. Không mặc định tự động sinh toàn bộ tri thức đã xác minh khi nạp sách.

**RAG** là một phương pháp sử dụng các đoạn tìm được để hỗ trợ AI; chỉ mục ngữ nghĩa/embeddings có thể tăng khả năng tìm ứng viên. Nhưng chunk và kết quả AI không được làm mất định vị nguồn. Semantic search không nhất thiết gọi LLM *tạo sinh* khi truy vấn, song có thể dùng mô hình học máy; vì vậy không đồng nghĩa với “hoàn toàn không có AI”.

**Ranh giới quan trọng:** *Tìm được đoạn có nhắc đến hai khái niệm* khác với *chứng minh tác giả đang phân biệt hai khái niệm*. V1 Core không hứa code thuần tự hiểu đúng mọi lập luận mở.

## 5. Mẫu phiếu truy nguyên nguồn chuẩn

> **MINH HỌA GIẢ ĐỊNH — không phải trích dẫn đã xác minh.** Mọi tên sách, trang và nội dung dưới đây chỉ mô tả cấu trúc đầu ra mong muốn.

### Nguồn 01 — Sách A, bản PDF (giả định)

- **Tác giả / ấn bản:** Tác giả A; ấn bản PDF giả định.
- **Vị trí:** Chương 3 · trang in 58 · trang PDF 64 · tọa độ vùng chữ (nếu xác minh được).
- **Nguyên văn:** *[Hệ thống hiển thị nguyên văn lấy từ bản trích xuất có thể đối chiếu với file gốc; không tự sáng tác câu trích].*
- **File và định vị:** File ID · SHA-256 · phiên bản trích xuất · source locator.
- **Trạng thái kỹ thuật:** *[Ví dụ: đã kiểm văn bản và locator / chỉ có khớp văn bản / OCR cần rà lại].*
- **Phân tích riêng:** *[Ví dụ giả định: Tác giả A liên hệ tính biến đổi của hiện tượng với khả năng phát sinh khổ. Đây là diễn giải cần đánh giá ngữ cảnh, không phải câu trích].*
- **Trạng thái đánh giá chứng cứ:** *[Chưa đánh giá / hỗ trợ một phần / có chứng cứ trái chiều ... kèm lý do].*

### Nguồn 02 — Sách B, bản EPUB (giả định)

- **Tác giả / ấn bản:** Tác giả B; ấn bản EPUB giả định.
- **Vị trí:** Chương 5 · đoạn 27 · tài nguyên EPUB · EPUB CFI (nếu có và xác minh được).
- **Nguyên văn:** *[Đoạn nguyên văn được truy xuất bằng locator trong EPUB].*
- **File và định vị:** File ID · SHA-256 · phiên bản trích xuất · source locator.
- **Trạng thái kỹ thuật:** *[Trạng thái đối chiếu chuỗi và vị trí].*
- **Phân tích riêng:** *[Ví dụ giả định: Tác giả B phân biệt vô thường và cảm thọ khổ trong một phạm vi lập luận nhất định].*

**Kết luận so sánh (chỉ khi đủ dữ liệu và đã thẩm định):** nêu rõ *nguồn nào hỗ trợ, nguồn nào trái chiều, điều gì còn thiếu và phần nào là suy luận của AI*. Không lấy một sự tương đồng từ vựng làm kết luận học thuật.

### 5.1. Ba nhóm trạng thái tuyệt đối không nhập làm một

1. **Tài liệu/chỉ mục:** đã xử lý đến đâu? (`READY`, `PARTIAL`, `OCR_UNCERTAIN`, ...).
2. **Câu chữ/vị trí:** có đúng văn bản và đúng file/ấn bản/locator? (`TEXT_AND_LOCATOR_VERIFIED`, `TEXT_ONLY`, `MISMATCH`, ...).
3. **Chứng cứ cho nhận định:** thực sự hỗ trợ, giới hạn hay phản bác luận điểm? (`SUPPORTS`, `PARTIAL`, `CONTRARY`, `INSUFFICIENT`, `NOT_ASSESSED`, ...).

Nhãn nêu ở đây là **ví dụ để định hướng thiết kế**, không khẳng định đã triển khai. Trạng thái (2) đã xác minh **không tự suy ra** trạng thái (3) là hỗ trợ. AI không tự phê duyệt kết luận học thuật.

## 6. Hai tình huống để xác định đúng giới hạn nghiệm thu

### Tình huống A — Tra cứu `anatta`

**Đầu vào:** `anatta`.

**Kết quả mong đợi:** tìm `anatta` nguyên văn; `anattā` qua cơ chế chuẩn hóa phù hợp; tìm gần đúng; gợi ý liên kết như `anātman`, `無我`, `vô ngã`, `non-self` **chỉ khi có quan hệ từ điển đủ tin cậy**. Mỗi kết quả phải nêu *kiểu khớp*, nguồn, ngữ cảnh và vị trí. Không tự khẳng định mọi thuật ngữ trên tương đương hoàn toàn.

### Tình huống B — Câu hỏi về vô thường và khổ

**Đầu vào:** “Trong các tài liệu tôi có, những tác giả nào phân biệt giữa vô thường và khổ? Họ lập luận như thế nào? Cho tôi vị trí chính xác trong sách.”

**V1 Core phải làm được:** tìm ứng viên trong phạm vi thư viện đã lập chỉ mục qua `vô thường`, `anicca`, `anitya`, `無常`, `khổ`, `dukkha`, `duḥkha`, `苦` và các quan hệ đã xác nhận; lọc theo tác giả/ấn bản; trả nguyên văn, ngữ cảnh và locator; làm rõ khoảng trống dữ liệu.

**Không được tự khẳng định:** hễ đoạn có hai từ khóa thì tác giả đã phân biệt chúng, hay tự viết tổng kết lập luận chính xác chỉ bằng khớp từ ngữ.

**Khi bật AI Research:** có thể đề xuất đọc hiểu lập luận, so sánh tác giả và tìm phản chứng dựa trên các nguồn ứng viên; mọi câu trích vẫn phải kiểm bằng cơ chế truy nguyên. Nhận định của AI phải được phân tách và thẩm định theo mức độ rủi ro.

## 7. Tiêu chí chứng minh V1 Core và nguyên tắc thay đổi

Để xác nhận năng lực cốt lõi, nên thử **một luồng đầy đủ từ file gốc đến phiếu truy nguyên**:

1. Nạp PDF văn bản, PDF scan, EPUB, DOCX và Markdown; kiểm tra hash, metadata và độ bao phủ.
2. Kiểm tài liệu có chú thích, hai cột, trang thiếu và OCR sai; không cho trường hợp lỗi giả là đã kiểm chứng.
3. Tìm nguyên văn, không dấu, Hán giản/phồn, Pāli/Sanskrit Latin có/không dấu; phân biệt `EXACT`/`NORMALIZED`/`FUZZY`/`LEXICON`.
4. Truy vấn `anatta` và tìm các đoạn ứng viên bàn về vô thường–khổ; ghi nhận nguồn tìm thiếu và kết quả nhiễu.
5. Mở lại đúng trang PDF hoặc đoạn EPUB, phân biệt trang in/trang PDF; kiểm việc định vị sau tái lập chỉ mục.
6. Xuất phiếu truy nguyên với nguyên văn, định vị, nguồn/ấn bản và ba nhóm trạng thái độc lập; trường hợp chưa đủ dữ liệu phải nói rõ.
7. Đánh giá riêng **độ bao phủ trích xuất, tỷ lệ tìm lại nguồn đã biết, độ chính xác định vị, lỗi dẫn chứng lọt qua, tốc độ và chi phí**. Với câu hỏi lập luận, chỉ chấm khả năng tìm nguồn ứng viên ở chế độ code-only.

Thử nghiệm lõi cần chạy **không dùng LLM tạo sinh** để đo chất lượng truy xuất thực tế. Semantic/hybrid và AI Research được đối chiếu sau, không dùng để che lấp lỗi của lõi.

**Không bắt buộc ở V1 Core:** tự động chưng cất mọi cuốn sách thành tri thức học thuật đã xác minh; tự giải thích chính xác mọi lập luận; knowledge graph quy mô lớn; hay tự xuất bản nghiên cứu không có người duyệt.

**Quy tắc quản trị:** Tài liệu này nêu nguyên tắc lâu dài, không chốt phần mềm, dịch vụ, cơ sở dữ liệu hay mô hình AI. Mọi thay đổi về phạm vi phải kiểm với PRD v1.4 và sổ tay rủi ro; sửa tài liệu có cập nhật **phiên bản, ngày sửa và lịch sử Git**.

---

**Tóm tắt một câu:** *Lõi BodhiAtlas là văn bản có cấu trúc + ánh xạ về nguồn + tìm kiếm đa ngôn ngữ bằng code + kiểm chứng độc lập + phiếu truy nguyên; Second Brain, RAG và AI Research là các lớp mở rộng trên nền tảng đó.*
