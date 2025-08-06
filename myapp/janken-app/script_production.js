// 本番用 - デバッグ機能なし
class Game {
    constructor() {
        this.state = { round: 1, playerWins: 0, computerWins: 0, draws: 0, finished: false };
        this.choices = ['グー', 'チョキ', 'パー'];
        this.icons = { 'グー': '✊', 'チョキ': '✌️', 'パー': '✋' };
        this.isProcessing = false;
        this.init();
    }
    
    init() {
        document.querySelectorAll('.choice-button').forEach(btn => {
            btn.onclick = () => {
                if (!this.isProcessing && !this.state.finished) {
                    this.play(btn.dataset.choice);
                }
            };
        });
        this.updateDisplay();
    }
    
    play(playerChoice) {
        if (this.isProcessing || this.state.finished) return;
        
        this.isProcessing = true;
        
        // ボタンを無効化
        document.querySelectorAll('.choice-button').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
        });
        
        const computerChoice = this.choices[Math.floor(Math.random() * 3)];
        
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
        
        document.getElementById('round-result').textContent = 'ラウンド' + this.state.round + ': ' + result;
        this.updateDisplay();
        
        if (this.state.round === 3) {
            setTimeout(() => {
                this.endGame();
            }, 3000);
        } else {
            this.state.round++;
            setTimeout(() => {
                this.nextRound();
            }, 3000);
        }
    }
    
    nextRound() {
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        this.updateDisplay();
        
        document.querySelectorAll('.choice-button').forEach(btn => {
            btn.disabled = false;
            btn.style.opacity = '1';
        });
        
        this.isProcessing = false;
    }
    
    endGame() {
        this.state.finished = true;
        this.isProcessing = false;
        
        let winner;
        if (this.state.playerWins > this.state.computerWins) winner = '🎉 あなたの勝利！';
        else if (this.state.playerWins < this.state.computerWins) winner = '😢 コンピューターの勝利';
        else winner = '🤝 引き分け';
        
        const resultText = winner + '<br><br>' + 
                          'プレイヤー: ' + this.state.playerWins + '勝<br>' +
                          'コンピューター: ' + this.state.computerWins + '勝<br>' +
                          '引き分け: ' + this.state.draws + '回<br><br>' +
                          '🔄 新しいゲーム';
        
        const existingBtn = document.getElementById('final-result-btn');
        if (existingBtn) existingBtn.remove();
        
        const bigButton = document.createElement('div');
        bigButton.id = 'final-result-btn';
        bigButton.innerHTML = resultText;
        bigButton.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:red;color:white;font-size:18px;padding:25px;text-align:center;cursor:pointer;z-index:9999;border:5px solid yellow;border-radius:15px;line-height:1.4;max-width:300px;';
        
        bigButton.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            bigButton.remove();
            this.reset();
        };
        
        document.body.appendChild(bigButton);
    }
    
    reset() {
        this.state = { round: 1, playerWins: 0, computerWins: 0, draws: 0, finished: false };
        this.isProcessing = false;
        
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        
        document.querySelectorAll('.choice-button').forEach(btn => {
            btn.disabled = false;
            btn.style.opacity = '1';
        });
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        document.getElementById('current-round').textContent = this.state.round;
        document.getElementById('player-score').textContent = this.state.playerWins;
        document.getElementById('computer-score').textContent = this.state.computerWins;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new Game();
});