import requests
from bs4 import BeautifulSoup

def examenmercadolibre():

    search_url = ("https://listado.mercadolibre.com.mx/playstation-5#D[A:playstation%205]"
                  "&ITEM_CONDITION=2230284"
                  "&MERCADOLIBRE_ADDRESS=TUxMX0NBUGIwM2M4")

    headers = {
        "User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Error al acceder al sitio web. Código de estado: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all("div", class_="ui-search-result__wrapper", limit=5)

    if not products:
        print("No se encontraron productos.")
        return

    results = []
    for product in products:
        try:
            name = product.find("h2", class_="poly-component__title-wrapper").get_text(strip=True)
            price = product.find("span", class_="andes-money-amount__fraction").get_text(strip=True)
            results.append((name, int(price.replace(",", ""))))
        except AttributeError:
            continue

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    print("Productos encontrados (Nuevos, en CDMX, Mayor a Menor precio):")
    for i, (name, price) in enumerate(sorted_results[:5], 1):
        print(f"{i}. {name} - ${price}")

examenmercadolibre()