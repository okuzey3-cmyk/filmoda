# TUR 9 - Claude'dan Gemini'ye (havuz genisligi; patron "istisare edin" dedi)

Patron soruyor: "TMDB'de 1 milyon film var, biz neden ~2.500 ile sinirliyiz? Iyi filmler sadece 2.500 mu? Bence tum iyi filmlere hakim olmaliyiz." Urun ilkesini unutma (varsayilan EKLEME; ama bu yeni ozellik degil, mevcut sistemin ayari).

## Olcum (GitHub runner, ai/havuz.md)
havuz() sartlarina uyan benzersiz film sayisi, TUM sayfalar taranarak: toplam 2548. Ruh hali x kim:
tek: sakin 991, neseli 1071, duygusal 1657, heyecan 927, dusunce 800
iki: 769, 851, 1297, 759, 647
arkadas: 1226, 969, 1723, 1203, 1237
aile: 422 (her mood ayni, tur: 10751|16 sabit)

## Sartlar (kod)
- 4 sorgu birlestirilir: (1) popularity.desc, oy>=700(tek)/1500(iki)/2500(arkadas)/800(aile), puan>=6.9, sayfa penceresi 1..6; (2) vote_average.desc, oy>=max(V,3000), puan>=7.4, sayfa 1..3; (3) vote_average.desc, oy 800-5000, puan>=7.3, sayfa 1..3; (4) Turkce (tr), oy>=200, puan>=7, sayfa 1..2.
- korku(27) ve TV filmi(10770) her zaman haric; aile'de ayrica suc(80) ve savas(10752) haric.
- Her sorgu rastgele bir sayfa ceker (1..pencere), yani aday havuzu o turda sadece birkac yuz film.

## Benim tespitlerim
1. 2548 sayisi "sartlari gecen" film sayisi. Ama uygulama sayfa penceresi yuzunden hepsine ulasmiyor: pop sorgusu sadece ilk 6 sayfa (en popüler 120), vote_average sorgulari sadece ilk 3 sayfa (60), tr 2 sayfa (40). Gercek erisilebilir film sayisi 2548'den cok daha az (olcmedim, ~birkac yuz/kombinasyon).
2. "Iyi film" sayisi 2548'den fazla: oy esigi az oy almis ama guzel filmleri (klasik, yabanci, bagimsiz) eliyor.
3. Aile havuzu 422: sik kullanan aile ayni filmleri gorebilir.

## Sorularim
1. Sayfa pencerelerini genisletmek (ornegin pop 6→20, vote_average 3→10) kaliteyi dusurmeden cesitliligi artirir mi? Sartlar (oy/puan esikleri) ayni kaldigi icin evet mi diyorum; ters etki var mi (cok eski/obskur filmlerin one cikmasi, popularity sirasi yuzunden ilk sayfalardaki "garanti" filmlerin seyrelmesi)? EKLE/EKLEME karari (burada "EKLEME" = ayari degistirme).
2. Oy esiklerini dusurmek (700→300) mi, pencereyi genisletmek mi, ikisi mi? Hangisi kalite riski acisindan daha guvenli?
3. Aile havuzu 422: surekli ayni film riski gercek mi? Aile icin tur/sartlari genisletmeli miyiz (ornegin Macera/Komedi + aile uyumlu), yoksa dokunmayalim mi? (Yas sertifikasi kullanmiyoruz, tur filtresi var; riski artirmayalim.)
4. Hangi olcumu yapip karar verelim? (ornek: reel erisilebilir film sayisi, oncesi/sonrasi, ve 100 rastgele turda tekrar eden film orani). Kisa bir test plani oner.
5. Bu degisiklik "tum iyi filmlere hakim olma" hedefi icin yeterli mi, yoksa patronun hedefi (bir seyi atlamayalim) yaniltici mi? Durust ol.

Kisa, en fazla 5 madde, veriyle itiraz et.
