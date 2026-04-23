import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

class GeradorCurriculo:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Currículo LaTeX - By Adiog0")
        self.root.geometry("800x900")

        self.main_canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas, padding="20")
        self.scrollable_frame.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        tk.Button(root, text="NEGRITO (SELECIONE O TEXTO NO CAMPO)", command=self.aplicar_negrito,
                  bg="#2c3e50", fg="white", font=("Arial", 9, "bold")).pack(fill="x")
        self.create_widgets()

    def create_widgets(self):
        self.create_section_label("Informações de Contacto")
        self.campos_pessoais = {}
        labels = [("Nome Completo", "nome"), ("Cidade/Estado", "local"), ("E-mail", "email"),
                  ("Telefone", "telefone"), ("LinkedIn (URL)", "linkedin"), ("GitHub (URL)", "github")]
        for text, var in labels:
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text=text, width=20).pack(side="left")
            entry = ttk.Entry(frame)
            entry.pack(side="right", fill="x", expand=True)
            self.campos_pessoais[var] = entry

        self.create_section_label("Resumo Profissional")
        self.txt_resumo = tk.Text(self.scrollable_frame, height=4, font=("Consolas", 10))
        self.txt_resumo.pack(fill="x", pady=5)

        self.create_section_label("Experiência Profissional")
        self.frame_exp = ttk.Frame(self.scrollable_frame)
        self.frame_exp.pack(fill="x")
        self.lista_exp = []
        self.add_exp_field()
        ttk.Button(self.scrollable_frame, text="+ Adicionar Experiência", command=self.add_exp_field).pack(pady=5)

        self.create_section_label("Habilidades (Ex: Infra: Linux, Docker, Proxmox)")
        self.txt_habilidades = tk.Text(self.scrollable_frame, height=5, font=("Consolas", 10))
        self.txt_habilidades.pack(fill="x", pady=5)

        self.create_section_label("Formação Acadêmica")
        self.frame_edu = ttk.Frame(self.scrollable_frame)
        self.frame_edu.pack(fill="x")
        self.lista_edu = []
        self.add_edu_field()
        ttk.Button(self.scrollable_frame, text="+ Adicionar Formação", command=self.add_edu_field).pack(pady=5)

        self.create_section_label("Idiomas")
        self.txt_idiomas = ttk.Entry(self.scrollable_frame)
        self.txt_idiomas.pack(fill="x", pady=5)

        tk.Button(self.scrollable_frame, text="GERAR PDF", command=self.processar_latex,
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"), height=2).pack(fill="x", pady=20)

    def create_section_label(self, text):
        ttk.Label(self.scrollable_frame, text=text.upper(), font=("Arial", 10, "bold")).pack(anchor="w", pady=(15, 5))

    def aplicar_negrito(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Text):
                try:
                    content = widget.get("sel.first", "sel.last")
                    if content:
                        widget.delete("sel.first", "sel.last")
                        widget.insert("insert", rf"\textbf{{{content}}}")
                except tk.TclError:
                    pass
        except:
            pass

    def add_exp_field(self):
        f = ttk.LabelFrame(self.frame_exp, text="Experiência", padding=10)
        f.pack(fill="x", pady=5)
        g1 = ttk.Frame(f); g1.pack(fill="x")
        ttk.Label(g1, text="Empresa:", width=8).pack(side="left")
        emp = ttk.Entry(g1); emp.pack(side="left", fill="x", expand=True)
        ttk.Label(g1, text="Período:", width=8).pack(side="left", padx=(10,0))
        per = ttk.Entry(g1, width=25); per.pack(side="left", padx=5)
        g2 = ttk.Frame(f); g2.pack(fill="x", pady=2)
        ttk.Label(g2, text="Cargo:", width=8).pack(side="left")
        car = ttk.Entry(g2); car.pack(side="left", fill="x", expand=True)
        ttk.Label(g2, text="Local:", width=8).pack(side="left", padx=(10,0))
        loc = ttk.Entry(g2, width=20); loc.pack(side="left", padx=5)
        ttk.Label(f, text="Descrição:").pack(anchor="w")
        desc = tk.Text(f, height=4, font=("Consolas", 10)); desc.pack(fill="x", pady=5)
        self.lista_exp.append({'emp': emp, 'per': per, 'car': car, 'loc': loc, 'desc': desc})

    def add_edu_field(self):
        f = ttk.LabelFrame(self.frame_edu, text="Educação", padding=10)
        f.pack(fill="x", pady=5)
        g1 = ttk.Frame(f); g1.pack(fill="x")
        ttk.Label(g1, text="Curso:", width=8).pack(side="left")
        cur = ttk.Entry(g1); cur.pack(side="left", fill="x", expand=True)
        ttk.Label(g1, text="Conclusão:", width=10).pack(side="left", padx=(10,0))
        data = ttk.Entry(g1, width=15); data.pack(side="left", padx=5)
        g2 = ttk.Frame(f); g2.pack(fill="x", pady=2)
        ttk.Label(g2, text="Instituição:", width=10).pack(side="left")
        inst = ttk.Entry(g2); inst.pack(side="left", fill="x", expand=True)
        self.lista_edu.append({'cur': cur, 'inst': inst, 'data': data})

    def limpar_latex(self, texto):
        if not texto:
            return ""
        return (texto.replace("\\", r"\textbackslash ")
                     .replace("&", r"\&")
                     .replace("%", r"\%")
                     .replace("$", r"\$")
                     .replace("#", r"\#")
                     .replace("_", r"\_")
                     .replace("{", r"\{")
                     .replace("}", r"\}"))

    def processar_latex(self):
        try:
            p = {k: self.limpar_latex(v.get()) for k, v in self.campos_pessoais.items()}

            # --- Experiência ---
            exp_itens = []
            for item in self.lista_exp:
                emp = item['emp'].get().strip()
                if emp:  # só inclui se empresa preenchida
                    cargo = item['car'].get().strip()
                    periodo = item['per'].get().strip()
                    local = item['loc'].get().strip()
                    bloco = rf"\resumeSubheading{{{self.limpar_latex(emp)}}}{{{self.limpar_latex(cargo)}}}{{{self.limpar_latex(periodo)}}}{{{self.limpar_latex(local)}}}" + "\n"
                    desc_txt = item['desc'].get("1.0", "end-1c").strip()
                    if desc_txt:
                        bloco += r"\begin{itemize}[leftmargin=12pt, label=\textbullet, itemsep=1pt, parsep=1pt]" + "\n"
                        for linha in desc_txt.split('\n'):
                            linha = linha.strip()
                            if linha:
                                bloco += rf"  \resumeItem{{{self.limpar_latex(linha)}}}" + "\n"
                        bloco += r"\end{itemize}" + "\n"
                    exp_itens.append(bloco)
            exp_tex = "\n".join(exp_itens) if exp_itens else r"\item Nenhuma experiência profissional registrada."

            # --- Formação ---
            edu_itens = []
            for item in self.lista_edu:
                curso = item['cur'].get().strip()
                if curso:
                    inst = item['inst'].get().strip()
                    data = item['data'].get().strip()
                    edu_itens.append(rf"\resumeSubheading{{{self.limpar_latex(inst)}}}{{{self.limpar_latex(curso)}}}{{{self.limpar_latex(data)}}}{{}}")
            edu_tex = "\n".join(edu_itens) if edu_itens else r"\item Nenhuma formação acadêmica registrada."

            # --- Habilidades ---
            hab_itens = []
            hab_lines = self.txt_habilidades.get("1.0", "end-1c").strip().split('\n')
            for l in hab_lines:
                if ":" in l:
                    dom, itens = l.split(":", 1)
                    hab_itens.append(rf"\item[{self.limpar_latex(dom.strip())}:] {self.limpar_latex(itens.strip())}")
            hab_tex = "\n".join(hab_itens) if hab_itens else r"\item Nenhuma habilidade registrada."

            # --- Links condicionais ---
            linkedin = p['linkedin']
            github = p['github']
            def format_link(url, texto):
                if not url or url == "#" or url.isspace():
                    return texto
                return rf"\href{{{url}}}{{{texto}}}"
            linkedin_display = format_link(linkedin, "LinkedIn")
            github_display = format_link(github, "GitHub")

            # --- Template ---
            template_base = r"""\documentclass[a4paper,10pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[portuguese]{babel}
\usepackage{lmodern, titlesec, enumitem, microtype}
\usepackage[left=1.2cm, right=1.2cm, top=1.0cm, bottom=1.0cm]{geometry}
\usepackage[hidelinks]{hyperref}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\titleformat{\section}{\bfseries\large}{}{0pt}{\uppercase}
\titlespacing{\section}{0pt}{8pt}{4pt}
\newcommand{\sectionrule}{\vspace{-4pt}\hrule\vspace{5pt}}
\newcommand{\resumeItem}[1]{\item \small #1}
\newcommand{\resumeSubheading}[4]{\item \begin{tabular*}{\textwidth}[t]{l@{\extracolsep{\fill}}r} \textbf{#1} & #3 \\ \textit{\small #2} & \textit{\small #4} \end{tabular*}\vspace{-6pt}}

\begin{document}
\begin{center}
    {\Huge \textbf{VAR_NOME}} \\[5pt]
    \small VAR_LOCAL $|$ \href{mailto:VAR_EMAIL}{VAR_EMAIL} $|$ VAR_FONE \\
    VAR_LINKEDINLINK $|$ VAR_GITHUBLINK
\end{center}

\section{Resumo Profissional} \sectionrule
VAR_RESUMO

\section{Experiência Profissional} \sectionrule
\begin{itemize}[leftmargin=0pt, label={}]
VAR_EXP
\end{itemize}

\section{Habilidades e Tecnologias} \sectionrule
\begin{description}[leftmargin=0pt, font=\bfseries, itemsep=-2pt]
VAR_HAB
\end{description}

\section{Formação Acadêmica} \sectionrule
\begin{itemize}[leftmargin=0pt, label={}]
VAR_EDU
\end{itemize}

\section{Idiomas} \sectionrule
\textbf{VAR_LANG}
\end{document}"""


            final_tex = (template_base
                .replace("VAR_NOME", p['nome'] or "NOME COMPLETO")
                .replace("VAR_LOCAL", p['local'] or "Cidade, Estado")
                .replace("VAR_EMAIL", p['email'] or "email@exemplo.com")
                .replace("VAR_FONE", p['telefone'] or "(00) 00000-0000")
                .replace("VAR_LINKEDINLINK", linkedin_display)
                .replace("VAR_GITHUBLINK", github_display)
                .replace("VAR_RESUMO", self.limpar_latex(self.txt_resumo.get("1.0", "end-1c").strip()) or "Resumo profissional não informado.")
                .replace("VAR_EXP", exp_tex)
                .replace("VAR_HAB", hab_tex)
                .replace("VAR_EDU", edu_tex)
                .replace("VAR_LANG", self.limpar_latex(self.txt_idiomas.get().strip()) or "Idiomas não informados."))

            with open("curriculo.tex", "w", encoding="utf-8") as f:
                f.write(final_tex)


            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "curriculo.tex"],
                capture_output=True, text=True
            )
            if "Error:" in (result.stdout + result.stderr) or result.returncode != 0:
                with open("curriculo_error.log", "w", encoding="utf-8") as log:
                    log.write(result.stdout + "\n" + result.stderr)
                raise Exception("Erro na compilação LaTeX. Verifique 'curriculo_error.log'.")


            for ext in ["aux", "log", "out"]:
                try:
                    os.remove(f"curriculo.{ext}")
                except:
                    pass

            messagebox.showinfo("Sucesso", "PDF gerado com sucesso!\nArquivo: curriculo.pdf")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Erro ao executar pdflatex: {e}\nVerifique se o LaTeX está instalado.")
        except FileNotFoundError:
            messagebox.showerror("Erro", "pdflatex não encontrado. Instale o MiKTeX ou TeX Live.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorCurriculo(root)
    root.mainloop()
