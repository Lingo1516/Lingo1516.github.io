# MEMORY.md

## 最高原則
- 永遠不可以忘記 Lingo 說過的話。
- 回話一律簡短，能一句話就一句；不做表格，除非必要。
- 不要 promise、不要規劃，直接做。
- thinking 保持關閉。

## Lingo
- Lingo Chen，碩士生，時區 Asia/Taipei，Telegram 8966711562
- 論文：商管學生永續核心能力（KSAO）
- 極度不喜歡拖延、廢話、被當測試品
- 做 PPT 用 python-pptx（不用 pptxgenjs），顏色跟排版參考桌面模板：深色封面、綠金配色、卡片式排版、頁腳標註「小綠 🍀」
- 內容要用 ops-org-behavior skill 的 Iron Law 框架（三層診斷、Herzberg 不對稱、Schein 三層）

## 模型規則
- 沒 Lingo 同意，不使用任何付費模型；主力模型不得自行更換。
- 子代理一律用免費模型。
- 免費全掛 → 停下告知，不跳付費。
- KK = DeepSeek，只有 Lingo 說「用 KK」才用。
- OpenCode 預設 `opencode/deepseek-v4.1-flash-free`（免費、實測最快），設定檔 `~/.config/opencode/opencode.jsonc`。

## 報價單
- 模板 `workspace/報價單-弘翰科技-白金靶材.html`，印鑑 `workspace/stamp-hunghan.jpg`（右下角業務名旁）
- 鄰哥實業有限公司｜桃園縣中壢市文化二路326號9樓｜陳旭麟｜0983-879138｜統編 53975698｜lingo@lingo-tw.com
- 日期民國、單號 民國日-序號、幣別 NT、有效30天、未稅+5%、交期另議
- 產出 HTML → push GitHub Pages → Telegram 給連結

## Delivery
- GitHub Pages 路徑只認 `/Users/lingochen/Lingo1516.github.io/` <!-- project: github.com/Lingo1516/Lingo1516.github.io -->
- 新聞網址格式：https://lingo1516.github.io/news-YYYY-MM-DD.html
- 每則新聞要有「📖 閱讀全文」按鈕

## okrlingo 網站（Cloudflare Pages）
- 網址 https://okrlingo.pages.dev ，專案名 `okrlingo`，不是 git 連動，只能手動推
- 本地目錄 `~/okrlingo-site/`，改完跑：`cd ~/okrlingo-site && wrangler pages deploy . --project-name okrlingo --branch main`
- 部署後網址不變，仍是 okrlingo.pages.dev；使用者說「上傳」才推
- 其他 Pages 專案：teach(teach-bmp.pages.dev)、tutor、course、kc、mdo、okm
- `~/okrlingo-edit.sh` 走 DirectAdmin API 推到 okrlingo.xyz，舊主機備援，非 Pages 流程

## 歷史錯誤（不可再犯）
1. Email 傳錯地址
2. 股票分析廢話太多、給漲停股
3. 論文 PPT 拖 10 小時、誤用 Python
4. 只說「我會做」沒執行
5. HTML 沒驗證就給網址

## 排程
- 9:00 新聞懶人包、9:55 當沖分析、13:30 驗證報告、13:50 ET 美股報告
- 當沖分析與早上推薦儲存曾卡 error，需排查

## 工具
- pptxgenjs、cloudscraper、requests、EbookLib、BeautifulSoup4、yt-dlp、pdftotext、sherpa-onnx TTS
- OpenCode 手機入口：https://leadership-guide.vercel.app/m.html
- OpenCode DB 清理：`sqlite3 opencode.db "PRAGMA wal_checkpoint(TRUNCATE); VACUUM;"`

## 已知問題
- 系統碟曾變 read-only，需 `sudo diskutil apfs updatePreboot /`
- GitHub Pages 空白頁快取：加 ?v=2 跳快取

## opencode 交接（2026-10-23）
- 遲鈍根因：swap 滿、ContinuityCaptureAgent/WindowServer 吃 CPU → `~/Desktop/輸入提速.command`
- 工具雲端（自動同步桌面工具，含金鑰檔自動排除）：https://tools-44w.pages.dev ，腳本 `~/toolbox-runner/toolsync.sh`，執行台每 5 分自動推
- 工具執行台 port 4098（手機可開），審計 `/tmp/toolbox-run.log`
- 交接詳情（網址總表、10-22 晚起過程、密碼指引）：`memory/2026-10-23.md`；**明文密碼勿寫進 git**

_更新：2026-10-23_
