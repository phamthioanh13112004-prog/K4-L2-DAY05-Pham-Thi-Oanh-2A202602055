# Dữ liệu bài Day 5

Bộ này sao chép nguyên **3 ảnh Easy, 3 ảnh Medium, 2 ảnh Hard và 6 ảnh checkpoint**, cùng các `classes.json` và `manifest.json`, từ [starter Day 5](https://github.com/VinUni-AI20k/Day5-Segmentation-Data-Student) commit `3bff13d`. Không dùng bộ 5 ảnh thử nghiệm làm bài chấm.

Starter ghi nguồn ảnh là BDD100K cho semantic và COCO val2017/COCO Panoptic cho instance, panoptic; xem tài liệu nguồn trong starter để kiểm điều kiện sử dụng. Chỉ dùng trong phạm vi khóa học đã được người phụ trách cho phép. `groundtruth/` không có trong repo học viên. Không tải script tạo lại dữ liệu, đáp án hoặc cache nhãn lên bài nộp.

Mỗi task có `images/`, `classes.json` và `cvat-labels.json` riêng. `classes.json` là metadata gốc cho tên class/chấm bài, **không dán vào ô Raw của CVAT**. Muốn tạo labels nhanh, mở `cvat-labels.json` cùng task, sao chép toàn bộ mảng JSON và dán vào **Labels → Raw** trước khi tạo task; hoặc dùng Constructor để thêm từng tên trong `classes.json`. File `manifest.json` quy định task, loại và trọng số.
