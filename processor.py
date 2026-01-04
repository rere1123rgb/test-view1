import re
import json
import streamlit as st
import uuid
import unicodedata

# [GLOBAL] 정규식
RE_HEADER_RESPONSE = re.compile(r'^#\s+응답.*$', re.MULTILINE)
RE_HEADER_SHARP = re.compile(r'^#{2,3}\s+.*$', re.MULTILINE)
RE_LB_LAZY = re.compile(r'<lb-lazy[^>]*>.*?</lb-lazy>', re.DOTALL)
RE_HANJA_BRACKET = re.compile(r'《([^가-힣]+?)》')
RE_MULTI_NEWLINE = re.compile(r'\n{3,}')
RE_ENGLISH_CHAR = re.compile(r'[a-zA-Z]')
RE_STATUS_DATE = re.compile(r'Date\s*:\s*([^|\]]+)', re.IGNORECASE)
RE_STATUS_TIME = re.compile(r'Time\s*:\s*([^|\]]+)', re.IGNORECASE)

# 허용할 안전한 태그 목록 (Whitelist)
ALLOWED_TAGS = {
    'div', 'span', 'p', 'br', 'hr', 'img', 'details', 'summary',
    'b', 'i', 'strong', 'em', 'u', 'mark', 'small', 'sub', 'sup', 'del', 'ins'
}

# 태그 패턴
RE_TAG_PATTERN = re.compile(r'<(/?[^\s>]+)([^>]*)>')

RE_SYS_MSG = re.compile(r'^-\s*System Message:\s*(.*)', re.MULTILINE)
RE_SYS_MSG_BRACE = re.compile(r'-\s*\{System\s+Message:\s*([\s\S]*?)\}', re.MULTILINE)

RE_QUOTE_DOUBLE = re.compile(r'"([^"]*)"')
RE_QUOTE_SINGLE = re.compile(r"'([^']*)'") 

RE_PREV_SUMMARY = re.compile(r'▽.*?△', re.DOTALL)

RE_LIGHTBOARD = re.compile(r'<lightboard-comments>(.*?)</lightboard-comments>', re.DOTALL | re.IGNORECASE)

# 텍스트 정화 강화
def sanitize_text(text):
    if not text: return ""
    text = unicodedata.normalize('NFC', text)
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ufffd]', '', text)

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

def convert_lightboard_content(raw_content):
    lines = raw_content.strip().split('\n')
    html = '<div class="lightboard-container">'
    for line in lines:
        line = line.strip()
        if not line: continue
        is_post = line.startswith('[Post]')
        is_comment = line.startswith('[Comment]')
        if not (is_post or is_comment): continue
        content_part = line[6:] if is_post else line[9:]
        fields = content_part.split('|')
        data = {}
        for field in fields:
            if ':' in field:
                key, val = field.split(':', 1)
                data[key.strip()] = val.strip()
        author = data.get('Author', 'Unknown')
        time_str = data.get('Time', '')
        body = data.get('Content', '')
        meta_parts = []
        if time_str: meta_parts.append(time_str)
        if is_post:
            up = data.get('Upvotes', '0')
            down = data.get('Downvotes', '0')
            meta_parts.append(f"추천 {up}")
        meta_str = " | ".join(meta_parts)
        row_class = "lb-post" if is_post else "lb-comment"
        html += f'<div class="{row_class}"><span class="lb-header"><b>{author}</b> <span class="lb-meta">{meta_str}</span></span><br><span class="lb-body">{body}</span></div>'
    html += '</div>'
    return f'<details><summary>🔻 라이트보드 (Lightboard)</summary>{html}</details>'

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
            posts_html += f'<span class="comm-title">{p_data.get("PT", "")}</span><br>'
            posts_html += f'<span class="comm-meta">{p_data.get("PA","")} | {p_data.get("PDATE","")} | 조회 {p_data.get("PVIEWS","")} | 추천 {p_data.get("PRECOM","")}</span><br>'
            posts_html += f'<span class="comm-body">{p_data.get("PCONT", "")}</span>'
            if p_data['C']:
                posts_html += '<div class="comm-comments">'
                for author, body in p_data['C']:
                    posts_html += f'<span class="comm-cmt-row"><span class="comm-cmt-user">{author}</span> {body}</span><br>'
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
            if len(parts) >= 3:
                html += f'<div class="wncs-item wncs-reply"><span class="wncs-user">↳ {parts[1]}</span> {parts[2]}</div>'
        else:
            parts = line.split('|')
            if len(parts) >= 5:
                html += f'<div class="wncs-item"><span class="wncs-info">{parts[1]} | 👍 {parts[3]}</span><br><span class="wncs-user">{parts[0]}</span> {parts[4]}</div>'
    html += '</div>'
    summary_label = "🔻 댓글창 (Comments)"
    if gn_text: summary_label += f" - {gn_text}"
    return f'<details><summary>{summary_label}</summary>{html}</details>'

def format_novel_content(text):
    if not text: return ""
    text = sanitize_text(text)
    
    # [V86] 불필요한 메타데이터/더미 문자열 삭제 (최우선 처리)
    text = text.replace('<Thoughts>', '')
    text = text.replace('</Thoughts>', '')
    text = text.replace(''<!-- End platform managed -->, '')
    text = text.replace('<!-- End platform managed -->', '')
    
    text = text.strip()
    text = text.replace('[Status Interface]', '')
    text = RE_HEADER_RESPONSE.sub('', text)
    text = RE_HEADER_SHARP.sub('', text)
    text = RE_LB_LAZY.sub('', text)
    text = RE_HANJA_BRACKET.sub('', text)
    text = RE_PREV_SUMMARY.sub('', text)
    text = RE_MULTI_NEWLINE.sub('\n\n', text)

    protected_map = {}
    def protect_content(content):
        key = f"__KVIEWER_PROTECTED_{uuid.uuid4().hex}__"
        protected_map[key] = content
        return key

    text = RE_LIGHTBOARD.sub(lambda m: protect_content(convert_lightboard_content(m.group(1))), text)

    def repl_img_tag_safe(match):
        full_tag = match.group(0)
        file_match = re.search(r'[\'"]([^\'"]+)[\'"]', full_tag)
        filename = file_match.group(1) if file_match else "이미지"
        return protect_content(f"<div class='novel-img-placeholder'>🖼️ [Image] {filename}</div>")
    
    text = re.sub(r'<img[^>]+>', repl_img_tag_safe, text)

    # 태그 안전성 검사 (Whitelist)
    def check_and_protect_tag(match):
        full_tag = match.group(0)
        tag_name = match.group(1).replace('/', '').lower()
        if tag_name not in ALLOWED_TAGS:
            safe_text = full_tag.replace('<', '&lt;').replace('>', '&gt;')
            return protect_content(safe_text)
        return protect_content(full_tag)

    text = RE_TAG_PATTERN.sub(check_and_protect_tag, text)

    text = parse_nested_block(text, 'HN[', '[', ']', lambda c: protect_content(convert_hn_content(c)))
    text = parse_nested_block(text, 'WNCS{', '{', '}', lambda c: protect_content(convert_wncs_content(c)))

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

    def repl_sys_msg_brace_wrapper(match):
        content = match.group(1)
        content = content.replace('**', '') 
        return protect_content(f"<div class='system-msg'>🔔 System: {content}</div>")
    text = RE_SYS_MSG_BRACE.sub(repl_sys_msg_brace_wrapper, text)

    def repl_sys_msg_wrapper(match):
        content = match.group(1)
        return protect_content(f"<div class='system-msg'>🔔 System: {content}</div>")
    text = RE_SYS_MSG.sub(repl_sys_msg_wrapper, text)

    # 영어 문장 필터링 (보호된 블록 제외)
    lines = text.split('\n')
    filtered_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            filtered_lines.append(line)
            continue
        
        if stripped.startswith('__KVIEWER_PROTECTED_'):
            filtered_lines.append(line)
            continue
        
        eng_count = sum(1 for c in line if 65 <= ord(c) <= 90 or 97 <= ord(c) <= 122)
        if len(line) > 0 and (eng_count / len(line)) >= 0.3:
             continue 
        
        filtered_lines.append(line)
    text = '\n'.join(filtered_lines)

    replacements = {
        '“': '"', '”': '"', '〝': '"', '〞': '"', '″': '"',
        '‘': "'", '’': "'", '‚': "'", '‛': "'", '′': "'",
        '『': '"', '』': '"', '「': "'", '」': "'" 
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    text = RE_QUOTE_DOUBLE.sub(r'﹇DIA_S﹈\1﹇DIA_E﹈', text)
    
    def single_quote_classifier(match):
        content = match.group(1)
        stripped = content.strip()
        if not stripped: return f"'{content}'"
        is_thought = (len(stripped) >= 15) or (stripped[-1] in ['.', '?', '!', '…', '~'])
        if is_thought:
            return f'<span class="thought">‘{content}’</span>'
        else:
            return f'<span class="emphasis">‘{content}’</span>'

    text = RE_QUOTE_SINGLE.sub(single_quote_classifier, text)
    text = text.replace('﹇DIA_S﹈', '<span class="dialogue">“')
    text = text.replace('﹇DIA_E﹈', '”</span>')

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