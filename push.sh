#!/bin/bash

# ============================================
# Git 自动提交推送脚本 (push.sh)
# 用法: 在 Git 仓库目录下执行 './push.sh [可选的提交信息]'
# ============================================

# 1. 检查是否有需要提交的更改
if git diff --cached --quiet && git diff --quiet; then
    echo "============================================"
    echo "✅ 工作区和暂存区都很干净，无需提交。"
    echo "============================================"
    exit 0
fi

# 2. 自动添加所有更改到暂存区 (git add .)
echo "🚀 正在执行 git add ...."
git add .

# 3. 确定提交信息
COMMIT_MSG="$1" # 尝试使用命令行传入的第一个参数作为提交信息

if [ -z "$COMMIT_MSG" ]; then
    # 如果没有传入参数，则提示用户输入
    echo ""
    echo "请为本次提交输入一个简短的描述 (Commit Message):"
    read -r USER_INPUT_MSG

    # 再次检查用户输入是否为空
    if [ -z "$USER_INPUT_MSG" ]; then
        COMMIT_MSG="Auto commit on $(date +'%Y-%m-%d %H:%M:%S')"
        echo "⚠️ 提交信息为空，使用默认信息: $COMMIT_MSG"
    else
        COMMIT_MSG="$USER_INPUT_MSG"
    fi
fi


# 4. 执行 git commit
echo ""
echo "📝 正在执行 git commit -m \"$COMMIT_MSG\" ..."
if git commit -m "$COMMIT_MSG"; then
    echo "✅ 提交成功!"
else
    echo "❌ Git 提交失败，请检查错误信息。"
    exit 1
fi

# 5. 执行 git push
echo ""
echo "📤 正在执行 git push ..."
if git push; then
    echo "============================================"
    echo "🎉 推送成功! 代码已更新到远程仓库。"
    echo "============================================"
else
    echo "❌ Git 推送失败，请检查远程分支和网络连接。"
    exit 1
fi