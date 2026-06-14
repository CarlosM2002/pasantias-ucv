import re
from pathlib import Path

ROOT_BASE = Path(__file__).resolve().parents[1]
TARGET_DIRS = ['static', 'template']
EXTS = {'.js', '.css', '.scss', '.html', '.htm'}

removed_files = []
def remove_html_comments(text: str) -> str:
    # remove HTML comments but preserve conditional comments like <!--[if ...]>...<![endif]-->
    def _repl(m):
        s = m.group(0)
        if re.search(r"\[if|\[endif", s, flags=re.I):
            return s
        return ''
    return re.sub(r'<!--.*?-->', _repl, text, flags=re.S)

for target in TARGET_DIRS:
    ROOT = ROOT_BASE / target
    if not ROOT.exists():
        continue
    for p in sorted(ROOT.rglob('*')):
        if p.suffix.lower() not in EXTS:
            continue
        if p.suffix.lower() == '.map':
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        original = text
        # remove block comments /* ... */
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
        # remove template comments {# ... #}
        text = re.sub(r'\{#.*?#\}', '', text, flags=re.S)
        # remove HTML comments <!-- ... --> unless conditional (IE) comments
        if p.suffix.lower() in {'.html', '.htm'}:
            text = remove_html_comments(text)
        # remove full-line single-line comments // ... (only when they start the line)
        text = re.sub(r'^\s*//.*$', '', text, flags=re.M)
        # remove trailing whitespace on lines
        text = '\n'.join([line.rstrip() for line in text.splitlines()]) + ('\n' if text.endswith('\n') else '')
        if text != original:
            p.write_text(text, encoding='utf-8')
            removed_files.append(str(p.relative_to(Path.cwd())))

print('Modified files:')
for f in removed_files:
    print(f)
print('Done')
