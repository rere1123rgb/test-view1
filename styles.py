def get_css(bg_color, text_color, font_family, font_size, line_height, margin_pct, is_mobile=False):
    
    border_color = f"{text_color}20"
    bg_subtle = f"{text_color}06"   # 아주 연한 배경색
    accent_color = f"{text_color}60" # 강조 포인트 색상
    
    scrollbar_width = "18px" if is_mobile else "10px"
    small_font_size = int(font_size * 0.88) # 가독성을 위해 조금 키움
    
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Nanum+Gothic:wght@400;700&family=Nanum+Myeongjo:wght@400;700&display=swap');
        @import url('https://fonts.googleapis.com/earlyaccess/kopubbatang.css');
        @font-face {{ font-family: 'Ridibatang'; src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_two@1.0/Ridibatang.woff') format('woff'); font-weight: normal; font-style: normal; font-display: swap; }}
        @font-face {{ font-family: 'ChosunMj'; src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@1.0/ChosunMj.woff2') format('woff2'); font-weight: normal; font-style: normal; font-display: swap; }}

        .stApp {{ background-color: {bg_color}; }}

        .block-container {{
            padding-top: 35px !important;
            padding-bottom: 0rem !important;
            max-width: 100% !important;
        }}
        
        header {{
            background: transparent !important;
            height: auto !important;
            z-index: 99 !important;
        }}
        [data-testid="stSidebarCollapsedControl"] {{
            color: {text_color} !important;
            background-color: {bg_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 50% !important;
            padding: 4px !important;
            margin-top: 10px !important;
            margin-left: 10px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

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

        .novel-container-page {{
            background-color: {bg_color};
            color: {text_color};
            padding: 5px {margin_pct}% 50px {margin_pct}%;
            max-width: 1200px;
            margin: 0 auto;
            min-height: 0px !important; 
            border: none;
        }}

        /* 본문 텍스트 스타일 */
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

        div.novel-text span.dialogue {{ font-weight: 900 !important; color: {text_color} !important; }}
        div.novel-text span.thought {{ color: #7f8c8d !important; font-weight: normal !important; }}
        div.novel-text span.emphasis {{ color: #1a237e !important; font-weight: bold !important; }}
        
        /* 효과음 스타일 */
        div.novel-text span.sound-effect {{ 
            color: #95a5a6 !important; 
            font-style: italic !important; 
            font-weight: normal !important;
            font-size: 0.95em !important;
        }}
        
        @media (prefers-color-scheme: dark) {{
            div.novel-text span.thought {{ color: #a0a0a0 !important; }}
            div.novel-text span.emphasis {{ color: #7986cb !important; }}
            div.novel-text span.sound-effect {{ color: #b0bec5 !important; }}
        }}

        @media (max-width: 768px) {{
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
            div.nav-anchor ~ div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
                width: auto !important;
                flex: 0 1 auto !important;
                min-width: 0 !important;
            }}
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
        .novel-dateline {{ font-family: 'Nanum Gothic', sans-serif !important; font-size: 0.85em !important; color: {text_color}; opacity: 0.7; margin: 5px 0 15px 0; padding-bottom: 5px; border-bottom: 1px dashed {border_color}; text-align: right; display: block; }}
        .system-msg {{ font-family: 'Nanum Gothic', sans-serif !important; font-weight: bold; color: {text_color}; background-color: {text_color}10; border-left: 4px solid {text_color}60; padding: 8px 12px; margin: 10px 0; border-radius: 4px; font-size: {font_size}px; line-height: 1.4; white-space: pre-wrap !important; }}
        
        details, .community-box, .wncs-container, .lightboard-container {{ font-family: 'Nanum Gothic', sans-serif !important; }}
        details {{ margin: 15px 0; padding: 5px; border: 1px solid {border_color}; border-radius: 5px; background-color: {bg_subtle}; transition: all 0.3s ease; }}
        details[open] {{ background-color: transparent; border: none; }}
        summary {{ cursor: pointer; font-weight: bold; color: {text_color}; padding: 5px 10px; list-style: none; }}
        
        div.novel-text .community-box *, 
        div.novel-text .wncs-container *,
        div.novel-text .lightboard-container * {{
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.45 !important;
            font-family: 'Nanum Gothic', sans-serif !important;
            font-size: inherit !important;
        }}

        .community-box {{ background-color: {bg_color}; border: 1px solid {text_color}30; margin-top: 10px; font-size: {small_font_size}px !important; }}
        .comm-header {{ background-color: {bg_subtle}; padding: 8px 12px !important; border-bottom: 1px solid {text_color}30; font-weight: bold; margin-bottom: 5px !important; }}
        .comm-post {{ padding: 15px !important; border-bottom: 1px solid {text_color}20; }}
        .comm-title {{ font-size: 1.1em !important; font-weight: bold; display: block !important; margin-bottom: 5px !important; }}
        .comm-meta {{ font-size: 0.8em !important; opacity: 0.6; display: block !important; margin-bottom: 15px !important; border-bottom: 1px solid {text_color}10; padding-bottom: 5px !important; }}
        .comm-body {{ display: block !important; margin-bottom: 15px !important; line-height: 1.5 !important; }}
        .comm-comments {{ background-color: {bg_subtle}; padding: 10px !important; border-radius: 4px; font-size: 0.9em !important; }}
        .comm-cmt-row {{ display: block !important; margin-bottom: 6px !important; border-bottom: 1px dashed {text_color}10; padding-bottom: 2px !important; }}
        .comm-cmt-user {{ font-weight: bold; margin-right: 6px !important; }}
        
        .wncs-container {{ margin-top: 10px; font-size: {small_font_size}px !important; border-top: 2px solid {text_color}; }}
        .wncs-header {{ padding: 10px 0 !important; font-weight: bold; border-bottom: 1px solid {text_color}20; }}
        .wncs-author-note {{ background-color: {bg_subtle}; padding: 15px !important; margin: 10px 0 !important; border-radius: 8px; border: 1px solid {text_color}20; font-weight: bold; }}
        .wncs-item {{ padding: 12px 0 !important; border-bottom: 1px solid {text_color}10; display: block !important; }}
        .wncs-info {{ font-size: 0.8em !important; opacity: 0.6; margin-bottom: 4px !important; display: block !important; }}
        .wncs-user {{ font-weight: bold; margin-right: 8px !important; }}
        .wncs-reply {{ margin-left: 20px !important; padding: 8px 0 8px 10px !important; border-left: 3px solid {text_color}20; background-color: {bg_subtle}50; }}
        
        /* [V0.95] 라이트보드(Lightboard) 스타일 - 예쁜 카드 디자인 */
        .lightboard-container {{ 
            margin-top: 15px; 
            margin-bottom: 15px;
            background-color: transparent; 
            border: none;
            padding: 5px;
            font-size: {small_font_size}px !important; 
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        /* 게시글 (Post) - 둥근 카드형 */
        .lb-post {{
            display: flex !important;
            flex-direction: column !important;
            background-color: {bg_subtle} !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px !important;
            padding: 12px 15px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
            transition: transform 0.2s ease;
        }}
        .lb-post:hover {{
            transform: translateY(-1px); /* 호버 시 살짝 떠오름 */
            box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
        }}
        
        /* 댓글 (Comment) - 깔끔한 대댓글 라인 */
        .lb-comment {{
            display: flex !important;
            flex-direction: column !important;
            background-color: transparent !important;
            border-left: 3px solid {accent_color} !important;
            padding: 6px 0px 6px 12px !important;
            margin-left: 15px !important;
            margin-top: 2px !important;
        }}
        
        /* 헤더 (작성자 + 메타) */
        .lb-header {{
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            border-bottom: 1px dashed {text_color}20 !important;
            padding-bottom: 6px !important;
            margin-bottom: 6px !important;
            width: 100% !important;
        }}
        
        .lb-author {{
            font-weight: 700 !important;
            color: {text_color} !important;
            font-size: 1.05em !important;
            display: flex !important;
            align-items: center !important;
        }}
        /* 작성자 앞 포인트 바 */
        .lb-author::before {{
            content: '' !important;
            display: inline-block !important;
            width: 4px !important;
            height: 12px !important;
            background-color: {accent_color} !important;
            border-radius: 2px !important;
            margin-right: 8px !important;
        }}
        
        .lb-meta {{
            font-size: 0.85em !important;
            color: {text_color}80 !important;
            letter-spacing: -0.3px !important;
        }}
        
        /* 본문 */
        .lb-body {{
            display: block !important;
            color: {text_color}E0 !important;
            word-break: break-all;
            white-space: pre-wrap;
        }}
        
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