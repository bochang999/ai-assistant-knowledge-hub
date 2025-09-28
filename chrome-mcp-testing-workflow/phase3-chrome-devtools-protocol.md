# Phase 3: Chrome DevTools Protocol Testing
**AI-Assistant Knowledge Hub - Chrome DevTools Testing Workflow**

## 🎯 目的
実際のChromiumブラウザを使用したDevTools Protocol経由でのリアルブラウザ動作テスト

## 📋 前提条件
- Phase 1, Phase 2 完了済み
- Chromium ブラウザ利用可能
- WebSocket パッケージ利用可能
- HTTP Server 稼働中

## 🔧 Chrome DevTools Protocol Setup

### 1. ヘッドレスChrome起動
```bash
# Chrome DevTools Protocol 用ポート確認
netstat -tuln | grep :9224 || echo "Port 9224 available"

# ヘッドレスChrome起動（デバッグポート有効）
echo "🚀 Starting headless Chrome with DevTools Protocol..."
chromium-browser \
  --headless \
  --remote-debugging-port=9224 \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --disable-extensions \
  --disable-plugins \
  --disable-images \
  --virtual-time-budget=1000 &

CHROME_PID=$!
echo "Chrome PID: $CHROME_PID"

# Chrome起動待機
sleep 3

# Chrome DevTools API確認
echo "📡 Testing Chrome DevTools API..."
curl -s http://localhost:9224/json/version | jq .
```

### 2. DevTools Protocol テストスクリプト作成
```bash
# Comprehensive Chrome DevTools Protocol test
cat > /tmp/test-chrome-devtools.cjs << 'EOF'
const http = require('http');
const WebSocket = require('ws');

class ChromeDevToolsTest {
  constructor() {
    this.testResults = {
      timestamp: new Date().toISOString(),
      phase: 'Chrome DevTools Protocol',
      tests: {}
    };
  }

  async runTests() {
    try {
      console.log('🚀 Starting Chrome DevTools Protocol test...');

      // Get available tabs
      const tabs = await this.getTabs();
      console.log('🔍 Available tabs:', tabs.length);

      if (tabs.length === 0) {
        throw new Error('No tabs available');
      }

      const tab = tabs[0];
      console.log('📱 Connecting to tab:', tab.id);

      // Connect to WebSocket
      const ws = new WebSocket(tab.webSocketDebuggerUrl);

      return new Promise((resolve, reject) => {
        let messageId = 1;
        const responses = {};

        ws.on('open', () => {
          console.log('✅ WebSocket connected to Chrome DevTools');

          // Enable required domains
          this.sendCommand(ws, messageId++, 'Page.enable', {});
          this.sendCommand(ws, messageId++, 'Runtime.enable', {});
          this.sendCommand(ws, messageId++, 'DOM.enable', {});

          // Navigate to our app
          console.log('🌐 Navigating to application...');
          this.sendCommand(ws, messageId++, 'Page.navigate', {
            url: 'http://127.0.0.1:8085'
          });

          // Wait for page load, then analyze DOM
          setTimeout(() => {
            console.log('🔍 Analyzing DOM structure...');
            this.sendCommand(ws, messageId++, 'Runtime.evaluate', {
              expression: `
                (function() {
                  // DOM Analysis Function
                  const analysis = {
                    timestamp: new Date().toISOString(),
                    url: window.location.href,
                    readyState: document.readyState,
                    elements: {}
                  };

                  // Action Buttons Row Analysis
                  const actionButtonsRows = document.querySelectorAll('.action-buttons-row');
                  analysis.elements.actionButtonsRow = {
                    found: actionButtonsRows.length > 0,
                    count: actionButtonsRows.length,
                    buttons: []
                  };

                  actionButtonsRows.forEach((row, rowIndex) => {
                    const buttons = row.querySelectorAll('button');
                    buttons.forEach((btn, btnIndex) => {
                      analysis.elements.actionButtonsRow.buttons.push({
                        rowIndex,
                        buttonIndex: btnIndex,
                        text: btn.textContent || btn.title || 'no-text',
                        classes: Array.from(btn.classList),
                        visible: btn.offsetParent !== null
                      });
                    });
                  });

                  // Form Elements Analysis
                  analysis.elements.formFields = {
                    title: {
                      found: !!document.getElementById('recipe-title'),
                      visible: document.getElementById('recipe-title')?.offsetParent !== null
                    },
                    ingredients: {
                      found: !!document.getElementById('recipe-ingredients'),
                      visible: document.getElementById('recipe-ingredients')?.offsetParent !== null
                    },
                    instructions: {
                      found: !!document.getElementById('recipe-instructions'),
                      visible: document.getElementById('recipe-instructions')?.offsetParent !== null
                    }
                  };

                  // Sort Tabs Analysis
                  const sortTabs = document.querySelectorAll('.sort-tab');
                  analysis.elements.sortTabs = {
                    found: sortTabs.length > 0,
                    count: sortTabs.length,
                    tabs: Array.from(sortTabs).map((tab, index) => ({
                      index,
                      text: tab.textContent,
                      active: tab.classList.contains('active'),
                      visible: tab.offsetParent !== null
                    }))
                  };

                  // Debug Buttons Analysis
                  const debugButtons = document.querySelectorAll('.debug-logs-button');
                  analysis.elements.debugButtons = {
                    found: debugButtons.length > 0,
                    count: debugButtons.length,
                    locations: Array.from(debugButtons).map((btn, index) => ({
                      index,
                      visible: btn.offsetParent !== null,
                      parentContainer: btn.closest('.action-buttons-row, .screen-header')?.className || 'unknown'
                    }))
                  };

                  // JavaScript Errors Check
                  const errors = [];
                  const originalError = window.console.error;
                  window.console.error = function(...args) {
                    errors.push(args.join(' '));
                    originalError.apply(console, args);
                  };
                  analysis.elements.jsErrors = errors;

                  // CSS Loading Check
                  analysis.elements.cssLoaded = {
                    stylesheets: document.styleSheets.length,
                    unifiedComponents: Array.from(document.styleSheets).some(sheet =>
                      sheet.href && sheet.href.includes('unified-ui-components.css')
                    )
                  };

                  return JSON.stringify(analysis, null, 2);
                })()
              `
            });

            this.testResults.tests.domAnalysisId = messageId - 1;
          }, 3000); // Wait 3 seconds for page load

          // Timeout for test completion
          setTimeout(() => {
            console.log('⏰ Test timeout reached');
            ws.close();
            resolve(this.testResults);
          }, 8000);
        });

        ws.on('message', (data) => {
          const response = JSON.parse(data);
          responses[response.id] = response;

          // Handle DOM analysis result
          if (response.id === this.testResults.tests.domAnalysisId && response.result) {
            try {
              const analysis = JSON.parse(response.result.result.value);
              console.log('🎯 DOM Analysis Results:');
              console.log(JSON.stringify(analysis, null, 2));

              this.testResults.tests.domAnalysis = analysis;
              this.testResults.tests.success = true;

              // Summary
              console.log('\n📊 Test Summary:');
              console.log(`Action Buttons Row: ${analysis.elements.actionButtonsRow.found ? '✅' : '❌'} (${analysis.elements.actionButtonsRow.count} found)`);
              console.log(`Form Fields: ${Object.values(analysis.elements.formFields).every(f => f.found) ? '✅' : '❌'}`);
              console.log(`Sort Tabs: ${analysis.elements.sortTabs.found ? '✅' : '❌'} (${analysis.elements.sortTabs.count} found)`);
              console.log(`Debug Buttons: ${analysis.elements.debugButtons.found ? '✅' : '❌'} (${analysis.elements.debugButtons.count} found)`);
              console.log(`CSS Loaded: ${analysis.elements.cssLoaded.unifiedComponents ? '✅' : '❌'}`);

              ws.close();
              resolve(this.testResults);
            } catch (error) {
              console.error('❌ Failed to parse DOM analysis:', error.message);
              this.testResults.tests.error = error.message;
              ws.close();
              resolve(this.testResults);
            }
          }
        });

        ws.on('error', (err) => {
          console.error('❌ WebSocket error:', err.message);
          this.testResults.tests.error = err.message;
          reject(err);
        });
      });

    } catch (error) {
      console.error('❌ Chrome DevTools Protocol test failed:', error.message);
      this.testResults.tests.error = error.message;
      return this.testResults;
    }
  }

  async getTabs() {
    return new Promise((resolve, reject) => {
      http.get('http://localhost:9224/json', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(e);
          }
        });
      }).on('error', reject);
    });
  }

  sendCommand(ws, id, method, params) {
    const command = { id, method, params };
    ws.send(JSON.stringify(command));
  }
}

// Run the test
const test = new ChromeDevToolsTest();
test.runTests().then(results => {
  console.log('\n✅ Chrome DevTools Protocol testing completed');
  process.exit(0);
}).catch(error => {
  console.error('❌ Test suite failed:', error.message);
  process.exit(1);
});
EOF
```

## 🧪 テスト実行

### 1. Chrome DevTools Protocol テスト実行
```bash
echo "🧪 Running Chrome DevTools Protocol Test..."

# テスト実行
node /tmp/test-chrome-devtools.cjs

# Chrome プロセス終了
echo "🔚 Cleaning up Chrome process..."
kill $CHROME_PID 2>/dev/null || echo "Chrome process already terminated"
```

### 2. ネットワーク分析テスト
```bash
# Network requests analysis
cat > /tmp/test-network.cjs << 'EOF'
const http = require('http');
const WebSocket = require('ws');

async function testNetworkRequests() {
  try {
    console.log('🌐 Starting network analysis test...');

    // Start Chrome with DevTools
    const { spawn } = require('child_process');
    const chrome = spawn('chromium-browser', [
      '--headless',
      '--remote-debugging-port=9225',
      '--no-sandbox',
      '--disable-gpu'
    ]);

    await new Promise(resolve => setTimeout(resolve, 2000));

    // Get tabs
    const tabs = await new Promise((resolve, reject) => {
      http.get('http://localhost:9225/json', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(JSON.parse(data)));
      }).on('error', reject);
    });

    if (tabs.length === 0) throw new Error('No tabs available');

    const ws = new WebSocket(tabs[0].webSocketDebuggerUrl);

    return new Promise((resolve) => {
      const networkRequests = [];

      ws.on('open', () => {
        console.log('📡 Connected to Chrome for network analysis');

        // Enable Network domain
        ws.send(JSON.stringify({ id: 1, method: 'Network.enable', params: {} }));
        ws.send(JSON.stringify({ id: 2, method: 'Page.enable', params: {} }));

        // Navigate to app
        ws.send(JSON.stringify({
          id: 3,
          method: 'Page.navigate',
          params: { url: 'http://127.0.0.1:8085' }
        }));

        setTimeout(() => {
          console.log('📊 Network Requests Summary:');
          console.log(`Total requests: ${networkRequests.length}`);

          const requestTypes = {};
          networkRequests.forEach(req => {
            const type = req.type || 'unknown';
            requestTypes[type] = (requestTypes[type] || 0) + 1;
          });

          console.log('Request types:', requestTypes);

          ws.close();
          chrome.kill();
          resolve(networkRequests);
        }, 5000);
      });

      ws.on('message', (data) => {
        const message = JSON.parse(data);
        if (message.method === 'Network.requestWillBeSent') {
          networkRequests.push({
            url: message.params.request.url,
            method: message.params.request.method,
            type: message.params.type
          });
          console.log(`📨 ${message.params.request.method} ${message.params.request.url}`);
        }
      });
    });

  } catch (error) {
    console.error('❌ Network analysis failed:', error.message);
  }
}

testNetworkRequests();
EOF

# Network test execution
node /tmp/test-network.cjs
```

## 📊 Phase 3 検証チェックリスト

### Chrome DevTools Protocol Tests
- [ ] Chrome起動成功 (PID確認)
- [ ] DevTools API応答 (http://localhost:9224/json)
- [ ] WebSocket接続成功
- [ ] Page.navigate 実行成功
- [ ] DOM analysis 実行成功
- [ ] Action Buttons Row検出
- [ ] Form Fields 検出
- [ ] Sort Tabs 検出
- [ ] Debug Buttons 検出
- [ ] CSS Loading 確認
- [ ] JavaScript エラーなし

### 期待される結果パターン
```json
{
  "elements": {
    "actionButtonsRow": {
      "found": true,
      "count": 2,
      "buttons": [...]
    },
    "formFields": {
      "title": { "found": true, "visible": true },
      "ingredients": { "found": true, "visible": true },
      "instructions": { "found": true, "visible": true }
    },
    "sortTabs": {
      "found": true,
      "count": 2
    },
    "debugButtons": {
      "found": true,
      "count": 4
    }
  }
}
```

### 3. テスト結果ログ保存
```bash
# テスト結果をログに追記
echo "Phase 3 Chrome DevTools Protocol Test Results - $(date)" >> ~/chrome-mcp-test-log.txt
node /tmp/test-chrome-devtools.cjs >> ~/chrome-mcp-test-log.txt 2>&1
echo "========================================" >> ~/chrome-mcp-test-log.txt
```

## 🛠️ トラブルシューティング

### よくある問題
1. **Chrome fails to start**: メモリ不足、権限問題
2. **DevTools port not available**: ポート競合、プロセス残留
3. **WebSocket connection failed**: Chrome起動待機時間不足
4. **DOM elements not found**: ページロード完了前のテスト実行
5. **Network service crashes**: Termux環境制約（非致命的）

### デバッグコマンド
```bash
# Chrome プロセス確認
ps aux | grep chromium

# DevTools ポート確認
netstat -tuln | grep :922

# Chrome DevTools API確認
curl -s http://localhost:9224/json | jq '.[] | {id, url, type}'

# WebSocket 手動接続テスト
node -e "
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:9224/devtools/page/TAB_ID');
ws.on('open', () => { console.log('Connected'); ws.close(); });
ws.on('error', (e) => console.error('Error:', e.message));
"
```

### Chrome 起動オプション調整
```bash
# より安定した Chrome 起動（メモリ制約環境）
chromium-browser \
  --headless \
  --remote-debugging-port=9224 \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --disable-extensions \
  --disable-plugins \
  --disable-images \
  --disable-javascript \
  --virtual-time-budget=2000 \
  --run-all-compositor-stages-before-draw \
  --disable-background-timer-throttling \
  --disable-backgrounding-occluded-windows \
  --disable-renderer-backgrounding &
```

---

**Phase 3 完了条件**: Chrome DevTools Protocol経由でのDOM要素検出成功
**所要時間**: 約5-10分
**次のステップ**: Phase 4 - Comprehensive Test Report
