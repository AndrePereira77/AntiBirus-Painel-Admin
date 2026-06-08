import sys
from PyQt5 import QtWidgets

# IMPORTAÇÕES DOS TEUS SCRIPTS DE FLUXO E DA CONEXÃO
from src.db.connect import conn
from src.scripts.splash import iniciar_splash
from src.scripts.login import iniciar_login
from src.scripts.dashboard import iniciar_dashboard

def fechar_programa():
    # Verifica se a conexão existe antes de fechar
    if conn and conn.is_connected():
        conn.close()
    app.quit()

# ==========================================
# FLUXO DAS JANELAS
# ==========================================
def ir_para_login():
    """ Abre a tela de login assim que o Splash Screen termina """
    iniciar_login(ao_sucesso=ir_para_dashboard)

def ir_para_dashboard():
    """ Abre o painel e passa a conexão importada do connect.py """
    iniciar_dashboard(conn)

# ==========================================
# INICIALIZAÇÃO DO PROGRAMA
# ==========================================
app = QtWidgets.QApplication(sys.argv)
app.aboutToQuit.connect(fechar_programa)

# Arranca o Splash Screen
iniciar_splash(funcao_ao_terminar=ir_para_login, funcao_carregar_dados=None)

sys.exit(app.exec_())