"""Funcionalidades existentes; evoluções descritas em docs/painel.md."""
import materiais as biblioteca


def mostrar_resumo ():
# DICIONÁRIOS de contagem, preenchidos a partir da LISTA de materiais.
    por_disciplina ={}
    por_serie ={}
    for material in biblioteca.materiais :
        disciplina =material ["disciplina"]
        serie =material ["serie"]
        if disciplina not in por_disciplina :
            por_disciplina [disciplina ]=0 
        por_disciplina [disciplina ]+=1 
        if serie not in por_serie :
            por_serie [serie ]=0 
        por_serie [serie ]+=1 

    print ("\n========================================")
    print ("RESUMO DA BIBLIOTECA")
    print ("========================================")
    print ("Total de materiais:",len (biblioteca.materiais ))
    print ("\nMateriais por disciplina:")
    for disciplina in por_disciplina :
        print (disciplina +": "+str (por_disciplina [disciplina ]))
    print ("\nMateriais por série:")
    for serie in por_serie :
        print (serie +": "+str (por_serie [serie ]))
    print ("========================================")

