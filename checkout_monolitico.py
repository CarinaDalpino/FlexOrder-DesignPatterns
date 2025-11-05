
from abc import ABC, abstractmethod

# interfaces


class EstrategiaFrete(ABC):
    """Lógica de frete acoplada e com ifs aninhados."""
    @abstractmethod
    def calcular_frete(self, valor_com_desconto: float) -> float:
        pass


class EstrategiaPagamento(ABC):
    """Lógica de pagamento acoplada e com ifs aninhados."""
    @abstractmethod
    def processar_pagamento(self, valor_final: float) -> bool:
        pass


# pagamento


class PagamentoCredito(EstrategiaPagamento):
    def processar_pagamento(self, valor_final):
        print(f"Processando R${valor_final:.2f} via Cartão de Crédito...")
        # Chamada direta e acoplada a um subsistema imaginário
        if valor_final < 1000:
            print("   -> Pagamento com Credito APROVADO.")
            return True
        else:
            print("   -> Pagamento com Credito REJEITADO (limite excedido).")
            return False


class PagamentoPix(EstrategiaPagamento):
    def processar_pagamento(self, valor_final):
        print(f"Processando R${valor_final:.2f} via PIX...")
        print("   -> Pagamento com PIX APROVADO (QR Code gerado).")
        return True

 # Frete VIP - Lógica de cálculo bizarra (precisa de lib externa)


class PagamentoMana(EstrategiaPagamento):
    def processar_pagamento(self, valor_final):
        print(f"Processando R${valor_final:.2f} via Transferência de Mana...")
        print("   -> Pagamento com Mana APROVADO (requer 10 segundos de espera).")
        return True


# frete

class FreteNormal(EstrategiaFrete):
    def calcular_frete(self, valor_com_desconto):
        custo_frete = valor_com_desconto * 0.05
        print(f"Frete Normal: R${custo_frete:.2f}")
        return custo_frete


class FreteExpresso(EstrategiaFrete):
    def calcular_frete(self, valor_com_desconto):
        custo_frete = valor_com_desconto * 0.10 + 15.00  # Taxa extra
        print(f"Frete Expresso (com taxa): R${custo_frete:.2f}")
        return custo_frete


class FreteTeletransporte(EstrategiaFrete):
    def calcular_frete(self, valor_com_desconto):
        custo_frete = 50.00
        print(f"Frete Teletransporte: R${custo_frete:.2f}")
        return custo_frete


# pedido novo

class Pedido:
    def __init__(self, itens: list, metodo_pagamento: EstrategiaPagamento, estrategia_frete: EstrategiaFrete):
        self.itens = itens
        self.metodo_pagamento = metodo_pagamento
        self.estrategia_frete = estrategia_frete
        self.tipo_frete = estrategia_frete
        self.embalagem = "padrao"
        self.valor_base = sum(
            itens['preco'] * itens['quantidade'] for itens in itens)

    def aplicar_desconto(self):
       self.valor_desconto = self.valor_base
       nome_estrategia = self.metodo_pagamento.__class__.__name__

       if nome_estrategia == "PagamentoPix":
           self.valor_desconto *= 0.95
           print(
               f"desconto de 10% aplicado via pix: R${self.valor_desconto:.2f}")
           
       elif self.valor_total > 500:
           print(
               f"desconto de 10% aplicado para pedidos grandes: R${self.valor_desconto:.2f}")
           self.valor_desconto *= 0.95
           
       return self.valor_desconto
    
    def compra_final(self):
       valor_desconto = self.aplicar_desconto()
       custo_frete = self.estrategia_frete.calcular_frete(valor_desconto)
       valor_final = valor_desconto + custo_frete
       print(f"Valor final do pedido: R${valor_final:.2f}")
       secesso_pagamento = self.metodo_pagamento.processar_pagamento(valor_final)
       return secesso_pagamento


##pedido base


class calcular_valor(ABC):
    @abstractmethod
    def calcular_valor_final(self) -> float:
        pass

    @abstractmethod
    def detalhes_pedido(self) -> str:
        pass


class PedidoBase(calcular_valor):
    def __init__(self, itens: list):
        self.itens= itens
        print("pedido criado com itens fornecidos. valor R$ {self.__calcular_valor:.2f}: ")

    def calcular_valor_final(self) -> float:
        return sum (itens ['preco'] * itens ['quantidade'] for itens in self.itens)
    
    def obter_detalhes(self) -> str:
        detalhes = "Itens no pedido:\n"
        for item in self.itens:
            detalhes += f"- {item['nome']}: R${item['preco']:.2f} x {item['quantidade']}\n"

            detalhes += f"Valor total: R${self.calcular_valor_final():.2f}\n"
        return detalhes
    

class sistema_estoque:
    def atualizar_estoque(self, itens:list) -> bool:
       print("Atualizando estoque para os itens do pedido...")
       if any(item['quantidade'] > 10 for item in itens):
          print("   -> Erro: Quantidade insuficiente em estoque.")
          return False
       
       print("   -> Estoque atualizado com sucesso.")
       return True
    
    def reverter_estoque(self, itens:list):
        print("reverter estoque : itens adicionais ao estoque.")


class gerador_nota:

    def emitir_nota(self, valor_final: float, itens:list):
       print("Emitindo nota fiscal para o pedido... R$ {:.2f}".format(valor_final))
       print(f"   -> Valor total: R${valor_final:.2f}")


class sistema_notificacao:
    def enviar_confirmacao(self, sucesso: bool):
       if sucesso:
          print(" Enviando confirmação de pedido ao cliente...")
          print("   -> Confirmação enviada com sucesso.")
       else:
          print(" nao foi possivel envar confirmacao...")
         

class CheckoutFacade:
    def _init_(self):
        self.estoque = sistema_estoque()
        self.nota = gerador_nota()
        self.notificacao = sistema_notificacao()

    def Concluir_pedido(self, pedido: Pedido) -> None:
        print("Iniciando processo de checkout...")
        
        if not self.estoque.atualizar_estoque(pedido.itens):
            print("Checkout cancelado: problemas no estoque.")
            return
        
        sucesso_pagamento = pedido.compra_final()
        
        if sucesso_pagamento:
            valor_com_desconto = pedido.aplicar_desconto()
            custo_frete = pedido.estrategia_frete.calcular_frete(valor_com_desconto)
            valor_final = valor_com_desconto + custo_frete
            self.nota.emitir_nota(valor_final, pedido.itens)
        else:
            self.estoque.reverter_estoque(pedido.itens)
            print("Checkout cancelado: pagamento falhou.")
            return
        
        self.notificacao.enviar_confirmacao(sucesso_pagamento)
        print("Checkout concluído com sucesso.")


class pedido:
    def __init__(self, id: int, itens: list, valor_total: float):
        self.itens = itens
        self.estrategia_pagamento = EstrategiaPagamento
        self.frete = EstrategiaFrete
        self.embalagem = "padrao"
        self.valor_total =sum(itens['preco'] * itens['quantidade'] for itens in itens)

    def aplicar_desconto(self):
        valor_apos_desconto = self.valor_total
        if self.valor_total > 500:
            print("Aplicando 10% de desconto para pedidos grandes.")
            valor_apos_desconto *= 0.90

        return valor_apos_desconto

       
