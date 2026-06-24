/* 樂學教室 6/25 期末考 — 向量考卷生成器
 * 範圍：翰林版 3-5～4-3｜每題一張 SVG 圖｜SEL + 生活連結 + 素養
 * 產出：exam.html（學生卷）/ answer.html（教師答案與評分）
 */
const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "樂學教室_6-25期末考_正式版");

/* ---------- 設計色票 ---------- */
const C = {
  ink: "#243049",      // 主墨色（圖形外框 / 標題）
  inkSoft: "#5A6B86",
  teal: "#0E8A8A",     // 已知值
  tealFill: "#E2F4F3",
  coral: "#E4572E",    // 未知 / 要求
  coralFill: "#FDEBE4",
  gold: "#C9890B",     // 角度
  goldFill: "#FBF0D6",
  violet: "#7C6CF0",
  violetFill: "#EEEBFD",
  sky: "#2B7FC9",
  skyFill: "#E6F1FB",
  rose: "#D9477E",
  paper: "#FFFFFF",
  faint: "#F4F7FB",
  line: "#D7E0EC",
};

/* ---------- SVG 基礎工具 ---------- */
function svg(inner, vb = "0 0 600 360") {
  return `<svg viewBox="${vb}" xmlns="http://www.w3.org/2000/svg" class="fig">
  <defs>
    <filter id="ds" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#243049" flood-opacity="0.18"/>
    </filter>
    <linearGradient id="gShape" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF3FA"/>
    </linearGradient>
    <linearGradient id="gTeal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E8F6F5"/><stop offset="1" stop-color="#D2ECEB"/>
    </linearGradient>
    <linearGradient id="gGold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FCF3DB"/><stop offset="1" stop-color="#F6E6B8"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="${vb.split(" ")[2] - 4}" height="${vb.split(" ")[3] - 4}" rx="20" fill="${C.faint}" stroke="${C.line}" stroke-width="2"/>
  ${inner}
</svg>`;
}
const poly = (pts, fill, stroke = C.ink, w = 3.6) =>
  `<polygon points="${pts.map((p) => p.join(",")).join(" ")}" fill="${fill}" stroke="${stroke}" stroke-width="${w}" stroke-linejoin="round" filter="url(#ds)"/>`;
const line = (a, b, stroke, w = 3, dash = "") =>
  `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="${stroke}" stroke-width="${w}" ${dash ? `stroke-dasharray="${dash}"` : ""} stroke-linecap="round"/>`;
const dot = (p, r = 5, fill = C.ink) => `<circle cx="${p[0]}" cy="${p[1]}" r="${r}" fill="${fill}"/>`;
const txt = (p, s, opt = {}) => {
  const { size = 22, fill = C.ink, w = 700, anchor = "middle", italic = false } = opt;
  return `<text x="${p[0]}" y="${p[1]}" font-family="'Microsoft JhengHei','Noto Sans TC',sans-serif" font-size="${size}" font-weight="${w}" fill="${fill}" text-anchor="${anchor}" dominant-baseline="middle" ${italic ? 'font-style="italic"' : ""}>${s}</text>`;
};
// 角弧
function arc(c, r, a0, a1, stroke, w = 4) {
  const p0 = [c[0] + r * Math.cos(a0), c[1] + r * Math.sin(a0)];
  const p1 = [c[0] + r * Math.cos(a1), c[1] + r * Math.sin(a1)];
  const large = Math.abs(a1 - a0) > Math.PI ? 1 : 0;
  const sweep = a1 > a0 ? 1 : 0;
  return `<path d="M ${p0[0]} ${p0[1]} A ${r} ${r} 0 ${large} ${sweep} ${p1[0]} ${p1[1]}" fill="none" stroke="${stroke}" stroke-width="${w}"/>`;
}
// 直角符號
function rightAngle(corner, d1, d2, len = 18, stroke = C.coral) {
  const n = (v) => { const m = Math.hypot(v[0], v[1]); return [v[0] / m, v[1] / m]; };
  const u = n(d1), v = n(d2);
  const p1 = [corner[0] + u[0] * len, corner[1] + u[1] * len];
  const p2 = [corner[0] + u[0] * len + v[0] * len, corner[1] + u[1] * len + v[1] * len];
  const p3 = [corner[0] + v[0] * len, corner[1] + v[1] * len];
  return `<polyline points="${p1[0]},${p1[1]} ${p2[0]},${p2[1]} ${p3[0]},${p3[1]}" fill="none" stroke="${stroke}" stroke-width="2.5"/>`;
}
const chip = (p, s, fill, ink) =>
  `<g><rect x="${p[0] - s.length * 7 - 14}" y="${p[1] - 17}" width="${s.length * 14 + 28}" height="34" rx="17" fill="${fill}"/>${txt([p[0], p[1] + 1], s, { size: 19, fill: ink, w: 800 })}</g>`;

/* ================= 各題圖形 ================= */
const FIG = {};

// 1) 三角形不等式：RGB 燈框
FIG.tri = () => {
  const A = [300, 52], B = [78, 300], Cc = [522, 300];
  return svg(`
    ${poly([A, B, Cc], "url(#gShape)")}
    ${line(A, B, "#E4572E", 7)}${line(A, Cc, "#16A34A", 7)}${line(B, Cc, "#2B7FC9", 7)}
    ${dot(A)}${dot(B)}${dot(Cc)}
    ${txt([300, 30], "A", { size: 24 })}${txt([52, 312], "B", { size: 24 })}${txt([548, 312], "C", { size: 24 })}
    ${txt([165, 158], "4", { size: 26, fill: "#C0392B" })}
    ${txt([437, 158], "9", { size: 26, fill: "#15803D" })}
    ${txt([300, 332], "2x − 1", { size: 26, fill: C.sky })}
    ${chip([300, 92], "RGB 三段燈條", "#FFFFFF", C.inkSoft)}`);
};

// 2) 三角形內角 → 拼平行四邊形
FIG.angle = () => {
  const A = [300, 52], B = [80, 300], Cc = [520, 300];
  return svg(`
    ${poly([A, B, Cc], "url(#gShape)")}
    ${dot(A)}${dot(B)}${dot(Cc)}
    ${txt([300, 30], "A", { size: 24 })}${txt([54, 312], "B", { size: 24 })}${txt([546, 312], "C", { size: 24 })}
    ${arc(B, 52, -0.86, 0, C.gold, 5)}
    ${arc(Cc, 52, Math.PI, Math.PI + 1.05, C.gold, 5)}
    ${txt([150, 268], "38°", { size: 23, fill: C.gold })}
    ${txt([452, 268], "72°", { size: 23, fill: C.gold })}
    ${txt([300, 118], "∠A = ?", { size: 24, fill: C.coral })}
    ${chip([300, 332], "兩塊全等三角形 → 拼平行四邊形", "#FFFFFF", C.inkSoft)}`);
};

// 平行線（內錯角 / 同側內角）共用 — 精確向量角弧
function parallelFig(mode, known) {
  const y1 = 116, y2 = 268, xl = 64, xr = 536;
  const P = [360, y1], Q = [250, y2];          // 截線與兩平行線交點
  const ux = (P[0] - Q[0]), uy = (P[1] - Q[1]);
  const ul = Math.hypot(ux, uy);
  const u = [ux / ul, uy / ul];                // Q→P 單位向量（往右上）
  const T_top = [P[0] + u[0] * 58, P[1] + u[1] * 58];
  const T_bot = [Q[0] - u[0] * 58, Q[1] - u[1] * 58];
  const ang = (dx, dy) => Math.atan2(dy, dx);
  const aQ = ang(-u[0], -u[1]);                // P→往下 (towardQ)
  const aP = ang(u[0], u[1]);                  // Q→往上 (towardP)
  const east = 0, west = Math.PI;
  const lab = (c, a, r, s, fill) => {
    const p = [c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)];
    return txt(p, s, { size: 23, fill, italic: s === "x", w: s === "x" ? 800 : 700 });
  };
  let arcs, labels;
  if (mode === "alt") {
    // 已知：P 內側左角(west↔towardQ)；x：Q 內側右角(towardP↔east) → 內錯角相等
    arcs = arc(P, 38, aQ, west, C.coral, 4) + arc(Q, 38, aP + 2 * Math.PI, 2 * Math.PI, C.teal, 4);
    labels = lab(P, (aQ + west) / 2, 42, known, C.coral) + lab(Q, (aP + 2 * Math.PI + 2 * Math.PI) / 2, 30, "x", C.teal);
  } else {
    // 已知：P 內側左角；x：Q 內側左角(west↔towardP) → 同側內角互補
    arcs = arc(P, 38, aQ, west, C.coral, 4) + arc(Q, 40, west, aP + 2 * Math.PI, C.teal, 4);
    labels = lab(P, (aQ + west) / 2, 42, known, C.coral) + lab(Q, (west + aP + 2 * Math.PI) / 2, 34, "x", C.teal);
  }
  return svg(`
    <rect x="${xl}" y="${y1}" width="${xr - xl}" height="${y2 - y1}" fill="url(#gGold)" opacity="0.45"/>
    ${line([xl, y1], [xr, y1], C.ink, 5)}
    ${line([xl, y2], [xr, y2], C.ink, 5)}
    ${line(T_bot, T_top, C.gold, 5)}
    ${dot(P, 5, C.ink)}${dot(Q, 5, C.ink)}
    ${txt([xr + 16, y1], "L₁", { size: 22, fill: C.inkSoft })}
    ${txt([xr + 16, y2], "L₂", { size: 22, fill: C.inkSoft })}
    ${arcs}${labels}
    ${chip([180, y1 - 26], "L₁ ∥ L₂", "#FFFFFF", C.inkSoft)}
    ${txt([300, 338], mode === "alt" ? "x 與已知角 → 內錯角（相等）" : "x 與已知角 → 同側內角（互補）", { size: 18, fill: C.inkSoft, w: 600 })}`);
}
FIG.alt = () => parallelFig("alt", "58°");
FIG.same = () => parallelFig("same", "63°");

// 5) 平行四邊形面積（E、F 中點，△BEF）
FIG.paArea = () => {
  const A = [120, 300], B = [430, 300], Cc = [540, 96], D = [230, 96];
  const E = [(A[0] + B[0]) / 2, 300]; // AB 中點
  const F = [(B[0] + Cc[0]) / 2, (B[1] + Cc[1]) / 2]; // BC 中點
  return svg(`
    ${poly([A, B, Cc, D], "url(#gShape)")}
    <polygon points="${B[0]},${B[1]} ${E[0]},${E[1]} ${F[0]},${F[1]}" fill="${C.coralFill}" stroke="${C.coral}" stroke-width="3"/>
    ${dot(A)}${dot(B)}${dot(Cc)}${dot(D)}${dot(E, 5, C.coral)}${dot(F, 5, C.coral)}
    ${txt([104, 312], "A", { size: 22 })}${txt([444, 320], "B", { size: 22 })}
    ${txt([556, 86], "C", { size: 22 })}${txt([214, 86], "D", { size: 22 })}
    ${txt([E[0], 326], "E", { size: 21, fill: C.coral })}${txt([F[0] + 20, F[1]], "F", { size: 21, fill: C.coral })}
    ${txt([352, 250], "△BEF = 3", { size: 21, fill: C.coral })}
    ${chip([300, 70], "E、F 分別是 AB、BC 的中點", "#FFFFFF", C.inkSoft)}`);
};

// 6) 對角線家族：平行四邊形 / 長方形 / 菱形
FIG.family = () => {
  const draw = (pts, labs, name) => {
    const cx = pts.reduce((s, p) => s + p[0], 0) / 4;
    return `${poly(pts, "url(#gShape)", C.ink, 3)}
      ${line(pts[0], pts[2], C.violet, 2.6, "5 4")}${line(pts[1], pts[3], C.violet, 2.6, "5 4")}
      ${pts.map((p, i) => txt([p[0] + labs[i][1], p[1] + labs[i][2]], labs[i][0], { size: 18 })).join("")}
      ${txt([cx, 332], name, { size: 20, fill: C.ink })}`;
  };
  const L = (a, dx, dy) => [a, dx, dy];
  return svg(`
    ${draw([[40, 250], [175, 250], [205, 110], [70, 110]], [L("A", -16, 8), L("B", 14, 8), L("C", 14, -8), L("D", -16, -8)], "平行四邊形")}
    ${draw([[250, 250], [400, 250], [400, 110], [250, 110]], [L("E", -16, 8), L("F", 14, 8), L("G", 14, -8), L("H", -16, -8)], "長方形")}
    ${draw([[505, 110], [575, 180], [505, 250], [435, 180]], [L("I", 0, -16), L("J", 16, 0), L("K", 0, 16), L("L", -16, 0)], "菱形")}`, "0 0 600 360");
};

// 7) 風箏（箏形）面積
FIG.kite = () => {
  const A = [300, 46], Cc = [300, 322], B = [150, 168], D = [450, 168], O = [300, 168];
  return svg(`
    ${poly([A, B, Cc, D], "url(#gShape)", C.teal, 3.6)}
    ${line(A, Cc, C.gold, 3, "6 5")}${line(B, D, C.gold, 3, "6 5")}
    ${rightAngle(O, [1, 0], [0, -1], 16, C.coral)}
    ${dot(A)}${dot(B)}${dot(Cc)}${dot(D)}${dot(O, 4, C.gold)}
    ${txt([300, 26], "A", { size: 22 })}${txt([128, 168], "B", { size: 22 })}
    ${txt([300, 344], "C", { size: 22 })}${txt([472, 168], "D", { size: 22 })}${txt([322, 188], "O", { size: 19, fill: C.gold })}
    ${txt([205, 96], "AB = 10", { size: 20, fill: C.teal })}
    ${txt([205, 250], "BC = 17", { size: 20, fill: C.teal })}
    ${txt([300, 144], "BD = 16", { size: 20, fill: C.coral })}`);
};

// 8) 梯形中點連線
FIG.trapMid = () => {
  const A = [80, 300], B = [520, 300], Cc = [420, 92], D = [185, 92];
  const E = [(A[0] + D[0]) / 2, (A[1] + D[1]) / 2], F = [(B[0] + Cc[0]) / 2, (B[1] + Cc[1]) / 2];
  return svg(`
    ${poly([A, B, Cc, D], "url(#gShape)")}
    ${line(E, F, C.coral, 4, "2 0")}
    ${dot(A)}${dot(B)}${dot(Cc)}${dot(D)}${dot(E, 5, C.coral)}${dot(F, 5, C.coral)}
    ${txt([62, 312], "A", { size: 22 })}${txt([536, 312], "B", { size: 22 })}
    ${txt([432, 80], "C", { size: 22 })}${txt([170, 80], "D", { size: 22 })}
    ${txt([E[0] - 22, E[1]], "E", { size: 20, fill: C.coral })}${txt([F[0] + 22, F[1]], "F", { size: 20, fill: C.coral })}
    ${txt([300, 80], "上底 DC = 6", { size: 20, fill: C.teal })}
    ${txt([300, 326], "下底 AB = 14", { size: 20, fill: C.teal })}
    ${txt([300, 188], "EF = ?", { size: 22, fill: C.coral })}
    ${chip([300, 130], "E、F 是兩腰中點", "#FFFFFF", C.inkSoft)}`);
};

// 9) 梯形面積（中點線 × 高）
FIG.trapArea = () => {
  const A = [90, 300], B = [510, 300], Cc = [395, 92], D = [205, 92];
  const E = [(A[0] + D[0]) / 2, (A[1] + D[1]) / 2], F = [(B[0] + Cc[0]) / 2, (B[1] + Cc[1]) / 2];
  const H = [D[0], 300];
  return svg(`
    ${poly([A, B, Cc, D], "url(#gShape)")}
    ${line(E, F, C.coral, 4)}
    ${line(D, H, C.gold, 3, "6 5")}${rightAngle(H, [1, 0], [0, -1], 15, C.coral)}
    ${dot(A)}${dot(B)}${dot(Cc)}${dot(D)}${dot(E, 5, C.coral)}${dot(F, 5, C.coral)}
    ${txt([72, 312], "A", { size: 22 })}${txt([526, 312], "B", { size: 22 })}
    ${txt([406, 80], "C", { size: 22 })}${txt([192, 80], "D", { size: 22 })}
    ${txt([H[0], 320], "H", { size: 19, fill: C.gold })}
    ${txt([300, 80], "上底 = 7", { size: 20, fill: C.teal })}
    ${txt([300, 326], "下底 = 11", { size: 20, fill: C.teal })}
    ${txt([243, 196], "高 8", { size: 20, fill: C.gold })}
    ${txt([430, 188], "EF = ?", { size: 21, fill: C.coral })}`);
};

// 10) 等腰梯形 + 畢氏
FIG.isos = () => {
  const A = [85, 300], B = [515, 300], Cc = [410, 96], D = [190, 96];
  const H = [D[0], 300];
  return svg(`
    ${poly([A, B, Cc, D], "url(#gShape)")}
    ${line(D, H, C.gold, 3, "6 5")}${rightAngle(H, [1, 0], [0, -1], 15, C.coral)}
    ${dot(A)}${dot(B)}${dot(Cc)}${dot(D)}
    ${txt([67, 312], "A", { size: 22 })}${txt([531, 312], "B", { size: 22 })}
    ${txt([421, 84], "C", { size: 22 })}${txt([178, 84], "D", { size: 22 })}
    ${txt([H[0], 320], "H", { size: 19, fill: C.gold })}
    ${txt([300, 84], "CD = 7", { size: 20, fill: C.teal })}
    ${txt([300, 326], "AB = 25", { size: 20, fill: C.teal })}
    ${txt([120, 188], "AD = 15", { size: 19, fill: C.teal })}
    ${txt([232, 220], "高 ?", { size: 20, fill: C.coral })}
    ${txt([137, 318], "← 9 →", { size: 16, fill: C.inkSoft })}`);
};

// 11) 梯形反求下底
FIG.trapRev = () => {
  const A = [80, 300], B = [520, 300], Cc = [400, 92], D = [200, 92];
  const E = [(A[0] + D[0]) / 2, (A[1] + D[1]) / 2], F = [(B[0] + Cc[0]) / 2, (B[1] + Cc[1]) / 2];
  return svg(`
    ${poly([A, B, Cc, D], "url(#gShape)")}
    ${line(E, F, C.teal, 4)}
    ${dot(A)}${dot(B)}${dot(Cc)}${dot(D)}${dot(E, 5, C.teal)}${dot(F, 5, C.teal)}
    ${txt([62, 312], "A", { size: 22 })}${txt([536, 312], "B", { size: 22 })}
    ${txt([410, 80], "C", { size: 22 })}${txt([188, 80], "D", { size: 22 })}
    ${txt([E[0] - 22, E[1]], "E", { size: 20, fill: C.teal })}${txt([F[0] + 22, F[1]], "F", { size: 20, fill: C.teal })}
    ${txt([300, 80], "上底 DC = 7", { size: 20, fill: C.teal })}
    ${txt([300, 326], "下底 AB = ?", { size: 21, fill: C.coral })}
    ${txt([300, 188], "EF = 12", { size: 21, fill: C.teal })}`);
};

// 12) 長方形判別：等腰梯形反例
FIG.judge = () => {
  // 左：等腰梯形（對角線等長卻不是長方形）；右：長方形
  const t = [[60, 250], [240, 250], [200, 120], [100, 120]];
  const r = [[360, 250], [540, 250], [540, 120], [360, 120]];
  return svg(`
    ${poly(t, "url(#gShape)")}
    ${line(t[0], t[2], C.coral, 2.6, "5 4")}${line(t[1], t[3], C.coral, 2.6, "5 4")}
    ${txt([150, 290], "等腰梯形", { size: 20, fill: C.coral })}
    ${txt([150, 314], "對角線等長 ✗ 不是長方形", { size: 16, fill: C.inkSoft })}
    ${poly(r, "url(#gShape)")}
    ${line(r[0], r[2], C.teal, 2.6, "5 4")}${line(r[1], r[3], C.teal, 2.6, "5 4")}
    ${txt([450, 290], "長方形", { size: 20, fill: C.teal })}
    ${txt([450, 314], "等長 + 互相平分 ✓", { size: 16, fill: C.inkSoft })}`, "0 0 600 360");
};

/* ================= 題目資料 ================= */
const Q = [
  {
    n: 1, title: "三角形組得成嗎？", pts: 8, fig: "tri", level: "A",
    life: "動漫房 RGB 三段燈框", sel: "先看圖找三邊，再決定第三邊能多長。你做得到。",
    prompt: ["三段燈條長度是 4、9、2x − 1。", "要圍成一個三角形，求 x 的範圍。"],
    steps: ["① 第三邊要比「兩邊差」大、比「兩邊和」小：9 − 4 ＜ 2x − 1 ＜ 9 + 4",
      "② ＿＿＿ ＜ 2x − 1 ＜ ＿＿＿", "③ 三段同時 +1、再 ÷2 → ＿＿＿ ＜ x ＜ ＿＿＿"],
    hint: "兩邊差 ＜ 第三邊 ＜ 兩邊和。",
    ans: "3 ＜ x ＜ 7", sol: "5 ＜ 2x−1 ＜ 13 → 6 ＜ 2x ＜ 14 → 3 ＜ x ＜ 7",
  },
  {
    n: 2, title: "拼出最大的角", pts: 8, fig: "angle", level: "A",
    life: "動漫社全等三角形徽章", sel: "角度也能拼圖。先補滿三角形，再想拼起來的樣子。",
    prompt: ["一種三角形紙片，兩個內角是 38° 與 72°。", "用兩塊這種紙片拼成平行四邊形，最大的內角是幾度？"],
    steps: ["① 第三個角 = 180° − 38° − 72° = ＿＿＿°",
      "② 平行四邊形最大內角 = 180° − 最小角(38°) = ＿＿＿°"],
    hint: "三角形最小角的「補角」，就是平行四邊形最大的角。",
    ans: "142°", sol: "第三角 70°；最小角 38°，180−38 = 142°",
  },
  {
    n: 3, title: "斜坡的轉角（內錯角）", pts: 8, fig: "alt", level: "A",
    life: "滑板場兩道平行護欄", sel: "兩條平行線是好朋友，會把角度一模一樣傳過去。",
    prompt: ["兩道護欄 L₁ ∥ L₂，一條斜桿穿過。", "圖中 58° 與 x 是內錯角，求 x。"],
    steps: ["內錯角相等 → x = ＿＿＿°"],
    hint: "x 在兩平行線「中間、兩側」→ 內錯角 → 相等。",
    ans: "58°", sol: "內錯角相等，x = 58°",
  },
  {
    n: 4, title: "護欄的同側角", pts: 8, fig: "same", level: "A",
    life: "滑板場護欄轉折處", sel: "同一邊的兩個角會「湊成 180°」，像合作的隊友。",
    prompt: ["L₁ ∥ L₂，63° 與 x 在截線的同一側、兩線之間。", "求 x。"],
    steps: ["同側內角互補 → 63° + x = 180°", "x = ＿＿＿°"],
    hint: "同側內角 → 兩角相加 = 180°（互補）。",
    ans: "117°", sol: "180 − 63 = 117°",
  },
  {
    n: 5, title: "舞台板面積放大術", pts: 9, fig: "paArea", level: "B",
    life: "音樂祭 LED 舞台板", sel: "小三角形藏著大面板的祕密，跟著比例放大就好。",
    prompt: ["平行四邊形 ABCD，E、F 是 AB、BC 的中點。", "若 △BEF 面積 = 3，求平行四邊形 ABCD 面積。"],
    steps: ["① △BEF 用了「半個底 × 半個高」 → 是整個平行四邊形的 1/8",
      "② 平行四邊形面積 = 3 × ＿＿＿ = ＿＿＿"],
    hint: "中點各砍一半：1/2 × 1/2，三角形再 ÷2，合起來是 1/8。",
    ans: "24", sol: "△BEF = 1/8 × □ → □ = 3 × 8 = 24",
  },
  {
    n: 6, title: "對角線偵探（打 ○／×）", pts: 9, fig: "family", level: "B",
    life: "手機相框與收藏卡版型", sel: "每個四邊形都有性格，對角線就是它的指紋。",
    prompt: ["看圖判斷，每句對的打 ○、錯的打 ×。"],
    judge: ["(1) 平行四邊形的對角線互相平分。（　　）",
      "(2) 長方形的對角線等長，而且互相垂直。（　　）",
      "(3) 菱形的對角線互相垂直平分。（　　）",
      "(4) 正方形同時具有長方形與菱形的對角線性質。（　　）"],
    hint: "長方形是「等長 + 互相平分」，不一定垂直喔。",
    ans: "○、×、○、○", sol: "(2) 長方形對角線不垂直，故為 ×",
  },
  {
    n: 7, title: "做一只會飛的風箏", pts: 9, fig: "kite", level: "B",
    life: "校慶風箏工坊", sel: "把風箏切成上下兩個直角三角形，畢氏定理就來幫忙。",
    prompt: ["箏形 ABCD，AC 垂直平分 BD。AB = 10、BC = 17、BD = 16。", "求對角線 AC 與風箏面積。"],
    steps: ["① BO = 16 ÷ 2 = ＿＿＿", "② AO = √(10² − 8²) = ＿＿＿　CO = √(17² − 8²) = ＿＿＿",
      "③ AC = AO + CO = ＿＿＿", "④ 面積 = AC × BD ÷ 2 = ＿＿＿"],
    hint: "對角線互相垂直 → 面積 = 兩對角線相乘 ÷ 2。",
    ans: "AC = 21；面積 = 168", sol: "BO=8, AO=6, CO=15, AC=21, 面積=21×16÷2=168",
  },
  {
    n: 8, title: "中間那層架要多長？", pts: 8, fig: "trapMid", level: "B",
    life: "手搖飲店梯形展示架", sel: "中間層板 = 上下兩底的平均，公平地剛剛好。",
    prompt: ["梯形展示架，上底 DC = 6、下底 AB = 14。", "E、F 是兩腰中點，求中層板 EF。"],
    steps: ["中點連線 = (上底 + 下底) ÷ 2", "EF = (6 + 14) ÷ 2 = ＿＿＿"],
    hint: "兩底相加再除以 2。",
    ans: "10", sol: "(6+14)÷2 = 10",
  },
  {
    n: 9, title: "螢幕面積一次算出", pts: 8, fig: "trapArea", level: "B",
    life: "音樂祭梯形主螢幕", sel: "學會中點線，面積就是「中點線 × 高」，超省力。",
    prompt: ["梯形主螢幕，上底 7、下底 11、高 8。", "先求中點線 EF，再求面積。"],
    steps: ["① EF = (7 + 11) ÷ 2 = ＿＿＿", "② 面積 = EF × 高 = ＿＿＿ × 8 = ＿＿＿"],
    hint: "梯形面積 = 中點線 × 高。",
    ans: "EF = 9；面積 = 72", sol: "(7+11)÷2=9；9×8=72",
  },
  {
    n: 10, title: "電競平台鋪多大？", pts: 9, fig: "isos", level: "C", star: true,
    life: "電競舞台等腰梯形平台", sel: "切下兩個全等直角三角形，高度就藏在裡面。挑戰看看！",
    prompt: ["等腰梯形 ABCD，AB = 25、CD = 7、AD = BC = 15。", "求這座平台的面積。"],
    steps: ["① 左右各凸出 (25 − 7) ÷ 2 = ＿＿＿", "② 高 = √(15² − 9²) = ＿＿＿",
      "③ 面積 = (25 + 7) × 高 ÷ 2 = ＿＿＿"],
    hint: "先算左右凸出 9，再用畢氏求高 12。",
    ans: "192", sol: "凸出9，高=√(225−81)=12，(25+7)×12÷2=192",
  },
  {
    n: 11, title: "下底被藏起來了", pts: 8, fig: "trapRev", level: "C", star: true,
    life: "夾娃娃機梯形展示層", sel: "公式可以倒著用，把未知數請出來。",
    prompt: ["梯形中點連線 EF = 12，上底 DC = 7。", "反推下底 AB。"],
    steps: ["12 = (7 + AB) ÷ 2", "兩邊 ×2 → 24 = 7 + AB", "AB = ＿＿＿"],
    hint: "先把 ÷2 還原成 ×2。",
    ans: "17", sol: "24 = 7 + AB → AB = 17",
  },
  {
    n: 12, title: "哪句話不能只信一半？", pts: 8, fig: "judge", level: "C", star: true,
    life: "社群貼文卡片版型", sel: "敢說『我覺得這裡怪怪的』，是數學最帥的勇氣。",
    prompt: ["小明說：『只要兩條對角線等長，四邊形就是長方形。』", "請判斷對錯，並補上還缺的條件。"],
    steps: ["判斷：□ 正確　　□ 錯誤", "反例：圖左的「＿＿＿＿＿」對角線也等長，卻不是長方形",
      "補上條件：對角線還要「＿＿＿＿＿＿＿＿」才行"],
    hint: "等腰梯形對角線也等長；長方形還要『互相平分』。",
    ans: "錯誤；還要互相平分", sol: "等腰梯形是反例；長方形=對角線等長且互相平分",
  },
];

/* ================= HTML 組裝 ================= */
function stepsHTML(q, withAns) {
  const rows = (q.judge || q.steps).map(
    (s) => `<div class="step">${s}</div>`).join("");
  return `<div class="steps">${rows}</div>`;
}
function card(q, withAns) {
  const lv = { A: ["關卡 A", C.tealFill, C.teal], B: ["關卡 B", C.skyFill, C.sky], C: ["挑戰關", C.goldFill, C.gold] }[q.level];
  const star = q.star ? `<span class="star">★ 挑戰</span>` : "";
  const ansBlock = withAns
    ? `<div class="ansbox"><b>答案</b>　${q.ans}<div class="sol">${q.sol}</div></div>`
    : `<div class="work"><span>作答區</span></div>`;
  return `<section class="q">
    <div class="qhead">
      <div class="qno" style="background:${lv[2]}">${q.n}</div>
      <div class="qtitle">
        <h3>${q.title}　<span class="pts">（${q.pts} 分）</span>${star}</h3>
        <div class="chips">
          <span class="lvchip" style="background:${lv[1]};color:${lv[2]}">${lv[0]}</span>
          <span class="life">🎯 ${q.life}</span>
        </div>
      </div>
    </div>
    <div class="sel">💬 ${q.sel}</div>
    <div class="qbody">
      <div class="figwrap">${FIG[q.fig]()}</div>
      <div class="qright">
        <div class="prompt">${q.prompt.map((p) => `<p>${p}</p>`).join("")}</div>
        ${stepsHTML(q, withAns)}
        <div class="hint"><b>💡 卡關提示</b>　${q.hint}</div>
        ${ansBlock}
      </div>
    </div>
  </section>`;
}

const CSS = `
  * { box-sizing: border-box; margin: 0; padding: 0; }
  @page { size: A4; margin: 11mm 10mm; }
  body { font-family: 'Microsoft JhengHei','Noto Sans TC',sans-serif; color: ${C.ink};
         font-size: 13px; line-height: 1.5; background: #fff; }
  .wrap { max-width: 195mm; margin: 0 auto; }
  /* 封面抬頭 */
  .hero { border-radius: 22px; padding: 20px 26px; color: #fff; position: relative; overflow: hidden;
          background: linear-gradient(120deg,#243049 0%,#2E5C8A 55%,#0E8A8A 100%); box-shadow: 0 8px 24px rgba(36,48,73,.25); }
  .hero h1 { font-size: 27px; letter-spacing: 1px; }
  .hero .sub { opacity: .92; margin-top: 4px; font-size: 14px; }
  .hero .meta { margin-top: 12px; display: flex; gap: 10px; flex-wrap: wrap; }
  .hero .meta span { background: rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.35);
                     padding: 4px 12px; border-radius: 20px; font-size: 12.5px; }
  .hero .blob { position:absolute; right:-40px; top:-40px; width:180px; height:180px; border-radius:50%;
                background: rgba(255,255,255,.10); }
  .hero .blob2 { position:absolute; right:60px; bottom:-60px; width:120px; height:120px; border-radius:50%;
                background: rgba(244,183,64,.20); }
  /* 學生資訊列 */
  .info { display:flex; gap:10px; margin:12px 0; }
  .info .box { flex:1; border:1.5px solid ${C.line}; border-radius:12px; padding:8px 12px; font-weight:700; color:${C.inkSoft}; }
  /* SEL 開場 */
  .opening { background:${C.violetFill}; border-radius:16px; padding:14px 18px; margin-bottom:14px; border-left:6px solid ${C.violet}; }
  .opening b { color:${C.violet}; }
  .mood { margin-top:8px; display:flex; gap:8px; flex-wrap:wrap; font-size:12.5px; }
  .mood span { background:#fff; border:1.5px solid ${C.line}; border-radius:20px; padding:4px 12px; }
  /* 題卡 */
  .q { border:1.6px solid ${C.line}; border-radius:18px; padding:14px 16px; margin-bottom:14px;
       break-inside: avoid; background:#fff; box-shadow: 0 3px 10px rgba(36,48,73,.05); }
  .qhead { display:flex; align-items:flex-start; gap:12px; }
  .qno { color:#fff; width:38px; height:38px; border-radius:12px; font-size:21px; font-weight:800;
         display:flex; align-items:center; justify-content:center; flex:0 0 38px; box-shadow:0 3px 8px rgba(36,48,73,.18); }
  .qtitle h3 { font-size:17px; }
  .qtitle .pts { font-size:13px; color:${C.inkSoft}; font-weight:700; }
  .star { color:${C.gold}; font-size:13px; font-weight:800; margin-left:6px; }
  .chips { margin-top:5px; display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
  .lvchip { font-weight:800; padding:2px 11px; border-radius:14px; font-size:12px; }
  .life { font-size:12.5px; color:${C.inkSoft}; font-weight:700; }
  .sel { margin:9px 0 11px; background:${C.faint}; border-radius:12px; padding:8px 13px; font-size:12.5px; color:#3F5170; }
  .qbody { display:flex; gap:16px; align-items:flex-start; }
  .figwrap { flex:0 0 43%; }
  .fig { width:100%; height:auto; display:block; }
  .qright { flex:1; }
  .prompt p { margin-bottom:3px; font-size:13.5px; }
  .steps { margin-top:9px; }
  .step { background:${C.faint}; border:1px solid ${C.line}; border-radius:10px; padding:7px 12px; margin-bottom:6px; font-size:13px; }
  .hint { margin-top:9px; background:${C.goldFill}; border-radius:10px; padding:8px 12px; font-size:12.5px; }
  .hint b { color:${C.gold}; }
  .work { margin-top:9px; border:1.5px dashed ${C.line}; border-radius:10px; height:70px; position:relative; }
  .work span { position:absolute; top:6px; left:10px; font-size:11px; color:#A9B6C8; }
  .ansbox { margin-top:9px; background:${C.tealFill}; border-radius:10px; padding:9px 13px; font-size:13.5px; }
  .ansbox b { color:${C.teal}; }
  .sol { margin-top:4px; font-size:12px; color:${C.inkSoft}; }
  /* 結尾 */
  .closing { background:linear-gradient(120deg,${C.tealFill},${C.violetFill}); border-radius:16px; padding:14px 18px; margin-top:6px; }
  .closing b { color:${C.teal}; }
  .checklist { margin-top:8px; display:flex; gap:8px; flex-wrap:wrap; font-size:12.5px; }
  .checklist span { background:#fff; border:1.5px solid ${C.line}; border-radius:10px; padding:5px 12px; }
  .band { background:${C.ink}; color:#fff; border-radius:13px; padding:9px 16px; margin:16px 0 12px;
          font-size:15px; font-weight:800; display:flex; justify-content:space-between; }
  .band small { font-weight:500; opacity:.8; font-size:12px; }
  .foot { text-align:center; color:#A9B6C8; font-size:11px; margin-top:14px; }
`;

function page(title, withAns) {
  const sectionBand = (lv, label, sub) => {
    const items = Q.filter((q) => q.level === lv).map((q) => card(q, withAns)).join("");
    return `<div class="band">${label}<small>${sub}</small></div>${items}`;
  };
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
  <title>${title}</title><style>${CSS}</style></head><body><div class="wrap">
  <div class="hero">
    <div class="blob"></div><div class="blob2"></div>
    <h1>樂學教室 ✦ 數學期末闖關地圖</h1>
    <div class="sub">八年級下學期第三次段考　範圍：翰林版 3-5 ～ 4-3（三角形邊角・平行線・四邊形・梯形）</div>
    <div class="meta"><span>📅 6/25（四）期末考</span><span>🧭 12 關・滿分 100</span><span>🖼️ 每題都有圖</span><span>🌿 慢慢來，一步一步</span></div>
  </div>
  ${withAns ? `<div class="opening"><b>教師版 ✦ 答案與評分</b>　每題附最短解法；性質正確、計算小錯，保留歷程分。對應原班段考 3-5～4-3 核心概念，學生下週回原班可直接銜接。</div>`
    : `<div class="info"><div class="box">班級：________</div><div class="box">座號：________</div><div class="box">姓名：____________</div><div class="box">得分：________</div></div>
  <div class="opening"><b>開考前，先深呼吸 🌿</b>　這張考卷的每一題都有圖。看不懂字沒關係，先看圖、圈出已知，再一步步算。卡住是正常的——你不是一個人，老師陪你。<div class="mood">今天的我：<span>😌 準備好了</span><span>🙂 有點緊張但可以</span><span>😟 需要老師提醒一下</span></div></div>`}
  ${sectionBand("A", "關卡 A ✦ 暖身基礎", "三角形與平行線　每題 8 分")}
  ${sectionBand("B", "關卡 B ✦ 四邊形與面積", "平行四邊形・箏形・梯形")}
  ${sectionBand("C", "挑戰關 ✦ 銜接原班", "畢氏・逆推・判別　做完核心再挑戰")}
  ${withAns ? "" : `<div class="closing"><b>闖關完成，給自己一個讚 👏</b>　寫完後檢查三件事，勾起來：<div class="checklist"><span>☐ 內錯角／同側內角沒有搞混</span><span>☐ 長方形 vs 菱形對角線分清楚</span><span>☐ 面積記得寫單位</span></div><div style="margin-top:8px;font-size:12.5px;color:#3F5170">「我今天又往前走了一步。」——這句話，請對自己說一次。</div></div>`}
  <div class="foot">樂學教室期末考 ✦ 範圍對齊原班翰林版 3-5～4-3 ✦ 程式向量繪圖製作</div>
  </div></body></html>`;
}

// 各題圖形輸出成獨立 HTML（給 Chrome 轉 PNG 用，供 Word 嵌入）
const FIGDIR = process.env.FIGDIR || path.join(OUT, "_figs_html");
fs.mkdirSync(FIGDIR, { recursive: true });
for (const k of Object.keys(FIG)) {
  const one = `<!doctype html><meta charset=utf-8><body style="margin:0;background:#fff">
<div style="width:600px;height:360px">${FIG[k]()}</div></body>`;
  fs.writeFileSync(path.join(FIGDIR, `${k}.html`), one, "utf8");
}

// 圖形檢視畫廊（除錯用）
const gallery = `<!doctype html><meta charset=utf-8><body style="background:#fff;font-family:sans-serif">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;width:1100px">
${Object.keys(FIG).map((k) => `<div style="border:1px solid #ccc"><div style="background:#eee;padding:4px">${k}</div>${FIG[k]()}</div>`).join("")}
</div></body>`;
fs.writeFileSync(path.join(OUT, "_gallery.html"), gallery, "utf8");
fs.writeFileSync(path.join(OUT, "exam.html"), page("樂學教室期末考｜學生卷", false), "utf8");
fs.writeFileSync(path.join(OUT, "answer.html"), page("樂學教室期末考｜教師答案卷", true), "utf8");
console.log("OK ->", OUT);
