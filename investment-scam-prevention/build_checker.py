"""
checker.html ビルドスクリプト
fsa_all.json のデータを checker.html に埋め込み、3リスト対応版を生成する。
"""

import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

CHECKER_HTML = "checker.html"
ALL_JSON     = "fsa_all.json"
START_MARK   = "/* EMBEDDED_DB_START */"
END_MARK     = "/* EMBEDDED_DB_END */"

# ── JSON 読み込み ──────────────────────────────────────────
print("fsa_all.json を読み込み中...")
with open(ALL_JSON, encoding="utf-8") as f:
    data = json.load(f)

kinyushohin = data["kinyushohin"]
chuukai     = data["chuukai"]
touroku     = data["touroku"]
generated   = data["generated"]

k_json = json.dumps(kinyushohin, ensure_ascii=False, separators=(',', ':'))
c_json = json.dumps(chuukai,     ensure_ascii=False, separators=(',', ':'))
t_json = json.dumps(touroku,     ensure_ascii=False, separators=(',', ':'))

print(f"  金融商品取引業者: {len(kinyushohin)} 件")
print(f"  金融商品仲介業者: {len(chuukai)} 件")
print(f"  登録金融機関:     {len(touroku)} 件")

# ── checker.html 読み込み ──────────────────────────────────
print("checker.html を読み込み中...")
html = Path(CHECKER_HTML).read_text(encoding="utf-8")

# ── データ埋め込み部分を置換 ──────────────────────────────
new_db_block = (
    f"{START_MARK}\n"
    f"const EMBEDDED_KINYUSHOHIN={k_json};\n"
    f"const EMBEDDED_CHUUKAI={c_json};\n"
    f"const EMBEDDED_TOUROKU={t_json};\n"
    f"{END_MARK}"
)

# EMBEDDED_DB_START ... EMBEDDED_DB_END の間を全て置換
pattern = re.compile(
    re.escape(START_MARK) + r".*?" + re.escape(END_MARK),
    re.DOTALL
)
if not pattern.search(html):
    print("エラー: EMBEDDED_DB_START/END マーカーが見つかりません")
    sys.exit(1)

html = pattern.sub(new_db_block, html)

# ── JavaScript ロジックを新バージョンに置換 ────────────────
# // ===== データ管理 ===== から </script> まで置換
OLD_JS_START = "// ============================================================\n// データ管理"
NEW_JS = r"""
// ============================================================
// データ管理
// ============================================================
let DB = [];

// --- 正規化 ---
function normalize(str) {
  if (!str) return '';
  str = str.replace(/[Ａ-Ｚａ-ｚ０-９]/g, c =>
    String.fromCharCode(c.charCodeAt(0) - 0xFEE0)
  );
  str = str.replace(
    /株式会社|有限会社|合同会社|合資会社|合名会社|一般社団法人|一般財団法人|\(株\)|\(有\)|（株）|（有）/g, ''
  );
  return str.replace(/[\s\u3000]/g, '').toLowerCase();
}

// --- データ読み込み ---
function loadData() {
  const dot  = document.getElementById('status-dot');
  const text = document.getElementById('status-text');
  DB = [
    ...EMBEDDED_KINYUSHOHIN,
    ...EMBEDDED_CHUUKAI,
    ...EMBEDDED_TOUROKU,
  ];
  const total = DB.length;
  dot.className = 'status-dot ok';
  text.innerHTML =
    `金融庁データ読込済 — 計 <strong>${total.toLocaleString()}</strong> 件`
    + ` <span style="font-size:.78rem;color:#718096">(`
    + `取引業者 ${EMBEDDED_KINYUSHOHIN.length.toLocaleString()}・`
    + `仲介業者 ${EMBEDDED_CHUUKAI.length.toLocaleString()}・`
    + `登録金融機関 ${EMBEDDED_TOUROKU.length.toLocaleString()}`
    + `)</span>`;
  document.getElementById('search-btn').disabled = false;
}

// ============================================================
// 検索ロジック
// ============================================================
function searchDB(name, address) {
  const normName = normalize(name);
  const normAddr = normalize(address);

  if (!normName) return { matched: [], partial: [] };

  const matched  = [];
  const partial  = [];

  for (const entry of DB) {
    const nameHit =
      entry.name_n.includes(normName) || normName.includes(entry.name_n);
    if (!nameHit) continue;

    if (normAddr && normAddr.length >= 3) {
      const addrHit =
        entry.addr_n.includes(normAddr) || normAddr.includes(entry.addr_n);
      if (addrHit) matched.push(entry);
      else partial.push(entry);
    } else {
      matched.push(entry);
    }
  }

  return { matched, partial };
}

// ============================================================
// 検索実行
// ============================================================
function doSearch() {
  const name    = document.getElementById('company-name').value.trim();
  const address = document.getElementById('company-address').value.trim();

  if (!name) {
    document.getElementById('company-name').focus();
    showFlash('会社名を入力してください');
    return;
  }

  const { matched, partial } = searchDB(name, address);

  if (matched.length > 0) {
    showModal('safe', name, address, matched[0]);
  } else if (partial.length > 0) {
    showModal('warning', name, address, partial[0]);
  } else {
    showModal('danger', name, address, null);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  ['company-name', 'company-address'].forEach(id => {
    document.getElementById(id).addEventListener('keydown', e => {
      if (e.key === 'Enter') doSearch();
    });
  });
  loadData();
  document.getElementById('search-btn').disabled = true;
});

// ============================================================
// 業種ラベル・Excel リンクのマッピング
// ============================================================
const CATEGORY_LABEL = {
  '金融商品取引業者': '金融商品取引業者',
  '金融商品仲介業者': '金融商品仲介業者',
  '登録金融機関':     '登録金融機関',
};
const CATEGORY_EXCEL = {
  '金融商品取引業者': 'https://www.fsa.go.jp/menkyo/menkyoj/kinyushohin.xlsx',
  '金融商品仲介業者': 'https://www.fsa.go.jp/menkyo/menkyoj/chuukai.xlsx',
  '登録金融機関':     'https://www.fsa.go.jp/menkyo/menkyoj/touroku.xlsx',
};

// ============================================================
// モーダル制御
// ============================================================
function showModal(type, name, address, match) {
  const modal   = document.getElementById('modal');
  const overlay = document.getElementById('modal-overlay');

  modal.className = `modal ${type}`;

  const iconMap  = { danger: '🚨', warning: '⚠️', safe: '✅' };
  const titleMap = {
    danger:  '金融庁の登録が確認できませんでした',
    warning: '住所情報が一致しません',
    safe:    '金融庁の登録を確認しました',
  };
  const subMap = {
    danger:  '未登録業者への投資は詐欺の可能性が極めて高いです',
    warning: '社名は存在しますが、住所が登録と異なります。確認が必要です',
    safe:    '登録業者として確認されました。ただし登録＝安全ではありません',
  };

  document.getElementById('modal-icon').textContent     = iconMap[type];
  document.getElementById('modal-title').textContent    = titleMap[type];
  document.getElementById('modal-subtitle').textContent = subMap[type];
  document.getElementById('query-display').textContent  =
    address ? `${name}（${address}）` : name;

  const riskMap = {
    danger:  { pct: 83, cls: 'high',   label: '詐欺リスク 83%', caption: '金融庁未登録業者は詐欺の可能性が極めて高いです' },
    warning: { pct: 55, cls: 'medium', label: '詐欺リスク 55%', caption: '住所が登録と異なります。公式サイトで直接確認してください' },
    safe:    { pct: 10, cls: 'low',    label: '詐欺リスク 低',  caption: '登録は確認されましたが、最終判断は公式サイトでご確認ください' },
  };
  const risk = riskMap[type];

  document.getElementById('risk-label-r').textContent = risk.label;
  document.getElementById('risk-pct').textContent     = type !== 'safe' ? risk.label : '登録あり';
  document.getElementById('risk-pct').className       = `risk-pct ${risk.cls}`;
  document.getElementById('risk-caption').textContent = risk.caption;

  const bar = document.getElementById('risk-bar');
  bar.className = `risk-bar ${risk.cls}`;
  bar.style.width = '0%';
  setTimeout(() => { bar.style.width = risk.pct + '%'; }, 100);

  // 登録情報
  const matchEl = document.getElementById('match-info');
  if (match && type !== 'danger') {
    const cat = match.category || '金融商品取引業者';

    // 業種バッジ
    const catBadge = `<div style="margin-bottom:.75rem">
      <span style="background:#ebf4ff;color:#2b6cb0;font-size:.75rem;font-weight:700;
        padding:.2rem .6rem;border-radius:4px;border:1px solid #bee3f8">${escHtml(cat)}</span>
    </div>`;

    // 業務種別（取引業者のみ）
    let bizTypes = '';
    if (cat === '金融商品取引業者') {
      const types = [];
      if (match.type1    && match.type1.includes('○'))    types.push('第一種金融商品取引業');
      if (match.type2    && match.type2.includes('○'))    types.push('第二種金融商品取引業');
      if (match.advisory && match.advisory.includes('○')) types.push('投資助言・代理業');
      if (match.mgmt     && match.mgmt.includes('○'))     types.push('投資運用業');
      if (types.length) {
        bizTypes = `<div class="mi-label">業務種別</div>
          <div class="mi-value">${types.map(escHtml).join('、')}</div>`;
      }
    }

    // 仲介業者専用フィールド
    let chuukaiFields = '';
    if (cat === '金融商品仲介業者') {
      if (match.corp_type) {
        chuukaiFields += `<div class="mi-label">法人・個人の別</div>
          <div class="mi-value">${escHtml(match.corp_type)}</div>`;
      }
      if (match.belongs) {
        chuukaiFields += `<div class="mi-label">所属金融商品取引業者等</div>
          <div class="mi-value" style="font-size:.85rem">${escHtml(match.belongs)}</div>`;
      }
    }

    matchEl.style.display = 'block';
    matchEl.innerHTML = `
      ${catBadge}
      <div class="mi-label">登録業者名</div>
      <div class="mi-value">${escHtml(match.name)}</div>
      ${match.reg_no   ? `<div class="mi-label">登録番号</div><div class="mi-value">${escHtml(match.reg_no)}</div>` : ''}
      ${match.reg_date ? `<div class="mi-label">登録年月日</div><div class="mi-value">${escHtml(match.reg_date)}</div>` : ''}
      ${match.address  ? `<div class="mi-label">登録住所</div><div class="mi-value">${escHtml(match.address)}</div>` : ''}
      ${match.phone    ? `<div class="mi-label">電話番号</div><div class="mi-value">${escHtml(match.phone)}</div>` : ''}
      ${bizTypes}
      ${chuukaiFields}
    `;
  } else {
    matchEl.style.display = 'none';
  }

  // アクションボタン
  const actions = document.getElementById('modal-actions');
  const cat  = match ? (match.category || '金融商品取引業者') : null;
  const xlsxUrl = cat ? CATEGORY_EXCEL[cat] : null;

  if (type === 'danger') {
    actions.innerHTML = `
      <a class="btn-primary" href="tel:188">☎ 188（消費者ホットライン）に電話する</a>
      <a class="btn-secondary"
         href="https://www.fsa.go.jp/menkyo/menkyo.html"
         target="_blank" rel="noopener">金融庁 公式登録一覧で直接確認する ↗</a>
      <a class="btn-secondary" href="index.html#steps">被害にあったときの対処法を見る</a>
    `;
  } else if (type === 'warning') {
    actions.innerHTML = `
      <a class="btn-secondary"
         href="${xlsxUrl || 'https://www.fsa.go.jp/menkyo/menkyo.html'}"
         target="_blank" rel="noopener">金融庁の公式Excelで直接確認する ↗</a>
      <a class="btn-secondary"
         href="https://www.fsa.go.jp/ordinary/tyuui/"
         target="_blank" rel="noopener">金融庁 注意情報を確認する ↗</a>
    `;
  } else {
    actions.innerHTML = `
      <a class="btn-secondary"
         href="${xlsxUrl || 'https://www.fsa.go.jp/menkyo/menkyo.html'}"
         target="_blank" rel="noopener">金融庁の公式Excelで直接確認する ↗</a>
    `;
  }

  overlay.classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('show');
  document.body.style.overflow = '';
}

function closeModalOutside(e) {
  if (e.target === document.getElementById('modal-overlay')) closeModal();
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// ============================================================
// ユーティリティ
// ============================================================
function escHtml(str) {
  return str.replace(/[&<>"']/g, c =>
    ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c])
  );
}

function showFlash(msg) {
  const btn = document.getElementById('search-btn');
  const orig = btn.textContent;
  btn.textContent = '⚠ ' + msg;
  btn.style.background = '#c05621';
  setTimeout(() => {
    btn.textContent = orig;
    btn.style.background = '';
  }, 2000);
}
</script>

</body>
</html>"""

# 既存のJSコード部分を置換（// ============= データ管理 から </html> まで）
old_js_pattern = re.compile(
    re.escape(OLD_JS_START) + r".*$",
    re.DOTALL
)
if not old_js_pattern.search(html):
    print("エラー: JS開始マーカーが見つかりません")
    sys.exit(1)

new_js_clean = NEW_JS.lstrip("\n")
html = old_js_pattern.sub(lambda _: new_js_clean, html)

# ── page-header の説明文も3リスト対応に更新 ─────────────────
html = html.replace(
    "会社名と住所を入力するだけで、金融庁の金融商品取引業者登録一覧に掲載されているかを即座に確認できます。",
    "会社名と住所を入力するだけで、金融庁の<strong>金融商品取引業者・金融商品仲介業者・登録金融機関</strong>の3リストを一括検索できます。"
)

# ── 書き出し ──────────────────────────────────────────────
Path(CHECKER_HTML).write_text(html, encoding="utf-8")
print(f"\n完了: {CHECKER_HTML} を更新しました")
print(f"  総件数: {len(kinyushohin)+len(chuukai)+len(touroku)} 件")
