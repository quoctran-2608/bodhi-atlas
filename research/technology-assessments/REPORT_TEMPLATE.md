# Technology Assessment — <Tên đối tượng>

**Mã nghiên cứu:** P<NN>  
**Dự án nhận:** BodhiAtlas  
**Ngày khảo sát:** DD/MM/YYYY (Asia/Ho_Chi_Minh)  
**Ngày cập nhật:** DD/MM/YYYY  
**Đối tượng & loại:** <sản phẩm / thành phần / corpus / pattern / tiêu chuẩn>  
**Snapshot:** <version/tag/commit/release và thời điểm>  
**Trạng thái:** DỰ THẢO / ĐANG THẨM ĐỊNH / ĐÃ HOÀN TẤT KHẢO SÁT / CẦN CẬP NHẬT

> **Giới hạn phương pháp:** Nêu chính xác tài liệu, mã, môi trường và trường hợp thử đã/không tiếp cận. Không coi yêu cầu trong PRD là chức năng sẵn có của ứng viên.

## 1. Executive Decision

- **Khuyến nghị trong báo cáo:** ADOPT / USE AS COMPONENT / TRIAL ONLY / DEFER / REJECT / UNKNOWN.
- **Mức tin cậy và phạm vi:** ...
- **Vai trò phù hợp nhất trong BodhiAtlas:** ...
- **Rủi ro quyết định:** ...
- **Điều kiện cần thí nghiệm hoặc kiểm chứng tiếp:** ...

*Đây là đề xuất nghiên cứu, không phải quyết định chốt công nghệ.*

## 2. Sources & Evidence Ledger

Quy ước: `DOC` = đã đọc tài liệu; `CODE` = đã đọc code; `TESTED` = đã tự thực thi, có log; `ISSUE` = báo cáo lỗi; `INFERRED` = suy luận; `UNKNOWN` = chưa xác minh.

| ID | Nhận định | Loại chứng cứ | URL/file và vị trí | Snapshot/phiên bản | Giới hạn |
|---|---|---|---|---|---|
| E01 | ... | DOC/CODE/TESTED/ISSUE/INFERRED/UNKNOWN | ... | ... | ... |

## 3. Architecture & Data Flow

Mô tả **kiến trúc quan sát được** tách khỏi **phương án tích hợp đề xuất**. Ghi rõ thẩm quyền của file gốc, văn bản trích xuất, chỉ mục và chứng cứ.

## 4. Feature Fit–Gap Matrix

Đối chiếu theo **đúng vai trò đang khảo sát** với [PRD](../../docs/PRD.md) và [Quality Gates](../../docs/ACADEMIC_RISKS_AND_VERIFICATION.md). Phân biệt `NATIVE`, `CONFIG`, `EXTENSION`, `EXTERNAL`, `MISSING`, `UNKNOWN` và `N/A`; không tự suy đoán năng lực.

| Năng lực | Tình trạng | Chứng cứ | Khoảng trống/rủi ro | Cách kiểm thử |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## 5. Findings & Limitations

Những điểm mạnh, điểm yếu và rủi ro thực tế theo bằng chứng. Chú ý các vấn đề BodhiAtlas quan tâm: **nguyên văn, ấn bản, nguồn gốc, locator, độ bao phủ OCR, tìm đa ngữ, độ chính xác tìm kiếm và quyền sử dụng**.

## 6. So sánh đúng vai trò (nếu cần)

So sánh với những ứng viên có **cùng chức năng**. Không dùng số sao GitHub, số file hoặc benchmark quảng cáo làm chứng cứ nghiệm thu.

## 7. Security, Licensing & Data Rights

Phân biệt giấy phép code, model/weights, corpus, ấn bản/bản dịch, quyền lưu trữ, chia sẻ hoặc gửi tới AI. Không đưa dữ liệu mật hoặc nội bộ lên repo công khai.

## 8. Practical POC & Reproduction Plan

Ghi rõ fixture, corpus, phiên bản, environment, cấu hình, gold set, câu truy vấn âm/dương, bước chạy, log, chỉ số và tiêu chí đạt/trượt. **Tách thử nghiệm đã thực hiện khỏi kế hoạch tương lai.**

## 9. Open Questions / Unknowns

Liệt kê những giả định, khoảng trống chứng cứ, khả năng chưa kiểm và lý do chưa thể kết luận.

## 10. Final Assessment & Next Steps

- Đề xuất có điều kiện, phạm vi áp dụng.
- Các quality gate chưa qua và các công việc phải làm tiếp.
- Ngày, phiên bản và điều kiện cần thẩm định lại.
