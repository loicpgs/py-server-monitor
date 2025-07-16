# 🖥️ Py Server Monitor

## 📋 Description

Script Python de supervision système simple et complet, permettant de surveiller les ressources principales d’un serveur :  
- Utilisation CPU, RAM, disque et swap  
- Statistiques réseau (débit en upload/download)  
- Affichage horodaté  
- Alertes basiques en cas de dépassement de seuils  

Ce projet est idéal pour un administrateur système ou un étudiant en TSSR souhaitant automatiser la surveillance basique d’un serveur.

---

## ⚙️ Fonctionnalités

- Collecte et affichage des métriques CPU, RAM, disque et swap en temps réel  
- Monitoring du trafic réseau en octets par seconde  
- Alertes simples avec seuils configurables  
- Sortie console claire et lisible  
- Facile à étendre pour intégrer d’autres métriques ou alertes

---

## 🛠️ Prérequis

- Python 3.x  
- Module `psutil` (installer avec `pip install psutil`)

---

## 🚀 Installation

1. Cloner le dépôt ou copier le script `monitor.py`  
2. Installer les dépendances :

pip install psutil

3.Lancer le script :

python monitor.py

📈 Exemple de sortie

[2025-07-16 13:50:29]
CPU: 1.2% | RAM: 52.6% | Disk: 20.6% | Swap: 1.7%
Net Sent: 0.00 MB/s | Net Recv: 0.00 MB/s
Aucune alerte.

🔧 Personnalisation

*Modifier les seuils d’alerte dans le script pour adapter la sensibilité

*Ajouter de nouvelles métriques ou des notifications (email, webhook, etc.)

*Intégrer dans un cron job ou un service pour une supervision continue

📚 Ressources

*psutil documentation
*Python officiel

📝 Licence

Ce projet est sous licence MIT.

