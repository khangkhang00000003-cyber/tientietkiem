import streamlit as st
import calendar
from datetime import date, timedelta

st.set_page_config(page_title="Tính lãi tiết kiệm", page_icon="💰", layout="centered")

# ----------------------------------------------------------------------------
# HÀM TIỆN ÍCH
# ----------------------------------------------------------------------------

def add_months(d: date, months: int) -> date:
    """Cộng thêm 'months' tháng vào ngày d (giữ nguyên ngày, xử lý tháng thiếu ngày)."""
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def split_into_monthly_chunks(start: date, end: date):
    """Chia khoảng [start, end) thành các đoạn theo từng tháng lịch (để hiển thị nhận lãi hàng tháng)."""
    chunks = []
    cur = start
    while cur < end:
        nxt = add_months(cur, 1)
        if nxt > end:
            nxt = end
        chunks.append((cur, nxt))
        cur = nxt
    return chunks


def fmt_money(x: float) -> str:
    return f"{x:,.0f} VNĐ".replace(",", ".")


def tinh_lai_tiet_kiem(principal, term_rate, demand_rate, deposit_date, withdrawal_date, term_months):
    """
    Tính lãi tiết kiệm có tái tục tự động khi đến hạn.
    Trả về danh sách các 'kỳ' (period) đã trải qua và tổng lãi.
    Mỗi kỳ: start, end, days, rate, rate_type ('Có kỳ hạn' / 'Không kỳ hạn'), interest, completed(bool)
    """
    periods = []
    current_start = deposit_date
    max_loops = 2000  # phòng vòng lặp vô hạn

    for _ in range(max_loops):
        maturity = add_months(current_start, term_months)

        if withdrawal_date >= maturity:
            # Kỳ này đã đủ hạn -> hưởng lãi suất có kỳ hạn trọn vẹn
            days = (maturity - current_start).days
            interest = principal * (term_rate / 100.0) * days / 365.0
            periods.append({
                "start": current_start,
                "end": maturity,
                "days": days,
                "rate": term_rate,
                "rate_type": "Có kỳ hạn (đủ hạn)",
                "interest": interest,
                "completed": True,
            })
            current_start = maturity
            if withdrawal_date == maturity:
                # Khách rút đúng ngày đáo hạn -> dừng, không tái tục
                break
            # Khách không rút -> ngân hàng tự động tái tục kỳ hạn mới, lặp tiếp
            continue
        else:
            # Rút trước hạn của kỳ hiện tại -> hưởng lãi suất không kỳ hạn
            days = (withdrawal_date - current_start).days
            if days > 0:
                interest = principal * (demand_rate / 100.0) * days / 365.0
                periods.append({
                    "start": current_start,
                    "end": withdrawal_date,
                    "days": days,
                    "rate": demand_rate,
                    "rate_type": "Không kỳ hạn (rút trước hạn)",
                    "interest": interest,
                    "completed": False,
                })
            break

    total_interest = sum(p["interest"] for p in periods)
    return periods, total_interest


# ----------------------------------------------------------------------------
# GIAO DIỆN
# ----------------------------------------------------------------------------

st.title("💰 Tính lãi tiết kiệm ngân hàng")
st.caption(
    "Ứng dụng tính tiền lãi và tổng số tiền nhận được khi gửi tiết kiệm có kỳ hạn. "
    "Nếu rút trước hạn, phần kỳ chưa đủ hạn sẽ được hưởng lãi suất không kỳ hạn. "
    "Nếu đến hạn mà không rút, ngân hàng tự động tái tục đúng kỳ hạn đã gửi."
)

st.divider()

col1, col2 = st.columns(2)
with col1:
    so_tien = st.number_input(
        "💵 Số tiền khách hàng gửi (VNĐ)",
        min_value=0.0, step=1_000_000.0, value=100_000_000.0, format="%.0f"
    )
    lai_suat_ky_han = st.number_input(
        "📈 Lãi suất có kỳ hạn (%/năm)", min_value=0.0, max_value=100.0, value=5.5, step=0.1, format="%.2f"
    )
    lai_suat_khong_ky_han = st.number_input(
        "📉 Lãi suất không kỳ hạn (%/năm)", min_value=0.0, max_value=100.0, value=0.2, step=0.1, format="%.2f"
    )

with col2:
    ngay_gui = st.date_input("📅 Ngày gửi tiền", value=date(2024, 1, 10))
    ky_han_thang = st.selectbox(
        "⏳ Kỳ hạn gửi tiền",
        options=[1, 2, 3, 6, 9, 12, 13, 18, 24, 36],
        format_func=lambda x: f"{x} tháng",
        index=2,
    )
    ngay_rut = st.date_input("📅 Ngày rút tiền", value=date(2024, 8, 15))

phuong_thuc = st.radio(
    "💳 Hình thức nhận lãi",
    ["Nhận lãi trước", "Nhận lãi hàng tháng", "Nhận lãi cuối kỳ"],
    horizontal=True,
)

st.divider()

tinh_toan = st.button("🧮 Tính toán", type="primary", use_container_width=True)

if tinh_toan:
    if ngay_rut <= ngay_gui:
        st.error("⚠️ Ngày rút tiền phải sau ngày gửi tiền. Vui lòng kiểm tra lại.")
    elif so_tien <= 0:
        st.error("⚠️ Số tiền gửi phải lớn hơn 0.")
    else:
        periods, total_interest = tinh_lai_tiet_kiem(
            so_tien, lai_suat_ky_han, lai_suat_khong_ky_han, ngay_gui, ngay_rut, ky_han_thang
        )
        total_amount = so_tien + total_interest

        so_ky_dao_han = sum(1 for p in periods if p["completed"])
        rut_truoc_han = any(not p["completed"] for p in periods)

        # ----- Thông báo trạng thái -----
        maturity_first = add_months(ngay_gui, ky_han_thang)
        if rut_truoc_han:
            st.warning(
                f"⚠️ Khách hàng rút tiền trước hạn của kỳ hiện hành "
                f"(kỳ này bắt đầu {periods[-1]['start'].strftime('%d/%m/%Y')}, "
                f"đáo hạn {add_months(periods[-1]['start'], ky_han_thang).strftime('%d/%m/%Y')}). "
                f"Phần chưa đủ kỳ hạn được tính theo **lãi suất không kỳ hạn ({lai_suat_khong_ky_han}%/năm)**."
            )
        else:
            st.success("✅ Khách hàng rút tiền đúng vào ngày đáo hạn — hưởng trọn lãi suất có kỳ hạn.")

        if so_ky_dao_han > 0:
            st.info(f"🔄 Sổ tiết kiệm đã được ngân hàng **tự động tái tục {so_ky_dao_han} kỳ** (mỗi kỳ {ky_han_thang} tháng) trước khi khách hàng rút tiền.")

        # ----- Kết quả tổng hợp -----
        st.subheader("📊 Kết quả tính toán")
        m1, m2, m3 = st.columns(3)
        m1.metric("Tiền gốc", fmt_money(so_tien))
        m2.metric("Tổng tiền lãi", fmt_money(total_interest))
        m3.metric("Tổng tiền nhận được", fmt_money(total_amount))

        st.caption(
            f"Ngày đáo hạn ban đầu: **{maturity_first.strftime('%d/%m/%Y')}**  |  "
            f"Tổng số ngày gửi: **{(ngay_rut - ngay_gui).days} ngày**"
        )

        # ----- Chi tiết theo từng kỳ -----
        st.subheader("📋 Chi tiết lãi theo từng kỳ")
        rows = []
        for i, p in enumerate(periods, start=1):
            rows.append({
                "Kỳ": i,
                "Từ ngày": p["start"].strftime("%d/%m/%Y"),
                "Đến ngày": p["end"].strftime("%d/%m/%Y"),
                "Số ngày": p["days"],
                "Loại lãi suất": p["rate_type"],
                "Lãi suất (%/năm)": p["rate"],
                "Tiền lãi kỳ": fmt_money(p["interest"]),
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)

        # ----- Chi tiết theo phương thức nhận lãi -----
        st.subheader(f"💳 Chi tiết theo hình thức: {phuong_thuc}")

        if phuong_thuc == "Nhận lãi cuối kỳ":
            st.write(
                f"Toàn bộ tiền lãi **{fmt_money(total_interest)}** được cộng dồn và trả **một lần cùng tiền gốc** "
                f"vào ngày khách hàng rút tiền ({ngay_rut.strftime('%d/%m/%Y')})."
            )
            st.table([{
                "Ngày nhận": ngay_rut.strftime("%d/%m/%Y"),
                "Số tiền nhận": fmt_money(total_amount),
                "Ghi chú": "Gốc + toàn bộ lãi"
            }])

        elif phuong_thuc == "Nhận lãi trước":
            st.write(
                "Với mỗi kỳ đủ hạn, tiền lãi được tạm tính và chi trả **ngay khi bắt đầu kỳ** (theo lãi suất có kỳ hạn). "
                "Nếu khách hàng rút trước hạn của kỳ hiện hành, phần lãi kỳ đó chỉ được hưởng theo lãi suất không kỳ hạn "
                "(thấp hơn) — ngân hàng sẽ thu hồi phần chênh lệch đã tạm ứng dư (nếu có) khi tất toán."
            )
            rows2 = []
            recovered_note = None
            for p in periods:
                if p["completed"]:
                    rows2.append({
                        "Ngày nhận lãi": p["start"].strftime("%d/%m/%Y"),
                        "Số tiền lãi nhận trước": fmt_money(p["interest"]),
                        "Ghi chú": f"Lãi kỳ {p['start'].strftime('%d/%m/%Y')} - {p['end'].strftime('%d/%m/%Y')}"
                    })
                else:
                    # kỳ cuối rút trước hạn: nếu đã lỡ tạm ứng theo lãi kỳ hạn thì cần thu hồi chênh lệch
                    full_maturity = add_months(p["start"], ky_han_thang)
                    full_term_days = (full_maturity - p["start"]).days
                    prepaid_estimate = so_tien * (lai_suat_ky_han / 100.0) * full_term_days / 365.0
                    actual = p["interest"]
                    thu_hoi = prepaid_estimate - actual
                    if thu_hoi > 0:
                        recovered_note = thu_hoi
                    rows2.append({
                        "Ngày nhận lãi": p["start"].strftime("%d/%m/%Y") + " (tạm ứng)",
                        "Số tiền lãi nhận trước": fmt_money(prepaid_estimate),
                        "Ghi chú": "Tạm ứng theo lãi suất có kỳ hạn — sẽ điều chỉnh khi tất toán do rút trước hạn"
                    })
            st.table(rows2)
            if recovered_note:
                st.warning(
                    f"🔻 Do rút trước hạn, ngân hàng thu hồi phần lãi đã tạm ứng dư: **{fmt_money(recovered_note)}**. "
                    f"Số tiền gốc hoàn trả khi tất toán = {fmt_money(so_tien - recovered_note)}."
                )
            st.caption(f"➡️ Tổng cộng tiền lãi thực hưởng (đã điều chỉnh): {fmt_money(total_interest)}. "
                       f"Tổng tiền khách hàng nhận (gồm các lần nhận lãi trước + gốc hoàn trả cuối kỳ) = {fmt_money(total_amount)}.")

        else:  # Nhận lãi hàng tháng
            st.write("Tiền lãi được chi trả **định kỳ hàng tháng** trong suốt thời gian gửi; tiền gốc được hoàn trả khi khách hàng rút tiền.")
            rows3 = []
            for p in periods:
                chunks = split_into_monthly_chunks(p["start"], p["end"])
                for c_start, c_end in chunks:
                    days = (c_end - c_start).days
                    interest_chunk = so_tien * (p["rate"] / 100.0) * days / 365.0
                    rows3.append({
                        "Ngày nhận lãi": c_end.strftime("%d/%m/%Y"),
                        "Số ngày": days,
                        "Lãi suất áp dụng": f"{p['rate']}%/năm ({p['rate_type']})",
                        "Tiền lãi tháng": fmt_money(interest_chunk),
                    })
            st.table(rows3)
            st.caption(
                f"➡️ Tổng tiền lãi đã nhận hàng tháng: {fmt_money(total_interest)}. "
                f"Khi rút tiền ({ngay_rut.strftime('%d/%m/%Y')}), khách hàng nhận lại tiền gốc: {fmt_money(so_tien)}."
            )

        st.divider()
        st.success(f"### 💰 Tổng số tiền khách hàng nhận được (gốc + lãi): {fmt_money(total_amount)}")

st.divider()
with st.expander("ℹ️ Quy tắc tính lãi áp dụng trong ứng dụng"):
    st.markdown(
        """
- **Số ngày tính lãi** cho mỗi kỳ = từ ngày bắt đầu kỳ đến **trước 1 ngày** đáo hạn hoặc trước 1 ngày rút tiền
  (tức là số ngày = *ngày kết thúc − ngày bắt đầu*, tính theo lịch dương, cơ sở 365 ngày/năm).
- Nếu khách hàng **rút đúng hoặc sau ngày đáo hạn** của một kỳ: kỳ đó được hưởng trọn **lãi suất có kỳ hạn**.
- Nếu đến hạn mà khách hàng **không rút tiền**: ngân hàng **tự động tái tục** một kỳ hạn mới đúng bằng kỳ hạn ban đầu, và tiếp tục tính lãi có kỳ hạn cho các kỳ tái tục đã hoàn tất.
- Nếu khách hàng **rút trước hạn** của kỳ hiện hành (kỳ chưa đáo hạn): riêng phần thời gian của kỳ đó được tính theo **lãi suất không kỳ hạn**, các kỳ trước đó đã đáo hạn vẫn được giữ nguyên lãi suất có kỳ hạn.
- Công thức lãi đơn: **Tiền lãi = Số tiền gửi × Lãi suất (%/năm) × Số ngày / 365**.
        """
    )
