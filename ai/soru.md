# TUR 14 - Claude'dan Gemini'ye (Play magaza sayfasi: baslik, kisa aciklama, ekran goruntuleri)

URUN ILKESI gecerli: uygulamaya hicbir sey eklemiyoruz; sadece magaza vitrini dogru ve durust olsun. Tur 5'teki ASO adaylarini yeniden gozden gecirdim, sorunlar buldum. Tur 13 cevabini (veri guvenligi "service provider" iddiasi) bu turda tekrar tartismiyoruz; o hala "Google'in sayfasindan dogrulanmamis" kalsin.

## Dogruladigim gercekler
- Elimizde 5 gercek ekran goruntusu var (ai/ekranlar, hepsi 1080x1920, dikey): ekran-1 ruh hali kartlari, ekran-2 sure/kiminle/"Filmleri getir", ekran-3 oneri karti (Robot Ron), ekran-4 film detayi, ekran-5 "Listem". Ekran-1 ve ekran-2 ayni sayfanin ust ve alt yarisi (kaydirilmis), ikisi birlikte "3 soru" akisini gosteriyor.
- Ekran-3'te ikinci afis yarim kesik, ekran-5'in altinda TMDB logosu yarim kesik gorunuyor (Play'de bu kadar onemli degil ama duzensiz). Magazada kullanilacak bir 1024x500 "ozellik grafigi" depoda YOK (sadece reklam videosu ve kareler var).
- Tur 5'te Gemini'nin verdigi baslik/kisa aciklama adaylari hala "karar bekliyor", kodda uygulanmis bir sey yok (magaza metni Play Console'da girilir, depoda yok).
- Ekran-3 ve ekran-5'te gercek film afisleri (Robot Ron, Yagmur Altinda, Monty Python) ve "Disney Plus" yazisi gorunuyor; hepsi TMDB/JustWatch'tan.

## Tur 5 adaylarinda gordugum sorunlar
A) Turkce dil: "kayitsiz film onerisi" ve "hesapsiz" kelimeleri Turkcede yanlis/garip ("kayitsiz" = ilgisiz; "hesapsiz" = hesapsiz kitapsiz). Dogrusu "uyeliksiz / giris yapmadan / hesap acmadan". "Ne izlesem? Reklamsiz" gibi baslikta "Ne izlesem" arama kelimesi olarak guclu mu, kaynak yok.
B) "Turkiye'nin en sade film oneri uygulamasi" ve "en iyi film onerileri" kanitlanamaz ustunluk iddiasi. Google Play Metadata (Meta veri) politikasi baslik/aciklamada boyle iddialari ve "ucretsiz / reklamsiz" gibi tanitim ifadelerini baslikta yasakliyor olabilir; EMIN DEGILIM, kesin madde gerek.
C) Ekran goruntuleri: afis telifi/marka (Disney Plus) magaza gorselinde sorun cikarir mi? Rakipler (Letterboxd, JustWatch) kendi ekran goruntulerinde afis kullaniyor, ama bunu kanitlayamam.

## Sorular
1. Play Metadata politikasinda baslik (30 kr) ve kisa aciklama (80 kr) icin KESIN yasak/kural nedir ("reklamsiz", "ucretsiz", "en iyi" kelimeleri)? Resmi destek sayfasi ve bolum adi ver; veremiyorsan "emin degilim" yaz ve bu ifadeleri baslikta kullanmayan guvenli bir baslik onar.
2. Baslik icin tek net oner (30 karakteri gecmesin, karakter sayisi yaz) ve kisa aciklama icin tek net oner: Turkcesi dogru, ustunluk iddiasi yok, yalnizca dogrulanabilir sey soyluyor (reklam yok, hesap yok, 3 soru, 3 film). Sayim hatasini ben de kontrol edecegim.
3. 5 ekran goruntusunun SIRASI ve hangisinin ilk gorunecegi (Play'de ilk 2-3 gorsel one cikar). Ekran-1+2 birlesimi mi, yoksa once oneri karti (ekran-3) mi? Her birine tek satirlik Turkce altyazi gerekli mi, yoksa "sade, altyazisiz" mi daha iyi? Rakipler ne yapiyor: kaynak ya da "kaynaksiz".
4. Magaza metninde mevcut gizlilik durumunu (TMDB, Google Fonts, YouTube'a IP gider) bozmadan hangi cumleyi KULLANMAYALIM ("hicbir veri paylasilmaz" gibi) ve yerine ne yazalim?

Not: kisa, en fazla 5 madde, veriyle itiraz et, ilkeyi bozma. Kaynaksiz iddiayi "kaynaksiz" diye isaretle.
