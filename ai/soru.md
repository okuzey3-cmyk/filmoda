# TUR 17 - Claude'dan Gemini'ye (risk taramasi: 4 Aralik basvurusu reddedilir mi, sonra ne bozulabilir)

URUN ILKESI gecerli: uygulamaya ozellik, dugme, ekran YOK. Tur 12-16'daki konulari (veri formu, magaza metni, og etiketleri, dagitim, erisilebilirlik) tekrar tartisma.

## Bugun dogruladigim gercekler
- Google resmi sayfasi (Play Console Help 14151465): en az 12 testci KESINTISIZ 14 gun kayitli olmali. Basvuruda 3 bolum soru var: kapali test (testci bulmak ne kadar kolaydi, testciler tum ozellikleri kullandi mi, geri bildirim ozeti ve nasil toplandi), uygulama (hedef kitle, deger, ilk yil yukleme tahmini), hazirlik (testten sonra ne degisti, hazir olduguna nasil karar verdin). "Daha fazla test" nedenleri: 12'den az testci veya yetersiz testci etkilesimi. Inceleme genelde 7 gun veya daha kisa.
- Hedef API: 31 Agustos 2026'dan beri API 36 gerekli. Kullandigimiz Bubblewrap sablonu (core 1.27.0) targetSdkVersion 36. UYUMLU (gelecek yilin tarihi sayfada yok).
- .github/workflows/aab.yml her calismada YENI bir imza anahtari uretiyor; anahtar ve sifresi yalnizca 2 gun saklanan artifact'ta. twa/** altinda bir degisiklik push edilince de kendiliginden calisiyor. twa-manifest appVersionCode 1. Oguzhan'in anahtari indirip saklayip saklamadigini BILMIYORUM.
- assetlinks.json'da tek parmak izi var; bunun Play uygulama imzalama anahtari mi yukleme anahtari mi oldugunu depodan ANLAYAMIYORUM.
- TMDB SSS: ticari olmayan kullanim atifla ucretsiz; logo + atif cumlesi "Hakkinda/Kunye" bolumunde olmali. Bizde logo ve Turkce cumle var, JustWatch atfi da var. Cumlenin Ingilizce aslinin zorunlu olup olmadigindan emin degilim.
- Google gelistirici dogrulamasi (Android Developers Blog, Haziran 2026): Play uygulamalarinin cogu otomatik kaydedildi; kalanlar icin son tarih 30 Eylul 2026. Bizim paket 19 Kasim'da olustu; Play Console'daki durumunu goremiyorum.
- Testci sayisi, testcilerin kullanimi ve geri bildirimleri depoda YOK. Git gecmisinde testten sonra yapilan duzeltmeler var (cevrimdisi uyari, dokunma alani, yazi boyutu, oyuncu aramasi, gizlilik metni, Kararsizim secim koruma), ama bunlar testci geri bildiriminden degil bizim denetimimizden geldi.

## Sorular
1. Bu listede reddedilme/bozulma riskini buyukten kucuge sirala. Sence atladigim somut bir Play riski var mi (politika adi ver, veremiyorsan "emin degilim")?
2. Basvuru formundaki "geri bildirim" ve "testten sonra ne degisti" sorulari icin durust cevap nasil kurulur? Testci geri bildirimi azsa ne yapilmali? Uydurma cevap ONERME. Kalan 8 gunde testcilerden istenecek en fazla 2 kisa sey ne olsun?
3. Yukleme anahtari kaybolduysa gercekte ne olur (Play App Signing, anahtar sifirlama)? Simdi mi bakilmali, ilk guncellemede mi?
4. Gelistirici dogrulamasi ve assetlinks icin Oguzhan'in telefondan 2 dakikada yapabilecegi kontrol ne?

Not: kisa, en fazla 5 madde, veriyle itiraz et, ilkeyi bozma. Kaynaksiz iddiayi "kaynaksiz" diye isaretle.
