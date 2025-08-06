// Hello World アプリのJavaScript

// Hello World を表示する関数
function showHelloWorld() {
    const messageArea = document.getElementById('messageArea');
    messageArea.textContent = 'Hello World!';
    messageArea.classList.add('show');
    messageArea.style.display = 'block';
}

// ページ読み込み完了後にイベントリスナーを設定
document.addEventListener('DOMContentLoaded', function() {
    const showButton = document.getElementById('showButton');
    showButton.addEventListener('click', showHelloWorld);
    
    console.log('Hello World アプリが正常に読み込まれました');
});