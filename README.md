# DSA---Project
# Trò chơi Tetris đơn giản với Pygame

Đây là một triển khai cơ bản của trò chơi kinh điển Tetris được xây dựng bằng Python và thư viện Pygame. Trò chơi bao gồm các cơ chế cốt lõi của Tetris, hệ thống tính điểm, lưu trữ điểm cao nhất vào tệp, bộ đếm thời gian và tốc độ rơi của khối tăng dần theo thời gian.

## Tính năng

* Lối chơi Tetris cổ điển với 7 hình dạng tetromino tiêu chuẩn.
* Tạo khối ngẫu nhiên với màu sắc ngẫu nhiên.
* Di chuyển khối (trái, phải, xuống) và xoay khối.
* Rơi mềm (giữ phím xuống) và rơi thẳng (phím Space).
* Phát hiện va chạm với tường, sàn và các khối đã xếp.
* Xóa hàng và tính điểm.
* **Hệ thống điểm cao nhất:** Lưu và tải điểm cao nhất từ tệp `highscore.txt`.
* **Bộ đếm thời gian chơi:** Hiển thị thời gian đã trôi qua ở định dạng MM:SS trong khi chơi game.
* **Độ khó tăng dần:** Tốc độ rơi của khối tăng dần một cách từ từ theo thời gian chơi, cho đến khi đạt tốc độ tối đa.
* Trạng thái Game Over.
* Khởi động lại game bằng phím ESC.

## Yêu cầu

* Python 3.x
* Thư viện Pygame

## Cài đặt

1.  Đảm bảo bạn đã cài đặt Python 3.x.
2.  Cài đặt thư viện Pygame sử dụng pip:
    ```bash
    pip install pygame
    ```

## Cách tải mã nguồn

Bạn có thể tải mã nguồn về máy theo hai cách:

1.  **Sử dụng Git (Nếu bạn đã cài Git):**
    Mở Terminal hoặc Command Prompt, sau đó chạy lệnh sau để clone (tải về) toàn bộ repository:
    ```bash
    git clone [here](https://github.com/Nhan-Laptop/DSA---Project)
    ```

2.  **Tải dưới dạng tệp ZIP:**
    Truy cập trang repository trên GitHub. Tìm nút "Code" (hoặc tương tự) và chọn "Download ZIP". Giải nén tệp ZIP đã tải về vào một thư mục trên máy tính của bạn.

## Cách chạy trò chơi

1.  Sau khi đã tải mã nguồn về, mở Terminal hoặc Command Prompt.
2.  Điều hướng đến thư mục chứa mã nguồn của trò chơi:
    ```bash
    cd /duong/dan/den/thu/muc/tro/choi
    ```
    (Thay `/duong/dan/den/thu/muc/tro/choi` bằng đường dẫn thực tế đến thư mục bạn đã giải nén hoặc clone).
3.  Chạy tệp script Python chính:
    ```bash
    python ten_file_tetris_cua_ban.py
    ```
    (Thay `ten_file_tetris_cua_ban.py` bằng tên tệp Python thực tế chứa mã nguồn game của bạn, ví dụ: `tetris_game.py`).

## Cách chơi

* **Mũi tên lên (↑):** Xoay khối hiện tại.
* **Mũi tên trái (←):** Di chuyển khối hiện tại sang trái.
* **Mũi tên phải (→):** Di chuyển khối hiện tại sang phải.
* **Mũi tên xuống (↓):** Rơi mềm (giúp khối rơi nhanh hơn khi giữ phím).
* **Phím Space:** Rơi thẳng (đưa khối rơi ngay lập tức xuống đáy).
* **Phím ESC:** Khởi động lại game (đặt lại điểm số, thời gian và bảng chơi, nhưng giữ lại điểm cao nhất).

Trò chơi sẽ hiển thị điểm số hiện tại của bạn, điểm cao nhất đã đạt được và thời gian đã trôi qua ở bên cạnh lưới chơi. Tốc độ rơi của khối sẽ tăng dần khi bạn chơi càng lâu.

## Tệp tin

* `ten_file_tetris_cua_ban.py`: Mã nguồn chính của trò chơi.
* `highscore.txt`: (Được tạo tự động khi đạt được điểm cao nhất mới) Lưu trữ điểm số cao nhất. Vui lòng không chỉnh sửa tệp này thủ công khi trò chơi đang chạy.

## Giấy phép (License)

Dự án này được cung cấp cho mục đích giáo dục.

---
