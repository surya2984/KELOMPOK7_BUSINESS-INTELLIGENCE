# visualisasi/models.py

from django.db import models

class DimWaktu(models.Model):
    id_waktu = models.IntegerField(primary_key=True)
    tanggal = models.DateField()
    minggu = models.IntegerField()
    bulan = models.IntegerField()
    tahun = models.IntegerField()

    def __str__(self):
        return str(self.tanggal)

class DimSaham(models.Model):
    kode_saham = models.CharField(max_length=10, primary_key=True)
    nama_saham = models.CharField(max_length=100)
    sektor = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_saham

class FactSaham(models.Model):
    id_fakta = models.AutoField(primary_key=True)
    # Membuat hubungan Foreign Key ke tabel dimensi
    id_waktu = models.ForeignKey(DimWaktu, on_delete=models.CASCADE)
    kode_saham = models.ForeignKey(DimSaham, on_delete=models.CASCADE)
    
    # Kolom ukuran (measures)
    harga_pembukaan = models.FloatField()
    harga_penutupan = models.FloatField()
    harga_tertinggi = models.FloatField()
    harga_terendah = models.FloatField()
    volume_transaksi = models.BigIntegerField()

    def __str__(self):
        return f"{self.kode_saham.nama_saham} pada {self.id_waktu.tanggal}"