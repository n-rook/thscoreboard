FROM sbtscala/scala-sbt:eclipse-temurin-21.0.8_9_1.11.6_2.13.16@sha256:7f8d1f78e15fd13905253b41b984ac9d52ae035b20e8376d385317e91c68bf13 AS kaitai-struct-compiler-builder

WORKDIR /tmp

RUN curl -fsSL -o kaitai-struct-compiler-0.9.zip https://github.com/kaitai-io/kaitai_struct_compiler/releases/download/0.9/kaitai-struct-compiler-0.9.zip \
    && echo "3038243334fb65bbb264f33b82986facfe1fbad2de1978766899855b40212215  kaitai-struct-compiler-0.9.zip" | sha256sum -c - \
    && cd /opt \
    && jar xf /tmp/kaitai-struct-compiler-0.9.zip \
    && mv kaitai-struct-compiler-0.9 kaitai-struct-compiler \
    && chmod +x /opt/kaitai-struct-compiler/bin/kaitai-struct-compiler

FROM mcr.microsoft.com/devcontainers/python:3.11@sha256:2da3e966c6fde093c757c6ea372bfb5b4302c6ec7d9f5fb60796cd211aaacc67

COPY --from=kaitai-struct-compiler-builder /opt/java/openjdk /opt/java/openjdk
COPY --from=kaitai-struct-compiler-builder /opt/kaitai-struct-compiler /opt/kaitai-struct-compiler

ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:/opt/kaitai-struct-compiler/bin:${PATH}"

RUN ln -s /opt/kaitai-struct-compiler/bin/kaitai-struct-compiler /usr/local/bin/kaitai-struct-compiler \
    && ln -s /opt/kaitai-struct-compiler/bin/kaitai-struct-compiler /usr/local/bin/ksc

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