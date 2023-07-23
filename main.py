# Arquivo main.py
from jogo import Jogo

if __name__ == "__main__":
    jogo = Jogo()
    jogo.tela_inicial()
    aviao_x = jogo.largura_tela // 20
    aviao_y = jogo.altura_tela // 2
    obstaculo_x, obstaculo_y, obstaculo_imagem = jogo.gerar_inimigo()
    jogo.jogo(aviao_x, aviao_y, obstaculo_x, obstaculo_y)
