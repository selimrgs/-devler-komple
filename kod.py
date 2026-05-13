import streamlit as st
import requests
import xml.etree.ElementTree as ET

def kripto_verileri():
    # Tum populer coinleri cekmek icin limiti artirdik
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
                fiyat = float(fiyat_metni)
                veriler[kod] = fiyat / birim
    return veriler

st.set_page_config(page_title="Hesapci")
st.title("Hesapci")

try:
    kripto = kripto_verileri()
    doviz = tcmb_verileri()

    st.subheader("Kripto Para Cevirici")
    kripto_secim = st.selectbox("Coin Secin:", list(kripto.keys()))
    # Arti eksi butonlari olmamasi icin text_input kullaniyoruz
    kripto_miktar_str = st.text_input(f"{kripto_secim} Miktari:", value="1.0")
    kripto_miktar = float(kripto_miktar_str) if kripto_miktar_str else 0.0
    st.write(f"Deger: {kripto_miktar * kripto[kripto_secim]:,.2f} USD")

    st.divider()

    st.subheader("Doviz Cevirici (TL)")
    doviz_secim = st.selectbox("Doviz Turu:", list(doviz.keys()))
    tl_miktar_str = st.text_input("TL Tutari Girin:", value="100.0")
    tl_miktar = float(tl_miktar_str) if tl_miktar_str else 0.0
    sonuc = tl_miktar / doviz[doviz_secim]
    st.write(f"Sonuc: {sonuc:.2f} {doviz_secim}")
    st.write(f"Guncel Kur: {doviz[doviz_secim]:.4f}")

except Exception as e:
    st.error("Veriler alinirken bir hata olustu.")
