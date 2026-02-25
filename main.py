import os

# Configurações do  caminho das pastas
PASTA_A = r'C:\Users\usuario\documents\pasta1'
PASTA_B = r'C:\Users\usuario\documents\pasta2'
ARQUIVO_SAIDA = 'divergentes.txt'

def deve_ignorar_linha(linha):
    """Verifica se a linha contém as assinaturas que devem invalidar a linha inteira."""
    assinaturas = []
    return any(sigla.lower() in linha.lower() for sigla in assinaturas)

def carregar_e_limpar(caminho):
    """Lê o arquivo e ignora completamente as linhas que contenham as assinaturas."""
    try:
        conteudo_filtrado = set()
        with open(caminho, 'r', encoding='latin1') as f:
            for line in f:
                linha_limpa = line.strip()
                # Se a linha não for vazia e não tiver a assinatura, nós a processamos
                if linha_limpa and not deve_ignorar_linha(linha_limpa):
                    # Normalizamos espaços internos para evitar falsos erros de formatação
                    linha_normalizada = " ".join(linha_limpa.split())
                    conteudo_filtrado.add(linha_normalizada)
        return conteudo_filtrado
    except Exception as e:
        print(f"Erro ao ler arquivo {os.path.basename(caminho)}: {e}")
        return set()

def comparar_pastas():
    arquivos_iguais = 0
    detalhes_divergencias = []
    
    if not os.path.exists(PASTA_A):
        print(f"Erro: Pasta PASTA A não encontrada.")
        return

    arquivos_a = [f for f in os.listdir(PASTA_A) if os.path.isfile(os.path.join(PASTA_A, f))]
    
    for nome_arquivo in arquivos_a:
        caminho_a = os.path.join(PASTA_A, nome_arquivo)
        caminho_b = os.path.join(PASTA_B, nome_arquivo)
        
        if not os.path.exists(caminho_b):
            detalhes_divergencias.append(f"ARQUIVO AUSENTE NA PASTA B: {nome_arquivo}\n")
            continue
        
        conteudo_a = carregar_e_limpar(caminho_a)
        conteudo_b = carregar_e_limpar(caminho_b)
        
        sobra_pastaA = conteudo_a - conteudo_b
        sobra_pastaB = conteudo_b - conteudo_a
        
        if not sobra_pastaA and not sobra_pastaB:
            arquivos_iguais += 1
        else:
            bloco_erro = [f"DIVERGÊNCIA REAL NO ARQUIVO: {nome_arquivo}"]
            
            if sobra_pastaA:
                bloco_erro.append("  [>] Linhas exclusivas da PASTA A:")
                for linha in sobra_pastaA:
                    bloco_erro.append(f"      {linha}")
            
            if sobra_pastaB:
                bloco_erro.append("  [<] Linhas exclusivas da PASTA B:")
                for linha in sobra_pastaB:
                    bloco_erro.append(f"      {linha}")
            
            bloco_erro.append("-" * 50)
            detalhes_divergencias.append("\n".join(bloco_erro))

    with open(ARQUIVO_SAIDA, 'w', encoding='latin1') as f_out:
        f_out.write("--- RELATÓRIO DE DIVERGÊNCIAS DE ARQUIVOS---\n\n")
        if detalhes_divergencias:
            f_out.write("\n\n".join(detalhes_divergencias))
        else:
            f_out.write("Nenhuma divergência de dados encontrada nas linhas de conteúdo!")

    print("--- Resumo da Execução ---")
    print(f"Arquivos iguais (ignorando assinaturas): {arquivos_iguais}")
    print(f"Arquivos com divergências reais: {len(detalhes_divergencias)}")
    
    os.startfile(ARQUIVO_SAIDA)

if __name__ == "__main__":
    comparar_pastas()