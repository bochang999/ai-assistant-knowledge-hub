# じゃんけんアプリ仕様書

## システム仕様

### アーキテクチャ
```
├── index.html     # メインページ（UI構造）
├── style.css      # スタイルシート（デザイン）
├── script.js      # ゲームロジック（機能）
├── requirements.md # 要件定義
├── spec.md        # 仕様書（本ファイル）
├── tasks.md       # 開発タスクリスト
└── devlog.md      # 開発ログ
```

## UI仕様

### メイン画面レイアウト
```
┌─────────────────────────────────┐
│          じゃんけんゲーム            │
├─────────────────────────────────┤
│   ラウンド: 1/3                    │
│   プレイヤー: 0勝  コンピューター: 0勝  │
├─────────────────────────────────┤
│      [グー] [チョキ] [パー]          │
├─────────────────────────────────┤
│   プレイヤー: [選択表示]             │
│   コンピューター: [選択表示]          │
├─────────────────────────────────┤
│         [結果表示エリア]            │
├─────────────────────────────────┤
│         [新しいゲーム]              │
└─────────────────────────────────┘
```

### 画面要素詳細

#### ヘッダー部分
- タイトル: "じゃんけんゲーム"
- フォントサイズ: 24px
- 配置: 中央揃え

#### スコア表示部分
- 現在ラウンド: "ラウンド: X/3"
- プレイヤースコア: "プレイヤー: X勝"
- コンピュータースコア: "コンピューター: X勝"
- フォントサイズ: 18px

#### 選択ボタン部分
- ボタン数: 3個（グー、チョキ、パー）
- ボタンサイズ: 80px × 80px
- 配置: 横並び、等間隔
- ホバー効果: 背景色変更

#### 結果表示部分
- プレイヤー選択: アイコンまたはテキスト
- コンピューター選択: アイコンまたはテキスト
- 勝敗結果: "勝ち"/"負け"/"引き分け"
- フォントサイズ: 16px

#### コントロール部分
- 新しいゲームボタン: ゲーム終了後に表示
- リセット機能を提供

## 機能仕様

### ゲームフロー
```
1. ゲーム開始
   ↓
2. プレイヤーが選択（グー/チョキ/パー）
   ↓
3. コンピューターがランダム選択
   ↓
4. 勝敗判定
   ↓
5. スコア更新
   ↓
6. ラウンド数チェック
   ├─ < 3ラウンド → 次のラウンドへ（2に戻る）
   └─ = 3ラウンド → ゲーム終了、最終結果表示
   ↓
7. 新しいゲーム選択
```

### 勝敗判定ロジック
```javascript
const judgeResult = (player, computer) => {
  if (player === computer) return "引き分け";
  
  const winPatterns = {
    "グー": "チョキ",
    "チョキ": "パー", 
    "パー": "グー"
  };
  
  return winPatterns[player] === computer ? "勝ち" : "負け";
};
```

### データ構造
```javascript
const gameState = {
  round: 1,           // 現在のラウンド数（1-3）
  playerWins: 0,      // プレイヤーの勝利数
  computerWins: 0,    // コンピューターの勝利数
  draws: 0,           // 引き分け数
  gameFinished: false, // ゲーム終了フラグ
  currentPlayerChoice: null,    // 現在のプレイヤー選択
  currentComputerChoice: null   // 現在のコンピューター選択
};
```

## デザイン仕様

### カラーパレット
- **プライマリ**: #2196F3 (ブルー)
- **セカンダリ**: #4CAF50 (グリーン)
- **アクセント**: #FF9800 (オレンジ)
- **背景**: #F5F5F5 (ライトグレー)
- **テキスト**: #333333 (ダークグレー)

### タイポグラフィ
- **メインフォント**: 'Arial', 'Helvetica', sans-serif
- **タイトル**: 24px, bold
- **スコア**: 18px, normal
- **ボタン**: 16px, bold
- **結果**: 16px, normal

### レスポンシブデザイン
```css
/* デスクトップ */
@media (min-width: 768px) {
  .container { max-width: 600px; }
  .choice-button { font-size: 18px; }
}

/* モバイル */
@media (max-width: 767px) {
  .container { max-width: 100%; padding: 10px; }
  .choice-button { font-size: 14px; }
}
```

## API仕様

### 関数一覧
```javascript
// ゲーム初期化
function initGame()

// プレイヤーの選択処理
function playerChoice(choice)

// コンピューターの選択生成
function getComputerChoice()

// 勝敗判定
function judgeRound(playerChoice, computerChoice)

// スコア更新
function updateScore(result)

// UI更新
function updateDisplay()

// ゲームリセット
function resetGame()

// ゲーム終了チェック
function checkGameEnd()
```

### イベントハンドリング
```javascript
// 選択ボタンクリック
document.querySelectorAll('.choice-button').forEach(button => {
  button.addEventListener('click', handleChoiceClick);
});

// 新しいゲームボタンクリック
document.getElementById('new-game').addEventListener('click', resetGame);
```

## 動作環境

### 対応ブラウザ
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### 画面解像度
- 最小: 320px × 568px (iPhone SE)
- 推奨: 375px × 667px (iPhone 8)
- 最大: 1920px × 1080px (デスクトップ)

### パフォーマンス目標
- 初回読み込み: 2秒以内
- ボタンレスポンス: 100ms以内

---

## 📋 最終実装仕様（2025-07-25完成版）

### 🎯 実装完了機能
1. **3回勝負システム**: 完全動作、ラウンド管理
2. **スコア表示**: リアルタイム更新、最終結果表示
3. **操作制御**: 連続クリック防止、適切な待機時間
4. **新ゲーム機能**: 確実なリセット、状態初期化
5. **UI/UX**: Atlassian Design適用、レスポンシブ対応

### 🔧 技術実装詳細

#### JavaScript構成
- **本番版**: `script_production.js` (108行)
  - デバッグ機能なし、軽量化
  - 純粋なゲーム機能のみ
- **デバッグ版**: `script_final_fixed.js` (152行)
  - フルデバッグログ機能
  - ワンクリックログコピー

#### 操作制御機構
```javascript
// 連続クリック防止
this.isProcessing = false;
btn.disabled = true;
btn.style.opacity = '0.5';

// 待機時間制御
setTimeout(() => this.nextRound(), 3000);
setTimeout(() => this.endGame(), 3000);
```

#### 状態管理
```javascript
this.state = {
    round: 1,           // 現在ラウンド
    playerWins: 0,      // プレイヤー勝利数
    computerWins: 0,    // コンピューター勝利数
    draws: 0,           // 引き分け数
    finished: false     // ゲーム終了フラグ
};
```

### 📱 モバイル最適化
- **タッチ操作**: 最適化済み
- **画面サイズ**: 320px～対応
- **レスポンシブ**: Flexbox/Grid活用
- **アクセシビリティ**: ARIA属性完全対応

### 🛠️ デバッグシステム
- **段階切り替え**: HTMLファイル1行変更で切り替え可能
- **ログ機能**: リアルタイム表示、ワンクリックコピー
- **問題解決**: モバイル環境での効率的デバッグを実現

### ✅ 品質保証達成
- **機能性**: 全要件100%実装
- **安定性**: エラー耐性、状態整合性確保
- **使いやすさ**: 直感的操作、適切フィードバック
- **保守性**: クリーンなコード構造、ドキュメント完備

### 🎨 アニメーション実装履歴
- **参考**: React Spring (https://www.react-spring.dev/examples)
- **試行**: Spring物理・Easing概念を検討
- **調整**: ユーザーフィードバックに基づく段階的調整
- **結論**: 機能性重視でシンプル化、将来的に用途別強化可能

### 🚀 成果物一覧
- **index.html**: メインページ（87行）
- **style.css**: スタイルシート（384行、Atlassian Design適用）
- **script_production.js**: 本番用JavaScript（108行）
- **script_final_fixed.js**: デバッグ用JavaScript（152行）
- **requirements.md**: 要件定義書
- **spec.md**: 技術仕様書（本書）
- **tasks.md**: タスク管理・進捗記録
- **devlog.md**: 開発ログ・技術記録

### 🔮 将来的拡張可能性
- **アニメーション強化**: 用途に応じてReact Spring風の派手なアニメーション実装
- **サウンド追加**: 効果音・BGM統合
- **テーマ切替**: ダーク/ライトモード、季節テーマなど
- アニメーション: 60fps維持