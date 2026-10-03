# Nộp bài Day 5 — fork → push → VLearn

Repo đề bài mở public. Bạn **fork về tài khoản GitHub của mình**, làm bài với CVAT local, đưa bài lên fork và nộp **link fork trên VLearn trong vòng 24 giờ sau buổi lab**. Tool chấm riêng chạy sau cửa sổ nộp. Lab thực hành 240 phút trên lớp; không có bài tập về nhà bắt buộc. Reference của ba tier được phát trong 60 phút cuối để tự đánh giá; bonus 10/20 theo thông báo lớp nhưng điểm ghi nhận không vượt 100. Notebook và lệnh kiểm cấu trúc không phải điều kiện nộp cốt lõi.

## 1. Xuất đúng format và đặt tên

| Task | Format trong CVAT | File sau khi đổi tên |
| --- | --- | --- |
| `easy_semantic` | Segmentation mask 1.1 | `easy_semantic.zip` |
| `medium_instance` | COCO 1.0 | `medium_instance.zip` |
| `hard_panoptic` | COCO 1.0 | `hard_panoptic.zip` |
| `cp1_holes`, `cp2_slice`, `cp5_occlusion` | COCO 1.0 | `<mã_task>.zip` |
| `cp3_thin`, `cp4_curb`, `cp6_coverage` | Segmentation mask 1.1 | `<mã_task>.zip` |

Đặt tất cả ở `submissions/` trong **fork của bạn**. Giữ nguyên nội dung bên trong mỗi ZIP. Nếu chưa xong trạm nào, không tạo ZIP rỗng; ghi rõ vào report.

## 2. Điền một report

Mở [`REPORT.md`](../REPORT.md) đã có sẵn ở gốc fork và điền mã học viên, task hoàn thành, một quyết định tự vẽ trước gợi ý, một lỗi đã sửa và ba ca cân nhắc. Nếu cần hiểu cách điền, xem [mẫu có giải thích](../reports/REPORT_TEMPLATE.md). Không tự điền điểm. Nếu export thất bại, ghi tên task, trạng thái đã Save trên CVAT và báo coach.

## 3. Tự kiểm tùy chọn

Từ thư mục gốc repo, chạy:

```bash
python3 scripts/inspect_submissions.py --dir submissions
```

`OK` chỉ có nghĩa ZIP đọc được và khớp hợp đồng ảnh/class/mask. `THIẾU` nghĩa chưa có ZIP; đó không phải lỗi kỹ thuật. `LỖI` cần sửa trong CVAT, Save và export lại. Với COCO, dòng `annotations` là số mask đã nộp, **không phải số object đúng**. Với panoptic, phải tự xem lại phủ vùng/chồng lấn trong CVAT. Bạn cũng có thể [upload một notebook lên Colab](../notebooks/README.md) hoặc mở bằng Jupyter trên máy.

Khi push ZIP lên fork, **Day 5 self-check** trong tab Actions tự kiểm cấu trúc. Sau khi ground truth ba tier được phát qua release chính thức, cùng workflow sẽ [hiện điểm tự đánh giá trong Summary](SELF_SCORING.md) mà không cần cài Python. Bật Actions một lần trên fork; nếu muốn chạy lại mà chưa sửa file, chọn **Run workflow**. Script trên máy vẫn là dự phòng. Chỉ gói reference chính thức mới được dùng; không đưa đáp án lên fork hay Colab công khai. Nếu action không chạy, báo coach trong buổi lab, vẫn giữ ZIP/report và nộp bài cốt lõi.

## 4. Đưa bài lên fork và nộp link

Không cần dòng lệnh Git: mở `REPORT.md` ngay trong fork → bấm biểu tượng bút chì **Edit** → điền bài rồi **Commit changes**. Mở `submissions/` → **Add file → Upload files** → upload từng ZIP đúng tên và Commit. Mở lại fork, kiểm report đã điền và các ZIP đã hiện, rồi dán **URL của fork cá nhân** vào bài nộp Day 5 trên VLearn. Đừng dán URL repo đề bài của lớp. Nếu dùng Git trên máy, commit và push các file tương tự; kết quả trên fork phải giống nhau.

Lệnh đóng thêm một ZIP duy nhất dưới đây là **tùy chọn để lưu/chuyển**, không thay cho `REPORT.md` và các ZIP riêng trên fork:

```bash
python3 scripts/package_submission.py --learner-id D5_012
```

Lệnh lấy các ZIP ở `submissions/`, tạo `day5-D5_012.zip` gồm `REPORT.md`, các ZIP trong thư mục `exports/` **bên trong gói cuối**, và `manifest.json` có SHA-256. Gói vẫn cho phép task chưa kịp, nhưng report phải giải thích. Không upload thêm bản sao ảnh gốc, file reference hay file tạm notebook lên fork.

Tool chấm của lớp hoạt động riêng sau hạn 24 giờ; lệnh tự kiểm ZIP chỉ báo cấu trúc, còn scorer với reference trong giờ cuối cho phản hồi để sửa. Bản tự đánh giá tối đa 82 điểm cho ba tier không thay điểm checkpoint hoặc tự quyết định bonus. Làm bài qua nút Upload files và làm bằng Git đều theo cùng một rubric 100 điểm.
