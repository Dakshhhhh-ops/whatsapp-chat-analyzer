import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChatLens",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Page background ── */
.stApp { background: #0f1117; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #161b27 !important;
    border-right: 1px solid #1e2535;
}
[data-testid="stSidebar"] > div:first-child { padding: 0; }

/* ── Sidebar upload area ── */
[data-testid="stFileUploader"] {
    background: #1a2033;
    border: 1px dashed #2a3550;
    border-radius: 10px;
    padding: 8px;
}
[data-testid="stFileUploader"]:hover { border-color: #3d85f5; }

/* ── Sidebar selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #1a2033 !important;
    border: 1px solid #1e2535 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #3d85f5 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    transition: background 0.2s;
}
.stButton > button:hover { background: #2563eb !important; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 12px;
    padding: 16px 20px !important;
}
[data-testid="stMetricLabel"] > div {
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricValue"] > div {
    color: #f1f5f9 !important;
    font-size: 28px !important;
    font-weight: 600 !important;
}
[data-testid="stMetricDelta"] > div { font-size: 12px !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e2535 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── Divider ── */
hr { border-color: #1e2535 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #161b27;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid #1e2535;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 7px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: #1e2a42 !important;
    color: #3d85f5 !important;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 28px 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #1e2535;
}
.section-header h3 {
    color: #94a3b8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0;
}
.section-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #3d85f5;
    flex-shrink: 0;
}

/* ── Page title area ── */
.page-title {
    padding: 24px 32px 0 32px;
}
.page-title h1 {
    color: #f1f5f9;
    font-size: 22px;
    font-weight: 600;
    margin: 0 0 4px 0;
}
.page-title p {
    color: #64748b;
    font-size: 13px;
    margin: 0;
}

/* ── Content area ── */
.content-pad { padding: 0 32px 32px 32px; }

/* ── Sidebar title ── */
.sidebar-title {
    padding: 22px 20px 16px 20px;
    border-bottom: 1px solid #1e2535;
    margin-bottom: 4px;
}
.sidebar-title h2 {
    color: #f1f5f9;
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 2px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sidebar-title p {
    color: #475569;
    font-size: 11px;
    margin: 0;
}
.brand-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #3d85f5;
    display: inline-block;
}

/* ── Emoji pills ── */
.emoji-pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 4px 0;
}
.emoji-pill {
    background: #1a2033;
    border: 1px solid #1e2535;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 13px;
    color: #e2e8f0;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.emoji-pill .count {
    color: #64748b;
    font-size: 11px;
    font-weight: 500;
}

/* ── Stat badge ── */
.stat-badge {
    background: #1a2033;
    border: 1px solid #1e2535;
    border-radius: 10px;
    padding: 14px 18px;
    text-align: center;
}
.stat-badge .val {
    font-size: 24px;
    font-weight: 600;
    color: #f1f5f9;
}
.stat-badge .lbl {
    font-size: 11px;
    color: #64748b;
    margin-top: 3px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
}

/* ── User badge in sidebar ── */
.user-badge {
    margin: 4px 12px;
    padding: 10px 12px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    transition: background 0.15s;
}
.user-badge:hover { background: #1a2033; }
.user-badge.active { background: #1a2a45; }
.user-avatar {
    width: 28px; height: 28px;
    border-radius: 50%;
    background: #1e3a5f;
    color: #3d85f5;
    font-size: 10px;
    font-weight: 600;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.user-name { color: #cbd5e1; font-size: 13px; font-weight: 500; flex: 1; }
.user-count { color: #475569; font-size: 11px; }

/* ── Chart wrapper ── */
.chart-box {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 12px;
    padding: 20px;
}

/* ── Wordcloud container ── */
.wc-container {
    background: #161b27;
    border: 1px solid #1e2535;
    border-radius: 12px;
    padding: 8px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #1e2535; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ───────────────────────────────────────────────────────
CHART_BG    = "#161b27"
CHART_TEXT  = "#94a3b8"
CHART_GRID  = "#1e2535"
ACCENT_BLUE = "#3d85f5"
ACCENT_GREEN= "#22c55e"
ACCENT_AMB  = "#f59e0b"
ACCENT_CORAL= "#f87171"

def apply_chart_style(fig, ax):
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)
    ax.tick_params(colors=CHART_TEXT, labelsize=10)
    ax.xaxis.label.set_color(CHART_TEXT)
    ax.yaxis.label.set_color(CHART_TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(CHART_GRID)
    ax.grid(axis='y', color=CHART_GRID, linewidth=0.5, alpha=0.7)
    ax.grid(axis='x', visible=False)

# ── Sidebar — only shown after analysis is running ────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
        <h2><span class="brand-dot"></span> ChatLens</h2>
        <p>WhatsApp conversation analyzer</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("df_loaded"):
        df   = st.session_state["df"]
        st.markdown("<div style='padding: 12px 12px 4px; font-size:11px; color:#475569; text-transform:uppercase; letter-spacing:0.06em; font-weight:600;'>Participants</div>", unsafe_allow_html=True)

        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.selectbox(
            "Analyse as", user_list, label_visibility="collapsed",
            key="sidebar_user_select"
        )
        st.session_state.selected_user = selected_user

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        user_msg_counts = df[df['user'] != 'group_notification']['user'].value_counts()
        total = len(df)
        for u in user_list[1:]:
            count    = user_msg_counts.get(u, 0)
            initials = "".join(p[0].upper() for p in u.split()[:2])
            st.markdown(f"""
            <div class="user-badge">
                <div class="user-avatar">{initials}</div>
                <span class="user-name">{u}</span>
                <span class="user-count">{count:,}</span>
            </div>""", unsafe_allow_html=True)

# ── Main content ───────────────────────────────────────────────────────────────
if not st.session_state.get("df_loaded"):
    # ── Landing page ──
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown(
            "<div style='text-align:center;padding:60px 0 16px;'>"
            "<div style='font-size:44px;margin-bottom:18px;'>&#128172;</div>"
            "<h1 style='color:#f1f5f9;font-size:26px;font-weight:600;margin:0 0 10px;'>"
            "Drop your chat, discover the story</h1>"
            "<p style='color:#475569;font-size:13px;line-height:1.75;margin:0 0 28px;'>"
            "Export a WhatsApp conversation<br>"
            "<span style='color:#334155;font-size:12px;'>"
            "Settings &#8594; Chat &#8594; Export chat &#8594; Without media"
            "</span></p></div>",
            unsafe_allow_html=True
        )

        landing_file = st.file_uploader(
            "chat", type=["txt"], label_visibility="collapsed", key="landing_uploader"
        )

        if landing_file:
            if st.button("Run analysis →", use_container_width=True):
                raw = landing_file.getvalue().decode("utf-8")
                df  = preprocessor.preprocess(raw)
                st.session_state["df"]        = df
                st.session_state["df_loaded"] = True
                st.session_state["selected_user"] = "Overall"
                st.rerun()

        st.markdown(
            "<div style='text-align:center;margin-top:32px;display:flex;gap:20px;"
            "justify-content:center;flex-wrap:wrap;color:#2a3550;font-size:11px;'>"
            "<span>&#128202; Message stats</span>"
            "<span>&#128336; Activity patterns</span>"
            "<span>&#128514; Emoji analysis</span>"
            "<span>&#9729; Word clouds</span></div>",
            unsafe_allow_html=True
        )
    st.stop()

# ── Analysis — df is in session state ─────────────────────────────────────────
df = st.session_state["df"]

# ── Analysis ────────────────────────────────────────────────────────────────────

# Build user list for the inline dropdown
_df = st.session_state["df"]
_user_list = _df['user'].unique().tolist()
_user_list.sort()
_user_list.insert(0, "Overall")

# Header row: title on left, user dropdown on right
hdr_left, hdr_right = st.columns([3, 1])
with hdr_left:
    st.markdown(
        "<div style='padding:24px 0 0 32px;'>"
        "<h1 style='color:#f1f5f9;font-size:22px;font-weight:600;margin:0 0 2px;'>ChatLens</h1>"
        "<p style='color:#64748b;font-size:13px;margin:0;'>WhatsApp conversation analysis</p>"
        "</div>",
        unsafe_allow_html=True
    )
with hdr_right:
    st.markdown("<div style='padding-top:20px;padding-right:24px;'>", unsafe_allow_html=True)
    selected_box = st.selectbox(
        "View analysis for",
        _user_list,
        index=_user_list.index(st.session_state.get("selected_user", "Overall")),
        key="main_user_select",
        label_visibility="collapsed",
    )
    st.session_state["selected_user"] = selected_box
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f"<div style='padding:0 32px 12px 32px;'>"
    f"<span style='color:#94a3b8;font-size:12px;font-weight:600;text-transform:uppercase;"
    f"letter-spacing:0.06em;'>Analysing: </span>"
    f"<span style='color:#3d85f5;font-size:12px;font-weight:600;'>{selected_box}</span>"
    f"</div>",
    unsafe_allow_html=True
)

num_messages, num_words, num_images, num_videos, num_audio, num_stickers, num_gifs, num_links = \
    helper.fetch_stats(selected_box, df)

st.markdown("<div class='content-pad'>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_overview, tab_timeline, tab_media, tab_raw = st.tabs(
    ["📊  Overview", "📅  Timeline", "📁  Media & Links", "🗃  Raw data"]
)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab_overview:

    # ── Metric row ──
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3>Summary</h3>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Messages",    f"{num_messages:,}")
    c2.metric("Words",       f"{num_words:,}",  delta=f"~{round(num_words/max(num_messages,1),1)} per msg")
    c3.metric("Links shared",f"{num_links:,}")
    c4.metric("Media files", f"{num_images + num_videos + num_audio + num_stickers + num_gifs:,}")

    # ── Busiest users (Overall only) ──
    if selected_box == "Overall":
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>Most active participants</h3>
        </div>""", unsafe_allow_html=True)

        x, percent = helper.busiest_users(df)
        col_chart, col_table = st.columns([3, 2])

        with col_chart:
            colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMB, ACCENT_CORAL, "#a78bfa"]
            fig, ax = plt.subplots(figsize=(6, 3.2))
            bars = ax.barh(x.index[::-1], x.values[::-1],
                           color=colors[:len(x)], height=0.55)
            apply_chart_style(fig, ax)
            ax.set_xlabel("Messages", color=CHART_TEXT, fontsize=10)
            ax.bar_label(bars, fmt="{:,.0f}", color=CHART_TEXT, fontsize=9, padding=4)
            ax.set_xlim(0, x.values.max() * 1.18)
            ax.grid(visible=False)
            plt.tight_layout(pad=0.6)
            st.pyplot(fig, use_container_width=True)

        with col_table:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if hasattr(percent, "columns"):
                pct_display = percent.rename(columns={percent.columns[0]: "Share %"})
            else:
                pct_display = percent.rename("Share %").to_frame()
            st.dataframe(pct_display, use_container_width=True, height=200)

    # ── Word cloud ──
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3>Most used words</h3>
    </div>""", unsafe_allow_html=True)

    df_wc = helper.create_wordcloud(selected_box, df)
    fig, ax = plt.subplots(figsize=(10, 3.5))
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)
    ax.imshow(df_wc)
    ax.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig, use_container_width=True)

    # ── Emoji analysis ──
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3>Emoji usage</h3>
    </div>""", unsafe_allow_html=True)

    emoji_df = pd.DataFrame(helper.emoji_helper(selected_box, df), columns=["emoji", "count"])
    top10 = emoji_df.head(10)

    col_ep, col_eb = st.columns([2, 3])

    with col_ep:
        # Pills
        pills_html = '<div class="emoji-pill-row">'
        for _, row in top10.iterrows():
            pills_html += f'<div class="emoji-pill">{row["emoji"]} <span class="count">{int(row["count"]):,}×</span></div>'
        pills_html += "</div>"
        st.markdown(pills_html, unsafe_allow_html=True)

    with col_eb:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.barh(top10["emoji"][::-1], top10["count"][::-1], color=ACCENT_BLUE, height=0.6)
        apply_chart_style(fig, ax)
        ax.set_xlabel("Count", color=CHART_TEXT, fontsize=10)
        plt.tight_layout(pad=0.5)
        st.pyplot(fig, use_container_width=True)

    # ── Activity heatmap ──
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3>Weekly activity heatmap</h3>
    </div>""", unsafe_allow_html=True)

    heatmap = helper.activity_heatmap(selected_box, df)
    fig, ax = plt.subplots(figsize=(11, 3.2))
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)

    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("chatlens", ["#1a2033", ACCENT_BLUE], N=256)

    im = ax.imshow(heatmap.values, aspect="auto", cmap=cmap)
    ax.set_xticks(range(len(heatmap.columns)))
    ax.set_xticklabels(heatmap.columns, rotation=45, ha="right",
                       color=CHART_TEXT, fontsize=9)
    ax.set_yticks(range(len(heatmap.index)))
    ax.set_yticklabels(heatmap.index, color=CHART_TEXT, fontsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)

    cbar = plt.colorbar(im, ax=ax, fraction=0.015, pad=0.01)
    cbar.ax.yaxis.set_tick_params(color=CHART_TEXT, labelsize=8)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=CHART_TEXT)
    cbar.outline.set_edgecolor(CHART_GRID)

    plt.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TIMELINE
# ═══════════════════════════════════════════════════════════════════════════════
with tab_timeline:

    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3>Monthly message volume</h3>
    </div>""", unsafe_allow_html=True)

    timeline = helper.monthly_timeline(selected_box, df)
    fig, ax = plt.subplots(figsize=(11, 3.5))
    ax.plot(timeline["time"], timeline["message"],
            color=ACCENT_BLUE, linewidth=2, marker="o",
            markersize=4, markerfacecolor=ACCENT_BLUE)
    ax.fill_between(timeline["time"], timeline["message"],
                    alpha=0.12, color=ACCENT_BLUE)
    apply_chart_style(fig, ax)
    ax.set_ylabel("Messages", color=CHART_TEXT, fontsize=10)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)

    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3>Daily message volume</h3>
    </div>""", unsafe_allow_html=True)

    daily = helper.daily_timelime(selected_box, df)
    fig, ax = plt.subplots(figsize=(11, 3))
    ax.plot(daily["only_date"], daily["message"],
            color=ACCENT_GREEN, linewidth=1.2, alpha=0.9)
    ax.fill_between(daily["only_date"], daily["message"],
                    alpha=0.08, color=ACCENT_GREEN)
    apply_chart_style(fig, ax)
    ax.set_ylabel("Messages", color=CHART_TEXT, fontsize=10)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)

    col_m, col_d = st.columns(2)

    with col_m:
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>Busiest months</h3>
        </div>""", unsafe_allow_html=True)
        busy_month = helper.month_activity_map(selected_box, df)
        fig, ax = plt.subplots(figsize=(5, 3.2))
        ax.bar(busy_month.index, busy_month.values, color=ACCENT_BLUE,
               width=0.6, edgecolor=CHART_BG)
        apply_chart_style(fig, ax)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout(pad=0.5)
        st.pyplot(fig, use_container_width=True)

    with col_d:
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>Busiest days of week</h3>
        </div>""", unsafe_allow_html=True)
        busy_day = helper.week_activity_map(selected_box, df)
        fig, ax = plt.subplots(figsize=(5, 3.2))
        ax.bar(busy_day.index, busy_day.values, color=ACCENT_AMB,
               width=0.6, edgecolor=CHART_BG)
        apply_chart_style(fig, ax)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout(pad=0.5)
        st.pyplot(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MEDIA & LINKS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_media:

    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3>Media breakdown</h3>
    </div>""", unsafe_allow_html=True)

    media_data = {
        "Images": (num_images, "🖼️"),
        "Videos": (num_videos, "🎬"),
        "Audio":  (num_audio,  "🎵"),
        "Stickers":(num_stickers,"🪄"),
        "GIFs":   (num_gifs,   "✨"),
        "Links":  (num_links,  "🔗"),
    }

    cols = st.columns(6)
    for col, (label, (val, icon)) in zip(cols, media_data.items()):
        with col:
            st.markdown(f"""
            <div class="stat-badge">
                <div style="font-size:22px; margin-bottom:6px">{icon}</div>
                <div class="val">{val:,}</div>
                <div class="lbl">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header" style="margin-top:28px">
        <div class="section-dot"></div>
        <h3>Media vs text ratio</h3>
    </div>""", unsafe_allow_html=True)

    total_media = num_images + num_videos + num_audio + num_stickers + num_gifs
    text_msgs   = max(num_messages - total_media, 0)

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)
    wedge_sizes  = [text_msgs, total_media, num_links]
    wedge_labels = ["Text", "Media", "Links"]
    wedge_colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMB]
    wedges, texts, autotexts = ax.pie(
        wedge_sizes, labels=wedge_labels, colors=wedge_colors,
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(edgecolor=CHART_BG, linewidth=2),
        textprops=dict(color=CHART_TEXT, fontsize=11),
    )
    for at in autotexts:
        at.set_color("#f1f5f9")
        at.set_fontsize(10)
    ax.axis("equal")
    plt.tight_layout(pad=0.3)

    _, pie_col, _ = st.columns([1, 2, 1])
    with pie_col:
        st.pyplot(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — RAW DATA
# ═══════════════════════════════════════════════════════════════════════════════
with tab_raw:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <h3>Parsed messages</h3>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<p style='color:#475569; font-size:13px; margin-bottom:12px'>{len(df):,} rows · {len(df.columns)} columns</p>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, height=420)

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 24px 0 16px; color:#2a3550; font-size:12px;">
    ChatLens · built with Streamlit
</div>
""", unsafe_allow_html=True)