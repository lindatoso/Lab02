""" CARICA_DA_FILE
1. Apro il file csv in lettura
2. Per ogni riga di file:
    se l'anno non è presente:
        inserisco l'anno come nuova chiave di un dizionario
    inserisco il codice come chiave del sotto-dizionario con chiave l'anno e gli altri campi come lista

AGGIUNGI_FOTO
1. Seleziono il dizionario relativo all'anno selezionato
2. Aggiungo alle chiavi del sotto dizionario il nuovo codice con valore il resto dei campi

CERCA_FOTO
1. Seleziono il dizionario relativo all'anno selezionato
2. Scorro le chiavi del sotto dizionario per trovare un match

ELENCO FOTO ANNO PER TITOLO
1. Seleziono il dizionario relativo all'anno selezionato
2. Per ogni chiave del sotto dizionario:
    aggiungo il campo del titolo a una nuova lista
3. Ordino la listagi"""

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    import csv # importo libreria di csv per lettura file

    infile=open(file_path, 'r', encoding='UTF-8') # apro file in lettura, encoding per accenti/caratteri speciali
    album=csv.reader(infile) # apro file csv come lista, ogni elemento del quale è una riga - per leggerla ciclo for
    next(album) # salto la prima riga (intestazione)
    dict_anni={} # creo dizionario per classificare in anni
    for riga in album:
        riga[4]=int(riga[4]) # trasformo il campo di anno e mese in intero
        riga[3]=int(riga[3])
        if riga[4] not in dict_anni: # se l'anno non è già presente nel dizionario (come chiave), crea una nuova chiave con annessa lista degli attributi rimanenti
            dict_anni[riga[4]]=[riga[:4]]
        else: # se l'anno è già presente, aggiungi alla lista di quell'anno gli attributi della foto in esame
            dict_anni[riga[4]].append(riga[:4])

    print(dict_anni)

    infile.close() # chiudi file
    return dict_anni # restituisci al main il dizionario con le foto


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path,dict):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    if codice not in dict[anno].values:
        if anno not in dict: # se l'anno inserito non è già presente nel dizionario, crea nuova chiave con relativi valori in lista
            dict[anno] = [codice, titolo, autore, mese]
        else: # come per carica_da_file
            dict[anno].append([codice, titolo, autore, mese])
        return True # restituisci booleano al main per stampare messaggi di successo/insuccesso
    else:
        return False


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path,album)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
