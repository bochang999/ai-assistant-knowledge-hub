# Phase 2: Static DOM Analysis
**AI-Assistant Knowledge Hub - Chrome DevTools Testing Workflow**

## 🎯 目的
JSDOMを使用したサーバー側HTML解析とDOM構造検証

## 📋 前提条件
- Phase 1 完了済み
- HTTP Server 稼働中 (http://127.0.0.1:8085)
- jsdom パッケージ利用可能

## 🔍 HTML配信確認

### 1. サーバー応答分析
```bash
# HTML応答詳細分析スクリプト作成
cat > /tmp/analyze-html.js << 'EOF'
const http = require('http');

http.get('http://127.0.0.1:8085', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('📊 HTML Response Analysis:');
    console.log('Status:', res.statusCode);
    console.log('Content-Type:', res.headers['content-type']);
    console.log('Content-Length:', data.length);

    const checks = {
      'HTML Structure': /<html/i.test(data),
      'Action Buttons Row': /action-buttons-row/.test(data),
      'Core.js Script': /src="core\.js"/.test(data),
      'UI.js Script': /src="ui\.js"/.test(data),
      'CSS Files': /unified-ui-components\.css/.test(data),
      'Recipe Title Input': /id="recipe-title"/.test(data),
      'Debug Button': /debug-logs-button/.test(data),
      'Sort Tabs': /sort-tab/.test(data)
    };

    console.log('\n🔍 Content Checks:');
    Object.entries(checks).forEach(([key, value]) => {
      console.log(`  ${value ? '✅' : '❌'} ${key}`);
    });

    if (checks['Action Buttons Row']) {
      const matches = data.match(/action-buttons-row[^>]*>/g);
      console.log('\n📋 Action Buttons Row instances:', matches ? matches.length : 0);
    }
  });
}).on('error', (err) => {
  console.error('❌ Request failed:', err.message);
});
EOF

# スクリプト実行
node /tmp/analyze-html.js
```

## 🧪 JSDOM DOM構造テスト

### 1. JSDOM テストスクリプト作成
```bash
# JSDOM comprehensive test script
cat > /tmp/test-jsdom.cjs << 'EOF'
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const http = require('http');

async function testApplication() {
  try {
    console.log('🚀 Starting JSDOM test...');

    // Fetch HTML from server
    const response = await new Promise((resolve, reject) => {
      http.get('http://127.0.0.1:8085', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(data));
      }).on('error', reject);
    });

    console.log('📱 Creating DOM from HTML...');
    const dom = new JSDOM(response, {
      url: 'http://127.0.0.1:8085',
      pretendToBeVisual: true,
      resources: 'usable'
    });

    const { document } = dom.window;

    // Test Results Object
    const testResults = {
      timestamp: new Date().toISOString(),
      tests: {}
    };

    console.log('🔍 Testing button layout...');
    const actionButtonsRow = document.querySelector('.action-buttons-row');
    testResults.tests.actionButtonsRow = {
      found: !!actionButtonsRow,
      count: actionButtonsRow ? actionButtonsRow.querySelectorAll('button').length : 0
    };

    if (actionButtonsRow) {
      const buttons = actionButtonsRow.querySelectorAll('button');
      testResults.tests.buttons = [];

      buttons.forEach((btn, index) => {
        const classes = Array.from(btn.classList);
        const text = btn.textContent || btn.title || 'No text';
        testResults.tests.buttons.push({
          index: index + 1,
          text,
          classes,
          id: btn.id || null
        });
        console.log(`  Button ${index + 1}: ${text} - Classes: ${classes.join(', ')}`);
      });
    }

    console.log('📝 Testing form elements...');
    const formElements = {
      title: document.getElementById('recipe-title'),
      ingredients: document.getElementById('recipe-ingredients'),
      instructions: document.getElementById('recipe-instructions')
    };

    testResults.tests.formFields = {
      title: !!formElements.title,
      ingredients: !!formElements.ingredients,
      instructions: !!formElements.instructions
    };

    console.log('📝 Form elements found:');
    Object.entries(testResults.tests.formFields).forEach(([key, value]) => {
      console.log(`  - ${key}: ${value ? '✅' : '❌'}`);
    });

    console.log('🎨 Testing sort tabs...');
    const sortTabs = document.querySelectorAll('.sort-tab');
    testResults.tests.sortTabs = {
      count: sortTabs.length,
      tabs: []
    };

    sortTabs.forEach((tab, index) => {
      const isActive = tab.classList.contains('active');
      testResults.tests.sortTabs.tabs.push({
        index: index + 1,
        text: tab.textContent,
        active: isActive
      });
      console.log(`  Tab ${index + 1}: ${tab.textContent} - Active: ${isActive}`);
    });

    console.log('🍳 Testing debug buttons...');
    const debugButtons = document.querySelectorAll('.debug-logs-button');
    testResults.tests.debugButtons = {
      count: debugButtons.length,
      locations: []
    };

    debugButtons.forEach((btn, index) => {
      const parent = btn.closest('.action-buttons-row, .screen-header');
      testResults.tests.debugButtons.locations.push({
        index: index + 1,
        parentClass: parent ? Array.from(parent.classList).join(' ') : 'no-parent'
      });
    });

    console.log(`🍳 Debug buttons found: ${debugButtons.length}`);

    // Save test results
    console.log('\n📊 Test Results Summary:');
    console.log(JSON.stringify(testResults, null, 2));

    console.log('✅ JSDOM test completed successfully');
    return testResults;

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    return { error: error.message, timestamp: new Date().toISOString() };
  }
}

testApplication();
EOF

# JSDOM テスト実行
node /tmp/test-jsdom.cjs
```

### 2. CSS スタイル確認
```bash
# CSS files verification
echo "🎨 CSS Files Analysis:"

# unified-ui-components.css の重要セクション確認
curl -s http://127.0.0.1:8085/unified-ui-components.css | grep -A 5 -B 2 "action-buttons-row"

echo -e "\n📋 CSS Ingredients List Styling:"
curl -s http://127.0.0.1:8085/unified-ui-components.css | grep -A 3 "ingredients-list"

echo -e "\n🔍 CSS Variables:"
curl -s http://127.0.0.1:8085/unified-ui-components.css | grep -A 10 ":root"
```

## 📊 Phase 2 検証チェックリスト

### DOM Structure Tests
- [ ] HTML Response Status: 200 OK
- [ ] Content-Length: > 20,000 bytes
- [ ] Action Buttons Row: 2+ instances found
- [ ] Button Count: 4 buttons per row
- [ ] Form Fields: All 3 IDs present (recipe-title, recipe-ingredients, recipe-instructions)
- [ ] Sort Tabs: 2 tabs found (時系列, あいうえお順)
- [ ] Debug Buttons: 4+ instances across pages
- [ ] CSS Files: unified-ui-components.css loaded

### Expected Results Pattern
```json
{
  "actionButtonsRow": true,
  "buttonCount": 4,
  "formFields": {
    "title": true,
    "ingredients": true,
    "instructions": true
  },
  "sortTabs": 2,
  "debugButtons": 4
}
```

### 3. 結果ログ保存
```bash
# テスト結果をログファイルに保存
echo "Phase 2 JSDOM Test Results - $(date)" >> ~/chrome-mcp-test-log.txt
node /tmp/test-jsdom.cjs >> ~/chrome-mcp-test-log.txt 2>&1
echo "========================================" >> ~/chrome-mcp-test-log.txt
```

## 🛠️ トラブルシューティング

### よくある問題
1. **JSDOM parsing error**: HTML構文エラー、サーバー応答確認
2. **Elements not found**: クラス名・ID名の変更、HTMLテンプレート確認
3. **Button count mismatch**: JavaScript動的生成、ロードタイミング
4. **CSS not loading**: ファイルパス、HTTP配信確認

### デバッグコマンド
```bash
# サーバーログ確認
tail -f /tmp/http-server.log 2>/dev/null

# HTML構文チェック
curl -s http://127.0.0.1:8085 | head -50 | grep -E "(action-buttons-row|recipe-title)"

# DOM要素数カウント
node -e "
const jsdom = require('jsdom');
const http = require('http');
http.get('http://127.0.0.1:8085', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const dom = new (jsdom.JSDOM)(data);
    const doc = dom.window.document;
    console.log('Total buttons:', doc.querySelectorAll('button').length);
    console.log('Action rows:', doc.querySelectorAll('.action-buttons-row').length);
    console.log('Form inputs:', doc.querySelectorAll('input, textarea').length);
  });
});
"
```

---

**Phase 2 完了条件**: すべてのDOM要素が期待通りに検出されること
**所要時間**: 約3-5分
**次のステップ**: Phase 3 - Chrome DevTools Protocol Testing
