import re
import json
import streamlit as st
import uuid

# [GLOBAL] 정규식
RE_HEADER_RESPONSE = re.compile(r'^#\s+응답.*$', re.MULTILINE)
RE_HEADER_SHARP = re.compile(r'^#{2,3}\s+.*$', re.MULTILINE)
RE_LB_LAZY = re.compile(r'<lb-lazy[^>]*>.*?</lb-lazy>', re.DOTALL)
RE_HANJA_BRACKET = re.compile(r'《([^가-힣]+?)》')
RE_MULTI_NEWLINE = re.compile(r'\n{3,}')
RE_ENGLISH_CHAR = re.compile(r'[a-zA-Z]')
RE_STATUS_DATE = re.compile(r'Date\s*:\s*([^|\]]+)', re.IGNORECASE)
RE_STATUS_TIME = re.compile(r'Time\s*:\s*([^|\]]+)', re.IGNORECASE)
RE_IMG_TAG = re.compile(r'<img=["\'](.*?)["\']>')

# 시스템 메시지
RE_SYS_MSG = re.compile(r'^-\s*System Message:\s*(.*)', re.MULTILINE)
RE_SYS_MSG_BRACE = re.compile(r'^-\s*\{System Message:\s*(.*?)\}', re.MULTILINE)

# 따옴표 감지
RE_QUOTE_DOUBLE = re.compile(r'"([^"]*)"')
RE_QUOTE_SINGLE = re.compile(r"'([^']*)'") 

RE_HTML_TAG = re.compile(r'<[^>]+>') 
RE_PREV_SUMMARY = re.compile(r'▽.*?△', re.DOTALL)

# 파서 유틸리티
def parse_nested_block(text, start_marker, open_char, close_char, repl_func):
    result = []
    cursor = 0
    text_len = len(text)
    use_marker = bool(start_marker)
    while cursor < text_len:
        if use_marker: start_idx = text.find(start_marker, cursor)
        else: start_idx = text.find(open_char, cursor)
        if start_idx == -1:
            result.append(text[cursor:])
            break
        result.append(text[cursor:start_idx])
        content_start = start_idx + len(start_marker) if use_marker else start_idx + 1
        current = content_start
        balance = 1
        while current < text_len and balance > 0:
            char = text[current]
            if char == open_char: balance += 1
            elif char == close_char: balance -= 1
            current += 1
        if balance == 0:
            raw_content = text[content_start : current - 1]
            if repl_func:
                converted = repl_func(raw_content)
                if converted is None: result.append(text[start_idx:current])
                else: result.append(converted)
            else: result.append(text[start_idx:current])
            cursor = current
        else:
            result.append(text[start_idx:])
            break
    return "".join(result)

def convert_hn_content(raw_content):
    def parse_single_hn(full_str):
        posts_html = ""
        raw_posts = full_str.split('|PID:')
        header_part = raw_posts[0]
        gn_match = re.search(r'GN:(.*?)(?:\||$)', header_part)
        if gn_match: posts_html += f'<div class="comm-header">{gn_match.group(1)}</div>'
        target_posts = raw_posts[1:] if len(raw_posts) > 1 else []
        for p in target_posts:
            fields = p.split('|')
            p_data = {'C': []}
            current_cmt_author = None
            for f in fields:
                if f.startswith('PT:'): p_data['PT'] = f[3:]
                elif f.startswith('PA:'): p_data['PA'] = f[3:]
                elif f.startswith('PDATE:'): p_data['PDATE'] = f[6:]
                elif f.startswith('PVIEWS:'): p_data['PVIEWS'] = f[7:]
                elif f.startswith('PRECOM:'): p_data['PRECOM'] = f[7:]
                elif f.startswith('PCONT:'): p_data['PCONT'] = f[6:]
                elif f.startswith('C:'):
                    auth = f[2:]
                    if auth.startswith('F:') or auth.startswith('S:'): auth = auth.split(':', 1)[1]
                    current_cmt_author = auth
                else:
                    if current_cmt_author: p_data['C'].append((current_cmt_author, f))
                    current_cmt_author = None
            posts_html += '<div class="comm-post">'
            posts_html += f'<div class="comm-title">{p_data.get("PT", "")}</div>'
            posts_html += f'<div class="comm-meta">{p_data.get("PA","")} | {p_data.get("PDATE","")} | 조회 {p_data.get("PVIEWS","")} | 추천 {p_data.get("PRECOM","")}</div>'
            posts_html += f'<div class="comm-body">{p_data.get("PCONT", "")}</div>'
            if p_data['C']:
                posts_html += '<div class="comm-comments">'
                for author, body in p_data['C']: posts_html += f'<div class="comm-cmt-row"><span class="comm-cmt-user">{author}</span> {body}</div>'
                posts_html += '</div>'
            posts_html += '</div>'
        return posts_html
    final_html = '<div class="community-box">' + parse_single_hn(raw_content) + '</div>'
    return f'<details><summary>🔻 커뮤니티 반응 (Community)</summary>{final_html}</details>'

def convert_wncs_content(raw_content):
    lines = raw_content.strip().split('\n')
    gn_text, an_text = "", ""
    html = '<div class="wncs-container">'
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith('GN:'):
            gn_text = line[3:]
            html += f'<div class="wncs-header">{gn_text}</div>'
        elif line.startswith('AN:'):
            an_text = line[3:]
            html += f'<div class="wncs-author-note">작가의 말: {an_text}</div>'
        elif line.startswith('R:|'):
            parts = line.split('|')
            if len(parts) >= 3: html += f'<div class="wncs-item wncs-reply"><span class="wncs-user">↳ {parts[1]}</span> <span class="wncs-content">{parts[2]}</span></div>'
        else:
            parts = line.split('|')
            if len(parts) >= 5:
                html += f'<div class="wncs-item"><div class="wncs-info">{parts[1]} | 👍 {parts[3]}</div><div class="wncs-main"><span class="wncs-user">{parts[0]}</span> {parts[4]}</div></div>'
    html += '</div>'
    summary_label = "🔻 댓글창 (Comments)"
    if gn_text or an_text:
        summary_label += '<div style="margin-top: 6px; font-weight: normal; font-size: 0.85em; color: inherit; opacity: 0.8; line-height: 1.4;">'
        if gn_text: summary_label += f'{gn_text}<br>'
        if an_text: summary_label += f'{an_text}'
        summary_label += '</div>'
    return f'<details><summary>{summary_label}</summary>{html}</details>'

def format_novel_content(text):
    if not text: return ""
    
    # 1. 기본 청소
    text = text.strip()
    text = text.replace('[Status Interface]', '')
    text = RE_HEADER_RESPONSE.sub('', text)
    text = RE_HEADER_SHARP.sub('', text)
    text = RE_LB_LAZY.sub('', text)
    text = RE_HANJA_BRACKET.sub('', text)
    text = RE_PREV_SUMMARY.sub('', text)
    text = RE_MULTI_NEWLINE.sub('\n\n', text)

    lines = text.split('\n')
    filtered_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            filtered_lines.append(line)
            continue
        if (stripped.startswith('HN[') or stripped.startswith('WNCS{') or stripped.startswith('[Date') or stripped.startswith('[Level') or stripped.startswith('[ ')):
            filtered_lines.append(line)
            continue
        eng_count = sum(1 for c in line if 65 <= ord(c) <= 90 or 97 <= ord(c) <= 122)
        if len(line) > 0 and (eng_count / len(line)) >= 0.2:
            continue
        filtered_lines.append(line)
    text = '\n'.join(filtered_lines)

    # 2. 따옴표 표준화 (가장 먼저 수행)
    replacements = {
        '“': '"', '”': '"', '〝': '"', '〞': '"', '″': '"',
        '‘': "'", '’': "'", '‚': "'", '‛': "'", '′': "'",
        '『': '"', '』': '"', '「': "'", '」': "'" 
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # 3. [중요] 구조적 태그 보호 (Protect Structural Tags FIRST)
    # 이미지, 상태창 등 HTML 태그가 포함된 요소들을 먼저 보호하여
    # 이후 텍스트 스타일링 로직(대화/속마음)이 건드리지 못하게 함.
    protected_map = {}
    def protect_content(content):
        key = f"__KVIEWER_PROTECTED_{uuid.uuid4().hex}__"
        protected_map[key] = content
        return key

    # (1) 이미지 태그 보호
    text = RE_IMG_TAG.sub(lambda m: protect_content(f"<div class='novel-img-placeholder'>🖼️ [Image] {m.group(1)}</div>"), text)

    # (2) 상태창 보호
    def convert_status_content(raw_content):
        if not RE_STATUS_DATE.search(raw_content): return None
        date_match = RE_STATUS_DATE.search(raw_content)
        time_match = RE_STATUS_TIME.search(raw_content)
        parts = []
        if date_match: parts.append(f"📅 {date_match.group(1).strip()}")
        if time_match: parts.append(f"⏰ {time_match.group(1).strip()}")
        if not parts: return ""
        html = f"<div class='novel-dateline'>{' &nbsp;|&nbsp; '.join(parts)}</div>"
        return protect_content(html)
    text = parse_nested_block(text, '', '[', ']', convert_status_content)

    # (3) 커뮤니티/댓글창 보호
    text = parse_nested_block(text, 'HN[', '[', ']', lambda c: protect_content(convert_hn_content(c)))
    text = parse_nested_block(text, 'WNCS{', '{', '}', lambda c: protect_content(convert_wncs_content(c)))

    # (4) 시스템 메시지 보호
    def repl_sys_msg_brace_wrapper(match):
        content = match.group(1)
        content = content.replace('**', '') 
        return protect_content(f"<div class='system-msg'>🔔 System: {content}</div>")
    text = RE_SYS_MSG_BRACE.sub(repl_sys_msg_brace_wrapper, text)

    def repl_sys_msg_wrapper(match):
        content = match.group(1)
        return protect_content(f"<div class='system-msg'>🔔 System: {content}</div>")
    text = RE_SYS_MSG.sub(repl_sys_msg_wrapper, text)

    # 4. 텍스트 스타일링 (이제 안전함!)
    # (1) 대화문 마킹
    text = RE_QUOTE_DOUBLE.sub(r'﹇DIA_S﹈\1﹇DIA_E﹈', text)
    
    # (2) 작은따옴표(속마음/강조) 분류
    def single_quote_classifier(match):
        content = match.group(1)
        stripped = content.strip()
        if not stripped: return f"'{content}'"
        
        # 15자 이상이거나 문장부호가 있으면 '속마음'
        is_thought = (len(stripped) >= 15) or (stripped[-1] in ['.', '?', '!', '…', '~'])
        
        if is_thought:
            return f'<span class="thought">‘{content}’</span>'
        else:
            return f'<span class="emphasis">‘{content}’</span>'

    text = RE_QUOTE_SINGLE.sub(single_quote_classifier, text)

    # (3) 대화문 HTML 변환
    text = text.replace('﹇DIA_S﹈', '<span class="dialogue">“')
    text = text.replace('﹇DIA_E﹈', '”</span>')

    # 5. 보호된 태그 복원
    for key, html in protected_map.items():
        text = text.replace(key, html)

    text = RE_MULTI_NEWLINE.sub('\n\n', text)
    text = text.replace('\n', '<br>')
    return text

@st.cache_data(show_spinner=False)
def get_novel_content(file_content, chunk_size=1000):
    try:
        json_data = json.loads(file_content)
        messages = []
        if 'data' in json_data and 'message' in json_data['data']:
            for item in json_data['data']['message']:
                if item.get('role') == 'char' and item.get('data'):
                    messages.append(item.get('data'))
        if not messages: return None, "내용 없음"

        final_pages = [] 
        for content in messages:
            formatted_text = format_novel_content(content)
            paragraphs = formatted_text.split('<br>')
            current_page_content = ""
            for p in paragraphs:
                paragraph_len = len(p)
                if len(current_page_content) + paragraph_len < chunk_size:
                    if current_page_content: current_page_content += "<br>" + p
                    else: current_page_content = p
                else:
                    if current_page_content: final_pages.append(f'<div class="novel-text">{current_page_content}</div>')
                    current_page_content = p
            if current_page_content: final_pages.append(f'<div class="novel-text">{current_page_content}</div>')
            if final_pages: final_pages[-1] += '<hr class="chapter-divider">'
        return final_pages, None
    except Exception as e:
        return None, str(e)