# Phase 1: Chrome MCP Testing Environment Setup
**AI-Assistant Knowledge Hub - Chrome DevTools Testing Workflow**

## 🎯 目的
Termux環境でのChrome MCPテスト環境構築とブラウザ互換性確認

## 📋 前提条件チェック

### 1. Chrome DevTools MCP インストール確認
```bash
# バージョン確認
npx chrome-devtools-mcp --version
# 期待値: 0.4.0 または最新版

# グローバルインストールされているか確認
which npx chrome-devtools-mcp
# 期待値: /data/data/com.termux/files/usr/bin/npx
```

### 2. Chromium ブラウザ確認
```bash
# Chromiumバージョン確認
chromium-browser --version
# 期待値: Chromium 138.x.x.x またはそれ以上

# ヘッドレス起動テスト
chromium-browser --headless --version
# 期待値: バージョン表示（エラーなし）
```

### 3. Node.js & npm 環境確認
```bash
# Node.jsバージョン
node --version
# 期待値: v24.x.x またはそれ以上

# 必要パッケージインストール
npm list jsdom ws 2>/dev/null || npm install jsdom ws
# 期待値: インストール完了
```

## 🔧 Chrome DevTools Proxy Setup

### 1. 既存Proxyサービス確認
```bash
# Chrome DevToolsサービス状態確認
~/.chrome-devtools-service.sh status
# 期待値: "Service running (PID: XXXXX)" または "Service not running"

# 必要に応じて再起動
~/.chrome-devtools-service.sh stop
~/.chrome-devtools-service.sh start
```

### 2. Proxy API動作確認
```bash
# HTTP endpoint確認
curl -s http://localhost:9222 | jq
# 期待値: JSON レスポンス with description, version, webSocketDebuggerUrl

# WebSocket接続テスト
node -e "
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:9223/devtools');
ws.on('open', () => {
  console.log('✅ DevTools WebSocket connected');
  ws.close();
});
ws.on('error', (err) => {
  console.error('❌ WebSocket error:', err.message);
});
setTimeout(() => process.exit(1), 3000);
"
```

## 🚀 HTTP Server Setup

### 1. アプリケーションサーバー起動
```bash
# 利用可能ポート確認
netstat -tuln 2>/dev/null | grep :808 || echo "Ports 808x available"

# HTTP Server起動（バックグラウンド）
npx http-server -p 8085 -a 127.0.0.1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# 起動確認
sleep 2
curl -I http://127.0.0.1:8085
# 期待値: HTTP/1.1 200 OK
```

### 2. サーバー応答確認
```bash
# HTML配信確認
curl -s http://127.0.0.1:8085 | head -20
# 期待値: <!DOCTYPE html> で始まるHTML

# 静的ファイル確認
curl -I http://127.0.0.1:8085/core.js
curl -I http://127.0.0.1:8085/ui.js
curl -I http://127.0.0.1:8085/unified-ui-components.css
# 期待値: すべて HTTP/1.1 200 OK
```

## 📊 環境検証結果

### チェックリスト
- [ ] Chrome DevTools MCP v0.4.0+ インストール済み
- [ ] Chromium 138+ 利用可能
- [ ] Node.js v24+ 環境確認
- [ ] jsdom, ws パッケージ利用可能
- [ ] Chrome DevTools Proxy サービス稼働中
- [ ] WebSocket接続テスト成功
- [ ] HTTP Server (port 8085) 起動済み
- [ ] 静的ファイル配信確認済み

### 次のPhase準備
```bash
# 環境変数設定
export TEST_APP_URL="http://127.0.0.1:8085"
export CHROME_DEVTOOLS_PORT="9222"
export CHROME_DEVTOOLS_WS_PORT="9223"

echo "✅ Phase 1 完了 - Phase 2 に進んでください"
```

## 🛠️ トラブルシューティング

### よくある問題
1. **Chrome DevTools MCP not found**: `npm install -g chrome-devtools-mcp`
2. **Chromium not available**: `pkg install chromium`
3. **Port already in use**: 別のポート番号を使用
4. **WebSocket connection failed**: Proxyサービス再起動

### 確認コマンド
```bash
# プロセス確認
ps aux | grep -E "(chrome|node|http-server)"

# ポート使用状況
netstat -tuln | grep -E ":(808|922)"

# ログ確認
tail -f ~/.chrome-devtools.log 2>/dev/null || echo "No log file"
```

---

**Phase 1 完了条件**: すべてのチェックリスト項目が✅になること
**所要時間**: 約5-10分
**次のステップ**: Phase 2 - Static DOM Analysis
