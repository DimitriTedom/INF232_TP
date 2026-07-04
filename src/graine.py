def calculer_graine(nom_complet: str) -> int:
    """
    Calcule une graine numérique unique et déterministe à partir d'un nom complet.
    
    L'algorithme implémente un hachage polynomial (rolling hash) déterministe :
    - Nettoie la chaîne en supprimant les espaces et en la mettant en majuscules.
    - Utilise le multiplicateur premier p = 31 (pour minimiser les collisions).
    - Utilise le modulo premier de Mersenne m = 2^31 - 1 (pour borner la graine
      sur 31 bits tout en garantissant une excellente distribution).
    """
    # Nettoyage de la chaîne de caractères (retrait des espaces et mise en majuscules)
    chaine = "".join(nom_complet.split()).upper()
    
    p = 31
    m = (1 << 31) - 1  # 2**31 - 1 (Mersenne prime M31)
    hash_val = 0
    
    for char in chaine:
        hash_val = (hash_val * p + ord(char)) % m
        
    return hash_val
