# visualisasi/views.py

from django.shortcuts import render
from .models import FactSaham, DimWaktu
import json

def dashboard_view(request):
    # --- LOGIKA FILTER BARU ---
    
    # 1. Dapatkan daftar semua tahun unik dari database untuk mengisi dropdown
    all_years = list(DimWaktu.objects.values_list('tahun', flat=True).distinct().order_by('-tahun'))
    
    # 2. Cek apakah ada parameter 'tahun' di URL (hasil dari submit form)
    #    request.GET.get('tahun') akan mengambil nilai dari URL, contoh: /?tahun=2023
    selected_tahun = request.GET.get('tahun')
    
    # --- AKHIR LOGIKA FILTER ---

    # Query dasar untuk mengambil data
    query_data = FactSaham.objects.select_related('id_waktu').order_by('id_waktu__tanggal')
    
    # --- PENERAPAN FILTER BARU ---
    # 3. Jika pengguna memilih tahun, filter query-nya
    if selected_tahun and selected_tahun != "":
        # Ubah string dari URL menjadi integer untuk memfilter
        selected_tahun = int(selected_tahun)
        query_data = query_data.filter(id_waktu__tahun=selected_tahun)
    # --- AKHIR PENERAPAN FILTER ---

    # Menyiapkan data untuk Chart.js dari data yang sudah difilter
    labels = [data.id_waktu.tanggal.strftime('%Y-%m-%d') for data in query_data]
    harga_penutupan = [data.harga_penutupan for data in query_data]
    volume_transaksi = [data.volume_transaksi for data in query_data]
    
    context = {
        'labels': json.dumps(labels),
        'data_harga_penutupan': json.dumps(harga_penutupan),
        'data_volume': json.dumps(volume_transaksi),
        
        # --- DATA BARU UNTUK TEMPLATE ---
        'all_years': all_years,
        'selected_tahun': selected_tahun,
        # --- AKHIR DATA BARU ---
    }
    
    return render(request, 'visualisasi/dashboard.html', context)