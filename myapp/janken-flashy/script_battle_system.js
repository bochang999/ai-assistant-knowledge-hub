// 🔥 ド派手バトルシステム
console.log('📄 script_battle_system.js loaded!');

class MegaBattleSystem {
    constructor(game) {
        console.log('🔥 MegaBattleSystem constructor called');
        console.log('🔥 Game object received:', !!game);
        this.game = game;
        this.isAnimating = false;
        
        try {
            this.setupBattleElements();
            console.log('🔥 MegaBattleSystem initialized successfully');
        } catch (error) {
            console.error('❌ MegaBattleSystem setup error:', error);
        }
    }
    
    setupBattleElements() {
        // バトルエフェクト用オーバーレイ要素作成
        this.createOverlayElements();
    }
    
    createOverlayElements() {
        // フラッシュオーバーレイ
        this.flashOverlay = document.createElement('div');
        this.flashOverlay.className = 'flash-overlay';
        document.body.appendChild(this.flashOverlay);
        
        // 爆発オーバーレイ
        this.explosionOverlay = document.createElement('div');
        this.explosionOverlay.className = 'explosion-overlay';
        document.body.appendChild(this.explosionOverlay);
        
        // バトルエフェクトコンテナ
        this.battleContainer = document.createElement('div');
        this.battleContainer.className = 'battle-effect-overlay';
        document.body.appendChild(this.battleContainer);
    }
    
    // メインバトル開始
    async startMegaBattle(playerChoice, computerChoice) {
        if (this.isAnimating) return { result: '引き分け', playerChoice, computerChoice };
        this.isAnimating = true;
        
        console.log('🔥 MEGA BATTLE START:', playerChoice, 'vs', computerChoice);
        
        try {
            // フェーズ1: カウントダウン
            await this.countdownPhase();
            
            // フェーズ2: 攻撃エフェクト
            await this.attackPhase(playerChoice, computerChoice);
            
            // フェーズ3: 衝突判定
            const result = this.calculateBattleResult(playerChoice, computerChoice);
            await this.collisionPhase();
            
            // フェーズ4: 結果演出
            await this.resultPhase(result, playerChoice, computerChoice);
            
            this.isAnimating = false;
            return { result, playerChoice, computerChoice };
        } catch (error) {
            console.error('Battle system error:', error);
            this.isAnimating = false;
            return { result: '引き分け', playerChoice, computerChoice };
        }
    }
    
    // カウントダウンフェーズ
    async countdownPhase() {
        const playerEl = document.getElementById('player-choice');
        const computerEl = document.getElementById('computer-choice');
        
        // カウントダウン演出
        for (let i = 3; i > 0; i--) {
            playerEl.textContent = i;
            computerEl.textContent = i;
            
            // 数字を虹色に
            const hue = (4 - i) * 120;
            playerEl.style.color = `hsl(${hue}, 70%, 60%)`;
            computerEl.style.color = `hsl(${hue}, 70%, 60%)`;
            playerEl.style.fontSize = '6rem';
            computerEl.style.fontSize = '6rem';
            
            // 画面フラッシュ
            this.screenFlash();
            
            await this.wait(600);
        }
        
        // FIGHT!
        playerEl.textContent = 'FIGHT!';
        computerEl.textContent = 'FIGHT!';
        playerEl.style.color = '#ff0000';
        computerEl.style.color = '#ff0000';
        playerEl.style.fontSize = '3rem';
        computerEl.style.fontSize = '3rem';
        
        await this.wait(500);
        
        // 元のサイズに戻す
        playerEl.style.fontSize = '';
        computerEl.style.fontSize = '';
        playerEl.style.color = '';
        computerEl.style.color = '';
    }
    
    // 攻撃フェーズ
    async attackPhase(playerChoice, computerChoice) {
        const playerEl = document.getElementById('player-choice');
        const computerEl = document.getElementById('computer-choice');
        
        // 選択した手を表示
        playerEl.textContent = this.game.icons[playerChoice];
        computerEl.textContent = this.game.icons[computerChoice];
        
        // 同時攻撃開始
        await Promise.all([
            this.launchPlayerAttack(playerChoice),
            this.launchComputerAttack(computerChoice)
        ]);
    }
    
    // プレイヤー攻撃
    async launchPlayerAttack(choice) {
        const attackType = this.getAttackType(choice);
        
        // 攻撃エフェクト作成
        const effect = this.createAttackEffect(choice, 'player');
        
        // 画面エフェクト
        await this.executeAttackEffects(attackType, 'player');
        
        return effect;
    }
    
    // コンピューター攻撃
    async launchComputerAttack(choice) {
        const attackType = this.getAttackType(choice);
        
        // 攻撃エフェクト作成  
        const effect = this.createAttackEffect(choice, 'computer');
        
        // 画面エフェクト
        await this.executeAttackEffects(attackType, 'computer');
        
        return effect;
    }
    
    getAttackType(choice) {
        const types = {
            'グー': 'rock',
            'チョキ': 'scissors', 
            'パー': 'paper'
        };
        return types[choice];
    }
    
    createAttackEffect(choice, side) {
        const effect = document.createElement('div');
        effect.className = `attack-effect ${this.getAttackType(choice)}`;
        effect.textContent = this.game.icons[choice];
        
        // 位置設定
        if (side === 'player') {
            effect.style.left = '20%';
            effect.style.top = '45%';
        } else {
            effect.style.right = '20%';
            effect.style.top = '45%';
            effect.style.transform = 'scaleX(-1)'; // 左向きに
        }
        
        this.battleContainer.appendChild(effect);
        
        // 自動削除
        setTimeout(() => {
            if (effect.parentNode) {
                effect.parentNode.removeChild(effect);
            }
        }, 2000);
        
        return effect;
    }
    
    async executeAttackEffects(attackType, side) {
        switch (attackType) {
            case 'rock':
                await this.rockAttackEffect();
                break;
            case 'scissors':
                await this.scissorsAttackEffect();
                break;
            case 'paper':
                await this.paperAttackEffect();
                break;
        }
    }
    
    // グー攻撃「岩石大爆発」
    async rockAttackEffect() {
        // 画面を茶色に染める
        document.body.style.animation = 'colorFlashRed 1s ease-out';
        
        // 地震エフェクト
        document.body.style.animation += ', megaShake 1s ease-out';
        
        // 岩石パーティクル大量生成
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                this.game.particles.push({
                    x: Math.random() * window.innerWidth,
                    y: Math.random() * window.innerHeight,
                    vx: (Math.random() - 0.5) * 20,
                    vy: (Math.random() - 0.5) * 20,
                    life: 100,
                    maxLife: 100,
                    color: '#8B4513',
                    size: Math.random() * 12 + 5
                });
            }, i * 20);
        }
        
        await this.wait(1000);
        document.body.style.animation = '';
    }
    
    // チョキ攻撃「超音速斬撃」
    async scissorsAttackEffect() {
        // 画面を白くフラッシュ
        this.flashOverlay.classList.add('active');
        
        // 青い光線エフェクト
        document.body.style.animation = 'colorFlashBlue 1.5s ease-out';
        
        // 斬撃パーティクル
        for (let i = 0; i < 30; i++) {
            setTimeout(() => {
                this.game.particles.push({
                    x: Math.random() * window.innerWidth,
                    y: Math.random() * window.innerHeight,
                    vx: Math.random() * 30 - 15,
                    vy: Math.random() * 30 - 15,
                    life: 80,
                    maxLife: 80,
                    color: '#00ffff',
                    size: Math.random() * 8 + 3
                });
            }, i * 30);
        }
        
        setTimeout(() => {
            this.flashOverlay.classList.remove('active');
        }, 300);
        
        await this.wait(1500);
        document.body.style.animation = '';
    }
    
    // パー攻撃「嵐の竜巻」  
    async paperAttackEffect() {
        // 画面を白く染める
        document.body.style.animation = 'colorFlashWhite 2s ease-out';
        
        // 竜巻パーティクル
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        
        for (let i = 0; i < 80; i++) {
            setTimeout(() => {
                const angle = (i / 80) * Math.PI * 8; // 螺旋
                const radius = (i / 80) * 200;
                this.game.particles.push({
                    x: centerX + Math.cos(angle) * radius,
                    y: centerY + Math.sin(angle) * radius,
                    vx: Math.cos(angle + Math.PI/2) * 5,
                    vy: Math.sin(angle + Math.PI/2) * 5,
                    life: 120,
                    maxLife: 120,
                    color: '#87CEEB',
                    size: Math.random() * 6 + 4
                });
            }, i * 25);
        }
        
        await this.wait(2000);
        document.body.style.animation = '';
    }
    
    // 衝突フェーズ
    async collisionPhase() {
        // 時間停止演出
        const allElements = document.querySelectorAll('*');
        allElements.forEach(el => {
            if (el.style.animation) {
                el.classList.add('freeze-frame');
            }
        });
        
        await this.wait(300);
        
        // 大爆発
        this.explosionOverlay.classList.add('active');
        this.screenShake('MEGA');
        
        // 時間停止解除
        allElements.forEach(el => {
            el.classList.remove('freeze-frame');
        });
        
        setTimeout(() => {
            this.explosionOverlay.classList.remove('active');
        }, 1000);
        
        await this.wait(1000);
    }
    
    // 結果フェーズ
    async resultPhase(result, playerChoice, computerChoice) {
        const playerEl = document.getElementById('player-choice');
        const computerEl = document.getElementById('computer-choice');
        
        if (result === '勝ち') {
            await this.victoryExplosion(playerEl, computerEl);
        } else if (result === '負け') {
            await this.defeatDrama(playerEl, computerEl);
        } else {
            await this.drawChaos(playerEl, computerEl);
        }
    }
    
    // 勝利大爆発
    async victoryExplosion(winner, loser) {
        // 勝利テキスト表示
        const victoryText = document.createElement('div');
        victoryText.className = 'mega-victory-text';
        victoryText.textContent = '🎉 VICTORY! 🎉';
        document.body.appendChild(victoryText);
        
        // 勝者の超派手演出
        winner.classList.add('hand-3d-victory');
        winner.style.animation = 'victoryMegaCelebration 3s ease-in-out';
        
        // 敗者の演出
        loser.classList.add('hand-3d-defeat');
        loser.style.animation = 'defeatDramaticFall 2s ease-in forwards';
        
        // 金色パーティクル大爆発
        for (let i = 0; i < 100; i++) {
            setTimeout(() => {
                this.game.particles.push({
                    x: window.innerWidth / 2,
                    y: window.innerHeight / 2,
                    vx: (Math.random() - 0.5) * 25,
                    vy: (Math.random() - 0.5) * 25,
                    life: 150,
                    maxLife: 150,
                    color: 'gold',
                    size: Math.random() * 10 + 5
                });
            }, i * 30);
        }
        
        await this.wait(3000);
        
        // クリーンアップ
        victoryText.remove();
        winner.classList.remove('hand-3d-victory');
        loser.classList.remove('hand-3d-defeat');
        winner.style.animation = '';
        loser.style.animation = '';
    }
    
    // 敗北ドラマ
    async defeatDrama(winner, loser) {
        // 敗北テキスト
        const defeatText = document.createElement('div');
        defeatText.className = 'mega-defeat-text';
        defeatText.textContent = '💀 DEFEAT... 💀';
        document.body.appendChild(defeatText);
        
        // 敗者（プレイヤー）の演出
        loser.classList.add('hand-3d-defeat');
        loser.style.animation = 'defeatDramaticFall 2s ease-in forwards';
        
        // 勝者の控えめ勝利
        winner.style.animation = 'victoryMegaCelebration 2s ease-in-out';
        
        // 暗いパーティクル
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                this.game.particles.push({
                    x: Math.random() * window.innerWidth,
                    y: window.innerHeight + 50,
                    vx: (Math.random() - 0.5) * 4,
                    vy: -Math.random() * 8 - 2,
                    life: 100,
                    maxLife: 100,
                    color: '#444444',
                    size: Math.random() * 6 + 3
                });
            }, i * 40);
        }
        
        await this.wait(3000);
        
        // クリーンアップ
        defeatText.remove();
        loser.classList.remove('hand-3d-defeat');
        winner.style.animation = '';
        loser.style.animation = '';
    }
    
    // 引き分けカオス
    async drawChaos(playerEl, computerEl) {
        // 引き分けテキスト
        const drawText = document.createElement('div');
        drawText.className = 'mega-draw-text';
        drawText.textContent = '🤝 DRAW! 🤝';
        document.body.appendChild(drawText);
        
        // 両方混乱演出
        playerEl.style.animation = 'drawConfusion 2s ease-in-out';
        computerEl.style.animation = 'drawConfusion 2s ease-in-out';
        
        // カラフルパーティクル
        for (let i = 0; i < 60; i++) {
            setTimeout(() => {
                this.game.particles.push({
                    x: Math.random() * window.innerWidth,
                    y: Math.random() * window.innerHeight,
                    vx: (Math.random() - 0.5) * 6,
                    vy: (Math.random() - 0.5) * 6,
                    life: 80,
                    maxLife: 80,
                    color: `hsl(${Math.random() * 360}, 70%, 60%)`,
                    size: Math.random() * 5 + 2
                });
            }, i * 25);
        }
        
        await this.wait(2000);
        
        // クリーンアップ
        drawText.remove();
        playerEl.style.animation = '';
        computerEl.style.animation = '';
    }
    
    calculateBattleResult(playerChoice, computerChoice) {
        if (playerChoice === computerChoice) return '引き分け';
        
        const wins = { 'グー': 'チョキ', 'チョキ': 'パー', 'パー': 'グー' };
        return wins[playerChoice] === computerChoice ? '勝ち' : '負け';
    }
    
    // ユーティリティメソッド
    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    screenFlash() {
        this.flashOverlay.classList.add('active');
        setTimeout(() => {
            this.flashOverlay.classList.remove('active');
        }, 200);
    }
    
    screenShake(intensity = 'normal') {
        if (intensity === 'MEGA') {
            document.body.style.animation = 'megaShake 1s ease-out';
        } else {
            document.body.style.animation = 'megaShake 0.5s ease-out';
        }
        
        setTimeout(() => {
            document.body.style.animation = '';
        }, intensity === 'MEGA' ? 1000 : 500);
    }
    
    cleanup() {
        // 全エフェクト要素を削除
        if (this.flashOverlay) this.flashOverlay.remove();
        if (this.explosionOverlay) this.explosionOverlay.remove();
        if (this.battleContainer) this.battleContainer.remove();
    }
}