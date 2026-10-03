# Tự đánh giá với reference được phát trong giờ cuối

Phần điểm tự đánh giá **chỉ mở khi người phụ trách phát ground truth cho Easy, Medium và Hard**, dự kiến trong 60 phút cuối của buổi lab. Trước thời điểm đó, hãy tự vẽ, Save, export và kiểm bằng mắt; repo học viên không chứa đáp án. Cách dễ nhất là để GitHub Actions chạy scorer sau khi bạn push ZIP lên fork. Không cần cài Python hay tự giải nén ground truth. Đây là vòng phản hồi để tìm lỗi và sửa, không thay bài gán nhãn, report hay chấm điểm chính thức.

## Cách dễ nhất — xem điểm ngay trên fork

1. Trên **fork của bạn**, mở tab **Actions** và bật workflows nếu GitHub hỏi xác nhận. GitHub không tự bật Actions trên fork mới. Không cần tạo secret, token hoặc sửa file workflow.
2. Save/export từ CVAT rồi upload ZIP đúng tên vào `submissions/` trên fork; bấm **Commit changes**. Workflow **Day 5 self-check** sẽ tự chạy mỗi khi ZIP hoặc `REPORT.md` được push. Mở **Actions → Day 5 self-check → lần chạy mới nhất → Summary**. Nếu chưa thấy lần chạy, kiểm Actions đã bật; sau đó chọn **Run workflow** để chạy thủ công.
3. Trước lúc gói đáp án chính thức xuất hiện, Summary chỉ kiểm cấu trúc ZIP và ghi “chưa có ground truth”; **không cho điểm 0**. Sau khi người phụ trách công bố gói đáp án trong giờ cuối, bấm **Run workflow** hoặc push ZIP mới. Summary sẽ hiện scorecard Easy + Medium + Hard tối đa **82**, task chưa có ZIP hiện `missing`/0. Sáu checkpoint vẫn theo rubric nhưng không được tự chấm khi chưa có reference.
4. Nếu kết quả chưa hợp lý, mở đúng task trong CVAT, xem mask/class/object, sửa → Save → export lại → upload ZIP mới cùng tên vào fork. Bạn có thể lặp lại để xem phản hồi mới; **lần chạy cũ không phải bài nộp cuối**. Nếu ZIP lỗi, xem dòng `LỖI` trong Summary; nếu workflow đỏ, mở log bước lỗi và báo coach. Không sửa JSON/PNG trong ZIP hoặc sửa workflow để “đạt điểm”.

Action lấy gói đáp án từ release chính thức của repo lớp **sau khi** được phát; không chép đáp án vào fork. Nếu lớp chỉ gửi file qua kênh khác mà chưa công bố release, GitHub Actions **chưa thể tính điểm**; dùng hướng dẫn chạy trên máy bên dưới hoặc chờ người phụ trách. Điểm tự đánh giá sau lúc xem đáp án **không chứng minh chất lượng bản làm độc lập trước đó**, không tự quyết định PASS, bonus hay top 3. Trên fork, học viên có quyền sửa workflow/code; vì vậy Summary chỉ là phản hồi cá nhân, **công cụ chấm riêng của lớp vẫn là nguồn điểm chính thức**.

## Cách dự phòng — chạy script trên máy

## Trước khi mở đáp án

1. Giữ ba ZIP đầu tiên đã xuất từ CVAT: `submissions/easy_semantic.zip`, `submissions/medium_instance.zip`, `submissions/hard_panoptic.zip`. Nếu chưa xong task nào, không tạo ZIP rỗng.
2. Hoàn thành phần tự làm và tự QC trước khi xem reference. Để việc xếp hạng có thể kiểm chứng, người phụ trách cần công bố cách ghi nhận **bản export trước lúc phát ground truth**; kết quả sửa sau khi đã xem đáp án không thể tự coi là bằng chứng độc lập để xếp top 3.
3. Ground truth chỉ được dùng theo hướng dẫn phát trong lớp. **Không commit/push, upload lên Colab công khai, gửi lên VLearn hoặc chia sẻ lại** các thư mục `groundtruth/`, file `instances.json`, `panoptic.json` hay ảnh PNG đáp án. `.gitignore` đã bỏ qua `data/**/groundtruth/`, nhưng điều đó không bảo vệ bản ZIP đáp án nếu bạn cố thêm hoặc đưa file ra ngoài repo.

### Bước 1 — đặt reference đúng chỗ

Sau khi giải nén gói chính thức trên máy, đối chiếu cấu trúc bên dưới; các đường dẫn là **thư mục con trong bản fork tải về**, không phải thư mục ở GitHub:

```text
data/tiers/easy_semantic/groundtruth/<tên_ảnh>.png
data/tiers/medium_instance/groundtruth/instances.json
data/tiers/hard_panoptic/groundtruth/panoptic.json
data/tiers/hard_panoptic/groundtruth/png/<tên_ảnh>.png
```

Mỗi task phải khớp **đủ tên ảnh** trong thư mục `images/` tương ứng. Gói phát có thể có tên ZIP/thư mục ngoài khác nhau; hãy xem cấu trúc thực tế hoặc hỏi coach trước khi chép, không đổi tên JSON/PNG để ép chạy. Không đưa reference vào `submissions/` hoặc vào fork GitHub. Các checkpoint **không nằm trong đợt phát ba tier này**, trừ khi người phụ trách nói rõ.

### Bước 2 — cài thư viện trên máy đang chạy scorer

Mở Terminal tại thư mục gốc của bản fork đã tải về (nơi có `requirements.txt` và thư mục `scoring/`). Trên macOS/Linux:

```bash
python3 --version
python3 -m pip install -r requirements.txt
python3 scoring/score.py --list
```

Trên Windows, thay `python3` bằng `py -3` trong các lệnh. Cần Python 3.10+ và các thư viện `numpy`, `pillow`, `pycocotools`. Nếu lớp đã có môi trường `ai-lab`, có thể dùng đường dẫn Python của môi trường đó như trong [hướng dẫn repo gốc](https://github.com/VinUni-AI20k/Day5-Segmentation-Data-Student/blob/main/GUIDE.md); **không bắt buộc cài thêm một môi trường khác**. Nếu `pip` hoặc `pycocotools` lỗi, báo coach và tiếp tục Save/export/report; không có điểm phạt cốt lõi vì máy thiếu môi trường chấm.

### Bước 3 — chạy một task, đọc và sửa

Đặt ZIP CVAT của bạn trong `submissions/`, giữ nguyên nội dung bên trong. Chạy từng dòng từ thư mục gốc:

```bash
python3 scoring/score.py easy_semantic submissions/easy_semantic.zip --group tiers
python3 scoring/score.py medium_instance submissions/medium_instance.zip --group tiers
python3 scoring/score.py hard_panoptic submissions/hard_panoptic.zip --group tiers
```

Easy in `per-class IoU`: class nào thấp thì nhìn lại đúng ranh/vùng đó trong CVAT. Medium xem `mean matched IoU`, `R@0.5`, số `FP/FN` để tìm mask ăn nền, vật thừa hoặc bỏ sót. Hard xem `PQ`, `SQ`, `RQ` để phân biệt vấn đề biên với vật/vùng thiếu-thừa. Điểm cao là mức khớp với **reference được phát**, không phải bằng chứng bạn đã tự làm trước khi xem nó. Nếu sửa, **sửa trong CVAT → Save → export ZIP mới → chạy lại**; không chỉnh JSON/PNG trong ZIP hay chép đáp án. Ghi một lỗi và hành động sửa có thật vào mục 3 của `REPORT.md`.

### Bước 4 — gộp riêng ba tier

Khi có đủ reference ba tier, chạy:

```bash
python3 scoring/scorecard.py --group tiers --dir submissions --out reports/tiers
```

Mở `reports/tiers/SCORECARD.md` để xem **điểm ba tier tối đa 82**, và `reports/tiers/scorecard.json` nếu cần dữ liệu máy đọc. Ba tier = Easy 20 + Medium 32 + Hard 30. Checkpoint vẫn có **18 điểm** trong rubric 100 nhưng không được tự chấm nếu chưa có reference của từng trạm. Nếu không có ZIP nào trong ba tier, script không tạo scorecard; nếu thiếu một ZIP, task đó hiện `missing`/0 trong bản tự đánh giá, không phải lỗi môi trường.

Nếu script báo `Protected reference missing`, kiểm đúng cấu trúc ở Bước 1 hoặc chờ gói chính thức. Nếu báo ảnh không khớp task, kiểm tên ZIP và ảnh export; **không đổi nhãn/ảnh để qua lỗi**. Nếu có `REVIEW SIGNALS`/`SUSPECT`, đó là cờ cần người xem lại, **không phải kết luận gian lận**; đặc biệt sau khi reference đã phát, độ giống cao có thể do đã xem đáp án. `SCORECARD.md` **không có chữ PASS** hay bảng xếp hạng top 3; người phụ trách xác nhận theo tiêu chí công bố riêng.

## Điểm 100 và bonus

Rubric gốc vẫn là **20 + 32 + 30 + 18 = 100**. Theo thông báo của người phụ trách, phần chạy report đạt yêu cầu có mức bonus **10 điểm**; top 3 độ chính xác cao nhất có mức **20 điểm**. Đây là **hai mức, không cộng dồn**; điểm ghi nhận cuối cùng không vượt **100**: `min(100, điểm_core + mức_bonus_được_xác_nhận)`. Không tự điền bonus hay chữ PASS vào report. Tiêu chí `PASS`, cách xếp top 3, thời điểm chốt bản độc lập và xử lý đồng hạng do người phụ trách công bố; script hiện tại **chưa tự quyết định** các việc đó.

Bạn vẫn nộp **link fork** cùng `REPORT.md` và ZIP của task đã làm trên VLearn trong hạn lớp thông báo. Có thể ghi kết quả tự đánh giá trong report và đính kèm `reports/tiers/SCORECARD.md` nếu muốn, nhưng scorecard **không thay ZIP**. Không đưa đáp án vào repo công khai. Công cụ chấm chính thức sau hạn nộp vẫn đối chiếu bản đã nộp theo quy trình lớp.
