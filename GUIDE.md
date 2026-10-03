# Lộ trình Day 5 — 240 phút

Đọc [lab-guide.html](lab-guide.html) nếu bạn cần ảnh minh họa CVAT từng bước. Tên lớp và quy tắc trong [guideline-mini-sheet.md](guideline-mini-sheet.md) áp dụng cho tất cả; file `classes.json` của mỗi task quyết định tên lớp chính xác.

| Phút | Việc cần làm | Bằng chứng giữ lại |
| ---: | --- | --- |
| 0–15 | Mở CVAT, đọc quy tắc, tạo task Easy | Nhìn đủ 3 ảnh và đúng 5 lớp |
| 15–45 | Easy semantic: tô vùng, tự QC, Save và export | `easy_semantic.zip` |
| 45–110 | Medium instance: từng vật một mask; object đầu tự vẽ trước gợi ý | `medium_instance.zip`; một quyết định trong REPORT |
| 110–120 | Nghỉ | Giữ hai ZIP an toàn |
| 120–175 | Hard panoptic: stuff + từng thing, tự QC và export | `hard_panoptic.zip` |
| 175–185 | Nghỉ; ground truth ba tier được phát từ phút 180 theo hướng dẫn lớp | Chưa đưa đáp án vào fork |
| 185–215 | Sáu checkpoint; người xong sớm có thể chạy scorer ba tier | ZIP trạm đã làm; kết quả tự đánh giá nếu có |
| 215–235 | Kiểm export, ghi lỗi, hành động sửa và ba ca chưa chắc vào report | `REPORT.md` |
| 235–240 | Save lần cuối, kiểm ZIP và report, ghi lỗi cần báo coach | Bài sẵn để push lên fork |

Các mốc là **timebox thực hành**, không phải hạn nộp ngay trong lớp hay lý do bỏ qua Save/QC. Fork repo đề bài public, push `REPORT.md` và các ZIP đã làm lên fork của bạn, rồi nộp **link fork trên VLearn trong vòng 24 giờ sau buổi lab**. Công cụ chấm riêng chạy sau cửa sổ nộp. Nếu không đủ giờ, ghi phần đã hoàn thành và phần còn thiếu trung thực; không có bài tập về nhà bắt buộc. Bonus giờ cuối có hai mức 10/20 theo [rubric](RUBRIC.md), điểm ghi nhận vẫn tối đa 100.

## Easy: semantic — 20 điểm

Ba ảnh ở `data/tiers/easy_semantic/images/`. Semantic hỏi “pixel thuộc loại vùng nào?”; lớp là `road`, `sidewalk`, `building`, `vegetation`, `sky`. Dùng Brush/Polygon để phủ vùng nhìn thấy, đặc biệt kiểm ranh `road`–`sidewalk`. Không gộp hai lớp chỉ vì màu ảnh gần giống. Save và export **Segmentation mask 1.1**.

## Medium: instance — 32 điểm

Ba ảnh ở `data/tiers/medium_instance/images/`; lấy sáu tên lớp từ `classes.json`. Mỗi vật đếm được là một mask riêng. Trước khi dùng gợi ý tự động, tự vẽ **một object** rồi ghi ảnh, vị trí, class, quy tắc biên trong report. Nếu dùng gợi ý sau đó, ghi một lỗi hoặc lý do giữ đề xuất. Không có gợi ý vẫn làm bình thường bằng Brush/Polygon. Kiểm vật thiếu/thừa, gộp/tách nhầm, biên ăn nền rồi export **COCO 1.0**.

## Hard: panoptic — 30 điểm

Hai ảnh ở `data/tiers/hard_panoptic/images/`. Panoptic cần cả **stuff** (`road`, `sky`…) và từng **thing** (`car #1`, `car #2`…). Dùng đúng 12 lớp trong `classes.json`. Vẽ từ xa tới gần, kiểm chồng lấn và vùng chưa phủ. Pixel không thể quyết định thì ghi ca mơ hồ; đừng bịa class. Save và export **COCO 1.0**. Định dạng này là hợp đồng của starter; nếu CVAT lớp không giữ mask đúng khi export, báo coach thay vì sửa ZIP bằng tay.

## Sáu checkpoint — 18 điểm

Mỗi checkpoint là một ảnh và **3 điểm**: `cp1_holes` (lỗ/kính), `cp2_slice` (hai vật sát nhau), `cp5_occlusion` (vật bị che), `cp3_thin` (nét mảnh), `cp4_curb` (bó vỉa), `cp6_coverage` (phủ vùng). Mở `classes.json` riêng của mỗi trạm; đừng dùng class list của task khác. Task instance export COCO 1.0; task semantic export Segmentation mask 1.1.

## Tự QC rồi nộp

Theo thứ tự: đúng ảnh → đúng loại segmentation → đúng tên lớp → đủ số object/vùng → biên → Save → ZIP đúng format. Một lỗi thực tế và cách sửa phải xuất hiện trong `REPORT.md`. Trên fork, bật **Actions** một lần; khi upload ZIP vào `submissions/` và Commit, **Day 5 self-check** tự kiểm cấu trúc. Sau khi ground truth ba tier được công bố qua release chính thức, action tự hiện điểm phản hồi **/82** trong Summary; bạn có thể sửa/export/push lại để xem điểm mới. [Hướng dẫn từng nút và cách chạy script trên máy nếu cần](docs/SELF_SCORING.md). [Notebook Colab](notebooks/README.md) vẫn là tùy chọn; action không tự chứng nhận PASS hoặc top 3.
