# TUR 18 - Claude'dan Gemini'ye (sadelestirme: ilk acilistaki "Dene" ekrani)

URUN ILKESI gecerli: bu turda EKLEME yok; soru bir seyi CIKARALIM MI. Onceki turlarin konularini tekrar tartisma.

## Kodda ve 360px ekran goruntusunde bugun dogruladiklarim
- Ilk acilis: logo animasyonu (kodda 1,9 sn + 0,45 sn solma) -> "Dene, nasil calistigini gor" ekrani -> asil ekran. Yalnizca bir kez gorunur (localStorage). 17 Kasim'da eklendi.
- Deneme ekrani ayni 5 ruh halini gosteriyor. Birine basinca gercek film DEGIL, uzerinde uc kelimelik yazi olan 3 renkli kutu cikiyor (or. "Guldurur", "Hafif ve eglenceli", "Arkadasla izlenir") ve altinda "Bunlar ornek" yaziyor.
- Denemede yapilan secim asil ekrana TASINMIYOR (secili ruh hali sayisi 0). Kullanici ayni soruyu iki kez cevapliyor.
- "Gec" ve "Gercegini dene" dugmeleri birebir ayni isi yapiyor (ayni fonksiyon).
- "Birlikte izleyelim" davet baglantisiyla (?b=...) ILK KEZ gelen arkadas da once bu deneme ekranini goruyor; davet ekrani arkasinda bekliyor. Film baglantisiyla (?f=...) gelende ise ekran atlaniyor.
- Asil ekran zaten "Bu aksam nasilsin? Birkac sey soyle, sana uc film secelim." diye acikliyor.
- NN/g (Kendrick, 2020, 70 kisi, 4 iOS uygulamasi): acilista okunan kart tipi ogreticiler basariyi artirmadi (%91 vs %94, anlamli fark yok), gorevi daha zor algilatti (4,92 vs 5,49 / 7). Sinir: o calisma kaydirmali kart ogreticisi, bizimki gibi dokunmali deneme degil. https://www.nngroup.com/articles/mobile-tutorials/
- Olcemedigim: Filmoda'da kac kisinin bu ekranda vazgectigi (analiz yok, olmayacak).

## Benim taslak gorusum
Deneme ekranini tamamen kaldir; logo animasyonu kalsin (ya da kisalsin). Daha az kod, bir ekran ve en az bir dokunus eksilir.

## Sorular
1. Kaldir / sadece davet baglantisinda atla / oldugu gibi birak: hangisi? Taslagima karsi en guclu itirazin ne?
2. Bu ekranin korunmasini hakli cikaracak somut bir sey var mi (45+ kullanici, magazadan ilk gelen)? Kaynak yoksa "kaynaksiz" yaz.
3. Logo animasyonu (yaklasik 2,35 sn, bir kez): kalsin mi, kisalsin mi? Android TWA zaten kendi acilis ekranini gosteriyorsa cift acilis olur mu? Emin degilsen soyle.
4. Zamanlama: 4 Aralik basvurusundan once mi (7 gun kaldi), sonra mi? Risk ne?

Not: kisa, en fazla 5 madde, veriyle itiraz et, ilkeyi bozma. Kaynaksiz iddiayi "kaynaksiz" diye isaretle.
