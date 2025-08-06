npx @google/gemini-cli
pkg install imagemagick
cd /storage/emulated/0/Download  # 画像があるフォルダへ移動
mogrify -strip collage, various pose, {Periphery line, auxiliary lines on body and head}, Contr s-2405017506.png
mogrify -list format
mogrify -strip meta.png
# パッケージ更新
pkg update && pkg upgrade
# Whisper ビルドに必要なツール
pkg install -y git clang cmake make ffmpeg wget unzip
# 内部ストレージへのアクセス許可
termux-setup-storage     # 許可ダイアログが出るので「許可」
mkdir -p ~/src && cd ~/src
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp
make -j$(nproc)                  # 2〜3 分程度
# サイズ感と速度のバランスで medium を推奨（≈900 MB）
./models/download-ggml-model.sh medium
# 例）Download フォルダに rec001.mp3 がある場合
cd ~/src/whisper.cpp/build/bin
./whisper-cli   -f /sdcard/Download/rec001.mp3   -m ../../models/ggml-medium.bin   -l ja -otxt   -of /sdcard/Download/2025-07-05_11_17_53
#!/data/data/com.termux/files/usr/bin/bash
# 使い方: wtranscribe /sdcard/Download/foo.mp3
set -e
IN="$1"
MODEL=$HOME/src/whisper.cpp/models/ggml-medium.bin
BASENAME=$(basename "$IN"); BASENAME=${BASENAME%.*}
OUTDIR=$(dirname "$IN")
ffmpeg -y -i "$IN" -ar 16000 -ac 1 -c:a pcm_s16le /tmp/${BASENAME}.wav
#!/data/data/com.termux/files/usr/bin/bash
# 使い方: wtranscribe /sdcard/Download/foo.mp3
set -e
mkdir -p /tmp             # これを追加！
IN="$1"
MODEL=$HOME/src/whisper.cpp/models/ggml-medium.bin
BASENAME=$(basename "$IN"); BASENAME=${BASENAME%.*}
OUTDIR=$(dirname "$IN")
ffmpeg -y -i "$IN" -ar 16000 -ac 1 -c:a pcm_s16le /tmp/${BASENAME}.wav
ls /sdcard/Download/2025-07-05_11_17_53.mp3
wtranscribe /sdcard/Download/2025-07-05_11_17_53.mp3
ls ~/bin/wtranscribe
mkdir -p ~/bin
nano ~/bin/wtranscribe
chmod +x ~/bin/wtranscribe
~/bin/wtranscribe /sdcard/Download/2025-07-05_11_17_53.mp3
mkdir -p ~/tm
#!/data/data/com.termux/files/usr/bin/bash
set -e
mkdir -p $HOME/tmp
IN="$1"
MODEL=$HOME/src/whisper.cpp/models/ggml-medium.bin
BASENAME=$(basename "$IN"); BASENAME=${BASENAME%.*}
OUTDIR=$(dirname "$IN")
mkdir -p "$OUTDIR"
ffmpeg -y -i "$IN" -ar 16000 -ac 1 -c:a pcm_s16le $HOME/tmp/${BASENAME}.wav
mkdir -p ~/tmp
#!/data/data/com.termux/files/usr/bin/bash
set -e
mkdir -p $HOME/tmp
IN="$1"
echo "IN=[$IN]"
MODEL=$HOME/src/whisper.cpp/models/ggml-medium.bin
BASENAME=$(basename "$IN"); BASENAME=${BASENAME%.*}
OUTDIR=$(dirname "$IN")
mkdir -p "$OUTDIR"
ffmpeg -y -i "$IN" -ar 16000 -ac 1 -c:a pcm_s16le $HOME/tmp/${BASENAME}.wav
pkg update
pkg install python git
pip install beeware briefcase toga
briefcase new
cd tarot_clip
nano src/tarot_clip/app.py
briefcase dev
https://github.com/bochang999/tarot_clip
cd ~/tarot_clip
# まだGitを初期化していなければ
git init
# GitHubと連携（URLを正しく指定）
git remote add origin https://github.com/bochang999/tarot_clip.git
# 全ファイルをGit管理対象に追加
git add .
# 最初のコミット
git commit -m "Initial commit"
# メインブランチ名をmainに統一
git branch -M main
# GitHubにPush！
git push -u origin main
git push -u origin main --force
mkdir -p .github/workflows
nano .github/workflows/android.yml
git add .github/workflows/android.yml
git commit -m "Add GitHub Actions workflow for APK build"
git push
nano .github/workflows/android.yml
git add .github/workflows/android.yml
git commit -m "Fix YAML syntax error"
git push
git add .github/workflows/android.yml
git commit -m "Fix YAML syntax error"
git push
git add .github/workflows/android.yml
git commit -m "Fix YAML syntax error"
git push？
git add .github/workflows/android.yml
git commit -m "Fix YAML syntax error"
git status
rm ".github/workflows\342\201\267


rm ".github/workflows\342\201\267"
rm ".github/workflows\342\201\267"
git status
git add .github/workflows/android.yml
git commit -m "Fix YAML syntax error"
git push
nano .github/workflows/android.yml
git add .github/workflows/android.yml
git commit -m "Fix YAML structure: separate name and on"
git push
nano .github/workflows/android.yml
git add .github/workflows/android.yml
git commit -m "Fix YAML structure: separate name and on"
git push
nano src/tarot_clip/app.py
git add src/tarot_clip/app.py
git commit -m "Fix app.py layout or logic"
git status
git push
nano src/tarot_clip/app.py
git add src/tarot_clip/app.py
git commit -m "Fix main() app name issue"
git push
# Termuxの初期更新
pkg update
pkg upgrade -y
# 必要なパッケージをインストール
pkg install python git -y
# pipとビルドツールをアップグレード
pip install --upgrade pip setuptools wheel
# 必要なライブラリをインストール
pip install fastapi uvicorn
pkg install rust -y
pip install fastapi uvicorn
かたまった？
exit
# 一旦破棄して、明示的に旧バージョンを入れる
pip install "pydantic<2.0.0" "fastapi<0.100" "uvicorn<0.20"
mkdir mcp-test && cd mcp-test
cat > main.py <<EOF
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, MCP world!"}
EOF

# サーバー起動
uvicorn main:app --host 127.0.0.1 --port 8000
exit
curl http://127.0.0.1:8000
git clone https://github.com/modelcontextprotocol/quickstart
cd quickstart/server
pip install 'mcp[cli]'
mcp serve --path tools/example.yaml
git clone https://github.com/modelcontextprotocol/quickstart-resources.git
cd quickstart-resources/weather-server-python
uv run mcp dev server.py
python server.py
ls
python weather.py
exit
top | grep rust
exit
uvicorn weather:app --host 0.0.0.0 --port 8000
ls
cd .../quickstart-resources/weather-server-python
cd /quickstart-resources/weather-server-python
cd quickstart-resources/weather-server-python
uvicorn weather:app --host 0.0.0.0 --port 8000
cat weather.py
mcp --help
mcp run weather.py
printf '{"method":"get_alerts","params":{"state":"CA"}}\n' | mcp client -
nano weather.py
python weather.py
mcp dev weather.yaml
nano weather.yaml
export PYTHONPATH=.
mcp dev weather.yaml
export PYTHONPATH=.
mcp dev "$(pwd)/weather.yaml"
exit
name: weather
description: Get weather forecast and alerts from NWS
tools:
nano weather.yaml
mcp eval --path weather.yaml 'get_alerts("CA")'
mcp run --path weather.yaml
mcp run weather.yaml
nano weather.yaml
mcp run weather.yaml
nano weather.yaml
mcp run weather.yaml
nano weather.yaml
mcp run weather.yaml
nanoweather.yam
nano weather.yaml
nanoweather.py
nano weather.py
mcp run weather.yaml
nano weather.yaml
nano weather.py
mcp run weather.yaml
nano weather.yaml
mcp run weather.yaml
nano weather.yaml
python -c "import weather; print(weather.app)"
mcp run weather.yaml
ls
nano weather.yaml
nano weather.py
python -c "import weather; print(weather.app)"
mcp run --debug weather.yaml
PYTHONPATH=. mcp run weather.yaml
export PYTHONPATH=.
mcp run weather.yaml
nano weather.yaml
mcp run weather.yaml
nano weather.yaml
python -c "from weather import app; print(app)"
nano weather.yaml
PYTHONPATH=. mcp run weather.yaml
nano weather.yaml
PYTHONPATH=. mcp run weather.py
exit
curl -X POST http://127.0.0.1:8000   -H "Content-Type: application/json"   -d '{"method": "get_forecast", "params": {"latitude": 35.6895, "longitude": 139.6917}}'
ps aux | grep mcp
PYTHONPATH=$(pwd) mcp run weather_server.py:app
# → すぐ次のコマンド打ってしまう（サーバー終わってる）
PYTHONPATH=$(pwd) mcp run weather_server.py:app
exit
curl -X POST http://127.0.0.1:8000   -H "Content-Type: application/json"   -d '{"method": "get_forecast", "params": {"latitude": 35.6895, "longitude": 139.6917}}'
curl -X POST http://127.0.0.1:8000   -H "Content-Type: application/json"   -d '{"method": "get_forecast", "params": {"latitude": 35.6895, "longitude": 139.6917}}'
PYTHONPATH=. uvicorn weather_server:app --p ort 8000
PYTHONPATH=. uvicorn weather_server:app --port 8000
exit
curl -X POST http://127.0.0.1:8000   -H "Content-Type: application/json"   -d '{
    "id": 1,
    "jsonrpc": "2.0",
    "method": "get_forecast",
    "params": {
      "latitude": 35.6895,
      "longitude": 139.6917
    }
  }'
exit
cd /data/data/com.termux/files/home/tarot
git remote set-url origin
git push -u origin main
git push origin main
git push
git statas
git status
git push
git status
git push
git staus
git status
git push
git status
git push
git status
git push
git status
git push
adb logcat -
exit
pkg update && pkg upgrade
pkg install nodejs
npm install -g @anthropic-ai/claude-code
run
claude
git status
git push
logcat -d | grep -i python
~/tarot $ logcat -d | grep -i python
~/tarot $logcat -d | grep -i error
cd
logcat -d | grep -i error
logcat -d | grep -i tarot
logcat -d -t 100 | grep -E "(Fatal|FATAL|Crash)"
cd /data/data/com.termux/files/home/tarot
git status
git push
logcat -d | grep -i python
git put
git push
logcat -d | grep -i python
logcat -d | grep -i tarot
claude
cd ~/tarot
cp ~/Download/tarot_icon.png    src/tarot/resources/tarot_icon.png
cp ~/Download/tarot_icon.png    src/tarot/resources/tarot_icon.png
cp ~/Download/tarot_icon.png 
cp /sdcard/Download/tarot_icon.png ~/tarot/src/tarot/resources/
cd ~/tarot
git add src/tarot/resources/tarot_icon.png
git commit -m "Replace tarot_icon.png with moon card icon"
git push origin main
cd /data/data/com.termux/files/home/tarot
git push
だめですね。やったことと現状報告とあなたの次の策を教えて。他のAIにも打開策効くから
git push
git  push
git commit -m "🎉 問題解決成功記録：APKインストール・ア
  イコン変更・アプリ更新完了"
pkg update
pkg install git tmux golang
# GoのbinディレクトリをPATHに追加（ターミナルの起動ごとに自動で追加するのがおすすめ）
export PATH=$PATH:$(go env GOPATH)/bin
# 最新のリリースを go install で導入（例: v0.2.6 の場合）
go install github.com/smtg-ai/claude-squad@latest
# インストール後に
claude-squad help
git clone https://github.com/smtg-ai/claude-squad.git
cd claude-squad
go build -o claude-squad
mv claude-squad ~/../usr/bin/
claude-squad help
claude-squad -p "claude" -p "npx @google/gemini-cli"
claude
claude-squad -p "claude" -p "npx @google/gemini-cli"
which claude
claude-squad -p "/data/data/com.termux/files/usr/bin/claude" -p "npx @google/gemini-cli"
claude-squad -v -p "/data/data/com.termux/files/usr/bin/claude" -p "npx @google/gemini-cli"
claude-squad --program "claude" --program "npx @google/gemini-cli"
claude-squad  "claude" --program "npx @google/gemini-cli"
rm ~/go/bin/claude-squad
cc
rm -rf ~/.claude-squad
rm -rf ~/claude-squad

exit
npx @google/gemini-cli
~ $ kill 30483
~ $ kill -9 30483
~ $
gemini
cd /data/data/com.termux/files/home/download/novel
gemini
claude
cd /data/data/com.termux/files/home/download/novel/
claude
pkill -f gemini
ps aux | grep gemini
kill 30483
kill -9 30483
kill 30483
pkill -f gemini
ps aux | grep gemini
kill 4205
kill -9 4205
termux-setup-storage
ls /storage/emulated/0/
ps aux | grep gemini
kill -9 20947
http-server -p 8080
reset
exit
claude
さっきそれしたらそんなのclaude.mdはなかったって言われたよ
claude
claude --model sonnet 
