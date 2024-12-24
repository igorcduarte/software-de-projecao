import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from projecao import projetar_estrofes

# Cor base para o tema
COR_BASE = "#27115A"
COR_CONTRASTE = "#FFFFFF"
COR_BOTAO = "#3D2C8D"
COR_TEXTO = "#E0E0E0"

class ProjecaoApp:
    def __init__(self):
        self.letras_salvas = {}
        self.janela = tk.Tk()
        self.janela.title("Projeção de Letras")
        self.janela.geometry("1000x800")
        self.janela.resizable(True, True)
        self.janela.minsize(800, 600)
        self.janela.configure(bg=COR_BASE)
        
        self.criar_interface()

    def criar_interface(self):
        # Divisão principal
        self.frame_principal = tk.PanedWindow(self.janela, orient=tk.HORIZONTAL, bg=COR_BASE)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Aba lateral para letras salvas
        self.frame_letras = tk.Frame(self.frame_principal, bg=COR_BASE)
        self.frame_principal.add(self.frame_letras, width=200)

        # Label para lista de letras
        self.label_lista = tk.Label(self.frame_letras, text="Letras Salvas", bg=COR_BASE, 
                                  fg=COR_CONTRASTE, font=("Arial", 14, "bold"))
        self.label_lista.pack(pady=5)

        # Lista de letras
        self.lista_letras = tk.Listbox(self.frame_letras, bg=COR_BASE, fg=COR_TEXTO, 
                                     selectbackground=COR_BOTAO, font=("Arial", 12))
        self.lista_letras.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lista_letras.bind('<<ListboxSelect>>', self.mostrar_letra_selecionada)

        # Botões
        self.btn_projetar = tk.Button(self.frame_letras, text="Projetar", 
                                    command=self.projetar_selecionada, bg=COR_BOTAO, 
                                    fg=COR_CONTRASTE, font=("Arial", 12))
        self.btn_projetar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.btn_excluir = tk.Button(self.frame_letras, text="Excluir Letra", 
                                   command=self.excluir_letra, bg=COR_BOTAO, 
                                   fg=COR_CONTRASTE, font=("Arial", 12))
        self.btn_excluir.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.btn_criar = tk.Button(self.frame_letras, text="Criar Letra", 
                                 command=self.abrir_janela_criacao, bg=COR_BOTAO, 
                                 fg=COR_CONTRASTE, font=("Arial", 12))
        self.btn_criar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Área de visualização
        self.frame_visualizacao = tk.Frame(self.frame_principal, bg=COR_BASE)
        self.frame_principal.add(self.frame_visualizacao)

        # Label para título da visualização
        self.label_visualizacao = tk.Label(self.frame_visualizacao, text="Visualização da Letra", 
                                         bg=COR_BASE, fg=COR_CONTRASTE, font=("Arial", 14, "bold"))
        self.label_visualizacao.pack(pady=5)

        # Texto para visualização
        self.texto_visualizacao = tk.Text(self.frame_visualizacao, wrap=tk.WORD, 
                                        bg=COR_BASE, fg=COR_TEXTO, font=("Arial", 12))
        self.texto_visualizacao.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def mostrar_letra_selecionada(self, event=None):
        try:
            if self.lista_letras.curselection():
                selecionado = self.lista_letras.get(self.lista_letras.curselection())
                if selecionado in self.letras_salvas:
                    self.texto_visualizacao.delete(1.0, tk.END)
                    self.texto_visualizacao.insert(1.0, self.letras_salvas[selecionado])
        except Exception as e:
            print(f"Erro ao mostrar letra: {e}")

    def atualizar_lista_letras(self):
        self.lista_letras.delete(0, tk.END)
        for nome in self.letras_salvas:
            self.lista_letras.insert(tk.END, nome)

    def projetar_selecionada(self):
        try:
            selecionado = self.lista_letras.get(self.lista_letras.curselection())
            projetar_estrofes(self.letras_salvas[selecionado])
        except tk.TclError:
            messagebox.showwarning("Aviso", "Nenhuma letra foi selecionada para projeção!")

    def excluir_letra(self):
        try:
            selecionado = self.lista_letras.get(self.lista_letras.curselection())
            del self.letras_salvas[selecionado]
            self.atualizar_lista_letras()
            self.texto_visualizacao.delete(1.0, tk.END)
            messagebox.showinfo("Sucesso", f"Letra '{selecionado}' excluída com sucesso!")
        except tk.TclError:
            messagebox.showwarning("Aviso", "Nenhuma letra foi selecionada para exclusão!")

    def abrir_janela_criacao(self):
        janela_criacao = tk.Toplevel(self.janela)
        janela_criacao.title("Criar Letra")
        janela_criacao.geometry("1000x800")
        janela_criacao.resizable(True, True)
        janela_criacao.minsize(800, 600)
        janela_criacao.configure(bg=COR_BASE)
        janela_criacao.transient(self.janela)
        janela_criacao.grab_set()

        def salvar_letra():
            nome = nome_entrada.get()
            if not nome:
                messagebox.showwarning("Aviso", "Insira um nome para salvar a letra!")
                return
            
            self.letras_salvas[nome] = texto_letra.get(1.0, tk.END).strip()
            messagebox.showinfo("Sucesso", f"Letra '{nome}' salva com sucesso!")
            self.atualizar_lista_letras()
            janela_criacao.destroy()

        def importar_letra():
            arquivo = filedialog.askopenfilename(
                title="Selecione o arquivo de letras",
                filetypes=[("Arquivos de Texto", "*.txt")]
            )
            if arquivo:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    texto_letra.delete(1.0, tk.END)
                    texto_letra.insert(tk.END, f.read())

        def organizar_estrofes():
            texto = texto_letra.get(1.0, tk.END).strip()
            linhas = texto.split("\n")
            estrofes = ["\n".join(linhas[i:i+4]) for i in range(0, len(linhas), 4)]
            texto_letra.delete(1.0, tk.END)
            texto_letra.insert(tk.END, "\n\n".join(estrofes))

        # Nome da letra
        nome_entrada = tk.Entry(janela_criacao, font=("Arial", 14), bg=COR_BOTAO, fg=COR_CONTRASTE)
        nome_entrada.pack(fill=tk.X, padx=10, pady=10)
        nome_entrada.insert(0, "Nome da Letra")

        # Texto da letra
        texto_letra = tk.Text(janela_criacao, wrap=tk.WORD, font=("Arial", 14), 
                            bg=COR_BASE, fg=COR_TEXTO, insertbackground=COR_CONTRASTE)
        texto_letra.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Barra de ferramentas
        barra_ferramentas = tk.Frame(janela_criacao, bg=COR_BASE)
        barra_ferramentas.pack(side=tk.BOTTOM, fill=tk.X)

        btn_importar = tk.Button(barra_ferramentas, text="Importar", command=importar_letra, 
                               bg=COR_BOTAO, fg=COR_CONTRASTE, font=("Arial", 12))
        btn_importar.pack(side=tk.LEFT, padx=5, pady=5)

        btn_organizar = tk.Button(barra_ferramentas, text="Organizar Estrofes", 
                                command=organizar_estrofes, bg=COR_BOTAO, 
                                fg=COR_CONTRASTE, font=("Arial", 12))
        btn_organizar.pack(side=tk.LEFT, padx=5, pady=5)

        btn_salvar = tk.Button(barra_ferramentas, text="Salvar", command=salvar_letra, 
                             bg=COR_BOTAO, fg=COR_CONTRASTE, font=("Arial", 12))
        btn_salvar.pack(side=tk.LEFT, padx=5, pady=5)

    def executar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = ProjecaoApp()
    app.executar()