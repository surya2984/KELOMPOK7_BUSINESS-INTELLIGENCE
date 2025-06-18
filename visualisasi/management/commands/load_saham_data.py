# visualisasi/management/commands/load_saham_data.py

import pandas as pd
from django.core.management.base import BaseCommand
from visualisasi.models import DimWaktu, DimSaham, FactSaham

class Command(BaseCommand):
    help = 'Memuat data saham dari file CSV ke dalam database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Memulai proses pemuatan data...'))

        # Hapus data lama untuk menghindari duplikasi
        DimWaktu.objects.all().delete()
        DimSaham.objects.all().delete()
        FactSaham.objects.all().delete()
        self.stdout.write(self.style.WARNING('Data lama berhasil dihapus.'))

        # Muat Dimensi Waktu
        df_waktu = pd.read_csv('output/dim_waktu.csv')
        for _, row in df_waktu.iterrows():
            DimWaktu.objects.create(
                id_waktu=row['id_waktu'],
                tanggal=row['tanggal'],
                minggu=row['minggu'],
                bulan=row['bulan'],
                tahun=row['tahun']
            )
        self.stdout.write(self.style.SUCCESS(f'{len(df_waktu)} baris data waktu dimuat.'))

        # Muat Dimensi Saham
        df_saham = pd.read_csv('output/dim_saham.csv')
        for _, row in df_saham.iterrows():
            DimSaham.objects.create(
                kode_saham=row['kode_saham'],
                nama_saham=row['nama_saham'],
                sektor=row['sektor']
            )
        self.stdout.write(self.style.SUCCESS(f'{len(df_saham)} baris data saham dimuat.'))

        # Muat Tabel Fakta
        df_fakta = pd.read_csv('output/fact_saham.csv')
        for _, row in df_fakta.iterrows():
            # Dapatkan objek dimensi yang sesuai
            waktu_obj = DimWaktu.objects.get(id_waktu=row['id_waktu'])
            saham_obj = DimSaham.objects.get(kode_saham=row['kode_saham'])

            FactSaham.objects.create(
                id_waktu=waktu_obj,
                kode_saham=saham_obj,
                harga_pembukaan=row['harga_pembukaan'],
                harga_penutupan=row['harga_penutupan'],
                harga_tertinggi=row['harga_tertinggi'],
                harga_terendah=row['harga_terendah'],
                volume_transaksi=row['volume_transaksi']
            )
        self.stdout.write(self.style.SUCCESS(f'{len(df_fakta)} baris data fakta dimuat.'))

        self.stdout.write(self.style.SUCCESS('🎉 Semua data berhasil dimuat!'))