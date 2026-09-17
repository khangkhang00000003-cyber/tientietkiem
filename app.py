import streamlit as st
import base64
from datetime import date, timedelta

# 1. Cấu hình trang
st.set_page_config(
    page_title="Tính tiền lãi của Võ Hoàn Khang",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Đọc ảnh thành dạng Base64 để làm nền ổn định trên Streamlit
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

img_base64 = get_base64_of_bin_file("logo.jpg.jpg")

# 3. CSS xử lý hiển thị ảnh nền
# Đã giảm opacity của lớp phủ xuống 0.55 để ảnh nền rõ hơn
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0.55)), url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# GIAO DIỆN CHÍNH
# =========================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        color: #17324d;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 30px 34px;
        border: 1px solid rgba(217, 237, 240, 0.7);
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(233,251,247,0.95) 55%, rgba(238,246,255,0.95) 100%);
        box-shadow: 0 18px 50px rgba(57, 91, 117, .10);
        margin-bottom: 22px;
    }

    .hero h1 {
        margin: 0;
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -.7px;
        color: #17324d;
    }

    .hero p {
        margin: 8px 0 0;
        color: #5f7185;
        font-size: 15px;
    }

    .section-title {
        font-size: 19px;
        font-weight: 800;
        color: #23445f;
        margin: 20px 0 10px;
        text-shadow: 0px 1px 2px rgba(255,255,255,0.8);
    }

    .card {
        border: 1px solid #dcecf0;
        border-radius: 18px;
        padding: 22px 24px;
        background: rgba(255, 255, 255, 0.92); /* Tăng độ đục của thẻ để chữ dễ đọc hơn */
        box-shadow: 0 10px 28px rgba(45, 82, 105, .08);
        margin-bottom: 14px;
    }

    .metric-card {
        border: 1px solid #d7ebe7;
        border-radius: 18px;
        padding: 20px;
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(239,251,248,0.95));
        min-height: 115px;
        box-shadow: 0 10px 26px rgba(49, 117, 112, .08);
    }

    .metric-label {
        color: #6d7f92;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #108b78;
    }

    .subtle {
        color: #7890a3;
        font-size: 13px;
    }

    .rule {
        height: 1px;
        background: #e4eef2;
        margin: 14px 0;
    }

    div[data-testid="stButton"] > button {
        border-radius: 12px;
        border: 0;
        padding: 0.75rem 1.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #22c7a6, #1e9ee8);
        color: white;
        box-shadow: 0 10px 24px rgba(30, 158, 232, .25);
    }

    div[data-testid="stButton"] > button:hover {
        filter: brightness(1.04);
        transform: translateY(-1px);
    }

    .info-box {
        border-left: 4px solid #1e9ee8;
        background: rgba(237, 248, 255, 0.95);
        padding: 12px 14px;
        border-radius: 0 12px 12px 0;
        color: #34536d;
        margin: 8px 0 16px;
    }

    .success-box {
        border-left: 4px solid #20b486;
        background: rgba(234, 251, 245, 0.95);
        padding: 12px 14px;
        border-radius: 0 12px 12px 0;
        color: #256451;
        margin: 8px 0 16px;
    }

    .danger-box {
        border-left: 4px solid #f47f7f;
        background: rgba(255, 241, 241, 0.95);
        padding: 12px 14px;
        border-radius: 0 12px 12px 0;
        color: #875052;
        margin: 8px 0 16px;
    }

    label, .stMarkdown p, .stMarkdown li {
        color: #3c5369 !important;
        font-weight: 500;
    }

    /* LÀM NỔI BẬT CÁC Ô NHẬP LIỆU */
    [data-baseweb="input"], [data-baseweb="select"], [data-baseweb="base-input"] {
        border-radius: 10px !important;
        border: 2px solid #94cce6 !important; /* Viền màu xanh nhạt nổi bật */
        background: #ffffff !important;       /* Nền trắng tinh 100% */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important; /* Đổ bóng để ô nổi lên */
        transition: all 0.2s ease-in-out;
    }

    [data-baseweb="input"]:focus-within, [data-baseweb="select"]:focus-within {
        border-color: #1e9ee8 !important; /* Viền đậm hơn khi click vào */
        box-shadow: 0 4px 14px rgba(30, 158, 232, 0.15) !important;
    }

    [data-baseweb="select"] > div {
        background: transparent !important; 
    }

    /* Nút chọn (Radio Button) */
    .stRadio label {
        background: #ffffff !important;
        border: 1px solid #94cce6;
        border-radius: 8px;
        padding: 8px 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-weight: 600;
    }

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #dcecf0;
        background: rgba(255,255,255,0.95);
    }

    .stRadio [role="radiogroup"] {
        gap: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# HÀM XỬ LÝ NGÀY VÀ ĐỊNH DẠNG SỐ
# =========================
def add_months(d: date, months: int) -> date:
    total = d.year * 12 + (d.month - 1) + months
    year = total // 12
    month = total % 12 + 1

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    last_day = (next_month - timedelta(days=1)).day
    day = min(d.day, last_day)
    return date(year, month, day)

def money(v: float) -> str:
    return f"{v:,.0f} VNĐ".replace(",", ".")

def rate(v: float) -> str:
    return f"{v:.2f}%"


# =========================
# TÍNH TOÁN
# =========================
def calculate_deposit(
    principal: float,
    term_rate: float,
    non_term_rate: float,
    deposit_date: date,
    withdraw_date: date,
    term_months: int,
    payout_mode: str,
):
    if withdraw_date <= deposit_date:
        raise ValueError("Ngày rút phải sau ngày gửi.")

    current_start = deposit_date
    total_interest_paid = 0.0
    settlement_cash = 0.0
    breakdown = []
    cycle_no = 1
    principal_current = principal
    early_withdrawal = False
    max_cycles = 5000

    while current_start < withdraw_date and cycle_no <= max_cycles:
        maturity = add_months(current_start, term_months)

        if withdraw_date < maturity:
            early_withdrawal = True
            days = (withdraw_date - current_start).days
            actual_interest = (principal_current * (non_term_rate / 100.0) * days / 365.0)
            paid_in_current_cycle = 0.0

            if payout_mode == "Nhận lãi trước":
                planned_days = (maturity - current_start).days
                paid_in_current_cycle = (principal_current * (term_rate / 100.0) * planned_days / 365.0)
            elif payout_mode == "Nhận lãi hàng tháng":
                paid_in_current_cycle = 0.0
                month_cursor = current_start
                while True:
                    next_month = add_months(current_start, (month_cursor.month - current_start.month) + 12 * (month_cursor.year - current_start.year) + 1)
                    if next_month >= withdraw_date or next_month >= maturity:
                        break
                    days_month = (next_month - month_cursor).days
                    paid_in_current_cycle += (principal_current * (term_rate / 100.0) * days_month / 365.0)
                    month_cursor = next_month

            settlement_cash = principal_current + actual_interest - paid_in_current_cycle
            total_interest_paid += paid_in_current_cycle

            breakdown.append({
                "Vòng": cycle_no,
                "Từ ngày": current_start.strftime("%d/%m/%Y"),
                "Đến ngày": withdraw_date.strftime("%d/%m/%Y"),
                "Số ngày": days,
                "Trạng thái": "Rút trước hạn",
                "Lãi suất áp dụng": rate(non_term_rate),
                "Tiền gốc": principal_current,
                "Lãi tính lại": actual_interest,
                "Lãi đã trả trong kỳ": paid_in_current_cycle,
                "Tiền quyết toán": settlement_cash,
            })
            break

        days = (maturity - current_start).days
        cycle_interest = (principal_current * (term_rate / 100.0) * days / 365.0)

        if maturity == withdraw_date:
            final_cash = principal_current + cycle_interest
            total_interest_paid += 0.0

            if payout_mode == "Nhận lãi trước":
                planned_days = days
                interest_paid_current = (principal_current * (term_rate / 100.0) * planned_days / 365.0)
                final_cash = principal_current
                total_interest_paid += interest_paid_current
                settlement_cash = final_cash
                status = "Đến hạn – lãi đã nhận trước"
            elif payout_mode == "Nhận lãi hàng tháng":
                paid_monthly = 0.0
                month_cursor = current_start
                while True:
                    next_month = add_months(current_start, (month_cursor.month - current_start.month) + 12 * (month_cursor.year - current_start.year) + 1)
                    if next_month > maturity or next_month == maturity:
                        break
                    month_days = (next_month - month_cursor).days
                    paid_monthly += (principal_current * (term_rate / 100.0) * month_days / 365.0)
                    month_cursor = next_month

                remaining_interest = max(0.0, cycle_interest - paid_monthly)
                total_interest_paid += paid_monthly + remaining_interest
                settlement_cash = principal_current + remaining_interest
                final_cash = settlement_cash
                status = "Đến hạn – trả lãi kỳ cuối"
            else:
                total_interest_paid += cycle_interest
                settlement_cash = principal_current + cycle_interest
                final_cash = settlement_cash
                status = "Đến hạn – nhận lãi cuối kỳ"

            breakdown.append({
                "Vòng": cycle_no,
                "Từ ngày": current_start.strftime("%d/%m/%Y"),
                "Đến ngày": maturity.strftime("%d/%m/%Y"),
                "Số ngày": days,
                "Trạng thái": status,
                "Lãi suất áp dụng": rate(term_rate),
                "Tiền gốc": principal_current,
                "Lãi tính": cycle_interest,
                "Lãi đã trả trong vòng": total_interest_paid,
                "Tiền quyết toán": final_cash,
            })
            break

        if payout_mode == "Nhận lãi trước" or payout_mode == "Nhận lãi hàng tháng" or payout_mode == "Nhận lãi cuối kỳ":
            cycle_paid = cycle_interest
            total_interest_paid += cycle_paid
            settlement_cycle = principal_current

        breakdown.append({
            "Vòng": cycle_no,
            "Từ ngày": current_start.strftime("%d/%m/%Y"),
            "Đến ngày": maturity.strftime("%d/%m/%Y"),
            "Số ngày": days,
            "Trạng thái": "Đã đáo hạn và tái tục",
            "Lãi suất áp dụng": rate(term_rate),
            "Tiền gốc": principal_current,
            "Lãi tính": cycle_interest,
            "Lãi đã trả": cycle_paid,
            "Tiền quyết toán": settlement_cycle,
        })

        current_start = maturity
        cycle_no += 1

    if cycle_no > max_cycles:
        raise RuntimeError("Khoảng thời gian quá lớn, số vòng tái tục vượt giới hạn an toàn.")

    total_received = total_interest_paid + settlement_cash

    return {
        "principal": principal,
        "term_rate": term_rate,
        "non_term_rate": non_term_rate,
        "deposit_date": deposit_date,
        "withdraw_date": withdraw_date,
        "term_months": term_months,
        "payout_mode": payout_mode,
        "interest_total": total_received - principal,
        "interest_paid_before_settlement": total_interest_paid,
        "settlement_cash": settlement_cash,
        "total_received": total_received,
        "early_withdrawal": early_withdrawal,
        "breakdown": breakdown,
    }

# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class="hero">
        <h1>💰 Tính tiền lãi của Võ Hoàn Khang</h1>
        <p>Công cụ tính tiền lãi tiền gửi • Tái tục tự động • Xử lý rút trước hạn</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# INPUT
# =========================
left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown('<div class="section-title">Thông tin tiền gửi</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    principal = st.number_input("Số tiền khách hàng gửi (VNĐ)", min_value=0.0, value=100_000_000.0, step=1_000_000.0, format="%.0f")

    c1, c2 = st.columns(2)
    with c1:
        term_rate = st.number_input("Lãi suất có kỳ hạn (%/năm)", min_value=0.0, value=5.5, step=0.1, format="%.2f")
    with c2:
        non_term_rate = st.number_input("Lãi suất không kỳ hạn (%/năm)", min_value=0.0, value=0.2, step=0.05, format="%.2f")

    c3, c4 = st.columns(2)
    with c3:
        deposit_date = st.date_input("Ngày gửi tiền", value=date.today(), format="DD/MM/YYYY")
    with c4:
        withdraw_date = st.date_input("Ngày rút tiền", value=add_months(date.today(), 6), format="DD/MM/YYYY")

    term_options = {
        "1 tháng": 1, "2 tháng": 2, "3 tháng": 3, "6 tháng": 6,
        "9 tháng": 9, "12 tháng": 12, "18 tháng": 18, "24 tháng": 24,
        "36 tháng": 36, "48 tháng": 48, "60 tháng": 60,
    }

    term_label = st.selectbox("Kỳ hạn gửi tiền", list(term_options.keys()), index=3)
    term_months = term_options[term_label]

    payout_mode = st.radio("Cách nhận tiền lãi", ["Nhận lãi trước", "Nhận lãi hàng tháng", "Nhận lãi cuối kỳ"], horizontal=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
        <b>Quy tắc tính:</b> ngày tính lãi được tính từ ngày gửi đến trước ngày đáo hạn/rút tiền.
        Nếu qua ngày đáo hạn mà khách chưa rút, tiền gửi sẽ tự động tái tục đúng kỳ hạn đã chọn.
        Khi rút trước hạn, vòng đang gửi được áp dụng lãi suất không kỳ hạn.
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown('<div class="section-title">Tóm tắt giao dịch</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write(f"**Gốc ban đầu:** {money(principal)}")
    st.write(f"**Kỳ hạn:** {term_label}")
    st.write(f"**Lãi có kỳ hạn:** {rate(term_rate)}/năm")
    st.write(f"**Lãi không kỳ hạn:** {rate(non_term_rate)}/năm")
    st.write(f"**Ngày gửi:** {deposit_date.strftime('%d/%m/%Y')}")
    st.write(f"**Ngày rút:** {withdraw_date.strftime('%d/%m/%Y')}")
    st.write(f"**Hình thức nhận lãi:** {payout_mode}")

    st.markdown("</div>", unsafe_allow_html=True)

    if withdraw_date <= deposit_date:
        st.markdown('<div class="danger-box">Ngày rút phải sau ngày gửi.</div>', unsafe_allow_html=True)

    calculate = st.button("🧮 TÍNH TOÁN", use_container_width=True)

# =========================
# KẾT QUẢ
# =========================
if calculate:
    if principal <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if withdraw_date <= deposit_date:
        st.error("Ngày rút phải sau ngày gửi.")
        st.stop()

    try:
        result = calculate_deposit(
            principal=principal,
            term_rate=term_rate,
            non_term_rate=non_term_rate,
            deposit_date=deposit_date,
            withdraw_date=withdraw_date,
            term_months=term_months,
            payout_mode=payout_mode,
        )
    except Exception as e:
        st.error(f"Không thể tính toán: {e}")
        st.stop()

    st.markdown('<div class="section-title">Kết quả</div>', unsafe_allow_html=True)

    if result["early_withdrawal"]:
        st.markdown(
            """
            <div class="danger-box">
            <b>Rút trước hạn:</b> vòng tiền gửi hiện tại được tính lại theo lãi suất không kỳ hạn.
            Nếu khách đã nhận lãi trước/hàng tháng trong vòng hiện tại, khoản đó được đối trừ khi quyết toán.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="success-box">
            <b>Giao dịch đến hạn:</b> các vòng đã đáo hạn được xử lý và tự động tái tục đúng kỳ hạn đã chọn.
            </div>
            """,
            unsafe_allow_html=True,
        )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Tiền gốc ban đầu</div><div class="metric-value">{money(result["principal"])}</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Tổng tiền lãi</div><div class="metric-value">{money(result["interest_total"])}</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Tiền quyết toán cuối</div><div class="metric-value">{money(result["settlement_cash"])}</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Tổng giá trị khách nhận</div><div class="metric-value">{money(result["total_received"])}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Chi tiết từng vòng tiền gửi</div>', unsafe_allow_html=True)

    rows = []
    for item in result["breakdown"]:
        rows.append({
            "Vòng": item.get("Vòng"),
            "Từ ngày": item.get("Từ ngày"),
            "Đến ngày": item.get("Đến ngày"),
            "Số ngày": item.get("Số ngày"),
            "Trạng thái": item.get("Trạng thái"),
            "Lãi suất": item.get("Lãi suất áp dụng"),
            "Tiền gốc": money(item.get("Tiền gốc", 0)),
            "Lãi": money(item.get("Lãi tính", item.get("Lãi tính lại", 0))),
            "Lãi đã trả": money(item.get("Lãi đã trả", item.get("Lãi đã trả trong vòng", 0))),
            "Tiền quyết toán": money(item.get("Tiền quyết toán", 0)),
        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Vòng": st.column_config.NumberColumn(width="small"),
            "Số ngày": st.column_config.NumberColumn(width="small"),
        },
    )

    st.markdown(
        f"""
        <div class="card">
            <div><b>Hình thức nhận lãi:</b> {payout_mode}</div>
            <div class="rule"></div>
            <div><b>Tổng lãi:</b> {money(result["interest_total"])}</div>
            <div><b>Tiền quyết toán cuối cùng:</b> {money(result["settlement_cash"])}</div>
            <div><b>Tổng giá trị khách nhận:</b> {money(result["total_received"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("ℹ️ Lưu ý về mô hình tính toán"):
        st.markdown(
            """
            - Lãi suất được nhập theo **%/năm**, quy đổi số ngày theo **365 ngày**.
            - Ngày gửi được tính, ngày kết thúc kỳ/rút tiền là mốc kết thúc nên số ngày tính lãi là `ngày_kết_thúc - ngày_bắt_đầu`.
            - Nếu chưa rút khi đến hạn, tiền gửi được **tái tục đúng kỳ hạn đã chọn**.
            - Với **nhận lãi trước** hoặc **nhận lãi hàng tháng**, lãi đã chi trả trong vòng đang rút trước hạn sẽ được **đối trừ** khi quyết toán.
            - Với **nhận lãi cuối kỳ**, lãi của vòng đã đáo hạn được ghi nhận tại thời điểm đáo hạn.
            - Đây là công cụ mô phỏng nghiệp vụ; quy định thực tế của từng ngân hàng có thể khác về cách tính ngày, cơ chế tái tục và xử lý lãi đã trả khi tất toán trước hạn.
            """
        )
else:
    st.markdown(
        """
        <div class="card" style="text-align:center; padding:34px;">
            <div style="font-size:44px;">🏦</div>
            <div style="font-size:22px; font-weight:800; margin-top:8px;">Sẵn sàng tính tiền gửi</div>
            <div class="subtle" style="margin-top:8px;">
                Nhập thông tin giao dịch ở trên rồi nhấn <b>TÍNH TOÁN</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="text-align:center; color:#7b93a6; font-size:12px; margin-top:28px;">
        Smart Deposit Calculator • Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
