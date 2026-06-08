from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

janela_login = None
funcao_sucesso = None

def verificar_login():
    global janela_login, funcao_sucesso
    
    usuario = janela_login.txt_utilizador.text().strip()
    senha = janela_login.txt_pass.text().strip()
    
    if usuario == "admin" and senha == "12345":
        print("Login correto!")
        janela_login.close()
        if funcao_sucesso:
            funcao_sucesso()
    else:
        print("Erro: Usuário ou Password incorreta!")
        janela_login.txt_pass.clear()

def iniciar_login(ao_sucesso):
    global janela_login, funcao_sucesso
    funcao_sucesso = ao_sucesso
    
    # Carrega o teu ficheiro UI da pasta que queres
    janela_login = uic.loadUi("src/UI/login.xml")
    janela_login.txt_pass.setEchoMode(QtWidgets.QLineEdit.Password)
    
    # CARREGA O LOGOTIPO EVITANDO QUE FIQUE ESTICADO
    pixmap = QPixmap("src/foto/logotipo.png")
    # O truque está no scaled() para respeitar o tamanho real da imagem
    logotipo_redimensionado = pixmap.scaled(350, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    janela_login.lbl_logo.setPixmap(logotipo_redimensionado)
    
    janela_login.btn_entrar.clicked.connect(verificar_login)
    janela_login.show()