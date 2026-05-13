import streamlit as st
import requests
import xml.etree.ElementTree as ET

def kripto_verileri():
    cevap = requests.get("https://api.coinlore.net/api/ticker/?id=90,80,48543,2710")
    veriler = cevap.json()
    return {coin['symbol']: float(coin['price_usd']) for coin in veriler}

def tcmb_verileri():
    r = requests.get("https://www.tcmb.gov.tr/kurlar/today.xml")
    root = ET.fromstring(r.content)
    veriler = {}
    hedefler = ['USD', 'EUR', 'RUB', 'JPY', 'GBP', 'CHF']
    for currency in root.findall('Currency'):
        kod = currency.get('CurrencyCode')
        if kod in hedefler:
            birim = int(currency.find('Unit').text)
            fiyat = float(currency.find('ForexBuying').text)
            veriler[kod] = fiyat / birim
    return veriler

st.set_page_config(page_title="Hesapci")
st.title("Hesapci")

kripto = kripto_verileri()
doviz = tcmb_verileri()

st.subheader("Kripto Degerleri (USD)")
# Artik btc/eth arasinda secim yapmana gerek yok, hepsi ekranda
for sembol, fiyat in kripto.items():
    miktar = st.text_input(f"{sembol} Miktari:", value="0.0", key=sembol)
    if miktar and float(miktar) > 0:
        st.write(f"{miktar} {sembol} = **{float(miktar) * fiyat:,.2f} USD**")

st.divider()

st.subheader("Doviz Cevirici (TL)")

for kod, kur in doviz.items():
    tl_giris = st.text_input(f"{kod} icin TL miktari girin:", value="0.0", key=kod)
    if tl_giris and float(tl_giris) > 0:
        sonuc = float(tl_giris) / kur
        st.write(f"{tl_giris} TL = **{sonuc:.2f} {kod}** (Kur: {kur:.4f})")
