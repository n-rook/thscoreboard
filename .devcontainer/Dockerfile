FROM mcr.microsoft.com/devcontainers/python:3.11@sha256:2da3e966c6fde093c757c6ea372bfb5b4302c6ec7d9f5fb60796cd211aaacc67

RUN mkdir -p \
        /workspace/thscoreboard \
        /workspace/.pnpm-store \
        /home/vscode/.ssh \
        /home/vscode/.codex \
        /home/vscode/.vscode-server \
    && chown -R vscode:vscode \
        /workspace \
        /home/vscode/.ssh \
        /home/vscode/.codex \
        /home/vscode/.vscode-server \
    && printf '\nexport GPG_TTY=$(tty)\n' >> /etc/bash.bashrc

USER vscode