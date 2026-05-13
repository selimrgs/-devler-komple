import streamlit as st
import requests
import xml.etree.ElementTree as ET

def kripto_verileri():
    cevap = requests.get("https://api.coinlore.net/api/ticker/?id=90,80")
    veriler = cevap.json()
    return {coin['symbol']: float(coin['price_usd']) for coin in veriler}

def tcmb_verileri():
    r = requests.get("https://www.tcmb.gov.tr/kurlar/today.xml")
    root = ET.fromstring(r.content)
    veriler = {}
    hedefler = {'USD': 'ABD DOLARI', 'EUR': 'EURO', 'RUB': 'RUS RUBLESİ', 'JPY': 'JAPON YENİ'}
    
    for currency in root.findall('Currency'):
        kod = currency.get('CurrencyCode')
        if kod in hedefler:
            birim = int(currency.find('Unit').text)
            fiyat = float(currency.find('ForexBuying').text)
            veriler[kod] = fiyat / birim
    return veriler

st.set_page_config(page_title="Finans Paneli")
st.title("Doviz ve Kripto Hesaplayici")

kripto = kripto_verileri()
doviz = tcmb_verileri()

st.subheader("Kripto Para Cevirici")
kripto_secim = st.selectbox("Coin Secin:", list(kripto.keys()))
kripto_miktar = st.number_input(f"{kripto_secim} Miktari:", value=1.0)
st.write(f"Deger: {kripto_miktar * kripto[kripto_secim]:,.2f} USD")

st.divider()

st.subheader("Doviz Cevirici (TL)")
doviz_secim = st.selectbox("Doviz Turu:", list(doviz.keys()))
tl_miktar = st.number_input("TL Tutari Girin:", value=100.0)
sonuc = tl_miktar / doviz[doviz_secim]
st.write(f"Sonuc: {sonuc:.2f} {doviz_secim}")
st.write(f"Guncel Kur: {doviz[doviz_secim]:.4f}")
