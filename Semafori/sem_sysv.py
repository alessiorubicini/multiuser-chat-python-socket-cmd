'''

Utilizzo semafori System V in Python

Sviluppato da Alessio Rubicini

Versione Python: 3.8.2

'''


# ------------ MODULI -----------------------

import sysv_ipc as ipc      # IPC System V
import os                   # Funzioni di sistema (es. fork)
import time                 # Modulo time per sleep()

# ------------ ESECUZIONE --------------------


'''
Creazione semaforo

Parametri:
    - Chiave: deve essere None, IPC_PRIVATE o un intero. Se è None il modulo sceglie una chiave random non utilizzata
    - Flag: 0 (default) apre un semaforo esistente, IPC_CREAT apre o crea il semaforo se non esiste, IPC_CREX crea un semaforo e restituisce errore se già esiste
    - Mode: permessi
    - Initial_value: valore a cui viene inizializzato il semaforo
'''
try:
    sem = ipc.Semaphore(10, ipc.IPC_CREAT, initial_value=1)
except ipc.Error as errore:
    print(errore);
    

print("Semaforo creato con chiave 10")

# Acquisice il semaforo
sem.acquire()

# Fork
pid = os.fork()

# Controllo errore fork
if pid < 0:
    print("Errore fork")
    exit()

# Processo figlio
if pid == 0:

    # Apre il semaforo creato precedentemente
    child_sem = ipc.Semaphore(10)

    with child_sem:
        print("Figlio: ho acquisito il semaforo con chiave 10")
        
        # REGIONE CRITICA
        # Scrive qualcosa sul file
        with open("prova.txt", "w") as file:
            file.write("Ciao a tutti, sono il processo figlio")
        
        # Aspetta 3 secondi
        time.sleep(2)

        # Uscendo dal costrutto 'With' rilascia il semaforo

# Processo padre
elif pid > 0:
    
    # Legge il contenuto iniziale del file
    with open("prova.txt", "r") as file:
        print("Contenuto iniziale del file: " + file.read())
    
    # Rilascia il semaforo
    sem.release()
    print("Padre: rilascio il semaforo per il figlio")

    # Aspetta 1 secondo per dare al figlio la possibilità di acquisire il semaforo
    time.sleep(1)

    # Aspetta che il figlio rilasci il semaforo
    sem.acquire(10)

    # Legge cosa ha scritto il figlio nel file
    with open("prova.txt", "r") as file:
        print("Il padre ha letto: " + file.read())

    print("Padre: elimino il semaforo")

    # Appena lo acquisisce lo rilascia e lo elimina
    try:
        sem.release()
        sem.remove()
    except ipc.Error as errore:
        print(errore)

    print("Padre: semaforo rilasciato ed eliminato con successo")
