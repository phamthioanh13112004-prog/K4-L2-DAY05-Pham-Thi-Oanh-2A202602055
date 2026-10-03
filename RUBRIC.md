# Rubric Day 5 — tối đa 100 điểm trong lớp

Trọng số giữ từ [starter Day 5](https://github.com/VinUni-AI20k/Day5-Segmentation-Data-Student) commit `3bff13d`; không có bài về nhà bắt buộc. Task chưa nộp được ghi là chưa có bằng chứng, không tự điền điểm giả. Học viên nộp link fork trên VLearn trong vòng 24 giờ sau buổi lab; công cụ chấm riêng chạy sau cửa sổ nộp. Bản nộp được xem cùng ảnh, class và quy tắc của task. Ground truth ba tier được phát **trong 60 phút cuối buổi lab** theo hướng dẫn lớp; đáp án checkpoint chỉ được dùng nếu người phụ trách cung cấp riêng.

| Task | Loại | Điểm tối đa | Điều cần chứng minh |
| --- | --- | ---: | --- |
| `easy_semantic` | Semantic | 20 | Phủ đúng vùng và lớp, nhất là road/sidewalk |
| `medium_instance` | Instance | 32 | Đủ vật, đúng class, từng vật một mask, biên theo phần nhìn thấy |
| `hard_panoptic` | Panoptic | 30 | Stuff và things cùng đúng; things tách instance, ít vùng bỏ trống/chồng lấn |
| Sáu checkpoint | Theo từng trạm | 6 × 3 = 18 | Xử lý lỗ, tách, nét mảnh, bó vỉa, che khuất, phủ vùng |
| **Tổng** | | **100** | |

Metric của starter gồm mIoU/coverage cho semantic, matched IoU và recall cho instance, PQ cho panoptic. **Chỉ có thể tính điểm so reference khi người chấm có ground truth phù hợp.** IoU giữa hai bản nhãn hoặc với gợi ý máy chỉ là độ giống nhau, không phải correctness. Điểm, cờ bất thường hoặc tốc độ không tự chứng minh người học gian lận; khi cần coach xem lại cách áp dụng quy tắc và bằng chứng trước/sau sửa.

## Bonus giờ cuối, vẫn tối đa 100

Thông báo của người phụ trách có **hai mức bonus**: **10** khi chạy report và đáp ứng yêu cầu, **20** cho top 3 độ chính xác cao nhất. Để giữ trần 100 theo yêu cầu lớp, cách ghi nhận đề xuất là `điểm_cuối = min(100, điểm_core + mức_bonus_được_xác_nhận)`, với `mức_bonus` là **0, 10 hoặc 20** (lấy mức cao nhất, không cộng dồn 10 + 20). Ví dụ core 74, bonus 10 → 84; core 92, bonus 20 → 100. Bốn trọng số task ở bảng trên **không giảm và không đổi**. Phần điểm vượt trần không chuyển sang ngày khác.

Script `score.py` trả metric/điểm từng task và `scorecard.py --group tiers` gộp ba tier tối đa **82 điểm**; **không script nào in PASS, tính bonus, xếp top 3 hoặc kiểm tra ai vẽ trước giờ phát đáp án**. Người phụ trách cần công bố tiêu chí PASS cụ thể, cách xếp hạng/đồng hạng và bản export dùng để xét top 3. Để top 3 phản ánh chất lượng độc lập, nên chốt ZIP và thời điểm trước lúc phát ground truth; bài sửa sau khi xem reference dùng cho học và chấm theo quy định, không thể tự nhận là bài chưa xem đáp án. Chưa có xác nhận từ người phụ trách thì học viên **không tự cộng điểm bonus** vào `REPORT.md`.

[Hướng dẫn GitHub Actions tự đánh giá sau khi nhận reference](docs/SELF_SCORING.md) có đường xem Summary không cần Python, cùng lệnh dự phòng trên máy. Học viên có thể lặp lại lượt tự đánh giá; kết quả sau khi đáp án đã phát **không dùng làm bằng chứng độc lập để xếp top 3**. Người không chạy được Action vẫn làm/nộp bài cốt lõi; nếu muốn xét bonus do môi trường lỗi, báo coach ngay trong giờ lab. Ground truth đã phát **không được đưa vào fork công khai**. Cờ `SUSPECT` khi metric cao chỉ là tín hiệu xem lại, đặc biệt không đủ kết luận gì sau lúc đáp án đã được phát.

## Cách đọc điểm kỹ thuật của starter

Khi reference đã được người chấm chuẩn bị và đối chiếu đúng ảnh/class, scorer gốc đổi metric thành điểm bằng `clamp((metric − floor)/(cap − floor), 0, 1) × trọng số`, làm tròn một chữ số. Đây là quy tắc chấm của starter, không phải lời hứa rằng tự kiểm ZIP sẽ cho điểm.

| Loại | Metric dùng để chấm | Floor | Cap nhận đủ điểm |
| --- | --- | ---: | ---: |
| Semantic | mIoU theo class; coverage là tín hiệu QC kèm theo | 0.40 | 0.85 |
| Instance | mean matched IoU × recall@0.5 | 0.40 | 0.85 |
| Panoptic | PQ trên stuff và từng thing | 0.20 | 0.65 |

Thiếu object làm recall giảm, thừa object ảnh hưởng precision và việc ghép; một mask khít không bù được những vật bỏ sót. Mask thiếu/khác ảnh hoặc sai class cần kiểm lại trên CVAT trước khi bàn về điểm. Coach xem cả file xuất và report cho những ca quy tắc mơ hồ; không suy diễn hành vi của học viên từ một ngưỡng hay cờ kỹ thuật.

## Điều cần quan sát ở sáu checkpoint

| Trạm | Bằng chứng đúng | Lỗi dễ gặp cần sửa |
| --- | --- | --- |
| `cp1_holes` | Kính/khe nằm trong mask vật theo quy tắc task | Khoét lỗ tùy tiện khiến vật bị rỗng |
| `cp2_slice` | Hai xe sát nhau vẫn là hai instance | Một mask gộp hai xe |
| `cp5_occlusion` | Vật bị che vẫn được đếm là một instance | Tách thành hai object hoặc tự vẽ xuyên vùng bị che |
| `cp3_thin` | Nét mảnh có class đúng, xem ở zoom lớn | Bỏ cột/biển hoặc brush quá dày |
| `cp4_curb` | Ranh road–sidewalk theo chức năng/bó vỉa | Chọn theo màu nhựa đường |
| `cp6_coverage` | Vùng nhìn thấy thuộc lớp cần có được phủ | Khe trống lớn hoặc tô bừa vùng không chắc |

Mọi học viên có cùng bài, lớp và chuẩn bằng chứng. Hướng dẫn trực quan giúp người mới thao tác; người xong sớm có thể dùng reference để phân tích và sửa lỗi. Dùng công cụ hỗ trợ không thay thế việc tự kiểm và giải thích một quyết định gán nhãn.
