"""Funcionalidades existentes; evoluções descritas em consultas/README.md."""
from materiais import materiais as biblioteca


def pesquisar_material ():
    termo =biblioteca.ler_texto ("Digite o termo de pesquisa: ").lower ()
    encontrou =False 
    for material in biblioteca.materiais :
        if (termo in material ["titulo"].lower ()
        or termo in material ["disciplina"].lower ()
        or termo in material ["serie"].lower ()
        or termo in material ["conteudo"].lower ()
        or termo in material ["bncc"].lower ()):
            print ("\n["+str (material ["id"])+"] "+material ["titulo"])
            print ("Disciplina:",material ["disciplina"])
            print ("Série:",material ["serie"])
            encontrou =True 

    if not encontrou :
        print ("Nenhum material encontrado.")



def consultar_conteudo ():
    termo =biblioteca.ler_texto ("Digite um assunto ou palavra que deseja consultar: ").lower ()
    encontrou =False 
    for material in biblioteca.materiais :
        if termo in material ["conteudo"].lower ():
            print ("\n========================================")
            print ("RESULTADO DA CONSULTA")
            print ("========================================")
            print ("Material:",material ["titulo"])
            print ("Disciplina:",material ["disciplina"])
            print ("\nConteúdo:")
            print (material ["conteudo"])
            print ("\nFonte:")
            print (material ["titulo"]+" - "+material ["disciplina"])
            print ("========================================")
            encontrou =True 

    if not encontrou :
        print ("Não encontrei informações sobre esse assunto nos materiais cadastrados.")

