import streamlit as st
import calendar
from datetime import date

st.set_page_config(page_title="Tính lãi tiết kiệm_Võ Hoàn Khang", page_icon="◆", layout="centered")

# ============================================================================
# TOKEN HỆ THỐNG THIẾT KẾ
#   Màu nền  : #0A1420 (navy gần đen, chất liệu "két sắt")
#   Bề mặt   : #101C2B / #142335
#   Viền     : #223349
#   Vàng     : #C9A961 (vàng đồng, dịu — điểm nhấn duy nhất)
#   Chữ chính: #ECEEF1     Chữ phụ: #8B97A8
#   Tích cực : #7FBF9E (sage)   Cảnh báo: #C9A961   Lỗi: #C97B6B
#   Font hiển thị số/tiêu đề: Fraunces (serif có cá tính)
#   Font nội dung: Inter
#   Bố cục: dạng "bảng sao kê" — không dùng card/bóng đổ, chỉ dùng
#           đường kẻ mảnh (hairline) màu vàng để phân tách.
# ============================================================================

PALETTE = {
    "bg": "#0A1420",
    "surface": "#101C2B",
    "surface2": "#14233A",
    "border": "#223349",
    "gold": "#C9A961",
    "gold_soft": "rgba(201,169,97,0.16)",
    "text": "#ECEEF1",
    "muted": "#8B97A8",
    "positive": "#7FBF9E",
    "warn": "#C9A961",
    "error": "#C97B6B",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: radial-gradient(ellipse 1200px 600px at 50% -10%, #101F30 0%, {PALETTE['bg']} 55%);
    color: {PALETTE['text']};
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.block-container {{
    max-width: 760px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}}

/* ---------- Hero ---------- */
.hero-eyebrow {{
    color: {PALETTE['gold']};
    font-size: 0.82rem;
    letter-spacing: 0.02em;
    margin-bottom: 0.3rem;
    font-weight: 500;
}}
.hero-title {{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 2.5rem;
    line-height: 1.15;
    color: {PALETTE['text']};
    margin: 0 0 0.6rem 0;
}}
.hero-sub {{
    color: {PALETTE['muted']};
    font-size: 1rem;
    line-height: 1.6;
    max-width: 560px;
    margin-bottom: 1.6rem;
}}
.gold-rule {{
    border: none;
    border-top: 1px solid {PALETTE['gold']};
    opacity: 0.55;
    margin: 1.6rem 0;
}}
.hair-rule {{
    border: none;
    border-top: 1px solid {PALETTE['border']};
    margin: 1.4rem 0;
}}

/* ---------- Section labels ---------- */
.section-label {{
    font-family: 'Fraunces', serif;
    font-size: 1.05rem;
    color: {PALETTE['text']};
    margin: 0.2rem 0 0.9rem 0;
    font-weight: 500;
}}

/* ---------- Inputs ---------- */
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
    background-color: {PALETTE['surface2']} !important;
    color: {PALETTE['text']} !important;
    border: 1px solid {PALETTE['border']} !important;
    border-radius: 3px !important;
}}
label[data-testid="stWidgetLabel"] p {{
    color: {PALETTE['muted']} !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
}}
[data-testid="stNumberInput"] button {{
    background-color: {PALETTE['surface2']} !important;
    border-color: {PALETTE['border']} !important;
    color: {PALETTE['gold']} !important;
}}

/* ---------- Radio -> segmented tabs ---------- */
[data-testid="stRadio"] > div {{
    gap: 0.4rem;
}}
[data-testid="stRadio"] label {{
    background-color: {PALETTE['surface']};
    border: 1px solid {PALETTE['border']};
    padding: 0.5rem 1rem;
    border-radius: 3px;
    margin-right: 0;
}}
[data-testid="stRadio"] label:has(input:checked) {{
    border-color: {PALETTE['gold']};
    background-color: {PALETTE['gold_soft']};
}}
[data-testid="stRadio"] label div p {{
    color: {PALETTE['text']} !important;
    font-size: 0.88rem;
}}

/* ---------- Button ---------- */
.stButton > button {{
    background-color: {PALETTE['gold']};
    color: #16212E;
    border: none;
    border-radius: 3px;
    font-weight: 600;
    padding: 0.7rem 1rem;
    letter-spacing: 0.01em;
    transition: background-color 0.15s ease;
}}
.stButton > button:hover {{
    background-color: #DDBE7C;
    color: #16212E;
}}
.stButton > button:active {{
    background-color: #B6944F;
}}

/* ---------- Alerts fallback (validation errors) ---------- */
[data-testid="stAlert"] {{
    background-color: {PALETTE['surface']} !important;
    border: 1px solid {PALETTE['border']} !important;
    border-left: 3px solid {PALETTE['error']} !important;
    color: {PALETTE['text']} !important;
    border-radius: 2px !important;
}}

/* ---------- Expander ---------- */
[data-testid="stExpander"] {{
    border: 1px solid {PALETTE['border']} !important;
    border-radius: 3px !important;
    background-color: {PALETTE['surface']} !important;
}}
[data-testid="stExpander"] summary {{
    color: {PALETTE['muted']} !important;
    font-size: 0.9rem;
}}

/* ---------- Custom banner ---------- */
.banner {{
    border-left: 3px solid {PALETTE['gold']};
    background-color: {PALETTE['surface']};
    padding: 0.85rem 1.1rem;
    margin: 0.9rem 0;
    border-radius: 2px;
    font-size: 0.92rem;
    line-height: 1.55;
    color: {PALETTE['text']};
}}
.banner.positive {{ border-left-color: {PALETTE['positive']}; }}
.banner.warn {{ border-left-color: {PALETTE['warn']}; }}
.banner.muted {{ border-left-color: {PALETTE['border']}; color: {PALETTE['muted']}; }}

/* ---------- Ledger summary row ---------- */
.ledger-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 1.6rem 0 1.4rem 0;
}}
.ledger-item {{
    flex: 1;
    padding-right: 1.2rem;
}}
.ledger-item .l {{
    color: {PALETTE['muted']};
    font-size: 0.82rem;
    margin-bottom: 0.35rem;
}}
.ledger-item .v {{
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    color: {PALETTE['text']};
    font-weight: 500;
}}
.ledger-item.total .v {{
    color: {PALETTE['gold']};
    font-size: 2.05rem;
}}
.ledger-item.total .l {{
    color: {PALETTE['gold']};
}}

/* ---------- Ledger table ---------- */
table.ledger-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
    margin: 0.6rem 0 1.2rem 0;
}}
table.ledger-table th {{
    text-align: left;
    color: {PALETTE['muted']};
    font-weight: 500;
    font-size: 0.78rem;
    padding: 0.5rem 0.7rem;
    border-bottom: 1px solid {PALETTE['gold']};
}}
table.ledger-table td {{
    padding: 0.6rem 0.7rem;
    border-bottom: 1px solid {PALETTE['border']};
    color: {PALETTE['text']};
}}
table.ledger-table tr:last-child td {{
    border-bottom: none;
}}
table.ledger-table td.num, table.ledger-table th.num {{
    text-align: right;
    font-variant-numeric: tabular-nums;
}}
table.ledger-table td.tag {{
    color: {PALETTE['muted']};
    font-size: 0.84rem;
}}

footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# HÀM TÍNH TOÁN (logic giữ nguyên, không đổi)
# ----------------------------------------------------------------------------

def add_months(d: date, months: int) -> date:
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def split_into_monthly_chunks(start: date, end: date):
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
    return f"{x:,.0f} ₫".replace(",", ".")


def tinh_lai_tiet_kiem(principal, term_rate, demand_rate, deposit_date, withdrawal_date, term_months):
    periods = []
    current_start = deposit_date
    max_loops = 2000

    for _ in range(max_loops):
        maturity = add_months(current_start, term_months)

        if withdrawal_date >= maturity:
            days = (maturity - current_start).days
            interest = principal * (term_rate / 100.0) * days / 365.0
            periods.append({
                "start": current_start, "end": maturity, "days": days,
                "rate": term_rate, "rate_type": "Có kỳ hạn (đủ hạn)",
                "interest": interest, "completed": True,
            })
            current_start = maturity
            if withdrawal_date == maturity:
                break
            continue
        else:
            days = (withdrawal_date - current_start).days
            if days > 0:
                interest = principal * (demand_rate / 100.0) * days / 365.0
                periods.append({
                    "start": current_start, "end": withdrawal_date, "days": days,
                    "rate": demand_rate, "rate_type": "Không kỳ hạn (rút trước hạn)",
                    "interest": interest, "completed": False,
                })
            break

    total_interest = sum(p["interest"] for p in periods)
    return periods, total_interest


# ----------------------------------------------------------------------------
# GIAO DIỆN
# ----------------------------------------------------------------------------

st.markdown(f"""
<div class="hero-eyebrow">Công cụ tính lãi</div>
<div class="hero-title">Lãi tiết kiệm của bạn</div>
<div class="hero-sub">Nhập thông tin sổ tiết kiệm để xem số tiền lãi và tổng số tiền
nhận được khi đáo hạn — tự động xử lý trường hợp tái tục và rút trước hạn.</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Thông tin gửi tiền</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    so_tien = st.number_input("Số tiền gửi (VNĐ)", min_value=0.0, step=1_000_000.0,
                               value=100_000_000.0, format="%.0f")
    lai_suat_ky_han = st.number_input("Lãi suất có kỳ hạn (%/năm)", min_value=0.0,
                                       max_value=100.0, value=5.5, step=0.1, format="%.2f")
    lai_suat_khong_ky_han = st.number_input("Lãi suất không kỳ hạn (%/năm)", min_value=0.0,
                                             max_value=100.0, value=0.2, step=0.1, format="%.2f")
with col2:
    ngay_gui = st.date_input("Ngày gửi tiền", value=date(2024, 1, 10))
    ky_han_thang = st.selectbox("Kỳ hạn gửi tiền", options=[1, 2, 3, 6, 9, 12, 13, 18, 24, 36],
                                 format_func=lambda x: f"{x} tháng", index=2)
    ngay_rut = st.date_input("Ngày rút tiền", value=date(2024, 8, 15))

st.markdown('<div class="section-label" style="margin-top:0.4rem;">Hình thức nhận lãi</div>', unsafe_allow_html=True)
phuong_thuc = st.radio("Hình thức nhận lãi", ["Nhận lãi trước", "Nhận lãi hàng tháng", "Nhận lãi cuối kỳ"],
                        horizontal=True, label_visibility="collapsed")

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
tinh_toan = st.button("Tính toán", type="primary", use_container_width=True)

if tinh_toan:
    if ngay_rut <= ngay_gui:
        st.error("Ngày rút tiền phải sau ngày gửi tiền. Vui lòng kiểm tra lại.")
    elif so_tien <= 0:
        st.error("Số tiền gửi phải lớn hơn 0.")
    else:
        periods, total_interest = tinh_lai_tiet_kiem(
            so_tien, lai_suat_ky_han, lai_suat_khong_ky_han, ngay_gui, ngay_rut, ky_han_thang
        )
        total_amount = so_tien + total_interest
        so_ky_dao_han = sum(1 for p in periods if p["completed"])
        rut_truoc_han = any(not p["completed"] for p in periods)

        st.markdown('<hr class="gold-rule">', unsafe_allow_html=True)

        # ----- Banner trạng thái -----
        if rut_truoc_han:
            last = periods[-1]
            mat = add_months(last["start"], ky_han_thang)
            st.markdown(f"""
            <div class="banner warn">
            Rút trước hạn của kỳ hiện hành ({last['start'].strftime('%d/%m/%Y')} – {mat.strftime('%d/%m/%Y')}).
            Phần thời gian chưa đủ kỳ hạn được tính theo lãi suất không kỳ hạn
            ({lai_suat_khong_ky_han}%/năm).
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="banner positive">
            Rút tiền đúng ngày đáo hạn — toàn bộ thời gian gửi được hưởng lãi suất có kỳ hạn.
            </div>
            """, unsafe_allow_html=True)

        if so_ky_dao_han > 0:
            st.markdown(f"""
            <div class="banner muted">
            Sổ tiết kiệm đã được ngân hàng tự động tái tục {so_ky_dao_han} kỳ
            (mỗi kỳ {ky_han_thang} tháng) trước khi rút tiền.
            </div>
            """, unsafe_allow_html=True)

        # ----- Ledger tổng hợp -----
        maturity_first = add_months(ngay_gui, ky_han_thang)
        st.markdown(f"""
        <div class="ledger-row">
            <div class="ledger-item">
                <div class="l">Tiền gốc</div>
                <div class="v">{fmt_money(so_tien)}</div>
            </div>
            <div class="ledger-item">
                <div class="l">Tổng tiền lãi</div>
                <div class="v">{fmt_money(total_interest)}</div>
            </div>
            <div class="ledger-item total">
                <div class="l">Tổng tiền nhận được</div>
                <div class="v">{fmt_money(total_amount)}</div>
            </div>
        </div>
        <div style="color:{PALETTE['muted']}; font-size:0.84rem; margin-bottom:0.4rem;">
            Đáo hạn ban đầu {maturity_first.strftime('%d/%m/%Y')} · tổng {(ngay_rut - ngay_gui).days} ngày gửi
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="hair-rule">', unsafe_allow_html=True)

        # ----- Bảng chi tiết theo kỳ -----
        st.markdown('<div class="section-label">Chi tiết lãi theo từng kỳ</div>', unsafe_allow_html=True)
        rows_html = ""
        for i, p in enumerate(periods, start=1):
            rows_html += f"""
            <tr>
                <td>{i}</td>
                <td>{p['start'].strftime('%d/%m/%Y')} – {p['end'].strftime('%d/%m/%Y')}</td>
                <td class="num">{p['days']}</td>
                <td class="tag">{p['rate_type']}</td>
                <td class="num">{p['rate']:.2f}%</td>
                <td class="num">{fmt_money(p['interest'])}</td>
            </tr>"""
        st.markdown(f"""
        <table class="ledger-table">
            <tr>
                <th>Kỳ</th><th>Thời gian</th><th class="num">Số ngày</th>
                <th>Loại lãi suất</th><th class="num">Lãi suất</th><th class="num">Tiền lãi</th>
            </tr>
            {rows_html}
        </table>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="hair-rule">', unsafe_allow_html=True)

        # ----- Chi tiết theo phương thức -----
        st.markdown(f'<div class="section-label">{phuong_thuc}</div>', unsafe_allow_html=True)

        if phuong_thuc == "Nhận lãi cuối kỳ":
            st.markdown(f"""
            <div class="banner muted">
            Toàn bộ tiền lãi {fmt_money(total_interest)} được cộng dồn và trả một lần cùng
            tiền gốc vào ngày rút tiền ({ngay_rut.strftime('%d/%m/%Y')}).
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <table class="ledger-table">
                <tr><th>Ngày nhận</th><th class="num">Số tiền</th><th>Ghi chú</th></tr>
                <tr>
                    <td>{ngay_rut.strftime('%d/%m/%Y')}</td>
                    <td class="num">{fmt_money(total_amount)}</td>
                    <td class="tag">Gốc + toàn bộ lãi</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)

        elif phuong_thuc == "Nhận lãi trước":
            st.markdown("""
            <div class="banner muted">
            Với mỗi kỳ đủ hạn, tiền lãi được tạm ứng ngay khi bắt đầu kỳ theo lãi suất
            có kỳ hạn. Nếu rút trước hạn của kỳ hiện hành, phần lãi tạm ứng dư (nếu có)
            sẽ được ngân hàng thu hồi khi tất toán.
            </div>
            """, unsafe_allow_html=True)
            rows2 = ""
            recovered = 0
            for p in periods:
                if p["completed"]:
                    rows2 += f"""
                    <tr>
                        <td>{p['start'].strftime('%d/%m/%Y')}</td>
                        <td class="num">{fmt_money(p['interest'])}</td>
                        <td class="tag">Lãi kỳ {p['start'].strftime('%d/%m/%Y')} – {p['end'].strftime('%d/%m/%Y')}</td>
                    </tr>"""
                else:
                    full_maturity = add_months(p["start"], ky_han_thang)
                    full_days = (full_maturity - p["start"]).days
                    prepaid_estimate = so_tien * (lai_suat_ky_han / 100.0) * full_days / 365.0
                    recovered = max(0, prepaid_estimate - p["interest"])
                    rows2 += f"""
                    <tr>
                        <td>{p['start'].strftime('%d/%m/%Y')} (tạm ứng)</td>
                        <td class="num">{fmt_money(prepaid_estimate)}</td>
                        <td class="tag">Điều chỉnh khi tất toán do rút trước hạn</td>
                    </tr>"""
            st.markdown(f"""
            <table class="ledger-table">
                <tr><th>Ngày nhận lãi</th><th class="num">Số tiền</th><th>Ghi chú</th></tr>
                {rows2}
            </table>
            """, unsafe_allow_html=True)
            if recovered > 0:
                st.markdown(f"""
                <div class="banner warn">
                Ngân hàng thu hồi phần lãi tạm ứng dư: {fmt_money(recovered)}.
                Tiền gốc hoàn trả khi tất toán: {fmt_money(so_tien - recovered)}.
                </div>
                """, unsafe_allow_html=True)

        else:  # Nhận lãi hàng tháng
            st.markdown("""
            <div class="banner muted">
            Tiền lãi được chi trả định kỳ hàng tháng trong suốt thời gian gửi;
            tiền gốc được hoàn trả khi rút tiền.
            </div>
            """, unsafe_allow_html=True)
            rows3 = ""
            for p in periods:
                for c_start, c_end in split_into_monthly_chunks(p["start"], p["end"]):
                    days = (c_end - c_start).days
                    interest_chunk = so_tien * (p["rate"] / 100.0) * days / 365.0
                    rows3 += f"""
                    <tr>
                        <td>{c_end.strftime('%d/%m/%Y')}</td>
                        <td class="num">{days}</td>
                        <td class="tag">{p['rate']:.2f}%/năm · {p['rate_type']}</td>
                        <td class="num">{fmt_money(interest_chunk)}</td>
                    </tr>"""
            st.markdown(f"""
            <table class="ledger-table">
                <tr><th>Ngày nhận lãi</th><th class="num">Số ngày</th><th>Lãi suất áp dụng</th><th class="num">Tiền lãi</th></tr>
                {rows3}
            </table>
            <div style="color:{PALETTE['muted']}; font-size:0.86rem;">
                Khi rút tiền ({ngay_rut.strftime('%d/%m/%Y')}), tiền gốc {fmt_money(so_tien)} được hoàn trả.
            </div>
            """, unsafe_allow_html=True)

st.markdown('<hr class="hair-rule">', unsafe_allow_html=True)
with st.expander("Quy tắc tính lãi áp dụng"):
    st.markdown(f"""
- Số ngày tính lãi mỗi kỳ = từ ngày bắt đầu kỳ đến trước 1 ngày đáo hạn hoặc trước 1 ngày rút tiền (cơ sở 365 ngày/năm).
- Rút đúng hoặc sau ngày đáo hạn của một kỳ → kỳ đó hưởng trọn lãi suất có kỳ hạn.
- Đến hạn mà không rút → ngân hàng tự động tái tục đúng kỳ hạn ban đầu.
- Rút trước hạn của kỳ hiện hành → riêng phần thời gian đó tính theo lãi suất không kỳ hạn; các kỳ đã đáo hạn trước đó vẫn giữ nguyên lãi suất có kỳ hạn.
- Công thức lãi đơn: Tiền lãi = Số tiền gửi × Lãi suất (%/năm) × Số ngày / 365.
    """)
