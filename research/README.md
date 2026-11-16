# Không gian nghiên cứu công nghệ — BodhiAtlas

**Ngày khởi tạo:** 16/11/2026  
**Trạng thái:** Nghiên cứu và thẩm định — **chưa phải quyết định chọn công nghệ**  
**Phạm vi:** Khảo sát sản phẩm, thành phần, mô hình thiết kế và các tài sản kỹ thuật có thể tái sử dụng.

## Mục đích

Đây là nơi lưu giữ các **báo cáo nghiên cứu có dẫn chứng**, nhằm đánh giá khách quan mức độ phù hợp với những yêu cầu của BodhiAtlas. Các báo cáo có thể đề xuất thử nghiệm, sử dụng một thành phần, hoãn hoặc từ chối một phương án; **không** tự biến khuyến nghị đó thành quyết định triển khai.

**Bắt đầu tại:** [Danh mục thẩm định công nghệ](technology-assessments/README.md).

## Quan hệ với các tài liệu chính

| Tài liệu | Vai trò |
|---|---|
| [PRD v1.4](../docs/PRD.md) | Yêu cầu sản phẩm và tiêu chí nghiệm thu chính thức |
| [V1 Core Foundation](../docs/V1_CORE_FOUNDATION.md) | Định hướng thiết kế nền tảng; không chốt công nghệ |
| [Academic Risks & Verification](../docs/ACADEMIC_RISKS_AND_VERIFICATION.md) | Rủi ro, giới hạn chứng cứ và các cổng chất lượng |
| **Báo cáo trong `research/`** | Đánh giá phương án theo bằng chứng, phạm vi khảo sát và mức độ chưa chắc chắn |

## Các quy tắc sử dụng

1. So sánh từng ứng viên **theo đúng vai trò**, ví dụ bộ nạp tài liệu, bộ máy tìm kiếm, công cụ thư mục, kho corpus hoặc mô hình Second Brain; không cộng điểm tổng cho các chức năng không thuộc phạm vi của nó.
2. Phân biệt **đã đọc tài liệu** (`DOC`), **đã đọc mã** (`CODE`), **đã tự chạy thử có log** (`TESTED`), **báo cáo lỗi** (`ISSUE`), **suy luận** (`INFERRED`) và **chưa xác minh** (`UNKNOWN`).
3. Ghi **ngày khảo sát, phiên bản, commit hoặc snapshot, phạm vi đã đọc, điểm chưa thử và điều kiện đánh giá lại**. Không suy diễn rằng công cụ sẽ luôn giống thời điểm khảo sát.
4. Một nhận định `USE AS COMPONENT` là **khuyến nghị của báo cáo**, không phải phê duyệt tích hợp, nghiệm thu G1–G6 hay lựa chọn kiến trúc chính thức.
5. Giữ nguyên các báo cáo nguồn đã nhập. Khi cần cập nhật, tạo commit có mô tả, ghi ngày cập nhật/phạm vi và bảo toàn khả năng truy xuất bản trước.

## Quyền truy cập và bảo mật

**Repository BodhiAtlas là công khai.** Chỉ đưa vào đây nội dung được chủ thể có thẩm quyền cho phép công bố. Không commit thông tin đăng nhập, bí mật truy cập, dữ liệu bị hạn chế quyền phát hành hoặc bản thảo mật. Đối với báo cáo đánh giá **repo nguồn PRIVATE**, cần nêu rõ nguồn là private và kiểm tra quyền công bố báo cáo; **đánh dấu PRIVATE không làm cho file báo cáo trên repo công khai trở thành riêng tư**. Ngày 16/11/2026, theo yêu cầu công bố của chủ dự án, báo cáo **P39 — Bang-ha-giac-ngo** được lưu tại đây và công khai; repository nguồn vẫn private, các liên kết nguồn có thể yêu cầu quyền đọc.

> **Nguyên tắc:** Khảo sát có căn cứ → thử nghiệm có thể tái lập → đối chiếu PRD và cổng chất lượng → quyết định có người chịu trách nhiệm. Không đảo ngược thứ tự này.
