# CVAT local — vào lớp, vẽ, lưu, xuất

Địa chỉ CVAT do lớp cung cấp; nếu chạy trên chính máy của bạn thường là `http://localhost:8080`. Dùng Chrome hoặc Edge. Nếu không vào được, báo coach với màn hình lỗi và thời điểm, không tự cài một stack CVAT khác giữa giờ lab.

1. **Tasks → Create new task.** Mỗi mục trong `data/manifest.json` là một task riêng. Đặt tên đúng mã task; tải đúng ảnh trong `data/tiers/<task>/images/` hoặc `data/checkpoints/<task>/images/`.
2. Trong **Labels**, chọn một trong hai cách: **Raw** → dán toàn bộ nội dung `cvat-labels.json` của đúng task → **Done**; hoặc **Constructor → Add label** để thêm từng tên từ `classes.json`. `classes.json` chứa metadata của bài lab, **không dán nguyên file vào Raw**. Ví dụ `traffic sign` có dấu cách; không tự đổi thành `traffic_sign`. Kiểm tên/số label rồi mới Submit. Nếu task đã có annotation, không dán đè Raw; báo coach khi cần sửa nhãn.
3. Mở Job, chọn Brush/Polygon, vẽ mask; dùng danh sách Objects để kiểm class và số object. Bấm **Save** rồi đổi ảnh và kiểm lại.
4. Menu góc trái Job → **Export job dataset**. Semantic xuất `Segmentation mask 1.1`; instance và panoptic xuất `COCO 1.0` theo hợp đồng của starter. Đặt tên ZIP bằng mã task.
5. Nếu format không xuất hiện hoặc export lỗi, giữ dữ liệu Save trên CVAT và báo coach; không tự thay bằng format khác rồi coi là tương đương.

SAM là **tùy chọn, không bảo đảm có** trên CVAT local. Không thấy SAM là bình thường; dùng Brush/Polygon. Nếu Intelligent Scissors xuất hiện, có thể dùng để gợi ý biên rồi tự kiểm. Ảnh thao tác từng bước trong [lab-guide.html](lab-guide.html).
