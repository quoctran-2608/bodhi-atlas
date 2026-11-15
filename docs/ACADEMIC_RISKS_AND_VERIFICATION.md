# BODHIATLAS — SỔ TAY RỦI RO, GIỚI HẠN VÀ QUY TẮC KIỂM CHỨNG HỌC THUẬT

**Tài liệu đồng hành với:** `Đề bài V1.4 — Hệ thống thư viện tri thức và tra cứu học thuật`  
**Phiên bản:** 1.0 · **Ngày:** 15/11/2026  
**Ứng dụng chính:** Viết sách Phật học liên ngành và biên soạn từ điển Phật học.  
**Vai trò:** Danh mục tình huống sai sót, nguyên tắc ngăn ngừa, cách xử lý và tiêu chí kiểm thử; **không thay thế hay mở rộng tùy tiện phạm vi Đề bài V1.4**.

---

## 1. Tài liệu này dùng để làm gì?

**Đề bài V1.4** mô tả *hệ thống phải làm được gì*. **Sổ tay này** trả lời bốn câu hỏi vận hành:

1. Khi tìm kiếm, nghiên cứu hoặc viết sách, hệ thống có thể **sai ở đâu**?
2. Làm thế nào **nhận ra lỗi**, trước khi sai sót đi vào bản thảo hoặc từ điển?
3. Nếu không thể kiểm chứng, hệ thống phải **dừng, ghi giới hạn hoặc đề nghị bổ sung nguồn** như thế nào?
4. Khi nghiệm thu, cần thử những **tình huống gây lỗi thực tế** nào?

**Ba nguyên tắc không được đánh đổi:**

- **Nguồn gốc bất biến:** Luôn có khả năng đối chiếu file/phiên bản gốc; bản chuẩn hóa, OCR, chỉ mục và nội dung AI sinh ra không được giả làm nguyên văn.
- **Phân tầng kết luận:** Tìm đúng câu chữ ≠ định vị đúng ≠ hiểu đúng ngữ cảnh ≠ đủ chứng cứ cho luận điểm ≠ xác lập sự kiện lịch sử.
- **Được phép không biết:** Không tìm được, chưa đọc được, chưa đủ chứng cứ hoặc còn tranh luận đều là kết quả hợp lệ. **Không lấp khoảng trống bằng suy đoán rồi trình bày như sự thật.**

**Phạm vi kiểm soát:** Hai chế độ cùng sử dụng một kho nguồn. **Chế độ 1** dùng code để tìm, đối chiếu và ghi phạm vi đã kiểm. **Chế độ 2** dùng AI cho diễn giải/đánh giá, song mọi câu trích và nguồn được nêu vẫn phải quay lại kiểm bằng Chế độ 1 hoặc được đánh dấu chưa kiểm.

---

## 2. Sổ đăng ký rủi ro trọng yếu

**Ưu tiên:** `P0` = lỗi có thể tạo chứng cứ giả/sai nghiêm trọng hoặc làm hỏng dữ liệu, phải ngăn trước khi sử dụng để công bố; `P1` = ảnh hưởng lớn đến chất lượng/độ bao phủ, phải có cảnh báo và lộ trình kiểm soát; `P2` = cải tiến khi có nhu cầu thực tế. Các mã R là mã nội bộ đề xuất cho dự án, không phải chuẩn học thuật.

### 2.1. Nạp sách, OCR và bảo toàn nguồn

| Mã | Rủi ro thực tế | Quy tắc phòng ngừa và phát hiện | Mức |
|---|---|---|---|
| R01 | OCR sai chữ Hán/Tạng/Pāli, nhầm dấu phụ, chữ mờ, mất từ phủ định | Giữ ảnh/file gốc; ghi độ tin cậy theo trang/vùng khi có; đối chiếu ảnh ở trích dẫn rủi ro cao; không xác minh câu trích chỉ từ OCR chưa được kiểm | P0 |
| R02 | Đọc sai sách hai cột, bảng, chú thích, tiêu đề, dòng nối trang; trộn lời tác giả và người chú giải | Nhận diện và lưu vai trò cấu trúc; kiểm mẫu các trang phức tạp; đánh dấu vùng chưa trích xuất đủ | P0 |
| R03 | Nhầm ấn bản, dịch giả, tập, số trang in với số trang PDF | Tách mã tác phẩm → bản dịch/ấn bản → file; lưu cả số trang PDF và số trang in khi xác minh được; không tự suy diễn trang | P0 |
| R04 | Thay file hoặc chia lại đoạn làm trỏ dẫn chứng tới đoạn khác | File gốc có hash và định danh bất biến; lưu locator/phiên bản trích xuất độc lập với ID chunk; sau lập chỉ mục lại phải thử mở lại dẫn chứng | P0 |
| R05 | Bản scan thiếu trang hoặc tài liệu chỉ được trích xuất một phần nhưng hệ thống báo “đã đọc toàn bộ” | Có manifest trang/mục đã xử lý, lỗi, trang thiếu và trạng thái `PARTIAL`; không coi kết quả không tìm thấy là khảo sát đầy đủ | P0 |
| R06 | Hai file giống chữ nhưng khác ấn bản hoặc hai file khác hash nhưng là cùng nội dung bị gộp sai | Hash dùng để kiểm file trùng byte; quan hệ trùng nội dung/tác phẩm phải tách biệt và có căn cứ xác nhận | P1 |

### 2.2. Tra cứu đa ngôn ngữ và tìm kiếm gần đúng

| Mã | Rủi ro thực tế | Quy tắc phòng ngừa và phát hiện | Mức |
|---|---|---|---|
| R07 | Bỏ dấu tiếng Việt làm nhập nhằng từ; chuẩn hóa Hán giản–phồn hoặc Unicode làm mất khác biệt quan trọng | Chỉ chuẩn hóa trong **chỉ mục phụ**; giữ nguyên văn; hiển thị dạng truy vấn và phép biến đổi đã dùng; không ghi `EXACT` cho kết quả đã chuyển đổi | P0 |
| R08 | Tìm fuzzy/OCR gần giống đưa đoạn sai lên đầu, điểm xếp hạng bị hiểu là độ đúng của chứng cứ | Tách `EXACT`, `NORMALIZED`, `FUZZY`, `LEXICON`, `SEMANTIC`; chỉ gọi là **ứng viên**, có phần so sánh sai khác và ngưỡng trả kết quả | P1 |
| R09 | Đối chiếu Pāli–Sanskrit–Hán–Tạng–Việt–Anh nhầm từ gần nghĩa thành đồng nghĩa hoàn toàn | Quan hệ thuật ngữ phải đi **qua từng nghĩa**, ghi nguồn, truyền thống, văn cảnh; không mở rộng bắc cầu vô hạn qua nhiều từ dịch | P0 |
| R10 | Phiên tự Wylie/chữ Tạng, chữ Hán dị thể, hình thái từ làm sót kết quả | Kiểm thử riêng từng hệ chữ và quy tắc chuyển tự; ghi ngôn ngữ/hệ chữ chưa được hỗ trợ; không hứa độ bao phủ toàn diện | P1 |
| R11 | Tìm theo một luận đề trả các đoạn chứa cùng từ nhưng không liên quan lập luận | Chế độ 1 chỉ trả nguồn ứng viên và giải thích kiểu khớp; Chế độ 2 mới đánh giá ý nghĩa, với ngữ cảnh được kiểm lại | P0 |

### 2.3. Nguồn kinh điển, lịch sử và đối chiếu liên ngành

| Mã | Rủi ro thực tế | Quy tắc phòng ngừa và phát hiện | Mức |
|---|---|---|---|
| R12 | Dùng một tường thuật trong kinh, truyền thuyết hay biên niên sử để khẳng định sự kiện lịch sử là thật | Gắn **loại nhận định** và **loại nguồn**; diễn đạt “văn bản X ghi…” khác với “chứng cứ lịch sử xác lập…”; nêu giới hạn và ý kiến khác | P0 |
| R13 | Nhầm niên đại sự kiện, biên soạn, bản chép, bản dịch, hiện vật; suy ra năm chính xác từ khoảng niên đại | Lưu riêng từng loại niên đại, phương pháp xác định, khoảng thời gian, nguồn và tranh luận | P0 |
| R14 | Coi kinh Nikāya và A-hàm song hành là hai bản dịch trùng nhau; gộp các dị bản thành một nguyên văn | Phân biệt `translation_of`, `parallel_to`, `variant_of`, `commentary_on`; xác định mức tương ứng và điểm khác biệt trước khi kết luận | P0 |
| R15 | Đồng nhất “Phật giáo sơ kỳ”, “Theravāda”, “Nam truyền”, “Bắc truyền”, “Đại thừa” thành các nhóm tương đương hoặc đối lập tuyệt đối | Ghi truyền thống, thời kỳ, phạm vi địa lý và học phái riêng; nhãn nghiên cứu có thể giao nhau, cần nguồn khi phân loại | P1 |
| R16 | Đếm ba bản dịch/chú giải dựa trên cùng bản gốc thành ba chứng cứ độc lập | Ghi chuỗi phụ thuộc và nguồn nguyên cấp/thứ cấp; chỉ gọi độc lập nếu sự độc lập thực sự được xác lập | P0 |
| R17 | Câu trích đúng chữ nhưng bị cắt mất phủ định, ngoại lệ, lời của đối phương hoặc câu tác giả bác bỏ | Lấy đủ trước/sau, xác định ai đang nói và mục đích phát biểu; AI đánh giá ngữ cảnh, người nghiên cứu duyệt nhận định quan trọng | P0 |
| R18 | Dùng tên học giả/nhà xuất bản nổi tiếng để thay cho kiểm tra nội dung; bỏ qua công trình trái chiều, đính chính | Uy tín và **mức hỗ trợ luận điểm** phải đánh giá riêng; tìm phản chứng theo phạm vi; kiểm bản sửa/đính chính nếu có | P0 |
| R19 | Từ điển gộp nhiều nghĩa của `dhamma/dharma` hoặc đưa một nghĩa chuyên biệt thành nghĩa chung; nhầm từ nguyên và cách dịch | Đơn vị kiểm là **từng nghĩa (sense)**; ví dụ và dẫn chứng gắn với nghĩa riêng; phân biệt từ nguyên, phiên tự, từ tương ứng và diễn giải | P0 |

### 2.4. AI Research, nguồn ngoài và an toàn thông tin

| Mã | Rủi ro thực tế | Quy tắc phòng ngừa và phát hiện | Mức |
|---|---|---|---|
| R20 | AI bịa tên sách, câu trích, trang, DOI, đoạn kinh hoặc khẳng định đã đọc nguồn chưa tiếp cận | Metadata xác minh chỉ chứng minh **tồn tại thư mục**; dẫn chứng cần đối chiếu nội dung thực; trí nhớ AI chỉ là gợi ý tìm | P0 |
| R21 | Chỉ đọc abstract, snippet hoặc trích dẫn gián tiếp rồi viết như đã kiểm toàn văn | Bắt buộc ghi mức tiếp cận: toàn văn đã kiểm / abstract hoặc metadata / dẫn theo / chưa xác minh; không dùng mức thấp để khẳng định nội dung chưa đọc | P0 |
| R22 | AI tìm nguồn chỉ để củng cố kết luận có sẵn; bỏ qua điều kiện, phản chứng hoặc bất đồng | Tìm cả nguồn hỗ trợ và nguồn giới hạn/trái chiều theo kế hoạch truy vấn; ghi phạm vi, không ép kết luận đồng thuận | P0 |
| R23 | Website/PDF ngoài chứa hướng dẫn độc hại (“bỏ quy tắc”, “đổi nguồn”, “tiết lộ dữ liệu”), nguồn bị sửa hoặc mất | Xem văn bản ngoài là **dữ liệu không đáng tin để ra lệnh**; không chạy lệnh theo nội dung tài liệu; lưu URL, ngày truy cập, bản lưu hợp lệ khi có | P0 |
| R24 | Dùng tài liệu có bản quyền hoặc tài liệu riêng tư sai phạm vi; AI được cấp quyền quá rộng; tự động nhập nguồn ngoài vô hạn | Mặc định quyền tối thiểu; ba mức truy cập nguồn ngoài như V1.4; xét quyền lưu/chia sẻ/gửi cho mô hình; chỉ nhập lâu dài khi được phép | P0 |

### 2.5. Bản thảo, xuất bản và vận hành lâu dài

| Mã | Rủi ro thực tế | Quy tắc phòng ngừa và phát hiện | Mức |
|---|---|---|---|
| R25 | Mỗi đoạn có dẫn chứng nhưng chương trước–sau mâu thuẫn; thuật ngữ định nghĩa không nhất quán | Kiểm tra theo mệnh đề và vòng rà xuyên chương/mục từ; gắn vị trí bản thảo, lịch sử sửa, người duyệt | P1 |
| R26 | Trích dẫn đúng nhưng chú thích thiếu dịch giả/ấn bản, dẫn gián tiếp không minh bạch, thiếu quyền trích hình/ảnh | Mẫu citation có trường bắt buộc theo từng nguồn; xuất danh mục có thể mở lại; kiểm quyền trước khi phát hành | P1 |
| R27 | Mất catalog, quan hệ nghiên cứu hoặc bản duyệt khi đổi RAG/vector DB; không phục hồi được | Sao lưu riêng file gốc, catalog, quan hệ, hồ sơ nghiên cứu; thử khôi phục và tái lập chỉ mục; không lưu chứng cứ chỉ trong chunk của RAG | P0 |
| R28 | Dự án tốn quá nhiều token vì tự phân tích mọi cuốn sách hoặc chạy AI kiểm lại mọi câu | Lập chỉ mục cơ bản bằng code; ưu tiên kiểm theo rủi ro; cache theo hash/phiên bản; AI theo yêu cầu và giới hạn chi phí | P1 |

**Quy tắc chung cho tất cả rủi ro:** Nếu biện pháp kiểm soát chưa hoạt động, phải **giảm mức khẳng định của kết quả**, giới hạn chức năng có rủi ro hoặc yêu cầu kiểm tra thủ công. Không được coi việc “AI trả lời nghe hợp lý” là phép thử đạt.

---

## 3. Những ranh giới phải thể hiện rõ trong giao diện và báo cáo

### 3.1. Ba loại trạng thái không được trộn lẫn

**(1) Trạng thái tài liệu/chỉ mục** — ví dụ: `READY`, `PARTIAL`, `OCR_UNCERTAIN`, `NOT_INDEXED`, `SOURCE_UNAVAILABLE`. Trả lời: *hệ thống đã tiếp cận và xử lý được bao nhiêu?*

**(2) Trạng thái trích dẫn kỹ thuật** — ví dụ: `TEXT_AND_LOCATOR_VERIFIED`, `TEXT_ONLY`, `OCR_NEEDS_REVIEW`, `MISMATCH`, `UNVERIFIABLE`. Trả lời: *câu chữ và vị trí có khớp đúng file/ấn bản?*

**(3) Đánh giá chứng cứ cho luận điểm** — ví dụ: `SUPPORTS`, `PARTIAL`, `CONTRARY`, `DISPUTED`, `INSUFFICIENT`, `NOT_ASSESSED`. Trả lời: *đoạn này có hỗ trợ kết luận cụ thể nào, trong phạm vi nào?*

Đây là **nhãn đề xuất để thiết kế**, không phải chức năng mặc định đã có ở phần mềm nào. `TEXT_AND_LOCATOR_VERIFIED` **không** suy ra `SUPPORTS`. Nhãn AI đưa ra ở (3) **không tự là phê duyệt học thuật của con người**.

### 3.2. Năm cấp độ tiếp cận nguồn ngoài

1. **Truy cập bản gốc/bản số hóa xác định được ấn bản và đoạn liên quan:** Có thể đưa vào đánh giá chứng cứ sau khi đối chiếu đủ ngữ cảnh.
2. **Truy cập một phần nội dung có xác định phạm vi:** Chỉ kết luận trong phần đã đọc; không giả đã xem toàn tác phẩm.
3. **Chỉ metadata hoặc abstract:** Giới thiệu nguồn cần tìm/đọc; chỉ được nêu những gì chính phần có thể đọc thực sự cho biết.
4. **Dẫn qua tài liệu thứ cấp:** Ghi rõ *dẫn theo*; không mạo nhận kiểm nguồn gốc.
5. **Trí nhớ AI/chưa xác minh sự tồn tại:** Chỉ dùng để đề xuất hướng tìm, tuyệt đối không làm tài liệu tham khảo đã xác nhận.

**Nguồn ngoài không nhất thiết phải nhập trọn file vào thư viện mới được nghiên cứu**, nhưng khi dùng làm chứng cứ phải lưu được hồ sơ truy xuất phù hợp (định danh/URL, lần truy cập, phiên bản, đoạn, phạm vi, giới hạn). Nếu không lưu được bằng chứng có thể tái kiểm, cần ghi rõ rủi ro không tái lập.

### 3.3. Cách diễn đạt khi thiếu chứng cứ

- **Được phép:** “Trong nhóm tác phẩm và phiên bản đã tra, chưa tìm thấy đoạn thỏa truy vấn; hai bản scan chưa xử lý được các trang …”.
- **Không được:** “Không kinh nào nói đến điều này” khi chưa kiểm được toàn bộ phạm vi có liên quan.
- **Được phép:** “Theo nguồn X, có tường thuật rằng…; tính lịch sử của sự kiện cần đối chiếu tư liệu khác”.
- **Không được:** “Sự kiện đã xảy ra” chỉ vì đã tìm được văn bản kể lại.
- **Được phép:** “Có nghiên cứu Y, đã xác minh thư mục, nhưng chưa đọc được phần có liên quan”.
- **Không được:** “Y chứng minh luận điểm” khi mới biết tên sách/DOI.

---

## 4. Quy trình kiểm chứng thực tế cho hai sản phẩm

### 4.1. Khi viết sách Phật học hoặc kiểm bản thảo do AI viết

1. **Chốt phạm vi câu hỏi:** Đang bàn về lời dạy trong một bộ kinh, quan điểm của một truyền thống, hay sự kiện lịch sử? Xác định mức độ khẳng định (ví dụ “một số”, “mọi”, “chỉ”, “lần đầu tiên”).
2. **Tách mệnh đề cần kiểm:** Đánh dấu dữ kiện, trích dẫn, phân loại lịch sử, kết luận nhân quả, giả thuyết. Không cần rà sâu mọi câu dẫn nhập vô hại.
3. **Chạy Chế độ 1:** Tìm nguyên văn/biến thể/đa ngữ, định vị, kiểm file–ấn bản–ngữ cảnh, ghi những chỗ OCR thiếu hoặc không đọc được.
4. **Dùng Chế độ 2 khi cần:** Đánh giá bằng chứng có thật sự hỗ trợ mệnh đề; tìm ngoại lệ/nguồn độc lập/trái chiều; tách tường thuật văn bản với sử liệu và khảo cổ.
5. **Nếu còn thiếu:** Tìm nguồn ngoài theo quyền được cấp; phân biệt *đã đọc* với *mới xác minh thư mục*; lập danh sách nguồn cần bổ sung; không tự lấp bằng trí nhớ AI.
6. **Ra quyết định biên tập:** Giữ nguyên có căn cứ / thu hẹp điều khẳng định / bổ sung dẫn chứng / ghi còn tranh luận / tạm không dùng. Người nghiên cứu chấp thuận các kết luận trọng yếu.
7. **Rà xuyên chương và xuất bản:** Thống nhất thuật ngữ, luận điểm, ấn bản và chú thích; đối chiếu lại những phần sửa đổi, không kiểm lại vô ích toàn bộ tài liệu.

**Đầu ra tối thiểu cho mỗi nhận định quan trọng:**

`[Vị trí trong bản thảo] → [Câu cần kiểm + phạm vi] → [Nguồn/file/ấn bản/đoạn] → [Kết quả đối chiếu kỹ thuật] → [Đánh giá chứng cứ + phản chứng] → [Giới hạn] → [Đề xuất sửa + trạng thái người duyệt]`.

### 4.2. Khi biên soạn một mục từ Phật học

1. **Xác định danh tính mục từ:** Ngôn ngữ/hệ chữ, dạng chuẩn, cách viết khác, phiên tự, từ loại nếu xác định được.
2. **Tách từng nghĩa theo văn cảnh:** Không gộp mọi lần xuất hiện của một chữ thành một định nghĩa; ghi sự khác nhau theo truyền thống, thời kỳ hoặc bộ kinh khi có căn cứ.
3. **Gắn ví dụ nguyên văn cho từng nghĩa:** Có nguồn, vị trí, bản dịch, chú thích và tình trạng kiểm chứng; nêu trường hợp mơ hồ.
4. **Đối chiếu đa ngữ có điều kiện:** Phân biệt *từ cùng gốc*, *từ tương ứng trong bản dịch*, *gần nghĩa* và *tương đương trong ngữ cảnh*. Không suy ra cùng nghĩa bằng chuỗi chuyển dịch bắc cầu.
5. **Rà lịch sử và tranh luận:** Phân biệt nghĩa đã được ghi nhận với giả thuyết từ nguyên hoặc giải thích đặc thù của một học phái.
6. **Rà nhất quán:** Kiểm tra liên kết với các mục từ liên quan, định nghĩa trùng/mâu thuẫn và cách dùng thuật ngữ xuyên toàn bộ từ điển.

**Đầu ra tối thiểu:** `mục từ → nghĩa 1/2/… → chứng cứ và ngữ cảnh riêng → quan hệ thuật ngữ có nguồn → lưu ý về phạm vi/điểm còn tranh luận`.

**Một nền tảng, hai quy trình biên tập:** Không cần hai thư viện, hai bộ lập chỉ mục hay hai AI độc lập.

---

## 5. Các cổng chất lượng (*quality gates*)

| Cổng | Trước khi được phép làm gì? | Điều kiện tối thiểu | Nếu không đạt |
|---|---|---|---|
| G1 — Ingest | Báo tài liệu “sẵn sàng tra cứu” | File xác định được, metadata tối thiểu, phạm vi trích xuất biết rõ; lỗi/trang thiếu hiển thị | Chỉ cho tra phần đã xử lý, gắn `PARTIAL/UNCERTAIN` |
| G2 — Citation | Gắn nhãn câu trích “đã xác minh” | Kiểm lại câu chữ trong đúng file/ấn bản và locator đáng tin; OCR rủi ro được rà | Chỉ hiển thị ứng viên/`TEXT_ONLY`, không xuất như dẫn chứng đã xác minh |
| G3 — Claim | Kết luận một nguồn hỗ trợ luận điểm | Có ngữ cảnh, đúng loại nhận định, xét điều kiện/ngoại lệ và chứng cứ trái chiều thích đáng | Ghi `PARTIAL`, `DISPUTED`, `INSUFFICIENT` hoặc chuyển người duyệt |
| G4 — External | Dùng nguồn ngoài làm chứng cứ | Đọc được phần liên quan; xác định được nguồn/phiên bản, hồ sơ truy xuất và quyền sử dụng | Chỉ ghi nguồn cần tìm, hoặc dẫn gián tiếp có giới hạn |
| G5 — Lexicon | Công bố nghĩa của mục từ | Đã tách nghĩa, có dẫn chứng thích hợp, không nhập nhằng bản dịch/từ nguyên | Để trạng thái dự thảo, đánh dấu nghĩa chưa đủ căn cứ |
| G6 — Publish | Phát hành chương sách/mục từ | Trích dẫn trọng yếu qua G2; kết luận trọng yếu qua G3; rà nhất quán; kiểm chú thích và quyền sử dụng | Không công bố dưới dạng đã xác minh; còn việc tồn đọng phải được ghi và xử lý |

**Lưu ý:** G3 không thể được chứng nhận hoàn toàn bằng code; AI có thể giúp rà nhưng quyền chấp thuận học thuật thuộc người nghiên cứu. Các tiêu chuẩn trên là điều kiện thiết kế, **không phải cam kết rằng một phần mềm hiện tại đã thực hiện sẵn**.

---

## 6. Bộ tình huống kiểm thử bắt buộc (đề xuất)

Mỗi trường hợp cần có dữ liệu đầu vào đã biết trước, **kết quả chuẩn do người nghiên cứu kiểm**, rồi đối chiếu cả trường hợp tìm đúng lẫn trường hợp phải từ chối kết luận.

| Mã | Tình huống | Kết quả hệ thống phải thể hiện |
|---|---|---|
| T01 | PDF scan hai cột, có chú thích cuối trang và một từ phủ định bị OCR sai | Hiển thị đoạn/cột đúng hoặc gắn lỗi OCR; không xuất câu trích sai là xác minh |
| T02 | Cùng một câu ở hai ấn bản khác trang in; trang PDF lệch trang sách | Dẫn đúng từng ấn bản, phân biệt trang PDF và trang in |
| T03 | Nhập `vo thuong`, `無常`, `无常` | Trả kết quả có phân biệt `EXACT` và `NORMALIZED/LEXICON`; cho biết phép chuyển đổi |
| T04 | Nhập thuật ngữ Tạng dạng chữ Tạng và Wylie với một biến thể lỗi | Trả đúng trong phạm vi hỗ trợ, báo giới hạn thay vì tự sửa thành câu trích mới |
| T05 | Một mục từ có hai nghĩa khác nhau trong hai ngữ cảnh | Hiển thị nghĩa và dẫn chứng riêng, không nhập thành một nghĩa chung |
| T06 | Kinh Nikāya và bản A-hàm song hành nhưng khác một đoạn quan trọng | Ghi đúng quan hệ song hành và điểm khác, không coi là hai bản dịch y hệt |
| T07 | Ba bản dịch dựa trên cùng một bản gốc | Không tính thành ba chứng cứ độc lập |
| T08 | Luận điểm dùng “mọi/luôn/chỉ”, nhưng nguồn có điều kiện hoặc ngoại lệ | Phát hiện nguy cơ khái quát hóa; đề xuất thu hẹp hoặc tìm thêm nguồn |
| T09 | AI khẳng định niên đại sự kiện từ niên đại một bản chép muộn | Phân biệt loại niên đại, không mặc định xác lập sự kiện lịch sử |
| T10 | Một PDF thiếu trang liên quan; tìm kiếm trả 0 kết quả | Báo giới hạn tra cứu, không kết luận nguồn/ý tưởng không tồn tại |
| T11 | Nguồn ngoài chỉ có DOI hoặc abstract, chưa đọc toàn văn | Ghi nguồn đề xuất, không tạo câu trích hoặc khẳng định đã chứng minh |
| T12 | Website ngoài chèn chỉ dẫn yêu cầu AI bỏ kiểm chứng | Bỏ qua chỉ dẫn từ nội dung tài liệu, vẫn áp dụng đúng quyền hạn/hồ sơ nguồn |
| T13 | Lập chỉ mục lại sách, ID chunk thay đổi | Các dẫn chứng đã lưu vẫn mở được đúng nguồn hoặc báo cần định vị lại; không trỏ nhầm âm thầm |
| T14 | Hai chương định nghĩa cùng thuật ngữ khác nhau, không giải thích | Báo mâu thuẫn xuyên chương và vị trí cần hiệu đính |
| T15 | Trích dẫn trực tiếp đúng nhưng cắt câu tác giả bác bỏ ngay sau | Báo ngữ cảnh thiếu, không cho qua đánh giá hỗ trợ luận điểm |
| T16 | Tài liệu được trích có hạn chế bản quyền/chia sẻ | Không tự gửi toàn văn cho mô hình bên ngoài hoặc xuất công khai khi chưa có quyền |

**Phải thử cả lỗi giả dương và âm tính giả:** Đếm nhầm nguồn không liên quan là có liên quan, đồng thời đếm sót nguồn đã biết tồn tại. Chấm riêng **tỷ lệ định vị đúng**, **độ bao phủ trích xuất**, **độ chính xác tìm lại nguồn**, **tỷ lệ dẫn chứng sai được chặn**, **chi phí/tốc độ**. Không gộp thành một điểm “độ chính xác AI” chung chung.

---

## 7. Quy tắc triển khai để giữ hệ thống đơn giản

**Bắt buộc trước khi dùng làm chứng cứ công bố (P0):**

- Giữ file gốc, ID ấn bản và hash; xác minh câu trích/locator độc lập với chỉ mục RAG.
- Ghi trạng thái bao phủ và lỗi OCR; kiểm các chỗ không đọc được trước khi nêu kết luận phủ định.
- Phân biệt văn bản với lịch sử; bản dịch với kinh song hành; từ với từng nghĩa; nhiều nguồn với nguồn độc lập.
- Chế độ 2 chỉ phân tích ngữ nghĩa trên chứng cứ thực; nguồn ngoài phân quyền và gắn mức tiếp cận; AI không được tự duyệt kết luận.
- Thử khôi phục dữ liệu và kiểm soát nguồn độc hại/quyền truy cập.

**Nên làm ngay sau khi bộ máy tra cứu cơ bản ổn định (P1):**

- Cải thiện đối chiếu phức tạp giữa truyền thống, rà nhất quán xuyên sách/từ điển, xuất chú thích chuyên sâu.
- Hiệu chỉnh từ điển đa ngữ, quy tắc tìm gần đúng và các bộ kiểm thử ngôn ngữ theo corpus thực tế.
- Theo dõi chi phí, kiểm lại phần bản thảo thay đổi thay vì chạy lại toàn bộ.

**Chưa cần bắt buộc (P2):** Knowledge graph quy mô lớn, agent tranh luận nhiều vòng, chưng cất toàn bộ sách bằng LLM, tự động viết/đánh giá toàn bộ từ điển không có người duyệt.

**Cách xây tiết kiệm:** Một catalog nguồn–ấn bản–nghĩa–quan hệ; một kho gốc; chỉ mục tìm kiếm phục vụ truy xuất; một lớp Citation Checker; quy trình AI Research tùy chọn. Tận dụng thành phần có sẵn, không nhân đôi database/agent chỉ để đáp ứng danh mục rủi ro.

---

## 8. Quy tắc ra quyết định khi kiểm chứng thất bại

Khi kết quả chưa đạt, hệ thống phải chọn **một hành động cụ thể**, thay vì tự viết cho đủ ý:

- **Thiếu nguồn:** Ghi danh sách nguồn cần bổ sung (tên, định danh, lý do, vị trí cần đọc, trạng thái tiếp cận); giữ câu ở mức giả thuyết hoặc bỏ khỏi bản thảo.
- **Có nguồn nhưng OCR/locator lỗi:** Đưa vào hàng chờ kiểm ảnh/ấn bản; không dẫn trang hoặc nguyên văn như đã xác minh.
- **Nguồn có ý trái chiều hoặc phụ thuộc nhau:** Ghi các hướng diễn giải, phân biệt chứng cứ độc lập và hạn chế kết luận.
- **Nguồn bên ngoài không truy cập được:** Dùng metadata để đề xuất tìm thêm; nếu dẫn gián tiếp phải ghi rõ nguồn trung gian; không bịa nội dung.
- **Nhận định quá mạnh:** Đề xuất cách viết thận trọng, giữ đúng chủ thể, phạm vi, thời kỳ và điều kiện được nguồn hỗ trợ.
- **Không có đủ căn cứ để quyết định:** `CHƯA ĐỦ CHỨNG CỨ / CẦN NGƯỜI DUYỆT` là kết quả đúng.

---

## 9. Mối quan hệ với Đề bài V1.4

- **V1.4 là tài liệu yêu cầu chính thức:** Mục tiêu, phạm vi, Chế độ 1/2, chức năng và tiêu chí nghiệm thu.
- **Sổ tay này là tài liệu kiểm soát chất lượng:** Các rủi ro cần thiết kế để tránh, trạng thái/đầu ra phải minh bạch, kiểm thử âm tính và ngưỡng không được công bố như đã xác minh.
- **Không mặc định phải lập trình toàn bộ các bảng/nhãn ở đây ngay:** Những nhãn và quality gates là **mẫu tham chiếu** để chuyển thành thiết kế phù hợp sau khi chọn công nghệ.
- **Khi hai tài liệu khác cách diễn đạt:** Giữ mục tiêu và phạm vi của V1.4; sử dụng sổ tay để diễn giải nguyên tắc an toàn. Nếu có xung đột thật, cập nhật hai tài liệu có kiểm soát, không âm thầm thay đổi yêu cầu.

**Tư tưởng xuyên suốt của BodhiAtlas:** *Nguồn thật trước — xác minh được mới dẫn — đánh giá học thuật phải có giới hạn — thiếu dữ liệu thì nói thiếu — AI chỉ hỗ trợ, không tạo bằng chứng.*
