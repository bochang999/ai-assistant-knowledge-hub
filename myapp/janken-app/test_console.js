// コンソールテスト用スクリプト
console.log('=== DOM要素テスト ===');

// 必要な要素がすべて存在するかチェック
const requiredElements = [
    'current-round', 'player-score', 'computer-score',
    'player-choice', 'computer-choice', 'round-result'
];

requiredElements.forEach(id => {
    const element = document.getElementById(id);
    console.log(id + ': ' + (element ? '✅ 存在' : '❌ 不在'));
});

// choice-buttonクラスの要素をチェック
const choiceButtons = document.querySelectorAll('.choice-button');
console.log('choice-button要素数: ' + choiceButtons.length);

choiceButtons.forEach((btn, index) => {
    console.log('Button ' + (index + 1) + ': ' + btn.dataset.choice);
});

// script_fixed.jsが読み込まれているかチェック
console.log('=== スクリプトテスト ===');
if (typeof Game !== 'undefined') {
    console.log('✅ Gameクラスが定義されている');
} else {
    console.log('❌ Gameクラスが定義されていない');
}

if (typeof log !== 'undefined') {
    console.log('✅ log関数が定義されている');
    log('テストログメッセージ');
} else {
    console.log('❌ log関数が定義されていない');
}

// デバッグエリアが作成されるかテスト
setTimeout(() => {
    const logArea = document.getElementById('log-area');
    const copyBtn = document.querySelector('button[style*="lime"]');
    
    console.log('log-area: ' + (logArea ? '✅ 作成された' : '❌ 作成されていない'));
    console.log('COPYボタン: ' + (copyBtn ? '✅ 作成された' : '❌ 作成されていない'));
}, 1000);