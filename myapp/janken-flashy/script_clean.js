// Screen log function for mobile debugging - BOTTOM POSITION
function screenLog(message) {
    console.log(message);
    let debugDiv = document.getElementById('debug-log');
    if (!debugDiv) {
        debugDiv = document.createElement('div');
        debugDiv.id = 'debug-log';
        debugDiv.style.cssText = 'position: fixed; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.95); color: lime; font-size: 11px; padding: 8px; height: 30vh; overflow-y: scroll; font-family: monospace; z-index: 8888; border-top: 2px solid lime; user-select: text;';
        document.body.appendChild(debugDiv);
        
        // Add copy button at bottom right
        const copyBtn = document.createElement('button');
        copyBtn.textContent = '📋 COPY';
        copyBtn.style.cssText = 'position: fixed; bottom: 5px; right: 5px; background: lime; color: black; border: none; padding: 8px 12px; font-size: 11px; cursor: pointer; z-index: 8889; font-weight: bold; border-radius: 4px;';
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(debugDiv.textContent).then(() => {
                copyBtn.textContent = '✅ OK!';
                setTimeout(() => copyBtn.textContent = '📋 COPY', 1500);
            });
        };
        document.body.appendChild(copyBtn);
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
        
        // SIMPLE BUTTON CREATION - ABOVE DEBUG LOG
        setTimeout(() => {
            screenLog('Creating restart button...');
            
            // Remove any existing button first
            const existingBtn = document.getElementById('restart-btn-super');
            if (existingBtn) existingBtn.remove();
            
            const restartBtn = document.createElement('div');
            restartBtn.id = 'restart-btn-super';
            restartBtn.innerHTML = '🔄 新しいゲーム';
            restartBtn.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: #FF6B35;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 20px 30px;
                border-radius: 15px;
                cursor: pointer;
                z-index: 99999;
                box-shadow: 0 5px 20px rgba(255, 107, 53, 0.5);
                user-select: none;
                border: 3px solid white;
            `;
            
            restartBtn.onclick = () => {
                screenLog('RESTART BUTTON CLICKED!');
                restartBtn.remove();
                this.resetGame();
            };
            
            document.body.appendChild(restartBtn);
            screenLog('RESTART BUTTON ADDED TO SCREEN CENTER!');
        }, 500);
        
        // Add click handler to modal for closing
        modal.onclick = (e) => {
            if (e.target === modal) {
                screenLog('Modal background clicked - closing');
                this.closeFinalResult();
            }
        };
        
        screenLog('Modal setup complete! Look for green button at bottom center!');
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
        
        // Hide modal and all restart buttons
        const modal = document.getElementById('final-result');
        const newGameBtn = document.getElementById('new-game-btn');
        const customBtn = document.getElementById('new-game-btn-custom');
        const restartBtn = document.getElementById('restart-btn-super');
        
        modal.style.display = 'none';
        if (newGameBtn) newGameBtn.style.display = 'none';
        if (customBtn) customBtn.remove();
        if (restartBtn) restartBtn.remove();
        
        document.querySelectorAll('.choice-button').forEach(btn => btn.classList.remove('disabled'));
        
        this.updateDisplay();
        screenLog('Game reset complete');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    screenLog('DOM loaded, creating game');
    new JankenGame();
});