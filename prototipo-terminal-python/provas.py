"""Funcionalidades existentes; evoluções descritas em docs/provas.md."""
import materiais as biblioteca


def gerar_atividade ():
    biblioteca.listar_materiais ()
    if len (biblioteca.materiais )==0 :
        return 

    material =biblioteca.buscar_material_por_id ("Digite o ID do material para gerar uma atividade: ")
    if material is None :
        return 

        # LISTA de perguntas fixas: não há IA ou geração de respostas.
    perguntas =[
    'Qual é o tema principal do material "'+material ["titulo"]+'"?',
    "Escreva três informações que você aprendeu com esse conteúdo.",
    "Explique com suas próprias palavras o assunto estudado.",
    "Qual parte do conteúdo você considera mais importante? Por quê?"
    ]
    print ("\n========================================")
    print ("ATIVIDADE")
    print ("========================================")
    print ("Material:",material ["titulo"])
    print ("Disciplina:",material ["disciplina"])
    for numero in range (len (perguntas )):
        print ("\n"+str (numero +1 )+". "+perguntas [numero ])
    print ("\n========================================")

