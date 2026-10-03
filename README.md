# Day 5 — Segmentation Data Lab

**Dành cho học viên · 240 phút thực hành trên lớp · điểm ghi nhận tối đa 100.** Repo đề bài mở công khai; mỗi học viên **fork repo này**, làm bài trong fork của mình, push kết quả rồi nộp link fork trên VLearn trong vòng 24 giờ sau buổi lab. Bài được chấm bằng công cụ riêng sau cửa sổ nộp. Không có bài tập bắt buộc về nhà. Bài giữ nguyên cấu trúc, ảnh, lớp và trọng số của [starter Day 5](https://github.com/VinUni-AI20k/Day5-Segmentation-Data-Student) tại commit `3bff13d`: Easy semantic → Medium instance → Hard panoptic → sáu checkpoint. Repo này bổ sung hướng dẫn CVAT local, tự kiểm và cách nộp, **không thay bài starter bằng bộ ảnh pilot khác**.

Bạn sẽ tự tạo mask cho ảnh trong repo, kiểm lại theo quy tắc, sửa một lỗi và giải thích quyết định của mình. Bằng chứng cần nộp là **ZIP export từ CVAT cho các task đã làm và một `REPORT.md`** trong fork của bạn. Có thể hoàn thành toàn bộ mà không cần lập trình, Jupyter hay SAM. [Hướng dẫn trực quan có ảnh chụp CVAT](lab-guide.html) dành cho người mới; README này là lộ trình đầy đủ để tra cứu trong lúc làm. Nếu xem trên GitHub không mở được HTML, tải fork về và mở file đó trong Chrome/Edge.

## Bắt đầu trong 5 phút

1. Đăng nhập GitHub, bấm **Fork** ở repo đề bài và chọn tài khoản của bạn. Tải fork về máy (Download ZIP hoặc clone), giải nén nếu cần; mở `lab-guide.html` để xem ảnh chụp giao diện. Không cần cài notebook để bắt đầu.
2. Mở **CVAT local của lớp** theo địa chỉ coach cung cấp. Nếu CVAT chạy trên chính máy bạn, địa chỉ thường là `http://localhost:8080`; nếu không mở được, báo coach với ảnh màn hình lỗi. Đừng tự cài một CVAT khác giữa giờ.
3. Đọc [phiếu quy tắc](guideline-mini-sheet.md). Tạo task đầu tiên tên `easy_semantic`, tải đúng ba ảnh trong [`data/tiers/easy_semantic/images/`](data/tiers/easy_semantic/images/). Nếu dùng ô **Labels → Raw** của CVAT, sao chép **toàn bộ** [`cvat-labels.json`](data/tiers/easy_semantic/cvat-labels.json) của task rồi dán vào đó. Nếu thêm từng label bằng **Constructor**, đọc tên trong [`classes.json`](data/tiers/easy_semantic/classes.json).
4. Vẽ mask, kiểm class và vùng, bấm **Save**, xuất **Segmentation mask 1.1**, lưu thành `easy_semantic.zip`. Các task tiếp theo có bộ ảnh và `classes.json` riêng.
5. Trước khi nộp, mở [`REPORT.md`](REPORT.md) đã có sẵn ở gốc fork và điền thật; [mẫu giải thích chi tiết](reports/REPORT_TEMPLATE.md) giúp bạn hiểu từng ô. Push/upload report cùng các ZIP lên fork rồi nộp link fork trên VLearn. Nếu không kịp task nào, ghi phần đã làm và phần còn thiếu; không tạo export rỗng.

> **Ảnh trong screenshot CVAT chỉ để tìm nút, không phải ảnh chấm.** Ảnh chấm nằm trong `data/` của repo này. Tên class phải giống từng chữ trong `classes.json` của chính task đang làm.

## Ba loại segmentation trong cùng bài

| Loại | Câu hỏi cần trả lời | Task | Ví dụ quyết định |
| --- | --- | --- | --- |
| **Semantic** | Pixel nhìn thấy thuộc **lớp vùng nào**? | Easy; `cp3_thin`, `cp4_curb`, `cp6_coverage` | Road và sidewalk là hai lớp dù màu gần giống. |
| **Instance** | Pixel nhìn thấy thuộc **vật nào**? | Medium; `cp1_holes`, `cp2_slice`, `cp5_occlusion` | Hai xe cùng class sát nhau vẫn là hai object/mask. |
| **Panoptic** | Vùng thuộc lớp nào, và vật đếm được là **instance nào**? | Hard | Vẽ stuff như road/sky cùng từng thing như car #1, car #2. |

**Mask** là vùng pixel bạn gán cho một lớp/vật; một bounding box không thay mask. **Stuff** là vùng không đếm từng cá thể như road, sky; **thing** là vật đếm được như car, person. Chỉ vẽ phần nhìn thấy, không tự đoán biên sau vật che. Một vật bị che thành hai mảng nhìn thấy rời nhau vẫn có thể là **một instance** theo quy tắc task. Xem [phiếu quy tắc](guideline-mini-sheet.md) để kiểm trước export.

## Toàn bộ task và thang 100 điểm

[`data/manifest.json`](data/manifest.json) là danh mục task, loại và trọng số; `classes.json` của từng task là nguồn chuẩn cho tên class, **không phải JSON để dán vào CVAT**. File `cvat-labels.json` cùng thư mục là bản **dán vào Labels → Raw**; tên label trong hai file được kiểm tự động là giống nhau. Các đường dẫn dưới đây chứa ảnh đầu vào, **không chứa đáp án**.

| Task | Ảnh | Điều cần thể hiện | Export CVAT | Tối đa |
| --- | ---: | --- | --- | ---: |
| [`easy_semantic`](data/tiers/easy_semantic/) | 3 | Road, sidewalk, building, vegetation, sky | Segmentation mask 1.1 | 20 |
| [`medium_instance`](data/tiers/medium_instance/) | 3 | Mỗi person/bicycle/car/motorcycle/bus/truck là object riêng | COCO 1.0 | 32 |
| [`hard_panoptic`](data/tiers/hard_panoptic/) | 2 | Stuff và từng thing theo 12 class của task | COCO 1.0 | 30 |
| [`cp1_holes`](data/checkpoints/cp1_holes/) | 1 | Kính/khe nằm trong mask vật, không khoét tùy tiện | COCO 1.0 | 3 |
| [`cp2_slice`](data/checkpoints/cp2_slice/) | 1 | Hai xe sát nhau là hai instance | COCO 1.0 | 3 |
| [`cp5_occlusion`](data/checkpoints/cp5_occlusion/) | 1 | Vật bị che vẫn một instance; đếm đúng | COCO 1.0 | 3 |
| [`cp3_thin`](data/checkpoints/cp3_thin/) | 1 | Nét mảnh/cột/biển, phóng to và dùng brush nhỏ | Segmentation mask 1.1 | 3 |
| [`cp4_curb`](data/checkpoints/cp4_curb/) | 1 | Ranh road–sidewalk theo chức năng/bó vỉa | Segmentation mask 1.1 | 3 |
| [`cp6_coverage`](data/checkpoints/cp6_coverage/) | 1 | Kiểm vùng thuộc class của task còn bỏ sót | Segmentation mask 1.1 | 3 |
| **Tổng** | **14** | Ba cấp + sáu checkpoint | | **100** |

Checkpoint có **class list riêng**. Ví dụ `cp3_thin` có `pole`, `traffic sign`, `sky`, `road`; `cp4_curb` chỉ có `road`, `sidewalk`. Đọc `classes.json` trước khi tạo mỗi task, không dùng nhầm class của Easy cho mọi task.

## Lộ trình 240 phút trên lớp

Đây là **timebox cho 240 phút thực hành**, để còn giờ Save, tự QC và chuẩn bị bài nộp. Nếu chậm hơn dự kiến, ghi rõ phần đã làm và phần còn thiếu. **Ground truth của Easy, Medium và Hard dự kiến được phát trong 60 phút cuối**, sau phần tự làm; lúc đó có thể dùng script để tìm và sửa lỗi. Hạn đưa link fork lên VLearn là **24 giờ sau buổi lab**; công cụ chấm riêng chạy sau cửa sổ nộp. [Bản lộ trình văn bản](GUIDE.md) có thể mở cạnh CVAT.

| Phút | Việc chính | Bằng chứng giữ lại |
| ---: | --- | --- |
| 0–15 | Vào CVAT, đọc quy tắc, tạo Easy với 3 ảnh và đúng 5 class | Task đầu mở được; biết Save/export ở đâu |
| 15–45 | Easy semantic: tô vùng, kiểm road–sidewalk, Save/export | `easy_semantic.zip` |
| 45–110 | Medium instance: tự vẽ object đầu rồi tiếp tục từng vật, kiểm thiếu/thừa/gộp/tách | `medium_instance.zip`; một quyết định trong report |
| 110–120 | Nghỉ | Giữ an toàn các ZIP đã xuất |
| 120–175 | Hard panoptic: stuff + từng thing trên hai ảnh, QC/export | `hard_panoptic.zip` |
| 175–185 | Nghỉ; nhận reference ba tier từ phút 180 theo hướng dẫn lớp | Không đưa đáp án lên fork |
| 185–215 | Sáu checkpoint; người xong sớm chạy scorer ba tier | ZIP trạm đã làm; kết quả tự đánh giá nếu có |
| 215–235 | Kiểm file, sửa và export lại nếu cần; điền report | `REPORT.md`: lỗi, hành động, ba ca cân nhắc |
| 235–240 | Save lần cuối, kiểm danh sách ZIP/report, ghi lỗi cần báo coach | Bài sẵn để đưa lên fork |

## CVAT local: làm từng bước, không cần code

Giao diện có thể khác đôi chút theo cấu hình lớp. Các ảnh chụp sau chỉ vị trí nút trên **CVAT local**, không phải ảnh/nhãn bài chấm. Nhấp ảnh trong [bản HTML](lab-guide.html#cvat) để xem lớn.

1. **Tạo task.** Trong CVAT chọn **Tasks → Create new task**. Name là mã task đúng như bảng trên, ví dụ `medium_instance`. Ở phần ảnh, chỉ chọn JPG trong `images/` của task đó; đừng gộp ảnh Easy, Medium và Hard vào một task. [Ảnh màn hình tạo task](docs/images/03-task-form.png).
2. **Thêm labels.** Có hai cách tương đương: mở `cvat-labels.json` **của đúng task**, chọn toàn bộ nội dung từ `[` đến `]`, copy, rồi vào **Labels → Raw**, dán đè nội dung hiện có và bấm **Done**; hoặc mở `classes.json` và thêm **từng tên** qua **Constructor → Add label**. Đừng dán `classes.json` vào Raw: file đó có thêm metadata dành cho bài lab nên CVAT không nhận. Kiểm số lượng/tên label trước khi Submit; `traffic sign` có dấu cách. Nếu task đã có annotation, **không dán đè Raw** vì thay label có thể làm mất liên kết annotation. [Ảnh màn hình thêm từng label](docs/images/04-label.png).
3. **Mở Job và vẽ mask.** Chọn Brush hoặc Polygon trong công cụ mask, chọn đúng label rồi vẽ theo phần nhìn thấy. Phóng to ranh giới, thu nhỏ brush cho nét mảnh. Danh sách **Objects** giúp xem class/số object. Một bounding box hình chữ nhật không thay mask. [Ảnh vị trí công cụ](docs/images/08-brush.jpg).
4. **Tự QC và Save.** Đi qua từng ảnh theo thứ tự: đúng ảnh → đúng class → đủ vùng/vật → biên → vùng bỏ sót/tràn nền. Với instance, kiểm hai xe có bị gộp hoặc một vật bị tách thành hai object không; với panoptic, kiểm stuff/thing có chồng lấn hay khoảng trống bất hợp lý không. Bấm **Save**, đổi ảnh rồi quay lại một ảnh để chắc dữ liệu còn đó.
5. **Export từ Job.** Menu Job → **Export job dataset**. Semantic chọn `Segmentation mask 1.1`; instance/panoptic chọn `COCO 1.0`. Tải ZIP rồi đổi **tên ZIP bên ngoài** thành `<mã_task>.zip`, giữ nguyên file bên trong. [Ảnh menu export](docs/images/10-export-menu.jpg) · [Ảnh chọn format](docs/images/11-export-format.jpg).
6. **Nếu export lỗi.** Giữ dữ liệu đã Save, ghi task và màn hình lỗi, báo coach. Đừng tự đổi format rồi coi là tương đương hoặc sửa JSON/PNG bên trong ZIP bằng tay. [CVAT_SETUP.md](CVAT_SETUP.md) là bản tra nhanh khi bị kẹt.

### Quy tắc riêng cho từng chặng

- **Easy — semantic:** chỉ dùng năm class trong [`classes.json`](data/tiers/easy_semantic/classes.json). Tô phần vùng nhìn thấy; ranh road–sidewalk theo chức năng/bó vỉa, không chỉ màu ảnh. Kiểm các mảng rõ ràng còn trống trước khi xuất.
- **Medium — instance:** sáu class trong [`classes.json`](data/tiers/medium_instance/classes.json). **Trước khi xem gợi ý tự động**, tự vẽ một object đầu tiên và ghi ảnh/vị trí, class, quy tắc chọn biên vào mục 2 của report. Sau đó nếu dùng gợi ý, tự kiểm class, số object, biên và ghi một lỗi đã sửa hoặc lý do giữ đề xuất. Không có gợi ý thì Brush/Polygon vẫn hoàn thành được.
- **Hard — panoptic:** 12 class trong [`classes.json`](data/tiers/hard_panoptic/classes.json), trong đó road/sidewalk/building/vegetation/sky là stuff. Vẽ cả stuff và **từng** thing; một mask `car` không thay cho mọi xe. Kiểm chồng lấn/khoảng trống bằng mắt trong CVAT. ZIP COCO cấu trúc hợp lệ **không tự chứng minh** panoptic đúng.
- **Sáu checkpoint:** `cp1_holes` kiểm kính/khe không bị khoét; `cp2_slice` tách hai vật sát nhau; `cp5_occlusion` giữ định danh một vật bị che; `cp3_thin` kiểm nét mảnh; `cp4_curb` kiểm ranh chức năng; `cp6_coverage` kiểm vùng nhìn thấy thuộc các class còn bỏ sót. Mỗi trạm có `classes.json` riêng. Nếu ca mơ hồ, ghi hai cách hiểu và bằng chứng, không bịa nhãn cho đủ.

## Công cụ hỗ trợ: quyết định vẫn là của bạn

**SAM không phải điều kiện làm bài và không bảo đảm có trên CVAT local.** Không thấy SAM thì dùng Brush/Polygon; Intelligent Scissors chỉ là tùy chọn nếu cấu hình lớp có. Không cần cài tool mới để được chấm. Gợi ý tự động có thể ăn bóng/nền, gộp hai xe hoặc bỏ sót chi tiết; bạn vẫn chọn class, kiểm số object và sửa mask. Một object Medium tự làm cùng lời giải thích trong report giúp coach nhìn thấy **cách áp dụng quy tắc**, không phải cơ chế kết luận ai dùng hay không dùng AI.

Người mới có ảnh hướng dẫn, checklist và đường báo lỗi; người quen công cụ làm **cùng bài và cùng bằng chứng**, rồi có thể phân tích sâu một lỗi mơ hồ hoặc hạn chế export khi xong sớm. Sau khi reference được phát, người hoàn thành sớm có thể chạy scorer để nhận phản hồi theo [hướng dẫn từng lệnh](docs/SELF_SCORING.md); đây không phải điều kiện nộp bài cốt lõi.

## QC và báo cáo trước khi nộp

Checklist chung: **đúng task/ảnh → đúng loại segmentation/class → đủ vùng/vật → biên theo phần nhìn thấy → không gộp/tách nhầm → Save → ZIP đúng format và tên**. Nếu ca không chắc, ghi vị trí, hai cách hiểu, quy tắc/bằng chứng và quyết định hoặc câu hỏi cho coach. Đừng sửa JSON/PNG trong ZIP để làm cho kiểm tra “xanh”.

Mở [`REPORT.md`](REPORT.md) ở gốc fork rồi điền; [mẫu có ví dụ](reports/REPORT_TEMPLATE.md) giải thích từng mục:

1. Mã học viên, các task và ảnh đã hoàn thành, ZIP tương ứng; task chưa kịp ghi rõ, **không tự điền điểm**.
2. Object Medium đầu tiên tự làm: ảnh, vị trí, class và quy tắc chọn biên. Nếu dùng gợi ý sau đó, ghi một quyết định sửa/giữ và lý do; nếu không dùng, vẫn giải thích quyết định gán nhãn.
3. Một lỗi thật đã phát hiện: task/ảnh/vùng, loại lỗi, dấu hiệu quan sát, hành động sửa, đã Save và export lại chưa.
4. Ba ca chưa chắc hoặc đã cân nhắc: hai cách hiểu, chứng cứ/quy tắc, quyết định hoặc câu hỏi cụ thể cho coach.

### GitHub Actions tự kiểm khi push; notebook và lệnh trên máy là dự phòng

Trên fork của bạn, bật tab **Actions** một lần, upload ZIP CVAT vào `submissions/` rồi Commit. Workflow **Day 5 self-check** sẽ chạy tự động và hiện kết quả ở **Actions → lần chạy mới nhất → Summary**: trước giờ phát đáp án là kiểm cấu trúc; sau khi release ground truth chính thức được công bố là điểm tự đánh giá Easy + Medium + Hard **/82**. Có thể sửa mask trong CVAT, Save/export/push lại bao nhiêu lần cần để nhận phản hồi mới. [Hướng dẫn từng nút và giới hạn của điểm tự đánh giá](docs/SELF_SCORING.md). Không cần Python, Colab hay đưa đáp án vào fork. Nếu release chưa được công bố, action chưa thể tính điểm; bài cốt lõi vẫn nộp bình thường.

[Một notebook dùng được trên Colab](notebooks/day5-segmentation-tu-kiem.ipynb) dẫn từ nhận ảnh đến nộp: xem ảnh, mask semantic, số mask instance, panoptic và tình trạng ZIP. Nó **không thêm task**, không bắt bạn viết code và không cần để nhận điểm. Notebook có ô kiểm môi trường/tự cài IPython nếu thiếu và giải thích từng trạng thái QC; [cách upload notebook lên Colab và nhập link fork](notebooks/README.md) có từng bước. Bạn không cần upload cả repo. Nếu máy có Python 3.10+, đặt ZIP vào `submissions/<mã_task>.zip` rồi chạy từ thư mục repo:

```bash
python3 scripts/inspect_submissions.py --dir submissions
```

Lệnh không cần thư viện ngoài; nó kiểm tên ảnh, class, cấu trúc `Segmentation mask 1.1`/`COCO 1.0` và dạng polygon/RLE. **Nó không đọc reference, không biết số object đúng, không kiểm biên đúng và không tính điểm.** `OK` là cấu trúc phù hợp; `THIẾU` là chưa có ZIP; `LỖI` cần xem và export lại trong CVAT. Số `annotations` ở COCO chỉ là số mask *bạn đã nộp*. Người không có Python cứ tự kiểm bằng CVAT và nộp trực tiếp. Sau giờ phát đáp án, GitHub Actions có thể chạy scorer; [cách chạy script bằng tay](docs/SELF_SCORING.md) vẫn là dự phòng.

## Fork → làm bài → push → nộp link trong vòng 24 giờ

Từ repo đề bài public, bấm **Fork** để có bản trên tài khoản GitHub của bạn. Làm bài với bộ ảnh trong fork; khi xuất từ CVAT, đưa `REPORT.md` vào gốc fork và các ZIP vào `submissions/` (ví dụ `submissions/easy_semantic.zip`, `submissions/cp2_slice.zip`). Dùng **Add file → Upload files** trên GitHub hoặc Git để push thay đổi, mở lại fork để chắc file đã hiện, rồi **dán link fork trên VLearn trong vòng 24 giờ sau buổi lab**. Không cần chạy Git bằng lệnh nếu bạn dùng nút Upload files. Nếu muốn có thêm một gói lưu/chuyển, lệnh sau là tùy chọn:

```bash
python3 scripts/package_submission.py --learner-id D5_012
```

[Hướng dẫn nộp](docs/SUBMISSION.md) ghi format, tên từng ZIP và cách đưa bài lên GitHub/VLearn không cần code. **Không upload thêm bản sao ảnh gốc, file tạm notebook hoặc đáp án vào fork.** Nếu export lỗi, báo coach và ghi trạng thái đã Save trong report; không tạo ZIP rỗng. Hạn 24 giờ là cửa sổ nhận bài, không phải một bài tập hoặc thang điểm mới.

## Mã nguồn starter có ngay trong repo này

Mã xử lý mask và tính metric từ starter nằm ở [`lab_utils.py`](lab_utils.py); hai lệnh tham khảo chấm một task và lập scorecard nằm ở [`scoring/score.py`](scoring/score.py) và [`scoring/scorecard.py`](scoring/scorecard.py). [Hướng dẫn tự đánh giá ba tier](docs/SELF_SCORING.md) giải thích từng lệnh và giới hạn của report. Công cụ chấm chính thức của lớp được vận hành riêng **sau cửa sổ nộp 24 giờ**. **Học viên không phải chạy các lệnh chấm để hoàn thành bài cốt lõi.**

Các lệnh chấm cần reference được giữ riêng và ba thư viện trong [`requirements.txt`](requirements.txt). Repo này chỉ có ảnh đầu vào, không có reference nên chạy chấm trước lúc phát sẽ báo thiếu reference, **không tạo điểm 0**. Repo có mã **kiểm và giải nén gói reference chính thức** cho Action, nhưng không có mã tạo đáp án hay file đáp án. Lệnh [`scripts/inspect_submissions.py`](scripts/inspect_submissions.py) ở trên vẫn là cách tự kiểm ZIP không cần reference hay thư viện ngoài. **Không đưa đáp án đã nhận vào fork public**.

## Điểm và giới hạn của phép đo

[Rubric 100 điểm](RUBRIC.md) giữ trọng số starter: Easy 20, Medium 32, Hard 30 và sáu checkpoint mỗi trạm 3. Người chấm đối chiếu với reference phù hợp: semantic dùng mIoU (coverage là tín hiệu QC kèm theo), instance dùng chất lượng mask ghép cặp cùng recall, panoptic dùng PQ. Bonus giờ cuối có mức 10 cho report đạt yêu cầu và 20 cho top 3 độ chính xác; **điểm ghi nhận vẫn không vượt 100**, hai mức không tự cộng chồng. Cách xác nhận PASS và xếp top 3 do người phụ trách thông báo; scorer không tự quyết định. **Repo học viên không chứa ground truth.** Tên class/format sai có thể làm bài không đọc đúng. IoU giữa hai bản gán nhãn hoặc với gợi ý máy chỉ là **độ giống nhau**, không phải correctness. Điểm rất cao, thời gian hay cờ kỹ thuật không tự kết luận hành vi của học viên; coach xem file và giải thích theo quy tắc.

## Khi bị kẹt, hãy báo đúng vấn đề

| Tình huống | Việc làm ngay |
| --- | --- |
| Không vào được CVAT local | Giữ ảnh màn hình lỗi, thời điểm và địa chỉ đã thử; báo coach. |
| Không thấy SAM | Tiếp tục Brush/Polygon; không chờ cài tool. |
| Không biết chọn class/ranh | Mở `classes.json` và [phiếu quy tắc](guideline-mini-sheet.md); ghi ảnh/vị trí cùng hai cách hiểu vào report. |
| Hai vật sát nhau hoặc một vật bị che | Xem quy tắc instance/checkpoint, đếm object trong CVAT trước khi Save. |
| Export sai format hoặc thiếu ảnh | Save dữ liệu CVAT, export lại đúng task; nếu format không có, báo coach, không sửa ZIP bằng tay. |
| Không có Python/Jupyter | Vẫn làm toàn bộ trên CVAT, nén thủ công và nộp report. |

**Nguồn bài:** ảnh, taxonomy và trọng số từ starter Day 5 commit `3bff13d`; xem [ghi chú dữ liệu](data/README.md) cho nguồn ảnh và giới hạn sử dụng. Khả năng có SAM và export của cấu hình CVAT lớp cần được kiểm tại môi trường lớp. Tự kiểm ZIP không thay lần chấm có reference của coach.
