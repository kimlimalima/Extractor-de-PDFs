from bs4 import BeautifulSoup

import os, re, requests, time

# Exemplo de url que deve ser inserida na lista
urls = ["https://www.google.com/search?q=%22naruto%22+filetype%3A+pdf&oq=%22naruto%22+filetype%3A+pdf&aqs=chrome..69i57.13079j0j7&sourceid=chrome&ie=UTF-8"]

# Local que contém respectivamente o path da pasta que está sendo utilizada para testes do extractor e a pasta que está sendo alimentada com os pdf catalogados.
pathPastaLocal = input("insira o caminho da pasta que armazenará os arquivos: ")
pause = time.sleep(1)

# Captura dos links páginas de busca do google.
def linksPaginasDeBusca(urls):
    listaLinksPagesExtraidos = []
    for url in urls:
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.text, 'html.parser') 
        pause
        # Extraído os links das páginas do google
        for link in soup.find_all('a', attrs={'href': re.compile("^/search")}):
            link = link.get('href')
            listaLinksPagesExtraidos.append(f"https://www.google.com{link}")
            pause
        
    return listaLinksPagesExtraidos

listaLinksPagesExtraidos = linksPaginasDeBusca(urls)
pause

# Extaindo o link dos pdfs
def extracaoLinksPDFs(listaLinksPagesExtraidos):
    listaDeUrlsPDF = []
    for link in listaLinksPagesExtraidos:
        html_document = requests.get(link)
        pause
        soup = BeautifulSoup(html_document.text, 'html.parser')
        # testeste
        # Créditos Samuel, o cirurgião do regex.
        for url in soup.find_all('a', attrs={'href': re.compile(r'.*\.pdf')}):
            urls = re.findall(r"(?<=/url\?q=).*\.pdf", url.get("href"))[0]
            listaDeUrlsPDF.append(urls)

    return listaDeUrlsPDF

listaDeUrlsPDF = extracaoLinksPDFs(listaLinksPagesExtraidos)

# Realizando o download dos pdfs
def downloadPDF(listaDeUrlsPDF, pathPastaLocal):
    try:
        listaDeUrlsPDF = set(listaDeUrlsPDF)
        for url in listaDeUrlsPDF:
            response = requests.get(url)
            pause

            if response.status_code == 200:
                arquivo_path = os.path.join(pathPastaLocal, os.path.basename(url))
                with open(arquivo_path, "wb") as f:
                    f.write(response.content)

    except Exception:
        pass

print(downloadPDF(listaDeUrlsPDF, pathPastaLocal))