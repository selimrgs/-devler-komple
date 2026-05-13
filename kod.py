import streamlit as st
import requests
import xml.etree.ElementTree as ET

def kripto_verileri():
    cevap = requests.get("https://api.coinlore.net/api/ticker/?id=90,80,48543,2710,58,2,1,5,4321")
    veriler = cevap.json()
    return {coin['symbol']: float(coin['price_usd']) for coin in veriler}

def tcmb_verileri():
    r = requests.get("https://www.tcmb.gov.tr/kurlar/today.xml")
    root = ET.fromstring(r.content)
    veriler = {}
    for currency in root.findall('Currency'):
        kod = currency.get('CurrencyCode')
        if kod:
            birim = int(currency.find('Unit').text)
            fiyat_metni = currency.find('ForexBuying').text
            if fiyat_metni:
                veriler[kod] = float(fiyat_metni) / birim
    return veriler

st.set_page_config(page_title="Hesapci")
st.title("Hesapci")

kripto = kripto_verileri()
doviz = tcmb_verileri()

arama = st.text_input("", value="")

if arama:
    if arama in kripto:
        st.subheader(f"{arama}")
        miktar = st.text_input("Miktar:", value="1.0")
        if miktar:
            sonuc = float(miktar) * kripto[arama]
            st.write(f"Deger: {sonuc:,.2f} USD")
            
    elif arama in doviz:
        st.subheader(f"{arama}")
        miktar = st.text_input("TL Tutari:", value="100.0")
        if miktar:
            sonuc = float(miktar) / doviz[arama]
            st.write(f"Sonuc: {sonuc:.2f} {arama}")
            st.write(f"Kur: {doviz[arama]:.4f}")
