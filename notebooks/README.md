# Notebook Day 5 — một file cho Colab hoặc Jupyter

Lộ trình vẫn là 9 task, 14 ảnh và 100 điểm trong 240 phút. [Mở một notebook duy nhất](day5-segmentation-tu-kiem.ipynb) để đi từ nhận ảnh → QC semantic → QC instance → QC panoptic → kiểm nộp. Notebook không thêm bài, không mở đáp án, không bắt bạn viết code. Nếu mới dùng máy tính, cứ theo `lab-guide.html` và CVAT; coach có thể dùng notebook để hỗ trợ kiểm export.

## Dùng trên Google Colab

1. Nếu đang xem `lab-guide.html` trên máy, bấm **Tải một file notebook**. Nếu đang xem GitHub, mở `day5-segmentation-tu-kiem.ipynb` rồi bấm **Download raw file**. Vào Google Colab → **File → Upload notebook** và chọn file vừa tải.
2. Chạy ô **BƯỚC 0 · Thư viện cần dùng**. Notebook cần Python 3.10+ và IPython để hiện ảnh; ô này kiểm tra, chỉ tự cài IPython nếu thiếu. Không cần cài `requirements.txt`, SAM, NumPy, Pillow hay pycocotools để dùng notebook tự kiểm. Đợi dòng `SẴN SÀNG` rồi mới tiếp tục.
3. Ở ô **BƯỚC 1**, dán URL gốc **fork của bạn** vào `FORK_URL = "..."` rồi chạy. Notebook tự tải ảnh, manifest và script tự kiểm từ fork công khai. Không cần upload cả repo. Đừng dán mật khẩu/token. Nếu fork chưa public hoặc Colab không truy cập được GitHub, dùng Jupyter trên bản repo đã tải về máy.
4. Nếu ZIP CVAT đã push vào `submissions/` trên fork, chạy tiếp với `UPLOAD_ZIPS = False`. Nếu chưa push, ở **BƯỚC 2** đổi thành `True`, chọn các ZIP tên đúng mã task rồi tiếp tục. File upload chỉ nằm tạm trong phiên Colab: **vẫn phải đưa ZIP và report lên fork để nộp**.
5. Chạy các ô theo thứ tự. Mỗi phần giải thích `CHƯA XUẤT`, `LỖI`, `OK`, `KIỂM`; các dòng này chỉ kiểm cấu trúc hoặc hiện số mask đã nộp. Xem lại CVAT bằng mắt để sửa. Cuối cùng nộp **link fork trên VLearn**, không nộp notebook hay ZIP Colab.

Nếu dùng JupyterLab/VS Code trên máy, mở notebook từ gốc repo hoặc thư mục `notebooks/`, chạy từ trên xuống bằng Shift+Enter; không cần điền `FORK_URL`. Môi trường notebook cần Python 3.10+ và Jupyter/IPython; công cụ CLI `scripts/inspect_submissions.py` chỉ cần Python 3.10+ chuẩn. Không cần notebook để nhận điểm. Không đưa dữ liệu cá nhân hoặc dữ liệu không được phép lên dịch vụ ngoài.

Không notebook nào tính IoU hoặc điểm khi chưa có reference. Thiếu/thừa object không thể xác định chỉ từ file của bạn: con số được in ra là **số object đã nộp**, để bạn kiểm lại bằng mắt. Nếu bạn so hai export, `annotation_id` trong COCO không phải định danh ổn định và IoU chỉ là độ giống nhau, không phải correctness.
