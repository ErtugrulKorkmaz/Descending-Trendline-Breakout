import yfinance as yf
import pandas as pd
import numpy as np
import talib
import mplfinance as mpf
import time
import os
from scipy.stats import linregress
from scipy.signal import argrelextrema
from datetime import datetime

# --- AYARLAR ---
LOOKBACK_PERIOD = 250    
PIVOT_WINDOW = 5        
VOLUME_MULTIPLIER = 1.5  
RISK_REWARD_1 = 1.5      
RISK_REWARD_2 = 2.5      
SAVE_FOLDER = "Sinyal_Grafikleri" 

# Klasör yoksa oluştur
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def get_bist30_tickers():
    return ['A1CAP.IS', 'ADESE.IS','ADGYO.IS', 'AEFES.IS', 'AFYON.IS','AGHOL.IS', 'AGESA.IS', 'AGROT.IS', 'AGYO.IS','AHGAZ.IS', 'AHSGY.IS', 'AKBNK.IS', 'AKCNS.IS', 'AKENR.IS', 'AKFGY.IS', 'AKFYE.IS', 'AKGRT.IS', 'AKGRT.IS', 'AKMGY.IS', 'AKMGY.IS', 'AKSEN.IS', 'AKSGY.IS','AKSUE.IS', 'AKYHO.IS', 'ALARK.IS','ALBRK.IS', 'ALCAR.IS', 'ALCTL.IS', 'ALFAS.IS', 'ALKIM.IS', 'ALKLC.IS', 'ALKA.IS', 'ALMAD.IS', 'ALVES.IS', 'ALTNY.IS', 'ANGEN.IS', 'ANELE.IS', 'ANHYT.IS', 'ARCLK.IS', 'ARDYZ.IS', 'ARENA.IS', 'ARSAN.IS', 'ARTMS.IS', 'ARZUM.IS', 'ASELS.IS', 'ASGYO.IS', 'ASTOR.IS', 'ATAGY.IS', 'ATAKP.IS', 'ATATP.IS', 'ATEKS.IS', 'ATLAS.IS', 'ATSYH.IS', 'AVHOL.IS', 'AVGYO.IS', 'AVOD.IS', 'AVPGY.IS', 'AVTUR.IS', 'AYDEM.IS', 'AYEN.IS', 'AYES.IS', 'AYGAZ.IS', 'AZTEK.IS', 'BAGFS.IS', 'BAHKM.IS', 'BAKAB.IS', 'BALAT.IS', 'BANVT.IS', 'BARMA.IS', 'BASCM.IS', 'BASGZ.IS', 'BAYRK.IS', 'BEGYO.IS', 'BEYAZ.IS', 'BFREN.IS', 'BIMAS.IS','BINHO.IS', 'BIOEN.IS', 'BIENY.IS', 'BIGCH.IS', 'BIZIM.IS', 'BJKAS.IS','BLCYT.IS', 'BMSCH.IS', 'BMSTL.IS', 'BNTAS.IS', 'BOBET.IS', 'BOSSA.IS', 'BORLS.IS', 'BORSK.IS', 'BRISA.IS', 'BRKSN.IS', 'BRKVY.IS', 'BRLSM.IS', 'BRMEN.IS', 'BRYAT.IS', 'BSOKE.IS', 'BTCIM.IS', 'BURCE.IS', 'BURVA.IS', 'BUCIM.IS', 'BVSAN.IS', 'BYDNR.IS','CIMSA.IS', 'CANTE.IS', 'CASA.IS', 'CATES.IS', 'CCOLA.IS', 'CEOEM.IS', 'CELHA.IS', 'CEMAS.IS', 'CEMTS.IS', 'CEMZY.IS', 'CLEBI.IS',   'CONSE.IS', 'COSMO.IS', 'CRDFA.IS', 'CRFSA.IS', 'CVKMD.IS', 'CWENE.IS', 'CUSAN.IS', 'DAGHL.IS', 'DAGI.IS', 'DAPGM.IS', 'DARDL.IS',  'DCTTR.IS', 'DEVA.IS', 'DGATE.IS', 'DENGE.IS', 'DERHL.IS', 'DERIM.IS', 'DESA.IS', 'DESPC.IS', 'DGNMO.IS', 'DGNMO.IS', 'DIRIT.IS', 'DITAS.IS', 'DMSAS.IS', 'DMRGD.IS', 'DNISI.IS', 'DOAS.IS', 'DOBUR.IS', 'DOCO.IS', 'DOGUB.IS', 'DOFER.IS', 'DOHOL.IS', 'DOKTA.IS', 'DURDO.IS', 'DURKN.IS', 'DZGYO.IS', 'ECILC.IS', 'ECZYT.IS', 'EDIP.IS', 'EFORC.IS', 'EGEEN.IS', 'EGGUB.IS', 'EGPRO.IS', 'EGSER.IS', 'EKGYO.IS', 'EKIZ.IS', 'ELITE.IS', 'EMNIS.IS', 'EMKEL.IS', 'ENJSA.IS', 'ENKAI.IS', 'ENSRI.IS', 'ERBOS.IS', 'EREGL.IS', 'ERSU.IS', 'ESCAR.IS', 'ESCOM.IS', 'ESEN.IS', 'ETILR.IS', 'ETYAT.IS', 'EUKYO.IS', 'EUREN.IS', 'EUYO.IS', 'FADE.IS', 'FENER.IS', 'FENER.IS','EDATA.IS',   'FLAP.IS', 'FMIZP.IS', 'FONET.IS', 'FORMT.IS', 'FORTE.IS', 'FRIGO.IS', 'FROTO.IS', 'FZLGY.IS', 'GARAN.IS', 'GARFA.IS', 'GEDIK.IS', 'GEDZA.IS', 'GENIL.IS', 'GENTS.IS', 'GESAN.IS', 'GIPTA.IS', 'GLBMD.IS', 'GLCVY.IS', 'GLRYH.IS', 'GLYHO.IS', 'GMTAS.IS', 'GOKNR.IS', 'GOLTS.IS', 'GOODY.IS', 'GOZDE.IS', 'GRNYO.IS', 'GRSEL.IS', 'GRTHO.IS', 'GSRAY.IS', 'GSDDE.IS', 'GSDHO.IS', 'GUBRF.IS', 'GUNDG.IS', 'GWIND.IS', 'GZNMI.IS', 'HALKB.IS',   'HATEK.IS', 'HATSN.IS', 'HDFGS.IS',  'HEDEF.IS', 'HEKTS.IS', 'HLGYO.IS',   'HKTM.IS', 'HOROZ.IS', 'HRKET.IS', 'HTTBT.IS', 'HUBVC.IS', 'HUNER.IS',  'HURGZ.IS',  'ICBCT.IS', 'ICUGS.IS', 'IDGYO.IS', 'IEYHO.IS', 'IHAAS.IS', 'IHEVA.IS', 'IHGZT.IS', 'IHLAS.IS', 'IHLGM.IS', 'IHYAY.IS', 'IMASM.IS', 'INDES.IS', 'INGRM.IS', 'INTEK.IS', 'INTEM.IS', 'INVEO.IS', 'INVES.IS',  'IPEKE.IS', 'ISATR.IS', 'ISBIR.IS', 'ISBTR.IS', 'ISCTR.IS', 'ISDMR.IS', 'ISFIN.IS', 'ISGYO.IS', 'ISGSY.IS', 'ISKPL.IS', 'ISKUR.IS', 'ISMEN.IS', 'ISSEN.IS', 'ISYAT.IS', 'IZENR.IS', 'IZFAS.IS', 'IZINV.IS', 'IZMDC.IS', 'JANTS.IS', 'KAPLM.IS', 'KAREL.IS', 'KARSN.IS', 'KARYE.IS', 'KARTN.IS', 'KATMR.IS', 'KAYSE.IS', 'KCAER.IS', 'KCHOL.IS', 'KFEIN.IS',  'KGYO.IS', 'KIMMR.IS', 'KLGYO.IS', 'KLKIM.IS', 'KLMSN.IS', 'KLRHO.IS', 'KLSER.IS', 'KLSYN.IS', 'KMPUR.IS', 'KNFRT.IS', 'KONKA.IS', 'KONTR.IS', 'KONYA.IS', 'KOPOL.IS', 'KORDS.IS', 'KRPLS.IS', 'KRONT.IS', 'KRSTL.IS', 'KRVGD.IS', 'KRTEK.IS', 'KRGYO.IS', 'KRDMA.IS', 'KRDMB.IS', 'KRDMD.IS', 'KSTUR.IS',  'KTLEV.IS', 'KUYAS.IS', 'KUVVA.IS', 'KZBGY.IS', 'KZGYO.IS', 'LIDFA.IS', 'LIDER.IS', 'LILAK.IS', 'LINK.IS', 'LKMNH.IS', 'LMKDC.IS', 'LOGO.IS', 'LRSHO.IS', 'LUKSK.IS', 'LYDHO.IS', 'MACKO.IS', 'MAGEN.IS', 'MAKIM.IS', 'MAKTK.IS', 'MAALT.IS', 'MANAS.IS', 'MARKA.IS', 'MARTI.IS', 'MAVI.IS', 'MEGAP.IS', 'MEGMT.IS', 'MEKAG.IS', 'MERCN.IS', 'MERIT.IS', 'MERKO.IS', 'METRO.IS', 'METUR.IS', 'MGROS.IS', 'MIATK.IS', 'MNDTR.IS', 'MNDRS.IS', 'MOBTL.IS', 'MOGAN.IS', 'MPARK.IS', 'MRGYO.IS', 'MRSHL.IS', 'MSGYO.IS', 'MTRKS.IS', 'MTRYO.IS', 'MZHLD.IS', 'NATEN.IS', 'NETAS.IS', 'NIBAS.IS', 'NTHOL.IS', 'NUHCM.IS', 'NUGYO.IS',  'ODAS.IS', 'ODINE.IS', 'OFSYM.IS', 'OBASE.IS', 'OBAMS.IS','ONCSM.IS', 'ONRYT.IS', 'ORCAY.IS', 'ORGE.IS', 'ORMA.IS', 'OSMEN.IS', 'OSTIM.IS', 'OTKAR.IS', 'OTTO.IS', 'OYAKC.IS', 'OYAYO.IS', 'OYLUM.IS', 'OZATD.IS', 'OZKGY.IS', 'OZGYO.IS', 'OZYSR.IS', 'OZRDN.IS', 'OZSUB.IS', 'PAGYO.IS', 'PAMEL.IS', 'PAPIL.IS', 'PARSN.IS', 'PASEU.IS', 'PATEK.IS', 'PCILT.IS', 'PEKGY.IS', 'PENGD.IS', 'PENTA.IS', 'PEHOL.IS', 'PETKM.IS', 'PETUN.IS', 'PGSUS.IS', 'PKART.IS', 'PKENT.IS', 'PKENT.IS', 'PKENT.IS', 'PKENT.IS', 'PNSUT.IS', 'POLHO.IS', 'POLTK.IS', 'PRDGS.IS', 'PRKME.IS', 'PRKAB.IS', 'PRZMA.IS', 'PSGYO.IS', 'PSDTC.IS', 'QNBFB.IS',  'QNBFL.IS', 'QUAGR.IS',   'RALYH.IS', 'RAYSG.IS', 'RNPOL.IS', 'RODRG.IS', 'ROYAL.IS', 'RTALB.IS', 'RUBNS.IS', 'RYGYO.IS', 'RYSAS.IS', 'SAFKR.IS', 'SAHOL.IS', 'SAMAT.IS', 'SANEL.IS', 'SANKO.IS', 'SANFM.IS', 'SARKY.IS', 'SASA.IS', 'SAYAS.IS', 'SELEC.IS', 'SEYKM.IS', 'SEKFK.IS', 'SEGYO.IS', 'SELEC.IS', 'SELGD.IS', 'SELVA.IS',  'SILVR.IS', 'SISE.IS', 'SKBNK.IS', 'SKTAS.IS', 'SMART.IS',   'SMRTG.IS', 'SNGYO.IS', 'SNICA.IS', 'SNKRN.IS', 'SODSN.IS', 'SOKE.IS', 'SONME.IS', 'SUMAS.IS', 'SUNTK.IS', 'SURGY.IS', 'SUWEN.IS', 'TABGD.IS',    'TAVHL.IS', 'TATGD.IS', 'TATEN.IS', 'TBORG.IS', 'TCELL.IS', 'TCKRC.IS',  'TDGYO.IS', 'TEKTU.IS', 'TERA.IS', 'THYAO.IS', 'TKFEN.IS', 'TKNSA.IS', 'TLMAN.IS', 'TMSN.IS', 'TOASO.IS', 'TRCAS.IS', 'TRGYO.IS', 'TRILC.IS',      'TSKB.IS', 'TSGYO.IS', 'TSPOR.IS', 'TTKOM.IS', 'TTRAK.IS', 'TUPRS.IS', 'TURGG.IS', 'TUREX.IS', 'UFUK.IS', 'ULAS.IS', 'ULKER.IS', 'ULUFA.IS', 'ULUSE.IS', 'ULUUN.IS', 'UNLU.IS', 'USAK.IS', 'VAKBN.IS', 'VAKFN.IS', 'VAKKO.IS', 'VANGD.IS', 'VBTYZ.IS','VERUS.IS', 'VERTU.IS', 'VESBE.IS', 'VESTL.IS', 'VKFYO.IS', 'VKGYO.IS', 'VKING.IS', 'YAPRK.IS', 'YATAS.IS', 'YAYLA.IS', 'YAYLA.IS', 'YBTAS.IS', 'YEOTK.IS', 'YESIL.IS', 'YGYO.IS', 'YIGIT.IS', 'YKBNK.IS', 'YKSLN.IS', 'YONGA.IS', 'YUNSA.IS', 'YYAPI.IS', 'YYLGD.IS', 'ZEDUR.IS',  'ZOREN.IS', 'ZRGYO.IS']

def plot_signal(df, symbol, slope, intercept, pivots_idx):
    """
    Sinyal gelen hissenin grafiğini ve trend çizgisini çizer/kaydeder.
    """
    try:
        lookback_plot = 150
        if len(df) > lookback_plot:
            plot_df = df.iloc[-lookback_plot:]
        else:
            plot_df = df

        first_pivot_global_idx = df.index.get_loc(pivots_idx[0])
        last_global_idx = len(df) - 1
        
        price_start = (slope * first_pivot_global_idx) + intercept
        price_end = (slope * last_global_idx) + intercept
        
        date_start = df.index[first_pivot_global_idx]
        date_end = df.index[last_global_idx]
        

        trend_line = [(date_start, price_start), (date_end, price_end)]


        mc = mpf.make_marketcolors(up='green', down='red', edge='i', wick='i', volume='in', inherit=True)
        s = mpf.make_mpf_style(marketcolors=mc, gridstyle=':', y_on_right=True)
        
        filename = f"{SAVE_FOLDER}/{symbol}_{datetime.now().strftime('%Y%m%d')}.png"
        
        print(f"   >>> Grafik Çiziliyor: {filename}")
        
        mpf.plot(plot_df, 
                 type='candle', 
                 volume=True, 
                 style=s, 
                 title=f"\n{symbol} - TREND KIRILIMI (Slope: {slope:.4f})",
                 alines=dict(alines=trend_line, colors=['cyan'], linewidths=2.5, linestyle='-'),
                 vlines=dict(vlines=date_end, colors=['gold'], linewidths=1, alpha=0.5),
                 savefig=filename
                 )
        
    except Exception as e:
        print(f"   !!! Grafik Hatası ({symbol}): {e}")

def analyze_stock(symbol):
    try:
        df = yf.download(symbol, period="1y", interval="1d", progress=False)
        if len(df) < 50: return None
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)


        df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
        df['Vol_SMA'] = df['Volume'].rolling(window=20).mean()
        

        df['is_pivot'] = df.iloc[argrelextrema(df['High'].values, np.greater_equal, order=PIVOT_WINDOW)[0]]['High']
        pivots = df[df['is_pivot'].notna()]
        
        if len(pivots) < 3: return None

        last_pivots = pivots.iloc[-3:-1]
        if len(last_pivots) < 2: return None

        x_pivots = [df.index.get_loc(idx) for idx in last_pivots.index]
        y_pivots = last_pivots['High'].values
        
        slope, intercept, _, _, _ = linregress(x_pivots, y_pivots)
        

        if slope >= -0.02: return None 

        current_idx = len(df) - 1
        trendline_val = slope * current_idx + intercept
        
        current_close = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2]
        current_vol = df['Volume'].iloc[-1]
        avg_vol = df['Vol_SMA'].iloc[-1]

        breakout = (prev_close < trendline_val) and (current_close > trendline_val)
        vol_check = current_vol > (avg_vol * VOLUME_MULTIPLIER)
        
        engulfing = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
        marubozu = talib.CDLMARUBOZU(df['Open'], df['High'], df['Low'], df['Close'])
        candle_signal = (engulfing.iloc[-1] != 0) or (marubozu.iloc[-1] != 0)

        if breakout and vol_check:
            plot_signal(df, symbol, slope, intercept, last_pivots.index)
            
            atr = df['ATR'].iloc[-1]
            stop_loss = df['Low'].iloc[-1] - (atr * 0.2)
            entry_price = current_close
            risk = entry_price - stop_loss
            

            if risk < atr * 0.5:
                stop_loss = entry_price - (atr * 1.5)
                risk = entry_price - stop_loss

            return {
                "Sembol": symbol,
                "Fiyat": round(entry_price, 2),
                "Mum_Teyidi": "VAR" if candle_signal else "YOK",
                "Stop": round(stop_loss, 2),
                "TP1": round(entry_price + risk * RISK_REWARD_1, 2),
                "TP2": round(entry_price + risk * RISK_REWARD_2, 2),
                "Hacim_Kat": round(current_vol/avg_vol, 1)
            }
            
    except Exception as e:
        return None
    return None

def run_scanner():
    print(f"--- TARAMA BAŞLIYOR: BIST 30 ({datetime.now().strftime('%H:%M')}) ---")
    print(f"Kriter: Düşen Trend Kırılımı + Hacim (x{VOLUME_MULTIPLIER})")
    print(f"Grafikler '{SAVE_FOLDER}' klasörüne kaydedilecek.\n")
    
    tickers = get_bist30_tickers()
    results = []
    
    for ticker in tickers:
        print(f"Taranıyor: {ticker:<10}", end="\r")
        signal = analyze_stock(ticker)
        if signal:
            results.append(signal)
            print(f"BULUNDU: {ticker:<10} (Grafik Kaydedildi)        ")
        
        time.sleep(0.3) 
        
    print("\n" + "="*70)
    
    if results:
        df_res = pd.DataFrame(results)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        print(df_res[['Sembol', 'Fiyat', 'Stop', 'TP1', 'TP2', 'Hacim_Kat', 'Mum_Teyidi']])
        print("="*70)
        print(f"Toplam {len(results)} hisse bulundu. Detaylı grafikler klasörde.")
    else:
        print("Kriterlere uyan hisse bulunamadı.")

if __name__ == "__main__":
    run_scanner()
