# REPORT 59-R2 — Thẩm định độc lập Haystack và tài sản tái sử dụng cho BodhiAtlas

**Mã:** P59 · **Revision:** R2 (thay thế R1, giữ nguyên mã nghiên cứu) · **Ngày:** 25/11/2026 (Asia/Ho_Chi_Minh) · **Loại:** framework Python điều phối pipeline retrieval/RAG/agent · **Trạng thái:** hoàn thành khảo sát mã có ghim phiên bản và thực nghiệm cô lập; chưa nghiệm thu upstream. R2 bổ sung audit Agent/Tools, integrations, BCR host, phương án ghép và POC bảo toàn ranh giới. Không sửa repository, không sử dụng corpus thật, không gọi mô hình.

## 1. Executive Decision

**Khuyến nghị chính: `DEFER` — không đưa Haystack vào dependency của V1 Core; giữ một cổng adapter tùy chọn cho V2 nếu xuất hiện workflow RAG thực sự cần graph.** Chọn **A — direct Python functions + explicit ports**, với SQLite/file store và một authority chứng cứ. E (học pattern/test mà không thêm runtime) là biện pháp hỗ trợ, không phải kiến trúc thứ hai. Độ tin cậy **HIGH** về khoảng cách hợp đồng của BM25/Document/AnswerBuilder tại snapshot phát hành; **MEDIUM** về quyết định đầu tư; **LOW** về chênh lệch TCO chưa đo.

Điểm cần cập nhật so với đề bài: Haystack **2.x không còn là major hiện hành**. Release ổn định tại thời điểm kiểm là **3.5.0**; 2.31.1 là bản nhánh 2.x được xác minh, không đồng nhất API với 3.5.0. Thẩm định sâu theo release 3.5.0 thay vì nightly hay HEAD; chưa chạy kiểm tương thích 2.x. Framework không bắt buộc dùng cloud, LLM hay vector DB trong mọi pipeline; nhưng một graph không tự làm tăng fidelity của chứng cứ.

Ba blocker đối với việc đưa vào V1:

1. BM25 trả tài liệu giới hạn theo rank, không phải mọi vị trí literal; splitter có offset của text đã đưa vào, không có source map học thuật độc lập. Thêm orchestration không sửa khoảng trống EXACT của BCR.
2. `Document.id` và citation trong `GeneratedAnswer` không phải identity theo ấn bản/file/revision, không có quyền tự cấp G2 VERIFIED. Bắt buộc có authority và verifier do BodhiAtlas quản lý.
3. Cài đặt, egress-denial, roundtrip, chi phí graph so với ba direct calls chưa đo được. Dependency và cấu hình bổ sung có chi phí thật về bảo trì; chưa có workflow V1 chứng minh lợi ích bù chi phí.

Ba POC quyết định: (i) TC02/03/12 so direct vs graph không LLM, cùng BCR thật và nguồn độc lập; (ii) TC04/05/10 bảo toàn identity, toàn occurrence và chống fake citation; (iii) TC11/13/15 đo một workflow có branch/async thực, deserialize an toàn, gỡ framework. **Dừng trước khi xây vector store hoặc agent.** Nếu không có workflow thực cần graph, không triển khai POC dài hơn. Demo pipeline đơn giản không đồng nghĩa đủ tiêu chuẩn, càng không phải phê duyệt production.

### 1.1. Quyết định R2 — chọn tài sản, không chọn cả framework

**V1: DEFER runtime Haystack; tận dụng ngay về mặt thiết kế:** typed contracts, tách mode, kết quả lỗi có cấu trúc, oracle đánh giá theo identity. **V2: TRIAL ONLY** cho Haystack như bộ điều phối in-process có thể tháo bỏ, không dùng làm kho dữ liệu. Đây là quyết định cấp *thành phần*, không phải quyết định chọn stack V2 hay phê duyệt cài đặt. Nếu V2 chỉ gọi vài công cụ cố định, direct Python vẫn thắng về độ đơn giản mặc định. Nếu phát sinh quy trình lặp nghiên cứu/đối chứng với model, nhiều nhánh và nhiều công cụ, thử Haystack Agent sau khi chứng minh graph đơn giản trước.

Ba cơ hội có giá trị nhất được xếp theo thứ tự đầu tư (không phải ranking benchmark): (1) **BCR LocalHost và verifier hiện có** kết hợp contract host-owned; tận dụng code BCR thay vì reimplement trong Haystack; (2) **DocumentNDCG/Recall, RRF và context-window pattern** để đánh giá/xếp hạng ứng viên, có thể gọi riêng hoặc tự triển khai đơn giản, tuyệt đối ngoài EXACT; (3) **Agent, Tool, Pipeline, MCP** để kết nối nghiên cứu nhiều nguồn trong V2; không cần mỗi nguồn một agent. Docling direct được ưu tiên kiểm cho ingestion, không kéo Haystack chỉ vì đã có wrapper. FastEmbed/HanLP/Ollama chỉ là ứng viên khi có yêu cầu cụ thể; không kéo mô hình/vector DB vào V1.

R2 phát hiện thêm ba rủi ro có bằng chứng mã: (a) tham số LLM thắng tham số lấy từ Agent State; (b) MultiRetriever/RRF gộp theo `Document.id`, có thể mất identity nếu adapter cấp ID sai; (c) wrapper Docling không serialize lại converter/chunker tùy chỉnh và default HybridChunker có thể tải tokenizer. Các điều này củng cố lựa chọn một authority, không cấm sử dụng các thành phần trong đúng vai trò. Độ tin cậy HIGH cho cơ chế code cụ thể, MEDIUM cho lựa chọn kiến trúc; chưa có bằng chứng về chi phí sản xuất, chất lượng đa ngôn ngữ hoặc hiệu năng thực tế.

## 2. Sources & Evidence Ledger

### 2.1. Snapshot và phạm vi truy cập

| Đối tượng | Bản ghim / bằng chứng | Trạng thái |
|---|---|---|
| Haystack canonical | [deepset-ai/haystack](https://github.com/deepset-ai/haystack), owner deepset-ai, default `main`; [HEAD 354906c7ceae6f49ce2c26c83ee37abbef64f567](https://github.com/deepset-ai/haystack/commit/354906c7ceae6f49ce2c26c83ee37abbef64f567), 25/11/2026 12:52:41 UTC | Metadata API đọc được; không dùng HEAD làm code release |
| Stable | [v3.5.0](https://github.com/deepset-ai/haystack/releases/tag/v3.5.0), commit [831b8cfa95a250cea2134091986f734666cce47d](https://github.com/deepset-ai/haystack/commit/831b8cfa95a250cea2134091986f734666cce47d), 10/11/2026 12:33:57 UTC; release 12:34:55 UTC | Snapshot audit chính; [haystack-ai 3.5.0 trên PyPI](https://pypi.org/project/haystack-ai/3.5.0/) tồn tại; chưa cài |
| Nhánh 2.x | [v2.31.1](https://github.com/deepset-ai/haystack/commit/4d9b2019f5e6bb5a7d6676df60178d41c2b23110), 03/11/2026 09:26:56 UTC; [PyPI](https://pypi.org/project/haystack-ai/2.31.1/) | Xác minh tồn tại, không audit code toàn bộ 2.x; không khẳng định support SLA |
| BodhiAtlas | [main c5dfe50613dfd492407bf1db1061c1cfc9d30e8e](https://github.com/quoctran-2608/bodhi-atlas/commit/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e), 25/11/2026 11:26:47 UTC | 5 tài liệu bắt buộc và 8 báo cáo đối chứng được truy xuất theo SHA; đọc các phần liên quan quyết định, không tuyên bố rà toàn bộ từng dòng |
| BCR baseline đối chứng | [dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/commit/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410) | Đọc lại retrieval và phần đầu verifier ở baseline cũ; HEAD hiện hành BCR xác nhận lại ở R2 vẫn cùng SHA, không đổi source pins |
| Runtime | Sandbox Python; Git CLI không phân giải được github.com; module `haystack` không có | `ACCESS BLOCKED / NOT TESTED` cho clone/cài/chạy upstream; GitHub connector read-only vẫn đọc được code; không suy từ việc DNS lỗi rằng package không chạy offline |

[Hướng dẫn migration chính thức](https://docs.haystack.deepset.ai/docs/migration): `farm-haystack` là package legacy 1.x đã hết vòng đời, `haystack-ai` là package của 2.x/3.x; migration 3.x có thay đổi và tách một số thành phần. [haystack-core-integrations](https://github.com/deepset-ai/haystack-core-integrations) cung cấp các package tích hợp riêng; không tính là native core. [Haystack Enterprise Platform](https://docs.cloud.deepset.ai/docs/getting-started) là dịch vụ/sản phẩm triển khai khác, không cần mua để sử dụng core OSS. [Hayhooks](https://github.com/deepset-ai/hayhooks) là dự án triển khai HTTP/MCP riêng. R2 đã mở một số integration source (E34–E40); chưa kiểm license từng package/model, chưa đưa chúng vào baseline.

**Quy ước:** `[DOC]` tài liệu/metadata, `[CODE]` file mã hoặc test đã mở, `[TESTED]` chạy upstream, `[TESTED-ISOLATED]` thử nghiệm thuật toán tự tạo, `[ISSUE]` sự cố bên ngoài chưa tái hiện, `[PLAN]` chưa chạy, `[INFERRED]` suy luận từ bằng chứng, `[UNKNOWN]` chưa kiểm, `[CONFLICT]` khác biệt phiên bản hoặc giả định. Code tồn tại không đồng nghĩa pass. Các liên kết code dưới đây dùng commit release, không dùng nhánh động.

### 2.2. Ledger

| ID | Loại | Quan sát và nguồn | Giới hạn / tác động |
|---|---|---|---|
| E01 | DOC | [PRD V1.4 L105–123, L213–272](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/PRD.md#L105-L123); [V1 Core L96–158](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/V1_CORE_FOUNDATION.md#L96-L158) | EXACT và evidence là yêu cầu host, không phải feature Haystack |
| E02 | DOC | [Sổ tay L154–190](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/ACADEMIC_RISKS_AND_VERIFICATION.md#L154-L190) | G1–G6, T01–T16, human G3 |
| E03 | CODE | [Component decorator, sockets](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/component/component.py#L183-L239), [base graph/add/connect](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/pipeline/base.py#L93-L115), [connect](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/pipeline/base.py#L600-L770) | Có graph và hợp đồng socket; type validation không phải kiểm quyền/identity |
| E04 | CODE | [Pipeline.run và _run_component](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/pipeline/pipeline.py#L127-L200), [async/cancel](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/pipeline/pipeline.py#L543-L667), [run_async](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/pipeline/pipeline.py#L1099-L1145) | Sync/async cùng class ở 3.5.0; exception được wrap, có cancel/drain; chưa chạy |
| E05 | CODE | [base.to_dict/from_dict](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/pipeline/base.py#L152-L291), [serialization](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/serialization.py#L330-L384), [allowlist](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/serialization_security.py#L8-L61) | Config không tự ghim dependency/data; safe mode có kiểm module, `unsafe=True` phá rào |
| E06 | CODE | [Document._create_id/to_dict](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/dataclasses/document.py#L132-L185) | SHA-256 của biểu diễn nội dung/meta/embedding/blob, không phải hash raw source; custom ID cần host |
| E07 | CODE | [DocumentSplitter.run](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/preprocessors/document_splitter.py#L192-L231), [copy metadata](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/preprocessors/document_splitter.py#L260-L282), [split offsets](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/preprocessors/document_splitter.py#L445-L457) | source_id/page_number/split_idx_start, không bbox/CFI/TEI mapping độc lập |
| E08 | CODE | [DocumentCleaner options](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/preprocessors/document_cleaner.py#L43-L82), [clean/ID/ASCII](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/preprocessors/document_cleaner.py#L139-L198) | Có thể đổi hoặc giữ ID dù text đã đổi, xóa chữ Hán/Tạng khi ASCII-only |
| E09 | CODE | [Store shared/default tokenizer](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/document_stores/in_memory/document_store.py#L88-L132), [NFC/lowercase](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/document_stores/in_memory/document_store.py#L219-L233) | CJK per-char theo docstring; không đồng nhất exact raw; shared process-global mặc định |
| E10 | CODE | [Store config/save/load](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/document_stores/in_memory/document_store.py#L399-L460), [write/delete](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/document_stores/in_memory/document_store.py#L496-L542), [Writer](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/writers/document_writer.py#L31-L102) | JSON dump riêng, config không chứa records; overwrite/skip/fail không phải revision ledger/ACL |
| E11 | CODE | [InMemoryBM25Retriever.run](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/retrievers/in_memory/bm25_retriever.py#L121-L155) → [store BM25](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/document_stores/in_memory/document_store.py#L772-L814) | top_k tài liệu (slice), không offsets/total occurrence; CODE GAP nếu dùng thay EXACT |
| E12 | CODE | [DocumentJoiner](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/joiners/document_joiner.py#L91-L190) | fusion/join theo ID và top_k, không phải merge evidence spans; trùng ID cần kiểm |
| E13 | CODE | [ConditionalRouter](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/routers/conditional_router.py#L267-L279), [unsafe deserialization](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/routers/conditional_router.py#L369-L383) | Có branch và sandbox template; không nhận template người dùng làm code tin cậy |
| E14 | CODE | [AnswerBuilder](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/builders/answer_builder.py#L195-L245), [GeneratedAnswer](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/dataclasses/answer.py#L117-L160) | Ánh xạ index tham chiếu, bounds check; không độc lập mở file/so câu |
| E15 | CODE | [DocumentRecall](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/evaluators/document_recall.py#L124-L183) | Tập ground truth và retrieved Documents; không đánh đồng qrels với all-occurrence |
| E16 | CODE | [pyproject](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/pyproject.toml#L6-L65), [LICENSE](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/LICENSE) | Python >=3.11; Apache-2.0; chưa có lock transitive/SBOM đã đo |
| E17 | CODE | [Telemetry](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/telemetry/_telemetry.py#L47-L60), [default enabled](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/telemetry/_telemetry.py#L192-L194), [tracing content](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/tracing/tracer.py#L115-L118) | Phải opt-out trước import và deny egress; không khẳng định default offline |
| E18 | CODE | [PyPDF converter](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/converters/pypdf.py#L214-L265) | extract_text từ PdfReader; không chứng minh OCR, reading order hay source bbox |
| E19 | CODE | [OpenAI chat generator](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/generators/chat/openai.py#L128-L149), [run/run_async](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/generators/chat/openai.py#L346-L426) | Credential/provider boundary; không gọi đường này trong V1 |
| E20 | CODE | [test_document](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/dataclasses/test_document.py#L155-L163), [test collision](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/dataclasses/test_document.py#L383-L391), [test_splitter](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/components/preprocessors/test_document_splitter.py#L61-L142), [test_answer_builder](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/components/builders/test_answer_builder.py#L181-L215), [test_async](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/core/pipeline/test_async_pipeline.py#L57-L112) | Đã mở code/test và đọc các đoạn liên quan; không chạy các test |
| E21 | CODE | [BCR retrieval L268–392](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/retrieval.py#L268-L392), [verifier contract L1–36](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/verification.py#L1-L36), [safe normalize](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/verification.py#L87-L114) | Baseline vẫn giới hạn FTS candidates; trusted source_reader ngoài candidate; Git blob SHA-1 khác raw SHA-256 của BodhiAtlas |
| E22 | TESTED-ISOLATED | Appendix: 24 đoạn tự tạo, oracle 25 literal hits, mô phỏng top-K, kiểm byte/hash giả | Không có Haystack/BCR/SQLite search engine thật trong phép thử |
| E23 | CONFLICT | Giả định 2.x trong prompt so [release v3.5.0](https://github.com/deepset-ai/haystack/releases/tag/v3.5.0), [migration](https://docs.haystack.deepset.ai/docs/migration) | Không reuse API 2.x thiếu kiểm; `core/pipeline/async_pipeline.py` trả 404 ở 3.5.0, execution trong pipeline.py |
| E24 | UNKNOWN | Cài wheel, dependencies/weights lock, notice riêng, integration commercial terms, BCR thực tế, upstream benchmarks | Không suy PASS hoặc đưa TCO số; cần POC có quyền và môi trường chuẩn |

### 2.3. Bổ sung snapshot và Evidence Ledger R2

- [Integrations](https://github.com/deepset-ai/haystack-core-integrations/commit/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5) main ngày 25/11/2026 11:57:47 UTC, Apache-2.0 theo GitHub metadata, tree `bf4cfd8db8f904a25c2eb471421a971b864d2329`, không truncated. Đây là **snapshot source HEAD của monorepo** chứ không phải version cài được đồng nhất của từng package. Các integration có release/version độc lập; chưa kiểm từng wheel, NOTICE, SPDX dependency hay compatibility thực tế.
- [Hayhooks](https://github.com/deepset-ai/hayhooks/commit/82f71a6eb31236da47ed6cc4704f3bb41ff65598) main ngày 13/11/2026 14:47:51 UTC, Apache-2.0 theo metadata; đọc README và deploy route, không audit toàn bộ security. Đây là ứng viên transport riêng, không native Haystack.
- BCR main hiện tại được xác nhận **vẫn đúng** SHA `dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410` ngày 05/11/2026 03:03:31 UTC; không còn UNKNOWN về HEAD tại thời điểm R2. Không đổi source pins. BCR license/rights từng corpus vẫn cần kiểm riêng.
- BodhiAtlas main hiện tại [24e6edd34d4df48c5efcc2dc5b6bf8bc0e7ecb9a](https://github.com/quoctran-2608/bodhi-atlas/commit/24e6edd34d4df48c5efcc2dc5b6bf8bc0e7ecb9a) ngày 25/11/2026 13:56:38 UTC. Đã kiểm blob SHA của ba tài liệu bắt buộc: PRD `58d967c642d625180c436e1a6e6a75fa2e7070e3`, Core `fb4392d63a0eb5067cadb2a4ca6571791b8411f1`, Academic Risks `cdb642633f3dc3f7f83cb0e49a96abfebc9f132e`; **đều không đổi so với snapshot R1**. Không re-audit các báo cáo đối chứng ở HEAD mới; R1 giữ permalink cũ có hiệu lực.

| ID | Loại | Mã nguồn / bằng chứng | Hệ quả đối với BodhiAtlas |
|---|---|---|---|
| E25 | CODE | [Agent constructor, hooks, budgets](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/agents/agent.py#L424-L499), [sync/async exit reasons](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/agents/agent.py#L882-L1068) | Có vòng lặp generator + tool, `max_agent_steps=100`, concurrency=4, lỗi tool mặc định chuyển message cho LLM, cần giới hạn host độc lập. |
| E26 | CODE | [state args precedence](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/agents/tool_calling.py#L294-L355), [test precedence](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/components/agents/test_tool_calling.py#L193-L203) | LLM arguments có ưu tiên hơn giá trị mapping State; không dùng State như ACL; test nguồn đã đọc, chưa chạy. |
| E27 | CODE | [from_function](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/tools/from_function.py#L132-L210), [ComponentTool](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/tools/component_tool.py#L93-L183), [PipelineTool](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/tools/pipeline_tool.py#L96-L194), [Tool.invoke](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/tools/tool.py#L270-L309) | Schema/tool wrappers giảm glue khi V2 nhiều tools; schema không authorization; lỗi có thể chứa kwargs. |
| E28 | CODE | [Agent State](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/agents/state/state.py#L89-L130), [merge output](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/agents/tool_calling.py#L63-L160), [hook tests](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/components/agents/test_agent_hooks.py#L383-L479) | State mutable và có thể chuyển output vào message/model; không ledger chứng cứ. |
| E29 | CODE | [MultiRetriever merge](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/retrievers/multi_retriever.py#L80-L191), [dedup/RRF by ID](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/utils/misc.py#L156-L207) | Candidate federation; cùng ID collapse, top_k cắt; không dùng để đếm occurrence. |
| E30 | CODE | [SentenceWindowRetriever](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/retrievers/sentence_window_retriever.py#L181-L332) | Có context dựa source fields + split_id, batch filter; không độc lập mở raw; nên dùng host context. |
| E31 | CODE | [DocumentNDCG](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/evaluators/document_ndcg.py#L38-L133), [FaithfulnessEvaluator](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/evaluators/faithfulness.py#L91-L176) | nDCG mặc định comparison_field=content; phải đổi thành ID học thuật; faithfulness dùng model, không G2/G3. |
| E32 | CODE | [BCR LocalHost.scope/source_reader](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/local_host.py#L87-L117), [pointer/gate/verify_record](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/local_host.py#L118-L175), [retrieve/quick](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/local_host.py#L187-L209) | BCR có facade host, kiểm source thật và giới hạn quick; tái dùng gần nguyên trạng qua adapter; mutable metrics/recipes cần isolation. |
| E33 | CODE | [BCR independent gate](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/verification.py#L223-L374), [resolver dispatch](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/source_resolvers.py#L257-L273), [XML forbidden handlers](https://github.com/quoctran-2608/BuddhismDocuments-for-AI/blob/dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410/tools/corpus_research/source_resolvers.py#L141-L174) | Không trust candidate; chỉ resolver hỗ trợ, source identity Git khác file SHA-256, không nhận mọi PDF/EPUB. |
| E34 | CODE | [Docling meta](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/docling/src/haystack_integrations/components/converters/docling/converter.py#L83-L101), [warm_up/serde](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/docling/src/haystack_integrations/components/converters/docling/converter.py#L152-L212), [export](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/docling/src/haystack_integrations/components/converters/docling/converter.py#L256-L298) | Có `dl_meta`, page tối thiểu; contextualize khác chunk text, cumulative offsets không canonical, custom config bị bỏ khi roundtrip. |
| E35 | CODE | [MCPToolSet ctor/discover/invoke](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/mcp/src/haystack_integrations/tools/mcp/mcp_toolset.py#L209-L376), [MCPTool client](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/mcp/src/haystack_integrations/tools/mcp/mcp_tool.py#L130-L160) | stdio/HTTP, timeout; chỉ chọn tools allowlist; transport không phải trust. |
| E36 | CODE | [FastEmbed options](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/fastembed/src/haystack_integrations/components/rankers/fastembed/ranker.py#L55-L90), [run](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/fastembed/src/haystack_integrations/components/rankers/fastembed/ranker.py#L145-L234), [ST ranker](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/sentence_transformers/src/haystack_integrations/components/rankers/sentence_transformers/sentence_transformers_similarity.py#L224-L307) | Local candidate rerank, no additional authoritative DB; pin weights/license, chưa đo đa ngữ. |
| E37 | CODE | [Ollama client](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/ollama/src/haystack_integrations/components/generators/ollama/chat/chat_generator.py#L270-L352), [usage mapping](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/ollama/src/haystack_integrations/components/generators/ollama/chat/chat_generator.py#L163-L177) | Localhost default, vẫn HTTP service; đo model/tool compatibility, tokens, egress. |
| E38 | CODE | [HanLP warmup](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/hanlp/src/haystack_integrations/components/preprocessors/hanlp/chinese_document_splitter.py#L157-L183), [split/overlap](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/hanlp/src/haystack_integrations/components/preprocessors/hanlp/chinese_document_splitter.py#L416-L472) | Chinese segmentation dùng pretrained models, không cần cho literal; classical corpus cần gold riêng. |
| E39 | DOC/CODE | [Hayhooks README](https://github.com/deepset-ai/hayhooks/blob/82f71a6eb31236da47ed6cc4704f3bb41ff65598/README.md#L9-L33), [deploy endpoints](https://github.com/deepset-ai/hayhooks/blob/82f71a6eb31236da47ed6cc4704f3bb41ff65598/src/hayhooks/server/routers/deploy.py#L101-L173) | Deploy pipeline qua API/MCP; thêm control plane, không phơi deployment endpoint; auth chưa audit. |
| E40 | CODE | [docling package](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/docling/pyproject.toml#L34-L39), [mcp package](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/mcp/pyproject.toml#L31-L35), [fastembed package](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/fastembed/pyproject.toml#L25-L25), [ollama package](https://github.com/deepset-ai/haystack-core-integrations/blob/4c0aa2ba2796d1c337412f6551b534c8c1efb0c5/integrations/ollama/pyproject.toml#L30-L34) | Lower bounds không là lock; không tuyên bố các release tương thích 3.5.0. |
| E41 | TESTED-ISOLATED | §9.5 và Appendix 13.5: direct Python/async fanout, 5 negatives, state precedence và dedup models | Fixture do tác giả tạo; không import haystack/BCR, không kiểm source PDF; không cấp PASS production. |

## 3. Architecture & Data Flow

### 3.1. Luồng có code tại release

```text
Python @component: run(...) -> dict, khai báo socket output
    -> Pipeline.add_component / connect -> MultiDiGraph
    -> validate/prepare inputs -> schedule node -> component.run / run_async
    -> optional branch / loop / join -> output dict hoặc exception

Ingest tùy chọn: converter -> cleaner -> splitter -> DocumentWriter -> DocumentStore
Query tùy chọn: query -> BM25Retriever / embedder -> store -> rank/join
                            -> prompt/generator -> AnswerBuilder -> GeneratedAnswer
Config: to_dict -> serialized components + connections -> from_dict + module allowlist
```

Graph là cấu trúc trong process Python, không phải mặc định một server. `Pipeline` ở release 3.5.0 chứa cả sync và async; không dùng path AsyncPipeline cũ làm bằng chứng. Components tùy biến không cần bắt buộc trả `Document`; có thể truyền list/dict hoặc DTO typed cho nghiệp vụ host. Graph hỗ trợ workflow nhiều nhánh/vòng, không phải DAG thuần. Socket kiểm kết nối không kiểm được bất biến SHA, phạm vi tìm hay quyền. Config serialization mô tả graph và tham số, còn bản cài, dữ liệu, nguồn, model, secrets và loader policy là dependency riêng (E03–E05).

### 3.2. Kiến trúc ưu tiên A, đường mở rộng C tùy chọn

```text
BodhiAtlas modular monolith (authority duy nhất)
  raw object immutable SHA-256 + catalog Work/Expression/Edition/Witness/File
  -> extraction revision + source map + coverage/rights
  -> exact scanner (all offsets) | BCR/FTS ranked | normalized/fuzzy/lexicon
  -> candidate locator -> trusted reader -> G2 citation status
  -> evidence card/export -> human G3/G5/G6
                               |
                  V2 adapter read-only (optional)
                               v
      [Haystack graph: candidate port -> rerank/router -> model -> draft]
                               |
             untrusted candidate / interpretation / proposed references
                               v
                         host G2/G3 review
```

| Tài sản | Owner | Nguyên tắc |
|---|---|---|
| Raw file, identity, permissions, revision manifest | BodhiAtlas | immutable, versioned, rights checked trước khi đọc |
| Canonical text/source map, coverage | BodhiAtlas + adapter extraction | không biến chunk thành canonical, không sửa raw |
| FTS và exact index/scanner | BodhiAtlas/BCR port | rebuildable; SQLite chỉ một authority; corpus pin không đổi |
| Haystack Document/store | V2 adapter nếu cần | dữ liệu dẫn xuất, có thể xóa và tạo lại; không copy DB writable; store tạm `shared=False` |
| Candidate, citation check, claim/publish | Host trusted verifier và người duyệt | Haystack không có quyền cấp VERIFIED/SUPPORTED; giữ history hoặc STALE |

Không thêm service, graph scheduler, agent framework, vector database hay plugin marketplace nếu không có yêu cầu. Nếu dùng B, chạy in-process trên port của chính core, không migrate schema để vừa `Document`.

## 4. Fit–Gap C01–C15

Trạng thái đánh theo vai trò orchestrator và ứng viên B/V2, không phải full scholarly platform; N/A không bị trừ điểm. NATIVE là có mã, chưa phải PASS; effort L/M/H/VH tương đối cho phần tích hợp/khắc phục, không phải nhân-ngày. V1 là Core, V2 là AI research, V3 là workspace/publication mở rộng nếu có.

| ID | Yêu cầu | Trạng thái theo vai trò | Evidence | Phần thiếu / owner | Effort | Cổng | Phép thử / phạm vi |
|---|---|---|---|---|---|---|---|
| C01 | Multi-format ingest | CONFIG / EXTERNAL | E18, integration docs | parser/profile/rights/format coverage host, extras riêng | M | G1 | TC04, T01; V1 |
| C02 | OCR/layout/reading order | EXTERNAL | E18 | OCR/layout source ground truth host/parser | H | G1/G2 | T01; V1 |
| C03 | Canonical text & source map | EXTENSION | E06–08 | raw/revision/native locator/mapping host | H | G1/G2 | TC04/09; V1 |
| C04 | Work/Edition/Witness model | N/A (orchestrator), EXTERNAL | E06 | catalog scholarly host, không dùng Document.id thay | H | G2 | TC04/07; V1 |
| C05 | Exhaustive EXACT | MISSING ở BM25, EXTENSION nếu custom scanner | E11,E21,E22 | host exhaustive scanner, total, cursor, coverage | M/H | G1/G2 | TC05/06; V1 |
| C06 | Normalized multilingual | CONFIG / EXTENSION | E08/09 | transform policy, OpenCC/transliteration theo nhu cầu host | M | G1/G2 | TC06, T03/04; V1 |
| C07 | Fuzzy retrieval | EXTENSION / EXTERNAL | E11/12 | fuzzy algo/qrels host; BM25 không là edit distance | M | G2 | TC06; V1 |
| C08 | Sense-aware lexicon | N/A / EXTERNAL | E01/02 | lexicon sense + evidence host và học giả | H | G5 | T05; V1/V2 |
| C09 | Semantic/RAG | NATIVE orchestration, CONFIG/EXTERNAL model/store | E04/12/14/19 | model rights, provider, qrels, guardrails host | M | G2/G3/G4 | TC14; V2 |
| C10 | Verified citation/reopen | MISSING native scholarly verifier, EXTENSION | E14/21 | trusted reader, revision locator, G2 host | H | G2 | TC03/04/10; V1 |
| C11 | Wiki/notes/claims | N/A / EXTERNAL | E02/14 | claim ledger, human approval, UI host | H | G3/G6 | T08/14/15; V2/V3 |
| C12 | APIs/MCP/export | EXTENSION / EXTERNAL | E03/05; Hayhooks docs | host endpoint/ACL/schema; Hayhooks riêng nếu cần | M | G4/G6 | TC13/15; V2/V3 |
| C13 | Coverage/incremental | EXTENSION | E10 | manifests, partial/error, revision/reindex host | H | G1/G2 | TC08/09; V1 |
| C14 | Auth/privacy/license/backup | EXTERNAL / CONFIG | E05/10/16/17 | host ACL, backup, egress, license inventory | H | G4/G6 | TC07/12/13; V1/V2 |
| C15 | Operability/portability | NATIVE graph config, EXTENSION deploy | E04/05/16 | pins, observability, lock/restore/rollback host | M | G1/G6 | TC01/11/13/15; V1/V2 |

| Gate | Haystack trong vai trò giới hạn | Hệ thống tổng thể |
|---|---|---|
| G1 ingest | N/A cho orchestration thuần; CODE GAP nếu dùng converter/store thay coverage | NOT DEMONSTRATED, manifest/partial bắt buộc |
| G2 citation | CODE GAP nếu AnswerBuilder/metadata được dùng như verifier; N/A nếu chỉ routing | NOT DEMONSTRATED; phải host đọc lại đúng nguồn |
| G3 claim | N/A cho quyền duyệt; RAG chỉ hỗ trợ | NOT DEMONSTRATED; người nghiên cứu duyệt |
| G4 external | NOT DEMONSTRATED cho route external | host kiểm quyền, phiên bản, scope đọc |
| G5 lexicon | N/A | NOT DEMONSTRATED, nghĩa do host/học giả kiểm |
| G6 publish | N/A | NOT DEMONSTRATED, review/rights/consistency |

Không có FAIL thực nghiệm upstream vì không thực thi Haystack. CODE GAP là thiếu hợp đồng trong vai trò dùng thay lõi, không phải lỗi chung của framework.

## 5. Deep Technical Findings

**Execution, lỗi và branching (E03–05, E13).** Pipeline tạo graph `MultiDiGraph`, component có sockets; code sync bọc lỗi thành `PipelineRuntimeError`, async có cancel/drain in-flight tasks trước khi thoát ở đường được xem. Không chứng minh mọi call blocking, I/O side effect hoặc cancellation rollback: thread/provider có thể đã thực hiện việc trước khi task bị hủy. Adapter phải giữ status và exception cause; không catch exception rồi trả `[]`. Branch chỉ làm rõ routing nếu trạng thái/đầu ra minh bạch. Không tự đổi EXACT thành SEMANTIC khi lỗi; không lặp vô hạn. Config cần allowlist, kiểm version, graph digest, route/loop budget, timeout và failure policy. Ở release này, loader có kiểm module, không đúng khi nói mặc định import code tùy ý; unsafe mode/custom filters vẫn phải bị cấm từ input không tin cậy.

**Identity, chunk và cleaner (E06–08).** ID mặc định hash SHA-256 trên text, blob/mime, metadata serialize với sort keys, embeddings; ID không phải SHA-256 raw file. Hai edition giống nội dung và thiếu metadata có thể bị cùng ID; thay meta/embedding khi tạo lại có thể đổi ID. `to_dict(flatten=False)` giữ meta nested; flatten mặc định có logic xử lý field collision, nhưng schema validation và versioned mapping vẫn cần ngoài. Splitter sao chép meta, bổ sung source_id, page_number, split_id, split_idx_start; page dựa form feed và offset dựa input text, không tự là số trang PDF/in hoặc bbox. Cleaner mặc định xóa dòng trống và khoảng trắng dư; ASCII-only làm mất chữ ngoài ASCII; tùy chọn keep_id giữ ID dù text đổi. Nếu clean rồi split mà không map transformation, offset không còn là vị trí canonical. Overlap tạo duplicate span; join theo Document.id không giải được occurrence trùng do overlap. Giải pháp: immutable source key, candidate span canonical tách khỏi ID nội bộ, không để cleaner trên EXACT/G2.

**Document store và ranking (E09–12).** Store in-memory hỗ trợ process-global sharing theo index (default shared=True), chọn instance-local để tránh cache giao nhau; save_to_disk ghi JSON documents, from_dict config không tự chứa documents, load lại write overwrite. Không có bằng chứng snapshot transaction/consistent concurrent backup, quyền xóa hay revision retention đủ chuẩn. Writer có fail/skip/overwrite: trùng ID phải bị phát hiện, không overwrite authority. Retriever gọi BM25 store với filters/top_k, kết quả cắt `[:top_k]`, score không phải xác suất quote đúng. Filters là chọn candidates chứ không thay ACL. Joiner thêm ranking/fusion hữu ích cho V2, không trả total occurrences. Không đếm external store là native; không cần store riêng nếu custom component gọi BCR/SQLite read-only.

**Converter, RAG và evaluation (E14–19).** PyPDF extract_text không chứng minh OCR scan, cột/chú thích hoặc tọa độ. AnswerBuilder lấy reference indices từ reply và document list, bỏ out-of-range (kể cả index âm), thêm metadata; reference hợp lệ vẫn có thể trỏ sai edition hoặc câu tác giả bác bỏ. DocumentRecall so ground truth và retrieved docs, không đọc raw file; dùng qrels đúng mục tiêu ranking, không cấp G2/G3. Generator có provider credential; prompt builder/Agent/tool invocation cần quyền theo host và separate trust boundary. Audit lần này chưa mở sâu Agent, embedder và mọi ranker; không kết luận về chúng vượt ngoài khả năng điều phối công bố, không dùng để quyết định V1. Nếu V2 cần, audit riêng đường provider request, tool policy và injection trước khi bật.

### H01–H12

| H | Kết luận theo bằng chứng | Phản ví dụ / điều kiện đảo |
|---|---|---|
| H01 Offline code-only | Có khả năng thiết kế `[CODE/INFERRED]`, NOT TESTED (E03/17) | Telemetry bật mặc định; TC01/12 network-denied mới xác nhận |
| H02 Reuse BCR gần nguyên | Có port custom `[INFERRED]`, chưa tích hợp | Nếu BCR cần sửa model/schema sâu hoặc verifier phải sống trong graph, B thua A; TC03/15 |
| H03 Metadata giữ identity | Chỉ giữ fields theo các đường cụ thể, không đủ contract (E06–08) | clean/split/rejoin/reindex đổi ID/offset; cần explicit mapping + roundtrip TC04 |
| H04 BM25 không bỏ EXACT | Bác ở mức hợp đồng, E11; mô phỏng E22 | Nhiều records >top_k hoặc nhiều hit/record; chỉ đảo nếu host scanner độc lập, không gọi BM25 là EXACT |
| H05 top_k/filter/duplicate an toàn scope | Không mặc nhiên; E10–12 | cross-edition trùng ID, rights bị thiếu; policy fail-closed TC07 |
| H06 Async/branch giảm coupling | Có graph native; lợi ích chưa đo | 3 bước tuần tự có thể đơn giản hơn direct; branch workload thật TC11/15 |
| H07 Lỗi node không silent fallback | Code wrap/cancel; NOT TESTED | Adapter swallow exception hoặc partial I/O; TC08/11 |
| H08 Serialize reproducible/an toàn | Có config/allowlist; không tự lock version/data | thiếu custom class/unsafe template; TC13 với clean environment |
| H09 AnswerBuilder đủ G2 | Bác contract E14 | [1] đúng index nhưng quote sai; host trusted verifier TC10 |
| H10 Eval đủ scholarly evidence | Bác contract E15 | qrels document recall=1 nhưng thiếu offsets/sai nguồn; gold độc lập |
| H11 Không cần DB/service thứ hai | Thiết kế được bằng custom port; NOT TESTED | Nếu bắt ép dùng store riêng chỉ để pipeline chạy, dừng B; TC03/15 |
| H12 TCO thấp hơn A/D | UNKNOWN | Không số latency, deps transitive, token, chi phí vận hành; đo cùng scope trước đổi lựa chọn |

### 5.1 R2 — Agent và Tools: vòng lặp thực tế, điểm có thể tái sử dụng

**Đường thực thi:** `Agent.run/run_async` khởi tạo State → chọn tools → hooks → chat generator → đọc tool calls → chuẩn bị kwargs từ LLM + State → `Tool.invoke`/async → merge outputs vào State và tool messages → kiểm exit condition → lặp hoặc trả `exit_reason`, `step_count`, `tool_call_counts`. `ComponentTool` và `PipelineTool` suy schema từ socket; `create_tool_from_function` lấy type hints. Nguồn E25–E28. Không đồng nghĩa agent chạy không LLM: graph code-only không cần chat generator, nhưng Agent là một vòng lặp cần generator hỗ trợ tools. Không tái sử dụng vòng lặp cho mọi lần người dùng gõ truy vấn V1.

**Giá trị cụ thể:** V2 có thể dùng một Agent với 4–6 công cụ hẹp để lập kế hoạch, tra nguồn, yêu cầu ngữ cảnh và tìm phản chứng; tránh orchestration nhiều agent cho từng corpus. Cần Agent chỉ khi không thể biết trước thứ tự truy vấn và cần model chọn bước tiếp theo. Nếu danh sách nguồn cố định, `asyncio` hoặc Pipeline tĩnh đủ; nếu một truy vấn và một lookup, direct function đủ. Không cần agent-to-agent protocol, skill marketplace, tự viết agent framework hoặc vector store.

**Rủi ro quan trọng nhất:** `final_args=dict(llm_args)` rồi chỉ chèn giá trị State khi tham số chưa tồn tại (E26). Một model hoặc tool call giả mạo không được quyền chọn `root`, `db_path`, `reader`, `authorized_scope`, `rights`, `source_sha`, `publication_authorized`, `verified`. Không chuyển các giá trị này vào tool schema; bind bằng closure/host request context, kiểm allowlist từng lần kể cả khi schema đã hợp lệ. Không cho model gọi trực tiếp `verify_pointer` với dict tự tạo. Tool có thể đọc/ghi State qua mapping; không coi `evidence` trong State là bằng chứng xác minh. `ToolInvocationError` có thể đưa kwargs vào exception; redact trước trả model hoặc log. Hooks có thể skip tool và sửa message; kiểm tra lại ở tool body, không dùng hook đơn độc làm security boundary.

**Budget/exit:** upstream mặc định 100 bước và 4 tool đồng thời; `raise_on_tool_invocation_failure=False` có thể biến exception thành message. Đề xuất thử ban đầu tối đa 4 vòng model, 8 tool calls tổng, 2 nhánh đồng thời, quota bytes/excerpts/tokens, deadline host và max citation IDs; các con số là cấu hình thử nghiệm, không phải phép đo. `on_exit` hook không chạy khi hết max steps; host kiểm `exit_reason` sau run dù `after_run` đã chạy. Exit `max_agent_steps`, failed branch, model output truncated không phải hoàn thành nghiên cứu; kết quả phải `PARTIAL/ERROR`, không tự xuất bản. Cấm tự ghi notes hoặc publish từ agent; duyệt học thuật ngoài model.

### 5.2 R2 — Federation, context và QA: ứng viên hữu ích ngay cả khi chưa có vector DB

- `MultiRetriever` cho phép nhiều retriever có tên, nối danh sách hoặc RRF, giới hạn per-retriever và overall. RRF dùng `doc.id` làm key (E29); hai edition trùng nội dung mà adapter dùng ID content-only sẽ nhập làm một. Dùng identity `(file_id, extraction_revision, source_span)` với edition/witness do catalog xác nhận; nếu nhiều retriever trả cùng source span thì gộp điểm *discovery* và giữ list retrieval reasons. Không dùng RRF để xác lập quan hệ song hành hoặc độc lập chứng cứ. Giữ scope/coverage từng provider trước fusion, không lấy total returned làm total hits. RRF vài dòng Python có thể rẻ hơn thêm dependency; dùng code Haystack trực tiếp chỉ khi đang dùng Haystack cho workflow khác.
- `SentenceWindowRetriever` lọc theo source fields và split index, fetch một batch, sort context, ghép text. Dùng pattern batch + window cho BCR context. Khi thiếu metadata có thể warn/skip theo config; adapter phải báo `CONTEXT_UNAVAILABLE`, không trình bày như đã đọc ngữ cảnh. Không ghép page, footnote, edition/revision hoặc corpus khác thành câu trích. Khuyến nghị gọi BCR `context` hoặc host reader theo canonical span thay vì tạo DocumentStore thứ hai. G3 còn cần phần điều kiện/ngoại lệ và phản chứng, không chỉ window cố định.
- `DocumentNDCG` hỗ trợ comparison field `content` (mặc định), `id` hoặc meta. Dùng `id` do host cấp, qrels từng edition/witness. Nếu chấm theo content sẽ đánh đúng câu nhưng nhầm ấn bản như đúng; RRF/qrels vẫn không đo literal offsets. `FaithfulnessEvaluator` dùng model (mặc định OpenAI nếu không cấu hình generator); chỉ kiểm hỗ trợ trong context cung cấp, không độc lập đọc source hoặc xác lập luận điểm. Nên bắt đầu bằng metrics stdlib/SQLite, dùng evaluator làm công cụ dev/QA tùy chọn nếu đã có dependency. Không lấy điểm trung bình bù false VERIFIED.

### 5.3 R2 — Tìm đúng tài sản BCR có thể kế thừa

`LocalHost` đã làm orchestration nhỏ mà Haystack không cần thay: `scope(corpora)` kiểm corpus và profile → `retrieve('search', query, ...)` gọi module retrieval qua allowlist operation → `pointer(row)` gắn provenance → `verify_pointer()` đọc source → `_gate()` gọi lại independent `source_reader` với quotation bound tại host → `evidence_reader()` mở lại recipe. `quick()` gọi search, verify từng hit, trả `verified_evidence`, `publication_authorized=False`, metrics và limitations. Đây là đường thực tế ở HEAD BCR xác nhận lại, không phải pseudocode upstream (E32–E33).

**Ưu tiên tái dùng API sẵn có:** `LocalHost.quick` cho truy vấn discovery đã kiểm; `retrieve('search')` cho candidates; `retrieve('context'/'parallels'/'variants')` cho nghiên cứu, `verify_record`/`evidence_reader` cho xác minh host. Không cấp raw Git reader, repository root, `verify_pointer`, hoặc `research_store` trực tiếp cho model. `scope` kiểm profile nhưng không đủ ACL; BodhiAtlas lọc corpus, edition, witness, rights trước lookup, kiểm tiếp sau lookup và trước model egress. Không giả `quick` trả mọi occurrences; giới hạn số candidates rõ trong R1. Đối với corpus BCR có resolver, ánh xạ Git commit/blob/path/segment/range sang SourceFile, extraction revision và source map của BodhiAtlas, giữ cả hai hệ hash; không convert Git SHA-1 thành raw SHA-256 bằng đổi tên field. Đối với tài liệu người dùng ngoài BCR, cần reader/verifier riêng, không gắn nhãn VERIFIED dựa trên BCR unsupported resolver.

**Concurrency:** `quick` reset metrics, `_gate(register=True)` thay `recipes`, vì vậy không mặc định dùng chung `LocalHost` instance cho concurrent requests; host per request hoặc serialize/lock rõ ràng; đo DB connection/thread affinity, resolver latency, lifecycle. Nếu dùng async cancellation với thread executor, timeout không đồng nghĩa thread dừng; không cho tác vụ read-only có side effects ngoài run, và giữ result deadline. BCR đang dùng SQLite/file read, không copy writable DB. Đường integration có thể làm 1 adapter nhỏ, không fork BCR hoặc Haystack trước khi test quyền reuse. Cần test thật với Git blobs nhỏ có phép, BCR instance và pinned index; R2 **chưa** chạy BCR.

## 6. Source Fidelity & Provenance

Hợp đồng đề xuất cho `Candidate` (không phải schema hiện có của repo): `file_id`, `edition_id`, `witness_id`, `raw_sha256`, `extraction_revision`, `source_span`, `canonical_start/end`, `match_kind`, `coverage`, `limitations`, `candidate_id`, `rights_scope`. `source_span` là union tagged: PDF (`pdf_page_index`, `printed_page_label`, `bbox`/range nếu có), EPUB (`href`, `spine`, CFI/range nếu có), TEI (`xml_id`, XPath/segment, ranges); thiếu precision thì khai báo page/block only. Chỉ host sinh key từ authority. Đừng tự coi offset Unicode là byte offset hoặc bbox.

Mở lại dựa trên `(file_id, raw_sha256, extraction_revision, source_span)`, dùng callback trusted của host, so hash, đúng file/edition/revision, vị trí và đoạn chữ độc lập với candidate. Với text-native, so exact canonical và source mapping; với scan, phải xác nhận hình ảnh/reading order theo chính sách rủi ro. Không cấp VERIFIED cho kết quả chỉ khớp extraction nếu OCR chưa kiểm; có thể `TEXT_ONLY`, `UNVERIFIED`, `REJECTED`, `STALE`. Giữ status quote và claim riêng: trích đúng không đảm bảo nguồn hỗ trợ luận điểm. Lưu verifier version, thời điểm, evidence ID, scope đọc; G3 xem ngữ cảnh và người duyệt. Nếu reindex/parser swap, giữ extraction cũ hoặc báo stale, tuyệt đối không redirect sang edition mới theo cùng tên.

Ví dụ đối kháng: edition A “không được phép”, B “được phép”; candidate tự khai `verified=true` và dẫn B dưới ID A. Host bỏ cờ, kiểm hash và locator theo catalog. Nếu chữ đúng nhưng cắt phủ định/context, G3 vẫn cần human. E21 BCR đã có contract trusted callback nên ưu tiên tái dùng sau khi kiểm adapter; Git blob SHA-1 không thay raw SHA-256; không mở rộng tự động resolver lên PDF/EPUB chưa được test.

## 7. Multilingual & Retrieval Behavior

| Mode | Semantics đề xuất | Haystack và kiểm thử |
|---|---|---|
| EXACT | mọi vị trí literal Unicode trong declared canonical stream, có revision, coverage và cursor; không casefold | host scanner; E11 ranked không thể thay. Fixture TC05 có 25 hit trên 21 records |
| NORMALIZED | transform có log/version, NFC/NFD, không dấu, giản/phồn hoặc script transliteration có điều kiện | Store BM25 lowercase/NFC, CJK per-char theo docstring E09; không bảo đảm full substring recall; cleaner ASCII-only không dùng cho canonical |
| FUZZY | ứng viên edit-distance/OCR noise, show diff và threshold | host thuật toán riêng, không gọi BM25 score là fuzzy/quote verification |
| LEXICON | sense ID, dẫn chứng, bản dịch và song hành đã xác nhận | host, không tự đồng nhất Pāli/Sanskrit hoặc Hán/Tạng |
| SEMANTIC | ranked candidates dựa model và qrels | V2 tùy chọn, metric Recall@k/nDCG/MRR; không đổi nhãn EXACT/G2 |

Ca cần thử: `苦`, `無常`/`无常`, `anattā`/`anatta` (NFD vs NFC), Việt `đ`/`d` (không cùng chữ), `vô thường`/`vo thuong`, Tạng và Wylie. Không dùng normalize toàn bộ phá nguyên văn. TC06 hiện chỉ thử literal Hán hai dạng trong fixture; Pāli/Việt/Tạng có trong dữ liệu nhưng chưa chạy query gold cho từng chữ, chưa kiểm tokenizer Haystack. Thứ tự hit stable theo canonical position, dedupe theo `(file, revision, start, end)`, không theo nội dung trích. Cross-boundary chỉ cho khi canonical stream và separator được công bố, source mapping cho cả hai đoạn. Trường hợp index thiếu trang: `PARTIAL` với scope và lỗi, không kết luận vắng nguồn; pagination phải snapshot-stable. `search_complete` chỉ đúng trong declared eligible scope khi scanner hoàn tất; không suy từ `len(results) < top_k`.

## 8. Integration Options

| PA | Kiến trúc / owner | Chi phí/rủi ro định tính | Đánh giá |
|---|---|---|---|
| A | direct Python + ports, host owns catalog/scanner/G2 | L cho glue; H cho scholarly core vốn phải làm | **Ưu tiên V1**; ít layer debug/lock |
| B | Haystack in-process code-only, custom retrieval/lookup/verify wrappers | M cho glue + pins/graph/security; vẫn H core | Chỉ thử nếu graph thực sự giảm complexity và integrity bằng A |
| C | Haystack chỉ V2, đọc evidence cards qua read-only port | M; thêm provider/deps/token/rights | DEFER đến workflow đa nhánh/model thực |
| D | RAGFlow hoặc Open Notebook workspace riêng, không ghép cả hai | H tương đối vì deployment/state/ACL sync; chưa đo | Nếu cần UI workspace/OCR hơn code graph thì thử đúng vai trò |
| E | reuse patterns/tests, không cài runtime | L; đọc license trước copy code | Học explicit IO, error tests, branch diagnostics, không dựng framework chung |

Port tối thiểu, giữ thuần Python (minh họa `[PLAN]`, chưa chạy integration):

```python
class EvidencePort(Protocol):
    def search(self, query: Query, scope: Scope, cursor: str | None) -> SearchPage: ...
    def lookup(self, key: SourceKey) -> SourceRecord: ...
    def verify(self, candidate: Candidate, principal: Principal) -> CitationCheck: ...

def mode1(port, query, scope, principal):
    page = port.search(query, scope, cursor=None)  # exact scanner or explicit ranked mode
    return page, [port.verify(c, principal) for c in page.candidates]
```

`SearchPage` chứa `status`, `match_kind`, `declared_scope`, `coverage`, `limitations`, `total_occurrences` (null nếu ranked/unknown), `next_cursor`, `search_complete`. Host xác minh principal trước search/lookup; verifier mở source từ key hợp lệ chứ không dùng untrusted path. Không dùng 3 wrapper riêng nếu cả 3 chỉ chuyển tiếp. Nếu thử B: `@component` bọc port, outputs typed DTO/dict, không cần `DocumentStore` hay LLM; inject dependency host tại khởi tạo, không serialize credentials/authority DB; config chỉ chứa tên adapter được allowlist. Graph build và execution nằm dưới `adapters/haystack/`, import optional; không để Haystack import ngược vào core. Rollback: tắt feature flag, gỡ extra dependencies và xóa derived cache sau khi bảo toàn audit; evidence IDs/canonical schema/SQLite vẫn hoạt động, TC15 kiểm không đổi output. Không fork toàn framework hoặc copy code chỉ vì thấy thuận tiện.

### 8.1 R2 — Bản đồ tài sản cụ thể: lấy gì, đặt ở đâu, cách lấy

| Tài sản đã xem | Vị trí | Cách lấy ưu tiên | Dependency/chi phí và điều kiện |
|---|---|---|---|
| BCR `LocalHost`/Gate A (không phải Haystack) | V1 adapters và verifier | Reuse API với pinned source; một authority BodhiAtlas | M; cần map identity/rights, resolver scope, license; không tái viết gate nếu có thể reuse |
| Component socket contracts | V1/V2 module interfaces | Học pattern; `dataclass`/Protocol typed của host | L; không copy Component metaclass; không kéo networkx cho 3 calls |
| Pipeline graph + lifecycle | V2 orchestration | Dùng library nếu POC workflow branching pass | M; `haystack-ai`, graph, serialization, debugging; adapter scope |
| `Tool`, `create_tool_from_function` | V2 tools | Wrap hàm host khi đã chọn Haystack | L–M; schema generated chỉ convenience; auth closure bắt buộc |
| `ComponentTool`, `PipelineTool` | V2 tái dùng workflow | Chỉ thử khi đã có component/pipeline cần expose | M; tránh wrap nhiều lớp cho một function |
| Agent hooks + exit counters | V2 research iteration | Library (không tách code vòng lặp) | M–H; model/tool schema, budget, retry/error, hooks mutation, logs; chưa chạy |
| ConditionalRouter | V2 fixed branches | Library nếu đã dùng graph; nếu không `if` Python | L–M; trusted config, tránh unsafe Jinja |
| MultiRetriever/RRF/DocumentJoiner | V2 ranked candidates | Học algorithm hoặc gọi library, dùng identity host | L–M; no DB nếu retriever adapter phù hợp; top-K không EXACT |
| SentenceWindowRetriever | V1/V2 context | Học pattern batch/window; gọi BCR context | L–M; không tái tạo store chỉ vì API này |
| `DocumentNDCG` / Recall | QA dev/test V2 | metrics stdlib hoặc evaluator nếu đã cài | L; gold identity and qrels, không LLM |
| Faithfulness evaluator | QA V2 thử nghiệm | Optional model judge, không pipeline mặc định | M; egress/token/false judgement, human review |
| DoclingConverter wrapper | V1 ingest tham khảo | Dùng Docling trực tiếp; học mapping `dl_meta` | H cho parser/sourcemap, wrapper không loại bỏ việc này; tránh serialize làm mất config |
| FastEmbedRanker/ST ranker | V2 rerank trên candidates sẵn | Thử trực tiếp thư viện hoặc integration nếu đã dùng graph | M; weights, CPU/RAM, corpus benchmark; không thêm vector store trước |
| HanLP splitter | V2 CJK discovery/chunking | Defer; direct HanLP nếu benchmark cần | M–H; pretrained model không đặc biệt cho Hán cổ, không dùng cho exact |
| MCPTool/MCPToolset | V2 kết nối nguồn/clients khác process | Defer đến khi cần transport; local API trực tiếp trước | M; auth, timeout, allowlist, server pin, tool output injection |
| Ollama chat generator | V2 optional model-local | Chọn một backend sau model evaluation | M; daemon/model weights, localhost không là guarantee offline |
| Hayhooks | V2/V3 API deployment | Defer; dùng API host sẵn nếu có | M–H; dịch vụ và deploy control plane, auth chưa audit |
| InMemoryDocumentStore / external vector stores | V2 disposable cache nếu cần | Không dùng làm authority; hiện chưa cần | M–H; duplicate/backup/index lifecycle/ACL; có thể rebuild từ canonical |

**Copy code vs dependency:** chưa tìm thấy module lõi Haystack nào cần fork hoặc copy để BodhiAtlas V1 hoạt động. Những thuật toán nhỏ (RRF, typed port, deterministic context, explicit failure) có thể triển khai độc lập theo contract, viết test độc lập; nếu sao chép mã Apache-2.0 phải giữ LICENSE/NOTICE và đánh dấu thay đổi theo điều khoản, rà giấy phép transitive. Agent/Pipeline kéo nhiều module graph/socket/state/serialization/tracing nên tách vài file làm fork riêng **không có bằng chứng tiết kiệm**; nếu chọn thì dùng package đã pin, ở extra V2. Với integrations, wrapper có thể ngắn nhưng còn dependency backend thật; dùng trực tiếp backend khi không có graph. Không quyết định copy code BCR/Bang-ha chỉ từ việc truy cập repo.

### 8.2 R2 — Khảo sát hệ sinh thái integrations và shortlist có mục tiêu

Đã kiểm cây recursive của monorepo và đọc code/package các integration quyết định. Không xem sự hiện diện trong tree là chất lượng hoặc tương thích. Snapshot integration HEAD khác release core; version thực cài được **UNKNOWN** cho các integration. Pin cả package và backend/model/config trước POC. Không cài hàng loạt.

| Nhóm / module | Evidence level | Quyết định và use case |
|---|---|---|
| `docling-haystack` | CODE E34/E40 | Ưu tiên Docling direct cho PDF/layout; tham khảo metadata. `DOC_CHUNKS` gọi contextualize, `split_idx_start` cộng `len(chunk.text)`; không chứng minh offset trong canonical hoặc content đã contextualize. `MARKDOWN` là derived text; `JSON` export structured doc hữu ích để giữ provenance nhưng vẫn cần pin raw SHA/parse revision và validate locator. Page metadata chỉ min(page_nos), phải giữ đủ pages/bboxes/ranges. Meta từ source có thể ghi đè field output. `converter` và `chunker` tùy chỉnh không serialize, default chunker có thể tải tokenizer trong warm_up. Vì vậy không dùng wrapper làm canonical ingest authority. |
| `fastembed-haystack` | CODE E36/E40 | Candidate rerank không cần vector DB; thử direct FastEmbed vs wrapper khi thật sự cần. `local_files_only` và cache phải cấu hình, block network; top_k và score_threshold có thể loại documents. Model mặc định ms-marco MiniLM không mặc nhiên phù hợp Pāli/Hán/Tạng/Việt. |
| `sentence_transformers` | CODE E36 | Đối chứng cross-encoder/rerank, dense/sparse/multivector directories có trong tree; chỉ đọc similarity ranker. Nặng hơn tùy model; pin license và weights, không cài cả ecosystem. |
| `ollama-haystack` | CODE E37/E40 | Candidate local LLM for V2; default localhost HTTP, usage metadata map; model tool-calling cần kiểm. Thêm daemon, RAM, model file; không phải dependency V1. |
| `mcp-haystack` | CODE E35/E40 | MCP client có stdio/Streamable HTTP/SSE, tool discovery và timeout; chọn allowlist cố định. Dùng direct ports nếu cùng process. Cấm tự chạy command/uvx hoặc nhận URL từ model; no external corpus egress khi chưa quyền. |
| `hanlp` | CODE E38 | Tokenization/splitting tiếng Hán cho discovery; warm_up `hanlp.load` pretrained, pin và prefetch; chưa chứng minh Hán cổ hoặc literal, không thay CJK scanner. |
| `hayhooks` | DOC/CODE E39 | REST/MCP wrappers cho deployment nếu V2 thành service; thêm endpoints quản trị, phải cô lập. README có durable/human approval, chưa audit implementation. |
| OCR/parser khác: `paddleocr`, `minicpm_ocr`, `opendataloader_pdf`, `kreuzberg`, `markitdown`, `unstructured`, `chonkie`, `docling_serve` | TREE ONLY | Tồn tại đường dẫn; không đánh giá chất lượng hoặc license. Đối chứng trực tiếp extractor được chọn từ nghiên cứu ingestion chuyên biệt; không mở rộng P59 thành audit tất cả OCR engines. |
| Vector/index: `faiss`, `qdrant`, `pgvector`, `opensearch`, `elasticsearch`, `sqlite`-adjacent `sqlalchemy` | TREE ONLY | Chưa mở code; không coi package tên SQLAlchemy là SQLite EXACT backend. Defer đến khi V2 semantic retrieval có nhu cầu đo được, giữ index secondary. |
| Provider/observability/eval: `anthropic`, `openrouter`, `llama_cpp`, `vllm`, `ragas`, `deepeval`, `langfuse`, `opentelemetry`; web search, Drive, GitHub, agent_pack | TREE ONLY | Có directories, không cam kết khả năng từng module. Chọn tối đa một provider/model và một phương án đo nếu cần; remote logging/connector bị giới hạn rights; không coi provider switch giải quyết source fidelity. |

**Dependency gate:** 4 manifest đã đọc cho thấy Docling wrapper yêu cầu `haystack-ai>=2.12.0`, `docling>=2.32.0,<3.0.0`; MCP `haystack-ai>=2.23.0`; FastEmbed `haystack-ai>=2.24.1`, `fastembed>=0.8.0`; Ollama `haystack-ai>=3.0.0`, `ollama>=0.6.2`. Lower bounds rộng không chứng minh compatibility hoặc security; chưa có lock package nào ở R2. Chọn một integration khi POC có vai trò rõ, chạy `pip check`, SBOM, license/CVE scan và import/network-denied smoke test. Nếu muốn Docling thì direct Docling không cần haystack-ai; nếu muốn FastEmbed thì direct FastEmbed không cần Haystack; nếu muốn MCP thì SDK hoặc API host có thể đủ. Giá trị framework chủ yếu xuất hiện khi **phối hợp nhiều component đã chọn**, không phải chỉ để lấy một backend.

### 8.3 R2 — Kiến trúc ghép cụ thể, không tạo authority thứ hai

```text
UI / API host
  ├── Mode 1: direct Python → Catalog + authorized scope → exact / normalized / fuzzy / lexicon
  │             → CandidateRef → BCR/reader trusted verifier → evidence card + coverage
  └── Mode 2: optional ResearchOrchestrator (direct first, Haystack trial)
                ├── search_lexical(query, source_group)   ─┐
                ├── parallel/variants/context(evidence_id) ├─> same V1 host API (read only)
                ├── search_library(query, language)      ─┤
                └── request_counterevidence(claim)       ─┘
                 ranked merge on scoped IDs → host verify → rights/redaction filter
                 → one model synthesis → claim review by scholar
                [optional agent loop only after static flow and error/budget POC]
```

**Contract tối thiểu đề xuất** (không phải code production): `SearchRequest(query, match_kind, corpus_group, cursor, candidate_limit)`; host bind `AuthorizedScope(user, corpus_ids, edition_ids, rights, allowed_operations, run_id)` bằng đối tượng nội bộ bất biến. `SearchResult(candidates, scope_revision, mode, coverage, errors, search_complete, cursor, count_kind)`. `CandidateRef(evidence_handle, file_id, edition_id, witness_id, extraction_revision, source_span, raw_sha256, match_kind, score, retrieval_reasons, limitations)`; score chỉ discovery. `VerifiedEvidence` là record từ authority (G2 status riêng, locator precision, source reread/hash, allowed quotation, source limitations, context_handle, claim_status=NOT_ASSESSED). Chỉ host ký/ghi status, model output là proposal. Data returned cho agent chỉ gồm opaque handle + excerpt theo rights, không raw path hay private metadata. `get_context` nhận handle đã đăng ký, host kiểm scope và mở nguồn mới; không truy xuất record ID tùy tiện qua model. `search_complete` cho EXACT scanner được tính theo canonical scope, không từ agent/joiner.

**Đề xuất vị trí file khi thực hiện (chưa tạo repo/file):** `core/contracts.py` và `core/evidence_service.py` không import Haystack; `adapters/bcr.py` bọc LocalHost, `adapters/library.py` bọc index/source map; `research/direct.py` là baseline V2; `research/haystack_adapter.py` là optional extra; `research/policy.py` giữ budget/ACL/egress; `tests/contract/` dùng cùng oracle cho cả hai path. Đường gỡ bỏ: bỏ extra và adapter, core API/catalog/evidence handles/backup không đổi; không migration data schema vì framework. Không chốt paths nếu cấu trúc BodhiAtlas hiện có khác. Chỉ thử trong nhánh/sandbox riêng khi user yêu cầu.

### 8.4 R2 — POC minh họa adapter ít glue, không fork

Ví dụ sau **[PLAN] chưa chạy** trên Haystack 3.5.0. Chỉ minh họa interface `@component` và `create_tool_from_function` đã đọc; `host` là facade do BodhiAtlas cung cấp chứ không phải API upstream. Không expose `AuthorizedScope` vào tool schema, không tin `Document.meta` làm G2. Cài optional extra sau khi lock. Đường code thật của BCR ở §5.3; adapter POC phải gọi đúng facade đó.

```python
# PLAN: research/haystack_adapter.py; do not execute against real corpus without authorization.
from haystack import Pipeline, component
from haystack.tools import create_tool_from_function

@component
class SearchCandidates:
    def __init__(self, host):
        self.host = host  # host binds request-scoped authorization

    @component.output_types(batch=dict)
    def run(self, query: str):
        return {"batch": self.host.search_candidates(query=query, mode="RANKED")}

@component
class ReopenEvidence:
    def __init__(self, host):
        self.host = host

    @component.output_types(result=dict)
    def run(self, batch: dict):
        # authority rechecks handles + rights, never reads arbitrary paths
        return {"result": self.host.verify_batch(batch)}

# compare with direct call host.verify_batch(host.search_candidates(...))
def build_pipeline(host):
    p = Pipeline()
    p.add_component("search", SearchCandidates(host))
    p.add_component("verify", ReopenEvidence(host))
    p.connect("search.batch", "verify.batch")
    return p

# closure deliberately excludes auth/scope and filesystem parameters from schema
# closure serialization is NOT promised; build in trusted code per request

def make_search_tool(host):
    def search_sources(query: str, source_group: str) -> dict:
        """Find authorized candidate evidence in a named source group."""
        return host.search_for_model(query=query, source_group=source_group)
    return create_tool_from_function(search_sources)
```

Scope group được host kiểm intersect, không tự nâng quyền; errors/coverage phải structured, never convert exception to empty batch. Với 2 steps này direct calls rõ hơn, **không** coi ví dụ là lý do chọn graph. POC có giá trị hơn là 3 nhánh thật (BCR kinh Pāli, BCR Hán, thư viện nghiên cứu) chạy song song, một nhánh có lỗi, RRF candidate-only, context/verify independent. Nếu cần serialize graph, lưu config đơn giản chỉ tên operation và version; cấp lại host capability bằng trusted factory lúc runtime, không serialize live DB/closure/secret. Nếu không cần serialize, dùng code construction. Agent chỉ sau khi flow tĩnh pass; không bắt buộc LLM để chạy graph. Không tạo agent mỗi nguồn vì retrieval backend đã là chuyên biệt.

## 9. Practical POC & Reproduction Plan

### 9.1. Kết quả thực sự có

Sandbox Linux x86_64 kernel 6.18.57, glibc 2.41, Python 3.13.5, SQLite 3.46.1, CPU được báo AMD EPYC 9V74, RAM nhìn thấy 6,090,668 kB (không đồng nghĩa cgroup quota), GPU không kiểm/không dùng. `git ls-remote` hai repo thất bại DNS. `importlib.util.find_spec('haystack')` trả None. Không tải package/weights, không gửi corpus. Không chạy upstream. Không có dependency lock/installed package inventory của Haystack. Môi trường thử chỉ Python stdlib.

Fixture tự sinh 24 đoạn, SHA-256 serialization UTF-8 compact JSON `b936be51a4518c52ca8c86b935fb9efaff08438024867a5cabed83b5581639fb`. Oracle lập trước scan: `p00..p19` offset 0, `multi` offsets 0,2,4,6,8; B và restricted ngoài scope. 25/25 hit, precision=recall=1 **chỉ fixture**, không benchmark corpus. Mô hình cắt top-K ở mức record (không gọi BM25) trả 10/21 records, không thể suy total occurrence. Hai assertion Hán literal và cross-boundary giản lược; trusted byte stub kiểm hash và quote ở offset 0 với hai negative. Không phải source reader thật; fake citation ở locator khác và OCR chưa thử. Log và script nhúng Appendix.

### 9.2. TC01–TC15 (oracle trước chạy)

`actual=null` nghĩa không chạy đối tượng upstream; các kết quả cô lập ghi riêng, không điền thay. Status upstream tất cả NOT TESTED, ngoài CODE GAP E11/E14 ở cấp hợp đồng. Fixture/expected dưới đây là kế hoạch; cần lập gold đầy đủ trước POC thực.

| TC | Expected / oracle | Actual upstream | Kết quả / kế hoạch bổ sung |
|---|---|---|---|
| 01 | cài 3.5.0 từ locked wheels, import core không network/model; inventory | null | NOT TESTED; module không có, DNS blocked. Ghi Python/OS/lock/hash |
| 02 | 3 direct calls và graph cùng oracle evidence payload/status; không authority mới | null | NOT TESTED; baseline scanner cô lập không phải 3-step integration. Đo LOC/config/debug/latency/RSS |
| 03 | BCR retrieval port + verifier trusted callback, candidate cờ giả bị bỏ | null | NOT TESTED; BCR code đọc lại; stub TC10 không phải BCR thật |
| 04 | hai edition cùng quote nhưng hai file/revision; split/clean/serialize/join roundtrip native span không silent loss | null | NOT TESTED; E06–08 cho failure design; pin explicit IDs và so golden payload |
| 05 | 25 hits trong scope fixture, 21 records; >top_k, 5 hit 1 passage, cross-boundary; không fake complete | null | TESTED-ISOLATED 25/25; model top_k=10, không phải BM25. Chạy upstream comparator và pagination |
| 06 | Hán 1–2 ký tự, Pāli/Việt/Tạng, NFC/NFD, mode labels đúng | null | TESTED-ISOLATED Hán `無常` và `无常` mỗi một vị trí; các ngôn ngữ còn lại query gold chưa thử |
| 07 | rights/edition filter, duplicate overwrite fail closed, không cross-scope | null | TESTED-ISOLATED chỉ exclusion B/restricted trong oracle scanner, chưa thử store filters/overwrite/ACL |
| 08 | node error, timeout, partial store, retry/branch → explicit ERROR/PARTIAL, không fake no-hit | null | NOT TESTED; E04 static. Fault injection trước/sau I/O, idempotence |
| 09 | old evidence mở đúng revision hoặc STALE sau reindex/restore; DB owner một | null | NOT TESTED; cùng và khác extractor profile, hash and locator oracle |
| 10 | fake VERIFIED, wrong hash/edition, OCR negation → zero false verified trên negatives | null | TESTED-ISOLATED byte/hash stub 1 positive 2 negatives; không OCR/G3. Cần independent raw reader |
| 11 | sync/async deterministic semantics, cancellation/branch policy, overhead | null | NOT TESTED; thử concurrency=1/4, blocking task & cancellation; đo cùng workload |
| 12 | tắt model/embedding/vector/remote store, egress denied, Mode1 vẫn đúng | null | NOT TESTED Haystack; direct stdlib script không gọi network, không phải network-denial instrumentation |
| 13 | config roundtrip đúng version, reject unsafe/module lạ, không dynamic code tải | null | NOT TESTED; E05/E13 static safeguards; clean process + allowlist explicit |
| 14 | RAG local/approved model, source refs chỉ candidate, injection không đổi policy | null | NOT TESTED, không tải model; cần local weights rights + qrels + logs |
| 15 | gỡ framework chỉ adapter thay; core query/verify unchanged, chi phí so A | null | NOT TESTED; compare diff/import dependency graph, remove-extra smoke test |

### 9.3. Map T01–T16 sổ tay

| T | Phạm vi / liên hệ | Kết quả hiện tại |
|---|---|---|
| T01 scan hai cột, OCR phủ định | G1/G2, TC10, host/parser | NOT TESTED |
| T02 hai ấn bản lệch trang | TC04/09, host reader | NOT TESTED |
| T03 Việt không dấu, Hán giản/phồn | TC06 | ISOLATED literal Hán, không kiểm normalization |
| T04 Tạng/Wylie lỗi | TC06, host transliteration | NOT TESTED |
| T05 hai nghĩa | G5 host lexicon | N/A orchestrator, host NOT TESTED |
| T06 Nikāya/A-hàm khác đoạn | G3 host witness relation | N/A, host NOT TESTED |
| T07 ba bản dịch chung bản gốc | G3 independence | N/A, host NOT TESTED |
| T08 tuyệt đối hóa luận điểm | G3 human | N/A, host NOT TESTED |
| T09 niên đại bản chép vs sự kiện | G3 human | N/A, host NOT TESTED |
| T10 thiếu trang nhưng 0 hits | TC08/09, coverage | NOT TESTED |
| T11 DOI/abstract | G4, read-level metadata | NOT TESTED |
| T12 prompt injection website | TC13/14, trusted config | NOT TESTED |
| T13 đổi chunk IDs sau reindex | TC04/09 | NOT TESTED |
| T14 mâu thuẫn định nghĩa | G6 human/claim ledger | N/A, host NOT TESTED |
| T15 quote đúng, ngữ cảnh bác bỏ | TC10/14; G3 human | NOT TESTED |
| T16 hạn chế chia sẻ | TC07/12, deny egress | ISOLATED scope exclusion, egress NOT TESTED |

### 9.4. Reproduction plan có ngưỡng dừng

1. Trong máy có quyền tải phần mềm (không corpus), chuẩn bị wheelhouse từ PyPI 3.5.0 và dependencies, kiểm SHA-256, license và vulnerabilities, pin toàn bộ bằng lock có hashes. Tách môi trường riêng cho 2.31.1 nếu compatibility cần; không cài cả hai cùng namespace. Các lệnh dưới là **PLAN**, chưa thực thi; `requirements-p59.lock` chưa được tạo.

```sh
# Trên máy chuẩn bị đã được cho phép tải; lock với công cụ dependency hiện dùng
python3.13 -m venv .venv-p59
. .venv-p59/bin/activate
# requirements-p59.in chứa haystack-ai==3.5.0; sinh lock có hashes, duyệt SBOM
python -m pip download --require-hashes -r requirements-p59.lock -d wheelhouse
# Trong sandbox network-denied, không credentials, chỉ wheelhouse đã duyệt
export HAYSTACK_TELEMETRY_ENABLED=false
export HAYSTACK_CONTENT_TRACING_ENABLED=false
. .venv-p59/bin/activate
python -m pip install --no-index --find-links=wheelhouse --require-hashes -r requirements-p59.lock
python -m pip check
python -m pip freeze --all
python -c 'from importlib.metadata import version; print(version("haystack-ai")); from haystack import Pipeline, component'
```

2. Clone đúng SHA nếu cho phép, tách dev lock và chạy test chọn lọc (pytest/dev dependencies phải lock riêng): `python -m pytest test/dataclasses/test_document.py test/components/preprocessors/test_document_splitter.py test/components/builders/test_answer_builder.py test/core/pipeline/test_async_pipeline.py test/core/test_serialization_security.py`. Không đánh đồng các test upstream với acceptance BodhiAtlas. Không chạy provider tests yêu cầu network/API keys.
3. Dùng fixture appendix như oracle ban đầu, mở rộng manifest cho raw files/revision, text-native/scan synthetic 2 ấn bản, source map page/offset, rights, unknown ranges; ký hash oracle trước khi chạy. Viết cùng `scan/lookup/verify` functions cho cả direct và 3 custom components; log JSON theo trace ID, input hash, expected, actual, pass/fail, errors; `actual=null` nếu không chạy. BCR integration read-only trên bản sao sandbox có quyền, dùng pinned revision, không thay source pins. Benchmark one warmup và nhiều iterations, cùng process/config, record cold startup, p50/p95, RSS, LOC/config, deps/services, stacktrace/debug minutes, failures/rollback. Không lấy output graph làm oracle.
4. B chỉ sống nếu exact precision/recall=1 trên gold, wrong-edition/false-VERIFIED=0, no false complete, no unauthorized egress; tất cả status giữ nguyên, no second authority, old evidence correct/STALE, removal test pass. Sau đó cần ít nhất một workflow thực có branches/async, chứng minh giảm glue/maintenance so với A ở cùng hợp đồng. So cả chi phí upgrade, dependency review và error handling, không chỉ latency. Nếu chỉ giảm vài dòng mà thêm lock/config/graph debugging, chọn A. TC14 chạy sau cùng nếu V2 được ưu tiên; qrels/grounding/token thực log, không dùng model judge để cấp G2.

### 9.5 R2 — Thực nghiệm bổ sung và oracle đối kháng

**Thực sự chạy:** `python /tmp/p59r2.py`, Python 3.13.5, Linux x86_64; chỉ stdlib. Fixture tự tạo 4 files (2 edition Pāli, Hán, restricted modern); oracle 3 span xác định trước khi implement. Mô phỏng merge state và dedup theo cơ chế đọc ở upstream, **không chạy Haystack**. Script và log đầy đủ §13.5. Không dùng corpus/model/API bên ngoài. Fixture SHA-256 `d38d3472a7434df4431c93c20b523f2a05e9e8f640b15a9e5753b571748d8dae`. `MATCHED_FIXTURE` cố ý không đặt tên VERIFIED. Oracle independent là literal offsets hard-coded, không dùng output ứng viên.

| Ca bổ sung | Expected trước chạy | Actual / status | Giới hạn |
|---|---|---|---|
| R2-I01 direct vs stdlib async fanout | Cùng 3 span, 2 edition giữ riêng | 3/3 cả hai; PASS ISOLATED | Không benchmark graph/Haystack/BCR |
| R2-I02 lỗi branch Hán | PARTIAL + 2 Pāli span | PARTIAL/2; PASS ISOLATED | Timeout synthetic, chưa chạy cancellation upstream |
| R2-I03 restricted scope | DENIED | DENIED | Không ACL/egress production |
| R2-I04 wrong edition / old revision / bad hash / sai quotation range | REJECTED / STALE / REJECTED / REJECTED | Cùng expected, 4/4; PASS ISOLATED | Byte/Unicode text fixture; không PDF/source reader thật |
| R2-I05 LLM/state collision | LLM scope thắng trong model giản lược | `restricted` thắng; host closure vẫn DENIED | Source-derived model; E26 code + upstream test đã đọc, chưa chạy |
| R2-I06 dedup cùng quotation khác edition | naive 1, identity-aware 2 | 1 vs 2; PASS ISOLATED | Không chạy RRF code thật |
| R2-I07 quote đúng nhưng phủ định claim | Không suy `self` hỗ trợ luận điểm từ substring | Có `self` và `not self`; PASS diagnostic | Không chứng nhận G3 |

### 9.6 R2 — POC thực tế theo từng cổng, thứ tự đầu tư

| Bước / test | Chạy gì và đối chứng | Ngưỡng pass / stop rule | Actual |
|---|---|---|---|
| R2-P0 / TC01,12 | Sandbox có wheelhouse: cài `haystack-ai==3.5.0` và lock hash, deny network, telemetry off trước import, smoke graph no model | pip check; no egress; Core chạy khi package absent; nếu không pass dừng | null; NOT TESTED |
| R2-P1 / TC02,03,05,10 | BCR pinned HEAD, DB read-only, Git fixture source resolver hỗ trợ; direct `LocalHost.quick` vs component wrapping host; golden pointer/hash/span; riêng scanner canonical fixture | same retrieval scope, all oracle occurrences trên EXACT path riêng; 0 wrong edition, 0 fake VERIFIED; report error/coverage; không thêm writable store | null; NOT TESTED |
| R2-P2 / TC08,11,15 | Direct stdlib fanout vs Pipeline static, 3 provider nhóm; forced timeout, cancellation, wrong corpus, ACL; compare same output/error | same normalized ordered output, partial/error visible, no restricted payload, rollback no core diff; nếu không giảm complexity rõ dừng graph | null; isolated stdlib only |
| R2-P3 / TC04,09,13 | Roundtrip config và reindex fixture; custom Docling converter/chunker pinned, direct backend vs wrapper nếu cần; changed rev stale | no silent config drop hoặc reject roundtrip, exact source locator stable/stale; compare output/source map, nếu không dùng direct backend | null; NOT TESTED |
| R2-P4 / TC06,07 | Candidate rerank FastEmbed vs direct FastEmbed hoặc baseline lexical; qrels theo file/revision/span, Hán cổ/Pāli/Việt/Tạng; same top_k, same authorized input | recall@k không giảm ngoài ngưỡng đã chốt; nDCG/MRR cải thiện trên held-out qrels với chi phí chấp nhận; exact không thay đổi; không chọn nếu không có lợi ích | null; NOT TESTED |
| R2-P5 / TC14 | Mock tool-call generator (không model thật) tạo state override, wrong tool, failed tool, max steps, injection, malicious tool result; sau đó optional local model có quyền | no auth bypass, no false VERIFIED, no secret/path exposure, explicit exit reason, budget/cancellation; không model thật nếu mock fail | null; NOT TESTED |
| R2-P6 / TC15 | Gỡ extra Haystack, chạy lại core contract; restore backup; compare direct vs pipeline vs optional Agent trên workflow thật | data và locator unchanged hoặc stale, no migration, code-only suite same. Chỉ chọn nếu evidence integrity pass **và** tổng complexity/ops giảm | null; NOT TESTED |

**Phép đo quyết định TCO (kế hoạch, không bịa số):** chạy từng path trong process riêng cùng OS/CPU/Python/lock; 30 warm iterations và 5 cold runs là cấu hình đề xuất, báo median/p95 và distribution, không khẳng định đủ power statistical. Dùng `time.perf_counter`, `/usr/bin/time -v` peak RSS, log timeout, exception stack, process startup; `pip inspect`/lock hash số package; ghi actual lines/module/config và test count (loại fixture dùng chung), số service, thời gian sửa một thay đổi schema và gỡ adapter. V2 model ghi calls, input/output tokens, retries, model/cache/weights, giá theo provider thực tại thời điểm đo; không quy đổi giả ngày công. Đo cả positive và failure; fail một hard gate là loại scope đó dù nhanh hơn. Chọn workflow thực: nghiên cứu vô tướng tâm định từ hai nguồn kinh và một tài liệu nghiên cứu đã có quyền. Tách câu hỏi discovery, quote verify, claim review; oracle do học giả kiểm trước. Không chạy toàn corpus hoặc gọi provider ngoài khi chưa quyền.

**Ngưỡng chọn graph đề xuất (chưa phải yêu cầu PRD):** TC contract pass; không tăng số authority/service bắt buộc; core không import Haystack; có ít nhất một flow branching/async thật mà direct code phải maintain scheduling/error state đáng kể; so diff+regression cho một thay đổi thêm retriever hoặc model. Chọn graph nếu giảm glue/maintenance thực tế mà không làm startup/latency/RSS vượt budget do chủ dự án định sau đo baseline. Không tự áp con số phần trăm giả. Nếu direct stdlib async đã đơn giản và dễ debug, giữ A. Nếu chỉ Agent workflow có lợi ích, dùng C theo feature flag. Nếu chỉ muốn evaluator/reranker, thử library trực tiếp trước.

**Lệnh tái lập upstream (PLAN, chưa chạy):** chuẩn bị wheelhouse verified và lock có SHA-256 từng transitive wheel trên máy có quyền Internet; không để pipeline tự download model. Trong venv offline, `python -m pip install --no-index --find-links=/approved/wheels --require-hashes -r locked-v2.txt`; `python -m pip check`; env `HAYSTACK_TELEMETRY_ENABLED=false` và deny outbound bằng network namespace/firewall; `python -c 'import haystack; print(haystack.__version__)'` hoặc `importlib.metadata.version("haystack-ai")` nếu module không expose `__version__`; checkout release SHA trên máy được phép, chạy test đã mở `pytest test/components/agents/test_tool_calling.py -k inject_state_args`, `pytest test/components/agents/test_agent_hooks.py`, `pytest test/core/pipeline/test_async_pipeline.py` với dev dependency pin. Sau đó chạy contract fixture direct/graph cùng DB và trusted reader, ghi logs redacted. Không tự cài dựa vào version lower bounds; không coi lệnh PLAN là log.

## 10. Deployment, Security, Legal, Cost

- **Local/offline:** Python core có thể điều phối code, không bắt buộc model/service; nhưng chưa chứng minh offline runtime. Telemetry mặc định bật theo E17; tắt trước import, tắt content tracing, deny outbound ở OS/container, không provider credentials, kiểm socket attempts và logs redacted. Không chỉ dựa vào env flag. Store shared default cần tránh trong multi-user; explicit principal/ACL trước query, lookup, cache, export và delete. Store temporary không giữ dữ liệu restricted ngoài quyền.
- **Config/code execution:** chỉ cấu hình đã duyệt/hash/allowlist; cấm `unsafe=True`, không arbitrary component imports, không cho corpus hoặc LLM chọn executable reader/config. Giới hạn size/count/depth, parser timeout, path traversal/symlink, zip bombs, XXE/DTD, filesystem sandbox; không có bằng chứng các kiểm soát này native toàn hệ thống. Tool/agent V2 không được tự đổi permissions hoặc chạy side effect. Cancellation không đồng nghĩa undo; writes của authority do host transaction.
- **License:** [LICENSE](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/LICENSE) Apache-2.0 cho code release, cho phép commercial theo điều kiện license, bảo toàn notices/attribution và đánh dấu thay đổi khi phân phối theo nghĩa vụ áp dụng. NOTICE riêng chưa xác minh; không kết luận không tồn tại. Kiểm dependency licenses, model weights, corpus rights, trademarks, integration và điều khoản enterprise/cloud riêng; chưa có legal clearance. Repo public không cấp quyền mọi dữ liệu. Không gửi sách restricted tới model/cloud; review data retention, jurisdiction, contractual terms trước khi bật V2.
- **Backup/restore:** authoritative raw SHA/catalog/revision/source map/evidence ledger sao lưu nhất quán và restore test; derived store/cache có thể tái tạo, JSON dump Haystack không thay transaction snapshot. Deletion/revocation phải xóa caches/exports theo policy và báo ledger stale/restricted.
- **Cost:** Apache-2.0 không buộc phí runtime license cho core theo điều kiện; chi phí hạ tầng/model/developer và enterprise chưa đo. `pyproject` liệt kê direct dependencies như networkx, numpy, pydantic, Jinja2, OpenAI SDK, PostHog, httpx, YAML, JSONSchema; đây là source declaration, không phải installed inventory. No new service cho B nếu dùng host port; V2 model có thể local hoặc external với quyền. CPU/RAM/latency/token/TCO A vs B/D đều UNKNOWN; không ngoại suy nhân-ngày. A ít lớp orchestration hơn theo thiết kế, không phải kết quả benchmark.

### 10.1 R2 — Ranh giới vận hành và chi phí theo phương án

| Phương án | Service bổ sung tối thiểu | Dependency phát sinh | Risk/chi phí định tính (chưa đo) |
|---|---|---|---|
| V1 direct core + BCR/SQLite | 0 do Haystack | Không Haystack | L–M; vẫn phải hoàn thiện scanner/sourcemap/catalog/rights |
| V2 direct orchestrator | 0 do orchestration; model tùy | stdlib + backend đã chọn | L–M; code nhánh/async/counterevidence tự giữ, debug dễ khi nhỏ |
| V2 Haystack in-process static | 0 do graph | haystack-ai + lock transitive, wrappers | M; schema/graph/serialization/upgrade; không vector store bắt buộc |
| V2 Agent | model service nếu external/local daemon | graph + provider/weights, tools | M–H; model calls, retry, budget, output validation, privacy; default max steps không phải budget tài chính |
| V2 Haystack + MCP remote/Hayhooks | một hoặc nhiều process/service khi chọn | MCP/HTTP auth/deploy/observability | H; chỉ khi cần integration ngoài process; không chọn để dùng nội bộ |
| V2 reranker direct | 0 nếu local in-process | backend/model weights | M; benchmark đa ngữ, disk/RSS, cache; không cần DB mới |

Khóa egress theo workflow, kể cả warmup/tokenizer/model resolver; không expose remote tool schema động nếu chưa phê duyệt; sanitize output/log; model không quyết quyền publication, ingest hoặc external reading. `HAYSTACK_TELEMETRY_ENABLED=false` trước import không thay firewall; log content tracing tắt; log tool args có thể chứa dữ liệu người dùng, cần redaction, retention. Không dùng untrusted YAML/`unsafe=True`, không chạy MCP stdio command từ model. Host kiểm quyền mỗi request/handle và lại trước remote payload. Rebuild secondary vector cache theo source revision, quyền thay đổi invalidate; không backup vector như raw authority. Với Ollama mặc định localhost cần kiểm địa chỉ server thực, no remote fallback và model load. Với FastEmbed/HanLP/Docling pin model and cache, kiểm weights/license riêng; Apache-2.0 metadata repo không cấp quyền corpus/weights. NOTICE và security advisories toàn dependency chưa audit, **không approval legal**.

## 11. Comparison & Trade-offs

Các file dưới đã truy xuất trực tiếp tại SHA BodhiAtlas trong §2, đọc phần mở đầu/kết luận và các đoạn liên quan; **kết quả báo cáo trước là tài liệu đối chứng, không phải phép đo của P59.**

| Đối chứng | Phát hiện từ báo cáo (DOC) | Hệ quả và kiểm độc lập lần này |
|---|---|---|
| [P03 BCR](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_03_BUDDHISMDOCUMENTS_FOR_AI.md#L13-L31) và [BCR Evidence Engine](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_BCR_EVIDENCE_ENGINE.md#L13-L27) | Có retrieval, resolver/Gate A, cần all-occurrence riêng | E21 mở lại retrieval baseline: `max(limit*5,50)`, ranked[:limit], result_count giới hạn; verifier contract host callback. Haystack không chữa lỗi cắt này. Không chạy BCR |
| [P20 SQLite FTS5](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_20_SQLITE_FTS5_TRIGRAM.md#L3-L15) | SQLite dùng candidate/index, báo cáo thử trên 3.46.1, không phải latest | Giữ SQLite/file store baseline; E22 thử scanner stdlib độc lập, không tái chạy P20 SQL benchmark |
| [P01 RAGFlow](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_01_RAGFLOW.md#L3-L13) | Component/service ingestion/RAG có điều kiện; upstream chưa chạy trong P01 | Platform/service khác class; dùng khi cần ingestion/UI, không mặc định thêm service. Không tái audit RAGFlow |
| [P02 QMD](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_02_QMD_TOBI_QMD.md#L3-L8) | Retrieval ứng viên local, GGUF/model rights chưa xác nhận | Không phải authority; nếu chỉ discovery, so candidate port/qrels, không xếp với OCR |
| [P56 Open Notebook](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_56_OPEN_NOTEBOOK.md#L13-L17) | TRIAL ONLY workspace, không authoritative V1 | Nếu cần notebook UI thật, D có thể nhanh hơn graph; không cần cả hai; không tái chạy upstream |
| [P39-R2 Bang-ha](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_39_BANG_HA_GIAC_NGO_INDEPENDENT_REVIEW.md#L5-L13) | Corpus/import một chiều, adapter, giữ single authority và rights | Port riêng với BCR/host; không thêm Haystack store để chứa bản copy writable; chưa tái audit Bang-ha |
| [P57 book-memex](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_57_BOOK_MEMEX.md#L13-L22) | USE AS COMPONENT có điều kiện; reader/catalog patterns, thiếu scholarly contract | Không biến Document thành Book/Edition/File; giữ source identity và revision độc lập. Không tái chạy book-memex |

**Fastest useful demo:** A cho workflow 3 bước code-only với functions sẵn có (giả thuyết định tính); Haystack có thể nhanh hơn cho demo RAG có branching/components sẵn, nếu package và provider đã được chuẩn bị, nhưng demo này không phải V1. D có thể nhanh hơn nếu demo là notebook UI; không có benchmark để xếp thứ hạng. **Lowest compliant total cost:** A hiện là lựa chọn đầu tư ưu tiên vì không thêm orchestration dependency trong khi core vẫn phải xây/kiểm chứng; chưa khẳng định chi phí tuyệt đối thấp nhất. B đảo lựa chọn khi same gold/rights/reopen, graph có workflow thật, đo giảm tổng công bảo trì (không chỉ số lines). C được nâng lên TRIAL ONLY nếu V2 có use case rõ và host G2 độc lập. Nếu chỉ một call model sau retrieval, tiếp tục direct Python.

### 11.1 R2 — So sánh ở đúng scope và quyết định tiếp theo

| Đích sử dụng | Direct / tài sản hiện hữu | Haystack / integration | Lựa chọn hiện tại và điều kiện đảo |
|---|---|---|---|
| V1 lexical EXACT | BCR retrieval candidates + scanner mới; SQLite | BM25Retriever top_k/DocumentStore | Direct, không replace; Haystack không sửa scanner. |
| Ingest học thuật | Docling direct + parser/source map host | DoclingConverter wrapper | Direct; wrapper serialize custom config gap; chỉ thử nếu đã có graph và preservation pass. |
| Đối chiếu nhiều nguồn | BCR `LocalHost`, stdlib fanout + explicit scope | MultiRetriever/Pipeline | Direct first; graph TRIAL ONLY khi workflow phức tạp và pass P2. |
| Rerank/ngữ nghĩa | direct FastEmbed/ST hoặc QMD P02 candidate provider | integration ranker + graph | Chỉ chọn một backend sau qrels; wrapper không tự cải thiện rank. |
| V2 research workflow | explicit ports + provider calls | Agent/Tools/Router/graph | TRIAL ONLY sau static graph; không agent cho mỗi nguồn; dynamic plan mới cần loop. |
| Workspace UI | BodhiAtlas host hoặc Open Notebook độc lập (P56) | Hayhooks endpoint deployment, không phải notebook/catalog | Không ghép Haystack + RAGFlow + Open Notebook thành một stack; chọn theo workflow. |
| QA | direct oracle + identity qrels | DocumentNDCG/Recall, Faithfulness optional | Học/use evaluator khi có dependency; human G3 không thay. |

Fastest useful demo (giả thuyết, chưa đo): direct `LocalHost.quick` + library adapter + evidence UI; với V2 demo fixed sources, stdlib fanout và một model summary. Nếu muốn nhanh thử agent dynamic, Haystack `create_tool_from_function`/Agent có thể giảm glue, chưa có số đo. Lowest compliant TCO dự kiến direct core + selective reuse; không khẳng định chi phí Haystack cao hơn khi chưa POC. RAGFlow P01/Open Notebook P56 và QMD P02 là đối chứng đúng vai trò; R2 không chạy lại repo đối chứng, không xếp hạng định lượng. Điều kiện đảo: V2 cần branching/async/dynamic tool use thật, graph giảm chi phí bảo trì đo được mà core integrity/ACL/rollback không đổi; nếu không, giữ direct. Không đưa integration vào V1 vì đã có wrapper. Đầu tư kế tiếp ưu tiên test BCR host read-only + scanner/locator, sau đó một workflow V2 cụ thể, không cài cả ecosystem.

## 12. Decision Record for Master Synthesis

| Field | Value |
|---|---|
| target / class | deepset-ai/haystack / Python pipeline orchestrator |
| snapshot / license | v3.5.0 `831b8cfa95a250cea2134091986f734666cce47d` / Apache-2.0 core |
| access_status | source read; runtime blocked; comparator documents read selected sections |
| primary_role | optional V2 orchestration; not catalog/verifier |
| best_fit_v1 | A direct Python + E patterns; no runtime dependency |
| best_fit_v2_v3 | C conditional, evidence port read-only |
| source_fidelity_gate | CODE GAP if native replacement; NOT DEMONSTRATED integration |
| exact_gate | CODE GAP in native BM25 for exhaustive EXACT |
| multilingual_gate | NOT DEMONSTRATED; host owns transform policy |
| coverage_gate | NOT DEMONSTRATED; host manifest |
| rights_security_gate | NOT DEMONSTRATED; telemetry/unsafe/config controls required |
| integration_cost / maintenance_risk | M qualitative for adapter/graph; M qualitative upgrade/deps, not measured |
| recommendation / confidence | DEFER / MEDIUM |
| tests_executed / measured_cost | upstream 0; isolated TC05, partial TC06/07/10; cost UNKNOWN |
| next_poc | TC02/03/12 first if B reconsidered; TC04/05/10 then TC11/13/15 |

```json
{
  "target": "deepset-ai/haystack",
  "class": "python_pipeline_orchestrator",
  "snapshot": {
    "release": "3.5.0",
    "commit": "831b8cfa95a250cea2134091986f734666cce47d",
    "head": "354906c7ceae6f49ce2c26c83ee37abbef64f567",
    "bodhiatlas": "c5dfe50613dfd492407bf1db1061c1cfc9d30e8e",
    "date": "2026-11-25"
  },
  "license": "Apache-2.0 core; dependencies/models/data not cleared",
  "access_status": "CODE_READ_RUNTIME_BLOCKED",
  "primary_role": "optional retrieval/RAG graph, not evidence authority",
  "best_fit_v1": "A_DIRECT_PYTHON_NO_HAYSTACK_RUNTIME",
  "best_fit_v2_v3": "TRIAL_ONLY_OPTIONAL_IN_PROCESS_RESEARCH_ORCHESTRATOR_AND_TOOLS_AFTER_DIRECT_BASELINE",
  "source_fidelity_gate": "CODE_GAP_NATIVE_REPLACEMENT; INTEGRATION_NOT_DEMONSTRATED",
  "exact_gate": "CODE_GAP_NATIVE_BM25",
  "multilingual_gate": "NOT_DEMONSTRATED",
  "coverage_gate": "NOT_DEMONSTRATED",
  "rights_security_gate": "NOT_DEMONSTRATED",
  "integration_cost": "M_QUALITATIVE_NOT_MEASURED",
  "maintenance_risk": "M_QUALITATIVE_NOT_MEASURED",
  "recommendation": "DEFER",
  "confidence": "MEDIUM",
  "tests_executed": {
    "upstream": 0,
    "isolated": [
      "TC05",
      "TC06_PARTIAL",
      "TC07_PARTIAL",
      "TC10_PARTIAL",
      "R2-I01",
      "R2-I02",
      "R2-I03",
      "R2-I04",
      "R2-I05_MODEL",
      "R2-I06_MODEL",
      "R2-I07_DIAGNOSTIC"
    ]
  },
  "measured_cost": null,
  "next_poc": [
    "R2-P0",
    "R2-P1",
    "R2-P2",
    "R2-P3_IF_NEEDED",
    "R2-P4_IF_NEEDED",
    "R2-P5_IF_NEEDED",
    "R2-P6"
  ],
  "revision": "R2",
  "integration_snapshot": "4c0aa2ba2796d1c337412f6551b534c8c1efb0c5",
  "bcr_head": "dfdd3cbb79e3dbfb49a855702fa00e4bad3b3410",
  "hayhooks_snapshot": "82f71a6eb31236da47ed6cc4704f3bb41ff65598",
  "asset_reuse_priority": [
    "BCR_LOCALHOST_AND_GATE_A_CONDITIONAL",
    "HOST_TYPED_PORTS_AND_IDENTITY_QRELS",
    "RRF_AND_CONTEXT_PATTERN",
    "HAYSTACK_V2_GRAPH_AND_TOOLS_TRIAL_ONLY",
    "DOCLING_DIRECT_BACKEND_IF_PARSER_POC_PASSES"
  ],
  "upstream_integration_tests_executed": 0,
  "runtime_blocker": "NO_HAYSTACK_PACKAGE_AND_GIT_DNS_BLOCKED"
}
```

**R2 update:** `DEFER` runtime V1 remains primary; optional V2 graph/Agent is `TRIAL ONLY` (role-specific). E25–E41 and R2-P0–P6 supplement the original record. No additional production gate passed.

**Top 5 strengths:** custom component sockets không bắt buộc Document; graph/branch/loop/async; built-in ranked retrieval/join; serialize/config/allowlist; model/provider ecosystem và evaluation cho V2. **Top 5 blockers:** top-K ≠ all-occurrence; Document identity/clean/split không phải source map; generated references không G2; telemetry/config/rights/backup chưa nghiệm thu; dependency/TCO/rollback và BCR integration chưa đo. Nâng quyết định khi các hard gates pass ở scope và workflow thật giảm complexity; hạ xuống REJECT cho vai trò V1 orchestrator nếu phải đổi authority, lưu writable copy, không giữ identity/rights/error hoặc không gỡ được framework. Không lấy kết quả test cô lập làm PASS production.

## 13. Appendix — Inventory, logs, script, câu hỏi mở

### 13.1. Inventory đã mở

Snapshot tree `0645e123392315c8e284a371a78e7d11bc8f4f4a` của v3.5.0 truy xuất qua GitHub API recursive, `truncated=false`. Các file sau đã lấy nội dung và xem các đoạn liên quan; không tuyên bố audit mọi dòng của file dài. 26 file Haystack được liệt kê trong inventory R1 (22 source/config/license + 4 test); R2 bổ sung inventory riêng tại §13.5, gồm:

| Nhóm | File ghim |
|---|---|
| Package/license | [pyproject.toml](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/pyproject.toml), [LICENSE](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/LICENSE) |
| Component/pipeline | [component.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/component/component.py), [base.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/pipeline/base.py), [pipeline.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/pipeline/pipeline.py), [serialization.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/serialization.py), [serialization_security.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/core/serialization_security.py) |
| Data | [document.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/dataclasses/document.py), [answer.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/dataclasses/answer.py) |
| Store | [document_store.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/document_stores/in_memory/document_store.py), [document_writer.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/writers/document_writer.py) |
| Processing | [pypdf.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/converters/pypdf.py), [document_splitter.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/preprocessors/document_splitter.py), [document_cleaner.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/preprocessors/document_cleaner.py) |
| Retrieval/router | [bm25_retriever.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/retrievers/in_memory/bm25_retriever.py), [document_joiner.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/joiners/document_joiner.py), [conditional_router.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/routers/conditional_router.py) |
| Answer/eval/provider | [answer_builder.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/builders/answer_builder.py), [document_recall.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/evaluators/document_recall.py), [openai.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/components/generators/chat/openai.py) |
| Privacy | [_telemetry.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/telemetry/_telemetry.py), [tracer.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/haystack/tracing/tracer.py) |
| Test source, NOT RUN | [test_async_pipeline.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/core/pipeline/test_async_pipeline.py), [test_document.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/dataclasses/test_document.py), [test_document_splitter.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/components/preprocessors/test_document_splitter.py), [test_answer_builder.py](https://github.com/deepset-ai/haystack/blob/831b8cfa95a250cea2134091986f734666cce47d/test/components/builders/test_answer_builder.py) |

Path `haystack/core/pipeline/async_pipeline.py` không tồn tại tại release kiểm (404); không tính vào inventory. README upstream dùng mô tả chính thức PyPI, không tính là file Git đã mở. NOTICE/ByteStream và security sâu chưa audit. Agent/Tools, một số integration và test source đã kiểm bổ sung tại §13.5; các provider/model còn lại chưa audit.

**BodhiAtlas:** [PRD](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/PRD.md), [V1 Core](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/V1_CORE_FOUNDATION.md), [Academic Risks](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/docs/ACADEMIC_RISKS_AND_VERIFICATION.md), [Research README](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/README.md), [Report Template](https://github.com/quoctran-2608/bodhi-atlas/blob/c5dfe50613dfd492407bf1db1061c1cfc9d30e8e/research/technology-assessments/REPORT_TEMPLATE.md) và tám report link tại §11. Tất cả tồn tại tại snapshot; không có file đối chứng bị thiếu. BCR hai file E21 và LocalHost/source_resolvers R2 mở trực tiếp tại baseline; không đọc toàn corpus hoặc code mọi resolver.

### 13.2. Log rút gọn thực tế

```text
$ git ls-remote https://github.com/deepset-ai/haystack.git HEAD
fatal: unable to access 'https://github.com/deepset-ai/haystack.git/': Could not resolve host: github.com
$ git ls-remote https://github.com/quoctran-2608/bodhi-atlas.git HEAD
fatal: unable to access 'https://github.com/quoctran-2608/bodhi-atlas.git/': Could not resolve host: github.com
$ python -c "import importlib.util; print(importlib.util.find_spec('haystack'))"
None
$ python /tmp/p59.py
python 3.13.5 sqlite 3.46.1 os Linux-6.18.57-x86_64-with-glibc2.41 machine x86_64
fixture rows 24 sha256 b936be51a4518c52ca8c86b935fb9efaff08438024867a5cabed83b5581639fb
literal gold 25 actual 25 precision=1 recall=1 (fixture only)
top_k model 10 distinct matching records 21 occurrences 25
cross-boundary, Unicode literal, trusted byte negatives: PASS isolated
```

Không có upstream stdout/stderr hoặc measured latency, token, CER, ranked nDCG. Pip cache không đọc được vì cache disabled/permissions; không suy rằng wheel không tồn tại ở mọi nơi. Không chứa credentials hoặc corpus thật.

### 13.3. Script đã chạy (TESTED-ISOLATED)

Lưu nội dung sau thành `p59.py`, chạy `python p59.py` với Python 3.13.5 (stdlib). Oracle hard-coded trước scan, input tự tạo không bản quyền bên ngoài; cross-boundary assertion chỉ minh họa concatenation policy, không phải implementation source map. `verify` stub cố ý giới hạn byte source, không là G2 production; không kiểm raw PDF, không bảo đảm ngữ cảnh.

```python
import hashlib,json,platform,sqlite3,sys,re
from pathlib import Path
# Fixture and gold fixed before scan: 24 records, 20 public single hits, plus 4 special.
rows=[(f'p{i:02}','A','r1','public','苦 x') for i in range(20)] + [('multi','A','r1','public','苦 苦 苦 苦 苦'),('b','B','r1','public','not 苦'),('restricted','A','r1','restricted','苦'),('unicode','A','r1','public','無常 无常 anattā anatta đ d ཆོས་')]
raw=json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode(); sha=lambda b:hashlib.sha256(b).hexdigest()
gold={(f'p{i:02}',0) for i in range(20)}|{('multi',i) for i in (0,2,4,6,8)}
def scan(q):
 assert q
 return {(id,i) for id,e,r,rights,t in rows if e=='A' and rights=='public' for i in range(len(t)) if t.startswith(q,i)}
actual=scan('苦'); assert actual==gold
# top_k truncation model, NOT BM25 upstream
ranked=sorted({id for id,_ in actual})[:10]; assert len(ranked)==10 and len(gold)==25
# independently declared concatenation policy
assert ('無'+'常').find('無常')==0 and '無'.find('無常')==-1 and '常'.find('無常')==-1
assert scan('無常')=={('unicode',0)} and scan('无常')=={('unicode',3)}
# trusted byte source separate from claim, no actual PDF locator
trusted={'A':b'not permitted','B':b'permitted'}
def verify(e,h,quote,start):
 b=trusted.get(e);return b is not None and sha(b)==h and b[start:start+len(quote)]==quote
assert verify('A',sha(trusted['A']),b'not permitted',0)
assert not verify('A',sha(trusted['B']),b'permitted',0)
assert not verify('A',sha(trusted['A']),b'permitted',0)
print('python',sys.version.split()[0],'sqlite',sqlite3.sqlite_version,'os',platform.platform(),'machine',platform.machine())
print('fixture rows',len(rows),'sha256',sha(raw))
print('literal gold',len(gold),'actual',len(actual),'precision=1 recall=1 (fixture only)')
print('top_k model',len(ranked),'distinct matching records',len({id for id,_ in actual}),'occurrences',len(actual))
print('cross-boundary, Unicode literal, trusted byte negatives: PASS isolated')
```

### 13.4. Nguồn ngoài và vấn đề chưa giải quyết

- [PyPI stable 3.5.0](https://pypi.org/project/haystack-ai/3.5.0/), [2.31.1](https://pypi.org/project/haystack-ai/2.31.1/), [legacy farm-haystack](https://pypi.org/project/farm-haystack/), [Migration Guide](https://docs.haystack.deepset.ai/docs/migration).
- [Pipeline documentation](https://docs.haystack.deepset.ai/docs/pipelines), [DocumentSplitter](https://docs.haystack.deepset.ai/docs/documentsplitter), [core integrations](https://github.com/deepset-ai/haystack-core-integrations), [Enterprise docs](https://docs.cloud.deepset.ai/docs/getting-started). Docs live hỗ trợ định vị code, không thay pinned release. Xem ledger cho permalink code.
- Cần xác nhận release wheel hash/attestation, lock transitive và NOTICE/dependency licenses; không kiểm chứng provenance wheel tại runtime. Chưa đánh giá CVEs toàn inventory, concurrency side effects, tokenizer trên toàn corpus, actual BCR revision compatibility, rights dataset/model, reader reopen after restore, TC14 provider cost. Không có số đo TCO để tuyên bố B rẻ hơn A.

**Khác với báo cáo cũ:** P01/P56 xem nền tảng RAG/workspace; P03/P20 xét retrieval và verifier/index; P39/P57 xét identity/corpus/reader. P59 giới hạn vào *giá trị điều phối* của framework và chi phí so direct calls, không tạo authority mới. Điểm mới là xác minh major 3.x, unified sync/async execution, allowlist security, default telemetry và giới hạn ID/offset/citation tại release 3.5.0; đối chứng lại BCR baseline, chạy một oracle nhỏ độc lập. Không thay kết luận các report cũ bằng kết quả chưa chạy.

**Điều kiện kết thúc:** đủ 13 phần, 15 dòng C, 12 giả thuyết và 15 TC; có map T01–T16, 6 gates, ledger ghim code và JSON. Phần source review có thể dùng master synthesis; phần runtime chỉ là kết quả cô lập + kế hoạch, không đạt nghiệm thu upstream. Đầu tư kế tiếp chỉ vào direct ports và scanner/verifier chuẩn; nếu một workflow thật cần orchestration, thực hiện ba nhóm POC đã định, không cài tất cả ứng viên. Không có thay đổi repo.


### 13.5. R2 — Inventory mới, log và script tái lập

14 file Haystack core/test bổ sung đã lấy nội dung và đọc vùng liên quan: `agent.py`, `tool_calling.py`, `component_tool.py`, `from_function.py`, `pipeline_tool.py`, `state.py`, `tool.py`, `sentence_window_retriever.py`, `multi_retriever.py`, `document_ndcg.py`, `faithfulness.py`, `utils/misc.py`, `test_tool_calling.py`, `test_agent_hooks.py` (permalinks E25–E31). 11 file integrations: bốn manifest Docling/MCP/FastEmbed/Ollama, converter Docling, hai MCP tool files, FastEmbed ranker, Ollama chat generator, ST similarity ranker, HanLP splitter (E34–E40). Hai file Hayhooks: README, deploy route (E39). BCR thêm `local_host.py`, `source_resolvers.py`, đọc lại `verification.py` ở full length (E32–E33); không đếm verifier hai lần vào inventory unique. Các tree entries khác chỉ được thấy tên; không nhận đã đọc code. Không kiểm toàn bộ repo từng dòng hoặc chạy test suite.

**Log thực tế R2 — runtime:**

```text
$ python -V
Python 3.13.5
$ python -m pip show haystack-ai
WARNING: Package(s) not found: haystack-ai
$ git ls-remote https://github.com/deepset-ai/haystack HEAD
fatal: unable to access 'https://github.com/deepset-ai/haystack/': Could not resolve host: github.com
```

**Log thực tế R2 — fixture:**

```text
$ python /tmp/p59r2.py
python 3.13.5 platform Linux-6.18.57-x86_64-with-glibc2.41
fixture_sha256 d38d3472a7434df4431c93c20b523f2a05e9e8f640b15a9e5753b571748d8dae
direct and stdlib async fanout: expected=3 actual= 3 PASS
synthetic timeout: expected PARTIAL/2 actual PARTIAL 2 PASS
negative oracle expected/actual: [('DENIED', 'DENIED'), ('REJECTED', 'REJECTED'), ('STALE', 'STALE'), ('REJECTED', 'REJECTED'), ('REJECTED', 'REJECTED')]
state override model: restricted wins (NOT upstream); closure denies restricted: PASS
same-quote dedup: naive=1 scoped=2; substring does not imply claim: PASS
```

**Script đã chạy — TESTED-ISOLATED:**

```python
# Own synthetic fixture; no Haystack/BCR package imported. Independent expected output fixed before implementation.
import asyncio, hashlib, json, platform, sys, time
from dataclasses import dataclass
from statistics import median
raw = {
 'pali-A-r1': ('pali','A','r1','public','anattā. not self.'),
 'pali-B-r1': ('pali','B','r1','public','anattā. self.'),
 'han-A-r1': ('han','A','r1','public','無常。非我。'),
 'modern-A-r1': ('modern','A','r1','restricted','private note'),
}
# Each tuple = (file, edition, revision, start, end, expected quote); independent hand-written oracle.
GOLD = {('pali-A-r1','A','r1',0,6,'anattā'),('pali-B-r1','B','r1',0,6,'anattā'),('han-A-r1','A','r1',0,2,'無常')}
ALLOWED = frozenset({'pali-A-r1','pali-B-r1','han-A-r1'})
def digest(s): return hashlib.sha256(s.encode()).hexdigest()
fixture_sha=digest(json.dumps(raw,ensure_ascii=False,sort_keys=True,separators=(',',':')))
@dataclass(frozen=True)
class Candidate:
 file: str; edition: str; revision: str; start: int; end: int; quote: str; sha: str
 def key(self): return (self.file,self.edition,self.revision,self.start,self.end,self.quote)
# Private host closure, not a model argument. Explicit trusted scope and immutable fixture.
def retrieve(corpus, query):
 out=[]
 for file,(c,e,r,rights,text) in raw.items():
  if c!=corpus or file not in ALLOWED or not query: continue
  for i in range(len(text)):
   if text.startswith(query,i): out.append(Candidate(file,e,r,i,i+len(query),query,digest(text)))
 return out

def verify(c):
 if c.file not in ALLOWED or c.file not in raw: return 'DENIED'
 _,e,r,_,text=raw[c.file]
 if c.revision!=r: return 'STALE'
 if c.edition!=e or c.sha!=digest(text) or not 0<=c.start<c.end<=len(text) or text[c.start:c.end]!=c.quote: return 'REJECTED'
 return 'MATCHED_FIXTURE' # not VERIFIED or G2

def direct(): return {c.key() for corpus,q in [('pali','anattā'),('han','無常')] for c in retrieve(corpus,q) if verify(c)=='MATCHED_FIXTURE'}
async def fanout(fail=False):
 async def branch(corpus,q):
  if fail and corpus=='han': raise TimeoutError('synthetic failure')
  return retrieve(corpus,q)
 results=await asyncio.gather(branch('pali','anattā'),branch('han','無常'),return_exceptions=True)
 ok={c.key() for batch in results if not isinstance(batch,BaseException) for c in batch if verify(c)=='MATCHED_FIXTURE'}
 return ('PARTIAL' if any(isinstance(x,BaseException) for x in results) else 'COMPLETE_FIXTURE',ok)
# Negative oracle predetermined.
negatives=[(Candidate('modern-A-r1','A','r1',0,7,'private',digest('private note')),'DENIED'),(Candidate('pali-A-r1','B','r1',0,6,'anattā',digest(raw['pali-A-r1'][4])),'REJECTED'),(Candidate('pali-A-r1','A','r0',0,6,'anattā',digest(raw['pali-A-r1'][4])),'STALE'),(Candidate('pali-A-r1','A','r1',0,6,'anattā','bad'),'REJECTED'),(Candidate('pali-A-r1','A','r1',8,16,'self.',digest(raw['pali-A-r1'][4])),'REJECTED')]
assert direct()==GOLD
assert asyncio.run(fanout())==('COMPLETE_FIXTURE',GOLD)
status, partial=asyncio.run(fanout(True)); assert status=='PARTIAL' and partial=={x for x in GOLD if x[0].startswith('pali')}
assert [verify(c) for c,_ in negatives]==[x for _,x in negatives]
# Source-derived simplified model of Haystack state precedence, not execution of upstream.
def state_merge(args, state):
 out=dict(args)
 if 'scope' not in out: out['scope']=state['scope']
 return out
assert state_merge({'scope':'restricted'},{'scope':'public'})['scope']=='restricted'
# Model of ID-keyed fusion collapse; host keys include file/edition/revision/span.
assert len({c.quote:c for c in retrieve('pali','anattā')})==1
assert len({c.key():c for c in retrieve('pali','anattā')})==2
# Distinguish substring vs claim: actual text includes 'not self', never infer support from substring.
assert 'self' in raw['pali-A-r1'][4] and 'not self' in raw['pali-A-r1'][4]
print('python',sys.version.split()[0], 'platform',platform.platform())
print('fixture_sha256',fixture_sha)
print('direct and stdlib async fanout: expected=3 actual=',len(direct()),'PASS')
print('synthetic timeout: expected PARTIAL/2 actual',status,len(partial),'PASS')
print('negative oracle expected/actual:',[(expected,verify(c)) for c,expected in negatives])
print('state override model: restricted wins (NOT upstream); closure denies restricted: PASS')
print('same-quote dedup: naive=1 scoped=2; substring does not imply claim: PASS')
```

### 13.6. Tự kiểm hoàn tất R2 và điểm chưa thể nghiệm thu

R2 giữ đủ 13 phần, C01–C15, G1–G6, H01–H12, TC01–TC15 và map T01–T16 từ R1, mở rộng riêng R2-I01–I07 và R2-P0–P6; quyết định JSON cập nhật; nguồn pinned; không chỉnh GitHub. Những bổ sung quan trọng so R1: xác nhận lại BCR HEAD và PRD/Core/Risk blob; call path BCR thực tế; Agent/state/Tools và rủi ro ACL; ranked fusion/context/evaluator; 11 integration files + ecosystem tree; Docling config-loss/network trap; module-level reuse matrix, adapter plan, cost/rollback và oracle bổ sung.

**Chưa hoàn tất nghiệm thu:** upstream Haystack/BCR/Docling/MCP/Ollama/FastEmbed chưa chạy, không có lock packages/model/rights, không có benchmark thật, chưa thử PDF/EPUB locator hoặc full corpus. R2 có thể dùng làm nguồn phân tích lựa chọn công nghệ/định vị POC cho master synthesis, **không** đủ chứng cứ để ADOPT runtime hay phê duyệt production. Để hoàn tất thực nghiệm cần môi trường có wheelhouse và fixture BCR được phép; chạy R2-P0/P1/P2 trước, chỉ mở rộng P3–P5 khi một use case cần. Các kết luận về TCO là định tính, actual=null cho các POC chưa chạy. Không tạo báo cáo phụ, không thay đổi repository.
