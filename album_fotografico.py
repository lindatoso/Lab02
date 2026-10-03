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
3. Ordino la lista"""

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    import csv # importo libreria di csv per lettura file

    try:
        infile=open(file_path, 'r', encoding='UTF-8') # apro file in lettura, encoding per accenti/caratteri speciali
        album=csv.reader(infile) # apro file csv come lista, ogni elemento del quale è una riga - per leggerla ciclo for
        next(album) # salto la prima riga (intestazione)
        dict_anni={} # creo dizionario per classificare in anni
        d = {}
        for riga in album:
            riga[4]=int(riga[4]) # trasformo il campo di anno e mese in intero
            riga[3]=int(riga[3])
            if riga[4] not in dict_anni: # se l'anno non è già presente nel dizionario (come chiave), crea una nuova chiave + lista vuota
                dict_anni[riga[4]]={}
            dict_anni[riga[4]][riga[0]]=riga[1:4] # aggiungi il dizionario alla lista dell'anno corrispondente

        print(dict_anni)

        infile.close() # chiudi file
        return dict_anni # restituisci al main il dizionario con le foto
    except OSError:
        print("File inesistente")


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path,dict):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    import csv
    if anno not in dict.keys():  # se l'anno inserito non è già presente nel dizionario, crea nuova chiave con relativi valori in lista
        dict[anno] = {}
        if codice not in dict[anno].keys():
            dict[anno][codice]=[titolo, autore, mese]
            try:
                outfile=open(file_path, 'a')
                riga=[codice, titolo, autore, mese, anno]
                scrittore=csv.writer(outfile)
                scrittore.writerow(riga)
                outfile.close()

            except OSError:
                print('File inesistente')

            return True # restituisci booleano al main per stampare messaggi di successo/insuccesso
        else:
            return False


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    for i in album.keys():
        if codice in album[i]:
            risultato=[]
            risultato.append(codice)
            for k in album[i][codice]:
                risultato.append(k)
            risultato.append(i)
            riga=risultato[0]
            for j in range(1,len(risultato)):
                riga=riga+', '+str(risultato[j])
            return riga


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    if anno in album:
        dicto={}
        l=0
        for k in album[anno]:
            chiavi=list(album[anno].keys())
            dicto[album[anno][k][0]]=[chiavi[l]]
            for j in range(1,len(album[anno][k])):
                dicto[album[anno][k][0]].append(album[anno][k][j])
            l+=1
        ordinato=sorted(dicto.items())
        titoli=[]
        for a in range(0,len(ordinato)):
            titoli.append(str(ordinato[a][0]))
            for b in range (0,3):
                titoli[a]=titoli[a]+', '+str(ordinato[a][1][b])

        return titoli
    else:
        return None



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
                print("\n".join([f"- {title}" for title in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
