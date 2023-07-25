import io
import os
import re
from copy import copy
from datetime import datetime
import textwrap
import tkinter as tk
from tkinter import font
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128

def iniciar_programa():
    
    try:
        # Input da inscrição imobiliária
        inscricao = entry_inscricao.get()
        if not inscricao or inscricao.isalpha() :
            raise ValueError("Por favor, insira uma inscrição imobiliária")
        # Variáveis para armazenar os dados da linha referente à inscrição imobiliária
        numParcelas = 0
        linha = ""
        control = False
        # Busca a linha correspondente à inscrição imobiliária em todos os arquivos do diretório atual
        pasta_dados = "Dados"
        for fname in os.listdir(pasta_dados):
            if os.path.isfile(os.path.join(pasta_dados, fname)):
                with open(os.path.join(pasta_dados, fname), "r", encoding="latin1") as txt_file:
                    for line in txt_file:
                        if inscricao == line[4:24].strip():
                            # Se a linha correspondente for encontrada, armazena a linha e o número de parcelas 
                            print("found string in file %s" % fname)
                            control = True
                            linha = line
                            break
                    if control:
                        txt_file.seek(0)
                        numParcelas = int(txt_file.readline())
                        break
                    txt_file.close()
                    
        if not control:
            raise ValueError("Inscrição imobiliária não encontrada")

        # Abre o arquivo IPTUDigital.pdf e adiciona as informações da capa
        pdf_file = open("Arquivos/IPTUDigital.pdf", "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        # Adiciona os dados da capa
        page = pdf_reader.pages[0]
        packet = io.BytesIO()
        can = canvas.Canvas(packet)

        can.setFont("Helvetica-Bold", 6)
        can.drawString(355, 70, "Inscrição imobiliária: " + linha[4:24].strip())  # Inscrição
        can.drawString(355, 62, "Cadastro imobiliário: " + linha[24:30].strip())  # Cadastro

        can.setFont("Helvetica", 6)  # Destinatario
        can.drawString(355, 54, linha[30:90].strip())
        can.drawString(355, 46, linha[260:320].strip() + " " + linha[320:340].strip())
        can.drawString(355, 38, linha[340:365].strip())
        can.drawString(355, 30, linha[392:400].strip() + " - " + linha[365:390].strip() + " - " + linha[390:392].strip())

        can.save()
        packet.seek(0)
        overlay = PyPDF2.PdfReader(packet)
        page.merge_page(overlay.pages[0])
        pdf_writer.add_page(page)

        # Adiciona a página de mensagem
        pdf_writer.add_page(pdf_reader.pages[1])

        # Adiciona os dados da notificação de lançamento
        page = pdf_reader.pages[2]
        packet = io.BytesIO()
        can = canvas.Canvas(packet)

        can.setFont("Helvetica", 7)
        can.drawString(30, 205, linha[30:90].strip())  # Contribuinte

        can.setFont("Helvetica", 6)
        can.drawString(30, 189, linha[130:190].strip() + " " + linha[190:210].strip())  # Endereço imóvel
        can.drawString(30, 182, linha[210:230].strip())
        can.drawString(30, 175, linha[230:260].strip())
        can.drawString(30, 78, linha[260:320].strip() + " " + linha[320:340].strip())  # Endereço do beneficiário
        can.drawString(30, 71, linha[340:365].strip())
        can.drawString(30, 64, linha[392:400].strip() + " - " + linha[365:390].strip() + " - " + linha[390:392].strip())
        can.drawRightString(254, 112, linha[230:250].strip())   # Loteamento
        can.drawRightString(100, 25, linha[2328:2348].strip())  # Número do documento P1
        can.drawRightString(177, 25, linha[1794:1814].strip())  # Número do documento cota única 2
        can.drawRightString(254, 25, linha[1528:1548].strip())  # Número do documento cota única 1

        can.setFont("Helvetica", 5)
        can.drawString(376, 177, linha[1128:1158].strip())  # Tipo imposto
        can.drawString(376, 159, linha[1180:1195].strip())  # Cosip/Coleta

        can.setFont("Helvetica", 8)
        can.drawRightString(100, 132, linha[400:414].strip())   # Testada principal
        can.drawRightString(177, 132, linha[485:499].strip())   # Área edificada
        can.drawRightString(254, 132, linha[442:456].strip())   # Valor m2
        can.drawRightString(100, 112, linha[428:442].strip())   # Área do terreno
        can.drawRightString(177, 112, linha[545:559].strip())   # Valor venal da construção
        can.drawRightString(100, 92, linha[470:484].strip())    # Valor venal do terreno
        can.drawRightString(177, 92, linha[559:573].strip())    # Valor venal do imóvel
        can.drawRightString(215, 92, linha[251:255].strip())    # Quadra
        can.drawRightString(254, 92, linha[256:260].strip())    # Lote
        can.drawRightString(465, 205, linha[559:573].strip())   # Valor Imóvel
        can.drawRightString(465, 187, linha[587:601].strip())   # Aliquota
        can.drawRightString(465, 169, linha[1166:1180].strip()) # Valor imposto
        can.drawRightString(465, 151, linha[1200:1214].strip()) # Valor Cosip/Coleta
        can.drawRightString(565, 205, linha[4:24].strip())      # Inscrição
        can.drawRightString(565, 187, linha[24:30].strip())     # Código do conveniado
        can.drawRightString(565, 168, linha[2328:2348].strip()) # Nosso número parcela 1
        can.drawRightString(565, 150, linha[1794:1814].strip()) # Nosso número 2 cota única
        can.drawRightString(565, 131, linha[1528:1548].strip()) # Nosso número 1 cota única

        can.setFont("Helvetica-Bold", 8)
        can.drawString(328, 175, linha[1742:1752].strip())  # 1 única vencimento
        can.drawString(328, 163, linha[2008:2018].strip())  # 2 única vencimento
        can.drawString(328, 151, linha[2351:2361].strip())  # 1 parcela vencimento
        can.drawString(328, 139, linha[2591:2601].strip())  # 2 parcela vencimento
        can.drawString(328, 127, linha[2831:2841].strip())  # 3 parcela vencimento
        can.drawString(328, 115, linha[3071:3081].strip())  # 4 parcela vencimento
        can.drawString(328, 103, linha[3311:3321].strip())  # 5 parcela vencimento
        can.drawString(328, 91, linha[3551:3561].strip())   # 6 parcela vencimento
        can.drawString(328, 79, linha[3791:3801].strip())   # 7 parcela vencimento
        can.drawString(328, 67, linha[4031:4041].strip())   # 8 parcela vencimento
        can.drawString(328, 55, linha[4271:4281].strip())   # 9 parcela vencimento

        if linha[1742:1752].strip() != "":  # Nome parcelas
            can.drawString(262, 175, "1ª Única")  # 1 Única
        if linha[2008:2018].strip() != "":
            can.drawString(262, 163, "2ª Única")  # 2 Única
        for j in range(9):
            if linha[2351 + j * 240 : 2361 + j * 240].strip() != "":
                can.drawString(262, 151 + j * -12, str(j + 1) + "ª Parcela")  # Parcelas
                
        can.setFont("Helvetica-Bold", 9)
        can.drawRightString(565, 111, linha[2501:2515].strip())   # Valor parcela 1
        can.drawRightString(565, 92.3, linha[1983:1997].strip())  # Valor 2 cota única
        can.drawRightString(565, 73.7, linha[1717:1731].strip())  # Valor 1 cota única

        can.setFont("Helvetica-Bold", 10)
        can.drawRightString(465, 33, linha[1514:1528].strip())  # Valor total

        can.save()
        packet.seek(0)
        overlay = PyPDF2.PdfReader(packet)
        page.merge_page(overlay.pages[0])
        pdf_writer.add_page(page)

        # Adiciona os dados das cotas unicas
        for i in range(0, 2):
            page = copy(pdf_reader.pages[i + 3])
            packet = io.BytesIO()
            can = canvas.Canvas(packet)
            d = 266
            
            valor = float(linha[1717 + i * d : 1737 + i * d].strip().replace(",", "."))
            valor_formatado = "{:.2f}".format(round(valor, 2))
            
            can.setFont("Helvetica-Bold", 7)
            can.drawRightString(44, 215, str(i + 1) + "ª Única")  # Parcela
            
            can.setFont("Helvetica", 7)
            can.drawRightString(92, 36, linha[1528 + i * d : 1548 + i * d].strip())  # Número do Documento
            can.drawRightString(92, 20, linha[1528 + i * d : 1548 + i * d].strip())  # Nosso número
            
            can.setFont("Helvetica-Bold", 8)
            can.drawRightString(92, 215, linha[1742 + i * d : 1752 + i * d].strip()) # Vencimento
            can.drawRightString(92, 181, valor_formatado.replace(".", ","))  # Valor
            
            can.setFont("Helvetica", 8)
            can.drawRightString(92, 198, "5414–3/19550–2")  # Agência
            
            can.setFont("Helvetica", 4.8)
            pagador = (linha[30:90].strip() + " - CPF/CNPJ: " + linha[90:130].strip() + " " + linha[260:320].strip() + " " + linha[320:340].strip() + " - "
                + linha[340:365].strip() + " " + linha[392:400].strip() + " - " + linha[365:390].strip() + " - " + linha[390:392].strip())
            max_line_width = 26
            x, y = 16, 105
            palavras = re.findall(r"\S+\s*", pagador)
            linhas = textwrap.wrap("".join(palavras), max_line_width)
            for linha_texto in linhas:
                can.drawString(x, y, linha_texto)
                y -= 5
                
            can.setFont("Helvetica-Bold", 10)
            can.drawRightString(511, 230, str(i + 1) + "ª Única")   # Parcela
            can.drawRightString(578, 230, linha[1742 + i * d : 1752 + i * d].strip())   # Vencimento
            can.drawRightString(578, 175, valor_formatado.replace(".", ","))   # Valor
            
            can.setFont("Helvetica", 8)
            can.drawRightString(578, 212, "5414–3/19550–2")  # Agência
            can.drawRightString(578, 193, linha[1528 + i * d : 1548 + i * d].strip()) # Nosso Número
            can.drawRightString(180, 193, datetime.now().strftime("%d/%m/%Y"))  # Data de emissão
            can.drawRightString(288, 193, linha[1528 + i * d : 1548 + i * d].strip())   # Número do Documento
            can.drawRightString(340, 193, "DV") # Espécie
            can.drawRightString(375, 193, "N")  # Aceite
            can.drawRightString(455, 193, datetime.now().strftime("%d/%m/%Y"))  # Data de processamento
            
            can.setFont("Helvetica", 5.8)
            can.drawString(165, 78, linha[30:90].strip() + " - CPF/CNPJ: " + linha[90:130].strip())    # Pagador
            can.drawString(165, 71, linha[260:320].strip() + " " + linha[320:340].strip() + " - " + linha[340:365].strip())    # Pagador
            can.drawString(165, 64, linha[392:400].strip() + " - " + linha[365:390].strip() + " - " + linha[390:392].strip())  # Pagador
            
            can.setFont("Helvetica-Bold", 13.5)
            can.drawString(200, 250, linha[5845 + i * 170 : 5903 + i * 170].strip())    # LD
            barcode = code128.Code128(linha[5845 + i * 170 : 5903 + i * 170].strip().replace(".","").replace(" ", ""), barHeight=36, barWidth = .95)
            barcode.drawOn(can, 90, 10)
            
            can.save()
            packet.seek(0)
            overlay = PyPDF2.PdfReader(packet)
            page.merge_page(overlay.pages[0])
            pdf_writer.add_page(page)

        # Adiciona os dados das parcelas
        for i in range(0, numParcelas):
            page = copy(pdf_reader.pages[5])
            packet = io.BytesIO()
            can = canvas.Canvas(packet)
            d = 240
            
            valor = float(linha[2501 + i * d : 2521 + i * d].strip().replace(",", "."))
            valor_formatado = "{:.2f}".format(round(valor, 2))
            
            can.setFont("Helvetica-Bold", 7)
            can.drawRightString(44, 215, "{:02d}".format(i + 1) + "/" + "{:02d}".format(numParcelas))  # Parcela
            
            can.setFont("Helvetica", 7)
            can.drawRightString(92, 36, linha[2328 + i * d : 2348 + i * d].strip())  # Número do Documento
            can.drawRightString(92, 20, linha[2328 + i * d : 2348 + i * d].strip())  # Nosso número
            
            can.setFont("Helvetica-Bold", 8)
            can.drawRightString(92, 215, linha[2351 + i * d : 2361 + i * d].strip()) # Vencimento
            can.drawRightString(92, 181, valor_formatado.replace(".", ","))  # Valor
            
            can.setFont("Helvetica", 8)
            can.drawRightString(92, 198, "5414–3/19550–2")  # Agência
            
            can.setFont("Helvetica", 4.8)
            pagador = (linha[30:90].strip() + " - CPF/CNPJ: " + linha[90:130].strip() + " " + linha[260:320].strip() + " " + linha[320:340].strip() + " - "
                + linha[340:365].strip() + " " + linha[392:400].strip() + " - " + linha[365:390].strip() + " - " + linha[390:392].strip())
            max_line_width = 26
            x, y = 16, 105
            palavras = re.findall(r"\S+\s*", pagador)
            linhas = textwrap.wrap("".join(palavras), max_line_width)
            for linha_texto in linhas:
                can.drawString(x, y, linha_texto)
                y -= 5
                
            can.setFont("Helvetica-Bold", 10)
            can.drawRightString(511, 230, "{:02d}".format(i + 1) + "/" + "{:02d}".format(numParcelas))   # Parcela
            can.drawRightString(578, 230, linha[2351 + i * d : 2361 + i * d].strip())   # Vencimento
            can.drawRightString(578, 175, valor_formatado.replace(".", ","))   # Valor
            
            can.setFont("Helvetica", 8)
            can.drawRightString(578, 212, "5414–3/19550–2")  # Agência
            can.drawRightString(578, 193, linha[2328 + i * d : 2348 + i * d].strip()) # Nosso Número
            can.drawRightString(180, 193, datetime.now().strftime("%d/%m/%Y"))  # Data de emissão
            can.drawRightString(288, 193, linha[2328 + i * d : 2348 + i * d].strip())   # Número do Documento
            can.drawRightString(340, 193, "DV") # Espécie
            can.drawRightString(375, 193, "N")  # Aceite
            can.drawRightString(455, 193, datetime.now().strftime("%d/%m/%Y"))  # Data de processamento
            
            can.setFont("Helvetica", 5.8)
            can.drawString(165, 78, linha[30:90].strip() + " - CPF/CNPJ: " + linha[90:130].strip())    # Pagador
            can.drawString(165, 71, linha[260:320].strip() + " " + linha[320:340].strip() + " - " + linha[340:365].strip())    # Pagador
            can.drawString(165, 64, linha[392:400].strip() + " - " + linha[365:390].strip() + " - " + linha[390:392].strip())  # Pagador
            
            can.setFont("Helvetica-Bold", 13.5)
            can.drawString(200, 250, linha[6355 + i * 170 : 6413 + i * 170].strip())    # LD
            barcode = code128.Code128(linha[6355 + i * 170 : 6413 + i * 170].strip().replace(".","").replace(" ", ""), barHeight=36, barWidth = .95)
            barcode.drawOn(can, 90, 10)
            
            can.save()
            packet.seek(0)
            overlay = PyPDF2.PdfReader(packet)
            page.merge_page(overlay.pages[0])
            pdf_writer.add_page(page)

        pdf_writer.add_page(pdf_reader.pages[6])  # INFORMAÇÕES
        pdf_writer.add_page(pdf_reader.pages[7])  # CONTRACAPA

        # salvar o PDF em um arquivo na pasta superior
        pdf_output_path = "../pdfFinal.pdf"  # caminho para o arquivo na pasta superior
        with open(pdf_output_path, "wb") as pdf_output_file:
            pdf_writer.write(pdf_output_file)
        status_label.configure(text="PDF gerado com sucesso!") # atualiza o label de status
    except ValueError as e:
        # Exibe uma mensagem de erro na label de status
        status_label.configure(text=str(e))

#Criando janela do aplicativo
janela = tk.Tk()
janela.title("IPTU Digital")

# Define a cor de fundo da janela
janela.configure(bg='#FFFFFF')

# Define as dimensões da janela e centraliza na tela
largura_janela = 540
altura_janela = 100
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
posx = largura_tela/2 - largura_janela/2
posy = altura_tela/2 - altura_janela/2
janela.geometry("%dx%d+%d+%d" % (largura_janela, altura_janela, posx, posy))

# Adiciona ícone à janela
icone = tk.PhotoImage(file='Arquivos/icone.png')
janela.iconphoto(True, icone)

# Usa uma fonte mais moderna para o texto
fonte = font.Font(family='Helvetica', size=12)

# Cria o campo de entrada
label_inscricao = tk.Label(janela, text="Inscrição Cadastral:", font=fonte, bg='#FFFFFF')
label_inscricao.grid(row=0, column=0, padx=10, pady=12, sticky='w')
entry_inscricao = tk.Entry(janela, font=fonte)
entry_inscricao.grid(row=0, column=1, padx=10, pady=12, sticky='we')

# Cria o botão
botao_buscar = tk.Button(janela, text="Gerar", command=iniciar_programa, font=fonte, bg='#64B864', fg='#FFFFFF', bd=0, relief='flat', activebackground='#5CAF5C', activeforeground='#FFFFFF', cursor='hand2')
botao_buscar.grid(row=0, column=2, padx=12, pady=12, sticky='e')
botao_buscar.configure(width=8, height=1, highlightthickness=0, bd=0, pady=5)
botao_buscar.bind("<Enter>", lambda event, h=botao_buscar: h.config(bg="#5CAF5C"))
botao_buscar.bind("<Leave>", lambda event, h=botao_buscar: h.config(bg="#64B864"))

# Cria o label de status
status_label = tk.Label(janela, text="", font=fonte, bg='#FFFFFF')
status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0,10))

# Executa o loop da janela
janela.mainloop()