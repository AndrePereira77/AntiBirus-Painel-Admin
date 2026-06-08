from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QDateTime
from mysql.connector import Error

janela = None
conexao_bd = None
timer_relogio = None

def atualizar_relogio():
    """ Atualiza a label com o dia da semana, data e hora em tempo real """
    agora = QDateTime.currentDateTime()
    # Formato moderno em português europeu completo
    texto_data_hora = agora.toString("dddd, dd/MM/yyyy - HH:mm:ss")
    janela.lbl_relogio.setText(texto_data_hora)

def abrir_empresa():
    QMessageBox.information(janela, "Empresa", "🏢 ANTI BIRUS \n\nSistema Central de Gestão de Inventário e Distribuição de Equipamentos.")

def abrir_como_usar():
    QMessageBox.warning(janela, "Como Usar", "❌ Estado: Indisponível.")

def abrir_suporte():
    QMessageBox.information(janela, "Suporte Técnico", "🛠️ Apoio ao Cliente\n\nStatus: Brevemente.")

def abrir_creditos():
    QMessageBox.about(janela, "Créditos do Sistema", "👥 Desenvolvedores (DEVs):\n\n• André\n• Renato\n\nConstruído com Python e PyQt5 - 2026.")

def carregar_dados_tabela():
    try:
        cursor = conexao_bd.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos")
        linhas = cursor.fetchall()
       
        janela.tabela_produtos.setRowCount(len(linhas))
        janela.tabela_produtos.setHorizontalHeaderLabels(["ID", "Nome", "Categoria", "Preço", "Stock"])
       
        for num_linha, linha in enumerate(linhas):
            janela.tabela_produtos.setItem(num_linha, 0, QTableWidgetItem(str(linha['id_produto'])))
            janela.tabela_produtos.setItem(num_linha, 1, QTableWidgetItem(linha['nome']))
            janela.tabela_produtos.setItem(num_linha, 2, QTableWidgetItem(linha['categoria']))
            janela.tabela_produtos.setItem(num_linha, 3, QTableWidgetItem(f"{linha['preco']} €"))
            janela.tabela_produtos.setItem(num_linha, 4, QTableWidgetItem(str(linha['quantidade'])))
           
        cursor.close()
    except Error as err:
        print(f"Erro ao carregar tabela: {err}")

def adicionar_produto():
    nome = janela.txt_nome.text().strip()
    categoria = janela.cb_categoria.currentText()
    preco = janela.txt_preco.text().replace(',', '.')
    qtd = janela.txt_qtd.value()
   
    if not nome or not preco:
        QMessageBox.warning(janela, "Campos Vazios", "Por favor, preencha o Nome e o Preço!")
        return

    try:
        cursor = conexao_bd.cursor()
        sql = "INSERT INTO produtos (nome, categoria, preco, quantidade) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, categoria, float(preco), int(qtd)))
        conexao_bd.commit()
        cursor.close()
       
        janela.txt_nome.setText("")
        janela.txt_preco.setText("")
        janela.txt_qtd.setValue(0)
        carregar_dados_tabela()
    except (Error, ValueError) as err:
        print(f"Erro ao salvar: {err}")

def alterar_stock(quantidade_mudanca):
    linha_selecionada = janela.tabela_produtos.currentRow()
   
    if linha_selecionada == -1:
        QMessageBox.warning(janela, "Seleção Necessária", "Selecione um produto na tabela antes de alterar o stock!")
        return
       
    id_produto = janela.tabela_produtos.item(linha_selecionada, 0).text()
   
    try:
        cursor = conexao_bd.cursor()
        sql = """UPDATE produtos
                 SET quantidade = GREATEST(0, quantidade + %s)
                 WHERE id_produto = %s"""
        cursor.execute(sql, (quantidade_mudanca, id_produto))
        conexao_bd.commit()
        cursor.close()
       
        carregar_dados_tabela()
    except Error as err:
        print(f"Erro ao atualizar stock: {err}")

def iniciar_dashboard(conn):
    global janela, conexao_bd, timer_relogio
    conexao_bd = conn
    
    janela = uic.loadUi("src/UI/dashboard.xml")
    
    # ATIVAR FULL SCREEN AUTOMÁTICO
    janela.showFullScreen()
    
    # Tornar a tabela fluída e elástica para ecrãs grandes
    janela.tabela_produtos.setSelectionBehavior(QAbstractItemView.SelectRows)
    janela.tabela_produtos.setSelectionMode(QAbstractItemView.SingleSelection)
    janela.tabela_produtos.horizontalHeader().setStretchLastSection(True)
    janela.tabela_produtos.verticalHeader().setVisible(False)
    janela.tabela_produtos.verticalHeader().setDefaultSectionSize(40)
    
    # Ligar os novos botões da Barra Lateral às respetivas ações
    janela.btn_menu_empresa.clicked.connect(abrir_empresa)
    janela.btn_menu_como_usar.clicked.connect(abrir_como_usar)
    janela.btn_menu_suporte.clicked.connect(abrir_suporte)
    janela.btn_menu_creditos.clicked.connect(abrir_creditos)
    
    # Ações Principais
    janela.btn_adicionar.clicked.connect(adicionar_produto)
    janela.btn_vender.clicked.connect(lambda: alterar_stock(-1))
    janela.btn_repor.clicked.connect(lambda: alterar_stock(1))
    
    # ATIVAR E CONFIGURAR RELÓGIO (QTimer)
    timer_relogio = QTimer()
    timer_relogio.timeout.connect(atualizar_relogio)
    timer_relogio.start(1000)  # Atualiza a cada 1 segundo (1000ms)
    atualizar_relogio()        # Corre a primeira vez imediato
    
    carregar_dados_tabela()
    
    # Foto enquadrada de forma fixa no retângulo reservado da barra lateral
    pixmap = QPixmap("src/foto/Foto_Painel.png")
    foto_redimensionada = pixmap.scaled(220, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    janela.lbl_foto_painel.setPixmap(foto_redimensionada)
    
    janela.show()