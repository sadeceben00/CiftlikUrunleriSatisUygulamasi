# Tasarım

## UI/UX Tasarım
1. Anasayfa: Ürünlerin listelendiği, arama fonksiyonunun olduğu ana sayfa.
2. Ürün Detay Sayfası: Ürünlerin detaylarının ve satın alma butonunun olduğu sayfa.
3. Sepet Sayfası: Kullanıcının sepetindeki ürünleri görüntüleyebileceği ve ödeme yapabileceği sayfa.
4. Yönetim Paneli: Çiftlik sahiplerinin ürün ekleyebileceği ve siparişleri takip edebileceği panel.

## Veritabanı Tasarımı
### Kullanıcılar Tablosu
| ID | Kullanıcı Adı | E-posta | Şifre | Rol |
|----|---------------|---------|-------|-----|
| 1  | JohnDoe       | john@example.com | hashed_password | çiftlik_sahibi |
| 2  | JaneDoe       | jane@example.com | hashed_password | tüketici |

### Ürünler Tablosu
| ID | Ürün Adı | Açıklama | Fiyat | Stok | Çiftlik Sahibi ID |
|----|----------|----------|-------|------|-------------------|
| 1  | Elma     | Taze elma| 3.00  | 100  | 1                 |
| 2  | Domates  | Organik domates | 5.00  | 50   | 1                 |

### Siparişler Tablosu
| ID | Kullanıcı ID | Ürün ID | Miktar | Toplam Fiyat | Sipariş Tarihi | Durum |
|----|--------------|---------|--------|--------------|-----------------|-------|
| 1  | 2            | 1       | 10     | 30.00        | 2025-02-15      | Onaylandı |
| 2  | 2            | 2       | 5      | 25.00        | 2025-02-15      | Beklemede |