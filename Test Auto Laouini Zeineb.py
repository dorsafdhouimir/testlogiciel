import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style


def afficher_resultat_test(identifiant_test, statut, message=""):
    """
    Affiche le résultat d'un test avec une sortie colorée
    
    Args:
        identifiant_test (str): L'identifiant du test (ex: "TC-01")
        statut (str): Le statut du test ("PASS" ou "FAIL")
        message (str): Message descriptif optionnel
    """
    couleur = Fore.GREEN if statut == "PASS" else Fore.RED
    icone = "✔" if statut == "PASS" else "❌"
    print(couleur + f"{identifiant_test} : {statut} {icone}" + Style.RESET_ALL)
    if message:
        print(f"   ➜ {message}")


def executer_tests_formulaire_demoqa():
    """
    Fonction principale pour exécuter tous les tests automatisés 
    du formulaire d'inscription étudiant sur DemoQA
    """
    
    # Démarrer le chronomètre
    heure_debut = time.time()
    
    # Créer un dossier avec horodatage pour les captures d'écran
    horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dossier_captures = f"captures_formulaire_{horodatage}"
    os.makedirs(dossier_captures, exist_ok=True)

    # Initialiser le navigateur Chrome
    print("\nInitialisation du navigateur Chrome...")
    service = Service(ChromeDriverManager().install())
    navigateur = webdriver.Chrome(service=service)
    navigateur.maximize_window()
    attente = WebDriverWait(navigateur, 10)
    
    # Dictionnaire pour stocker les résultats des tests
    resultats = {}

    print("\n" + "="*60)
    print("TESTS AUTOMATISÉS - Formulaire DemoQA")
    print("="*60 + "\n")

    # ============================================
    # TC-01 : Remplissage valide du formulaire
    # ============================================
    try:
        # Accéder à la page du formulaire
        navigateur.get("https://demoqa.com/automation-practice-form")
        time.sleep(1)
        
        # Remplir le prénom
        navigateur.find_element(By.ID, "firstName").send_keys("Zeineb")
        
        # Remplir le nom de famille
        navigateur.find_element(By.ID, "lastName").send_keys("Laouini")
        
        # Sélectionner le genre (Féminin)
        navigateur.find_element(By.CSS_SELECTOR, "label[for='gender-radio-2']").click()
        
        # Remplir le numéro de téléphone
        navigateur.find_element(By.ID, "userNumber").send_keys("0123456789")
        
        # Test réussi
        resultats["TC-01"] = "PASS"
        afficher_resultat_test("TC-01", "PASS", "Tous les champs acceptent les données valides")
        
    except Exception as erreur:
        # Test échoué - prendre une capture d'écran
        navigateur.save_screenshot(f"{dossier_captures}/TC-01.png")
        resultats["TC-01"] = "FAIL"
        afficher_resultat_test("TC-01", "FAIL", f"Erreur: {str(erreur)[:50]}")

    # ============================================
    # TC-02 : Suppression de la date par défaut
    # ============================================
    try:
        # Recharger la page du formulaire
        navigateur.get("https://demoqa.com/automation-practice-form")
        time.sleep(1)
        
        # Localiser le champ de date et faire défiler jusqu'à lui
        champ_date = attente.until(EC.element_to_be_clickable((By.ID, "dateOfBirthInput")))
        navigateur.execute_script("arguments[0].scrollIntoView({block: 'center'});", champ_date)
        
        # Cliquer sur le champ de date
        champ_date.click()
        time.sleep(0.5)
        
        # Essayer de supprimer la date (Ctrl+A puis Backspace)
        champ_date.send_keys(Keys.CONTROL + "a")
        champ_date.send_keys(Keys.BACKSPACE)
        time.sleep(2)
        
        # Vérifier si la page a planté
        navigateur.find_element(By.ID, "firstName")
        
        # Si on arrive ici, la page n'a pas planté (bug corrigé)
        navigateur.save_screenshot(f"{dossier_captures}/TC-02.png")
        resultats["TC-02"] = "FAIL"
        afficher_resultat_test("TC-02", "FAIL", "Bug non reproduit: l'application n'a pas planté")
        
    except:
        # La page a planté (bug attendu)
        navigateur.save_screenshot(f"{dossier_captures}/TC-02.png")
        resultats["TC-02"] = "FAIL"
        afficher_resultat_test("TC-02", "FAIL", "Bug détecté: L'application a planté")

    # ============================================
    # TC-03 : Soumission sans le prénom (champ obligatoire)
    # ============================================
    try:
        # Recharger la page du formulaire
        navigateur.get("https://demoqa.com/automation-practice-form")
        time.sleep(1)
        
        # Laisser le prénom vide, remplir les autres champs obligatoires
        navigateur.find_element(By.ID, "lastName").send_keys("Ben Ali")
        
        # Sélectionner le genre (Masculin)
        navigateur.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']").click()
        
        # Remplir le numéro de téléphone
        navigateur.find_element(By.ID, "userNumber").send_keys("0123456789")
        
        # Localiser le bouton de soumission et faire défiler jusqu'à lui
        bouton_soumettre = navigateur.find_element(By.ID, "submit")
        navigateur.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton_soumettre)
        time.sleep(0.5)
        
        # Cliquer sur le bouton avec JavaScript
        navigateur.execute_script("arguments[0].click();", bouton_soumettre)
        time.sleep(2)
        
        # Vérifier si la fenêtre modale de confirmation apparaît
        try:
            attente.until(EC.presence_of_element_located((By.ID, "example-modal-sizes-title-lg")))
            
            # Modale trouvée = formulaire soumis malgré le champ vide = échec du test
            navigateur.save_screenshot(f"{dossier_captures}/TC-03.png")
            resultats["TC-03"] = "FAIL"
            afficher_resultat_test("TC-03", "FAIL", "Le formulaire s'est soumis malgré le champ vide")
        except:
            # Modale non trouvée = formulaire non soumis = succès du test
            resultats["TC-03"] = "PASS"
            afficher_resultat_test("TC-03", "PASS", "Le formulaire a correctement refusé la soumission")
            
    except Exception as erreur:
        navigateur.save_screenshot(f"{dossier_captures}/TC-03.png")
        resultats["TC-03"] = "FAIL"
        afficher_resultat_test("TC-03", "FAIL", f"Erreur: {str(erreur)[:50]}")

    # ============================================
    # TC-04 : Upload d'un fichier PDF (non-image)
    # ============================================
    try:
        # Recharger la page du formulaire
        navigateur.get("https://demoqa.com/automation-practice-form")
        time.sleep(1)
        
        # Remplir les champs obligatoires
        navigateur.find_element(By.ID, "firstName").send_keys("Zeineb")
        navigateur.find_element(By.ID, "lastName").send_keys("Laouini")
        navigateur.find_element(By.CSS_SELECTOR, "label[for='gender-radio-2']").click()
        navigateur.find_element(By.ID, "userNumber").send_keys("0123456789")
        
        # Créer un fichier PDF de test (simple fichier texte avec extension .pdf)
        chemin_pdf = os.path.abspath(os.path.join(dossier_captures, "test.pdf"))
        with open(chemin_pdf, "w") as fichier:
            # Écrire un simple texte - le formulaire devrait rejeter ce fichier
            fichier.write("Ceci est un fichier de test PDF")
        
        # Localiser le champ d'upload et faire défiler jusqu'à lui
        champ_upload = navigateur.find_element(By.ID, "uploadPicture")
        navigateur.execute_script("arguments[0].scrollIntoView({block: 'center'});", champ_upload)
        
        # Uploader le fichier PDF
        champ_upload.send_keys(chemin_pdf)
        time.sleep(1)
        
        # Localiser le bouton de soumission et faire défiler jusqu'à lui
        bouton_soumettre = navigateur.find_element(By.ID, "submit")
        navigateur.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton_soumettre)
        time.sleep(0.5)
        
        # Cliquer sur le bouton avec JavaScript
        navigateur.execute_script("arguments[0].click();", bouton_soumettre)
        time.sleep(2)
        
        # Vérifier si le formulaire s'est soumis
        try:
            attente.until(EC.presence_of_element_located((By.ID, "example-modal-sizes-title-lg")))
            
            # Modale trouvée = PDF accepté = bug détecté = échec du test
            navigateur.save_screenshot(f"{dossier_captures}/TC-04.png")
            resultats["TC-04"] = "FAIL"
            afficher_resultat_test("TC-04", "FAIL", "Bug: Le PDF a été accepté (devrait accepter uniquement des images)")
        except:
            # Modale non trouvée = PDF refusé = succès du test
            resultats["TC-04"] = "PASS"
            afficher_resultat_test("TC-04", "PASS", "Le PDF a été correctement refusé")
            
    except Exception as erreur:
        navigateur.save_screenshot(f"{dossier_captures}/TC-04.png")
        resultats["TC-04"] = "FAIL"
        afficher_resultat_test("TC-04", "FAIL", f"Erreur: {str(erreur)[:50]}")

    # ============================================
    # TC-05 : Numéro de téléphone avec des lettres
    # ============================================
    try:
        # Recharger la page du formulaire
        navigateur.get("https://demoqa.com/automation-practice-form")
        time.sleep(1)
        
        # Remplir les autres champs obligatoires
        navigateur.find_element(By.ID, "firstName").send_keys("Zeineb")
        navigateur.find_element(By.ID, "lastName").send_keys("Laouini")
        navigateur.find_element(By.CSS_SELECTOR, "label[for='gender-radio-2']").click()
        
        # Essayer de remplir le téléphone avec des lettres
        champ_telephone = navigateur.find_element(By.ID, "userNumber")
        champ_telephone.send_keys("abcdefghij")
        time.sleep(1)
        
        # Récupérer la valeur actuelle du champ téléphone
        valeur_telephone = champ_telephone.get_attribute("value")
        
        # Localiser le bouton de soumission et faire défiler jusqu'à lui
        bouton_soumettre = navigateur.find_element(By.ID, "submit")
        navigateur.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton_soumettre)
        time.sleep(0.5)
        
        # Cliquer sur le bouton avec JavaScript
        navigateur.execute_script("arguments[0].click();", bouton_soumettre)
        time.sleep(2)
        
        # Vérifier si le formulaire s'est soumis
        try:
            attente.until(EC.presence_of_element_located((By.ID, "example-modal-sizes-title-lg")))
            
            # Modale trouvée = lettres acceptées = échec du test
            navigateur.save_screenshot(f"{dossier_captures}/TC-05.png")
            resultats["TC-05"] = "FAIL"
            afficher_resultat_test("TC-05", "FAIL", f"Le champ accepte les lettres (valeur: '{valeur_telephone}')")
        except:
            # Modale non trouvée = lettres refusées = succès du test
            resultats["TC-05"] = "PASS"
            afficher_resultat_test("TC-05", "PASS", f"Le champ refuse correctement les lettres (valeur: '{valeur_telephone}')")
            
    except Exception as erreur:
        navigateur.save_screenshot(f"{dossier_captures}/TC-05.png")
        resultats["TC-05"] = "FAIL"
        afficher_resultat_test("TC-05", "FAIL", f"Erreur: {str(erreur)[:50]}")

    # Fermer le navigateur
    navigateur.quit()
    
    # Arrêter le chronomètre
    heure_fin = time.time()
    duree = round(heure_fin - heure_debut, 2)

    # ============================================
    # RAPPORT FINAL
    # ============================================
    tests_reussis = sum(1 for statut in resultats.values() if statut == "PASS")
    tests_echoues = sum(1 for statut in resultats.values() if statut == "FAIL")
    total_tests = len(resultats)
    taux_reussite = (tests_reussis / total_tests * 100) if total_tests > 0 else 0
    
    print("\n" + "="*60)
    print("📊 RAPPORT FINAL")
    print("="*60)
    print(f"Tests réussis    : {tests_reussis}")
    print(f"Tests échoués    : {tests_echoues}")
    print(f"Total            : {total_tests}")
    print(f"Taux de réussite : {taux_reussite:.1f}%")
    print(f"⏳ Temps d'exécution : {duree} secondes")
    print("="*60)
    
    # Exporter le rapport dans un fichier texte
    chemin_rapport = f"rapport_tests_formulaire_{horodatage}.txt"
    with open(chemin_rapport, "w", encoding="utf-8") as fichier:
        fichier.write("=== Rapport d'Automatisation - Formulaire DemoQA ===\n\n")
        for test, statut in resultats.items():
            fichier.write(f"{test} : {statut}\n")
        fichier.write(f"\nRéussis: {tests_reussis} | Échoués: {tests_echoues} | Total: {total_tests}\n")
        fichier.write(f"Taux de réussite: {taux_reussite:.1f}%\n")
        fichier.write(f"Temps d'exécution: {duree}s\n")
    
    print(f"\n📁 Rapport sauvegardé: {chemin_rapport}")
    print(f"📸 Captures d'écran sauvegardées dans: {dossier_captures}\n")


if __name__ == "__main__":
    executer_tests_formulaire_demoqa()