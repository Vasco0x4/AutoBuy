# AutoBuy
AutoBuy est un bot conçu pour acheter des actions aussi rapidement que possible sur le marché. Actuellement, il fonctionne avec l'API Bitget V2. Bien que le bot ait été initialement prévu pour rester en version de développement, il fonctionne sans problème.

## Utilisation
- Pour démarrer le bot, vous devez configurer vos clés API Bitget dans le fichier suivant :

`AutoBuy-main/telegram_channel_duplicator/config_controller.py`

- Le second fichier de configuration est centré sur Telegram. Entrez votre numéro de téléphone et votre clé API TELEGRAM.

Exemple de configuration (AutoBuy-main/config.yaml) :

groups:
  - name: test  # Ne pas modifier
    sources: 
      - "test"  # La source où le bot va chercher les actions à acheter
    destinations:
      - "test2"  # Sortie des logs / non obligatoire
    whitelist: [ ]  # Ne pas modifier



- Configuration pour le mapping des tailles de symboles (AutoBuy-main/telegram_channel_duplicator/duplicator.py) :
  
Le mapping est essentiel pour que le bot fonctionne. Si le message contient "SOL" ou "sol", il achètera l'actif 'SOLUSDT' sur l'application Bitget.

`python
Copier le code
SYMBOL_SIZE_MAPPING = {
    "BTC": {"symbol":"BTCUSDT","size":0.00729182},
    "ETH": {"symbol":"ETHUSDT","size":0.14270384},
    "USDT": {"symbol":"USDTUSDT","size":501.25263032},
    "BNB": {"symbol":"BNBUSDT","size":0.88440789},
    "SOL": {"symbol":"SOLUSDT","size":2.7499725},
}
`
Pour faciliter le mapping, il existe un script mapping.py qui va obtenir les 200 premières cryptomonnaies par capitalisation boursière et calculer la taille pour 50 $.


## exemple d'utilisation

Une fois que le bot Telegram aura lu un message contenant "BTC", il enverra un ordre Bitget avec une "size" de "0.00729182", ce qui correspond à 50 $.

Vous pouvez également ajouter des filtres dans AutoBuy-main/auto/duplicator.py. ligne 53

Exemple :

`python
Copier le code
if all(emoji in msg.message for emoji in ["🟢"]) and "test" in msg.message.upper():
`

Si le message comprend 🟢 ET "test", il sera pris en compte par le bot et transmis à order_bitget.py.

Le bot a un temps de réaction de moins d'une seconde, d'où l'intérêt du mapping qui évite un maximum de requêtes inutiles.





Bonne chance à toi si tu t'aventures dans ce code xD


source : 

https://www.bitget.com/api-doc/common/intro

https://github.com/deFiss/telegram_channel_duplicator

https://core.telegram.org/api/obtaining_api_id