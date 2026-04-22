import os
import subprocess
import platform

# ==============================================================================
# INSTRUÇÕES DE INSTALAÇÃO DO MOTOR LATEX:
#
# ARCH LINUX:
#   sudo pacman -S texlive-basic texlive-latexextra texlive-fontsrecommended
#
# UBUNTU / DEBIAN / MINT:
#   sudo apt update
#   sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
#
# WINDOWS:
#   1. Baixe e instale o MiKTeX (https://miktex.org/download) ou TeX Live.
#   2. Reinicie o terminal após a instalação.
#
# Sem regras de uso ou modificações By Adiog0
# ==============================================================================

def gerar_curriculo():

    latex_template = r"""
\documentclass[a4paper,10pt]{article}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[portuguese]{babel}
\usepackage{lmodern}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{microtype}
\usepackage[left=1.2cm, right=1.2cm, top=1.0cm, bottom=1.0cm]{geometry}

\pagestyle{empty}
\setlength{\parindent}{0pt}

\titleformat{\section}{\bfseries\large}{}{0pt}{\uppercase}
\titlespacing{\section}{0pt}{8pt}{4pt}

\newcommand{\sectionrule}{\vspace{-4pt}\hrule\vspace{5pt}}
\newcommand{\resumeItem}[1]{\item \small #1}

\newcommand{\resumeSubheading}[4]{
  \item
    \begin{tabular*}{\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #3 \\
      \textit{\small #2} & \textit{\small #4} \\
    \end{tabular*}\vspace{-6pt}
}

\begin{document}

% --- CABEÇALHO ---
\begin{center}
    {\Huge \textbf{NOME COMPLETO}} \\[5pt]
    \small Cidade, Estado $|$ \href{mailto:email@exemplo.com}{email@exemplo.com} $|$ (00) 00000-0000 \\
    \href{https://www.linkedin.com/in/seu-perfil}{linkedin.com/in/seu-perfil} $|$ \href{https://github.com/seu-usuario}{github.com/seu-usuario}
\end{center}

% --- RESUMO ESTRATÉGICO ---
\section{Resumo Profissional}
\sectionrule
Escreva aqui um resumo de 3 a 4 linhas \textbf{destacando}, principais áreas de domínio e conquistas relevantes. Use \textbf{palavras-chave fortes} do seu mercado para facilitar a triagem por IAs.

% --- EXPERIÊNCIA PROFISSIONAL ---
\section{Experiência Profissional}
\sectionrule
\begin{itemize}[leftmargin=0pt, label={}]

  \resumeSubheading{Nome da Empresa Atual}{Cargo Atual}{Mês/Ano -- Momento}{Cidade, Estado}
  \begin{itemize}[leftmargin=12pt, label=\textbullet, itemsep=1pt, parsep=1pt]
    \resumeItem{Descreva uma conquista quantificável (ex: Reduzi custos em 20\% através da implementação de X).}
    \resumeItem{Descreva uma responsabilidade técnica central utilizando as ferramentas do dia a dia.}
    \resumeItem{Mencione processos de liderança, mentoria ou melhoria contínua que você liderou.}
  \end{itemize}

  \resumeSubheading{Nome da Empresa Anterior}{Cargo Anterior}{Mês/Ano -- Mês/Ano}{Cidade, Estado}
  \begin{itemize}[leftmargin=12pt, label=\textbullet, itemsep=1pt, parsep=1pt]
    \resumeItem{Destaque projetos específicos entregues e o impacto gerado para a empresa.}
    \resumeItem{Foque em resultados: "Implementei Y que resultou na estabilidade de Z".}
  \end{itemize}

\end{itemize}

% --- COMPETÊNCIAS TÉCNICAS ---
\section{Habilidades e Tecnologias}
\sectionrule
\begin{description}[leftmargin=0pt, font=\bfseries, itemsep=-2pt]
  \item[Exemplo Sistemas e Virtualização:] Ferramenta 1, Ferramenta 2, Tecnologia X, Framework Y.
  \item[Domínio B:] Cloud Computing, Infraestrutura, Segurança, Bancos de Dados.
  \item[Domínio C:] Metodologias Ágeis, Governança, Liderança de Equipes.
\end{description}

% --- FORMAÇÃO ---
\section{Formação Acadêmica}
\sectionrule
\textbf{Nome do Curso de Graduação ou Pós} -- Nome da Instituição (Concluído em AAAA) \\
\textbf{Outro Curso ou Certificação Relevante} -- Instituição (Em andamento)

% --- IDIOMAS ---
\section{Idiomas}
\sectionrule
\textbf{Português:} Nativo \quad \textbf{Inglês:} Nível de Proficiência \quad \textbf{Espanhol:} Nível de Proficiência

\end{document}
"""

    file_name = "curriculo"
    tex_file = f"{file_name}.tex"

    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(latex_template)

    try:
        print(f"Sistema: {platform.system()}")
        print(f"Gerando '{file_name}.pdf'...")

        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file], check=True)

        for ext in ["tex", "log", "aux", "out"]:
            aux = f"{file_name}.{ext}"
            if os.path.exists(aux): os.remove(aux)

        print(f"\n[SUCESSO] O arquivo '{file_name}.pdf' foi gerado com sucesso!")

    except Exception as e:
        print(f"\n[ERRO] Ocorreu um problema: {e}")
        print("Dica: Verifique se o 'pdflatex' está instalado e configurado no seu PATH.")

if __name__ == "__main__":
    gerar_curriculo()
