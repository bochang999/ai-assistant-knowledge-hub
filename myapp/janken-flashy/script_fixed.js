// 確実に動作する修正版
let debugLogs = [];

function log(msg) {
    console.log(msg);
    debugLogs.push(new Date().toLocaleTimeString() + ': ' + msg);
    
    let logArea = document.getElementById('log-area');
    if (!logArea) {
        // デバッグエリア作成
        logArea = document.createElement('div');
        logArea.id = 'log-area';
        logArea.style.cssText = 'position:fixed;bottom:0;left:0;right:0;height:150px;background:black;color:lime;font-size:11px;padding:8px;overflow-y:scroll;font-family:monospace;z-index:8000;border-top:2px solid lime;';
        document.body.appendChild(logArea);
        
        // コピーボタン作成
        const copyBtn = document.createElement('button');
        copyBtn.textContent = 'COPY';
        copyBtn.style.cssText = 'position:fixed;bottom:155px;right:5px;background:lime;color:black;border:none;padding:8px;font-weight:bold;cursor:pointer;z-index:8001;';
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(debugLogs.join('\n')).then(() => {
                copyBtn.textContent = 'OK!';
                setTimeout(() => copyBtn.textContent = 'COPY', 1000);
            });
        };
        document.body.appendChild(copyBtn);
    }
    
    logArea.innerHTML = debugLogs.join('<br>');
    logArea.scrollTop = logArea.scrollHeight;
}

log('Script starting');

class Game {
    constructor() {
        this.state = { round: 1, playerWins: 0, computerWins: 0, draws: 0, finished: false };
        this.choices = ['グー', 'チョキ', 'パー'];
        this.icons = { 'グー': '✊', 'チョキ': '✌️', 'パー': '✋' };
        this.init();
    }
    
    init() {
        log('Game init');
        document.querySelectorAll('.choice-button').forEach(btn => {
            btn.onclick = () => this.play(btn.dataset.choice);
        });
        this.updateDisplay();
    }
    
    play(playerChoice) {
        if (this.state.finished) return;
        log('Round ' + this.state.round + ': Player=' + playerChoice);
        
        const computerChoice = this.choices[Math.floor(Math.random() * 3)];
        log('Computer=' + computerChoice);
        
        document.getElementById('player-choice').textContent = this.icons[playerChoice];
        document.getElementById('computer-choice').textContent = this.icons[computerChoice];
        
        let result;
        if (playerChoice === computerChoice) {
            result = '引き分け';
            this.state.draws++;
        } else {
            const wins = { 'グー': 'チョキ', 'チョキ': 'パー', 'パー': 'グー' };
            if (wins[playerChoice] === computerChoice) {
                result = '勝ち';
                this.state.playerWins++;
            } else {
                result = '負け';
                this.state.computerWins++;
            }
        }
        
        log('Result: ' + result);
        document.getElementById('round-result').textContent = 'ラウンド' + this.state.round + ': ' + result;
        this.updateDisplay();
        
        if (this.state.round === 3) {
            log('GAME ENDING');
            setTimeout(() => this.endGame(), 2000);
        } else {
            this.state.round++;
            setTimeout(() => this.nextRound(), 3000);
        }
    }
    
    nextRound() {
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        this.updateDisplay();
    }
    
    endGame() {
        log('END GAME CALLED');
        this.state.finished = true;
        
        let winner;
        if (this.state.playerWins > this.state.computerWins) winner = '🎉 あなたの勝利！';
        else if (this.state.playerWins < this.state.computerWins) winner = '😢 コンピューターの勝利';
        else winner = '🤝 引き分け';
        
        // 確実に表示される大きなボタンを作成
        const bigButton = document.createElement('div');
        bigButton.innerHTML = winner + '<br><br>🔄 新しいゲーム';
        bigButton.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:red;color:white;font-size:20px;padding:30px;text-align:center;cursor:pointer;z-index:9999;border:5px solid yellow;border-radius:15px;';
        bigButton.onclick = () => {
            log('RESTART CLICKED');
            bigButton.remove();
            this.reset();
        };
        document.body.appendChild(bigButton);
        log('BIG RESTART BUTTON CREATED');
    }
    
    reset() {
        this.state = { round: 1, playerWins: 0, computerWins: 0, draws: 0, finished: false };
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        this.updateDisplay();
        log('Game reset complete');
    }
    
    updateDisplay() {
        document.getElementById('current-round').textContent = this.state.round;
        document.getElementById('player-score').textContent = this.state.playerWins;
        document.getElementById('computer-score').textContent = this.state.computerWins;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    log('DOM loaded, creating game');
    new Game();
});