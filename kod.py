import streamlit as st
import requests
import xml.etree.ElementTree as ET

def btc_fiyat_al():
    istek = requests.get("https://api.coinlore.net/api/ticker/?id=90")
    return float(istek.json()[0]['price_usd'])

def tcmb_verileri():
    r = requests.get("https://www.tcmb.gov.tr/kurlar/today.xml")
    root = ET.fromstring(r.content)
    veriler = {}
    for currency in root.findall('Currency'):
        kod = currency.get('CurrencyCode')
        if kod in ['USD', 'EUR']:
            veriler[kod] = float(currency.find('ForexBuying').text)
    return veriler

st.set_page_config(page_title="Kur Hesaplayici")
st.title("Kur Hesaplama Paneli")

tab1, tab2 = st.tabs(["Bitcoin Hesaplayici", "Merkez Bankasi Kurlari"])

with tab1:
    btc_usd = btc_fiyat_al()
    st.metric("1 BTC / USD", f"{btc_usd:,}$")
    miktar = st.number_input("BTC Miktari Girin:", min_value=0.0, value=1.0)
    st.write(f"Toplam Deger: {miktar * btc_usd:,} USD")

with tab2:
    kurlar = tcmb_verileri()
    st.subheader("TCMB Efektif Alis")
    
    secilen_kur = st.selectbox("Cevrilecek Doviz:", ["USD", "EUR"])
    tl_miktari = st.number_input("TL Tutari Girin:", min_value=0.0)
    
    kur_degeri = kurlar[secilen_kur]
    sonuc = tl_miktari / kur_degeri
    st.write(f"{tl_miktari} TL = {sonuc:.2f} {secilen_kur}")
    st.write(f"Guncel {secilen_kur} Kuru: {kur_degeri} TL")
