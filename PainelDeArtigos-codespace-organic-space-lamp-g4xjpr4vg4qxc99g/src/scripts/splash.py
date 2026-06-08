from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

# Variáveis globais
tela_splash = None
contador = 0
timer = None
funcao_terminar = None
funcao_dados = None

def animar_carregamento():
    global contador, timer, tela_splash, funcao_terminar, funcao_dados
    
    # contador 
    contador += 5
    if contador == 25:
        tela_splash.lbl_loading.setText("A CONECTAR À BASE DE DADOS...")
    elif contador == 50:
        tela_splash.lbl_loading.setText("A CARREGAR PRODUTOS...")
        if funcao_dados:
            funcao_dados() # Carrega os dados da BD
    elif contador == 75:
        tela_splash.lbl_loading.setText("BEM VINDO")
        
    # Quando chega ao fim, para o timer e fecha a janela
    if contador >= 100:
        timer.stop()
        tela_splash.close()
        if funcao_terminar:
            funcao_terminar() 
   

def iniciar_splash(funcao_ao_terminar, funcao_carregar_dados):
    global tela_splash, timer, funcao_terminar, funcao_dados, contador
    
    funcao_terminar = funcao_ao_terminar
    funcao_dados = funcao_carregar_dados
    contador = 0
    
    tela_splash = uic.loadUi("src/UI/splash.xml")
    
    # tela tranparente
    tela_splash.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    tela_splash.setAttribute(Qt.WA_TranslucentBackground)
    
    pixmap = QPixmap("src/foto/logotipo.png")
    tela_splash.lbl_foto.setPixmap(pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    
    # tempo
    timer = QTimer()
    timer.timeout.connect(animar_carregamento) # Agora o editor já a conhece em cima!
    timer.start(100)
    
    tela_splash.show()