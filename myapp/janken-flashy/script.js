class JankenGame {
    constructor() {
        this.gameState = {
            round: 1,
            playerWins: 0,
            computerWins: 0,
            draws: 0,
            gameFinished: false,
            currentPlayerChoice: null,
            currentComputerChoice: null
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
        this.bindEvents();
        this.updateDisplay();
    }
    
    bindEvents() {
        const choiceButtons = document.querySelectorAll('.choice-button');
        choiceButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const choice = e.currentTarget.dataset.choice;
                this.handlePlayerChoice(choice);
            });
        });
        
        const newGameBtn = document.getElementById('new-game-btn');
        newGameBtn.addEventListener('click', () => {
            this.resetGame();
        });
        
        const finalResult = document.getElementById('final-result');
        finalResult.addEventListener('click', (e) => {
            if (e.target === finalResult) {
                this.closeFinalResult();
            }
        });
    }
    
    handlePlayerChoice(playerChoice) {
        if (this.gameState.gameFinished) return;
        
        this.gameState.currentPlayerChoice = playerChoice;
        this.gameState.currentComputerChoice = this.getComputerChoice();
        
        this.disableChoiceButtons();
        this.updateChoiceDisplay();
        
        setTimeout(() => {
            this.judgeRound();
            this.updateScore();
            this.updateDisplay();
            
            if (this.gameState.round >= 3) {
                setTimeout(() => {
                    this.endGame();
                }, 1000);
            } else {
                this.gameState.round++;
                setTimeout(() => {
                    this.resetRound();
                }, 2000);
            }
        }, 1000);
    }
    
    getComputerChoice() {
        const randomIndex = Math.floor(Math.random() * this.choices.length);
        return this.choices[randomIndex];
    }
    
    judgeRound() {
        const player = this.gameState.currentPlayerChoice;
        const computer = this.gameState.currentComputerChoice;
        
        if (player === computer) {
            this.gameState.roundResult = '引き分け';
            this.gameState.draws++;
        } else {
            const winPatterns = {
                'グー': 'チョキ',
                'チョキ': 'パー',
                'パー': 'グー'
            };
            
            if (winPatterns[player] === computer) {
                this.gameState.roundResult = '勝ち';
                this.gameState.playerWins++;
            } else {
                this.gameState.roundResult = '負け';
                this.gameState.computerWins++;
            }
        }
    }
    
    updateScore() {
        document.getElementById('player-score').textContent = this.gameState.playerWins;
        document.getElementById('computer-score').textContent = this.gameState.computerWins;
    }
    
    updateDisplay() {
        document.getElementById('current-round').textContent = this.gameState.round;
        this.updateScore();
        
        if (this.gameState.roundResult) {
            this.updateResultDisplay();
        }
    }
    
    updateChoiceDisplay() {
        const playerChoiceEl = document.getElementById('player-choice');
        const computerChoiceEl = document.getElementById('computer-choice');
        
        playerChoiceEl.textContent = this.choiceIcons[this.gameState.currentPlayerChoice];
        computerChoiceEl.textContent = this.choiceIcons[this.gameState.currentComputerChoice];
    }
    
    updateResultDisplay() {
        const resultEl = document.getElementById('round-result');
        const result = this.gameState.roundResult;
        
        resultEl.textContent = `ラウンド${this.gameState.round}: ${result}！`;
        resultEl.className = 'result-text';
        
        if (result === '勝ち') {
            resultEl.classList.add('win');
        } else if (result === '負け') {
            resultEl.classList.add('lose');
        } else {
            resultEl.classList.add('draw');
        }
    }
    
    disableChoiceButtons() {
        const choiceButtons = document.querySelectorAll('.choice-button');
        choiceButtons.forEach(button => {
            button.classList.add('disabled');
        });
    }
    
    enableChoiceButtons() {
        const choiceButtons = document.querySelectorAll('.choice-button');
        choiceButtons.forEach(button => {
            button.classList.remove('disabled');
        });
    }
    
    resetRound() {
        this.gameState.currentPlayerChoice = null;
        this.gameState.currentComputerChoice = null;
        this.gameState.roundResult = null;
        
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        document.getElementById('round-result').className = 'result-text';
        
        this.enableChoiceButtons();
        this.updateDisplay();
    }
    
    endGame() {
        this.gameState.gameFinished = true;
        this.showFinalResult();
        document.getElementById('new-game-btn').style.display = 'block';
    }
    
    showFinalResult() {
        const finalResultEl = document.getElementById('final-result');
        const titleEl = document.getElementById('final-result-title');
        const detailsEl = document.getElementById('final-result-details');
        
        let title, details;
        
        if (this.gameState.playerWins > this.gameState.computerWins) {
            title = '🎉 あなたの勝利！';
            titleEl.style.color = '#4CAF50';
        } else if (this.gameState.playerWins < this.gameState.computerWins) {
            title = '😢 コンピューターの勝利';
            titleEl.style.color = '#FF5722';
        } else {
            title = '🤝 引き分け';
            titleEl.style.color = '#FF9800';
        }
        
        details = `
            最終結果<br>
            プレイヤー: ${this.gameState.playerWins}勝<br>
            コンピューター: ${this.gameState.computerWins}勝<br>
            引き分け: ${this.gameState.draws}回
        `;
        
        titleEl.textContent = title;
        detailsEl.innerHTML = details;
        finalResultEl.style.display = 'flex';
    }
    
    closeFinalResult() {
        document.getElementById('final-result').style.display = 'none';
    }
    
    resetGame() {
        this.gameState = {
            round: 1,
            playerWins: 0,
            computerWins: 0,
            draws: 0,
            gameFinished: false,
            currentPlayerChoice: null,
            currentComputerChoice: null,
            roundResult: null
        };
        
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        document.getElementById('round-result').className = 'result-text';
        document.getElementById('new-game-btn').style.display = 'none';
        document.getElementById('final-result').style.display = 'none';
        
        this.enableChoiceButtons();
        this.updateDisplay();
    }
}

    // Animation helper methods
    animateWinner() {
        const playerChoiceEl = document.getElementById('player-choice');
        const computerChoiceEl = document.getElementById('computer-choice');
        
        if (this.gameState.roundResult === '勝ち') {
            playerChoiceEl.classList.add('animate-winner');
            computerChoiceEl.classList.add('animate-loser');
        } else if (this.gameState.roundResult === '負け') {
            computerChoiceEl.classList.add('animate-winner');
            playerChoiceEl.classList.add('animate-loser');
        }
    }
    
    animateLoser() {
        const playerChoiceEl = document.getElementById('player-choice');
        const computerChoiceEl = document.getElementById('computer-choice');
        
        if (this.gameState.roundResult === '負け') {
            playerChoiceEl.classList.add('animate-loser');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new JankenGame();
});