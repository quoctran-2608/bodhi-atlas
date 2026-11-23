# P57 — Hồ sơ tái hiện thử nghiệm cô lập cho book-memex

**Báo cáo liên quan:** [P57 — book-memex](../../REPORT_57_BOOK_MEMEX.md)  
**Ngày nghiên cứu / log:** 23/11/2026 (Asia/Ho_Chi_Minh)  
**Trạng thái chứng cứ:** `[TESTED-ISOLATED]` cho phép thử SQLite FTS5 và PDF tổng hợp; **không phải** `[TESTED]` trên repo `queelius/book-memex`.

## Các tệp đi kèm

- [`P57_ISOLATED_POC.py`](P57_ISOLATED_POC.py) — mã Python của phép thử độc lập. SHA-256 tệp nguồn đính kèm: `af6271212c60f76a3f0d7eda26d2108b7c6b8d2c50cdd173b957fefdf0487fae`.
- [`P57_ISOLATED_POC.log`](P57_ISOLATED_POC.log) — nhật ký do người nghiên cứu cung cấp. SHA-256 tệp nguồn đính kèm: `0293918420b03d6462d859ed00421ebc786b4bd2cda8b5884101993a6a1478e7`.
- [Báo cáo nguyên văn](../../REPORT_57_BOOK_MEMEX.md) — Evidence Ledger 30 mục, C01–C15, TC01–TC15, các phương án A–F và điều kiện đảo quyết định.

## Thử nghiệm này cho biết điều gì?

Script tạo cơ sở dữ liệu SQLite FTS5 `porter unicode61` trong bộ nhớ, dùng một thuật toán làm sạch query được mô phỏng từ mã upstream, rồi so kết quả FTS với đối chiếu chuỗi ký tự gốc của Python trên các chuỗi **tổng hợp**. Nó cũng tạo PDF 3 trang tổng hợp và dùng `pypdf` trích text theo trang.

Nhật ký ghi ví dụ `anatta` / `anattā` có thể cùng được FTS chọn nhưng không khớp `EXACT` như nhau; truy vấn Hán một ký tự bị FTS bỏ sót trong fixture; **5 lần xuất hiện** `anatta` trong một row chỉ tạo **1 row FTS**; trang PDF thứ hai không có text layer. Các quan sát chỉ áp dụng cho chính fixture và phiên bản runtime đã ghi.

**Đã kiểm thử:** logic cô lập trên Python 3.13.5, SQLite 3.46.1, PyMuPDF 1.26.7 và pypdf 5.9.0 theo log cung cấp. **Chưa thực hiện:** `git clone`/cài và chạy toàn repo upstream, upstream `pytest`, browser PDF/EPUB, import đa ấn bản, G1/G2 và benchmark trên corpus thực.

## Chạy lại trên máy có Python

Trong môi trường cô lập với các phiên bản thư viện được ghim theo log:

```bash
python -m pip install "pypdf==5.9.0" "PyMuPDF==1.26.7"
python P57_ISOLATED_POC.py > P57_ISOLATED_POC.replayed.log
```

`sqlite3` có sẵn theo bản Python, nhưng cần kiểm Python/SQLite build và tính sẵn có của FTS5; log có thể khác trên phiên bản khác. Lệnh trên là **hướng dẫn chạy lại**, không phải một phép thử mới mà BodhiAtlas đã thực hiện.

## Ghi chú bảo toàn nguồn và liên kết

Các tệp báo cáo, mã thử nghiệm và log được lưu **không sửa nội dung**. Trong P57, một số liên kết tới BodhiAtlas dùng owner `quocgempro361/bodhi-atlas` thay vì repo thực tế [`quoctran-2608/bodhi-atlas`](https://github.com/quoctran-2608/bodhi-atlas). Đó là **tham chiếu cần kiểm tra/đính chính trước khi sử dụng**, không tự coi các URL gốc là khả dụng hoặc sửa âm thầm báo cáo. SHA ghim trong báo cáo cũng cần đối chiếu đường dẫn repo đúng.

**Kết luận nghiên cứu, không phải quyết định triển khai:** `USE AS COMPONENT` có điều kiện cho một số ý tưởng/thành phần của book-memex; đề xuất `D — Minimal BodhiAtlas Evidence Core` là ưu tiên cần được kiểm chứng và có thể đảo khi POC cùng tiêu chí chứng minh điều ngược lại.
