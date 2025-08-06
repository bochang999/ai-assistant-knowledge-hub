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
            screenLog('New game button clicked');
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
        
        // Force show modal
        modal.style.display = 'flex';
        modal.style.opacity = '1';
        modal.style.visibility = 'visible';
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        modal.style.zIndex = '10000';
        
        screenLog('Modal forced to display');
        
        // Show new game button
        const newGameBtn = document.getElementById('new-game-btn');
        newGameBtn.style.display = 'block';\n        newGameBtn.style.position = 'fixed';\n        newGameBtn.style.bottom = '220px';\n        newGameBtn.style.left = '50%';\n        newGameBtn.style.transform = 'translateX(-50%)';\n        newGameBtn.style.zIndex = '10001';\n        newGameBtn.style.backgroundColor = '#4CAF50';\n        newGameBtn.style.color = 'white';\n        newGameBtn.style.padding = '15px 30px';\n        newGameBtn.style.border = 'none';\n        newGameBtn.style.borderRadius = '25px';\n        newGameBtn.style.fontSize = '16px';\n        newGameBtn.style.cursor = 'pointer';
        screenLog('New game button styled and positioned at bottom center');
        
        // Add click handler to modal for closing
        modal.onclick = (e) => {
            if (e.target === modal) {
                screenLog('Modal background clicked - closing');
                this.closeFinalResult();
            }
        };
        
        screenLog('Modal setup complete!');
    }
    
    closeFinalResult() {
        screenLog('Closing final result modal');
        const modal = document.getElementById('final-result');
        modal.style.display = 'none';
        modal.onclick = null; // Remove click handler
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
        
        // Hide modal and new game button
        const modal = document.getElementById('final-result');
        const newGameBtn = document.getElementById('new-game-btn');
        modal.style.display = 'none';
        newGameBtn.style.display = 'none';
        
        document.querySelectorAll('.choice-button').forEach(btn => btn.classList.remove('disabled'));
        
        this.updateDisplay();
        screenLog('Game reset complete');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    screenLog('DOM loaded, creating game');
    new JankenGame();
});