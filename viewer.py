import streamlit as st
import json
import re
import os
import styles
import processor

try:
    from streamlit_javascript import st_javascript
    HAS_JS_LIB = True
except ImportError:
    HAS_JS_LIB = False

CONFIG_FILE = "viewer_config.json"
DEFAULT_CONFIG = {
    "common": { "folder_path": "", "custom_orders": {}, "last_opened_path": None, "view_type": "scroll" },
    "pc": { "theme": "일반", "bg_color": "#fcfcfc", "text_color": "#2c3e50", "font_size": 18, "line_height": 1.8, "content_margin": 20, "font_family": "명조체 (Nanum Myeongjo)" },
    "mobile": { "theme": "일반", "bg_color": "#fcfcfc", "text_color": "#2c3e50", "font_size": 15, "line_height": 1.6, "content_margin": 3, "font_family": "리디바탕" }
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if "common" not in loaded: return DEFAULT_CONFIG 
            return {**DEFAULT_CONFIG, **loaded}
        except: return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config():
    mode = st.session_state.get("ui_mode", "pc")
    current_path = st.session_state.get("current_file_path")
    path_to_save = current_path if isinstance(current_path, str) else None
    current_full_config = load_config()
    current_full_config["common"]["folder_path"] = st.session_state.get("folder_path_input", "")
    current_full_config["common"]["custom_orders"] = st.session_state.get("custom_orders", {})
    current_full_config["common"]["last_opened_path"] = path_to_save
    current_full_config["common"]["view_type"] = st.session_state.get("view_type", "scroll")
    visual_settings = {
        "theme": st.session_state.get("theme_name", "일반"),
        "bg_color": st.session_state.get("bg_color", "#fcfcfc"),
        "text_color": st.session_state.get("text_color", "#2c3e50"),
        "font_size": st.session_state.get("font_size", 18),
        "line_height": st.session_state.get("line_height", 1.8),
        "content_margin": st.session_state.get("content_margin", 10),
        "font_family": st.session_state.get("font_family", "명조체 (Nanum Myeongjo)")
    }
    current_full_config[mode] = visual_settings
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(current_full_config, f, indent=4, ensure_ascii=False)

st.set_page_config(page_title="케이뷰어 (K-Viewer)", page_icon="📖", layout="wide")

screen_width = None
if HAS_JS_LIB: screen_width = st_javascript("window.innerWidth", key="screen_width_check")

if "ui_mode" not in st.session_state:
    st.session_state["ui_mode"] = "pc"
    if screen_width and screen_width > 0:
        if screen_width < 768:
            st.session_state["ui_mode"] = "mobile"
            st.rerun()

full_config = load_config()
active_config = full_config[st.session_state["ui_mode"]]
common_config = full_config["common"]
initial_file_path = None
if common_config["last_opened_path"] and os.path.exists(common_config["last_opened_path"]):
    initial_file_path = common_config["last_opened_path"]

session_defaults = {
    "bg_color": active_config["bg_color"], "text_color": active_config["text_color"], "font_size": active_config["font_size"], "line_height": active_config["line_height"],
    "content_margin": active_config["content_margin"], "font_family": active_config["font_family"], "theme_name": active_config["theme"],
    "folder_path_input": common_config["folder_path"], "custom_orders": common_config["custom_orders"], "saved_folder_path": common_config["folder_path"],
    "current_file_path": initial_file_path, "view_type": common_config.get("view_type", "scroll"), "expanded_folders": set(), "page_idx": 0
}
for key, val in session_defaults.items():
    if key not in st.session_state: st.session_state[key] = val

if st.session_state["ui_mode"] == "pc":
    st.session_state["view_type"] = "scroll"

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def get_sorted_items(path):
    try: all_items = os.listdir(path)
    except PermissionError: return [], []
    dirs, files = [], []
    for item in all_items:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path): dirs.append(item)
        elif item.lower().endswith('.json'): files.append(item)
    files.sort(key=natural_sort_key)
    dirs.sort(key=natural_sort_key)
    saved_order = st.session_state.custom_orders.get(path, [])
    if saved_order:
        ordered_dirs = [d for d in saved_order if d in dirs]
        new_dirs = [d for d in dirs if d not in ordered_dirs]
        dirs = ordered_dirs + new_dirs
    return dirs, files

def move_folder(path, folder_name, direction):
    dirs, _ = get_sorted_items(path)
    if folder_name not in dirs: return
    idx = dirs.index(folder_name)
    if direction == 'up' and idx > 0: dirs[idx], dirs[idx-1] = dirs[idx-1], dirs[idx]
    elif direction == 'down' and idx < len(dirs) - 1: dirs[idx], dirs[idx+1] = dirs[idx+1], dirs[idx]
    else: return
    st.session_state.custom_orders[path] = dirs
    save_config()
    st.rerun()

def toggle_folder(path):
    if path in st.session_state.expanded_folders: st.session_state.expanded_folders.remove(path)
    else: st.session_state.expanded_folders.add(path)

def change_page(delta, max_page):
    new_page = st.session_state.page_idx + delta
    if 0 <= new_page < max_page: st.session_state.page_idx = new_page

def apply_theme(theme_name):
    themes = {
        "일반": {"bg": "#fcfcfc", "text": "#2c3e50"}, "세피아": {"bg": "#f4ecd8", "text": "#5b4636"}, "눈 보호": {"bg": "#e8f5e9", "text": "#1b5e20"},
        "다크": {"bg": "#1e1e1e", "text": "#d4d4d4"}, "블랙": {"bg": "#000000", "text": "#999999"}
    }
    if theme_name in themes:
        st.session_state.bg_color = themes[theme_name]["bg"]
        st.session_state.text_color = themes[theme_name]["text"]
        st.session_state.theme_name = theme_name
        save_config()
        st.rerun()

def render_tree_ui(current_path, level=0):
    dirs, files = get_sorted_items(current_path)
    indent = "\u2001" * level 
    is_mobile = st.session_state.get("ui_mode") == "mobile"
    for idx, dir_name in enumerate(dirs):
        full_path = os.path.join(current_path, dir_name)
        is_expanded = full_path in st.session_state.expanded_folders
        icon = "📂" if is_expanded else "📁"
        if is_mobile:
            if st.sidebar.button(f"{indent}{icon} {dir_name}", key=f"btn_{full_path}", use_container_width=True):
                toggle_folder(full_path)
                st.rerun()
        else:
            c1, c2, c3 = st.sidebar.columns([0.6, 0.6, 8.8])
            with c1:
                if idx > 0: st.button("▴", key=f"u_{full_path}", on_click=move_folder, args=(current_path, dir_name, 'up'))
            with c2:
                if idx < len(dirs) - 1: st.button("▾", key=f"d_{full_path}", on_click=move_folder, args=(current_path, dir_name, 'down'))
            with c3:
                st.button(f"{indent}{icon} {dir_name}", key=f"btn_{full_path}", use_container_width=True, on_click=toggle_folder, args=(full_path,))
        if is_expanded: render_tree_ui(full_path, level + 1)
    for file_name in files:
        full_path = os.path.join(current_path, file_name)
        is_selected = (st.session_state.current_file_path == full_path)
        icon = "✅" if is_selected else "📄"
        if st.sidebar.button(f"{indent}{icon} {file_name}", key=f"f_{full_path}", use_container_width=True):
            st.session_state.current_file_path = full_path
            st.session_state.page_idx = 0
            save_config()
            st.rerun()

def switch_profile():
    new_mode = st.session_state.profile_selector
    st.session_state["ui_mode"] = "pc" if new_mode == "🖥️ PC" else "mobile"
    target_conf = load_config()[st.session_state["ui_mode"]]
    st.session_state.bg_color = target_conf["bg_color"]
    st.session_state.text_color = target_conf["text_color"]
    st.session_state.font_size = target_conf["font_size"]
    st.session_state.line_height = target_conf["line_height"]
    st.session_state.content_margin = target_conf["content_margin"]
    st.session_state.font_family = target_conf["font_family"]
    st.session_state.theme_name = target_conf["theme"]

def render_settings_popup():
    st.markdown("### ⚙️ 뷰어 설정")
    if not HAS_JS_LIB: st.caption("⚠️ 'pip install streamlit-javascript' 필요")
    idx = 0 if st.session_state["ui_mode"] == "pc" else 1
    st.radio("설정 프로필", ["🖥️ PC", "📱 Mobile"], index=idx, key="profile_selector", on_change=switch_profile, horizontal=True)
    st.markdown("---")
    if st.session_state["ui_mode"] == "mobile":
        view_type_idx = 0 if st.session_state.view_type == "scroll" else 1
        st.radio("보기 모드", ["📜 스크롤 (Scroll)", "📄 페이지 (Page)"], index=view_type_idx, key="view_type_radio", 
                 on_change=lambda: st.session_state.update(view_type="scroll" if st.session_state.view_type_radio.startswith("📜") else "page") or save_config(), horizontal=True)
        st.markdown("---")
    with st.expander("🎨 테마 프리셋", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            if st.button("일반", use_container_width=True): apply_theme("일반")
            if st.button("세피아", use_container_width=True): apply_theme("세피아")
            if st.button("블랙", use_container_width=True): apply_theme("블랙")
        with c2:
            if st.button("눈 보호", use_container_width=True): apply_theme("눈 보호")
            if st.button("다크", use_container_width=True): apply_theme("다크")
    st.slider("좌우 여백 (%)", 0, 35, key="content_margin", on_change=save_config)
    st.slider("글자 크기", 14, 36, key="font_size", on_change=save_config)
    st.slider("줄 간격", 1.4, 2.5, step=0.1, key="line_height", on_change=save_config)
    font_options = ["명조체 (Nanum Myeongjo)", "고딕체 (Nanum Gothic)", "리디바탕", "코펍바탕", "고운바탕 (Gowun Batang)"]
    st.selectbox("폰트 선택", font_options, key="font_family", on_change=save_config)

def main():
    font_map = { "명조체 (Nanum Myeongjo)": "'Nanum Myeongjo', serif", "고딕체 (Nanum Gothic)": "'Nanum Gothic', sans-serif", "리디바탕": "'Ridibatang', serif", "코펍바탕": "'KoPub Batang', serif", "고운바탕 (Gowun Batang)": "'Gowun Batang', serif" }
    is_mobile_mode = (st.session_state.get("ui_mode") == "mobile")
    css_code = styles.get_css(st.session_state.bg_color, st.session_state.text_color, font_map.get(st.session_state.font_family, "'Nanum Myeongjo', serif"), st.session_state.font_size, st.session_state.line_height, st.session_state.content_margin, is_mobile_mode)
    st.markdown(css_code, unsafe_allow_html=True)
    with st.sidebar:
        st.header("📂 케이뷰어")
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        folder_path = st.session_state.saved_folder_path
        if folder_path and os.path.isdir(folder_path):
            st.caption(f"Location: {os.path.basename(folder_path)}")
            with st.container(): render_tree_ui(folder_path, level=0)
        else: st.info("아래 설정에서 폴더 경로를 입력하세요.")
        st.markdown("---")
        with st.expander("⚙️ 경로 및 파일 열기", expanded=False):
            st.text_input("서고 폴더 경로", key="folder_path_input", on_change=save_config, placeholder="C:\\Novels")
            st.file_uploader("임시 파일 열기", type=['json'], key="uploader", on_change=lambda: st.session_state.update(current_file_path=st.session_state.uploader, page_idx=0) if st.session_state.uploader else None)
    with st.popover("⚙️", use_container_width=False): render_settings_popup()
    
    target_file = st.session_state.get("current_file_path")
    if target_file:
        display_name = os.path.basename(target_file) if isinstance(target_file, str) else target_file.name
        if isinstance(target_file, str):
            with open(target_file, 'r', encoding='utf-8') as f: file_content = f.read()
        else: file_content = target_file.getvalue().decode("utf-8")
        
        limit = 450 if is_mobile_mode else 2500
        content_list, error = processor.get_novel_content(file_content, chunk_size=limit)
        
        if error: st.error(f"오류: {error}")
        elif not content_list: st.warning("내용 없음")
        else:
            view_type = st.session_state.get("view_type", "scroll")
            if not is_mobile_mode: view_type = "scroll"
            
            if view_type == "scroll":
                full_html = "".join(content_list)
                st.markdown(f'<div class="novel-container-scroll"><h1 style="text-align: center; margin-bottom: 50px;">{display_name}</h1>{full_html}</div>', unsafe_allow_html=True)
            else:
                max_page = len(content_list)
                current_idx = st.session_state.get("page_idx", 0)
                if current_idx >= max_page: current_idx = max_page - 1
                if current_idx < 0: current_idx = 0
                st.session_state.page_idx = current_idx
                page_html = content_list[current_idx]
                st.markdown(f'<div class="novel-container-page">{page_html}</div>', unsafe_allow_html=True)
                
                # [핵심] 플로팅 앵커 및 버튼
                st.markdown('<div class="nav-anchor"></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="page-info-overlay">{current_idx + 1} / {max_page}</div>', unsafe_allow_html=True)
                
                # [NEW] use_container_width=False 적용 (버튼 작게 만들기)
                c_prev, c_next = st.columns([1, 1])
                with c_prev:
                    if st.button("◀", use_container_width=False):
                        change_page(-1, max_page)
                        st.rerun()
                with c_next:
                    if st.button("▶", use_container_width=False):
                        change_page(1, max_page)
                        st.rerun()
    else:
        st.markdown(f"""
        <div style='text-align:center; padding-top: 150px; opacity: 0.6; color: {st.session_state.text_color};'>
            <h2>📂 케이뷰어 V59</h2>
            <p>왼쪽 사이드바에서 책을 선택해주세요.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
