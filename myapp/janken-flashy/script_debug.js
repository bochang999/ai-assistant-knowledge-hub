// 超シンプルなデバッグ版
let logs = [];

function screenLog(message) {
    console.log(message);
    logs.push(message);
    
    let debugDiv = document.getElementById('debug-area');
    if (!debugDiv) {
        debugDiv = document.createElement('div');
        debugDiv.id = 'debug-area';
        debugDiv.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 200px;
            background: black;
            color: lime;
            font-size: 12px;
            padding: 10px;
            overflow-y: scroll;
            font-family: monospace;
            z-index: 5000;
            border-top: 2px solid lime;
        `;
        document.body.appendChild(debugDiv);
        
        // コピーボタンを追加
        const copyBtn = document.createElement('button');
        copyBtn.textContent = 'COPY ALL LOGS';
        copyBtn.style.cssText = `
            position: fixed;
            bottom: 210px;
            right: 10px;
            background: lime;
            color: black;
            border: none;
            padding: 10px;
            font-weight: bold;
            cursor: pointer;
            z-index: 5001;
        `;
        copyBtn.onclick = () => {
            const allLogs = logs.join('\n');
            navigator.clipboard.writeText(allLogs).then(() => {
                copyBtn.textContent = 'COPIED!';
                setTimeout(() => copyBtn.textContent = 'COPY ALL LOGS', 1000);
            });
        };
        document.body.appendChild(copyBtn);
    }
    
    debugDiv.innerHTML = logs.join('<br>');
    debugDiv.scrollTop = debugDiv.scrollHeight;
}

screenLog('Debug script loaded');

class JankenGame {
    constructor() {
        screenLog('JankenGame constructor');
        this.gameState = {
            round: 1,
            playerWins: 0,
            computerWins: 0,
            draws: 0,
            gameFinished: false
        };
        
        this.choices = ['グー', 'チョキ', 'パー'];
        this.choiceIcons = {
            'グー': '✊',
            'チョキ': '✌️',
            'パー': '✋'
        };
        
        this.init();
    }
    
    init() {
        screenLog('init called');
        this.bindEvents();
        this.updateDisplay();
    }
    
    bindEvents() {
        const choiceButtons = document.querySelectorAll('.choice-button');
        screenLog('Found buttons: ' + choiceButtons.length);
        
        choiceButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const choice = e.currentTarget.dataset.choice;
                screenLog('Button clicked: ' + choice);
                this.handlePlayerChoice(choice);
            });
        });
        
        const newGameBtn = document.getElementById('new-game-btn');
        if (newGameBtn) {
            newGameBtn.addEventListener('click', () => {
                screenLog('Original new game button clicked');
                this.resetGame();
            });
        }
    }
    
    handlePlayerChoice(playerChoice) {
        screenLog('=== ROUND ' + this.gameState.round + ' ===');
        screenLog('Player: ' + playerChoice);
        
        if (this.gameState.gameFinished) {
            screenLog('Game finished, ignoring');
            return;
        }
        
        const computerChoice = this.choices[Math.floor(Math.random() * this.choices.length)];
        screenLog('Computer: ' + computerChoice);
        
        // 表示更新
        document.getElementById('player-choice').textContent = this.choiceIcons[playerChoice];
        document.getElementById('computer-choice').textContent = this.choiceIcons[computerChoice];
        
        // ボタン無効化
        document.querySelectorAll('.choice-button').forEach(btn => btn.classList.add('disabled'));
        
        // 勝敗判定
        let result;
        if (playerChoice === computerChoice) {
            result = '引き分け';
            this.gameState.draws++;
        } else {
            const winPatterns = { 'グー': 'チョキ', 'チョキ': 'パー', 'パー': 'グー' };
            if (winPatterns[playerChoice] === computerChoice) {
                result = '勝ち';
                this.gameState.playerWins++;
            } else {
                result = '負け';
                this.gameState.computerWins++;
            }
        }
        
        screenLog('Result: ' + result);
        
        // 結果表示
        const resultEl = document.getElementById('round-result');
        resultEl.textContent = 'ラウンド' + this.gameState.round + ': ' + result + '！';
        resultEl.className = 'result-text show';
        if (result === '勝ち') resultEl.classList.add('win');
        else if (result === '負け') resultEl.classList.add('lose');
        else resultEl.classList.add('draw');
        
        // スコア更新
        document.getElementById('player-score').textContent = this.gameState.playerWins;
        document.getElementById('computer-score').textContent = this.gameState.computerWins;
        
        // ゲーム終了チェック
        if (this.gameState.round === 3) {
            screenLog('GAME ENDING - Round 3 completed');
            setTimeout(() => {
                this.endGame();
            }, 2000);
        } else {
            this.gameState.round++;
            setTimeout(() => {
                this.resetRound();
            }, 3000);
        }
    }
    
    resetRound() {
        screenLog('Reset round ' + this.gameState.round);
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        document.getElementById('round-result').className = 'result-text';
        document.getElementById('current-round').textContent = this.gameState.round;
        
        document.querySelectorAll('.choice-button').forEach(btn => btn.classList.remove('disabled'));
    }
    
    endGame() {
        screenLog('*** END GAME CALLED ***');
        this.gameState.gameFinished = true;
        
        const modal = document.getElementById('final-result');
        const title = document.getElementById('final-result-title');
        const details = document.getElementById('final-result-details');
        
        screenLog('Modal exists: ' + !!modal);
        screenLog('Title exists: ' + !!title);
        screenLog('Details exists: ' + !!details);
        
        let titleText;
        if (this.gameState.playerWins > this.gameState.computerWins) {
            titleText = '🎉 あなたの勝利！';
            title.style.color = '#4CAF50';
        } else if (this.gameState.playerWins < this.gameState.computerWins) {
            titleText = '😢 コンピューターの勝利';
            title.style.color = '#FF5722';
        } else {
            titleText = '🤝 引き分け';
            title.style.color = '#FF9800';
        }
        
        const detailsText = '最終結果<br>プレイヤー: ' + this.gameState.playerWins + '勝<br>コンピューター: ' + this.gameState.computerWins + '勝<br>引き分け: ' + this.gameState.draws + '回';
        
        title.textContent = titleText;
        details.innerHTML = detailsText;
        
        // モーダル表示
        modal.style.display = 'flex';
        screenLog('Modal display set to: ' + modal.style.display);
        
        // 超シンプルなボタン作成
        screenLog('Creating simple restart button...');
        setTimeout(() => {
            const bigBtn = document.createElement('div');
            bigBtn.innerHTML = '🔄 新しいゲーム';
            bigBtn.style.cssText = `
                position: fixed;
                top: 300px;
                left: 50%;
                transform: translateX(-50%);
                background: red;
                color: white;
                font-size: 24px;
                padding: 20px;
                cursor: pointer;
                z-index: 99999;
                border: 5px solid yellow;
            `;
            bigBtn.onclick = () => {
                screenLog('BIG BUTTON CLICKED!');
                bigBtn.remove();
                this.resetGame();
            };
            document.body.appendChild(bigBtn);
            screenLog('BIG RED BUTTON ADDED!');
        }, 1000);
    }
    
    updateDisplay() {
        document.getElementById('current-round').textContent = this.gameState.round;
        document.getElementById('player-score').textContent = this.gameState.playerWins;
        document.getElementById('computer-score').textContent = this.gameState.computerWins;
    }
    
    resetGame() {
        screenLog('RESET GAME CALLED');
        this.gameState = {
            round: 1,
            playerWins: 0,
            computerWins: 0,
            draws: 0,
            gameFinished: false
        };
        
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        document.getElementById('round-result').className = 'result-text';
        document.getElementById('final-result').style.display = 'none';
        
        document.querySelectorAll('.choice-button').forEach(btn => btn.classList.remove('disabled'));
        
        this.updateDisplay();
        screenLog('Game reset complete');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    screenLog('DOM loaded, starting game');
    new JankenGame();
});