from checkout_monolitico import (pedido, FreteNormal, FreteExpresso,CheckoutFacade,PagamentoPix,PagamentoCredito)


if __name__ == "__main__":

    fachada = CheckoutFacade()
    
    itens_sucesso = [
        {'nome': 'capa da invisibilidade', 'valor': 150.00},
        {'nome': 'poção de voo', 'valor': 80.00}
    ]

    print(" \n *******************************************************")
    print("\ CENARIO 1: SUCESSO \n")


    pedido1 = pedido(
        itens = itens_sucesso,
        estrategia_pagamento = PagamentoPix(),
        estrategia_frete = FreteNormal()
    )

    fachada.concluir_transacao(pedido1)

    itens_falha = [
        {'nome': 'castelo magico', 'preco': 1200.00, 'quantidade': 1},
        {'nome': 'item raro indisponivel', 'preco': 5.0, 'quantidade': 1}
    ]

    print(" \n *******************************************************")
    print("\ CENARIO 2: FALHA \n")


    itens2 = pedido [
        {'nome': 'Cristal Mágico', 'valor': 600.00}
    ]

    pedido2 = pedido(
        itens = itens_falha,
        estrategia_pagamento = PagamentoCredito(),
        estrategia_frete = FreteExpresso()
    )
    fachada.concluir_transacao(pedido2)

    print("\n--- Próximo Pedido ---\n") 










    



