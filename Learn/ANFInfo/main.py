import time
from datetime import datetime
from anaf_client import construieste_payload, trimite_request

def citeste_cuiuri_manual(): # Citeste CUI-uri de la utilizator, unu cate unu, pana la apasarea 'Enter' fara input
    cuiuri = []
    while True:
        cui = input("Introdu CUI: ").strip()
        if not cui:
            break
        if not cui.isdigit():
            print("CUI invalid! Te rog introdu doar cifre.")
            continue
        cuiuri.append(cui)
    return cuiuri

def citeste_cuiuri_din_fisier(nume_fisier): # Citeste CUI-uri din fisierul text specificat (un CUI pe linie)
    try:
        with open(nume_fisier, 'r') as f:
            linii = f.readlines()
        cuiuri = [linie.strip() for linie in linii if linie.strip().isdigit()]
        return cuiuri
    except FileNotFoundError:
        print("Fiscierul nu a fost gasit.")
        return []

def validare_data(data_str): # Verifica daca data respecta formatul YYYY-MM-DD
    try:
        datetime.strptime(data_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def interogheaza_anaf(cuiuri, data_interogare): #Construiesc payload-ul si trimit request-ul catre API.
    if len(cuiuri) > 100:
        print("Ai introdus mai mult de 100 de CUI-uri. Se vor trimite doar primii 100.")
        cuiuri = cuiuri[:100]

    payload = construieste_payload(cuiuri, data_interogare)
    raspuns = trimite_request(payload)
    time.sleep(1) # 1 request pe secunda
    return raspuns

def modifica_fisier_cuiuri(nume_fisier): # Meniu clasic pentru Modifica fisierul cuiuri.txt (adaugare/stergere/afisare)
    while True:
        print("=== Modificare fisier CUI-uri ===")
        print("1. Adauga CUI")
        print("2. Sterge CUI")
        print("3. Afisaza CUI-uri existente")
        print("4. Inapoi la meniul principal")
        alegere = input("Alege optiunea: ").strip()

        if alegere == "1": # Adaugare in fisier
            cui_nou = input("Introdu CUI-ul de adaugat: ").strip()
            if not cui_nou.isdigit():
                print("CUI invalid! Trebuie sa contina doar cifre.")
                continue
            try:
                with open(nume_fisier, 'a+') as f:
                    f.seek(0)
                    continut = f.read()
                    if continut and not continut.endswith('\n'):
                        f.write('\n')
                    f.write(cui_nou + "\n")
                print(f"CUI-ul {cui_nou} a fost adaugat!")
            except Exception as e:
                print(f"Eroare la scrierea in fisier: {e}")

        elif alegere == "2": # Sterge din fisier
            try:
                with open(nume_fisier, "r") as f:
                    cuiuri = [linie.strip() for linie in f.readlines()]
            except FileNotFoundError:
                print("Fiscierul nu exista.")
                continue

            if not cuiuri:
                print("Fisierul este gol.")
                continue

            print("CUI-uri existente:")
            for idx, cui in enumerate(cuiuri, 1):
                print(f"{idx}. {cui}")

            index_stergere = input("Introdu numarul CUI-ului de sters (sau Enter pentru a anula): ").strip()
            if not index_stergere:
                continue
            if not index_stergere.isdigit() or int(index_stergere) < 1 or int(index_stergere) > len(cuiuri):
                print("Index invalid!")
                continue

            sters = cuiuri.pop(int(index_stergere) - 1)
            with open(nume_fisier, "w") as f:
                for cui in cuiuri:
                    f.write(cui + "\n")
            print(f"CUI-ul {sters} a fost sters!")

        elif alegere == "3": # Afisarea datelor din fisier
            try:
                with open(nume_fisier, "r") as f:
                    cuiuri = [linie.strip() for linie in f if linie.strip().isdigit()]
                if cuiuri:
                    print("\nCUI-uri existente:")
                    for cui in cuiuri:
                        print(f"- {cui}")
                else:
                    print("Fisierul este gol.")
            except FileNotFoundError:
                print("Fiscierul nu exista.")

        elif alegere == "4":
            break

        else:
            print("Optiune invalida! Incearca din nou.")
            continue

def afiseaza_rezultatte(raspuns):
    if not raspuns:
        print("Nu s-a primit niciun raspuns valid.")
        return
    
    print("\n=== Rezultate gasite ===")
    for firma in raspuns.get("found", []):
        date_generale = firma.get("date_generale", {})
        adresa_sediu = firma.get("adresa_sediu_social", {})
        print(f"- CUI: {date_generale.get('cui')} | Denumire: {date_generale.get('denumire')}")
        print(f"  Adresa: {date_generale.get('adresa')}")
        print(f"  Nr. Reg. Com.: {date_generale.get('nrRegCom')}")
        print(f"  Telefon: {date_generale.get('telefon')}")
        print(f"  Cod Postal: {date_generale.get('codPostal')}")
        print(f"  Cod CAEN: {date_generale.get('cod_CAEN')}")
        print(f"  Forma juridica: {date_generale.get('forma_juridica')}")
        print(f"  RO e-Factura: {date_generale.get('statusRO_e_Factura')}")
        print(f"  Denumire Judet: {adresa_sediu.get('sdenumire_Judet')}")
        print(f"  Denumire Localitate: {adresa_sediu.get('sdenumire_Localitate')}")
        print("")

    if raspuns.get("not_found"):
        print("=== CUI-uri negasite ===")
        for cui in raspuns["notFound"]:
            print(f"- {cui}")

def main(): # Meniu clasic interactiv
    while True:
        print("=== Meniu Principal ===")
        print("1. Introdu CUI-uri manual")
        print("2. Introdu CUI-uri din fisier")
        print("3. Modifica fisierul cuiuri.txt (adaugare/stergere)")
        print("4. Iesire")
        optiune = input("Alegeti optiunea: ").strip()
        
        if optiune == "1":
            cuiuri = citeste_cuiuri_manual()
        elif optiune == "2":
            nume_fisier = input("Nume fisier (ex: cuiuri.txt): ").strip()
            cuiuri = citeste_cuiuri_din_fisier(nume_fisier)
        elif optiune == "3":
            modifica_fisier_cuiuri("cuiuri.txt")
            continue
        elif optiune == "4":
            print("Iesire...")
            break
        else:
            print("Optiune invalida! Incearca din nou.")
            continue
        
        if not cuiuri:
            print("Nu ai introdus niciun CUI.")
            continue
            
        data_interogare = input("Introdu data interogarii (YYYY-MM-DD): ").strip()
        if not validare_data(data_interogare):
            print("Data invalida! Te rog introdu data valida sau respecta formatul YYYY-MM-DD.")
            continue
            
        print("\nSe trimite cererea catre ANAF...")
        raspuns = interogheaza_anaf(cuiuri, data_interogare)
        afiseaza_rezultatte(raspuns)

if __name__ == "__main__":
    main()