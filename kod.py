import streamlit as st
import requests
import xml.etree.ElementTree as ET

def kripto_verileri():
    # Coinlore uzerinden geniş bir liste çekiyoruz
    cevap = requests.get("https://api.coinlore.net/api/ticker/?id=90,80,48543,2710,58,2,1,5,4321")
    veriler = cevap.json()
    return {coin['symbol'].upper(): float(coin['price_usd']) for coin in veriler}

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
                veriler[kod.upper()] = float(fiyat_metni) / birim
    return veriler

st.set_page_config(page_title="Hesapci")
st.title("Hesapci")

kripto = kripto_verileri()
doviz = tcmb_verileri()

# Arama motoru mantigi
arama = st.text_input("Kur veya Coin Ara (Ornek: BTC, USD, ETH, RUB):", "").upper()

if arama:
    if arama in kripto:
        st.subheader(f"{arama} - USD Cevirici")
        miktar = st.text_input("Miktar Girin:", value="1.0")
        if miktar:
            sonuc = float(miktar) * kripto[arama]
            st.write(f"Sonuc: {sonuc:,.2f} USD")
            
    elif arama in doviz:
        st.subheader(f"{arama} - TL Cevirici")
        miktar = st.text_input("TL Tutari Girin:", value="100.0")
        if miktar:
            sonuc = float(miktar) / doviz[arama]
            st.write(f"Sonuc: {sonuc:.2f} {arama}")
            st.write(f"Guncel Kur: {doviz[arama]:.4f}")
    else:
        st.warning("Kur bulunamadi. Lutfen gecerli bir sembol girin.")
else:
    st.info("Hesaplamak istediginiz birimi yukariya yazin.")
