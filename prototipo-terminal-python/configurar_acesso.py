"""Execute uma vez neste computador para criar a senha inicial da coordenação."""

from usuarios import usuarios


def configurar_acesso():
    print("\nCONFIGURAÇÃO INICIAL DO ÁGORA")
    try:
        cadastros = usuarios.carregar_usuarios()
        coordenacoes = []
        for cadastro in cadastros:
            if cadastro["ativo"] and cadastro["perfil"] == "coordenacao":
                if cadastro.get("senha_hash"):
                    print("O primeiro acesso já foi configurado. Entre pelo py main.py.")
                    return
                coordenacoes.append(cadastro)
        if not coordenacoes:
            print("Não há coordenação ativa cadastrada para configurar.")
            return
        if len(coordenacoes) == 1:
            conta = coordenacoes[0]
        else:
            print("Escolha a conta de coordenação para configurar:")
            for cadastro in coordenacoes:
                print(f"{cadastro['id']} - {cadastro['nome']}")
            numero = input("ID (0 para cancelar): ").strip()
            if numero == "0":
                return
            conta = None
            for cadastro in coordenacoes:
                if numero == str(cadastro["id"]):
                    conta = cadastro
            if conta is None:
                print("Conta de coordenação não encontrada.")
                return
        print(f"Conta de coordenação: {conta['nome']}")
        print("Você pode usar seu próprio e-mail. O ID e os demais dados serão mantidos.")
        print("Digite 0 para cancelar.")
        email = input("E-mail que você quer usar para entrar: ").strip()
        if email == "0":
            return
        usuarios.configurar_primeiro_acesso(email, usuarios.pedir_nova_senha(), email_atual=conta["email"])
        print(f"Acesso configurado para {email}. Execute py main.py e entre com sua senha.")
    except (ValueError, OSError) as erro:
        print("Não foi possível configurar o acesso:", erro)


if __name__ == "__main__":
    try:
        configurar_acesso()
    except (EOFError, KeyboardInterrupt):
        print("\nConfiguração cancelada.")
