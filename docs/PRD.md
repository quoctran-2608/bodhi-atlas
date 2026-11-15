# BodhiAtlas — ĐẶC TẢ YÊU CẦU SẢN PHẨM (PRD) V1.4

*Hệ thống thư viện tri thức và tra cứu học thuật*

## 1. MỤC TIÊU

Xây dựng một **thư viện tri thức tập trung**, có khả năng liên tục tiếp nhận, xử lý, phân loại và lập chỉ mục sách, tài liệu nghiên cứu để phục vụ tra cứu và nghiên cứu lâu dài.

**Năng lực quan trọng nhất:**

Khi nhập **một từ, thuật ngữ, cụm từ, đoạn văn, luận điểm hoặc luận đề**, hệ thống phải tìm được:

- Các nguồn khớp chính xác.
- Các nguồn gần giống về cách viết hoặc cách diễn đạt.
- Các nguồn liên quan thông qua thuật ngữ, bản dịch và quan hệ đã được xác định.
- Vị trí nguyên văn để kiểm chứng độc lập.

**Nguyên tắc:** Ưu tiên code và thuật toán tìm kiếm. Hạn chế AI tạo sinh để giảm ảo giác, tiết kiệm token và bảo đảm tính khách quan của dữ liệu nguồn.

AI chỉ là chế độ hỗ trợ nâng cao, không phải điều kiện bắt buộc để tra cứu thông thường.

**Ứng dụng trọng tâm:** Viết sách Phật học liên ngành (kinh điển, lịch sử, văn hóa, văn học, khảo cổ...) và biên soạn từ điển Phật học. Hệ thống phải phân biệt **điều một nguồn văn bản ghi lại** với **điều có thể kết luận về lịch sử hoặc giáo lý**; không đánh đồng sự tồn tại của câu trích với tính đúng đắn của luận điểm.

---

## 2. THƯ VIỆN TẬP TRUNG, CÓ PHÂN LOẠI VÀ LIÊN KẾT

### 2.1. Quản lý tài liệu

Lưu trữ và quản lý thống nhất:

- Sách gốc: PDF, EPUB, DOCX và các định dạng khác.
- Nhiều bản dịch, ngôn ngữ, ấn bản, dị bản của cùng một tác phẩm.
- Văn bản trích xuất, OCR, dữ liệu đã xử lý và chỉ mục.
- Bài nghiên cứu, chú giải, phân tích, bản thảo, mục từ điển và các sản phẩm phái sinh.
- Nguồn Internet, bài báo, website và tài liệu tham khảo liên quan.
- Khi phục vụ nghiên cứu liên ngành: tư liệu bia ký, bản thảo cổ, hình ảnh hiện vật, bản đồ, hồ sơ di tích và báo cáo khảo cổ; ít nhất phải quản lý được file, metadata và nguồn gốc, không mặc định có thể trích xuất tự động toàn bộ nội dung.

Mỗi tác phẩm, bản dịch, ấn bản và file có định danh riêng, đồng thời liên kết được với nhau.

Một bài nghiên cứu có thể liên kết tới nhiều sách, nhiều ấn bản và các đoạn văn cụ thể đã sử dụng.

### 2.2. Phân loại thư viện

Hỗ trợ hệ thống phân loại nhiều cấp:

**Lĩnh vực → Chủ đề → Chủ đề con → Chủ đề chi tiết.**

Ví dụ:

- Phật học → Phật học Nguyên thủy → Kinh Nikāya.
- Phật học → Phật học Đại thừa → Trung quán.
- Lịch sử → Lịch sử Việt Nam → Thời Trần.
- Địa lý → Địa lý tự nhiên → Khí hậu.

Yêu cầu:

- Một tài liệu có thể thuộc nhiều chủ đề.
- Phân biệt chủ đề nội dung với thể loại tài liệu: kinh điển, từ điển, nghiên cứu, giáo trình, luận văn...
- Có tag linh hoạt để bổ sung đặc điểm hoặc chủ đề chuyên biệt.
- Hỗ trợ phân loại tự động theo quy tắc, metadata và từ điển đã xác minh.
- Cho phép người dùng điều chỉnh, hợp nhất và bổ sung hệ thống phân loại.
- Quản lý riêng **truyền thống, thời kỳ, khu vực địa lý và loại nguồn** khi có dữ liệu; không mặc định các nhãn “Phật giáo sơ kỳ”, “Theravāda”, “Nam truyền”, “Bắc truyền”, “Đại thừa” là đồng nghĩa hoặc loại trừ nhau.

### 2.3. Nguồn học thuật và quan hệ văn bản

- Phân biệt **kinh điển, bản dịch, chú giải, sử liệu, văn học, nghiên cứu hiện đại, chứng cứ vật chất/khảo cổ và nguồn dẫn gián tiếp**; ghi rõ tác giả, truyền thống, niên đại và xuất xứ khi xác định được.
- Ghi quan hệ **bản dịch, ấn bản, dị bản, nhân chứng văn bản (witness), kinh song hành, chú giải, trích dẫn và nguồn phái sinh**. Quan hệ song hành/giống nhau một phần **không mặc nhiên là hai bản dịch tương đương hoàn toàn**.
- Với nhận định lịch sử, phân biệt **niên đại sự kiện, niên đại biên soạn, niên đại bản chép/bản dịch, niên đại hiện vật**; cho phép khoảng niên đại, cách xác định và ý kiến còn tranh luận.
- Mỗi quan hệ hoặc dữ kiện quan trọng có thể mang nguồn xác nhận và trạng thái **đã xác minh / đề xuất / chưa rõ**, không mặc định đề xuất của AI là sự thật.

### 2.4. Mục từ và nghĩa thuật ngữ Phật học

- Một **mục từ** có thể có nhiều **nghĩa**; mỗi nghĩa liên kết riêng với cách dùng, truyền thống, văn cảnh, bản dịch và dẫn chứng.
- Quản lý từ nguyên ngữ, chữ viết, phiên tự, biến thể chính tả, thuật ngữ tương ứng và các quan hệ **đồng nghĩa có điều kiện / gần nghĩa / khác nghĩa**.
- Không gộp các nghĩa chỉ vì cùng cách viết hoặc cùng một từ dịch, đặc biệt khi đối chiếu Pāli, Sanskrit, Hán, Tạng, Việt và Anh.

---

## 3. TỰ ĐỘNG NẠP VÀ “TIÊU HÓA” TÀI LIỆU

Quy trình mong muốn:

**Nạp tài liệu → Trích xuất/OCR → Nhận diện cấu trúc → Phân loại → Lập chỉ mục → Kiểm tra → Sẵn sàng tra cứu.**

Hệ thống phải:

1. Nhận một hoặc nhiều tài liệu, hỗ trợ bổ sung thường xuyên.
2. Tự phát hiện định dạng, ngôn ngữ, file trùng và phiên bản mới.
3. Trích xuất chính xác văn bản; OCR tài liệu scan khi cần.
4. Nhận diện chương, mục, đoạn, mục từ, chú thích và số trang khi có thể.
5. Giữ nguyên văn bản gốc và vị trí nguồn.
6. Tạo chỉ mục tìm kiếm phù hợp với từng hệ chữ/ngôn ngữ.
7. Tự cập nhật chỉ mục khi có tài liệu mới, tránh xử lý lại những tài liệu không thay đổi.
8. Kiểm tra độ bao phủ, ghi nhận lỗi và những phần chưa xử lý được.
9. Báo rõ **trang/đoạn bị thiếu, OCR chất lượng thấp, chú thích/bảng/cột chưa đọc được**, đồng thời bảo toàn liên kết từ văn bản trích xuất về trang/đoạn nguồn.
10. Với tư liệu hình ảnh, bản thảo cổ hoặc hiện vật chưa thể đọc máy đáng tin cậy, cho phép **tra metadata và mô tả đã xác minh**, không giả có toàn văn.

**Không bắt buộc dùng LLM để đọc, tóm tắt hoặc phân tích toàn bộ sách khi nhập.**

Mục tiêu của quá trình tiêu hóa cơ bản là biến tài liệu thành dữ liệu **dễ tìm, chính xác và có thể truy nguyên**, không phải tự động tạo ra những lời diễn giải về nội dung sách.

---

## 4. NĂNG LỰC TRA CỨU — TRỌNG TÂM CỦA HỆ THỐNG

### 4.1. Tìm kiếm nguyên văn chính xác

Nhập một từ, cụm từ hoặc đoạn văn để tìm tất cả vị trí xuất hiện trong phạm vi dữ liệu đã lập chỉ mục.

Yêu cầu:

- Khớp nguyên văn, kể cả dấu và ký tự gốc.
- Tìm được các lần xuất hiện trong nhiều tài liệu.
- Hỗ trợ đoạn văn dài, khác biệt xuống dòng hoặc khoảng trắng khi chọn chế độ phù hợp.
- Lọc theo tác phẩm, ấn bản, ngôn ngữ, chủ đề, tác giả, thể loại...
- Trả về nguyên văn, ngữ cảnh và vị trí nguồn.

Đây là chế độ có độ ưu tiên cao nhất.

### 4.2. Tìm kiếm không dấu, biến thể và gần đúng — KHÔNG CẦN LLM

Đây là chức năng bắt buộc, sử dụng thuật toán và dữ liệu ngôn ngữ.

**A. Tiếng Việt**

- Nhập không dấu vẫn tìm được văn bản có dấu: `vo thuong` → `vô thường`.
- Hỗ trợ khác biệt dấu, chữ hoa/thường, khoảng trắng và dấu câu.
- Tìm được những cách viết gần giống và lỗi gõ thông dụng.
- Với từ không dấu có nhiều cách hiểu, trả về các khả năng phù hợp; không tự khẳng định một cách hiểu duy nhất.

**B. Tiếng Hán**

- Hỗ trợ Hán phồn thể và giản thể: `無常` ↔ `无常`.
- Tìm kiếm chữ Hán không phụ thuộc vào việc tách từ theo khoảng trắng.
- Hỗ trợ các dị thể chữ, cách viết và thuật ngữ Hán đã được xác nhận.
- Hỗ trợ đối chiếu Hán–Việt và các thuật ngữ tương ứng khi có từ điển liên kết đáng tin cậy.

**C. Tiếng Tạng**

- Tìm kiếm trực tiếp bằng chữ Tạng Unicode.
- Hỗ trợ chuẩn hóa các khác biệt Unicode và dấu phân cách phù hợp.
- Hỗ trợ phiên tự Wylie và tìm tương ứng với chữ Tạng khi có quy tắc chuyển tự phù hợp.
- Hỗ trợ tìm cụm từ, thuật ngữ và các biến thể từ vựng/hình thái khi có dữ liệu hoặc công cụ phân tích ngôn ngữ phù hợp.

**D. Pāli và Sanskrit**

- Tìm được cả dạng có và không có dấu phụ khi phù hợp: `nibbāna` / `nibbana`.
- Hỗ trợ các cách chuyển tự, biến thể chính tả và hình thái từ đã xác định.
- Hỗ trợ Unicode và các hệ chữ có liên quan nếu được bổ sung.
- Không tự coi hai thuật ngữ gần giống là đồng nghĩa.

**E. Tiếng Anh và những ngôn ngữ khác**

- Không phân biệt chữ hoa/thường khi cần.
- Hỗ trợ số ít/số nhiều, dạng biến đổi của từ.
- Hỗ trợ stemming, lemmatization hoặc từ điển hình thái phù hợp.
- Tìm gần đúng khi sai chính tả hoặc khác một số từ.

**F. Tìm đoạn văn gần giống**

Hỗ trợ tìm khi nội dung có:

- Một vài từ khác nhau hoặc bị thiếu.
- Thứ tự từ thay đổi trong giới hạn xác định.
- Khác dấu câu, xuống dòng hoặc cách trình bày.
- Lỗi OCR.
- Các phiên bản văn bản có mức độ tương đồng cao.

Kết quả phải được xếp hạng theo mức độ khớp và hiển thị phần sai khác để người dùng kiểm tra.

**Nguyên tắc kỹ thuật quan trọng:** Luôn bảo toàn nguyên văn. Mọi dạng bỏ dấu, chuẩn hóa, chuyển tự hoặc sửa lỗi chỉ dùng để tạo chỉ mục và tìm ứng viên; không sửa trực tiếp câu chữ nguồn.

### 4.3. Tìm kiếm xuyên ngôn ngữ

Cho phép nhập thuật ngữ bằng một ngôn ngữ và tìm các thuật ngữ tương ứng trong những ngôn ngữ khác khi có dữ liệu liên kết.

Ví dụ:

`dukkha` ↔ `khổ` ↔ `苦` ↔ `suffering` ↔ `duḥkha`.

Các liên kết được xây dựng từ:

- Từ điển và bảng thuật ngữ đáng tin cậy.
- Quy tắc chuyển tự.
- Quan hệ bản dịch đã xác minh.
- Corpus song ngữ hoặc đa ngữ đã được đối chiếu.

**Không tự động xem mọi từ có nghĩa gần nhau là hoàn toàn tương đương.**

Quan hệ đa ngôn ngữ cần ghi rõ nguồn, **nghĩa cụ thể**, phạm vi sử dụng và mức độ xác nhận. Kết quả từ điển phải cho phép lọc **theo nghĩa, truyền thống và văn cảnh**, không chỉ theo cách viết.

### 4.4. Tìm nguồn cho luận điểm, luận đề

Người dùng có thể nhập một nhận định hoặc vấn đề nghiên cứu dài hơn từ khóa thông thường.

Ví dụ:

“Khổ có phải hoàn toàn do nghiệp quá khứ gây ra không?”

Hệ thống cần:

1. Trích ra những thuật ngữ, cụm từ và điều kiện quan trọng bằng quy tắc hoặc thuật toán phù hợp.
2. Tìm các nguồn khớp từ vựng và biến thể liên quan.
3. Mở rộng bằng từ điển thuật ngữ và quan hệ đã xác nhận.
4. Trả về các đoạn nguồn ứng viên, kèm nguyên văn và ngữ cảnh.
5. Cho biết mức độ khớp, phạm vi đã tìm kiếm và **những nguồn chưa được lập chỉ mục hoặc không đọc được** nếu có.

**Code thuần có thể tìm nguồn liên quan, nhưng không thể bảo đảm hiểu đúng mọi luận điểm phức tạp hoặc tìm đủ mọi cách diễn đạt tương đương.**

Không được mặc định một nguồn tìm thấy là bằng chứng hỗ trợ hoặc bác bỏ luận điểm.

### 4.5. Phân biệt rõ các loại kết quả

Hệ thống phải thể hiện kết quả thuộc loại nào:

- **EXACT:** Khớp nguyên văn.
- **NORMALIZED:** Khớp sau chuẩn hóa, như bỏ dấu hoặc chuẩn Unicode.
- **FUZZY:** Gần giống về chữ/cấu trúc.
- **LEXICON:** Liên quan qua từ điển thuật ngữ hoặc quan hệ đã xác nhận.
- **SEMANTIC:** Tương đồng ngữ nghĩa, khi bật công cụ thích hợp.

Điểm xếp hạng là điểm phù hợp để tìm kiếm, **không phải xác suất một luận điểm đúng**.

---

## 5. TRUY NGUYÊN VÀ KIỂM CHỨNG NGUỒN

Mỗi kết quả phải có khả năng dẫn về:

- Đúng tác phẩm, ngôn ngữ, dịch giả và ấn bản.
- Đúng file gốc, định danh và SHA-256.
- Đúng chương, mục, đoạn, số trang hoặc mã định vị khi có dữ liệu.
- Nguyên văn và ngữ cảnh đầy đủ để đối chiếu.
- **Loại nguồn** (kinh điển, chú giải, sử liệu, khảo cổ, nghiên cứu...), vai trò văn bản (nguyên bản, bản dịch, chú thích, lời dẫn gián tiếp) và trạng thái kiểm chứng khi có.

Hệ thống cần phân biệt:

1. **Khớp văn bản:** Câu có thật trong nguồn không?
2. **Khớp vị trí:** Có đúng bản sách, trang, đoạn không?
3. **Khớp ngữ cảnh:** Có bị bỏ sót điều kiện, ngoại lệ hoặc ý phủ định không?
4. **Hỗ trợ luận điểm:** Bằng chứng có thực sự chứng minh điều được nêu không?

Hai bước đầu ưu tiên code để kiểm chứng. Hai bước sau có thể cần người nghiên cứu hoặc AI hỗ trợ.

**Nguyên tắc phê bình nguồn:** Một kinh văn ghi lại câu chuyện không tự chứng minh câu chuyện là sự kiện lịch sử; một nguồn uy tín không tự chứng minh mọi luận điểm gán cho nó. Khi đánh giá chứng cứ, phải xét **loại nhận định, độ trực tiếp của nguồn, sự phụ thuộc giữa các nguồn, niên đại, ngữ cảnh và những cách diễn giải còn tranh luận**.

**Yêu cầu về độ chính xác:** Không chấp nhận dẫn chứng sai được trình bày như đã xác minh. Nếu chưa xác định được vị trí, OCR chưa đủ tin cậy hoặc tài liệu chưa được lập chỉ mục đầy đủ, phải báo rõ.

Không cam kết tìm được tuyệt đối mọi nguồn liên quan trong tất cả tài liệu nếu chưa có dữ liệu đầy đủ. **“Không tìm thấy trong phạm vi đã kiểm” khác với “không tồn tại trong kinh điển/lịch sử”**; hệ thống phải ghi lại phạm vi đã tìm và những giới hạn về nguồn, OCR, chỉ mục.

---

## 6. HAI CHẾ ĐỘ HOẠT ĐỘNG

### 6.1. CHẾ ĐỘ 1 — TRA CỨU VÀ KIỂM CHỨNG NGUỒN BẰNG CODE (MẶC ĐỊNH)

**Mục tiêu:** Tìm đúng tài liệu, đúng đoạn văn, phát hiện các nguồn liên quan và xác minh câu trích có thực sự tồn tại trong nguồn được khai báo; **không cần LLM tạo sinh**.

**Năng lực:**

- Tìm nguyên văn, không dấu, biến thể chính tả, gần đúng và đa ngôn ngữ theo các yêu cầu tại Mục 4.
- Mở rộng truy vấn qua từ điển thuật ngữ, bản dịch và những quan hệ đã xác nhận; phân biệt rõ kết quả `EXACT`, `NORMALIZED`, `FUZZY`, `LEXICON`.
- Truy xuất đoạn văn, ngữ cảnh, metadata, thể loại, chủ đề, tag và quan hệ tài liệu.
- Tra bằng code theo **nghĩa của mục từ, truyền thống, niên đại/địa điểm, loại nguồn, kinh song hành, dị bản và nhân chứng văn bản** khi có dữ liệu đã xác minh; không tự đồng nhất các văn bản liên quan.
- Kiểm tra câu trích bằng cách mở lại nguồn độc lập: đối chiếu nguyên văn, ấn bản, vị trí, hash và độ bao phủ trích xuất/OCR.
- Phát hiện trích sai, nguồn không khớp, vị trí không xác minh được hoặc không tìm thấy; trả về trạng thái và lý do cụ thể.
- Phân biệt **không có kết quả trong phạm vi đã kiểm**, **tài liệu thiếu/chưa lập chỉ mục**, **OCR/parsing lỗi** và **chưa tiếp cận nguồn**; không suy ra sự vắng mặt của chứng cứ trên toàn bộ truyền thống.

**Giới hạn:** Kết quả tìm kiếm chỉ là **nguồn ứng viên**; khớp từ ngữ không chứng minh một luận điểm. Chế độ 1 không tự kết luận lập luận phức tạp đúng/sai, không tự đánh giá đầy đủ ngữ cảnh và không tạo nguồn thay thế khi thiếu dữ liệu. Việc kiểm chứng vị trí chỉ đạt mức xác nhận khi văn bản nguồn và bộ định vị đủ tin cậy.

### 6.2. CHẾ ĐỘ 2 — AI RESEARCH VÀ KIỂM CHỨNG HỌC THUẬT (TÙY CHỌN)

**Mục tiêu:** Sử dụng năng lực suy luận của AI ở những bước Chế độ 1 không thể giải quyết đầy đủ, đặc biệt khi **kiểm chứng bản thảo do AI/con người viết** và **nghiên cứu một luận đề chưa đủ bằng chứng**. Mọi bước truy xuất nguyên văn và xác minh kỹ thuật vẫn phải dùng Chế độ 1 trước.

#### A. Kiểm chứng bản thảo — ưu tiên số một

**Đầu vào:** Đoạn văn, mục từ, bài nghiên cứu hoặc chương sách đã viết, có hoặc không có trích dẫn.

**Quy trình:**

1. AI tách các nhận định quan trọng thành mệnh đề đủ rõ để kiểm tra; giữ nguyên điều kiện, phạm vi, chủ thể phát ngôn, lượng từ và quan hệ nhân quả.
2. Chế độ 1 kiểm tra những câu trích và vị trí nguồn đã khai báo; tìm thêm các đoạn ứng viên trong thư viện bằng code.
3. AI đọc ngữ cảnh để đánh giá mỗi chứng cứ **hỗ trợ, giới hạn hay trái chiều** với từng mệnh đề, đồng thời tìm các ngoại lệ và lập luận phản bác.
4. Kiểm tra nguy cơ nhầm bản dịch/ấn bản, lấy lời được thuật lại thành quan điểm được tán thành, khái quát hóa quá mức, suy diễn quan hệ nhân quả hoặc bỏ sót điều kiện; **phân biệt tường thuật kinh điển, lập luận giáo lý và khẳng định lịch sử/khảo cổ**.
5. Xuất báo cáo **theo từng nhận định**: câu gốc, nguồn đã đối chiếu, đoạn chứng cứ và vị trí, loại chứng cứ, đánh giá ngữ nghĩa, điểm chưa chắc, phản chứng và đề xuất hiệu đính.
6. Khi kiểm cả chương hoặc công trình, kiểm tra **mâu thuẫn giữa các chương, dùng thuật ngữ/định nghĩa không nhất quán và dẫn chứng trùng nguồn nhưng bị đếm như độc lập**.

**Không được:** Gắn nhãn “đã chứng minh” chỉ vì một đoạn có từ khóa phù hợp hoặc vì AI tự đồng ý với câu mình vừa viết.

#### B. Nghiên cứu một vấn đề hoặc luận đề

**Đầu vào:** Câu hỏi, giả thuyết, luận điểm hoặc chủ đề nghiên cứu.

- Tìm nguồn trong thư viện bằng Chế độ 1; chỉ sử dụng semantic search/embeddings khi tìm bằng thuật toán chưa đủ.
- Đối chiếu nguyên bản, bản dịch, chú giải, nghiên cứu và các quan điểm khác biệt; không đếm những bản dịch hay bài viết phụ thuộc cùng một nguồn thành nhiều chứng cứ độc lập.
- Khi nghiên cứu xuyên truyền thống, phân biệt **kinh song hành, dị bản, bản dịch**, không mặc định tương đương từng câu; phân biệt **sự kiện lịch sử, niên đại văn bản, tư liệu khảo cổ và giả thuyết của học giả**.
- Ghi rõ **phần đã kiểm, phần chưa kiểm và khoảng trống chứng cứ**. Không suy ra “không tồn tại nguồn” chỉ vì tìm không thấy trong phạm vi đã tra.
- Tổng hợp thành hồ sơ nghiên cứu có thể truy nguyên, không ép hệ thống phải đưa ra kết luận khi chưa đủ căn cứ.

#### C. Mở rộng ra nguồn bên ngoài — có quyền hạn và kiểm soát

**Chỉ mở rộng khi có lý do cụ thể**: thư viện thiếu nguồn gốc, thiếu bản dịch/ấn bản, thiếu góc nhìn độc lập, có dấu hiệu mâu thuẫn hoặc chưa đủ chứng cứ để đánh giá một nhận định.

Người dùng chọn một trong ba mức quyền:

1. **Chỉ thư viện:** Không truy cập Internet hoặc nguồn ngoài.
2. **Tìm và đề xuất:** Được tìm tài liệu ngoài và báo những nguồn nên bổ sung; chưa dùng chúng làm chứng cứ cho kết luận chính.
3. **Nghiên cứu mở rộng:** Được đọc và sử dụng **nội dung nguồn ngoài đã trực tiếp kiểm chứng**, ghi nhãn riêng với nguồn nội bộ. Không tự động nhập tài liệu vào kho lâu dài nếu chưa được cho phép và kiểm tra quyền sử dụng.

**Quy tắc kiểm soát chứng cứ bên ngoài:**

- **Đã đọc và đối chiếu nguồn:** Xác minh được tài liệu, phiên bản, đoạn liên quan và ngữ cảnh; có thể dùng làm chứng cứ với URL/định danh, ngày truy cập, vị trí và hồ sơ truy xuất.
- **Chỉ xác minh thư mục:** Có tên sách, tác giả, DOI/ISBN hoặc thông tin catalog nhưng chưa đọc được nội dung liên quan; **chỉ là nguồn cần tìm**, không phải bằng chứng hỗ trợ luận điểm.
- **Nguồn dẫn gián tiếp:** Chỉ đọc được lời trích qua tác phẩm trung gian; phải ghi “dẫn theo”, không tuyên bố đã kiểm chứng trực tiếp bản gốc.
- **Trí nhớ hoặc suy đoán của AI:** Chỉ được dùng để đề xuất hướng tìm; **không được tạo câu trích, số trang, nguồn hay kết luận dựa trên đó**.

Nếu không tìm hoặc không đọc được toàn văn cần thiết, hệ thống phải báo **chưa đủ chứng cứ**, đề xuất tìm tài liệu, sử dụng nguồn gián tiếp có ghi hạn chế khi phù hợp hoặc thu hẹp/sửa nhận định. **Không tự lấp khoảng trống bằng kiến thức mô hình.**

Nguồn ngoài hữu ích được thêm vào **danh sách đề xuất bổ sung thư viện** với metadata đã xác minh, đường dẫn, lý do cần, phần cần kiểm, tình trạng truy cập và trạng thái bằng chứng. Khi người dùng nạp thêm nguồn, liên kết nó với câu hỏi/luận điểm trước đó để kiểm tra tiếp.

#### D. Hiệu đính, biên soạn từ điển và tích lũy kết quả

- Khi làm từ điển, hỗ trợ soạn và rà **từng nghĩa của mục từ**, cách dịch và dẫn chứng tương ứng; phát hiện định nghĩa trùng lặp, mâu thuẫn hoặc sử dụng sai ngữ cảnh.
- Hỗ trợ kiểm tra **tính nhất quán xuyên chương/mục từ**, liên kết chú thích và xuất danh mục tài liệu tham khảo hoặc hồ sơ chứng cứ để phục vụ biên tập/xuất bản.
- Đề xuất sửa những nhận định quá mạnh, sai nguồn hoặc thiếu điều kiện; **không tự ghi đè bản thảo gốc**.
- Lưu từng luận điểm, đoạn chứng cứ, phản chứng, kết quả thẩm định, nguồn bên ngoài và những vấn đề chưa giải quyết; liên kết đến đúng tác phẩm/ấn bản/đoạn nguồn.
- Tái sử dụng kết quả còn hiệu lực; khi bản thảo hoặc nguồn thay đổi, ưu tiên kiểm lại phần bị ảnh hưởng thay vì chạy lại toàn bộ.

#### E. Ranh giới tin cậy, đầu ra và chi phí

- **Tách hai kết quả:** (1) Kiểm chứng văn bản/vị trí bằng code; (2) Đánh giá **ý nghĩa và sức nặng chứng cứ** do AI đề xuất. Kết quả thứ hai không tự trở thành phê duyệt học thuật.
- Đánh giá theo từng nhận định, chẳng hạn: `HỖ TRỢ RÕ`, `HỖ TRỢ MỘT PHẦN`, `CÓ CHỨNG CỨ TRÁI CHIỀU`, `CHƯA ĐỦ CHỨNG CỨ`, `CHƯA THỂ KIỂM CHỨNG`. Luôn kèm căn cứ và giới hạn; không biến điểm tìm kiếm thành xác suất đúng.
- Báo cáo tối thiểu gồm: **nhận định → bằng chứng/nguồn → trạng thái xác minh → đánh giá → phản chứng/giới hạn → khuyến nghị**. Phân biệt nguồn nội bộ, ngoài thư viện, gián tiếp và chưa xác minh.
- Ưu tiên kiểm sâu các nhận định quan trọng hoặc rủi ro cao; giới hạn phạm vi, số lượt tìm ngoài và chi phí mô hình. Các tra cứu thông thường vẫn dùng Chế độ 1.
- AI có thể là ChatGPT, Claude, Javis hoặc hệ thống khác dùng API/MCP; không khóa vào một mô hình. Người dùng có quyền xem nguồn và chấp thuận những kết luận quan trọng trước khi sử dụng để công bố.

**Nguyên tắc bất biến:** **AI được phép đề xuất cách hiểu, giả thuyết và nguồn mới; nhưng không được tự tạo chứng cứ, tự nâng mức kiểm chứng hoặc che giấu tình trạng thiếu tài liệu.** Đánh giá học thuật của AI luôn là đề xuất cần xem xét; bằng chứng đúng nguyên văn không tự chứng minh tính đúng lịch sử hoặc lập luận.

---

## 7. KIẾN TRÚC VÀ TIÊU CHÍ NGHIỆM THU

### Yêu cầu kiến trúc

- Một kho tài liệu gốc tập trung, ưu tiên cloud.
- Một catalog quản lý tác phẩm, phiên bản, phân loại, tag và quan hệ.
- Một hệ thống tìm kiếm chính, kết hợp các chỉ mục phù hợp với từng ngôn ngữ.
- Một API/MCP chung cho ChatGPT, Claude, Javis và AI khác.
- Một giao diện thuận tiện cho người dùng.
- Có thể mở rộng và thay thế các thành phần mà không mất dữ liệu gốc.
- Đủ khả năng **sao lưu/phục hồi catalog, nguồn gốc, quan hệ, nghĩa thuật ngữ và lịch sử nghiên cứu**; kiểm soát quyền sử dụng tư liệu khi lưu, gửi cho AI hoặc xuất bản.
- Ưu tiên phần mềm sẵn có; hạn chế tự phát triển, trùng lặp và phụ thuộc nhà cung cấp.

### Các bài kiểm tra bắt buộc

Hệ thống phải được thử với PDF văn bản, PDF scan, EPUB, tài liệu đa ngôn ngữ và nhiều ấn bản.

Cần chứng minh được:

1. Nạp sách mới và tự động xử lý, lập chỉ mục.
2. Tìm tiếng Việt có dấu và không dấu.
3. Tìm chữ Hán phồn thể, giản thể và các cụm Hán văn.
4. Tìm chữ Tạng và phiên tự Wylie trong phạm vi hỗ trợ.
5. Tìm Pāli/Sanskrit có và không có dấu phụ.
6. Tìm tiếng Anh và các biến thể hình thái thông dụng.
7. Tìm được những đoạn văn gần giống, kể cả khác dấu câu và lỗi OCR ở mức xác định.
8. Phân biệt chính xác kết quả nguyên văn, chuẩn hóa, fuzzy, từ điển và semantic.
9. Truy ngược được câu trích về đúng file, ấn bản và vị trí.
10. Trả kết quả hữu ích khi nhập một luận điểm nhưng không tự nhận đã chứng minh luận điểm.
11. Phân loại được tài liệu theo chủ đề nhiều cấp, thể loại và tag.
12. Người dùng và AI có thể dùng chung hệ thống mà không phải lập chỉ mục riêng.
13. Chi phí tra cứu thông thường thấp, không cần LLM.
14. Truy vấn một mục từ đa nghĩa và nhận được **các nghĩa cùng dẫn chứng riêng**, không gộp nhầm từ tương ứng đa ngôn ngữ.
15. Đối chiếu kinh Nikāya/A-hàm hoặc văn bản song hành, **phân biệt đúng quan hệ song hành, dị bản và bản dịch**, hiển thị điểm khác biệt khi dữ liệu cho phép.
16. Kiểm một nhận định về lịch sử Phật giáo: **phân biệt nội dung kinh văn, sử liệu, niên đại bản chép và chứng cứ khảo cổ**; báo tranh luận khi chưa đủ căn cứ.
17. Khi thiếu trang, OCR lỗi hoặc chưa nhập một nguồn, hệ thống **không kết luận “không tồn tại chứng cứ”** mà thể hiện giới hạn rõ ràng.
18. Kiểm một chương sách AI viết để phát hiện **nhận định thiếu nguồn, suy diễn quá mức, sai ngữ cảnh và mâu thuẫn với chương/mục từ khác**; nguồn ngoài chưa đọc không được đưa thành chứng cứ.
19. Xuất được **báo cáo kiểm chứng theo từng nhận định, chú thích/danh mục nguồn và hồ sơ truy nguyên** để phục vụ hiệu đính.

Đo lường độ bao phủ, độ chính xác định vị, khả năng tìm lại nguồn đã biết, tốc độ và chi phí trên bộ dữ liệu kiểm thử thực tế.

---

## KẾT LUẬN — YÊU CẦU CỐT LÕI

**Tôi cần một thư viện tri thức có khả năng tự tiếp nhận và tiêu hóa sách mới, phân loại và liên kết tài liệu, rồi cho phép tra cứu chính xác hoặc gần đúng ở nhiều ngôn ngữ — chủ yếu bằng code, không phụ thuộc AI.**

Khi nhập một từ, đoạn văn hoặc luận điểm, hệ thống phải tìm được những nguồn phù hợp nhất, phân biệt rõ mức độ và kiểu tương đồng, đồng thời cung cấp nguyên văn cùng vị trí để kiểm tra.

Khi công việc đòi hỏi hiểu sâu, so sánh quan điểm, phản biện hoặc biên soạn, tôi có thể bật chế độ AI Research. Hệ thống phải phục vụ **cả viết sách Phật học liên ngành lẫn biên soạn từ điển theo từng nghĩa**, đồng thời phân biệt chứng cứ văn bản, dữ kiện lịch sử và diễn giải học thuật.

**Ưu tiên số một: Tìm đúng nguồn, kiểm chứng được.**

**Ưu tiên số hai: Nạp và xử lý tài liệu tự động, liên tục.**

**Ưu tiên số ba: Đơn giản, tiết kiệm, mở rộng lâu dài và độc lập với nhà cung cấp AI.**
