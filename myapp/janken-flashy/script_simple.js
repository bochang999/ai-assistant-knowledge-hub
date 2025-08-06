// Screen log function for mobile debugging
function screenLog(message) {
    console.log(message);
    let debugDiv = document.getElementById('debug-log');
    if (!debugDiv) {
        debugDiv = document.createElement('div');
        debugDiv.id = 'debug-log';
        debugDiv.style.cssText = 'position: fixed; bottom: 0; left: 0; right: 0; background: black; color: lime; font-size: 12px; padding: 10px; max-height: 200px; overflow-y: scroll; font-family: monospace; z-index: 9999;';
        document.body.appendChild(debugDiv);
    }
    debugDiv.innerHTML += message + '<br>';
    debugDiv.scrollTop = debugDiv.scrollHeight;
}

screenLog('Script loaded');

class JankenGame {
    constructor() {
        screenLog('JankenGame constructor called');
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
        screenLog('init() called');
        this.bindEvents();
        this.updateDisplay();
    }
    
    bindEvents() {
        const choiceButtons = document.querySelectorAll('.choice-button');
        screenLog('Found choice buttons: ' + choiceButtons.length);
        
        choiceButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const choice = e.currentTarget.dataset.choice;
                screenLog('Button clicked: ' + choice);
                this.handlePlayerChoice(choice);
            });
        });
        
        const newGameBtn = document.getElementById('new-game-btn');
        newGameBtn.addEventListener('click', () => {
            this.resetGame();
        });
    }
    
    handlePlayerChoice(playerChoice) {
        screenLog('=== ROUND ' + this.gameState.round + ' ===');
        screenLog('Player chose: ' + playerChoice);
        
        if (this.gameState.gameFinished) {
            screenLog('Game already finished, ignoring click');
            return;
        }
        
        // Computer choice
        const computerChoice = this.choices[Math.floor(Math.random() * this.choices.length)];
        screenLog('Computer chose: ' + computerChoice);
        
        // Update display immediately
        document.getElementById('player-choice').textContent = this.choiceIcons[playerChoice];
        document.getElementById('computer-choice').textContent = this.choiceIcons[computerChoice];
        
        // Disable buttons
        document.querySelectorAll('.choice-button').forEach(btn => btn.classList.add('disabled'));
        
        // Judge round
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
        
        screenLog('Round result: ' + result);
        screenLog('Current scores - Player: ' + this.gameState.playerWins + ' Computer: ' + this.gameState.computerWins);
        
        // Show result
        const resultEl = document.getElementById('round-result');
        resultEl.textContent = 'ラウンド' + this.gameState.round + ': ' + result + '！';
        resultEl.className = 'result-text show';
        if (result === '勝ち') resultEl.classList.add('win');
        else if (result === '負け') resultEl.classList.add('lose');
        else resultEl.classList.add('draw');
        
        // Update scores
        document.getElementById('player-score').textContent = this.gameState.playerWins;
        document.getElementById('computer-score').textContent = this.gameState.computerWins;
        
        // Check if game should end
        screenLog('Checking if game should end. Current round: ' + this.gameState.round);
        if (this.gameState.round === 3) {
            screenLog('GAME SHOULD END NOW!');
            setTimeout(() => {
                screenLog('Calling endGame() now...');
                this.endGame();
            }, 2000);
        } else {
            // Next round
            screenLog('Moving to next round...');
            this.gameState.round++;
            setTimeout(() => {
                this.resetRound();
            }, 3000);
        }
    }
    
    resetRound() {
        screenLog('resetRound() called for round ' + this.gameState.round);
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        document.getElementById('round-result').className = 'result-text';
        document.getElementById('current-round').textContent = this.gameState.round;
        
        // Enable buttons
        document.querySelectorAll('.choice-button').forEach(btn => btn.classList.remove('disabled'));
    }
    
    endGame() {
        screenLog('*** END GAME CALLED ***');
        this.gameState.gameFinished = true;
        
        // Show final result modal
        const modal = document.getElementById('final-result');
        const title = document.getElementById('final-result-title');
        const details = document.getElementById('final-result-details');
        
        screenLog('Modal found: ' + (modal ? 'YES' : 'NO'));
        screenLog('Title found: ' + (title ? 'YES' : 'NO'));
        screenLog('Details found: ' + (details ? 'YES' : 'NO'));
        
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
        modal.style.display = 'flex';\n        modal.style.opacity = '1';\n        modal.style.visibility = 'visible';
        
        screenLog('Modal display set to: ' + modal.style.display);
        screenLog('Modal should be visible now!');
        
        // Show new game button
        document.getElementById('new-game-btn').style.display = 'block';
        screenLog('New game button shown');
    }
    
    updateDisplay() {
        document.getElementById('current-round').textContent = this.gameState.round;
        document.getElementById('player-score').textContent = this.gameState.playerWins;
        document.getElementById('computer-score').textContent = this.gameState.computerWins;
    }
    
    resetGame() {
        screenLog('resetGame() called');
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
        document.getElementById('new-game-btn').style.display = 'none';
        
        document.querySelectorAll('.choice-button').forEach(btn => btn.classList.remove('disabled'));
        
        this.updateDisplay();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    screenLog('DOM loaded, creating game');
    new JankenGame();
});