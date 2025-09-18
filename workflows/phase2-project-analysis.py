#!/usr/bin/env python3
"""
Phase 2: Project Context Analysis
BOC-95に基づく段階的問題解決ワークフローシステム

目的: プロジェクト構造スキャン、目的・意図の理解、技術スタック特定
"""

import os
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re


class ProjectAnalysisEngine:
    def __init__(self, project_path: str = None):
        """Project Analysis Engine初期化"""
        self.project_path = Path(project_path or os.getcwd())
        self.ai_hub_dir = Path(
            "/data/data/com.termux/files/home/ai-assistant-knowledge-hub"
        )
        self.temp_dir = self.ai_hub_dir / "temp"

        # プロジェクト分析結果
        self.analysis_result = {
            "project_path": str(self.project_path),
            "project_structure": {},
            "project_purpose": {},
            "tech_stack": {},
            "architecture_patterns": {},
            "development_context": {},
        }

    def analyze_project_comprehensive(self) -> Dict:
        """包括的プロジェクト分析実行"""
        print(f"🔍 プロジェクト分析開始: {self.project_path}")

        # 1. プロジェクト構造スキャン
        self._scan_project_structure()

        # 2. プロジェクト目的・意図の理解
        self._analyze_project_purpose()

        # 3. 技術スタック特定
        self._detect_tech_stack()

        # 4. アーキテクチャパターン分析
        self._analyze_architecture_patterns()

        # 5. 開発コンテキスト分析
        self._analyze_development_context()

        # 6. 分析結果保存
        self._save_analysis_result()

        print("✅ プロジェクト分析完了")
        return self.analysis_result

    def _scan_project_structure(self):
        """プロジェクト構造スキャン"""
        print("📁 プロジェクト構造スキャン中...")

        structure = {
            "root_files": [],
            "directories": [],
            "key_files": {},
            "file_counts": {},
            "total_files": 0,
        }

        try:
            # ルートディレクトリのファイル・フォルダ取得
            for item in self.project_path.iterdir():
                if item.is_file():
                    structure["root_files"].append(item.name)
                elif item.is_dir() and not item.name.startswith("."):
                    structure["directories"].append(item.name)

            # 重要ファイルの存在確認
            key_files = [
                "package.json",
                "requirements.txt",
                "Cargo.toml",
                "go.mod",
                "README.md",
                "CLAUDE.md",
                "capacitor.config.json",
                "tsconfig.json",
                "webpack.config.js",
                "vite.config.js",
            ]

            for key_file in key_files:
                file_path = self.project_path / key_file
                if file_path.exists():
                    structure["key_files"][key_file] = str(file_path)

            # ファイル拡張子別カウント
            structure["file_counts"] = self._count_files_by_extension()

            # 総ファイル数
            result = subprocess.run(
                ["find", str(self.project_path), "-type", "f", "!", "-path", "*/.*"],
                capture_output=True,
                text=True,
            )
            structure["total_files"] = (
                len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            )

            self.analysis_result["project_structure"] = structure
            print(
                f"📊 構造スキャン完了: {structure['total_files']} files, {len(structure['directories'])} dirs"
            )

        except Exception as e:
            print(f"⚠️  構造スキャンエラー: {e}")

    def _count_files_by_extension(self) -> Dict[str, int]:
        """拡張子別ファイル数カウント"""
        file_counts = {}

        try:
            result = subprocess.run(
                ["find", str(self.project_path), "-type", "f", "!", "-path", "*/.*"],
                capture_output=True,
                text=True,
            )

            for file_path in result.stdout.strip().split("\n"):
                if file_path:
                    ext = Path(file_path).suffix.lower()
                    if ext:
                        file_counts[ext] = file_counts.get(ext, 0) + 1
                    else:
                        file_counts["no_extension"] = (
                            file_counts.get("no_extension", 0) + 1
                        )
        except:
            pass

        return file_counts

    def _analyze_project_purpose(self):
        """プロジェクト目的・意図の理解"""
        print("🎯 プロジェクト目的分析中...")

        purpose = {
            "name": "",
            "description": "",
            "purpose": "",
            "features": [],
            "domain": "",
            "user_target": "",
        }

        # README.md分析
        readme_path = self.project_path / "README.md"
        if readme_path.exists():
            purpose.update(self._analyze_readme(readme_path))

        # package.json分析 (Node.js/Web プロジェクト)
        package_json_path = self.project_path / "package.json"
        if package_json_path.exists():
            purpose.update(self._analyze_package_json(package_json_path))

        # CLAUDE.md分析
        claude_md_path = self.project_path / "CLAUDE.md"
        if claude_md_path.exists():
            purpose.update(self._analyze_claude_md(claude_md_path))

        # プロジェクト名から推測
        if not purpose["name"]:
            purpose["name"] = self.project_path.name

        # ドメイン推測
        purpose["domain"] = self._infer_project_domain(purpose)

        self.analysis_result["project_purpose"] = purpose
        print(f"🏷️  プロジェクト特定: {purpose['name']} ({purpose['domain']})")

    def _analyze_readme(self, readme_path: Path) -> Dict:
        """README.md分析"""
        purpose_data = {}

        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            # タイトル抽出
            title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
            if title_match:
                purpose_data["name"] = title_match.group(1).strip()

            # 説明抽出
            desc_match = re.search(
                r"#+\s*(Description|概要|説明)\s*\n(.+?)(?=\n#+|\n\n|\Z)",
                content,
                re.DOTALL | re.IGNORECASE,
            )
            if desc_match:
                purpose_data["description"] = desc_match.group(2).strip()

            # 機能リスト抽出
            features = re.findall(r"[-*]\s+(.+)", content)
            if features:
                purpose_data["features"] = features[:10]  # 最大10個

        except Exception as e:
            print(f"⚠️  README分析エラー: {e}")

        return purpose_data

    def _analyze_package_json(self, package_json_path: Path) -> Dict:
        """package.json分析"""
        purpose_data = {}

        try:
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)

            purpose_data["name"] = package_data.get("name", "")
            purpose_data["description"] = package_data.get("description", "")

            # スクリプトから推測
            scripts = package_data.get("scripts", {})
            if "dev" in scripts or "serve" in scripts:
                purpose_data["purpose"] = "Web Development Project"

        except Exception as e:
            print(f"⚠️  package.json分析エラー: {e}")

        return purpose_data

    def _analyze_claude_md(self, claude_md_path: Path) -> Dict:
        """CLAUDE.md分析"""
        purpose_data = {}

        try:
            with open(claude_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # プロジェクト情報抽出
            if "プロジェクト" in content or "Project" in content:
                purpose_data["user_target"] = "AI協業開発プロジェクト"

        except Exception as e:
            print(f"⚠️  CLAUDE.md分析エラー: {e}")

        return purpose_data

    def _infer_project_domain(self, purpose: Dict) -> str:
        """プロジェクトドメイン推測"""
        name = purpose.get("name", "").lower()
        description = purpose.get("description", "").lower()
        features = " ".join(purpose.get("features", [])).lower()

        # キーワードベースのドメイン判定
        if any(
            keyword in name + description + features
            for keyword in ["recipe", "レシピ", "cooking", "料理"]
        ):
            return "Food/Recipe Application"
        elif any(
            keyword in name + description + features
            for keyword in ["mcp", "server", "api"]
        ):
            return "MCP Server/API"
        elif any(
            keyword in name + description + features
            for keyword in ["web", "app", "pwa"]
        ):
            return "Web Application"
        elif any(
            keyword in name + description + features
            for keyword in ["mobile", "android", "ios"]
        ):
            return "Mobile Application"
        else:
            return "General Development"

    def _detect_tech_stack(self):
        """技術スタック特定"""
        print("🔧 技術スタック分析中...")

        tech_stack = {
            "framework": [],
            "language": [],
            "build_tools": [],
            "mobile_platform": [],
            "database": [],
            "deployment": [],
        }

        # package.json分析
        if "package.json" in self.analysis_result["project_structure"]["key_files"]:
            tech_stack.update(self._analyze_node_tech_stack())

        # Capacitor検出
        if (
            "capacitor.config.json"
            in self.analysis_result["project_structure"]["key_files"]
        ):
            tech_stack["mobile_platform"].append("Capacitor")

        # ファイル拡張子から言語推測
        file_counts = self.analysis_result["project_structure"]["file_counts"]
        if ".js" in file_counts:
            tech_stack["language"].append("JavaScript")
        if ".ts" in file_counts:
            tech_stack["language"].append("TypeScript")
        if ".py" in file_counts:
            tech_stack["language"].append("Python")
        if ".html" in file_counts:
            tech_stack["framework"].append("Web/HTML")
        if ".css" in file_counts:
            tech_stack["framework"].append("CSS")

        self.analysis_result["tech_stack"] = tech_stack
        print(f"⚙️  技術スタック: {', '.join(tech_stack.get('language', []))}")

    def _analyze_node_tech_stack(self) -> Dict:
        """Node.js技術スタック分析"""
        tech_update = {"framework": [], "build_tools": []}

        try:
            package_json_path = self.analysis_result["project_structure"]["key_files"][
                "package.json"
            ]
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)

            dependencies = {
                **package_data.get("dependencies", {}),
                **package_data.get("devDependencies", {}),
            }

            # フレームワーク検出
            framework_map = {
                "react": "React",
                "vue": "Vue.js",
                "angular": "Angular",
                "@capacitor/core": "Capacitor",
                "express": "Express.js",
            }

            for dep, framework in framework_map.items():
                if dep in dependencies:
                    tech_update["framework"].append(framework)

            # ビルドツール検出
            build_tool_map = {
                "webpack": "Webpack",
                "vite": "Vite",
                "rollup": "Rollup",
                "esbuild": "ESBuild",
            }

            for dep, tool in build_tool_map.items():
                if dep in dependencies:
                    tech_update["build_tools"].append(tool)

        except Exception as e:
            print(f"⚠️  Node.js技術スタック分析エラー: {e}")

        return tech_update

    def _analyze_architecture_patterns(self):
        """アーキテクチャパターン分析"""
        print("🏗️  アーキテクチャパターン分析中...")

        patterns = {
            "structure_type": "",
            "design_patterns": [],
            "file_organization": "",
            "complexity_level": "",
        }

        # ディレクトリ構造からパターン推測
        directories = self.analysis_result["project_structure"]["directories"]

        if "src" in directories:
            patterns["structure_type"] = "Source-based Organization"
        if "lib" in directories and "workflows" in directories:
            patterns["structure_type"] = "Library/Workflow Organization"
        if "android" in directories or "ios" in directories:
            patterns["design_patterns"].append("Mobile Hybrid Pattern")

        # ファイル数から複雑さ推測
        total_files = self.analysis_result["project_structure"]["total_files"]
        if total_files < 20:
            patterns["complexity_level"] = "Simple"
        elif total_files < 100:
            patterns["complexity_level"] = "Medium"
        else:
            patterns["complexity_level"] = "Complex"

        self.analysis_result["architecture_patterns"] = patterns
        print(
            f"🏛️  アーキテクチャ: {patterns['structure_type']} ({patterns['complexity_level']})"
        )

    def _analyze_development_context(self):
        """開発コンテキスト分析"""
        print("👥 開発コンテキスト分析中...")

        context = {
            "development_stage": "",
            "ai_integration": False,
            "collaboration_tools": [],
            "quality_tools": [],
            "development_approach": "",
        }

        # CLAUDE.mdの存在確認
        if "CLAUDE.md" in self.analysis_result["project_structure"]["key_files"]:
            context["ai_integration"] = True
            context["collaboration_tools"].append("Claude AI")

        # 開発ツール検出
        if ".gitignore" in self.analysis_result["project_structure"]["root_files"]:
            context["collaboration_tools"].append("Git")

        # package.jsonからESLint等検出
        if "package.json" in self.analysis_result["project_structure"]["key_files"]:
            context.update(self._analyze_dev_tools_context())

        # 開発段階推測
        if self.analysis_result["project_structure"]["total_files"] > 50:
            context["development_stage"] = "Active Development"
        else:
            context["development_stage"] = "Early Stage"

        self.analysis_result["development_context"] = context
        print(f"🚀 開発段階: {context['development_stage']}")

    def _analyze_dev_tools_context(self) -> Dict:
        """開発ツールコンテキスト分析"""
        context_update = {"quality_tools": [], "development_approach": ""}

        try:
            package_json_path = self.analysis_result["project_structure"]["key_files"][
                "package.json"
            ]
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)

            dev_dependencies = package_data.get("devDependencies", {})

            # 品質ツール検出
            quality_tools = ["eslint", "prettier", "jest", "cypress", "typescript"]
            for tool in quality_tools:
                if tool in dev_dependencies:
                    context_update["quality_tools"].append(tool)

            # 開発アプローチ推測
            if "typescript" in dev_dependencies:
                context_update["development_approach"] = "Type-safe Development"
            elif "eslint" in dev_dependencies:
                context_update["development_approach"] = "Quality-focused Development"

        except Exception as e:
            print(f"⚠️  開発ツール分析エラー: {e}")

        return context_update

    def _save_analysis_result(self):
        """分析結果保存"""
        self.temp_dir.mkdir(exist_ok=True)

        # Phase 2の結果ファイル
        analysis_file = self.temp_dir / f"phase2_analysis_{self.project_path.name}.json"

        with open(analysis_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "phase": "2-project-analysis",
                    "timestamp": subprocess.check_output(["date"]).decode().strip(),
                    "project_name": self.project_path.name,
                    "analysis_result": self.analysis_result,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"💾 分析結果保存: {analysis_file}")


def main():
    """メイン実行関数"""
    project_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    try:
        # Project Analysis Engine初期化
        analysis_engine = ProjectAnalysisEngine(project_path)

        # プロジェクト分析実行
        analysis_result = analysis_engine.analyze_project_comprehensive()

        print(f"🎯 Phase 2 完了: {analysis_result['project_purpose']['name']}")
        print(
            f"💡 次のコマンド: python {analysis_engine.ai_hub_dir}/workflows/phase3-requirements-analysis.py"
        )

    except Exception as e:
        print(f"❌ Phase 2 エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
