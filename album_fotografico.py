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

    try: # provo ad aprire il file
        infile=open(file_path, 'r', encoding='UTF-8') # apro file in lettura, encoding per accenti/caratteri speciali
        album=csv.reader(infile) # apro file csv come lista, ogni elemento del quale è una riga - per leggerla ciclo for
        next(album) # salto la prima riga (intestazione)
        dict_anni={} # creo dizionario per classificare in anni
        for riga in album:
            riga[4]=int(riga[4]) # trasformo il campo di anno e mese in intero
            riga[3]=int(riga[3])
            if riga[4] not in dict_anni: # se l'anno non è già presente nel dizionario (come chiave), crea una nuova chiave + dizionario vuoto
                dict_anni[riga[4]]={}
            dict_anni[riga[4]][riga[0]]=riga[1:4] # aggiungi il dizionario alla lista dell'anno corrispondente con chiave il codice e valori titolo, autore e mese in lista

        print(dict_anni)

        infile.close() # chiudi file
        return dict_anni # restituisci al main il dizionario con le foto
    except OSError: # errore sul file
        print("File inesistente")


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    import csv
    if anno not in album.keys():  # se l'anno inserito non è già presente nel dizionario, crea nuova chiave con relativo dizionario vuoto
        album[anno] = {}
        if codice not in album[anno].keys(): # se il codice non corrisponde già a quello di un'altra foto
            album[anno][codice]=[titolo, autore, mese] # aggiungi i dati inseriti in un dizionario con chiave il codice e attributi il resto
            try:
                outfile=open(file_path, 'a') # append - aggiungi al fondo del file
                riga=[codice, titolo, autore, mese, anno] # campi da aggiungere
                scrittore=csv.writer(outfile) # funzione csv che permette di aggiungere i campi in formato csv
                scrittore.writerow(riga) # funzione che inserisce i dati della riga
                outfile.close()

            except OSError:
                print('File inesistente')

            return True # restituisci booleano al main per stampare messaggi di successo/insuccesso
        else:
            print('Codice foto già in uso')
            return False
    else:
        return None


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    for i in album: # per ogni anno dell'album
        if codice in album[i]: # se il codice si trova tra le chiavi di quell'anno
            risultato=[codice] # aggiungo il codice a una lista
            for k in album[i][codice]: # per ogni attributo del codice
                risultato.append(k) # aggiungo l'attributo alla lista
            risultato.append(i) # aggiungo l'anno alla lista
            riga=risultato[0] # per stampare, creo una stringa che inizia con il codice
            for j in range(1,len(risultato)): # per ogni elemento della lista
                riga=riga+', '+str(risultato[j]) # alla riga concateno gli altri attributi
            return riga
        else:
            return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    if anno in album: # se l'anno si trova nell'album
        dicto={} # creo un dizionario vuoto
        for code in album[anno]: # per ogni codice dell'anno
            chiavi=list(album[anno].keys()) # creo una lista con i codici dell'anno
            dicto[album[anno][code][0]]=[code] # come chiave del dizionario vuoto metto il titolo e come primo valore in lista il codice
            for j in range(1,len(album[anno][k])): # contatore da 1 a 3 (attributi relativi al codice)
                dicto[album[anno][k][0]].append(album[anno][k][j]) # aggiungo al dizionario in lista autore e mese
        ordinato=sorted(dicto.items()) # creo una lista di tuple ordinate alfabeticamente per titolo
        titoli=[] # lista vuota
        for a in range(0,len(ordinato)): # contatore da 0 a lunghezza lista di tuple
            titoli.append(str(ordinato[a][0])) # alla lista vuota aggiungo il titolo
            for b in range (0,3): # contatore da 0 a 3 (lunghezza attributi)
                titoli[a]=titoli[a]+', '+str(ordinato[a][1][b]) # concateno al titolo gli altri attributi

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

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
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
