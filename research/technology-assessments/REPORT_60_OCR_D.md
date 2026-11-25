# REPORT 60 — OCR-D: thẩm định độc lập cho BodhiAtlas (R2)

**Bản cập nhật R2, 25/11/2026:** bổ sung audit schema và evaluator, chiến lược kế thừa module, 11 lần gọi Tesseract đối chứng và adapter PAGE/METS cô lập có negative tests; giữ kết quả R1 và thay các mục tổng hợp theo bằng chứng mới. Không sửa repository. Các đoạn mô tả R1 là lịch sử thực nghiệm, không phải tổng hiện hành.

**Mã:** P60 · **Ngày:** 25/11/2026 (Asia/Ho_Chi_Minh) · **Loại:** workflow/standards/QA component, không phải OCR model, catalog hoặc retrieval engine. **Trạng thái:** hoàn thành khảo sát tĩnh và baseline cục bộ giới hạn; chưa nghiệm thu OCR-D upstream. **Phạm vi:** OCR-D/core, OCR-D/ocrd_tesserocr, qurator-spk/dinglehopper. Không thay đổi repo, không tải corpus/weights, không gửi sách ra ngoài.

## 1. Executive Decision

**DEFER — chưa đưa OCR-D full workflow vào runtime V1.** Phương án ưu tiên **E**, giữ OCR-D làm tài liệu tham chiếu QA; thử **C** (PAGE/METS projection và evaluator như công cụ kiểm thử riêng) khi có dữ liệu PAGE thật hoặc corpus lịch sử đã được phép. **B** (workflow lịch sử có giới hạn) là đường nâng cấp nếu đo được lợi ích. Không loại bỏ OCR-D về mặt kỹ thuật; trì hoãn dependency cho đến khi có nhu cầu và bằng chứng. Confidence MED cho ưu tiên đầu tư, HIGH cho ranh giới trách nhiệm đọc được từ code, LOW cho chất lượng/chi phí tương đối của tài liệu cổ.

**Lý do độc lập:** OCR-D chuẩn hóa file group, page ID, metadata processor, polygon và các bước chuyển ảnh, rất hữu ích để thực hiện OCR nhiều giai đoạn. Nhưng hai đặc tính quan trọng cho BodhiAtlas không suy ra từ đó: (i) toàn bộ trang khai báo phải có trạng thái và không có fallback-copy giả thành OCR thành công; (ii) locator phải mở lại đúng file bất biến, đúng revision và kiểm chữ độc lập. Core có đường thay thế `Page.imageFilename` khi hệ tọa độ đổi, cho phép SKIP/COPY/OVERWRITE; đây là chức năng hợp lệ của framework nhưng tạo nghĩa vụ cho adapter, không phải lỗi OCR đã tái hiện. Cài full pipeline trước khi có nhu cầu sẽ thêm workspace, processor/model lifecycle, validator và storage derivatives, trong khi phần cốt lõi chứng cứ vẫn phải làm.

| Giai đoạn | Quyết định |
|---|---|
| V1 | PDF có text: parser trực tiếp giữ locator; scan: direct OCR/Docling làm baseline ứng viên, cùng manifest/QA; không thêm OCR-D mặc định. |
| V2 | PAGE import chỉ khi cần; công cụ dinglehopper offline trong môi trường dev/QA riêng nếu có GT. |
| V3 | Bounded historical profile có segmentation/deskew/review; không chuyển authority sang METS. |

**Ba blocker:** (1) chưa chạy core/processor/evaluator và chưa xác minh schema/transform với fixture chuẩn; (2) chưa có corpus lịch sử, GT được cấp quyền hoặc kết quả đa hệ chữ đại diện; (3) chưa đo được lợi ích so với direct OCR và chưa khép quyền model/dependency (có mâu thuẫn LICENSE/manifest của processor).

**Ba POC quyết định:** POC-A = TC02/09/12 (missing/error/immutable revision); POC-B = TC03/04/06/15 (order, inverse, all occurrences, reopen); POC-C = TC07/08/13/16 (script/GT/quality/TCO). Chỉ cấp nguồn lực POC-C khi A/B qua. Demo dễ nhất: direct Tesseract trên scan tự tạo đã chạy; chưa phải demo OCR-D. Đủ tiêu chuẩn = qua cổng cứng với corpus đã khai báo. Production = thêm rights, vận hành, backup/restore, regression và review độc lập; hiện chưa có phương án nào được chứng minh production trong P60.

### 1.1 Quyết định sau nghiên cứu bổ sung R2

**Giữ DEFER cho full OCR-D runtime; nâng mức ưu tiên thử C hẹp (PAGE import + QA tách riêng) khi thực sự có đầu vào PAGE hoặc layout khó.** Không nâng lên ADOPT/USE AS COMPONENT production chỉ vì fixture đạt. Có thể áp dụng ngay các nguyên tắc độc lập với framework: manifest trang khai báo, trạng thái per-page, bất biến revision, đánh giá theo oracle, phân biệt role/reading order. Không buộc toàn hệ thống xuất PAGE/METS. R2 đã chứng minh direct OCR có lỗi reading order và dùng vùng cắt thủ công khắc phục trên một ảnh; chưa chứng minh OCR-D tự tìm vùng tốt hơn. R2 kiểm tra namespace PAGE 2019-07-15, METS 1.12.1 theo XSD được bundling; biết chính xác normalization evaluator không tương đương literal. Adapter thử nghiệm giữ ba occurrences, từ chối nhầm edition và không cho confidence tự cấp VERIFIED. Các bằng chứng này giúp định vị OCR-D là lớp ingest/QA, không phải evidence authority. Tổng cả R1/R2: 12 subprocess OCR đối chứng, 4 phép thử cô lập R1 + 1 suite adapter R2 (7 negative cases và các assertions positive), 0 runtime OCR-D upstream. Xem §5.6, §8.3, §9.5, §13.6.

## 2. Sources & Evidence Ledger

### 2.1 Snapshot và phạm vi truy cập

| Nguồn | Snapshot quan sát | Access / giới hạn |
|---|---|---|
| [OCR-D/core](https://github.com/OCR-D/core) | master, [`c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3`](https://github.com/OCR-D/core/commit/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3), 2026-09-16 16:37:30 UTC; commit message v3.13.3 | GitHub connector đọc file theo SHA; trang [release](https://github.com/OCR-D/core/releases/tag/v3.13.3) ghi latest v3.13.3 và short SHA c9272c8; [PyPI 3.13.3](https://pypi.org/project/ocrd/3.13.3/) có wheel ngày 16/09/2026. Không tải wheel hay đối chiếu hash nội dung wheel với Git tree. |
| [OCR-D/ocrd_tesserocr](https://github.com/OCR-D/ocrd_tesserocr) | [`f412b60c664f41ca6efbafecb1785408750632bd`](https://github.com/OCR-D/ocrd_tesserocr/commit/f412b60c664f41ca6efbafecb1785408750632bd), 2026-06-05 17:47:49 UTC; ocrd-tool.json 0.21.2 | Code đọc được; R1 chưa xác minh tag/release/wheel digest; R2 xác nhận PyPI 0.21.2 có wheel, tag/digest vẫn chưa khóa; không cài. |
| [qurator-spk/dinglehopper](https://github.com/qurator-spk/dinglehopper) | [`1efb382a54c98cf2c6d716d134c57a2d1325a6b6`](https://github.com/qurator-spk/dinglehopper/commit/1efb382a54c98cf2c6d716d134c57a2d1325a6b6), 2025-08-22 14:56:10 UTC | Code CLI/processor đọc được; R2 xác nhận metadata 0.11.0 và PyPI 0.11.0 có wheel; artifact→commit chưa xác minh, không cài. |
| [BodhiAtlas](https://github.com/quoctran-2608/bodhi-atlas) | [`c5dfe50613dfd492407bf1db1061c1cfc9d30e8e`](https://github.com/quoctran-2608/bodhi-atlas/commit/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e), 2026-11-25 11:26:47 UTC | File qua GitHub connector, đọc trích đoạn liên quan; không tuyên bố đọc hết từng báo cáo hàng chục nghìn chữ. |
| [OCR-D specs](https://ocr-d.de/en/spec/) | web hiện hành 25/11/2026 | Mở METS, PAGE, GT và QA; snapshot web không ghim Git SHA; R2 xác nhận schema bundled PAGE 2019-07-15/METS 1.12.1, chưa chạy XSD validation. |
| Runtime | sandbox Linux; Git CLI lỗi DNS | ACCESS BLOCKED đối với clone/cài từ mạng; OCR-D, tesserocr và dinglehopper không có sẵn. Direct Tesseract có sẵn; xem §9, §13. |

HEAD ở đây là commit mới nhất trả về trong truy vấn GitHub và đối chiếu release trang công khai; không phải chứng nhận không có commit mới sau thời điểm truy vấn. Không có full recursive tree dump; xác nhận đường dẫn bằng fetch file thực tế ở SHA. Những tên file cũ trả 404 không được ghi là module tồn tại. Hơn 20 file upstream đã được truy xuất; đọc chọn lọc các hàm và đoạn có vai trò quyết định, không audit toàn bộ nội dung/generated schemas/CI.

### 2.2 Chuẩn dự án nhận và báo cáo đối chứng

Các link dưới đây ghim đúng commit BodhiAtlas; [DOC] là yêu cầu, không phải tính năng đã triển khai. Đã lấy file thực tế và đọc các phần liên quan, giới hạn trích đoạn được hiển thị bởi công cụ.

- [PRD v1.4](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/PRD.md): §2–5, 6.1 — phân biệt tác phẩm/ấn bản/file, bao phủ OCR, search code, literal vs biến thể, độc lập kiểm câu chữ/vị trí/claim.
- [V1 Core Foundation v1.1](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/V1_CORE_FOUNDATION.md): §1–2 — lõi source-grounded, không đồng nhất RAG với chứng cứ.
- [Academic Risks and Verification](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/ACADEMIC_RISKS_AND_VERIFICATION.md): kiểm ngữ cảnh/phủ định, tách nguồn chưa đọc với chứng cứ; G1–G6 theo prompt; chưa chạy suite T01–T16 của sổ tay.
- [Research inventory](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/README.md): ghi 57 đề tài, 28 báo cáo; phân loại, không phải xếp hạng. [Template](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_TEMPLATE.md) 10 phần; báo cáo này dùng 13 phần theo prompt.

| Báo cáo đã mở | Nội dung liên quan được đọc (không phải kết quả P60) |
|---|---|
| [P12 Docling](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_12_DOCLING.md) | Snapshot Docling 2.150.1, core 2.106.0; nghiên cứu tĩnh, chưa chạy fixture. Candidate baseline ingest/structured parsing, cần adapter source map. |
| [P45 MinerU](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_45_MINERU.md) | TRIAL ONLY; Middle JSON + sidecar; phân profile Flash/Basic/Standard/Advanced, chưa chạy. |
| [P46 Marker](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_46_MARKER_DATALAB.md) | Component có điều kiện; JSON block geometry không là char map; không đo OCR. |
| [P52 olmOCR](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_52_OLMOCR.md) | TRIAL ONLY fallback; GPU/model chưa chạy, tách weights và dataset rights. |
| [P39-R2 Bang-ha](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_39_BANG_HA_GIAC_NGO_INDEPENDENT_REVIEW.md) | Component có điều kiện, đề xuất minimal core và BCR resolver; không dùng kết luận này thay thực nghiệm. |
| [P03 BCR](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_03_BUDDHISMDOCUMENTS_FOR_AI.md) | Corpus tooling/resolver, nghiên cứu tĩnh không chạy toàn corpus. Không phải OCR. |
| P14, P15, P16, P19 | Fetch các tên REPORT_14_OCRMYPDF.md, REPORT_15_TESSERACT.md, REPORT_16_PADDLEOCR.md, REPORT_19_ESCRIPTORIUM.md trả 404 tại snapshot. Không khẳng định không có file tên khác. Tesseract direct có test P60; các công cụ khác chỉ xem vai trò giới hạn ở §11, không gán kết luận báo cáo cũ. |

### 2.3 Evidence Ledger

[DOC] tài liệu đã đọc; [CODE] mã/test source đã đọc; [TESTED] chạy upstream hoặc đối chứng thực; [TESTED-ISOLATED] fixture/thuật toán độc lập; [ISSUE] phản ánh chưa tái hiện; [PLAN] chưa chạy; [INFERRED] suy luận; [UNKNOWN] chưa biết; [CONFLICT] nguồn mâu thuẫn. CODE không đồng nghĩa PASS. Mỗi link code ghim SHA; các link tài liệu web không ghim nên có thể trôi.

| ID | Claim | Loại | Nguồn / vị trí | Giới hạn |
|---|---|---|---|---|
| E01 | Core triển khai specs và công cụ, Python >=3.8 | DOC/CODE | [README](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/README.md), [pyproject L10–47](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/pyproject.toml#L10-L47) | Không chứng minh mọi Python minor chạy được. |
| E02 | METS query/file groups, physical page identity và label | CODE | [ocrd_mets.py L250–414,634–758](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_models/ocrd_mets.py#L250-L414), [labels L1044–1054](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_models/ocrd_mets.py#L1044-L1054) | Workspace ID không là edition authority. |
| E03 | CLI init/add/validate/list/backup | CODE | [workspace CLI L113–243](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/cli/workspace.py#L113-L243), [L918–960](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/cli/workspace.py#L918-L960) | Restore toàn catalog chưa thử. |
| E04 | Core gọi process_page_pcgts; mặc định raise; output IDs/metadata và PAGE serialize | CODE | [base.py L809–946](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/processor/base.py#L809-L946) | Cần processor cụ thể. |
| E05 | SKIP/COPY/OVERWRITE, task error không đồng nghĩa lỗi toàn workflow | CODE | [base.py L718–780](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/processor/base.py#L718-L780), [config L204–250](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_utils/config.py#L204-L250) | Chưa chạy fail injection. |
| E06 | Zip page groups, require_first bỏ page không có group đầu, trùng file có policy | CODE | [base.py L1050–1188](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/processor/base.py#L1050-L1188) | Cần expected set ngoài workspace. |
| E07 | Transform affine và AlternativeImage, crop/rotate/scale | CODE | [workspace.py L565–800](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/workspace.py#L565-L800), [L1130–1241](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/workspace.py#L1130-L1241), [image.py L112–192](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_utils/image.py#L112-L192) | Không chứng minh inverse phi tuyến/pixel accuracy. |
| E08 | Dewarp có thể thay ảnh tham chiếu và kích thước | CODE | [base.py L859–893](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/processor/base.py#L859-L893) | Chưa có processor dewarp được audit; inverse raw UNKNOWN. |
| E09 | Validator reading order/text/coordinate và workspace checks | CODE | [page_validator.py L182–243](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/page_validator.py#L182-L243), [L276–448](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/page_validator.py#L276-L448), [workspace_validator.py L140–317](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/workspace_validator.py#L140-L317) | Structural validity không kiểm nội dung ảnh. |
| E10 | Network resolver/resource download là capability, không mặc nhiên offline | CODE | [resolver.py L29–158](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/resolver.py#L29-L158), [resource_manager.py L289–456](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/resource_manager.py#L289-L456) | Không audit an toàn archive hoàn chỉnh; không kết luận CVE. |
| E11 | Multiprocessing >1 yêu cầu METS server trong base | CODE | [base.py L509–585](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/processor/base.py#L509-L585) | Không benchmark song song. |
| E12 | Tesserocr recognition/segmentation từ vùng đến glyph, config model | CODE | [recognize.py L127–205](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/recognize.py#L127-L205), [L527–857](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/recognize.py#L527-L857), [segment.py](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/segment.py) | Không có số fidelity theo script. |
| E13 | Registry chứa Fraktur và language/model URLs; lựa chọn confidence | CODE/DOC | [ocrd-tool.json L172–260](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json#L172-L260), [README](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/README.md) | URL mutable không lock weights; không calibration. |
| E14 | Dinglehopper nhận PAGE/ALTO/text; CLI tính CER/WER, có OCR-D processor wrapper | CODE/DOC | [README](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/README.md), [cli.py L108–193](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/cli.py#L108-L193), [ocrd_cli.py L15–79](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/ocrd_cli.py#L15-L79) | Chưa đọc helper normalization/word segmentation đầy đủ hoặc chạy evaluator. |
| E15 | Core Apache-2.0; tesserocr wrapper LICENSE MIT-style nhưng manifest Apache-2.0 | CODE/CONFLICT | [core LICENSE](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/LICENSE), [processor LICENSE](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/LICENSE), [manifest L5–25](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/pyproject.toml#L5-L25), [dinglehopper LICENSE](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/LICENSE) | Resolve trước phân phối; model/corpus riêng. |
| E16 | Có test overwrite, backup, deskew, feature selector | CODE | [tests/test_workspace.py L61–157](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/tests/test_workspace.py#L61-L157), [L483–599](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/tests/test_workspace.py#L483-L599) | Test source, chưa chạy. |
| E17 | Direct baseline Tesseract 5.5.0 đọc scan tự tạo, mất 2 dấu Pāli | TESTED (đối chứng, không phải OCR-D) | §9, §13 log và script | 1 ảnh sạch, không đại diện. |
| E18 | XML order/alternative, missing set, affine, negation fixture | TESTED-ISOLATED | §9, §13 | Không chạy PAGE validator/XSD hoặc upstream. |
| E19 | PAGE/METS/GT/QA là specs riêng | DOC | [PAGE](https://ocr-d.de/en/spec/page), [METS](https://ocr-d.de/en/spec/mets), [GT](https://ocr-d.de/en/gt-guidelines/trans/), [QA](https://ocr-d.de/en/spec/ocrd_eval) | Chưa ghim commit spec hoặc xác nhận XSD tương thích. |
| E20 | Raw authority ngoài workspace, strict manifest và separate verify | INFERRED/PLAN | E02–E09 + PRD §3–5 | Thiết kế đề xuất, chưa triển khai. |

### 2.4 Evidence Ledger bổ sung (R2, cùng snapshot GitHub)

| ID | Claim | Loại | Nguồn / vị trí | Giới hạn |
|---|---|---|---|---|
| E21 | Namespace PAGE 2019-07-15; generated bindings lấy từ schema bundled; PcGts cần Metadata/Page | CODE | [constants](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_models/constants.py#L40-L49), [page.xsd L1–19](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/page.xsd#L1-L19), [generated header](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_models/ocrd_page_generateds.py#L5-L21) | XSD blob `497c494f69f7d4edc2cf8fa064bd4aade82d0049`; chưa chạy validator. |
| E22 | METS bundled 1.12.1, October 2019, CC0 declaration, local xlink import | CODE/DOC | [mets.xsd L1–28](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/mets.xsd#L1-L28) | Blob `7464f542c935eb2dd25529cd7397b7279d8d1424`; không suy METS 2.x tương thích. |
| E23 | XSD local resource lookup; XsdValidator compile/assertValid | CODE | [constants L42–46](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/constants.py#L42-L46), [xsd_validator L40–75](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/xsd_validator.py#L40-L75), [XsdPageValidator](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/xsd_page_validator.py), [XsdMetsValidator](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/xsd_mets_validator.py) | Không chạy; local schema dependencies cần lock. |
| E24 | TextEquiv Unicode bắt buộc, PlainText/index/conf optional; index thấp nhất là main; line/word/baseline không luôn có | CODE | [page.xsd L489–520](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/page.xsd#L489-L520), [L721–775](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/page.xsd#L721-L775), [AlternativeImage L2379–2388](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_validators/page.xsd#L2379-L2388) | XML hợp lệ không bảo đảm đủ nội dung. |
| E25 | Workflow runner validate task/group, kiểm returncode và tồn tại output group | CODE | [CLI process](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/cli/process.py), [task_sequence L90–169](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/task_sequence.py#L90-L169) | Không kiểm đủ per-page theo expected manifest độc lập ở vòng runner này. |
| E26 | Inverse affine áp ma trận nghịch đảo, float32 và làm tròn int32 | CODE | [image.py L112–192](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_utils/image.py#L112-L192) | Không suy pixel roundtrip exact hoặc dewarp mapping. |
| E27 | Tesserocr dùng model registry, xuất conf từ Tesseract/100 và có glyph alternatives | CODE | [recognize L735–857](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/recognize.py#L735-L857), [L1095–1172](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/recognize.py#L1095-L1172), [registry](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json) | Confidence chưa calibrated; không phải verification. |
| E28 | Dinglehopper CER dựa grapheme NFC, WER theo Unicode word break bỏ token chỉ dấu/khoảng trắng; zero ref có thể inf | CODE | [CER L1–60](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/character_error_rate.py), [WER L1–118](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/word_error_rate.py), [edit_distance](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/edit_distance.py) | Không phải chỉ số exact; khác metric của baseline R2. |
| E29 | Dinglehopper trích PAGE dùng NFC_SBB thay ligature và dấu câu; đọc theo RO, bỏ region rỗng, không tự bù region thiếu reference | CODE | [extracted_text L15–95](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/extracted_text.py#L15-L95), [L238–325](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/extracted_text.py#L238-L325), [ocr_files L60–146](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/ocr_files.py#L60-L146) | Có thể che mất sai khác literal và coverage; không dùng extractor đó làm canonical authority. |
| E30 | Dinglehopper metadata version 0.11.0 và package 0.11.0 có wheel; processor 0.21.2 có wheel | CODE/DOC | [ocrd-tool](https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/src/dinglehopper/ocrd-tool.json), [PyPI Dinglehopper](https://pypi.org/project/dinglehopper/0.11.0/), [PyPI processor](https://pypi.org/project/ocrd-tesserocr/0.21.2/) | Chưa xác minh SHA tag/wheel provenance khớp commit; không cài. |
| E31 | Resource extraction gọi zip/tar extractall; không coi archive tải từ URL là trusted mặc định | CODE/INFERRED | [resource_manager L351–397](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/resource_manager.py#L351-L397) | Không tuyên bố CVE/exploit; behavior tùy Python, sandbox bắt buộc. |
| E32 | R2 direct OCR đa ngữ, layout và cắt vùng thủ công | TESTED (baseline, không phải OCR-D) | §9.5, §13.6 raw log | Một số ảnh synthetic, không có OCR-D pipeline hay test corpus. |
| E33 | PAGE projection strict subset giữ offset, region, revision/edition và rejects | TESTED-ISOLATED | §9.5, §13.6 | Toy XML không XSD-valid (thiếu Metadata); không independent human visual verification, không phải production adapter. |

R2 đã mở thêm các file thật chưa có trong inventory R1: `src/ocrd_models/constants.py`, `mets-empty.xml`, `ocrd_page_generateds.py` (header), `src/ocrd_validators/constants.py`, `page.xsd`, `mets.xsd`, `xsd_validator.py`, `xsd_page_validator.py`, `xsd_mets_validator.py`, `src/ocrd/cli/process.py`, `src/ocrd/task_sequence.py`; Dinglehopper `character_error_rate.py`, `word_error_rate.py`, `edit_distance.py`, `ocr_files.py`, `extracted_text.py`, `__init__.py`, `ocrd-tool.json`. Đọc có mục tiêu, không giả là full-tree review. `NOTICE` tại root core trả 404; không suy mọi NOTICE trong dependencies đều không có. Web raw XSD trả DisabledError, Git CLI vẫn lỗi DNS. Nội dung XSD qua connector đọc được nhưng chưa materialize bytes để compile. Dinglehopper release 0.11.0 có wheel 24/04/2025, commit đọc 22/08/2025; không mặc định wheel là commit đó. Processor wheel 05/06/2026, provenance trang PyPI trỏ workflow ở commit khác commit package metadata; pin artifact digest trước POC.

## 3. Architecture & Data Flow

### 3.1 Quan sát code upstream

```text
ocrd workspace init/add → WorkspaceCtx → Resolver → Workspace/OcrdMets
                         physical structMap/page ID + fileGrp + file ID + location
processor CLI + ocrd-tool.json → Processor.verify → process_workspace
  → submit per-page tasks → process_page_file → page_from_file
    → processor.process_page_pcgts (TesserocrRecognize / Segment)
      → OcrdPageResult (+ images) → add_metadata → to_xml → Workspace.add_file
      → METS output group, physical page link → save_mets/validation
GT group + OCR group → dinglehopper processor hoặc CLI độc lập → evaluation reports
```

E03/E04/E06/E12 xác nhận các mắt xích chính; entrypoint registration end-to-end và workflow runner/network không chạy, không mô tả là đã kiểm. `page_from_file`/`page_from_image` ở [modelfactory L45–119](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_modelfactory/__init__.py#L45-L119). `OcrdFile` [L98–225](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_models/ocrd_file.py#L98-L225) biểu diễn ID/pageId/fileGrp/url/local filename. `OcrdPage` [L184–269](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd_models/ocrd_page.py#L184-L269) bọc PAGE và serialization; không tự tạo text đã verified. Processor override có thể không đi qua mọi bước base. Không xem package thành một microservice; local CLI đủ cho single-worker POC.

METS là manifest workflow: fileSec/fileGrp nhóm artifact, physical structMap liên kết trang với file qua fptr. PAGE chứa mô tả ảnh, region/line/word/glyph, text alternatives, polygon/baseline và reading order. PAGE ID theo tài liệu và output file; phải dùng namespace đầy đủ và khóa revision. Model weights không nằm trong định nghĩa PAGE; evaluator độc lập với recognizer. Workspace quản lý mutable state, không là hồ sơ pháp lý lâu dài.

### 3.2 Sơ đồ đề xuất (chưa triển khai)

```text
Catalog BodhiAtlas (SQLite + content-addressed file store)
  → immutable raw blob + rights + edition/witness + expected page manifest
  → router (direct PDF/EPUB/TEI; scan baseline; optional historical profile)
  → scratch workspace (METS/PAGE, copy/render; raw read-only)
  → artifact validation + page reconciliation + transform checks
  → immutable extraction revision + canonical text/source map + page statuses
  → EXACT scanner / candidate index; normalized, fuzzy, lexicon tách biệt
  → independent source reopen + reviewer → evidence status
  → claims/publish (gates riêng)
```

BodhiAtlas sở hữu catalog, expected page set, raw hash, revision, canonicalization policy, index, citation, review và quyền. OCR-D chỉ sở hữu workspace tạm và kết quả theo processor contract. PAGE/GT/eval có thể lưu nguyên blob để tái đọc mà không chạy lại framework. Không dual-write 2 catalog; mỗi page được reconcile trước commit revision atomically. Đổi parser không đổi identity file. BCR/Bang-ha là ứng viên reuse cho corpus/resolver; không có quyết định thay core từ P60.

## 4. Fit–Gap C01–C15

Scope = OCR workflow/QA cho scan, không chấm ngoài vai trò; effort là công tích hợp tăng thêm so với baseline V1, L/M/H/VH định tính, không phải nhân-ngày. NATIVE chỉ cho capability tĩnh, không bảo đảm fidelity. V1 = nền tảng, V2/3 = tùy nhu cầu.

| ID | Yêu cầu | Trạng thái | Bằng chứng | Gap / owner | Effort | Cổng | Phép thử / pha |
|---|---|---|---|---|---|---|---|
| C01 | Multi-format ingest | EXTERNAL | E02,E04; image/PAGE | PDF render, EPUB/TEI/DOCX native locators thuộc router | M | G1 | TC02,16 V1 |
| C02 | OCR/layout/reading order | NATIVE+CONFIG (processor) | E07,E09,E12 | Gold order, note roles, model quality; adapter/reviewer | H | G1,G2 | TC03,04,06,07,08 V2/3 |
| C03 | Canonical text & source map | EXTENSION | E04,E07,E09 | Projection span/role/precision/revision, core | H | G1,G2 | TC04,05,15 V1 |
| C04 | Work/Edition/Witness model | EXTERNAL | E02 | Catalog identity; không dùng METS file ID làm edition | M | G2,G4 | TC10 V1 |
| C05 | Exhaustive EXACT | N/A | Vai trò OCR | Core scanner/coverage oracle; no top-K | H (core chung) | G2 | TC15 V1 |
| C06 | Normalized multilingual | EXTERNAL | E12,E14 | Rule version và reversible mapping; search core | H | G2,G5 | TC07,13,15 V1 |
| C07 | Fuzzy retrieval | N/A | Vai trò OCR | Core candidate + ranking + labels | M (chung) | G2 | TC15 extension V1 |
| C08 | Sense-aware lexicon | N/A | Vai trò OCR | Lexicon owner; không suy sense qua OCR | H (chung) | G5 | TC07 + lexicon suite V1/2 |
| C09 | Semantic/RAG | N/A | Vai trò OCR | Optional discovery; no verification by similarity | L (handoff) | G3 | TC15 extension V2/3 |
| C10 | Verified citation/reopen | EXTENSION | E02,E07,E08 | Independent raw reader, no false VERIFIED, core/reviewer | H | G2 | TC04,10,12,15 V1 |
| C11 | Wiki/notes/claims | N/A | Vai trò OCR | Claim review/notes không thuộc PAGE | L (handoff) | G3,G6 | TC14 V2 |
| C12 | APIs/MCP/export | NATIVE (CLI/PAGE); MCP N/A | E03,E04,E14 | Export adapter; ALTO/PDF/TEI exporter chưa audit | M | G1,G2 | TC11,15 V1/2 |
| C13 | Coverage/incremental | CONFIG+EXTENSION | E05,E06 | Manifest status, atomic revisions, idempotency | H | G1 | TC02,09,12 V1 |
| C14 | Auth/privacy/license/backup | EXTERNAL+UNKNOWN | E03,E10,E15 | isolation, rights, retention, restore all; ops | H | G4,G6 | TC01,09,12 V1 |
| C15 | Operability/portability | CONFIG+UNKNOWN | E01,E11 | offline wheel/model lock, CPU test, failure isolation | M/H | G1,G4 | TC01,16 V2/3 |

### Quality gates theo phạm vi

| Gate | OCR-D role | Trạng thái P60 | Điều kiện đạt cho hệ thống |
|---|---|---|---|
| G1 ingest | Trọng tâm | NOT DEMONSTRATED; CODE GAP cho expected-set/READY của BodhiAtlas | TC02/09; mọi trang có status, phân biệt copy/skip/blank, raw immutable. |
| G2 citation | Handoff | NOT DEMONSTRATED; CODE GAP cho độc lập xác minh và revision locator | TC04/10/12/15; reopen raw đúng file/page/quote, không false VERIFIED. |
| G3 claim | N/A ứng viên | NOT DEMONSTRATED hệ thống | Người nghiên cứu kiểm context, polarity, loại nguồn, phản chứng. |
| G4 external | Handoff rights | NOT DEMONSTRATED | Offline sandbox, model/scan/GT rights, pin/version/access; external source chưa đọc không làm evidence. |
| G5 lexicon | N/A ứng viên | NOT DEMONSTRATED hệ thống | Tách sense, script, bản dịch/dẫn chứng. |
| G6 publish | N/A ứng viên | NOT DEMONSTRATED hệ thống | Rà G1/G2/G3/G4/G5, quyền, nhất quán. |

Không có PASS production. Baseline mất dấu Pāli ở TC07 subset, là FAIL của tiêu chí exact gold trên fixture đó, không suy OCR-D FAIL. Mapping các T01–T16 của sổ tay phải đối chiếu từng ID trong bước POC kế tiếp; chưa chạy suite gốc, không đổi tên TC thành T hoặc tự nhận đã qua sổ tay.

## 5. Deep Technical Findings

### 5.1 Workspace, identity, error semantics

E02/E03: file group biểu diễn stage, physical page ID kết nối nhiều output. Ưu điểm hơn tập ảnh rời là có structure và liên kết file. Nhưng `fileGrp`/ID không phải content hash; output có thể bị ghi đè. `Workspace.add_file` [L402–465](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/workspace.py#L402-L465) là đường ghi workspace và METS, không phải transaction BodhiAtlas. `remove_file`, `remove_file_group` [L234–327](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/workspace.py#L234-L327) cho thấy scratch phải tách raw. Physical label có thể thiếu/không bằng printed page, kể cả hai bản cùng page ID.

E05/E06: base có policy skip/abort/copy và `require_first`. Ví dụ expected p1,p2,p3, fileGrp đầu chỉ p1,p3; thành công hai task không là 100% ingest. COPY input là recovery hữu ích, không được gán recognized. `process_page_file` còn có nhánh bỏ qua input không parse được, return nếu không có PAGE; `zip(results, groups)` nghĩa số output group phải reconcile, không suy đủ từ log hoàn tất. Chọn abort + outer manifest strict; nếu ứng dụng cần tiếp tục sau lỗi thì trạng thái PARTIAL, không READY. Tách `missing`, `failed`, `unsupported`, `not_attempted`, `blank_verified`, `fallback_copy`, `extracted_unreviewed`, `reviewed`.

### 5.2 Geometry và fidelity

E07: `image_from_page` chọn AlternativeImage dựa feature selector/filter và annotation; trả ảnh, affine transform, angle/DPI/features. `_crop` shift offset; `_reflect` transpose; `_rotate` điều chỉnh transform và recrop; `_scale` có rounding; có log khi geometry không nhất quán. `image_from_segment` [L801–1060](https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/src/ocrd/workspace.py#L801-L1060) xử lý cấp segment. Ưu điểm thực sự là công cụ thao tác hệ tọa độ. Hạn chế: reconstruct từ features/orientation không phải chứng minh chuỗi provenance đầy đủ; log mismatch không nhất thiết abort; dewarp thay ảnh gốc trong PAGE output (E08). Cần pin ảnh tham chiếu trước/sau, inverse transform độc lập, kiểm bounds và roundtrip trên điểm ảnh thật. Không giả một ma trận affine giải được biến dạng phi tuyến. Khi không inverse: mở raw theo page, chỉ highlight derivative nếu nhãn derivative rõ; precision PAGE_ONLY, không giả word/char bbox.

### 5.3 PAGE hierarchy và reading order

[PAGE conventions](https://ocr-d.de/en/spec/page) và E09/E12 định hướng cấu trúc vùng, dòng, từ, glyph; reading order cần xử lý ordered/unordered groups, nested regions và reference IDs. TextEquiv có alternatives; chọn theo policy version, không nối tất cả alternatives như nội dung tuần tự. Confidence vắng là unknown, không phải 0 hay 1. Confidence cao không phải xác suất câu học thuật đúng. `page_validator.py` có `sorted_reading_order`, `get_text`, `concatenate`, `validate_consistency` hỗ trợ cấu trúc và kiểm text hierarchy. Điều này không bảo đảm thứ tự đọc khớp sách hai cột, header, footnote, marginalia, ruby hay bảng dọc. Không fallback âm thầm sang thứ tự XML khi reading order thiếu; lưu unknown hoặc review. Có thể chọn region-level nếu không có line/word/glyph. Không suy char offsets từ polygon cấp line.

PAGE schema version/namespace chính xác ở snapshot và METS XSD version chưa được xác minh trực tiếp trong file XSD; không tự gán 2019/2024 là contract thực thi. POC phải kiểm `root.nsmap`, schemaLocation, schema hash và validator tương ứng; không accept XML bằng local-name một cách im lặng. METS version/schema namespace cũng phải pin; website conventions không thay hash schema. Export ALTO/PDF/TEI chưa audit repo/implementation nên UNKNOWN, không đưa vào thiết kế bắt buộc.

### 5.4 Processor, models, evaluation

Tesserocr wrapper subclass Processor; `TesserocrSegment` tái dùng recognition path, recognizer hỗ trợ granularity và model config (E12). Registry E13 có tài nguyên Fraktur cụ thể và URL `.traineddata`; không mặc định chạy handwriting, Hán Nôm, Pāli hoặc Tạng manuscript. Model chọn theo confidence/XPath không giải calibration cross-language; phải lock bytes. Core không tự nhận dạng ảnh mọi loại, `process_page_pcgts` mặc định raise IncompleteProcessorImplementation. CLI standalone Tesseract dùng cùng họ engine nhưng không cùng config/calls/output OCR-D; baseline P60 không chứng minh wrapper.

Dinglehopper E14 có CLI standalone và OCR-D integration; tách evaluator ra khỏi runtime hoàn toàn khả thi về mặt giao diện. CLI gọi `words_normalized`, `character_error_rate_n`, `word_error_rate_n`; diff làm việc với grapheme clusters. Chưa đọc hết helper nên không khẳng định denominator, Unicode equivalence và alignment exact của phiên bản đó. Phải so với oracle codepoint/grapheme/word có định nghĩa rõ. GT policies: diplomatic vs normalized, diacritics/ligature, editorial additions, uncertain glyph, role and segmentation, GT reviewer, revision + rights. CER/WER chỉ đo distance; một từ phủ định mất có thể đổi luận điểm dù CER thấp. Region IoU/reading order/omission và reviewer time bổ sung; không dùng một số điểm trung bình duy nhất.

### 5.5 H01–H12: luận cứ thuận/ngược và điều kiện bác bỏ

| H | Thuận / ngược | Kết luận hiện tại | Phản chứng hoặc phép kiểm |
|---|---|---|---|
| H01 core tự OCR mọi ảnh/PDF | Base điều phối; E04 raise, E12 processor riêng | Bác bỏ phát biểu tuyệt đối bằng code | TC01 chạy core-only và processor; PDF render ngoài. |
| H02 lineage/coverage nhiều bước | E02 metadata/group; E05 skip/copy và mutable group | Một phần; coverage toàn bộ chưa chứng minh | TC02 expected-set + fail injection. |
| H03 mapping ngược raw đúng | E07 affine; E08 thay coordinate frame | Có cơ chế, không bảo đảm mọi transform | TC04 landmarks, crop/rotate/resize/dewarp, error/IoU. |
| H04 reading order note/cột | E09/E12 order generation/validation; structure valid != gold | UNKNOWN chất lượng | TC03/06 compare order, role và omitted region. |
| H05 GT evaluation nhạy phủ định/dấu | E14 distance/diff; E18 negation | Đo lỗi chữ được về nguyên tắc; không đo risk semantics | TC13 exact expected, long text one negation. |
| H06 confidence đủ VERIFIED | E13 model confidence; không independent raw verification | Bác bỏ như policy | TC05 wrong high-conf, missing conf, no false verified. |
| H07 đa ngữ/chữ cổ tốt | Registry có model đa chữ và Fraktur; direct fixture mất dấu Pāli | UNKNOWN OCR-D; không ngoại suy | TC07/08 model-by-script, rights, GT. |
| H08 thiếu trang/error báo PARTIAL | E05/E06 có lỗi/skip/copy, không global BA state | CODE GAP nếu dùng status workflow làm READY | TC02/09 crash và missing first group. |
| H09 rerun giữ old evidence | E04 có same group ID, overwrite; metadata step hữu ích | Không guarantee bất biến; wrapper phải làm | TC12 old locator valid hoặc explicit stale. |
| H10 reuse conventions/evaluator riêng | E14 standalone, PAGE/METS open specs | Khả thi tĩnh; effort chưa đo | TC11/13/15 minimal parser vs runtime adapter. |
| H11 offline/CPU/rights | E01 Python; E10 resource URLs, E15 license conflict | UNKNOWN đầy đủ; direct baseline CPU chạy | TC01 network-denied wheelhouse, SBOM, rights. |
| H12 workflow tiết kiệm lịch sử | Workspace + order + GT có thể giảm custom glue | UNKNOWN; chưa có lịch sử/benchmark | TC08/16 paired review minutes và TCO. |

### 5.6 Kết quả audit sâu R2: những khác biệt ảnh hưởng kiến trúc

**Schema và validator.** Core serialization lấy namespace PAGE 2019-07-15 từ constants, generated bindings dùng chính `src/ocrd_validators/page.xsd`. METS bundled là 1.12.1 (10/2019), không phải tuyên bố schema mới nhất của cả ecosystem. TextLine cần Coords nhưng baseline/word/TextEquiv có thể vắng; TextEquiv có Unicode, PlainText riêng (có thể mất ligature), index/conf tùy chọn; AlternativeImage chỉ có filename/comments/conf trong kiểu này, không chứa ma trận inverse. Việc validator XSD chấp nhận không chứng minh đúng câu chữ, không đo missing page ngoài METS. Adapter nên khóa namespace và schema blob, không tự tải schema từ XML. XSD compilation, migration 2013/2019/khác và actual output chưa thử. Fixture R2 cố ý subset, thiếu Metadata bắt buộc, không được dùng làm chứng minh XSD PASS.

**Workflow.** `run_tasks` kiểm nhóm đầu vào/đầu ra, gọi `run_cli` từng task, stop với nonzero return, reload METS rồi kiểm tồn tại group. Đây là contract stage hữu ích nhưng group tồn tại vẫn có thể chỉ chứa một phần trang. Kết hợp `zip_input_files`, SKIP/COPY và group check cho phản ví dụ tĩnh: p1 có output, p2 absent, group vẫn tồn tại; external manifest phải đối soát. Không kết luận đã chạy phản ví dụ qua OCR-D. Không cần kế thừa nguyên orchestration nếu BodhiAtlas chỉ gọi một adapter.

**Reading order/alternatives.** Dinglehopper `page_extract` ưu tiên ReadingOrder nếu có, sort indexed group, giữ thứ tự XML cho unordered group, bỏ region text rỗng. Nếu có region không được tham chiếu trong RO, nhánh này không bổ sung nó bằng một vòng kiểm expected regions. `get_first_textequiv` chọn min index, nếu không có index nào thì max conf, cuối cùng first. Validator core `get_text` có nhánh best/first nhưng `PageValidator.validate` ở L521–524 chỉ chấp nhận first; không coi best là public validator mode đã hỗ trợ. `fix` có thể sửa text từ child; chỉ chạy trên derivative scratch, không chạy trên artifact chứng cứ bất biến. R2 chọn policy bảo thủ hơn: một ordered group đầy đủ; thiếu/duplicate/không hỗ trợ → quarantine thay vì đoán. Không đề nghị viết lại bộ parser tổng quát.

**Evaluator không là exact verifier.** `normalize_sbb` dùng NFC rồi mở rộng ligature (ví dụ ﬁ → fi) và đổi một số dấu câu, ký tự PUA theo quy ước lịch sử châu Âu, kể cả `==` và em dash → en dash; mặc định extraction qua hàm này ở PAGE/plain/ALTO. WER dùng Unicode word breaks, loại token chỉ punctuation/marks/whitespace; CER đo grapheme clusters, không phải raw codepoint offsets. `segment_id_for_pos` hữu ích cho QA diff, không chứng minh source map raw. Có thể CER = 0 sau normalization trong khi literal khác; RO omission có thể làm cả GT và candidate cùng mất vùng. Giữ ba lớp metric: diplomatic/literal codepoint, NFC grapheme và normalized evaluator với policy ID, cộng critical error list (Không, số, dấu, Hán dị thể). Không thay raw bằng text evaluator. Không xem WER Unicode mặc định là segmentation ngôn ngữ học cho Hán/Tạng.

**Geometry.** `coordinates_for_segment` gọi `np.linalg.inv` và làm tròn, có ích cho transform affine; sau crop/rotate/scale lưu matrix/frame và rounding policy. Với nonlinear dewarp không có inverse field bắt buộc trong AlternativeImage XSD; nếu imageFilename bị thay thì chỉ giữ region tọa độ derivative, raw locator hạ PAGE đến khi có mapping đã thử. Raw reopen phải validate hash + page manifest + tọa độ/precision; OCR confidence không đủ.

**Model.** Registry có `vie`, `Vietnamese` ([L505–506](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json#L505-L506), [L1331–1332](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json#L1331-L1332)), `chi_sim`, `chi_tra` ([L617–632](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json#L617-L632)), `bod`, `Tibetan` ([L498–499](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json#L498-L499), [L568–569](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json#L568-L569)), `Latin`, `lat` ([L260–261](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json#L260-L261), [L974–975](https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/ocrd_tesserocr/ocrd-tool.json#L974-L975)). Đây là registry URL mutable trỏ `tessdata_best/main`, không đồng nhất weights local R2. Không tìm thấy mục `pli.traineddata` qua rà tên registry; không chứng minh absence mọi model Pāli trong ecosystem. Nôm, manuscript và Wylie OCR riêng UNKNOWN. R2 cho thấy Latin script model đỡ lỗi Pāli hơn lat/eng trong một mẫu; không chọn model production từ mẫu tuning đó.

## 6. Source Fidelity & Provenance

Hợp đồng đề xuất, không phải schema upstream:

```text
RawFile(file_id, sha256, media_type, byte_len, rights_id)
EditionWitness(edition_id, witness_id, file_id)
ExpectedPage(file_id, page_index0, physical_page_id, print_label_nullable)
ExtractionRevision(rev_id, file_id, parser_pin, processor_pin, model_sha,
                   schema_sha, parameter_sha, manifest_sha, canonical_policy)
Artifact(artifact_sha, rev_id, page_id, stage, parent_artifact_sha, uri, frame)
PageState(rev_id,page_id,status,reason,attempt,artifact_sha,review_state)
SourceSpan(rev_id, start_cp, end_cp, page_id, artifact_sha, region_id,
           line_id?, word_id?, polygon?, frame_id, inverse_id?, precision, role)
Citation(evidence_id, file_id, edition_id, rev_id, span_range, quote_sha,
         verifier_version, state, reviewed_by?, checked_at?)
```

RawFile SHA-256 là hash bytes, edition identity không suy chỉ từ hash (cùng file được gắn nhiều record); cấm replace. PDF: render page index 0-based, page count từ parser raw độc lập, cropbox/mediabox/rotation, DPI, matrix PDF points↔pixel; printed label nullable (có thể i, xii, 25a). PAGE physical ID chỉ mapping explicit. Scan ảnh: xác nhận dimensions, orientation/EXIF và decoder version; raw sha + derivative sha tách biệt. Mỗi region/line/word ID chỉ có nghĩa trong artifact/rev; cùng string qua processor khác không mặc nhiên cùng đoạn.

Chuỗi custody: raw SHA → page index/physical ID → render SHA + transform → processor stage artifact → PAGE geometry/text alternative → canonical span → independent raw reopen. `start_cp/end_cp` là codepoint half-open, có thể bổ sung byte offsets; grapheme cluster UI không thay tọa độ canonical. Separator tổng hợp được ghi provenance synthetic, không gán chữ vào raw. Cross-page match chỉ khi scope có quy tắc join explicit và locator multi-span; không tạo match giả giữa hai ấn bản/note. Text normalization là derivative với mapping nhiều-một/một-nhiều; không sửa canonical để tăng recall. Bất biến: extraction revision + artifacts được commit atomically; index rebuild không làm mất evidence. Nếu không còn artifact phải báo stale và reason, không silently redirect.

**Independent check:** resolver nhận file_id, edition_id, raw hash, page index, quote, revision và precision; kiểm raw bytes theo hash; mở ảnh gốc hoặc native text path khác; với scan, người duyệt chữ/vị trí trên ảnh hoặc verified independent GT. Không lấy cùng OCR output so chính nó để cấp VERIFIED. Exact match trong canonical scan chỉ là `EXTRACTED_MATCH`; nếu OCR mất chữ thì exact search vẫn đúng scope canonical, nhưng coverage/fidelity chưa xác nhận. Hai OCR engine đồng ý cũng không tự động thay kiểm gốc. Confidence missing/low/high đều không tự chuyển review state. Schema PASS khác fidelity PASS khác claim PASS.

Precision enum: RAW_FILE, PAGE, REGION, LINE, WORD, CHAR (chỉ khi thật có và validate), DERIVATIVE_ONLY; thiếu inverse giữ PAGE hoặc DERIVATIVE_ONLY. Kiểm điểm độc lập và polygon IoU chỉ nơi GT cùng frame. Nếu transform singular hoặc nonlinear không inverse, cấm highlight raw ở cấp region/word. Provenance reviewer correction lưu phiên bản riêng, original OCR và raw không đổi.

## 7. Multilingual & Retrieval Behavior

OCR-D không cung cấp exhaustive retrieval, sense-aware lexicon, normalized CJK variants, fuzzy hay RAG với nghĩa PRD. Các năng lực này là N/A theo role hoặc external handoff. E12 hỗ trợ input model selection; E13 có registry, nhưng không có benchmark BodhiAtlas. Kiểm riêng:

| Script/profile | Bằng chứng hiện tại | Negative case / yêu cầu |
|---|---|---|
| Việt | Direct Tesseract vie+eng trên scan sạch giữ câu Việt trong fixture; OCR-D chưa chạy | Không/không; dấu hỏi/ngã; đ/d; chú thích nhỏ, chữ nghiêng, tên riêng. |
| Pāli/Sanskrit Latin | Direct baseline mất macron ở nibbāna/anattā; không có model Pāli đã xác minh | a/ā, n/ṇ/ṅ, s/ś/ṣ, NFC/NFD, editorial punctuation. Không dùng bỏ dấu sửa canonical. |
| Hán/giản-phồn/Nôm | Sandbox có chi_sim/chi_tra, không chạy; model Nôm chưa xác minh | 無/无 normalized khác literal, chữ dị thể/rare Nôm, vertical order; missing glyph, không tự chuyển giản. |
| Tạng/Wylie | Sandbox có bod/Tibetan, không chạy; Wylie là transliteration rule riêng | tsheg, combining marks, stack, dấu câu; không coi Wylie text là cùng chuỗi Unicode. |
| Historic Latin/Fraktur | Registry model Fraktur E13 | Không đại diện manuscript, ligature/punctuation policy; GT theo witness. |
| Handwriting/manuscript | UNKNOWN | Cần ảnh được phép, model đúng script/hand, independent GT; không mặc định train model. |

EXACT: scan literal case-sensitive canonical codepoints, enumerate mọi occurrence (kể cả overlapping nếu policy), không phụ thuộc top-K. NORMALIZED: mapping có version, cả NFC/NFD, accent fold, case/spacing; hiển thị nguyên văn và offset; Hán giản-phồn, transliteration không đồng nhất meaning. FUZZY: candidates có giới hạn công khai, không gán EXACT; LEXICON: sense-specific mapping có chứng cứ; SEMANTIC: tùy chọn, tách ranking với truth. Query rỗng từ chối. Repeated phrase across two files → distinct evidence records. Literal search scope declared page statuses + excluded reasons; không trả kết luận vắng mặt toàn kinh điển từ thiếu scan. 

Định nghĩa metric POC: codepoint CER = Levenshtein edits / số codepoints GT sau normalization khai báo; grapheme CER báo riêng; WER = edits theo tokenizer version / token count GT (whitespace chỉ phù hợp fixture Latin, CJK/Tạng phải có tokenizer phù hợp). Empty GT: rate undefined, ghi insertion count; không chia 0/loại âm thầm. Micro = tổng edits/tổng denominator; macro = mean per page có denominator, báo số trang undefined. CER/WER có thể >1. Report mỗi script/role, critical error counts, blank/missing pages riêng. Gold normalized và diplomatic lưu riêng, không lấy output làm GT. Dinglehopper alignment và normalization cần kiểm TC13 trước so sánh trực tiếp với metric tự viết.

## 8. Integration Options

### 8.1 So sánh A–E

| Phương án | Giá trị có thể đạt | Phần còn phải làm / chi phí | Quyết định hiện tại |
|---|---|---|---|
| A full workflow mọi scan | Thống nhất groups, processor contract, layout/GT | Thêm workspace, stage orchestration, model/resource lock, artifact GC, adapter, QA; không giải EPUB/citation; H/VH | Không ưu tiên. Chỉ xét nếu đa số corpus thực cần nhiều stage và TCO thấp hơn. |
| B historical profile | Chuyên biệt layout/deskew/GT, có thể giảm review minutes | Thêm một optional local runner, mapping + historic GT, operational profile; H | TRIAL khi corpus khó đủ rõ và rights cleared. |
| C PAGE/METS + evaluator độc lập | Handoff chuẩn, giữ geometry/GT, ít phụ thuộc runtime | Parser namespace/RO/alternative, strict validation, conversion và evaluator env; M | Ưu tiên nghiên cứu component nếu có PAGE input thật; không tạo parser full spec trước nhu cầu. |
| D processor riêng | Tận dụng recognition/layout cần thiết | Nếu processor phụ thuộc core vẫn mang dependency; direct Tesseract là baseline D-like chứ không đồng nhất OCR-D wrapper; M | So với direct engine bằng cùng model, params; chỉ dùng nếu contract/quality hơn. |
| E QA reference, no runtime | Không thêm dependency; áp dụng manifest, GT, critical checks chung cho mọi parser | Vẫn cần core adapter, independent reopen, synthetic tests; L tăng thêm | **Ưu tiên V1 hiện nay.** |

C không có nghĩa tự xây một implementation PAGE/METS toàn diện: chỉ parse subset cần thiết, reject/mark unsupported phần ngoài contract; lưu artifact gốc để sau này có thể reproject. Nếu đã có thư viện parser nhỏ đáp ứng schema/reproducibility và license tốt, ưu tiên reuse hơn code XML riêng. Không cần xuất PAGE từ mọi native PDF/EPUB chỉ để chuẩn hóa định dạng; có thể dùng source span contract trực tiếp. Tránh duy trì hai nguồn authority. Dinglehopper chạy dev CLI offline khi cần đánh giá, không dùng service luôn bật.

### 8.2 Handoff và migration

Interface đề xuất `extract(input_file_ref, profile, expected_page_set) -> ExtractionCandidate` gồm `manifest_sha`, `processor_pin`, `artifacts[]`, `page_results[]`, `warnings[]`, `cost_metrics`. `project(candidate, canonical_policy) -> revision` không sửa raw. `validate(revision, expected_pages)` không đọc status từ exit code đơn thuần. `reopen(evidence_ref)` độc lập extraction worker. Core có adapter test suite dùng chung; scanner/search nhận canonical revision, không biết OCR-D implementation.

MVP E: một manifest builder, one ingest adapter (direct OCR hoặc Docling tùy corpus), status reconciliation, one raw reader. Nếu có PAGE sources thật: thêm `page_import` chỉ read artifact, schema validation và order/geometry projection, test namespace/version. B: optional process runner sandbox with profile config, mỗi run tạo workspace scratch, no network, one worker, stage boundaries; export results rồi xóa scratch theo retention policy nhưng giữ pinned artifact evidence. Không tự viết editor (dùng công cụ có sẵn khi được nghiệm thu), không huấn luyện model mới. Nếu cần human correction, lưu correction event và reviewed revision.

Migration: initial direct extraction revision R1; OCR-D thử R2 song song, không cập nhật active pointer cho tới G1/G2 smoke + người dùng duyệt scope. Rollback atomically active pointer về R1, giữ R2 audit, reindex lại từ canonical revision. Backup phục hồi hash + locator evidence test trước xóa scratch. Nếu model/namespace thay, run TC04/11/12/15 regression. Dừng nếu fail hard gate, không cải thiện review effort, không có rights hoặc không có profile thực. Nếu chỉ dùng evaluator, lock nó trong dev env; runtime không phụ thuộc. Không thay source pins BCR/Bang-ha; chỉ import có identity và rights.

### 8.3 Bản đồ module kế thừa cụ thể và thứ tự đầu tư (R2)

Quyết định cho từng module dựa trên contract đọc được, không phải cam kết copy mã. Dùng/ghép = thông qua adapter hoặc CLI, không fork mặc định. Chi phí tương đối tăng thêm, chưa đo nhân-ngày. Tên module BodhiAtlas dưới đây là thiết kế đề xuất, không tuyên bố file hiện hữu.

| Module/ý tưởng upstream | Handoff vào BodhiAtlas | Cách reuse tối thiểu | Việc vẫn phải tự sở hữu | Quyết định/stop |
|---|---|---|---|---|
| METS physical map / fileGrp (`ocrd_mets.py`, E02) | `ingest.manifest` | Mượn mô hình expected page set, stage artifacts; import METS khi nguồn dùng chuẩn | File hash, edition/witness, page index/printed label, status reconciliation | Áp dụng concept V1; không dùng mutable METS thay catalog. |
| PAGE models + XSD (`ocrd_models`, E21–24) | `ingest.adapters.page_xml` | Import PAGE chỉ đọc theo namespace, giữ artifact nguyên; validator upstream CLI khi cần | span offsets, role policy, coverage, frame mapping | Trial C trước full workflow; không viết toàn bộ PAGE parser. |
| `page_validator` | `qa.structural` | Chạy validator trong env riêng; no `fix` trên evidence | đối soát source scope, độc lập G2, review reason | Chỉ khi có PAGE input; schema pass không promote VERIFIED. |
| `ocrd_utils.image` affine | `source_map.geometry` | Thử gọi module có pin, hoặc dùng toán affine từ dependency đang có; không copy cả utils | frame IDs, PDF matrix, raw overlay, rounding tolerance | So effort và pixel test; không nhận dewarp nếu thiếu inverse. |
| `ocrd_tesserocr` | `ingest.ocr_profile.historical` | CLI/worker local có chọn profile, chỉ processor cần thiết | raw mount RO, explicit model lock, reject partial | TRIAL nếu direct OCR+layout không đủ; không lấy registry làm chứng nhận script. |
| `task_sequence` + `Processor` | `ingest.runner` | Tham khảo stage interface; gọi upstream runner trong workspace scratch khi nhiều stage | idempotency, revision, timeout, errors, atomic commit | DEFER trừ khi B chứng minh giảm review cost; không thêm service mặc định. |
| Dinglehopper CLI | `qa.benchmark` (dev only) | Tool ngoại tuyến xuất JSON/HTML, lưu policy/config/hash | GT độc lập, per-page coverage, literal và critical errors | Trial tool khi cần nhiều GT; không nhập normalized text làm canonical. |
| GT conventions | `qa.gold` / review queue | Chính sách transcription theo từng script, benchmark fixture | quyền GT, adjudication, review metadata | Áp dụng concept V1; không mặc định SBB rules cho Phật học. |
| Resource manager | packaging/build tooling | Không gọi tải model lúc ingest; pre-provision local read-only | allowlist, SHA, SBOM, rights, archive isolation | Không lấy làm downloader production mặc định. |
| Backup workspace | artifact scratch recovery | Tham khảo; workspace rebuildable | authoritative raw/revision/locator restore | Không thay backup BodhiAtlas. |

**Đường code dự kiến tối giản:** `SourceFile -> ExtractorRegistry -> DirectOCR/Docling | OptionalPageImport | OptionalHistoricalRunner -> ExtractionCandidate -> CoverageGate -> RevisionStore -> CanonicalSpanIndex -> EvidenceResolver -> IndependentReview`. Mỗi adapter chỉ xuất candidate, không có quyền cập nhật `VERIFIED`. Không nhập cả workspace vào catalog như source thứ hai. Mỗi run dùng `run_id`, `adapter_version`, `processor_pin`, `params_hash`, `expected_manifest_hash`, `source_sha`, `stage_input_hashes`, `artifact_sha`, `status`, `warnings`; lỗi/copy/skip không bao giờ đồng nghĩa `READY`. Raw store chỉ đọc; canonical projection bất biến; index tái tạo được. `source_span` chứa unit `unicode_codepoint`, offset nửa mở, role, locator frame, page index/ID/printed label độc lập, polygon nếu có và precision. `evidence_review` tách riêng reviewer, quote hash, revision, timestamp, check method và context. Chỉ đổi active revision khi transaction validate xong, old references vẫn trỏ revision cũ hoặc STALE rõ ràng.

**Không xây thêm gì lúc chưa cần:** không cần METS server, RabbitMQ/queue, OCR-D editor, model training, fork, service evaluator luôn chạy. Nếu có đúng một parser và một local runner, dùng giao diện chung và test chung. Khi có PAGE thật, ưu tiên xác minh khả năng dùng library/CLI sẵn có trước code custom; prototype §13.6 chỉ là đặc tả executable của subset và các cổng, không phải đề nghị tự viết toàn spec. Nếu nền tảng corpus BCR/Bang-ha được dùng, vẫn tiếp nhận một chiều theo catalog authority, không làm OCR-D thành định danh corpus. Nếu không có input scan khó thực sự, dừng ở E.

## 9. Practical POC & Reproduction Plan

### 9.1 Môi trường và phép thử đã chạy

- Sandbox Linux 6.18.57 x86_64 glibc 2.41, CPU AMD EPYC 9V74 (5 logical CPUs nhìn thấy), RAM 5.8 GiB theo `free -h`; không dùng GPU. Python 3.13.5, SQLite 3.46.1, Pillow 12.3.0, NumPy 2.3.5, lxml 6.1.1.0; Tesseract 5.5.0 + leptonica 1.84.1. `ocrd`, `ocrd_models`, `tesserocr`, `dinglehopper` không có trong sandbox.
- Git CLI `git ls-remote https://github.com/OCR-D/core.git HEAD` trả lỗi DNS (exit 128); code đọc qua connector. Không tải packages/models/corpus và không chạy upstream core/processor/evaluator. Không có Docker image lock, SBOM, full dependency resolution. Không suy Python 3.13 tương thích từ >=3.8.
- Baseline dùng binary Tesseract **đã có sẵn**, local `vie+eng` traineddata; SHA-256 vie `79df64caf7bcfb2a27df5042ecb6121e196eada34da774956995747636d5bfa1`, eng `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2`. Chưa xác minh nguồn phát hành/giấy phép bytes model cài sẵn để phân phối production. Không tải hoặc tái phân phối model/font. Chỉ xử lý nội dung tự tạo, không sử dụng kinh sách thật.
- Oracle độc lập: text viết tay trong script trước chạy, render PIL 1400×430 RGB, 300 DPI, DejaVuSans 42, ba dòng; dùng `--psm 6 -l vie+eng`, `OMP_THREAD_LIMIT=1`. GT text SHA-256 `b4dec20ee8d128d755d3144fa279b3a368a0ded2bd73461ac508454c16e3c0cc`; image SHA-256 `33b6637b615f7f2141e3788644230893a256608bea0ebe190586bdaa411758ed`. Font hash trong appendix. Không có ảnh lịch sử thật, không có gold polygon của scan baseline, không test notes/cột. Fixture text và XML tự tạo cho nghiên cứu, không có corpus third-party.

| Phép kiểm thực | Oracle / expected | Actual | Kết quả scope |
|---|---|---|---|
| BL01 direct OCR | Ba dòng đúng GT kể cả macron | Exit 0; Việt đúng trong mẫu, `nibbana anatta.` thay `nibbāna anattā.`; CER 2/64, WER 2/12 theo NFC + collapse whitespace, raw hash giữ nguyên | [TESTED] đối chứng; FAIL exact gold, không phải OCR-D test. |
| I01 XML alternative/order | r1 trước r2 theo oracle độc lập, chọn index 0, `abc\nabc abc` offsets [0,4,8], conf thiếu unknown | Đúng canonical/offsets/conf missing | [TESTED-ISOLATED] PASS fixture toy; không phải PAGE namespace/XSD validator, không phải independent raw reader. |
| I02 manifest missing | expected p1,p2,p3; actual p1,p3 → p2 missing/PARTIAL | p2, PARTIAL | [TESTED-ISOLATED] PASS set logic; chưa thực workspace. |
| I03 affine | crop (10,20), rotation 90° trong y-up, scale 2, 3 điểm forward hand-computed | forward đúng, max inverse abs error 0.0 | [TESTED-ISOLATED] PASS ma trận số; không có pixels hoặc OCR-D transform. |
| I04 negation | `Không có khổ` → `có khổ`: 6 char edits, 1 word edit | CER 6/12; WER 1/3 | [TESTED-ISOLATED] PASS oracle metric, semantic risk được flag theo policy thiết kế; chưa chạy dinglehopper. |

Đo BL01 wall clock 0.236 s cho một subprocess (kể startup), không phải throughput steady-state, không có peak RSS/GPU/disk/reviewer minutes. CER 3.125%, WER 16.67% trên mẫu, không ngoại suy. Hai lỗi dấu trên Pāli là lý do không gán VERIFIED tự động dù output phần Việt trông tốt. I01 XML cố tình rút gọn không namespace, order oracle cung cấp ngoài XML, không giả test reading order upstream. I03 error 0 trên tọa độ nguyên toán học không chứng minh pixel fidelity sau deskew. Không sử dụng kết quả cô lập để pass G1/G2.

### 9.2 TC01–TC16 (đủ tất cả, expected/actual tách)

Mọi actual OCR-D đều null; bảng ghi đối chứng/isolated nếu có. `NT` = NOT TESTED upstream, `PARTIAL-ISOLATED` không là PASS của TC đầy đủ.

| TC | Fixture, thao tác | Expected / acceptance | Actual | Status |
|---|---|---|---|---|
| TC01 | wheelhouse core 3.13.3 + processor 0.21.2 + evaluator pin, CPU, network denied | dependency/weights hash, no egress, help + smoke succeeds | null; git DNS blocked; local baseline only | NT |
| TC02 | p1,p2,p3 declared; image/PAGE groups thiếu p2 | p2 MISSING, revision PARTIAL, SHA raw unchanged; coverage 100% statuses | null upstream; I02 pass set logic | PARTIAL-ISOLATED |
| TC03 | scan hai cột, header/footer/note, chữ Không; gold order/role | no omitted region or false VERIFIED; polarity check | null; BL01 không phải 2 cột | NT |
| TC04 | crop/rotate/deskew/resize + known landmarks, nonlinear variant | raw locator roundtrip within agreed pixel tolerance, downgrade without inverse | null; I03 max 0 toán học | PARTIAL-ISOLATED |
| TC05 | TextEquiv 0/1, absent/high/low conf, wrong high conf | selected alternative only, missing unknown, no auto G2 | null; I01 checks index/conf only | PARTIAL-ISOLATED |
| TC06 | multi-region order, nested regions, line/word/glyph missing | gold order/coverage; granularity truthful | null; I01 synthetic order externally specified | NT |
| TC07 | modern Việt/Pāli/Hán/Tạng, Wylie negative | per script CER/WER, diacritics exact gold, no unsupported claims | null OCR-D; BL01 lost two macrons | PARTIAL-BASELINE (FAIL exact gold BL01) |
| TC08 | legal historic print/handwriting, degradation | same gold vs direct, correction minutes & fidelity | null; historic fixture not available | NT |
| TC09 | processor crash, malformed XML, bad ref, duplicate group, path outside sandbox | explicit partial/error, no raw write, no false READY | null | NT |
| TC10 | two editions with repeated string; print label ≠ index | 0 wrong file/edition/page on positives | null | NT |
| TC11 | PAGE/METS schema pins, serialize/export roundtrip | preserve IDs/roles/order/geometry/lineage; schema PASS ≠ text PASS | null; no XSD validated | NT |
| TC12 | rerun changed params/model; existing output policy | new immutable revision, old cite valid or stale | null | NT |
| TC13 | evaluator negative cases: negation, whitespace, NFC/NFD, empty GT | independent expected edits + denominator, critical errors separate | null evaluator; I04 6/12 & 1/3 | PARTIAL-ISOLATED |
| TC14 | human GT correction original OCR vs reviewed | reviewer, correction reason/revision, no raw/original overwrite | null | NT |
| TC15 | PAGE adapter → canonical → all occurrences → raw independent reopen | offsets all occurrences; honest precision; 0 false VERIFIED | null; I01 offsets [0,4,8] only | PARTIAL-ISOLATED |
| TC16 | paired direct/Docling/OCR-D same render/gold, optional MinerU/Marker | per-profile quality/review time/CPU/RAM/disk/latency/ops | null comparison; BL01 wall 0.236 s single case | PARTIAL-BASELINE |

### 9.3 Fixture/commands cho lần kiểm tiếp theo [PLAN]

1. Dựng locked wheelhouse/image ngoài môi trường dữ liệu riêng sau legal review. Pin core release + exact wheel hashes, processor build + Tesseract/libtesseract/leptonica versions, dinglehopper version + helper dependencies, Python minor đã được support, schema bundles, model files hashes, OS image digest. Tạo SBOM/license report. Không dùng `pip install latest`, không tự tải tài nguyên từ URL registry. Cài offline `python -m pip install --no-index --find-links ./wheelhouse --require-hashes -r requirements.lock`; file lock chưa tạo. Chạy `ocrd --version`, `ocrd workspace --help`, `ocrd-tesserocr-recognize --help`, `dinglehopper --help`, `tesseract --list-langs`. Kiểm options đúng release trước lệnh dưới.
2. Tạo `gold/manifest.json` trước processor: raw SHA, expected page set, edition ID, render dimensions/DPI, region polygons từ nguồn tạo ảnh (không từ OCR), explicit order, role, GT text + script/language, transcription policy. Mỗi page có 1 ảnh raw copy; cố tình thiếu một PAGE/group nhưng không xóa khai báo trang. Tạo 2 cột: header riêng, L1/L2 trái, R1/R2 phải, note chân trang, một câu phủ định; tạo bản ấn bản B cùng câu nhưng page label khác. Sinh gold text, coordinates và occurrence offsets bằng fixture author độc lập, hash mọi file. Chọn 1–2 trang lịch sử quyền rõ nếu có, ghi source/license, người duyệt GT; không tải không phép. Không trộn GT và candidate.
3. Ví dụ lệnh **chưa thực thi**, option syntax cần đối chiếu help đúng pin, thực hiện từ thư mục scratch chứa `raw/p1.png` v.v.:

```sh
# PLAN ONLY. raw originals reside outside scratch read-only; scratch has copies.
ocrd workspace init
ocrd workspace add -g OCR-D-IMG -i IMG_0001 -G PHYS_0001 -m image/png raw/p1.png
ocrd workspace add -g OCR-D-IMG -i IMG_0003 -G PHYS_0003 -m image/png raw/p3.png
ocrd workspace list-pages
ocrd workspace validate
# Keep PHYS_0002 in external expected manifest even if absent in METS.
export OCRD_MISSING_INPUT=ABORT OCRD_MISSING_OUTPUT=ABORT OCRD_EXISTING_OUTPUT=ABORT
export OCRD_MAX_PARALLEL_PAGES=1
ocrd-tesserocr-recognize -I OCR-D-IMG -O OCR-D-OCR -p params.json
ocrd workspace validate
# GT and output must use same physical IDs, each generated separately.
ocrd-dinglehopper -I OCR-D-GT-PAGE,OCR-D-OCR -O OCR-D-OCR-EVAL
# Standalone evaluator example: check pinned help for exact options.
dinglehopper gold/p1.txt candidate/p1.txt eval/p1
```

`params.json` chỉ lập sau khi đọc pin `ocrd-tool.json` và `--help`; explicit language model, segmentation/textequiv level, resources absolute read-only; không suy defaults. Ghim từng processor stage, nếu dùng deskew/segment riêng ghi input/output groups mới, không reuse group. Cố tình bad ref/duplicate/invalid namespace, inject error giữa workflow trong scratch; status derived bằng reconciliation, không coi exit zero là pass. Chạy rootless container `--network none --read-only` (scratch writable volume, input read-only), giới hạn pids/memory/time, no credentials, no external calls. Không chạy archive lạ.

4. TC04 transform oracle: tạo ảnh có fiducial markers, record raw coordinates independently, transform crop/rotation/resize có biết matrix và điểm thực (PIL rendering), so raw point error median/max, polygon IoU; chọn tolerance trước run theo DPI, ví dụ ≤2 pixels với fixture affine integer clean (đề xuất, chưa được chấp thuận), report rounding, bounds. Với dewarp không có inverse map, phải downgrade precision; không giả pass vì page reopen được. Cần kiểm cả PDF render→PDF coords và EXIF orientation.
5. TC15: projection policy order/roles/alternatives version; expected all-occurrence offsets từ gold canonical và canonical candidate scope riêng, compare multiset `(file,rev,start,end)`; verify raw independent trên từng positive và adversarial wrong file/rev, wrong quote, wrong coordinates. Một match đúng OCR string nhưng raw chữ khác phải không VERIFIED. Tách recall search trong canonical và recognition fidelity. TC12 giữ R1 hashes, rerun R2, index rebuild, reopen R1 hoặc stale explicit.
6. TC16 paired: cùng model+params nếu so wrapper vs direct Tesseract (isolate orchestration), cùng image/DPI/GT nếu so quality profile; direct Docling pinned model, optional MinerU/Marker chỉ khi format phù hợp. Cold/warm đo riêng, nhiều run, log hardware/version; `/usr/bin/time -v` peak RSS/wall, disk bytes theo stage, GPU memory nếu dùng, correction minutes bởi reviewer không biết tool, omitted region/page, critical errors, setup hours đo thực, dependency/service count, upgrade/restore time. Không có data số hiện tại ngoài BL01.

### 9.4 Decision thresholds

Cổng cứng (mọi candidate): raw mutation = 0; 100% expected pages có trạng thái, không false READY; wrong file/edition/false VERIFIED = 0 trên toàn bộ fixture positives/negatives; exact occurrence oracle equality; no unauthorized egress; model/GT/scan rights có bằng chứng. Missing source hoặc unsupported precision hạ trạng thái rõ, không đánh giá bằng trung bình. Ngưỡng CER/WER không phổ quát cho chữ cổ; chọn trước per-profile theo mục đích (discovery vs verified transcription), report critical errors riêng. Nếu quality gain không làm giảm correction minutes hoặc ops TCO vượt lợi ích thì không thêm workflow. Nếu baseline direct qua hard gates với chất lượng đủ cho profile thường, dừng A. Nếu B có paired improvement ổn định và không thêm authority, mở trial B có phạm vi. Nếu C adapter pass và tránh nhiều stage hơn, chọn C trước B. Không dùng chi phí giả nhân-ngày hay số model trong registry làm score.

### 9.5 Thực nghiệm R2 đã chạy: đối chứng đa ngữ + projection subset

**Scope:** 11 lần chạy executable Tesseract local (BL02–BL12; không phải `ocrd-tesserocr`), cộng một suite adapter toy (I05). Tất cả 11 lệnh returncode 0, stderr rỗng và hash ảnh input giữ nguyên. Môi trường cùng sandbox R1, Tesseract 5.5.0, OMP_THREAD_LIMIT=1, Python/Pillow/regex/RapidFuzz/lxml đã có sẵn; không tải weights/font, không gửi dữ liệu, temporary files tự dọn. Script đầy đủ và stdout gốc ở §13.6. Mỗi ảnh GT khai báo trước OCR, SHA text/ảnh/model/font log riêng. Nguồn model bytes local chưa xác minh license/provenance để phân phối; các model có tên giống registry không bảo đảm byte-identical. Không dùng nội dung sách thật.

**Metric độc lập:** NFC + collapse whitespace, codepoint Levenshtein (cp), grapheme clusters `regex \X`, whitespace-token distance (không gọi là WER ngôn ngữ học cho Hán/Tạng); numerator/denominator explicit. Không loại dấu/case/negation. Mọi số 0 ở đây là khớp normalized trong metric này, không khẳng định literal hay toàn corpus. Time là wall time subprocess gồm startup; không đo RAM, cost reviewer hoặc throughput. Không chạy evaluator upstream, không so trực tiếp CER của nó. Không aggregate các lần tuning hoặc crop như independent samples.

| ID/Model/PSM | CP edits / ref | Grapheme edits / ref | Token edits / ref | Wall s | Kết quả |
|---|---:|---:|---:|---:|---|
| VI / vie / 6 | 1/35 | 1/35 | 1/8 | 0.170 | Sai normalized |
| PALI / lat / 6 | 12/42 | 12/42 | 5/6 | 0.223 | Sai normalized |
| PALI_eng / eng / 6 | 8/42 | 8/42 | 5/6 | 0.153 | Sai normalized |
| PALI_Latin / Latin / 6 | 3/42 | 3/42 | 2/6 | 0.460 | Sai normalized |
| HAN / chi_tra / 6 | 0/17 | 0/17 | 0/5 | 0.165 | Đúng normalized |
| TIB / bod / 6 | 2/33 | 1/26 | 1/2 | 0.064 | Sai normalized |
| COL / vie / 3 | 34/106 | 34/106 | 10/22 | 0.239 | Sai normalized |
| COL / vie / 6 | 34/106 | 34/106 | 10/22 | 0.187 | Sai normalized |
| COL_crop_0 / vie / 6 | 0/42 | 0/42 | 0/9 | 0.113 | Đúng normalized |
| COL_crop_1 / vie / 6 | 0/38 | 0/38 | 0/8 | 0.118 | Đúng normalized |
| COL_crop_2 / vie / 6 | 0/24 | 0/24 | 0/5 | 0.112 | Đúng normalized |

**Phân tích:** Việt sai `sai`→`saI`; Pāli `lat` 12/42, `eng` 8/42, `Latin` 3/42 trên cùng bitmap, đều lỗi dấu/chữ. Hán truyền thống mẫu sạch khớp 17 codepoints (không ngoại suy Nôm/vertical/historical); Tạng sai `སྡུག`→`ཕྲུག`, chỉ số grapheme 1/26 khác CP 2/33. Hai chế độ whole page PSM 3/6 cùng xen hai cột, 34/106 CP, dù từng câu khá đúng và phủ định còn nguyên. Manual gold crop theo 3 vùng từ rendering plan → chạy PSM 6 từng vùng và nối left/right/note: 0/106 CP, 0/22 whitespace tokens sau normalize, tổng wall 0.343s (chỉ subprocess, **không** gồm người tìm vùng, crop/merge, pipeline). Giữ thêm newline khác raw GT nên không gọi EXACT đối với cả trang. Đây là counterexample cho giả định một bước whole-page luôn đủ; đồng thời chứng minh baseline ít dependency với vùng đã biết có thể đủ, không chứng minh khả năng phân vùng tự động hay lợi thế TCO OCR-D. Pāli model comparison chỉ exploratory, chọn model cần holdout và GT dài hơn.

**I05 — Strict projection suite:** fixture PAGE namespace 2019-07-15 có 3 vùng, physical ID dùng lại giữa 2 edition A/B nhưng ảnh gốc SHA khác, printed label iv/17, TextEquiv index 1 conf .99 sai và index 0 đúng không conf, XML order note/right/left khác reading order. Gold literal `vô thường vô thường\nvô thường\nKhông`, offsets [0,10,20] codepoint; independent expected manifest/boxes định trước từ rendering plan. Adapter giữ 3 region role/geometry, alternative và confidence null, review UNVERIFIED; sai edition bị từ chối, revision đổi khi sửa text, raw unchanged. Manifest p1,p2,p3 với p2 reference không có file ID và p3 absent → p1 CANDIDATE, p2/p3 PARTIAL. Bảy negative cases đều reject: missing reading-order region, duplicate ref, wrong raw, traversal, namespace lạ, DOCTYPE/XXE, malformed XML. Hash mọi fixture ở stdout.

| R2 mapping TC | Expected | Actual & kết luận scope |
|---|---|---|
| TC02/09 | missing page/ref không READY, invalid XML reject | I05 đạt trong mô hình subset; real workspace failure/retry NOT TESTED |
| TC03/06 | đúng order cột/note, không tự verified | Direct whole-page FAIL order, manual gold crop normalized PASS; I05 đúng role/order fixture, tự động layout upstream NOT TESTED |
| TC05 | index 0 wins; conf missing unknown, alternatives retained | I05 PASS synthetic subset; upstream TextEquiv roundtrip NOT TESTED |
| TC07 | kiểm từng script, không nhầm mất dấu | 6 lần direct single-script/profile, kết quả trên; model OCR-D/historic/Nôm/Wylie NOT TESTED |
| TC10/12 | wrong edition reject, revision bất biến | I05 PASS memory-only; durable storage, reader, migration/reindex NOT TESTED |
| TC11 | XSD schema/roundtrip | Schema read xác nhận phiên bản E21/E22; fixture thiếu Metadata và không validate; actual upstream=null |
| TC15 | all literal offsets, map/reopen đúng source | 3 offsets đúng canonical, checks raw digest + declared boxes đúng, cross-edition rejected, no auto VERIFIED; chưa có visual quote verification, PDF reader hay production index |
| TC16 | paired comparison cùng gold và TCO | Chỉ so direct PSM/config/manual crop; OCR-D/Docling/Marker/MinerU comparison actual=null |

TC01/04/08/13/14 upstream chưa chạy; TC04 R1 affine toy vẫn có, TC13 R1 metric toy vẫn có, không nâng status. Tất cả G1/G2 production NOT DEMONSTRATED. I05 không là parser XSD-valid hay một hệ thống thật; gold text/geometry và ảnh được dựng cùng rendering plan (oracle độc lập với candidate computation nhưng không phải independent visual transcription); checks coordinate equality không đo pixel IoU. Không kiểm PDF render DPI/page labels thực, nested RO, non-text omission, nonlinear dewarp, char mapping, persistence/backup, full path/symlink/zip race. Fixture tạo từ synthetic plaintext, không đại diện OCR noise. Stop rule không thay: nếu direct baseline đạt yêu cầu trên corpus thật với review cost thấp hơn, không thêm OCR-D runtime; nếu segmentation tự động của B giảm correction time và vượt strict gates, nâng B có giới hạn.

## 10. Deployment, Security, Legal, Cost

### 10.1 Vận hành và threat model

OCR-D core Python packages/validators + processor binary libs + traineddata + optional server khi parallel >1 (E11). V1 profile nhỏ chỉ cần CLI/process local, không khởi tạo RabbitMQ/METS server/cloud chỉ vì có trong ecosystem. Process isolated workspace, immutable input mount, no network, bounded CPU/RAM/time/disk; failed worker cannot commit READY. ResourceManager/Resolver có đường download (E10); không thể suy offline mặc định. Block network ở OS/container, verify local resources, no tokens/env secrets. Không gọi resource downloads tự động, đặc biệt không gửi ảnh scan đi cloud. `ocrd workspace backup` có CLI (E03/E16) không bảo đảm backup đầy đủ original/derived/catalog/rights/index; backup BodhiAtlas đồng bộ revision manifest, blob hashes, DB transaction, schema/version/lockfile, restore offline và reopen sample/negative.

Untrusted XML: dùng namespace-aware parser, disable entities/DTD/external refs, no network, max depth/bytes/attributes; validate against trusted local XSD hash, not remote schemaLocation; test XML bombs/malformed input. METS FLocat and PAGE imageFilename/AlternativeImage: reject absolute path, `..`, symlink traversal, URL scheme ngoài policy; resolve inside sandbox, verify MIME/size/hash; không dùng path input làm shell string. ZIP: reject traversal, symlinks/device, duplicate names, decompression bomb; cap bytes/member count, no blind extraction. PDFs/images: resource limits, page counts, pixel bomb, renderer sandbox; keep originals untouched. Report path and exception redacted. E10 cho thấy cần xem archive/download code trước enable; chưa audit exploit hoặc CVE, không tuyên bố vulnerable/safe. Run SBOM scanner offline (advisory database pinned) và dependency policy trước production.

### 10.2 Quyền và điều khoản

| Lớp | Bằng chứng / trạng thái | Hành động |
|---|---|---|
| Core code | Apache-2.0 LICENSE E15, thường cho phép commercial/reuse với conditions | Giữ LICENSE/NOTICE nếu có, attribution/change notices, patent terms; NOTICE chưa đọc trực tiếp. |
| OCR-D Tesserocr wrapper | [CONFLICT] LICENSE chứa MIT-style grant, pyproject ghi Apache-2.0 | Không chọn license thuận tiện; xác nhận upstream release/wheel LICENSE, per-file headers và giải thích maintainer trước phân phối. |
| Dinglehopper | Apache-2.0 LICENSE E15 | Dependencies/license scan; chưa xem NOTICE, package license artifact. |
| Native binaries/Tesseract/Leptonica | Chưa xác minh license files của bản cài, không gán quyền từ core | SBOM exact binary, lib versions và notices. |
| Models | Registry URLs không là grant; Fraktur/custom training corpus và `.traineddata` licenses riêng | Lock bytes + license/model card/attribution/training rights; không tải khi chưa clear. |
| Scan/PDF/GT | Không có corpus lịch sử được cấp phép trong P60 | Rights record per edition/witness/image/transcription; quyền ingest, lưu, review, trích, phân phối, cloud khác nhau. |
| Cloud/API | Không có cloud được dùng; chưa audit service terms | Nếu cần, approve vendor terms/region/retention/no training; opt-in explicit. Không áp license code cho cloud terms. |

Không có kết luận pháp lý cuối cùng; code Apache không tự cho quyền bản dịch Phật học, ảnh thư viện, GT hoặc weights. Không chuyển dữ liệu qua public repo; synthetic fixture chỉ nội dung tự tạo, không tái phân phối font/weights.

### 10.3 Chi phí và TCO

Measured: một ảnh BL01 wall 0.236 s, CPU subprocess giới hạn 1 thread, hai edits, không đo peak memory/disk/ops. `measured_cost` về monetary/engineering time = UNKNOWN. Không so với benchmark quảng cáo. Mô hình quyết định (đơn vị tiền hoặc giờ quy đổi thực tế): TCO(profile) = setup + adapter + rights review + lock/upgrade + compute + storage/backup + correction/review + failure recovery + migration/restore. Chi phí core identity/reopen là chung và không nên tính hai lần khi so A–E. Delta B/E gồm workload historical × (correction_time_E − correction_time_B) + tránh sửa glue − added setup/ops/artifact storage. Chỉ dùng số đo thực; nếu không có corpus lịch sử thì benefit chưa biết, ưu tiên trì hoãn dependency. Không đề xuất cloud GPU, editor mới, model training hay service orchestration chưa cần.

## 11. Comparison & Trade-offs

| Đối tượng | Vai trò đúng | Giá trị tiềm năng / giới hạn | Trạng thái bằng chứng ở P60 |
|---|---|---|---|
| Direct PDF parser | Native text/layout/coordinates | Tránh OCR khi text layer đúng; cần verify glyph/text ordering, hidden OCR layer | PLAN; không chạy |
| Direct Tesseract | OCR engine | CPU/local/simple; không tự tạo scholarly identity; mất dấu Pāli trong mẫu | TESTED BL01, 1 synthetic image |
| OCR-D + Tesserocr | Workflow + engine wrapper | Per-stage PAGE/METS, geometry, GT; extra integration and lifecycle | CODE E01–E13; NOT TESTED |
| Dinglehopper | Evaluator | GT compare/diff, independent dev tool; không phải engine | CODE E14; NOT TESTED |
| Docling | Document parser/structured layout | Baseline tốt để thử sách thường; adapter provenance, model rights | DOC P12; P60 không audit lại code/chạy |
| MinerU | PDF/document layout OCR | Middle JSON, multiple profiles; cần pin model/coordinates/license | DOC P45; NOT TESTED P60 |
| Marker | PDF conversion/layout | JSON block geometry; không suy char map | DOC P46; NOT TESTED P60 |
| olmOCR | OCR linearization model toolkit | Candidate fallback complex pages, compute/fidelity/rights unknown | DOC P52; NOT TESTED P60 |
| BCR/Bang-ha | Corpus retrieval/adapters/resolver | Đối chứng identity/Gate A/coverage, không OCR engine | DOC P03/P39-R2; không tái audit P60 |
| OCRmyPDF | PDF OCR text-layer workflow | Đối chứng tạo searchable PDF, không thay canonical evidence | Chỉ chức năng khái quát, chưa xác minh upstream ở P60 |
| PaddleOCR | OCR/layout engine ecosystem | Candidate per-script baseline nếu cần; chưa xác minh model/rights | UNKNOWN về fitness; chưa xem upstream code P60 |
| eScriptorium | Annotation/transcription workflow | Candidate human GT/editor cho tài liệu khó, không mặc định cần | UNKNOWN về fitness; chưa xem upstream code P60 |

P14/P15/P16/P19 tên báo cáo truy vấn không thấy, chưa đọc upstream OCRmyPDF/Paddle/eScriptorium trong phạm vi phiên này; do đó không có quyết định chất lượng cho chúng. Tesseract direct dùng local binary, không coi là audit upstream toàn repo. Không xếp dinglehopper cạnh OCR engine bằng CER của output riêng. Fastest useful demo có bằng chứng: direct baseline local. Lowest compliant TCO **chưa đo**; E được chọn vì giảm phụ thuộc trước nhu cầu, không vì chứng minh direct OCR chính xác nhất. Nếu corpus gồm nhiều manuscript có GT/PAGE sẵn, lợi thế C/B tăng rõ: dùng structured order, multi-stage derivatives, evaluation và annotation interoperability thay tự tạo format. Nếu corpus hầu hết born-digital PDF/EPUB, A không giải được native source path, thêm công không cần thiết. Nếu direct baseline mất critical words trên profile lịch sử, có thể thử B hoặc D nhưng vẫn independent verification; không chấp thuận chỉ vì CER giảm. Đảo ưu tiên E→C/B khi hard gates qua + measured reviewer/ops savings, E→A chỉ khi hầu hết scan cần workflow và measured TCO thấp hơn narrow profiles.

## 12. Decision Record for Master Synthesis

| Field | Value |
|---|---|
| target/class | OCR-D/core; workflow/standard/QA component |
| snapshot | c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3 / v3.13.3; 2026-09-16 |
| license | Core Apache-2.0; processor conflict; evaluator Apache-2.0; weights/corpus UNKNOWN |
| access_status | Source accessed via GitHub; direct clone/install blocked; schema versions pinned; schema runtime validation/full tree not completed |
| primary_role | historical OCR workflow and QA conventions |
| best_fit_v1 | QA reference (E), no default dependency |
| best_fit_v2_v3 | C import/evaluator, B optional historic profile after gates |
| source_fidelity_gate | NOT DEMONSTRATED; adapter + independent reopen required |
| exact_gate | N/A for OCR-D; BodhiAtlas core NOT DEMONSTRATED |
| multilingual_gate | UNKNOWN OCR-D; direct R1/R2 errors on Việt/Pāli/Tạng, one clean Hán fixture normalized match |
| coverage_gate | NOT DEMONSTRATED; skip/copy needs independent manifest |
| rights_security_gate | NOT DEMONSTRATED |
| integration_cost | E L / C M / B H / A H–VH qualitative |
| maintenance_risk | Full workflow MED/HIGH relative (inferred), E LOW incremental |
| recommendation/confidence | DEFER / MED architecture; LOW quality/TCO |
| tests_executed | OCR-D upstream 0; direct baseline 12 subprocess calls (R1 1, R2 11); isolated 4 R1 + 1 R2 suite (7 negative cases) |
| measured_cost | BL01 wall 0.236 s; R2 subprocess wall time §9.5; manual crop sum 0.343 s excluding layout/review; production cost null |
| next_poc | A: TC02/09/12; B: TC03/04/06/15; C: TC07/08/13/16 |

**Top 5 strengths:** (1) stage/file-group contract; (2) physical page links; (3) PAGE hierarchy and geometry/reading order; (4) affine helpers + processor metadata; (5) separate GT/evaluation and local CLI ecosystem. **Top 5 blockers:** (1) no upstream runtime evidence; (2) mutable/skip/copy workflow ≠ declared coverage/revision; (3) dewarp/coordinate frame and independent raw reopen unresolved; (4) multilingual historic model/GT/rights unknown; (5) no paired cost/quality and license conflict. 

Upgrade to USE AS COMPONENT only for narrow C or B after TC01/02/04/09/10/11/12/15 + per-profile quality and rights. Downgrade to REJECT specific profile if hard gate cannot be met without disproportionate custom code, rights incompatible, or repeated regression. Retain QA reference even if processor rejected. `confidence` is not probability or score.

```json
{
  "target": "OCR-D/core",
  "class": "workflow_standard_qa_component",
  "snapshot": {
    "branch": "master",
    "sha": "c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3",
    "commit_date_utc": "2026-09-16T16:37:30Z",
    "release": "v3.13.3",
    "pypi": "3.13.3",
    "bodhi_atlas_sha": "c5dfe50613dfd492407bf1db1061c1cfc9d30e8e",
    "processor_sha": "f412b60c664f41ca6efbafecb1785408750632bd",
    "processor_metadata_version": "0.21.2",
    "evaluator_sha": "1efb382a54c98cf2c6d716d134c57a2d1325a6b6",
    "evaluator_package_version": "0.11.0",
    "processor_pypi_version": "0.21.2",
    "page_schema_namespace": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15",
    "mets_schema_version": "1.12.1",
    "wheel_commit_match_verified": false
  },
  "license": {"core": "Apache-2.0", "processor": "CONFLICT: LICENSE MIT-style / manifest Apache-2.0", "evaluator": "Apache-2.0", "weights_and_corpus": "UNKNOWN"},
  "access_status": "SOURCE_ACCESSED_RUNTIME_BLOCKED_PARTIAL_AUDIT",
  "primary_role": "OCR workflow and PAGE/METS/GT quality assurance",
  "best_fit_v1": "E: QA reference without default runtime dependency",
  "best_fit_v2_v3": "C then B conditional on actual PAGE/historical corpus and measured benefits",
  "source_fidelity_gate": "NOT DEMONSTRATED",
  "exact_gate": "N/A_FOR_OCR_D; CORE_NOT_DEMONSTRATED",
  "multilingual_gate": "UNKNOWN",
  "coverage_gate": "NOT DEMONSTRATED",
  "rights_security_gate": "NOT DEMONSTRATED",
  "integration_cost": {"A": "H-VH", "B": "H", "C": "M", "D": "M", "E": "L", "basis": "qualitative_incremental"},
  "maintenance_risk": "MED-HIGH full workflow, inferred; LOW incremental E",
  "recommendation": "DEFER",
  "confidence": {"architecture": "MED", "code_scope": "HIGH", "quality_cost": "LOW"},
  "tests_executed": {"ocr_d_upstream": 0, "direct_baseline": ["BL01", "BL02", "BL03", "BL04", "BL05", "BL06", "BL07", "BL08", "BL09", "BL10", "BL11", "BL12"], "isolated": ["I01", "I02", "I03", "I04", "I05_suite"], "i05_negative_cases": 7, "production_gates_passed": 0},
  "measured_cost": {"baseline_wall_seconds": 0.236, "baseline_pages": 1, "r2_direct_calls": 11, "r2_distinct_full_page_images": 5, "r2_manual_crop_subprocess_sum_seconds": 0.343, "peak_rss_bytes": null, "human_review_minutes": null, "currency_cost": null, "integration_hours": null},
  "next_poc": ["TC02/09/12", "TC03/04/06/15", "TC07/08/13/16"]
}
```

## 13. Appendix

### 13.1 Inventory — file source thật đã mở (đọc có chọn lọc)

Core base URL `https://github.com/OCR-D/core/blob/c9272c82b2f4bf62ca7fa6773c00980a7b8e67b3/` + path. Các dòng xác định từ kết quả fetch file; hàm/test được nhận diện không có nghĩa chạy. Các nhóm code quan trọng được đọc kỹ đoạn ở E04/E05/E06/E07; với các file còn lại đọc excerpt/symbols liên quan, không khẳng định audit toàn văn.

| File | Dòng tổng | Vai trò đã xem |
|---|---:|---|
| README.md | 205 | package/specs, docs |
| LICENSE | 202 | Apache 2.0 |
| pyproject.toml | 50 | package, Python, scripts |
| requirements.txt | 44 | lxml/numpy/Pillow, dependencies chưa lock |
| src/ocrd/workspace.py | 1241 | download, add/remove, image transforms, save METS |
| src/ocrd/resolver.py | 326 | resolver / HTTP / workspace init |
| src/ocrd/processor/base.py | 1374 | processing, errors, output, zip, metadata |
| src/ocrd_models/ocrd_mets.py | 1089 | group/page/label |
| src/ocrd_models/ocrd_page.py | 269 | wrapper + serialization |
| src/ocrd_models/ocrd_file.py | 276 | identity/location |
| src/ocrd_modelfactory/__init__.py | 119 | page_from_image/page_from_file |
| src/ocrd_utils/image.py | 645 | inverse/forward transform helpers |
| src/ocrd_utils/config.py | 330 | runtime policies |
| src/ocrd_utils/constants.py | 139 | constants; schema version chưa xác minh |
| src/ocrd/cli/workspace.py | 1015 | init/add/validate/list/backup |
| src/ocrd/resource_manager.py | 470 | resource/archive handling |
| src/ocrd_validators/workspace_validator.py | 407 | workspace structural validation |
| src/ocrd_validators/page_validator.py | 530 | reading order/text/coords validation |
| tests/test_workspace.py | 756 | overwrite/backup/download/deskew tests (source only) |

Processor base URL `https://github.com/OCR-D/ocrd_tesserocr/blob/f412b60c664f41ca6efbafecb1785408750632bd/`: README.md (228), LICENSE (21), pyproject.toml (105), ocrd_tesserocr/recognize.py (1223), segment.py (71), ocrd-tool.json (1599). E12/E13/E15 chỉ ra đoạn/hàm quyết định. Evaluator base URL `https://github.com/qurator-spk/dinglehopper/blob/1efb382a54c98cf2c6d716d134c57a2d1325a6b6/`: README.md (153), LICENSE (202), pyproject.toml (115), src/dinglehopper/cli.py (313), src/dinglehopper/ocrd_cli.py (79). Tổng 30 file upstream truy xuất thành công (19 core + 6 processor + 5 evaluator). Không dùng số lượng file như bằng chứng test. Không fetch đầy đủ recursive tree; CI, ocrd-tool schema, PAGE/METS XSD, NOTICE, workflow runner, generated models, evaluator normalization/tests chưa audit hoàn chỉnh. Một số path cũ trả 404 (`ocrd/ocrd/workspace.py`, `ocrd/ocrd/processor/base.py`, `ocrd_models/ocrd_models/ocrd_mets.py`, `tests/test_processor.py`, `qurator/dinglehopper/cli.py`); dùng path `src/` đã fetch được thay thế khi có, không giả file tồn tại.

### 13.2 Raw logs (rút gọn, thật)

```text
$ git ls-remote https://github.com/OCR-D/core.git HEAD
fatal: unable to access 'https://github.com/OCR-D/core.git/': Could not resolve host: github.com
exit 128
$ python probe.py
Pillow 12.3.0 numpy 2.3.5 lxml (6, 1, 1, 0) font_sha 57f73e11f51999432bf7ab22ce55b6f945d5eca1bf824404cfa9ec2e3718c84e
gold_sha b4dec20ee8d128d755d3144fa279b3a368a0ded2bd73461ac508454c16e3c0cc image_sha 33b6637b615f7f2141e3788644230893a256608bea0ebe190586bdaa411758ed
{"test": "direct_baseline", "exit": 0, "stdout": "Không có gì thường hằng.\nVô thường là vô thường.\nnibbana anatta.\n", "stderr": "", "wall_sec": 0.236, "cer": [2, 64], "wer": [2, 12], "raw_unchanged": true}
isolated xml_sha 19a3a7a633e1114c5a820195cfc48b777e8a35821e78079f79b829ac52114c42 canonical 'abc\nabc abc' offsets [0, 4, 8] confidence_missing True
isolated coverage missing ['p2'] status PARTIAL
isolated affine_max_abs_error 0.0
isolated negation CER 6 12 WER 1 3
```

No OCR-D stdout/stderr because it was not executed. Baseline stdout in JSON is actual, newline escaped. No fabricated TC results. Local fixture not copied into report as separate binary; regenerate with script below, font and package versions must match hash if reproducibility byte-exact required. Model files used local only.

### 13.3 Script đã chạy [TESTED baseline + TESTED-ISOLATED]

```python
import hashlib, json, pathlib, subprocess, tempfile, time, unicodedata, os
from PIL import Image, ImageDraw, ImageFont
from lxml import etree
import numpy as np
from PIL import __version__ as pil_version
sha=lambda b:hashlib.sha256(b).hexdigest()
# Oracle fixed before execution; synthetic text, no source corpus.
gold='Không có gì thường hằng.\nVô thường là vô thường.\nnibbāna anattā.'
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
print('Pillow',pil_version,'numpy',np.__version__,'lxml',etree.LXML_VERSION,'font_sha',sha(pathlib.Path(fontpath).read_bytes()))
def dist(a,b):
    row=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        new=[i]
        for j,y in enumerate(b,1): new.append(min(row[j]+1,new[-1]+1,row[j-1]+(x!=y)))
        row=new
    return row[-1]
def norm(s):return ' '.join(unicodedata.normalize('NFC',s).split())
with tempfile.TemporaryDirectory() as d:
    p=pathlib.Path(d)/'scan.png'; im=Image.new('RGB',(1400,430),'white'); draw=ImageDraw.Draw(im); font=ImageFont.truetype(fontpath,42)
    for i,line in enumerate(gold.splitlines()):draw.text((60,60+100*i),line,font=font,fill='black')
    im.save(p,dpi=(300,300)); raw=sha(p.read_bytes()); print('gold_sha',sha(gold.encode()),'image_sha',raw)
    cmd=['tesseract',str(p),'stdout','-l','vie+eng','--psm','6']; t=time.monotonic(); q=subprocess.run(cmd,capture_output=True,text=True,timeout=30,env={**os.environ,'OMP_THREAD_LIMIT':'1'}); elapsed=time.monotonic()-t
    a,b=norm(gold),norm(q.stdout); print(json.dumps(dict(test='direct_baseline',exit=q.returncode,stdout=q.stdout,stderr=q.stderr,wall_sec=round(elapsed,3),cer=[dist(a,b),len(a)],wer=[dist(a.split(),b.split()),len(a.split())],raw_unchanged=raw==sha(p.read_bytes())),ensure_ascii=False))
# Isolated contracts, not OCR-D. Fixture bytes/expected values independent of engine.
xml=b'<PcGts><Page imageFilename="raw.png"><TextRegion id="r2"><TextEquiv index="0"><Unicode>abc abc</Unicode></TextEquiv></TextRegion><TextRegion id="r1"><TextEquiv index="0"><Unicode>abc</Unicode></TextEquiv><TextEquiv index="1" conf="0.99"><Unicode>xyz</Unicode></TextEquiv></TextRegion></Page></PcGts>'
root=etree.fromstring(xml,etree.XMLParser(resolve_entities=False,no_network=True)); reg={x.get('id'):x for x in root.xpath('//TextRegion')}; canonical='\n'.join(reg[i].xpath('./TextEquiv[@index="0"]/Unicode')[0].text for i in ['r1','r2']); offsets=[i for i in range(len(canonical)) if canonical.startswith('abc',i)]; assert canonical=='abc\nabc abc' and offsets==[0,4,8]; assert reg['r1'].xpath('./TextEquiv[@index="0"]')[0].get('conf') is None
print('isolated xml_sha',sha(xml),'canonical',repr(canonical),'offsets',offsets,'confidence_missing',True)
expected={'p1','p2','p3'}; actual={'p1','p3'}; missing=sorted(expected-actual); assert missing==['p2']; print('isolated coverage missing',missing,'status PARTIAL')
# Crop (10,20), rotate 90 degrees ccw in y-up, scale 2. Independent hand-computed points.
M=np.array([[0,-2,40],[2,0,-20],[0,0,1]],float); pts=np.array([[10,20,1],[13,24,1],[18,23,1]],float).T; expected_pts=np.array([[0,-8,-6],[0,6,16],[1,1,1]]); transformed=M@pts; assert np.array_equal(transformed,expected_pts); err=float(np.max(np.abs(np.linalg.inv(M)@transformed-pts))); print('isolated affine_max_abs_error',err)
a='Không có khổ'; b='có khổ'; assert dist(a,b)==6 and dist(a.split(),b.split())==1; print('isolated negation CER',dist(a,b),len(a),'WER',dist(a.split(),b.split()),len(a.split()))
```

Run `python probe.py` after saving exact block, on local env with pinned packages and model bytes; no downloads. Assertions are limited to independent toy oracle; not production integration. Script reports direct OCR failure rather than raising on mismatch because it is measurement, not approval gate. Affine coordinate example y-up mathematical, not PIL pixel coordinate convention; do not reuse matrix as PAGE transform without conversion. XML toy uses no namespaces and should not be treated as valid PAGE-XSD fixture. Neither I01 nor I03 independently reopens raw image; these tests are small exclusion checks only.

### 13.4 Bibliography & upstream validation queue

- [OCR-D organization](https://github.com/OCR-D), [core repo](https://github.com/OCR-D/core), [release list](https://github.com/OCR-D/core/releases), [PyPI package](https://pypi.org/project/ocrd/3.13.3/), [setup guide](https://ocr-d.de/en/setup).
- [OCR-D specifications index](https://ocr-d.de/en/spec/), [METS conventions](https://ocr-d.de/en/spec/mets), [PAGE conventions](https://ocr-d.de/en/spec/page), [GT guidelines](https://ocr-d.de/en/gt-guidelines/trans/), [QA metrics](https://ocr-d.de/en/spec/ocrd_eval). Các trang chính thức đã truy cập, nhưng chưa review toàn văn mọi subsection hoặc pin spec commit.
- [OCR-D Tesserocr](https://github.com/OCR-D/ocrd_tesserocr), [dinglehopper](https://github.com/qurator-spk/dinglehopper). Source permalinks trong ledger, inventory. Không mở rộng thêm processor repo khi chưa có historic profile thật.
- BodhiAtlas pin + 5 docs + 6 đối chứng tại §2.2. Chưa đọc full corpus upstream BCR/Bang-ha ở P60; không dùng báo cáo cũ làm oracle.

### 13.5 Câu hỏi chưa giải quyết và tự kiểm

1. R2 xác nhận PAGE 2019-07-15 và METS 1.12.1 từ pinned XSD; còn thiếu compile/validator execution, actual output TC11, migration, CI/deployment và exact tag/wheel digests. PyPI 0.21.2/0.11.0 đã xác nhận có wheel, chưa cài.
2. Có inverse transform per dewarp processor, raw PDF page→render→original, rounding tolerances? TC04 chưa chạy. Có role/reading order đủ cho footnote/marginalia/vertical script? TC03/06.
3. Which model and rights for historic Pāli/Hán/Nôm/Tạng? Có GT đã cấp quyền, review policy? Không mặc định train hoặc chọn model Fraktur cho Phật học.
4. Có need thực sự multi-stage? Chưa biết corpus composition, review time, storage/backup size, TCO paired; TC16. Release upgrade/regression/restore chưa chạy.
5. Quyền wrapper LICENSE vs manifest và package version, weights provenance, dependency/NOTICE, scan/GT rights cần giải quyết. P14/P15/P16/P19 báo cáo không fetch được ở tên thử; upstream ngoài Tesseract local chưa kiểm, các báo cáo dài đối chứng đọc phần liên quan không đọc hết. Không có P60 cũ được cung cấp để so diff; độc lập với P03/P39-R2/P12/P45/P46/P52, không chép kết luận của chúng. Không có quyết định về toàn bộ BodhiAtlas core được chốt từ P60.

Checklist: đúng canonical repo/snapshot và 2 repo bổ trợ; có 13 phần, C01–C15, G1–G6, H01–H12, TC01–TC16, evidence ledger, valid JSON, log/script thật, decision A–E/rollback/stop rule. Chưa hoàn tất nghiệm thu đầy đủ runtime, XSD/spec version, T01–T16 sổ tay, rights, corpus lịch sử và benchmark; các trạng thái ghi rõ. Scope chọn E vì ít dependency theo hiện trạng bằng chứng, không phải chứng minh nó có quality/TCO tốt nhất trên mọi tài liệu. Đầu tư tiếp theo: TC02/09/12 trên locked offline profile, sau đó TC04/15 trước benchmark lớn; nếu không có corpus lịch sử hoặc PAGE thực thì giữ E và hoãn cả workflow. Không chỉnh repository.


### 13.6 R2 reproduction — mã thực sự đã chạy và log

Lệnh `python /tmp/p60_r2.py` trong sandbox. Chép nguyên code vào file tạm; cần Tesseract 5.5.0 với các traineddata local `vie`, `lat`, `eng`, `Latin`, `chi_tra`, `bod`, font Noto có sẵn và Python dependencies nêu trên; nếu thiếu thì ghi NOT TESTED, không tự tải. Script không dùng OCR-D. GT được khai báo trước chạy; hash font/model/image/text in trong log, không đính kèm fonts/model/corpus. Raw stdout bên dưới chứa text synthetic, không có thông tin riêng tư. Không có benchmark framework runtime.

```python
import hashlib, json, os, subprocess, tempfile, time, unicodedata as ud
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from lxml import etree as E
import numpy as np
import regex
from rapidfuzz.distance import Levenshtein
from copy import deepcopy
H=lambda b:hashlib.sha256(b).hexdigest()
F=lambda p:H(Path(p).read_bytes())
NS='http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15'; M='http://www.loc.gov/METS/'; X='http://www.w3.org/1999/xlink'
N={'p':NS,'m':M,'x':X}; Q=lambda ns,k:f'{{{ns}}}{k}'
P=lambda el,k:el.find('p:'+k,N)
PS=lambda el,k:el.findall('p:'+k,N)
TD=Path('/usr/share/tesseract-ocr/5/tessdata'); LAT='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'; CJK='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; TIB='/usr/share/fonts/truetype/noto/NotoSerifTibetan-Regular.ttf'
# GT declared before OCR; not derived from candidate. Literal oracle NFC grapheme plus codepoints (raw line whitespace).
CASES=[('VI','vie',LAT,'Không có chữ sai.\nVô thường và khổ.'),('PALI','lat',LAT,'nibbāna anattā dukkha\nsaṅkhāra paññā mettā'),('HAN','chi_tra',CJK,'無常 苦 無我\n色即是空 空即是色'),('TIB','bod',TIB,'བདེ་སྡུག་མི་རྟག་པ།\nཆོས་དང་ཤེས་རབ།')]
def norm(t):return ud.normalize('NFC',' '.join(t.split()))
def metrics(gt,actual):
 a,b=norm(gt),norm(actual); g=lambda t:regex.findall(r'\X',t)
 return {'cp':[Levenshtein.distance(a,b),len(a)],'grapheme':[Levenshtein.distance(g(a),g(b)),len(g(a))],'whitespace_token':[Levenshtein.distance(a.split(),b.split()),len(a.split())]}
def ocr(p,gt,lang,psm,fonts):
 cmd=['tesseract',str(p),'stdout','--psm',str(psm),'-l',lang]; h=F(p); t=time.monotonic(); z=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'OMP_THREAD_LIMIT':'1'},timeout=45); sec=time.monotonic()-t
 return dict(id=p.stem,lang=lang,psm=psm,gt=gt,gt_sha=H(gt.encode()),image_sha=h,raw_unchanged=F(p)==h,fonts={Path(f).name:F(f) for f in fonts},weights={lang:F(TD/(lang+'.traineddata'))},actual=z.stdout.strip(),stderr=z.stderr.strip(),rc=z.returncode,seconds=round(sec,3),metrics=metrics(gt,z.stdout))
# Minimal subset adapter. Reject rather than infer nested or unordered groups; no XSD claim.
def parse(data):
 if len(data)>100000 or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():raise ValueError('unsafe XML')
 return E.fromstring(data,parser=E.XMLParser(resolve_entities=False,no_network=True,load_dtd=False,huge_tree=False))
def build_page(image_name, order=('left','right','note')):
 root=E.Element(Q(NS,'PcGts'),nsmap={None:NS}); page=E.SubElement(root,Q(NS,'Page'),imageFilename=image_name,imageWidth='1200',imageHeight='600'); ro=E.SubElement(page,Q(NS,'ReadingOrder')); grp=E.SubElement(ro,Q(NS,'OrderedGroup'),id='g')
 for i,r in enumerate(order):E.SubElement(grp,Q(NS,'RegionRefIndexed'),index=str(i),regionRef=r)
 # document order intentionally different from declared order
 for rid,role,text,box in REGIONS:
  r=E.SubElement(page,Q(NS,'TextRegion'),id=rid,type=role); E.SubElement(r,Q(NS,'Coords'),points=' '.join(f'{x},{y}' for x,y in box)); a=E.SubElement(r,Q(NS,'TextEquiv'),index='1',conf='0.99'); E.SubElement(a,Q(NS,'Unicode')).text='wrong alternative'; a=E.SubElement(r,Q(NS,'TextEquiv'),index='0'); E.SubElement(a,Q(NS,'Unicode')).text=text
 return E.tostring(root)
REGIONS=[('note','footnote','Không',[(70,460),(330,460),(330,525),(70,525)]),('right','paragraph','vô thường',[(650,110),(1000,110),(1000,185),(650,185)]),('left','paragraph','vô thường vô thường',[(70,110),(610,110),(610,185),(70,185)])]
GOLD='vô thường vô thường\nvô thường\nKhông'; GOLD_OFFSETS=[0,10,20]
def project(data,rootdir,manifest):
 root=parse(data)
 if root.tag!=Q(NS,'PcGts'):raise ValueError('namespace')
 page=P(root,'Page'); name=page.get('imageFilename'); f=(rootdir/name).resolve()
 if not f.is_relative_to(rootdir.resolve()) or f!=manifest['raw'].resolve():raise ValueError('raw mismatch')
 if F(f)!=manifest['sha']:raise ValueError('raw digest')
 with Image.open(f) as img:
  if img.size!=(int(page.get('imageWidth')),int(page.get('imageHeight'))):raise ValueError('dimensions')
 regions=PS(page,'TextRegion'); ids=[r.get('id') for r in regions]; by=dict(zip(ids,regions)); grp=P(P(page,'ReadingOrder'),'OrderedGroup')
 if len(by)!=len(ids) or grp is None:raise ValueError('order/ids')
 refs=PS(grp,'RegionRefIndexed'); inds=[int(r.get('index')) for r in refs]; order=[r.get('regionRef') for r in sorted(refs,key=lambda x:int(x.get('index')))]
 if len(refs)!=len(grp) or sorted(inds)!=list(range(len(inds))) or len(order)!=len(ids) or set(order)!=set(ids):raise ValueError('order coverage')
 segments=[]; text=''
 for k in order:
  r=by[k]; alts=PS(r,'TextEquiv'); idx=[int(a.get('index')) for a in alts]
  if len(idx)!=len(set(idx)) or 0 not in idx:raise ValueError('alternative')
  a=alts[idx.index(0)]; v=P(a,'Unicode').text
  poly=[tuple(map(int,p.split(','))) for p in P(r,'Coords').get('points').split()]
  if len(poly)<3 or any(not(0<=x<1200 and 0<=y<600) for x,y in poly):raise ValueError('polygon')
  if text:text+='\n'
  start=len(text); text+=v; segments.append(dict(id=k,start=start,end=len(text),role=r.get('type'),polygon=poly,confidence=a.get('conf'),precision='REGION',review='UNVERIFIED',alternatives=[{'index':j,'text':P(b,'Unicode').text,'conf':b.get('conf')} for j,b in zip(idx,alts)]))
 rev=H(data+manifest['sha'].encode()+b'projection_v1'); return dict(edition=manifest['edition'],page_id=manifest['page_id'],print_label=manifest['label'],raw_sha=manifest['sha'],revision=rev,canonical=text,segments=segments)
def check_reopen(e, manifest, gold_boxes):
 # independent oracle manifest and hand-authored boxes, not candidate output as gold
 if (e['edition'],e['raw_sha'],e['page_id'])!=(manifest['edition'],F(manifest['raw']),manifest['page_id']):return False
 return all(tuple(map(tuple,s['polygon']))==gold_boxes[s['id']] for s in e['segments'])
def mets_status(data,expected):
 root=parse(data); present={}
 for d in root.xpath('//m:structMap[@TYPE="PHYSICAL"]//m:div[m:fptr]',namespaces=N):
  ids=[x.get('FILEID') for x in d.findall('m:fptr',N)]; present[d.get('ID')]=ids
 files={f.get('ID') for f in root.xpath('//m:fileGrp[@USE="OCR"]//m:file',namespaces=N)}
 return {p:('CANDIDATE' if len(set(present.get(p,[])) & files)==1 else 'PARTIAL') for p in expected}
with tempfile.TemporaryDirectory() as td:
 d=Path(td); results=[]
 for tag,lang,font,gt in CASES:
  img=Image.new('RGB',(1600,360),'white'); dr=ImageDraw.Draw(img); ft=ImageFont.truetype(font,60,index=3 if tag=='HAN' else 0); dr.multiline_text((60,40),gt,font=ft,fill='black',spacing=30); p=d/(tag+'.png'); img.save(p,dpi=(300,300)); results.append(ocr(p,gt,lang,6,[font]))
  if tag=='PALI':
   for trial in ('eng','Latin'):
    row=ocr(p,gt,trial,6,[font]);row['id']='PALI_'+trial;results.append(row)
 # independent two-column expected order, same bitmap and model for 2 configs
 img=Image.new('RGB',(1600,1000),'white'); dr=ImageDraw.Draw(img); ft=ImageFont.truetype(LAT,36)
 cols=[(80,170,'Trái một.\nKhông có khổ.\nTrái ba.\nTrái bốn.'),(930,170,'Phải một.\nPhải hai.\nPhải ba.\nPhải bốn.'),(80,810,'Chú thích: không bỏ dấu.')]
 for x,y,t in cols:dr.multiline_text((x,y),t,font=ft,fill='black',spacing=32)
 p=d/'COL.png';img.save(p,dpi=(300,300));gt='\n'.join(t for x,y,t in cols)
 for mode in (3,6):results.append(ocr(p,gt,'vie',mode,[LAT]))
 # Manual gold region boxes predeclared from the rendering plan; not automatic layout.
 crops=[(40,140,800,650),(880,140,1560,650),(40,760,1200,950)]
 pieces=[]
 for k,(box,(_,_,gtpart)) in enumerate(zip(crops,cols)):
  pp=d/f'COL_crop_{k}.png';img.crop(box).save(pp,dpi=(300,300));r=ocr(pp,gtpart,'vie',6,[LAT]);results.append(r);pieces.append(r)
 joined='\n'.join(r['actual'] for r in pieces);print('MANUAL_CROP',json.dumps({'boxes':crops,'actual':joined,'metrics':metrics(gt,joined),'sum_seconds':round(sum(r['seconds'] for r in pieces),3),'raw_sha':F(p)},ensure_ascii=False))
 print('DIRECT',json.dumps(results,ensure_ascii=False))
 # raw fixture created independently of PAGE output; second edition visually different and different sha
 man=[]
 for edition,label in [('A','iv'),('B','17')]:
  p=d/(edition+'.png'); im=Image.new('RGB',(1200,600),'white');dr=ImageDraw.Draw(im);dr.text((30,20),edition,font=ft,fill='black')
  for rid,role,txt,box in REGIONS:dr.text((box[0][0],box[0][1]),txt,font=ft,fill='black')
  im.save(p,dpi=(300,300));man.append(dict(raw=p,sha=F(p),edition=edition,page_id='PHYS_1',label=label))
 data=build_page('A.png'); a=project(data,d,man[0]); b=project(build_page('B.png'),d,man[1]); gold_boxes={r[0]:tuple(r[3]) for r in REGIONS}
 offsets=[m.start() for m in regex.finditer('vô thường',a['canonical'],overlapped=True)]
 assert a['canonical']==GOLD and offsets==GOLD_OFFSETS and [s['role'] for s in a['segments']]==['paragraph','paragraph','footnote']; assert all(s['confidence'] is None and s['review']=='UNVERIFIED' for s in a['segments']); assert check_reopen(a,man[0],gold_boxes) and not check_reopen(a,man[1],gold_boxes); assert a['revision']!=b['revision']; assert a['print_label']=='iv' and b['print_label']=='17'
 print('PROJECTION',json.dumps({'page_sha':H(data),'raw_A':man[0]['sha'],'raw_B':man[1]['sha'],'canonical':a['canonical'],'offsets':offsets,'regions':a['segments'],'revision_A':a['revision'],'revision_B':b['revision'],'cross_edition_rejected':True},ensure_ascii=False))
 # one altered derivative never redirects old revision
 root=parse(data); root.xpath('//p:TextRegion[@id="left"]/p:TextEquiv[@index="0"]/p:Unicode',namespaces=N)[0].text='vô thường'; new=project(E.tostring(root),d,man[0]); assert new['revision']!=a['revision'] and a['canonical']==GOLD
 # failure cases
 cases={'missing_region':build_page('A.png',('left','right')),'duplicate_ref':build_page('A.png',('left','left','note')),'wrong_raw':build_page('B.png'),'traversal':build_page('../A.png'),'bad_namespace':data.replace(NS.encode(),b'urn:unknown'),'XXE':b'<!DOCTYPE x [<!ENTITY x SYSTEM "file:///etc/passwd">]><x>&x;</x>','malformed':data[:-15]}
 for k,v in cases.items():
  try:project(v,d,man[0]);raise AssertionError('accepted '+k)
  except (ValueError,E.XMLSyntaxError) as ex:print('NEGATIVE',k,type(ex).__name__,str(ex).splitlines()[0][:100],H(v))
 met=f'<mets xmlns="{M}"><fileSec><fileGrp USE="OCR"><file ID="o1"/></fileGrp></fileSec><structMap TYPE="PHYSICAL"><div><div ID="p1"><fptr FILEID="o1"/></div><div ID="p2"><fptr FILEID="missing"/></div></div></structMap></mets>'.encode();status=mets_status(met,['p1','p2','p3']);assert status=={'p1':'CANDIDATE','p2':'PARTIAL','p3':'PARTIAL'};print('METS',H(met),status)
 assert F(man[0]['raw'])==man[0]['sha'] and F(man[1]['raw'])==man[1]['sha']; print('REVISION',new['revision'],'old canonical retained',a['revision'],'RAW UNCHANGED')
```

```text
MANUAL_CROP {"boxes": [[40, 140, 800, 650], [880, 140, 1560, 650], [40, 760, 1200, 950]], "actual": "Trái một.\nKhông có khổ.\nTrái ba.\n\nTrái bốn.\nPhải một.\nPhải hai.\nPhải ba.\nPhải bốn.\nChú thích: không bỏ dấu.", "metrics": {"cp": [0, 106], "grapheme": [0, 106], "whitespace_token": [0, 22]}, "sum_seconds": 0.343, "raw_sha": "1d0674ceccf3846047332be24873434acbc1dca49a0351e640e7174d4960ecc1"}
DIRECT [{"id": "VI", "lang": "vie", "psm": 6, "gt": "Không có chữ sai.\nVô thường và khổ.", "gt_sha": "e49d881ea95f5189cca3b246b4d517b2f7a0fc4d58ffbc254706b00784028143", "image_sha": "6638da371e64aa0bcd40e7b3d40d6a2126d364760b25918de320a88f6568d519", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"vie": "79df64caf7bcfb2a27df5042ecb6121e196eada34da774956995747636d5bfa1"}, "actual": "Không có chữ saI.\nVô thường và khổ.", "stderr": "", "rc": 0, "seconds": 0.17, "metrics": {"cp": [1, 35], "grapheme": [1, 35], "whitespace_token": [1, 8]}}, {"id": "PALI", "lang": "lat", "psm": 6, "gt": "nibbāna anattā dukkha\nsaṅkhāra paññā mettā", "gt_sha": "80a41051cd8bd35697c98d17f60fc07490167c0042e1d375f7ae73e15474dc87", "image_sha": "bb0ff068c3de4c1c672158faaca3a426ebe85139966f57bd28422dd8bf674ca7", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"lat": "3859d8ba60404f4b79830622625bbc76fb4ee2808eac1ad360ffa77f0a533328"}, "actual": "nibbàna anatta dukkha\nsankhaàra pafrifia metta", "stderr": "", "rc": 0, "seconds": 0.223, "metrics": {"cp": [12, 42], "grapheme": [12, 42], "whitespace_token": [5, 6]}}, {"id": "PALI_eng", "lang": "eng", "psm": 6, "gt": "nibbāna anattā dukkha\nsaṅkhāra paññā mettā", "gt_sha": "80a41051cd8bd35697c98d17f60fc07490167c0042e1d375f7ae73e15474dc87", "image_sha": "bb0ff068c3de4c1c672158faaca3a426ebe85139966f57bd28422dd8bf674ca7", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"eng": "7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2"}, "actual": "nibbana anatta dukkha\nsankhara panna metta", "stderr": "", "rc": 0, "seconds": 0.153, "metrics": {"cp": [8, 42], "grapheme": [8, 42], "whitespace_token": [5, 6]}}, {"id": "PALI_Latin", "lang": "Latin", "psm": 6, "gt": "nibbāna anattā dukkha\nsaṅkhāra paññā mettā", "gt_sha": "80a41051cd8bd35697c98d17f60fc07490167c0042e1d375f7ae73e15474dc87", "image_sha": "bb0ff068c3de4c1c672158faaca3a426ebe85139966f57bd28422dd8bf674ca7", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"Latin": "6dbdaf8ecc6c40f025c2648bf3b3f3fbffe073e1fd2df2047fde2e2b2f020d53"}, "actual": "nibbāna anattā dukkha\nsañůkhāra pañňā mettā", "stderr": "", "rc": 0, "seconds": 0.46, "metrics": {"cp": [3, 42], "grapheme": [3, 42], "whitespace_token": [2, 6]}}, {"id": "HAN", "lang": "chi_tra", "psm": 6, "gt": "無常 苦 無我\n色即是空 空即是色", "gt_sha": "70f63a9fd7b56792f2b85a0e911fc401c33875c01a8476c9333f6e1315f4f08f", "image_sha": "f4617abfa9427b3d12a1cdd4b60fb4610c5a1cbae052c001ade793457190cec8", "raw_unchanged": true, "fonts": {"NotoSansCJK-Regular.ttc": "b76b0433203017ca80401b2ee0dd69350349871c4b19d504c34dbdd80541690a"}, "weights": {"chi_tra": "529c5b5797d64b126065cd55f2bb4c7fd7b15790798091b1ff259941a829330b"}, "actual": "無常 苦 無我\n色即是空 空即是色", "stderr": "", "rc": 0, "seconds": 0.165, "metrics": {"cp": [0, 17], "grapheme": [0, 17], "whitespace_token": [0, 5]}}, {"id": "TIB", "lang": "bod", "psm": 6, "gt": "བདེ་སྡུག་མི་རྟག་པ།\nཆོས་དང་ཤེས་རབ།", "gt_sha": "b18518b69f24d6727a5ccb02017519a578b83c592faaeee36677e990c84ae75d", "image_sha": "15594500ffe42023f0867a85f3c372cd5e12d15cb6e73fe8d56b960dab2de517", "raw_unchanged": true, "fonts": {"NotoSerifTibetan-Regular.ttf": "5893c1e0aefb250bcbeff5c0f8ee4bb27cd3dc19b47d14954b154b094e10ee63"}, "weights": {"bod": "1aab1db8dae337dfc8fa0f94a1c137c47e4c7857c3e6b30093ec726cef912a0b"}, "actual": "བདེ་ཕྲུག་མི་རྟག་པ།\nཆོས་དང་ཤེས་རབ།", "stderr": "", "rc": 0, "seconds": 0.064, "metrics": {"cp": [2, 33], "grapheme": [1, 26], "whitespace_token": [1, 2]}}, {"id": "COL", "lang": "vie", "psm": 3, "gt": "Trái một.\nKhông có khổ.\nTrái ba.\nTrái bốn.\nPhải một.\nPhải hai.\nPhải ba.\nPhải bốn.\nChú thích: không bỏ dấu.", "gt_sha": "70aa47223e0a03462211ecc1d2a0b301e83836c1ca39531e2c717a5d294abbb9", "image_sha": "1d0674ceccf3846047332be24873434acbc1dca49a0351e640e7174d4960ecc1", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"vie": "79df64caf7bcfb2a27df5042ecb6121e196eada34da774956995747636d5bfa1"}, "actual": "Trái một. Phải một.\n\nKhông có khổ. Phải hai.\nTrái ba. Phải ba.\nTrái bốn. Phải bốn.\n\nChú thích: không bỏ dấu.", "stderr": "", "rc": 0, "seconds": 0.239, "metrics": {"cp": [34, 106], "grapheme": [34, 106], "whitespace_token": [10, 22]}}, {"id": "COL", "lang": "vie", "psm": 6, "gt": "Trái một.\nKhông có khổ.\nTrái ba.\nTrái bốn.\nPhải một.\nPhải hai.\nPhải ba.\nPhải bốn.\nChú thích: không bỏ dấu.", "gt_sha": "70aa47223e0a03462211ecc1d2a0b301e83836c1ca39531e2c717a5d294abbb9", "image_sha": "1d0674ceccf3846047332be24873434acbc1dca49a0351e640e7174d4960ecc1", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"vie": "79df64caf7bcfb2a27df5042ecb6121e196eada34da774956995747636d5bfa1"}, "actual": "Trái một. Phải một.\nKhông có khổ. Phải hai.\nTrái ba. Phải ba.\nTrái bốn. Phải bốn.\nChú thích: không bỏ dấu.", "stderr": "", "rc": 0, "seconds": 0.187, "metrics": {"cp": [34, 106], "grapheme": [34, 106], "whitespace_token": [10, 22]}}, {"id": "COL_crop_0", "lang": "vie", "psm": 6, "gt": "Trái một.\nKhông có khổ.\nTrái ba.\nTrái bốn.", "gt_sha": "386fd44577d330e3c766009edfbed9d60c345e5dcb19e8756c57fd569ae7a18d", "image_sha": "c7f062aeb63e3be9842a8636c572a6bc867c550945aa481791c0258f57f9a02e", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"vie": "79df64caf7bcfb2a27df5042ecb6121e196eada34da774956995747636d5bfa1"}, "actual": "Trái một.\nKhông có khổ.\nTrái ba.\n\nTrái bốn.", "stderr": "", "rc": 0, "seconds": 0.113, "metrics": {"cp": [0, 42], "grapheme": [0, 42], "whitespace_token": [0, 9]}}, {"id": "COL_crop_1", "lang": "vie", "psm": 6, "gt": "Phải một.\nPhải hai.\nPhải ba.\nPhải bốn.", "gt_sha": "4c3d2afd3f444e507f8506d4d113b621ba9d755c9f0455f2919eebf8b7d6e8b3", "image_sha": "0c409cb016bce2549c4dcc95b71ffe9fc39304c19f4f56befc97630d4bdc840a", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"vie": "79df64caf7bcfb2a27df5042ecb6121e196eada34da774956995747636d5bfa1"}, "actual": "Phải một.\nPhải hai.\nPhải ba.\nPhải bốn.", "stderr": "", "rc": 0, "seconds": 0.118, "metrics": {"cp": [0, 38], "grapheme": [0, 38], "whitespace_token": [0, 8]}}, {"id": "COL_crop_2", "lang": "vie", "psm": 6, "gt": "Chú thích: không bỏ dấu.", "gt_sha": "4932d4232541e7899d01a389d17575d188c5bb1d79812638669e3fc327844943", "image_sha": "0e31f3160f61f77879b0f529d754b5c5900a893f3525e704e070ac734f8b2878", "raw_unchanged": true, "fonts": {"NotoSerif-Regular.ttf": "9d7583b7dc9e812afd32a14280c5cac3160012efe50c8d08938f4fea266ff67f"}, "weights": {"vie": "79df64caf7bcfb2a27df5042ecb6121e196eada34da774956995747636d5bfa1"}, "actual": "Chú thích: không bỏ dấu.", "stderr": "", "rc": 0, "seconds": 0.112, "metrics": {"cp": [0, 24], "grapheme": [0, 24], "whitespace_token": [0, 5]}}]
PROJECTION {"page_sha": "0d378cebcf4a2e56e8391099e920f5dc1ee79f9b48102b2bd758a4620474374b", "raw_A": "55b24426c842a5924faba66a8e09720b135b745d0b4e7db7af107a846ecf62c4", "raw_B": "520e5f49cde92aab5ca52e7e71347c3d1cc2e4be551994d2a4d41eb54d187a1c", "canonical": "vô thường vô thường\nvô thường\nKhông", "offsets": [0, 10, 20], "regions": [{"id": "left", "start": 0, "end": 19, "role": "paragraph", "polygon": [[70, 110], [610, 110], [610, 185], [70, 185]], "confidence": null, "precision": "REGION", "review": "UNVERIFIED", "alternatives": [{"index": 1, "text": "wrong alternative", "conf": "0.99"}, {"index": 0, "text": "vô thường vô thường", "conf": null}]}, {"id": "right", "start": 20, "end": 29, "role": "paragraph", "polygon": [[650, 110], [1000, 110], [1000, 185], [650, 185]], "confidence": null, "precision": "REGION", "review": "UNVERIFIED", "alternatives": [{"index": 1, "text": "wrong alternative", "conf": "0.99"}, {"index": 0, "text": "vô thường", "conf": null}]}, {"id": "note", "start": 30, "end": 35, "role": "footnote", "polygon": [[70, 460], [330, 460], [330, 525], [70, 525]], "confidence": null, "precision": "REGION", "review": "UNVERIFIED", "alternatives": [{"index": 1, "text": "wrong alternative", "conf": "0.99"}, {"index": 0, "text": "Không", "conf": null}]}], "revision_A": "090791a87971e4dfccd978ac6313295864aeaf9da1314c7f5eb43727f1a9f357", "revision_B": "4057d3b0923f1027b58bfd5c85f497c28fd21634a67a47364e3c964b00feb0c2", "cross_edition_rejected": true}
NEGATIVE missing_region ValueError order coverage 8083a3468042c53974cc7e6ca00fb4bad28861e263e5859dd8c4be0601e6da1b
NEGATIVE duplicate_ref ValueError order coverage d7f0b0937f2d8a7e386d766a05a25c908ce8278827f91545f9f40a1cab8d09c5
NEGATIVE wrong_raw ValueError raw mismatch bece580b31dc15cb5c5eb9fa7f593a148afda2fb778b4f470b7c305daa00ef25
NEGATIVE traversal ValueError raw mismatch bb02b09efe2c8d946c5ac96331af5d0de22eed65e9063b9068f6d2e9e6713451
NEGATIVE bad_namespace ValueError namespace a55b41bb77b8519fbe920fd17c75e837eae94c7823c61884ae6b30989dbadc05
NEGATIVE XXE ValueError unsafe XML a6154b09d3f94c25ae60d4b6399a369ff2d64a0cbbd8fe4e4736f1bf87260a2d
NEGATIVE malformed XMLSyntaxError Premature end of data in tag Page line 1, line 1, column 1137 (<string>, line 1) 2426ff53de6575be8dcc70c3a320b37d285323b524a7cec418d8ccb8bcc5a4a8
METS 39abf5fdb23cab1459e6b63bc90d7619780ec88bc1f9fc19a6284635e49d40ae {'p1': 'CANDIDATE', 'p2': 'PARTIAL', 'p3': 'PARTIAL'}
REVISION 731dc9a97b8496f75f3bd381951d28c995f88d50f53c63a8a2f5200c698560a1 old canonical retained 090791a87971e4dfccd978ac6313295864aeaf9da1314c7f5eb43727f1a9f357 RAW UNCHANGED
```

### 13.7 Chốt giới hạn và bàn giao R2

- Nâng độ chi tiết về schema, evaluator, module ownership và baseline; cập nhật master JSON, giữ 13 phần/C01–C15/TC01–TC16; §9.5 bổ sung trạng thái từng TC, không thay actual upstream=null thành PASS.
- Không chạy OCR-D vì thiếu package và DNS GitHub không hoạt động (connector đọc code được); raw web XSD bị DisabledError. Không chạy Docling/MinerU/Marker/dinglehopper; không có corpus lịch sử được phép, không audit tất cả code/tests/dependencies/NOTICE, không đo TCO thực. Chưa xác minh model license, tag/wheel pin, schema compile hoặc độc lập visual quote verification.
- Cần một POC thực upstream với wheelhouse offline đã lock và tài liệu được phép: TC02/09/12 trước, TC04/15 sau; so direct OCR + cùng model + layout trên gold holdout; chỉ tiếp tục nếu có nhu cầu scan khó thực. Không cần triển khai thêm framework để có báo cáo lựa chọn kiến trúc; không tuyên bố đã hoàn tất nghiệm thu production.
- Quyết định không đổi: E mặc định V1, C là thử thành phần hẹp theo nhu cầu, B nếu đo được lợi ích rõ. R2 là cập nhật báo cáo P60, không tạo nghiên cứu mã mới hoặc sửa repository.
