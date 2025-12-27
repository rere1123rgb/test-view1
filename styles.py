def get_css(bg_color, text_color, font_family, font_size, line_height, margin_pct, is_mobile=False):
    
    border_color = f"{text_color}20"
    bg_subtle = f"{text_color}05"
    scrollbar_width = "18px" if is_mobile else "10px"
    
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Nanum+Gothic:wght@400;700&family=Nanum+Myeongjo:wght@400;700&display=swap');
        @import url('https://fonts.googleapis.com/earlyaccess/kopubbatang.css');
        @font-face {{ font-family: 'Ridibatang'; src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/Ridibatang.woff') format('woff'); font-weight: normal; font-style: normal; font-display: swap; }}
        @font-face {{ font-family: 'ChosunMj'; src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@1.0/ChosunMj.woff2') format('woff2'); font-weight: normal; font-style: normal; font-display: swap; }}

        .stApp {{ background-color: {bg_color}; }}

        /* [V60 수정] 헤더를 숨기지 않고 '투명'하게 변경하여 사이드바 버튼 살림 */
        header {{
            background: transparent !important;
            height: auto !important;
            z-index: 99 !important; /* 맨 앞으로 */
        }}
        
        /* 사이드바 여는 화살표 버튼 커스텀 */
        [data-testid="stSidebarCollapsedControl"] {{
            color: {text_color} !important;
            background-color: {bg_color} !important; /* 본문 배경색과 동일하게 */
            border: 1px solid {border_color} !important;
            border-radius: 50% !important;
            padding: 4px !important;
            margin-top: 10px !important;
            margin-left: 10px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        /* 상단 여백 설정 (버튼과 겹치지 않게 아주 약간만 줌) */
        .block-container {{
            padding-top: 35px !important; /* 화살표 버튼 공간 확보 */
            padding-bottom: 0rem !important;
            max-width: 100% !important;
        }}

        /* 스크롤 모드 (PC) */
        .novel-container-scroll {{
            background-color: {bg_color};
            color: {text_color};
            padding: 40px {margin_pct}% 80px {margin_pct}%;
            max-width: 1200px;
            margin: 0 auto;
            height: 92vh; 
            overflow-y: auto;
            overflow-x: hidden;
            scroll-behavior: smooth;
            border: 1px solid {border_color};
            border-radius: 8px;
        }}
        .novel-container-scroll::-webkit-scrollbar {{ width: {scrollbar_width}; }}
        .novel-container-scroll::-webkit-scrollbar-track {{ background: {bg_subtle}; border-radius: 8px; }}
        .novel-container-scroll::-webkit-scrollbar-thumb {{ background-color: {text_color}40; border-radius: 10px; border: 3px solid {bg_color}; }}

        /* 페이지 모드 (모바일) - 여백 최소화 */
        .novel-container-page {{
            background-color: {bg_color};
            color: {text_color};
            padding: 5px {margin_pct}% 50px {margin_pct}%;
            max-width: 1200px;
            margin: 0 auto;
            min-height: 0px !important; 
            border: none;
        }}

        /* 텍스트 본문 */
        div.novel-text, div.novel-text p, div.novel-text span {{
            font-family: {font_family} !important; 
            font-size: {font_size}px !important; 
            line-height: {line_height} !important;
            color: {text_color};
            white-space: pre-wrap;
            text-align: justify !important; 
            word-break: break-all !important; 
            margin-bottom: 15px;
        }}

        /* 모바일 하단 플로팅 바 (슬림 & 미니멀) */
        @media (max-width: 768px) {{
            /* 1. 하단바 컨테이너 */
            div.nav-anchor ~ div[data-testid="stHorizontalBlock"] {{
                position: fixed !important;
                bottom: 10px !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
                
                width: auto !important;
                min-width: 280px !important;
                max-width: 90% !important;
                
                background-color: {bg_color}E6 !important;
                border: 1px solid {border_color} !important;
                border-radius: 50px !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
                
                padding: 4px 15px !important;
                z-index: 999999 !important;
                margin: 0 !important;
                
                display: flex !important;
                flex-direction: row !important;
                align-items: center !important;
                justify-content: space-between !important;
                gap: 0px !important;
            }}

            /* 2. 내부 컬럼 */
            div.nav-anchor ~ div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
                width: auto !important;
                flex: 0 1 auto !important;
                min-width: 0 !important;
            }}

            /* 3. 버튼 스타일 */
            div.nav-anchor ~ div[data-testid="stHorizontalBlock"] button {{
                width: auto !important;
                height: 32px !important;
                min-height: 0px !important;
                padding: 0px 12px !important;
                margin: 0 !important;
                
                border-radius: 20px !important;
                font-size: 0.85rem !important;
                border: 1px solid {border_color} !important;
                background-color: transparent !important;
                color: {text_color} !important;
                line-height: 1 !important;
            }}
            
            div.nav-anchor ~ div[data-testid="stHorizontalBlock"] button:active {{
                background-color: {text_color}10 !important;
            }}

            /* 4. 페이지 번호 텍스트 */
            div.nav-anchor ~ div[data-testid="stHorizontalBlock"] div.stMarkdown p {{
                font-size: 0.8rem !important;
                margin: 0 10px !important;
                white-space: nowrap !important;
                color: {text_color} !important;
                opacity: 0.8;
                line-height: 32px !important;
            }}
        }}

        h1 {{ color: {text_color} !important; font-family: {font_family} !important; text-align: center; margin-bottom: 20px; font-weight: bold; font-size: 1.8em; }}
        .dialogue {{ font-weight: bold; color: {text_color}; }}
        .thought {{ color: #7f8c8d; }}
        @media (prefers-color-scheme: dark) {{ .thought {{ color: #a0a0a0; }} }}
        .novel-dateline {{ font-family: 'Nanum Gothic', sans-serif !important; font-size: 0.85em !important; color: {text_color}; opacity: 0.7; margin: 5px 0 15px 0; padding-bottom: 5px; border-bottom: 1px dashed {border_color}; text-align: right; display: block; }}
        .system-msg {{ font-family: 'Nanum Gothic', sans-serif !important; font-weight: bold; color: {text_color}; background-color: {text_color}10; border-left: 4px solid {text_color}60; padding: 8px 12px; margin: 10px 0; border-radius: 4px; font-size: {font_size}px; line-height: 1.4; }}
        
        details, .community-box, .wncs-container {{ font-family: 'Nanum Gothic', sans-serif !important; }}
        details {{ margin: 15px 0; padding: 5px; border: 1px solid {border_color}; border-radius: 5px; background-color: {bg_subtle}; transition: all 0.3s ease; }}
        details[open] {{ background-color: transparent; border: none; }}
        summary {{ cursor: pointer; font-weight: bold; color: {text_color}; padding: 5px 10px; list-style: none; }}
        .community-box {{ background-color: {bg_color}; border: 1px solid {text_color}30; margin-top: 10px; font-size: {int(font_size * 0.85)}px; }}
        .comm-header {{ background-color: {bg_subtle}; padding: 8px 12px; border-bottom: 1px solid {text_color}30; font-weight: bold; }}
        .comm-post {{ padding: 15px; border-bottom: 1px solid {text_color}20; }}
        .comm-title {{ font-size: 1.1em; font-weight: bold; margin-bottom: 5px; }}
        .comm-meta {{ font-size: 0.8em; opacity: 0.6; margin-bottom: 15px; border-bottom: 1px solid {text_color}10; padding-bottom: 5px; }}
        .comm-body {{ margin-bottom: 15px; line-height: 1.5; }}
        .comm-comments {{ background-color: {bg_subtle}; padding: 10px; border-radius: 4px; font-size: 0.9em; }}
        .comm-cmt-row {{ margin-bottom: 6px; padding-bottom: 6px; border-bottom: 1px dashed {text_color}10; }}
        .comm-cmt-user {{ font-weight: bold; margin-right: 6px; }}
        .wncs-container {{ margin-top: 10px; font-size: {int(font_size * 0.85)}px; border-top: 2px solid {text_color}; }}
        .wncs-header {{ padding: 10px 0; font-weight: bold; border-bottom: 1px solid {text_color}20; }}
        .wncs-author-note {{ background-color: {bg_subtle}; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid {text_color}20; font-weight: bold; }}
        .wncs-item {{ padding: 12px 0; border-bottom: 1px solid {text_color}10; }}
        .wncs-info {{ font-size: 0.8em; opacity: 0.6; margin-bottom: 4px; }}
        .wncs-user {{ font-weight: bold; font-size: 1.0em; margin-right: 8px; }}
        .wncs-reply {{ margin-left: 20px; padding: 8px 0 8px 10px; border-left: 3px solid {text_color}20; background-color: {bg_subtle}50; }}
        .novel-img-placeholder {{ display: block; margin: 20px auto; padding: 10px; border: 1px dashed {border_color}; border-radius: 4px; text-align: center; color: {text_color}; opacity: 0.8; font-family: {font_family} !important; font-size: {int(font_size * 0.8)}px; }}
        .chapter-divider {{ border: none; border-top: 1px solid {border_color}; margin: 5px 0; width: 100%; height: 1px; }}

        div[data-testid="stPopover"] {{ position: fixed !important; top: 60px !important; right: 30px !important; z-index: 99999 !important; width: auto !important; }}
        div[data-testid="stPopover"] > button {{ background-color: {bg_color} !important; color: {text_color} !important; border: 1px solid {border_color} !important; border-radius: 50% !important; width: 45px !important; height: 45px !important; box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important; font-size: 1.2rem !important; transition: all 0.2s ease; }}
        div.stButton > button {{ border-radius: 8px; border: 1px solid {border_color}; background-color: {bg_subtle}; color: {text_color}; }}
        h2, h3, p, label, .stMarkdown, .stCaption {{ color: {text_color} !important; }}
        hr {{ border-color: {border_color} !important; }}
        section[data-testid="stSidebar"] {{ background-color: {bg_color}; }}
        [data-testid="stSidebar"] button {{ width: 100%; justify-content: flex-start !important; text-align: left !important; border: none !important; background: transparent !important; padding: 2px 0px !important; color: {text_color} !important; line-height: 1.2 !important; height: auto !important; margin: 0 !important; }}
        [data-testid="stSidebar"] button:hover {{ color: {text_color}80 !important; }}
        .stPopover [data-testid="stVerticalBlock"] {{ gap: 0.5rem !important; }}
        .stSlider {{ padding-top: 5px !important; padding-bottom: 5px !important; }}
        .stSelectbox {{ padding-top: 5px !important; }}
    </style>
    """
