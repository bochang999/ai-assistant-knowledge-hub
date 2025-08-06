// 🎆 FLASHY JANKEN - 派手なアニメーション版
class FlashyJankenGame {
    constructor() {
        this.state = { round: 1, playerWins: 0, computerWins: 0, draws: 0, finished: false };
        this.choices = ['グー', 'チョキ', 'パー'];
        this.icons = { 'グー': '✊', 'チョキ': '✌️', 'パー': '✋' };
        this.isProcessing = false;
        this.init();
        this.createParticleSystem();
        
        // 🔥 MEGA BATTLE SYSTEM初期化
        console.log('Initializing MEGA BATTLE SYSTEM...');
        this.battleSystem = new MegaBattleSystem(this);
        console.log('MEGA BATTLE SYSTEM ready!');
    }
    
    init() {
        this.bindEvents();
        this.updateDisplay();
        this.startBackgroundEffects();
    }
    
    bindEvents() {
        document.querySelectorAll('.choice-button').forEach(btn => {
            btn.onclick = () => {
                if (!this.isProcessing && !this.state.finished) {
                    this.playWithAnimation(btn.dataset.choice, btn);
                }
            };
            
            // ホバーエフェクト強化
            btn.addEventListener('mouseenter', () => {
                this.createHoverParticles(btn);
            });
        });
    }
    
    createParticleSystem() {
        // パーティクルシステム初期化
        this.particles = [];
        this.particleCanvas = document.createElement('canvas');
        this.particleCanvas.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;';
        document.body.appendChild(this.particleCanvas);
        this.ctx = this.particleCanvas.getContext('2d');
        this.resizeCanvas();
        
        window.addEventListener('resize', () => this.resizeCanvas());
        this.animateParticles();
    }
    
    resizeCanvas() {
        this.particleCanvas.width = window.innerWidth;
        this.particleCanvas.height = window.innerHeight;
    }
    
    createHoverParticles(button) {
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        for (let i = 0; i < 8; i++) {
            this.particles.push({
                x: centerX,
                y: centerY,
                vx: (Math.random() - 0.5) * 4,
                vy: (Math.random() - 0.5) * 4,
                life: 60,
                maxLife: 60,
                color: `hsl(${Math.random() * 360}, 70%, 60%)`,
                size: Math.random() * 4 + 2
            });
        }
    }
    
    createVictoryExplosion(x, y) {
        for (let i = 0; i < 30; i++) {
            this.particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                life: 120,
                maxLife: 120,
                color: `hsl(${Math.random() * 60 + 300}, 80%, 70%)`, // ピンク〜紫
                size: Math.random() * 6 + 3
            });
        }
    }
    
    animateParticles() {
        this.ctx.clearRect(0, 0, this.particleCanvas.width, this.particleCanvas.height);
        
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.1; // 重力
            p.life--;
            
            const alpha = p.life / p.maxLife;
            this.ctx.globalAlpha = alpha;
            this.ctx.fillStyle = p.color;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fill();
            
            if (p.life <= 0) {
                this.particles.splice(i, 1);
            }
        }
        
        requestAnimationFrame(() => this.animateParticles());
    }
    
    startBackgroundEffects() {
        // 定期的な背景エフェクト
        setInterval(() => {
            if (!this.isProcessing) {
                this.createRandomSparkle();
            }
        }, 2000);
    }
    
    createRandomSparkle() {
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;
        
        for (let i = 0; i < 5; i++) {
            this.particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                life: 80,
                maxLife: 80,
                color: '#ffffff',
                size: Math.random() * 3 + 1
            });
        }
    }
    
    async playWithAnimation(playerChoice, button) {
        if (this.isProcessing || this.state.finished) return;
        
        this.isProcessing = true;
        
        // ボタンクリックエフェクト
        this.createButtonExplosion(button);
        
        // 全ボタン無効化 + エフェクト
        document.querySelectorAll('.choice-button').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
            btn.style.transform = 'scale(0.9)';
        });
        
        // 🔥 MEGA BATTLE開始
        await this.animateChoice(playerChoice);
    }
    
    createButtonExplosion(button) {
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        // 爆発エフェクト
        for (let i = 0; i < 20; i++) {
            this.particles.push({
                x: centerX,
                y: centerY,
                vx: (Math.random() - 0.5) * 8,
                vy: (Math.random() - 0.5) * 8,
                life: 80,
                maxLife: 80,
                color: `hsl(${Math.random() * 60 + 40}, 90%, 60%)`, // 暖色系
                size: Math.random() * 5 + 2
            });
        }
        
        // 画面振動エフェクト
        document.body.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 500);
        
        // CSS振動アニメーション追加
        if (!document.getElementById('shake-animation')) {
            const style = document.createElement('style');
            style.id = 'shake-animation';
            style.textContent = `
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-2px); }
                    75% { transform: translateX(2px); }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    async animateChoice(playerChoice) {
        console.log('🎮 animateChoice called with:', playerChoice);
        console.log('🔍 Battle system exists?', !!this.battleSystem);
        console.log('🔍 Battle system type:', typeof this.battleSystem);
        
        const computerChoice = this.choices[Math.floor(Math.random() * 3)];
        console.log('🤖 Computer chose:', computerChoice);
        
        if (!this.battleSystem) {
            console.error('❌ Battle system not found! Falling back to simple animation.');
            this.showChoicesDramatically(playerChoice, computerChoice);
            setTimeout(() => {
                const result = this.calculateSimpleResult(playerChoice, computerChoice);
                this.applyBattleResult(result);
            }, 2000);
            return;
        }
        
        try {
            // 🔥 MEGA BATTLE SYSTEMを使用
            console.log('🔥 Starting MEGA BATTLE...');
            const battleResult = await this.battleSystem.startMegaBattle(playerChoice, computerChoice);
            console.log('🔥 Battle result:', battleResult);
            
            // 結果をゲーム状態に反映
            this.applyBattleResult(battleResult.result);
        } catch (error) {
            console.error('❌ Battle system error:', error);
            // フォールバック
            this.showChoicesDramatically(playerChoice, computerChoice);
            setTimeout(() => {
                const result = this.calculateSimpleResult(playerChoice, computerChoice);
                this.applyBattleResult(result);
            }, 2000);
        }
    }
    
    calculateSimpleResult(playerChoice, computerChoice) {
        if (playerChoice === computerChoice) return '引き分け';
        const wins = { 'グー': 'チョキ', 'チョキ': 'パー', 'パー': 'グー' };
        return wins[playerChoice] === computerChoice ? '勝ち' : '負け';
    }
    
    applyBattleResult(result) {
        // 結果に基づいてスコア更新
        if (result === '勝ち') {
            this.state.playerWins++;
        } else if (result === '負け') {
            this.state.computerWins++;
        } else {
            this.state.draws++;
        }
        
        // スコア表示更新
        this.updateDisplay();
        
        // ラウンド結果表示
        const resultEl = document.getElementById('round-result');
        resultEl.textContent = 'ラウンド' + this.state.round + ': ' + result + '！';
        resultEl.className = 'result-text show';
        if (result === '勝ち') resultEl.classList.add('win');
        else if (result === '負け') resultEl.classList.add('lose');
        else resultEl.classList.add('draw');
        
        // ゲーム進行制御
        if (this.state.round === 3) {
            setTimeout(() => {
                this.endGameSpectacularly();
            }, 3000);
        } else {
            this.state.round++;
            setTimeout(() => {
                this.nextRoundWithTransition();
            }, 3000);
        }
    }
    
    showChoicesDramatically(playerChoice, computerChoice) {
        const playerEl = document.getElementById('player-choice');
        const computerEl = document.getElementById('computer-choice');
        
        // 初期状態
        playerEl.textContent = '?';
        computerEl.textContent = '?';
        
        // カウントダウンエフェクト
        let countdown = 3;
        const countdownInterval = setInterval(() => {
            playerEl.textContent = countdown;
            computerEl.textContent = countdown;
            
            // 数字にカラフルエフェクト
            playerEl.style.color = `hsl(${Math.random() * 360}, 70%, 60%)`;
            computerEl.style.color = `hsl(${Math.random() * 360}, 70%, 60%)`;
            
            countdown--;
            
            if (countdown < 0) {
                clearInterval(countdownInterval);
                
                // 最終選択を派手に表示
                playerEl.textContent = this.icons[playerChoice];
                computerEl.textContent = this.icons[computerChoice];
                
                playerEl.style.color = '';
                computerEl.style.color = '';
                
                // 選択表示時のエフェクト
                playerEl.style.animation = 'resultMegaPulse 1s ease-out';
                computerEl.style.animation = 'resultMegaPulse 1s ease-out';
                
                // CSS追加
                if (!document.getElementById('mega-pulse-animation')) {
                    const style = document.createElement('style');
                    style.id = 'mega-pulse-animation';
                    style.textContent = `
                        @keyframes resultMegaPulse {
                            0% { transform: scale(0.3) rotate(0deg); opacity: 0; }
                            50% { transform: scale(1.3) rotate(180deg); opacity: 1; }
                            100% { transform: scale(1) rotate(360deg); opacity: 1; }
                        }
                    `;
                    document.head.appendChild(style);
                }
            }
        }, 600);
    }
    
    processResult(playerChoice, computerChoice) {
        let result;
        if (playerChoice === computerChoice) {
            result = '引き分け';
            this.state.draws++;
        } else {
            const wins = { 'グー': 'チョキ', 'チョキ': 'パー', 'パー': 'グー' };
            if (wins[playerChoice] === computerChoice) {
                result = '勝ち';
                this.state.playerWins++;
                this.celebrateWin();
            } else {
                result = '負け';
                this.state.computerWins++;
            }
        }
        
        this.showResultWithEffect(result);
        this.updateDisplay();
        
        if (this.state.round === 3) {
            setTimeout(() => {
                this.endGameSpectacularly();
            }, 3000);
        } else {
            this.state.round++;
            setTimeout(() => {
                this.nextRoundWithTransition();
            }, 3000);
        }
    }
    
    celebrateWin() {
        // 勝利時の特別エフェクト
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        this.createVictoryExplosion(centerX, centerY);
        
        // 勝利サウンドエフェクト（視覚的表現）
        document.body.style.background = 'linear-gradient(45deg, #56ab2f, #a8e6cf)';
        setTimeout(() => {
            document.body.style.background = '';
        }, 1000);
    }
    
    showResultWithEffect(result) {
        const resultEl = document.getElementById('round-result');
        resultEl.textContent = 'ラウンド' + this.state.round + ': ' + result + '！';
        resultEl.className = 'result-text show';
        
        if (result === '勝ち') {
            resultEl.classList.add('win');
            // 追加勝利エフェクト
            resultEl.style.animation = 'winMegaCelebration 2s ease-out';
        } else if (result === '負け') {
            resultEl.classList.add('lose');
        } else {
            resultEl.classList.add('draw');
        }
        
        // CSS追加
        if (!document.getElementById('win-mega-animation')) {
            const style = document.createElement('style');
            style.id = 'win-mega-animation';
            style.textContent = `
                @keyframes winMegaCelebration {
                    0% { transform: scale(0.5) rotate(-15deg); }
                    25% { transform: scale(1.3) rotate(5deg); }
                    50% { transform: scale(0.9) rotate(-5deg); }
                    75% { transform: scale(1.1) rotate(2deg); }
                    100% { transform: scale(1) rotate(0deg); }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    nextRoundWithTransition() {
        // 次ラウンドへの派手なトランジション
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        document.getElementById('round-result').className = 'result-text';
        
        this.updateDisplay();
        
        // ボタン再有効化 + エフェクト
        document.querySelectorAll('.choice-button').forEach((btn, index) => {
            setTimeout(() => {
                btn.disabled = false;
                btn.style.opacity = '1';
                btn.style.transform = 'scale(1)';
                btn.style.animation = 'buttonRevive 0.5s ease-out';
            }, index * 100);
        });
        
        // CSS追加
        if (!document.getElementById('button-revive-animation')) {
            const style = document.createElement('style');
            style.id = 'button-revive-animation';
            style.textContent = `
                @keyframes buttonRevive {
                    0% { transform: scale(0.8) rotate(-10deg); opacity: 0.5; }
                    50% { transform: scale(1.1) rotate(5deg); opacity: 0.8; }
                    100% { transform: scale(1) rotate(0deg); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
        
        this.isProcessing = false;
    }
    
    endGameSpectacularly() {
        this.state.finished = true;
        this.isProcessing = false;
        
        // 超派手な最終結果表示
        let winner;
        if (this.state.playerWins > this.state.computerWins) {
            winner = '🎉🎊 あなたの大勝利！ 🎊🎉';
            this.createMegaVictoryEffect();
        } else if (this.state.playerWins < this.state.computerWins) {
            winner = '😢 コンピューターの勝利 😢';
        } else {
            winner = '🤝 引き分け 🤝';
        }
        
        const resultText = winner + '<br><br>' + 
                          '🏆 最終結果 🏆<br>' +
                          'プレイヤー: ' + this.state.playerWins + '勝<br>' +
                          'コンピューター: ' + this.state.computerWins + '勝<br>' +
                          '引き分け: ' + this.state.draws + '回<br><br>' +
                          '✨🎮 もう一度遊ぶ 🎮✨';
        
        const existingBtn = document.getElementById('final-result-btn');
        if (existingBtn) existingBtn.remove();
        
        const megaButton = document.createElement('div');
        megaButton.id = 'final-result-btn';
        megaButton.innerHTML = resultText;
        megaButton.style.cssText = `
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57) !important;
            background-size: 400% 400% !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold !important;
            padding: 25px !important;
            text-align: center !important;
            cursor: pointer !important;
            z-index: 9999 !important;
            border-radius: 25px !important;
            border: 5px solid rgba(255, 255, 255, 0.8) !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4) !important;
            max-width: 350px !important;
            line-height: 1.4 !important;
            animation: finalMegaAnimation 3s ease-in-out infinite !important;
        `;
        
        // 巨大ボタンCSS
        if (!document.getElementById('final-mega-animation')) {
            const style = document.createElement('style');
            style.id = 'final-mega-animation';
            style.textContent = `
                @keyframes finalMegaAnimation {
                    0% { 
                        transform: translate(-50%, -50%) scale(1) rotate(0deg);
                        background-position: 0% 50%;
                        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
                    }
                    33% { 
                        transform: translate(-50%, -50%) scale(1.05) rotate(1deg);
                        background-position: 100% 50%;
                    }
                    66% { 
                        transform: translate(-50%, -50%) scale(0.98) rotate(-1deg);
                        background-position: 0% 50%;
                    }
                    100% { 
                        transform: translate(-50%, -50%) scale(1) rotate(0deg);
                        background-position: 100% 50%;
                        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        megaButton.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.createButtonExplosion(megaButton);
            setTimeout(() => {
                megaButton.remove();
                this.reset();
            }, 500);
        };
        
        document.body.appendChild(megaButton);
    }
    
    createMegaVictoryEffect() {
        // 画面全体に勝利エフェクト
        for (let i = 0; i < 100; i++) {
            setTimeout(() => {
                this.particles.push({
                    x: Math.random() * window.innerWidth,
                    y: window.innerHeight + 50,
                    vx: (Math.random() - 0.5) * 4,
                    vy: -Math.random() * 15 - 5,
                    life: 200,
                    maxLife: 200,
                    color: `hsl(${Math.random() * 60 + 300}, 80%, 70%)`,
                    size: Math.random() * 8 + 3
                });
            }, i * 50);
        }
    }
    
    updateDisplay() {
        document.getElementById('current-round').textContent = this.state.round;
        document.getElementById('player-score').textContent = this.state.playerWins;
        document.getElementById('computer-score').textContent = this.state.computerWins;
    }
    
    reset() {
        this.state = { round: 1, playerWins: 0, computerWins: 0, draws: 0, finished: false };
        this.isProcessing = false;
        
        document.getElementById('player-choice').textContent = '?';
        document.getElementById('computer-choice').textContent = '?';
        document.getElementById('round-result').textContent = '';
        document.getElementById('round-result').className = 'result-text';
        
        document.querySelectorAll('.choice-button').forEach(btn => {
            btn.disabled = false;
            btn.style.opacity = '1';
            btn.style.transform = 'scale(1)';
        });
        
        this.updateDisplay();
        
        // リセット時のエフェクト
        this.createRandomSparkle();
    }
}

// デバッグ情報表示関数
function showDebugInfo() {
    const info = [
        `MegaBattleSystem: ${typeof MegaBattleSystem}`,
        `FlashyJankenGame: ${typeof window.debugGame}`,
        `BattleSystem: ${window.debugGame ? typeof window.debugGame.battleSystem : 'no game'}`,
        `IsAnimating: ${window.debugGame ? window.debugGame.battleSystem?.isAnimating : 'unknown'}`
    ].join('\n');
    
    alert(info);
}

console.log('📄 script_flashy.js loaded!');

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM Content Loaded - Starting FlashyJankenGame...');
    console.log('🔍 MegaBattleSystem available?', typeof MegaBattleSystem);
    
    try {
        const game = new FlashyJankenGame();
        console.log('✅ FlashyJankenGame created successfully');
        window.debugGame = game; // デバッグ用にグローバルに保存
    } catch (error) {
        console.error('❌ FlashyJankenGame creation error:', error);
    }
});