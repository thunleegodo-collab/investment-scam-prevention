"""
3ファイルにハンバーガーメニュー（モバイル対応ナビ）を追加するスクリプト
"""
import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── 共通CSS ──────────────────────────────────────────────────
HAMBURGER_CSS = """
    /* ========= HAMBURGER MENU ========= */
    .hamburger {
      display: none;
      background: none; border: none;
      color: #fff; font-size: 1.6rem;
      cursor: pointer; padding: .2rem .4rem;
      line-height: 1; border-radius: 4px;
      transition: background .15s;
    }
    .hamburger:hover { background: rgba(255,255,255,.12); }

    /* モバイルドロワー */
    .nav-drawer {
      display: none;
      position: fixed; top: 60px; left: 0; right: 0; z-index: 99;
      background: var(--navy);
      flex-direction: column;
      box-shadow: 0 6px 20px rgba(0,0,0,.35);
      border-top: 1px solid rgba(255,255,255,.08);
    }
    .nav-drawer.open { display: flex; }
    .nav-drawer a {
      color: #cbd5e0; text-decoration: none;
      padding: .9rem 1.75rem; font-size: 1rem;
      border-bottom: 1px solid rgba(255,255,255,.06);
      transition: background .15s, color .15s;
      display: flex; align-items: center; gap: .5rem;
    }
    .nav-drawer a:hover { background: rgba(255,255,255,.07); color: #fff; }
    .nav-drawer a.active { color: #fff; font-weight: 700; }
    .nav-drawer a.news-link {
      color: #fff; background: rgba(229,62,62,.2);
    }
    .nav-drawer a.news-link:hover { background: rgba(229,62,62,.35); }
    .nav-drawer a.checker-link {
      color: #fff; background: rgba(43,108,176,.25);
    }
    .nav-drawer a.checker-link:hover { background: rgba(43,108,176,.4); }
"""

# ── 共通JS ────────────────────────────────────────────────────
HAMBURGER_JS = """
<script>
(function() {
  var btn    = document.getElementById('hamburger');
  var drawer = document.getElementById('nav-drawer');
  if (!btn || !drawer) return;

  function closeMenu() {
    drawer.classList.remove('open');
    btn.textContent = '☰';
    btn.setAttribute('aria-expanded', 'false');
  }
  function toggleMenu() {
    var isOpen = drawer.classList.toggle('open');
    btn.textContent = isOpen ? '✕' : '☰';
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  }

  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    toggleMenu();
  });

  // ドロワー外クリックで閉じる
  document.addEventListener('click', function(e) {
    if (!drawer.contains(e.target) && e.target !== btn) {
      closeMenu();
    }
  });

  // リンククリックで閉じる
  drawer.querySelectorAll('a').forEach(function(a) {
    a.addEventListener('click', closeMenu);
  });

  // Escキー
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeMenu();
  });
})();
</script>
"""

# ── ファイルごとの設定 ────────────────────────────────────────
FILES = {
    "index.html": {
        "breakpoint": "640px",
        "nav_links_hide": ".nav-links { display: none; }",
        # ナビのHTMLリンク一覧（ドロワー用）
        "drawer_links": """  <a href="#warning">⚠ 危険サイン</a>
  <a href="#types">📋 詐欺の手口</a>
  <a href="#checklist">✔ チェックリスト</a>
  <a href="#steps">🆘 被害にあったら</a>
  <a href="#resources">📞 相談窓口</a>
  <a href="checker.html" class="checker-link">🔍 業者チェック</a>
  <a href="news.html" class="news-link">📰 ニュース</a>""",
    },
    "checker.html": {
        "breakpoint": "480px",
        "nav_links_hide": ".nav-links { display: none; }",
        "drawer_links": """  <a href="index.html">🏠 トップ</a>
  <a href="index.html#warning">⚠ 危険サイン</a>
  <a href="index.html#checklist">✔ チェックリスト</a>
  <a href="checker.html" class="active checker-link">🔍 業者チェック</a>
  <a href="news.html" class="news-link">📰 ニュース</a>""",
    },
    "news.html": {
        "breakpoint": "768px",
        "nav_links_hide": ".nav-links { display: none; }",
        "drawer_links": """  <a href="index.html">🏠 トップ</a>
  <a href="index.html#warning">⚠ 危険サイン</a>
  <a href="index.html#checklist">✔ チェックリスト</a>
  <a href="checker.html" class="checker-link">🔍 業者チェック</a>
  <a href="news.html" class="active news-link">📰 ニュース</a>""",
    },
}

for filename, cfg in FILES.items():
    path = Path(filename)
    if not path.exists():
        print(f"スキップ（なし）: {filename}")
        continue

    html = path.read_text(encoding="utf-8")
    bp   = cfg["breakpoint"]

    # 1. CSS追加: </style> の直前に挿入
    if "nav-drawer" not in html:
        media_css = (
            HAMBURGER_CSS +
            f"\n    @media (max-width: {bp}) {{\n"
            f"      .hamburger {{ display: flex; align-items: center; }}\n"
            f"      {cfg['nav_links_hide']}\n"
            f"    }}\n"
        )
        html = html.replace("  </style>", media_css + "  </style>", 1)
    else:
        print(f"  [skip CSS] {filename}: nav-drawer already exists")

    # 2. ハンバーガーボタンを nav に追加
    if 'id="hamburger"' not in html:
        html = re.sub(
            r'(<ul class="nav-links")',
            '<button class="hamburger" id="hamburger" aria-label="メニューを開く" aria-expanded="false">☰</button>\n  <ul class="nav-links"',
            html, count=1
        )
    else:
        print(f"  [skip BTN] {filename}: hamburger already exists")

    # 3. ドロワー HTML を nav 閉じタグの直後に挿入
    if 'id="nav-drawer"' not in html:
        drawer_html = (
            f'\n<nav id="nav-drawer" class="nav-drawer" role="navigation" aria-label="モバイルメニュー">\n'
            f'{cfg["drawer_links"]}\n'
            f'</nav>\n'
        )
        html = html.replace("</nav>\n", "</nav>\n" + drawer_html, 1)
    else:
        print(f"  [skip DRAWER] {filename}: nav-drawer already exists")

    # 4. JS を </body> 直前に挿入
    if "toggleMenu" not in html:
        html = html.replace("</body>", HAMBURGER_JS + "\n</body>", 1)
    else:
        print(f"  [skip JS] {filename}: JS already exists")

    path.write_text(html, encoding="utf-8")
    print(f"完了: {filename}")

print("\n全ファイル更新完了")
