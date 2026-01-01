import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar

from models import SistemSewaLapangan, Member, Lapangan
from database import Database
import datetime as dt

class SewaLapanganGUI:
    """Kelas untuk GUI aplikasi sewa lapangan"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Sewa Lapangan Olahraga")
        self.root.geometry("1200x750")
        
        self.db = Database()
        self.sistem = SistemSewaLapangan(self.db)
        self.setup_gui()
    
    def setup_gui(self):
        """Setup antarmuka GUI"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Buat semua tab
        self.create_tab_pendaftaran()
        self.create_tab_lapangan()
        self.create_tab_pemesanan()
        self.create_tab_pembayaran()
        self.create_tab_member()
        self.create_tab_laporan()
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Sistem Sewa Lapangan Olahraga - Siap",
            relief='sunken',
            anchor='w'
        )
        self.status_bar.pack(fill='x', padx=10, pady=5)
    
    def create_tab_pendaftaran(self):
        """Tab untuk pendaftaran member"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Pendaftaran Member")
        
        # Frame form pendaftaran
        form_frame = ttk.LabelFrame(tab, text="Form Pendaftaran Member Baru", padding=20)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Input fields
        ttk.Label(form_frame, text="Nama Lengkap:").grid(row=0, column=0, sticky='w', pady=5)
        self.nama_entry = ttk.Entry(form_frame, width=40)
        self.nama_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Umur:").grid(row=1, column=0, sticky='w', pady=5)
        self.umur_entry = ttk.Entry(form_frame, width=10)
        self.umur_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        
        ttk.Label(form_frame, text="Jenis Kelamin:").grid(row=2, column=0, sticky='w', pady=5)
        self.jk_var = tk.StringVar(value="Laki-laki")
        ttk.Radiobutton(form_frame, text="Laki-laki", variable=self.jk_var, 
                       value="Laki-laki").grid(row=2, column=1, sticky='w', pady=5, padx=5)
        ttk.Radiobutton(form_frame, text="Perempuan", variable=self.jk_var, 
                       value="Perempuan").grid(row=2, column=1, sticky='w', pady=5, padx=100)
        
        ttk.Label(form_frame, text="Alamat:").grid(row=3, column=0, sticky='w', pady=5)
        self.alamat_text = tk.Text(form_frame, width=40, height=3)
        self.alamat_text.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="No. Telepon:").grid(row=4, column=0, sticky='w', pady=5)
        self.telp_entry = ttk.Entry(form_frame, width=20)
        self.telp_entry.grid(row=4, column=1, sticky='w', pady=5, padx=5)
        
        # Tombol daftar
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Daftarkan Member", 
                  command=self.daftarkan_member, width=20).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset Form", 
                  command=self.reset_form_pendaftaran, width=20).pack(side='left', padx=5)
        
        # Frame daftar member terdaftar
        list_frame = ttk.LabelFrame(tab, text="Daftar Member Terdaftar", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview untuk menampilkan member
        columns = ("ID", "Nama", "Umur", "JK", "Telepon", "Tanggal Daftar")
        self.member_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.member_tree.yview)
        self.member_tree.configure(yscrollcommand=scrollbar.set)
        
        self.member_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load data awal
        self.load_data_member()
    
    def create_tab_lapangan(self):
        """Tab untuk informasi lapangan"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Informasi Lapangan")
        
        # Frame utama
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame kiri: Filter
        filter_frame = ttk.LabelFrame(main_frame, text="Filter Lapangan", padding=15)
        filter_frame.pack(side='left', fill='y', padx=(0, 5))
        
        ttk.Label(filter_frame, text="Jenis Olahraga:").pack(anchor='w', pady=5)
        
        self.filter_jenis_var = tk.StringVar(value="Semua")
        jenis_options = ["Semua", "Futsal", "Badminton", "Tennis", "Basket", "Voli"]
        
        for jenis in jenis_options:
            ttk.Radiobutton(filter_frame, text=jenis, variable=self.filter_jenis_var, 
                          value=jenis, command=self.filter_lapangan).pack(anchor='w', padx=10)
        
        ttk.Label(filter_frame, text="Status:").pack(anchor='w', pady=(15, 5))
        
        self.filter_status_var = tk.StringVar(value="Semua")
        status_options = ["Semua", "Tersedia", "Dalam Perawatan", "Tidak Tersedia"]
        
        for status in status_options:
            ttk.Radiobutton(filter_frame, text=status, variable=self.filter_status_var, 
                          value=status, command=self.filter_lapangan).pack(anchor='w', padx=10)
        
        # Frame kanan: Daftar lapangan
        list_frame = ttk.LabelFrame(main_frame, text="Daftar Lapangan", padding=10)
        list_frame.pack(side='right', fill='both', expand=True)
        
        # Treeview lapangan
        columns = ("ID", "Nama Lapangan", "Jenis", "Harga/Jam", "Status")
        self.lapangan_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        widths = [80, 200, 100, 120, 120]
        for col, width in zip(columns, widths):
            self.lapangan_tree.heading(col, text=col)
            self.lapangan_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.lapangan_tree.yview)
        self.lapangan_tree.configure(yscrollcommand=scrollbar.set)
        
        self.lapangan_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Info harga rata-rata
        info_frame = ttk.Frame(list_frame)
        info_frame.pack(side='bottom', fill='x', pady=5)
        
        self.harga_info_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.harga_info_var, 
                 font=('Arial', 10, 'italic')).pack()
        
        # Load data awal
        self.load_data_lapangan()
        self.update_harga_info()
    
    def create_tab_pemesanan(self):
        """Tab untuk pemesanan lapangan"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Pemesanan Lapangan")
        
        # Container dengan 2 kolom
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ========== KOLOM KIRI: FORM PEMESANAN ==========
        left_frame = ttk.LabelFrame(main_frame, text="Form Pemesanan", padding=15)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # 1. Pilih Member
        ttk.Label(left_frame, text="ID Member:").grid(row=0, column=0, sticky='w', pady=5)
        self.pemesanan_id_member = ttk.Entry(left_frame, width=25)
        self.pemesanan_id_member.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        
        ttk.Button(left_frame, text="Cari Member", 
                  command=self.cari_member_untuk_pemesanan).grid(row=0, column=2, padx=10)
        
        ttk.Label(left_frame, text="Nama Member:").grid(row=1, column=0, sticky='w', pady=5)
        self.nama_member_pemesanan_var = tk.StringVar()
        ttk.Label(left_frame, textvariable=self.nama_member_pemesanan_var, 
                 relief='sunken', width=25).grid(row=1, column=1, sticky='w', pady=5, padx=5)
        
        # 2. Pilih Jenis Olahraga
        ttk.Label(left_frame, text="Jenis Olahraga:").grid(row=2, column=0, sticky='w', pady=5)
        self.jenis_olahraga_var = tk.StringVar()
        jenis_combo = ttk.Combobox(left_frame, textvariable=self.jenis_olahraga_var,
                                  values=["Futsal", "Badminton", "Tennis", "Basket", "Voli"],
                                  state='readonly', width=23)
        jenis_combo.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        jenis_combo.bind('<<ComboboxSelected>>', self.on_jenis_olahraga_selected)
        
        # 3. Pilih Lapangan
        ttk.Label(left_frame, text="Lapangan:").grid(row=3, column=0, sticky='w', pady=5)
        self.lapangan_combo = ttk.Combobox(left_frame, state='readonly', width=23)
        self.lapangan_combo.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        self.lapangan_combo.bind('<<ComboboxSelected>>', self.on_lapangan_selected)
        
        # 4. Pilih Tanggal
        ttk.Label(left_frame, text="Tanggal Sewa:").grid(row=4, column=0, sticky='w', pady=5)
        
        date_frame = ttk.Frame(left_frame)
        date_frame.grid(row=4, column=1, sticky='w', pady=5, padx=5)
        
        today = datetime.now()
        self.tanggal_sewa_var = tk.StringVar(value=today.strftime("%Y-%m-%d"))
        
        # Tombol tanggal
        ttk.Button(date_frame, text="Hari Ini", 
                  command=lambda: self.set_tanggal(today)).pack(side='left', padx=2)
        ttk.Button(date_frame, text="Besok", 
                  command=lambda: self.set_tanggal(today + timedelta(days=1))).pack(side='left', padx=2)
        
        # Entry tanggal
        ttk.Entry(left_frame, textvariable=self.tanggal_sewa_var, 
                 width=15).grid(row=5, column=1, sticky='w', pady=5, padx=5)
        ttk.Label(left_frame, text="Format: YYYY-MM-DD").grid(row=5, column=2, sticky='w', pady=5)
        
        # 5. Pilih Jam
        ttk.Label(left_frame, text="Jam Mulai:").grid(row=6, column=0, sticky='w', pady=5)
        self.jam_mulai_combo = ttk.Combobox(left_frame, width=8, state='readonly')
        self.jam_mulai_combo.grid(row=6, column=1, sticky='w', pady=5, padx=5)
        
        ttk.Label(left_frame, text="Jam Selesai:").grid(row=7, column=0, sticky='w', pady=5)
        self.jam_selesai_combo = ttk.Combobox(left_frame, width=8, state='readonly')
        self.jam_selesai_combo.grid(row=7, column=1, sticky='w', pady=5, padx=5)
        
        # Generate jam operasional
        self.generate_jam_operasional()
        
        # 6. Durasi dan Total
        ttk.Label(left_frame, text="Durasi:").grid(row=8, column=0, sticky='w', pady=10)
        self.durasi_var = tk.StringVar(value="0 jam")
        ttk.Label(left_frame, textvariable=self.durasi_var, 
                 font=('Arial', 10, 'bold')).grid(row=8, column=1, sticky='w', pady=10, padx=5)
        
        ttk.Label(left_frame, text="Total Biaya:").grid(row=9, column=0, sticky='w', pady=5)
        self.total_biaya_var = tk.StringVar(value="Rp 0")
        ttk.Label(left_frame, textvariable=self.total_biaya_var, 
                 font=('Arial', 11, 'bold'), foreground='green').grid(row=9, column=1, sticky='w', pady=5, padx=5)
        
        # 7. Tombol aksi
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=10, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Cek Ketersediaan", 
                  command=self.cek_ketersediaan, width=18).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Pesan Sekarang", 
                  command=self.pesan_lapangan, width=18).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset Form", 
                  command=self.reset_form_pemesanan, width=18).pack(side='left', padx=5)
        
        # ========== KOLOM KANAN: JADWAL HARI INI ==========
        right_frame = ttk.LabelFrame(main_frame, text="Jadwal Lapangan Hari Ini", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Treeview jadwal
        columns = ("Lapangan", "Jam", "Member", "Status")
        self.jadwal_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        widths = [150, 100, 150, 100]
        for col, width in zip(columns, widths):
            self.jadwal_tree.heading(col, text=col)
            self.jadwal_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.jadwal_tree.yview)
        self.jadwal_tree.configure(yscrollcommand=scrollbar.set)
        
        self.jadwal_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Tombol refresh jadwal
        ttk.Button(right_frame, text="Refresh Jadwal", 
                  command=self.load_jadwal_hari_ini).pack(side='bottom', pady=5)
        
        # Load data awal
        self.load_jadwal_hari_ini()
    
    def create_tab_pembayaran(self):
        """Tab untuk pembayaran"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Pembayaran")
        
        # Frame atas: Form pembayaran
        top_frame = ttk.LabelFrame(tab, text="Form Pembayaran", padding=20)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        # Input ID penyewaan
        ttk.Label(top_frame, text="ID Penyewaan:").grid(row=0, column=0, sticky='w', pady=5)
        self.pembayaran_id_penyewaan = ttk.Entry(top_frame, width=20)
        self.pembayaran_id_penyewaan.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        
        ttk.Button(top_frame, text="Cari Penyewaan", 
                  command=self.cari_penyewaan_untuk_bayar).grid(row=0, column=2, padx=10)
        
        # Info penyewaan
        info_frame = ttk.Frame(top_frame)
        info_frame.grid(row=1, column=0, columnspan=3, sticky='w', pady=10)
        
        self.pembayaran_info_vars = {}
        info_fields = [
            ("Member:", "nama_member_bayar"),
            ("Lapangan:", "lapangan_bayar"),
            ("Tanggal:", "tanggal_bayar"),
            ("Jam:", "jam_bayar"),
            ("Total Biaya:", "total_biaya_bayar"),
            ("Sudah Dibayar:", "sudah_dibayar_bayar"),
            ("Sisa:", "sisa_bayar_bayar"),
        ]
        
        for i, (label, key) in enumerate(info_fields):
            ttk.Label(info_frame, text=label, width=15, anchor='e').grid(row=i, column=0, sticky='w', pady=2)
            var = tk.StringVar()
            lbl = ttk.Label(info_frame, textvariable=var, width=30, relief='sunken')
            lbl.grid(row=i, column=1, sticky='w', pady=2, padx=5)
            self.pembayaran_info_vars[key] = var
        
        # Input pembayaran
        ttk.Label(top_frame, text="Jumlah Bayar:").grid(row=2, column=0, sticky='w', pady=10)
        self.jumlah_bayar_var = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.jumlah_bayar_var, width=20).grid(row=2, column=1, sticky='w', pady=10, padx=5)
        
        ttk.Label(top_frame, text="Metode:").grid(row=2, column=2, sticky='w', pady=10, padx=10)
        self.metode_bayar_var = tk.StringVar(value="Tunai")
        ttk.Combobox(top_frame, textvariable=self.metode_bayar_var,
                    values=["Tunai", "Transfer", "Debit", "Kredit"],
                    width=15).grid(row=2, column=3, sticky='w', pady=10)
        
        # Tombol
        btn_frame = ttk.Frame(top_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=20)
        
        ttk.Button(btn_frame, text="Proses Pembayaran", 
                  command=self.proses_pembayaran, width=20).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cetak Struk", 
                  command=self.cetak_struk, width=20).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Lihat Riwayat", 
                  command=self.lihat_riwayat_pembayaran, width=20).pack(side='left', padx=5)
        
        # Frame bawah: Riwayat pembayaran hari ini
        bottom_frame = ttk.LabelFrame(tab, text="Riwayat Pembayaran Hari Ini", padding=10)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        columns = ("ID", "Penyewaan", "Member", "Jumlah", "Metode", "Waktu")
        self.riwayat_pembayaran_tree = ttk.Treeview(bottom_frame, columns=columns, show='headings', height=10)
        
        widths = [60, 80, 120, 100, 80, 120]
        for col, width in zip(columns, widths):
            self.riwayat_pembayaran_tree.heading(col, text=col)
            self.riwayat_pembayaran_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(bottom_frame, orient='vertical', 
                                 command=self.riwayat_pembayaran_tree.yview)
        self.riwayat_pembayaran_tree.configure(yscrollcommand=scrollbar.set)
        
        self.riwayat_pembayaran_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load riwayat pembayaran
        self.load_riwayat_pembayaran_harian()
    
    def create_tab_member(self):
        """Tab untuk manajemen member"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Manajemen Member")
        
        # Container utama dengan 2 frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ========== FRAME KIRI: PENCARIAN & DETAIL ==========
        left_frame = ttk.LabelFrame(main_frame, text="Pencarian & Detail Member", padding=15)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Search box
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(search_frame, text="Cari:").pack(side='left', padx=(0, 10))
        self.search_member_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_member_var, width=30)
        search_entry.pack(side='left', padx=(0, 10))
        
        ttk.Button(search_frame, text="Cari", 
                  command=lambda: self.cari_member_gui(self.search_member_var.get())).pack(side='left', padx=(0, 10))
        ttk.Button(search_frame, text="Reset", 
                  command=self.reset_pencarian_member).pack(side='left')
        
        # Detail member
        detail_frame = ttk.LabelFrame(left_frame, text="Detail Member", padding=15)
        detail_frame.pack(fill='both', expand=True)
        
        # Fields detail
        detail_fields = [
            ("ID Member:", "id_detail"),
            ("Nama:", "nama_detail"),
            ("Umur:", "umur_detail"),
            ("JK:", "jk_detail"),
            ("Alamat:", "alamat_detail"),
            ("Telepon:", "telp_detail"),
            ("Tanggal Daftar:", "tgl_detail"),
            ("Total Penyewaan:", "total_sewa_detail")
        ]
        
        self.member_detail_vars = {}
        for i, (label, key) in enumerate(detail_fields):
            ttk.Label(detail_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky='w', pady=5, padx=(0, 10))
            
            if key == "alamat_detail":
                text_widget = tk.Text(detail_frame, height=3, width=30, state='disabled')
                text_widget.grid(row=i, column=1, sticky='w', pady=5)
                self.member_detail_vars[key] = text_widget
            else:
                var = tk.StringVar()
                entry = ttk.Entry(detail_frame, textvariable=var, state='readonly', width=30)
                entry.grid(row=i, column=1, sticky='w', pady=5)
                self.member_detail_vars[key] = var
        
        # Tombol aksi
        button_frame = ttk.Frame(detail_frame)
        button_frame.grid(row=len(detail_fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Edit Member", 
                  command=self.edit_member, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Hapus Member", 
                  command=self.hapus_member, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Lihat Riwayat", 
                  command=self.lihat_riwayat_member, width=15).pack(side='left', padx=5)
        
        # ========== FRAME KANAN: DAFTAR MEMBER ==========
        right_frame = ttk.LabelFrame(main_frame, text="Daftar Member", padding=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Treeview
        columns = ("ID", "Nama", "Umur", "JK", "Telepon", "Alamat")
        self.member_management_tree = ttk.Treeview(right_frame, columns=columns, 
                                                  show='headings', height=15)
        
        widths = [80, 150, 60, 60, 100, 150]
        for col, width in zip(columns, widths):
            self.member_management_tree.heading(col, text=col)
            self.member_management_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', 
                                 command=self.member_management_tree.yview)
        self.member_management_tree.configure(yscrollcommand=scrollbar.set)
        
        self.member_management_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double click
        self.member_management_tree.bind('<Double-1>', self.on_member_selected)
        
        # Load data awal
        self.load_member_management_data()
        
        # Status info
        info_label = ttk.Label(right_frame,
                              text="Double klik pada member untuk melihat detail",
                              font=('Arial', 9, 'italic'))
        info_label.pack(side='bottom', pady=5)
    
    def create_tab_laporan(self):
        """Tab untuk laporan"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Laporan")
        
        # Notebook dalam tab (sub-tab)
        laporan_notebook = ttk.Notebook(tab)
        laporan_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sub-tab 1: Statistik harian
        stats_tab = ttk.Frame(laporan_notebook)
        laporan_notebook.add(stats_tab, text="Statistik Harian")
        
        stats_frame = ttk.LabelFrame(stats_tab, text="Statistik 7 Hari Terakhir", padding=20)
        stats_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ("Tanggal", "Jumlah Penyewaan", "Jumlah Member", "Total Pendapatan")
        self.stats_tree = ttk.Treeview(stats_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(stats_frame, orient='vertical', command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stats_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Sub-tab 2: Popularitas lapangan
        popularitas_tab = ttk.Frame(laporan_notebook)
        laporan_notebook.add(popularitas_tab, text="Popularitas Lapangan")
        
        popularitas_frame = ttk.LabelFrame(popularitas_tab, text="Statistik Lapangan", padding=20)
        popularitas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns_pop = ("Lapangan", "Jenis", "Jumlah Penyewaan", "Total Pendapatan")
        self.popularitas_tree = ttk.Treeview(popularitas_frame, columns=columns_pop, 
                                           show='headings', height=10)
        
        widths_pop = [150, 100, 120, 150]
        for col, width in zip(columns_pop, widths_pop):
            self.popularitas_tree.heading(col, text=col)
            self.popularitas_tree.column(col, width=width)
        
        scrollbar2 = ttk.Scrollbar(popularitas_frame, orient='vertical', 
                                  command=self.popularitas_tree.yview)
        self.popularitas_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.popularitas_tree.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')
        
        # Sub-tab 3: Member aktif
        member_tab = ttk.Frame(laporan_notebook)
        laporan_notebook.add(member_tab, text="Member Aktif")
        
        member_frame = ttk.LabelFrame(member_tab, text="Top 10 Member", padding=20)
        member_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns_mem = ("Member", "Jumlah Penyewaan", "Total Pengeluaran", "Member Sejak")
        self.member_report_tree = ttk.Treeview(member_frame, columns=columns_mem, 
                                              show='headings', height=10)
        
        widths_mem = [150, 120, 150, 120]
        for col, width in zip(columns_mem, widths_mem):
            self.member_report_tree.heading(col, text=col)
            self.member_report_tree.column(col, width=width)
        
        scrollbar3 = ttk.Scrollbar(member_frame, orient='vertical', 
                                  command=self.member_report_tree.yview)
        self.member_report_tree.configure(yscrollcommand=scrollbar3.set)
        
        self.member_report_tree.pack(side='left', fill='both', expand=True)
        scrollbar3.pack(side='right', fill='y')
        
        # Tombol refresh
        refresh_frame = ttk.Frame(tab)
        refresh_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(refresh_frame, text="Refresh Semua Data", 
                  command=self.refresh_laporan).pack(side='right', padx=5)
        
        # Load statistik awal
        self.load_statistik_harian()
        self.load_statistik_popularitas()
        self.load_statistik_member()
    
    # ========== METHOD UNTUK TAB PENDAFTARAN ==========
    
    def daftarkan_member(self):
        """Mendaftarkan member baru"""
        # Validasi input
        nama = self.nama_entry.get().strip()
        umur = self.umur_entry.get().strip()
        alamat = self.alamat_text.get("1.0", tk.END).strip()
        telepon = self.telp_entry.get().strip()
        
        if not nama or not umur:
            messagebox.showwarning("Peringatan", "Nama dan umur harus diisi!")
            return
        
        try:
            umur = int(umur)
        except:
            messagebox.showwarning("Peringatan", "Umur harus berupa angka!")
            return
        
        # Daftarkan member
        member = self.sistem.daftar_member_baru(
            nama, umur, self.jk_var.get(), alamat, telepon
        )
        
        if member:
            messagebox.showinfo(
                "Berhasil",
                f"Member berhasil didaftarkan!\n\n"
                f"ID Member: {member.id_person}\n"
                f"Nama: {member.nama}\n"
                f"Telepon: {telepon}"
            )
            
            # Reset form
            self.reset_form_pendaftaran()
            
            # Refresh data
            self.load_data_member()
            self.load_member_management_data()
            
            self.status_bar.config(text=f"Member baru: {member.nama}")
        else:
            messagebox.showerror("Error", "Gagal mendaftarkan member!")
    
    def reset_form_pendaftaran(self):
        """Reset form pendaftaran"""
        self.nama_entry.delete(0, tk.END)
        self.umur_entry.delete(0, tk.END)
        self.alamat_text.delete("1.0", tk.END)
        self.telp_entry.delete(0, tk.END)
        self.jk_var.set("Laki-laki")
    
    def load_data_member(self):
        """Memuat data member ke treeview"""
        for item in self.member_tree.get_children():
            self.member_tree.delete(item)
        
        member_data = self.db.get_semua_member()
        if member_data:
            for member in member_data:
                self.member_tree.insert('', 'end', values=(
                    member['id_member'],
                    member['nama'],
                    member['umur'],
                    member['jenis_kelamin'],
                    member['no_telepon'],
                    member['tanggal_daftar']
                ))
    
    # ========== METHOD UNTUK TAB LAPANGAN ==========
    
    def load_data_lapangan(self):
        """Memuat data lapangan"""
        for item in self.lapangan_tree.get_children():
            self.lapangan_tree.delete(item)
        
        lapangan_data = self.db.get_semua_lapangan()
        if lapangan_data:
            for lapangan in lapangan_data:
                self.lapangan_tree.insert('', 'end', values=(
                    lapangan['id_lapangan'],
                    lapangan['nama_lapangan'],
                    lapangan['jenis_olahraga'],
                    f"Rp {lapangan['harga_per_jam']:,}",
                    lapangan['status']
                ))
    
    def filter_lapangan(self):
        """Filter lapangan berdasarkan jenis dan status"""
        for item in self.lapangan_tree.get_children():
            self.lapangan_tree.delete(item)
        
        jenis = self.filter_jenis_var.get()
        status = self.filter_status_var.get()
        
        lapangan_data = self.db.get_semua_lapangan()
        if lapangan_data:
            for lapangan in lapangan_data:
                # Filter jenis
                if jenis != "Semua" and lapangan['jenis_olahraga'] != jenis:
                    continue
                
                # Filter status
                if status != "Semua" and lapangan['status'] != status:
                    continue
                
                self.lapangan_tree.insert('', 'end', values=(
                    lapangan['id_lapangan'],
                    lapangan['nama_lapangan'],
                    lapangan['jenis_olahraga'],
                    f"Rp {lapangan['harga_per_jam']:,}",
                    lapangan['status']
                ))
        
        self.update_harga_info()
    
    def update_harga_info(self):
        """Update informasi harga rata-rata"""
        lapangan_data = self.db.get_semua_lapangan()
        if lapangan_data:
            total_harga = sum(l['harga_per_jam'] for l in lapangan_data)
            rata_rata = total_harga / len(lapangan_data)
            
            # Hitung harga termahal dan termurah
            harga_list = [l['harga_per_jam'] for l in lapangan_data]
            termahal = max(harga_list)
            termurah = min(harga_list)
            
            info_text = (f"Harga rata-rata: Rp {rata_rata:,.0f}/jam | "
                        f"Termurah: Rp {termurah:,.0f} | "
                        f"Termahal: Rp {termahal:,.0f}")
            self.harga_info_var.set(info_text)
    
    # ========== METHOD UNTUK TAB PEMESANAN ==========
    
    def generate_jam_operasional(self):
        """Generate pilihan jam operasional"""
        jam_list = []
        for jam in range(8, 22):  # Jam 8 pagi sampai 10 malam
            for menit in ['00', '30']:
                jam_list.append(f"{jam:02d}:{menit}")
        
        self.jam_mulai_combo['values'] = jam_list
        self.jam_selesai_combo['values'] = jam_list
        
        # Set default jam
        now = datetime.now()
        if 8 <= now.hour < 22:
            default_jam = f"{now.hour:02d}:00"
            self.jam_mulai_combo.set(default_jam)
            self.jam_selesai_combo.set(f"{now.hour + 1:02d}:00")
    
    def set_tanggal(self, tanggal_obj):
        """Set tanggal pada form pemesanan"""
        self.tanggal_sewa_var.set(tanggal_obj.strftime("%Y-%m-%d"))
    
    def on_jenis_olahraga_selected(self, event=None):
        """Ketika jenis olahraga dipilih"""
        jenis = self.jenis_olahraga_var.get()
        if jenis:
            # Load lapangan berdasarkan jenis
            lapangan_data = self.db.get_lapangan_by_jenis(jenis)
            lapangan_list = []
            
            for lapangan in lapangan_data:
                display_text = f"{lapangan['id_lapangan']} - {lapangan['nama_lapangan']} (Rp {lapangan['harga_per_jam']:,}/jam)"
                lapangan_list.append(display_text)
            
            self.lapangan_combo['values'] = lapangan_list
            if lapangan_list:
                self.lapangan_combo.set(lapangan_list[0])
    
    def on_lapangan_selected(self, event=None):
        """Ketika lapangan dipilih"""
        selected = self.lapangan_combo.get()
        if selected:
            # Ambil ID lapangan
            id_lapangan = selected.split(" - ")[0]
            
            # Dapatkan harga per jam
            lapangan_data = self.db.get_lapangan_by_id(id_lapangan)
            if lapangan_data:
                self.selected_lapangan_harga = lapangan_data['harga_per_jam']
    
    def cari_member_untuk_pemesanan(self):
        """Cari member untuk form pemesanan"""
        id_member = self.pemesanan_id_member.get().strip()
        if not id_member:
            messagebox.showwarning("Peringatan", "Masukkan ID Member terlebih dahulu!")
            return
        
        # Cari data member
        query = "SELECT * FROM member WHERE id_member = %s"
        result = self.db.execute_query(query, (id_member,), fetch=True)
        
        if result and len(result) > 0:
            member = result[0]
            self.nama_member_pemesanan_var.set(member['nama'])
            self.status_bar.config(text=f"Member ditemukan: {member['nama']}")
        else:
            self.nama_member_pemesanan_var.set("")
            messagebox.showerror("Error", f"Member dengan ID {id_member} tidak ditemukan!")
            self.status_bar.config(text=f"Member {id_member} tidak ditemukan")
    
    def cek_ketersediaan(self):
        """Cek ketersediaan lapangan"""
        # Validasi input
        id_lapangan = self.lapangan_combo.get()
        tanggal = self.tanggal_sewa_var.get()
        jam_mulai = self.jam_mulai_combo.get()
        jam_selesai = self.jam_selesai_combo.get()
        
        if not id_lapangan or not tanggal or not jam_mulai or not jam_selesai:
            messagebox.showwarning("Peringatan", "Harap lengkapi semua data!")
            return
        
        # Parse ID lapangan
        id_lapangan = id_lapangan.split(" - ")[0]
        
        # Cek ketersediaan
        tersedia = self.db.cek_ketersediaan_lapangan(id_lapangan, tanggal, jam_mulai, jam_selesai)
        
        if tersedia:
            messagebox.showinfo("Tersedia", "Lapangan tersedia untuk waktu tersebut!")
        else:
            messagebox.showwarning("Tidak Tersedia", 
                                 "Lapangan sudah dipesan pada waktu tersebut. Silakan pilih waktu lain.")
    
    def pesan_lapangan(self):
        """Proses pemesanan lapangan"""
        # Validasi
        id_member = self.pemesanan_id_member.get().strip()
        if not id_member:
            messagebox.showwarning("Peringatan", "ID Member harus diisi!")
            return
        
        id_lapangan = self.lapangan_combo.get()
        if not id_lapangan:
            messagebox.showwarning("Peringatan", "Pilih lapangan terlebih dahulu!")
            return
        
        tanggal = self.tanggal_sewa_var.get()
        jam_mulai = self.jam_mulai_combo.get()
        jam_selesai = self.jam_selesai_combo.get()
        
        if not tanggal or not jam_mulai or not jam_selesai:
            messagebox.showwarning("Peringatan", "Tanggal dan jam harus diisi!")
            return
        
        # Parse ID lapangan
        id_lapangan = id_lapangan.split(" - ")[0]
        
        # Hitung durasi dan total biaya
        jam_mulai_int = int(jam_mulai.split(":")[0])
        jam_selesai_int = int(jam_selesai.split(":")[0])
        durasi = jam_selesai_int - jam_mulai_int
        
        if durasi <= 0:
            messagebox.showwarning("Peringatan", "Jam selesai harus setelah jam mulai!")
            return
        
        # Dapatkan harga lapangan
        lapangan_data = self.db.get_lapangan_by_id(id_lapangan)
        if not lapangan_data:
            messagebox.showerror("Error", "Data lapangan tidak ditemukan!")
            return
        
        harga_per_jam = lapangan_data['harga_per_jam']
        total_biaya = harga_per_jam * durasi
        
        # Konfirmasi pemesanan
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Pemesanan",
            f"Detail Pemesanan:\n\n"
            f"ID Member: {id_member}\n"
            f"Lapangan: {lapangan_data['nama_lapangan']}\n"
            f"Tanggal: {tanggal}\n"
            f"Jam: {jam_mulai} - {jam_selesai} ({durasi} jam)\n"
            f"Total Biaya: Rp {total_biaya:,}\n\n"
            f"Apakah Anda yakin ingin memesan?"
        )
        
        if konfirmasi:
            # Simpan ke database
            success = self.db.tambah_penyewaan(
                id_member, id_lapangan, tanggal, jam_mulai, jam_selesai, durasi, total_biaya
            )
            
            if success:
                messagebox.showinfo("Berhasil", "Pemesanan berhasil disimpan!")
                
                # Reset form
                self.reset_form_pemesanan()
                
                # Refresh jadwal
                self.load_jadwal_hari_ini()
                
                # Update status lapangan (jika perlu)
                if self.db.cek_ketersediaan_lapangan(id_lapangan, tanggal, jam_mulai, jam_selesai) == False:
                    messagebox.showinfo("Info", "Lapangan telah berhasil dipesan!")
                
                self.status_bar.config(text=f"Pemesanan untuk member {id_member} berhasil")
            else:
                messagebox.showerror("Error", "Gagal menyimpan pemesanan!")
    
    def reset_form_pemesanan(self):
        """Reset form pemesanan"""
        self.pemesanan_id_member.delete(0, tk.END)
        self.nama_member_pemesanan_var.set("")
        self.jenis_olahraga_var.set("")
        self.lapangan_combo.set("")
        self.tanggal_sewa_var.set(datetime.now().strftime("%Y-%m-%d"))
        
        # Reset jam ke default
        now = datetime.now()
        if 8 <= now.hour < 22:
            default_jam = f"{now.hour:02d}:00"
            self.jam_mulai_combo.set(default_jam)
            self.jam_selesai_combo.set(f"{now.hour + 1:02d}:00")
        
        self.durasi_var.set("0 jam")
        self.total_biaya_var.set("Rp 0")
    
    def load_jadwal_hari_ini(self):
        """Load jadwal lapangan hari ini"""
        for item in self.jadwal_tree.get_children():
            self.jadwal_tree.delete(item)
        
        jadwal_data = self.db.get_jadwal_lapangan_hari_ini()
        if jadwal_data:
            for jadwal in jadwal_data:
                jam = f"{jadwal['jam_mulai']} - {jadwal['jam_selesai']}"
                self.jadwal_tree.insert('', 'end', values=(
                    jadwal['nama_lapangan'],
                    jam,
                    jadwal['nama_member'],
                    jadwal.get('status_pembayaran', 'Belum Bayar')
                ))
    
    # ========== METHOD UNTUK TAB PEMBAYARAN ==========
    
    def cari_penyewaan_untuk_bayar(self):
        """Cari penyewaan untuk pembayaran"""
        id_penyewaan = self.pembayaran_id_penyewaan.get().strip()
        if not id_penyewaan:
            messagebox.showwarning("Peringatan", "Masukkan ID Penyewaan terlebih dahulu!")
            return
        
        try:
            id_penyewaan = int(id_penyewaan)
        except ValueError:
            messagebox.showwarning("Peringatan", "ID Penyewaan harus berupa angka!")
            return
        
        # Ambil detail penyewaan
        penyewaan = self.db.get_detail_penyewaan(id_penyewaan)
        if not penyewaan:
            messagebox.showerror("Error", f"Penyewaan dengan ID {id_penyewaan} tidak ditemukan!")
            return
        
        # Hitung total yang sudah dibayar
        total_dibayar = self.db.get_total_sudah_dibayar(id_penyewaan)
        biaya = penyewaan.get('total_biaya', 0)
        sisa = biaya - total_dibayar
        
        # Tampilkan informasi
        self.pembayaran_info_vars['nama_member_bayar'].set(penyewaan.get('nama_member', '-'))
        self.pembayaran_info_vars['lapangan_bayar'].set(penyewaan.get('nama_lapangan', '-'))
        self.pembayaran_info_vars['tanggal_bayar'].set(penyewaan.get('tanggal_sewa', '-'))
        self.pembayaran_info_vars['jam_bayar'].set(f"{penyewaan.get('jam_mulai', '-')} - {penyewaan.get('jam_selesai', '-')}")
        self.pembayaran_info_vars['total_biaya_bayar'].set(f"Rp {biaya:,}")
        self.pembayaran_info_vars['sudah_dibayar_bayar'].set(f"Rp {total_dibayar:,}")
        self.pembayaran_info_vars['sisa_bayar_bayar'].set(f"Rp {sisa:,}")
        
        self.status_bar.config(text=f"Penyewaan ditemukan: {penyewaan['nama_member']}")
        
        # Simpan data untuk proses pembayaran
        self.selected_penyewaan = penyewaan
        self.selected_penyewaan_id = id_penyewaan
    
    def proses_pembayaran(self):
        """Proses pembayaran"""
        if not hasattr(self, 'selected_penyewaan_id'):
            messagebox.showwarning("Peringatan", "Cari penyewaan terlebih dahulu!")
            return
        
        # Validasi jumlah bayar
        try:
            jumlah_bayar = float(self.jumlah_bayar_var.get())
            if jumlah_bayar <= 0:
                messagebox.showwarning("Peringatan", "Jumlah bayar harus lebih dari 0!")
                return
        except ValueError:
            messagebox.showwarning("Peringatan", "Jumlah bayar harus berupa angka!")
            return
        
        metode = self.metode_bayar_var.get()
        
        # Konfirmasi
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Pembayaran",
            f"Proses pembayaran sebesar Rp {jumlah_bayar:,}?\n"
            f"Metode: {metode}"
        )
        
        if konfirmasi:
            # Simpan ke database
            success = self.db.tambah_pembayaran(
                self.selected_penyewaan_id, jumlah_bayar, metode
            )
            
            if success:
                messagebox.showinfo("Berhasil", "Pembayaran berhasil diproses!")
                
                # Update form
                self.cari_penyewaan_untuk_bayar()
                self.jumlah_bayar_var.set("")
                
                # Refresh data
                self.load_riwayat_pembayaran_harian()
                
                self.status_bar.config(text="Pembayaran berhasil diproses")
            else:
                messagebox.showerror("Error", "Gagal memproses pembayaran!")
    
    def cetak_struk(self):
        """Cetak struk pembayaran"""
        if not hasattr(self, 'selected_penyewaan_id'):
            messagebox.showwarning("Peringatan", "Pilih penyewaan terlebih dahulu!")
            return
        
        # Ambil riwayat pembayaran terakhir
        riwayat = self.db.get_pembayaran_by_penyewaan(self.selected_penyewaan_id)
        if not riwayat:
            messagebox.showwarning("Peringatan", "Belum ada pembayaran untuk penyewaan ini!")
            return
        
        # Ambil pembayaran terakhir
        pembayaran_terakhir = riwayat[-1]
        
        # Tampilkan struk dalam messagebox
        struk_text = f"""
=================================
STRUK PEMBAYARAN SEWA LAPANGAN
=================================
No. Transaksi : {pembayaran_terakhir['id_pembayaran']}
Tanggal       : {pembayaran_terakhir['tanggal_bayar']}

Data Member:
------------
Nama    : {self.selected_penyewaan.get('nama_member', '-')}
Alamat  : {self.selected_penyewaan.get('alamat', '-')}
Telepon : {self.selected_penyewaan.get('no_telepon', '-')}

Data Penyewaan:
---------------
Lapangan : {self.selected_penyewaan.get('nama_lapangan', '-')}
Tanggal  : {self.selected_penyewaan.get('tanggal_sewa', '-')}
Jam      : {self.selected_penyewaan.get('jam_mulai', '-')} - {self.selected_penyewaan.get('jam_selesai', '-')}

Pembayaran:
-----------
Jumlah Bayar : Rp {pembayaran_terakhir['jumlah_bayar']:,}
Metode       : {pembayaran_terakhir['metode_pembayaran']}

=================================
TERIMA KASIH
=================================
"""
        messagebox.showinfo("Struk Pembayaran", struk_text)
        self.status_bar.config(text="Struk berhasil dicetak")
    
    def lihat_riwayat_pembayaran(self):
        """Lihat riwayat pembayaran"""
        if not hasattr(self, 'selected_penyewaan_id'):
            messagebox.showwarning("Peringatan", "Pilih penyewaan terlebih dahulu!")
            return
        
        riwayat = self.db.get_pembayaran_by_penyewaan(self.selected_penyewaan_id)
        if not riwayat:
            messagebox.showinfo("Info", "Belum ada riwayat pembayaran untuk penyewaan ini.")
            return
        
        # Tampilkan dalam dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Riwayat Pembayaran - ID: {self.selected_penyewaan_id}")
        dialog.geometry("600x400")
        
        # Treeview riwayat
        columns = ("ID", "Jumlah", "Metode", "Tanggal")
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Isi data
        total_bayar = 0
        for pembayaran in riwayat:
            tree.insert('', 'end', values=(
                pembayaran['id_pembayaran'],
                f"Rp {pembayaran['jumlah_bayar']:,}",
                pembayaran['metode_pembayaran'],
                pembayaran['tanggal_bayar']
            ))
            total_bayar += pembayaran['jumlah_bayar']
        
        # Total
        ttk.Label(dialog, text=f"Total Telah Dibayar: Rp {total_bayar:,}",
                 font=('Arial', 10, 'bold')).pack(pady=10)
    
    def load_riwayat_pembayaran_harian(self):
        """Load riwayat pembayaran hari ini"""
        for item in self.riwayat_pembayaran_tree.get_children():
            self.riwayat_pembayaran_tree.delete(item)
        
        # Ambil tanggal hari ini
        today = dt.datetime.now().strftime("%Y-%m-%d")
        riwayat_data = self.db.get_total_pembayaran_harian(today)
        
        if riwayat_data:
            for riwayat in riwayat_data:
                self.riwayat_pembayaran_tree.insert('', 'end', values=(
                    riwayat.get('jumlah_transaksi', '-'),
                    riwayat.get('tanggal', '-'),
                    "-",
                    f"Rp {riwayat.get('total_pembayaran', 0):,}",
                    "-",
                    today
                ))
        
        # Ambil detail transaksi terbaru
        query = """
        SELECT p.*, ps.id_penyewaan, m.nama as nama_member
        FROM pembayaran p
        JOIN penyewaan ps ON p.id_penyewaan = ps.id_penyewaan
        JOIN member m ON ps.id_member = m.id_member
        WHERE DATE(p.tanggal_bayar) = %s
        ORDER BY p.tanggal_bayar DESC
        LIMIT 10
        """
        params = (today,)
        detail_data = self.db.execute_query(query, params, fetch=True)
        
        if detail_data:
            for i, transaksi in enumerate(detail_data):
                self.riwayat_pembayaran_tree.insert('', 'end', values=(
                    transaksi['id_pembayaran'],
                    transaksi['id_penyewaan'],
                    transaksi['nama_member'],
                    f"Rp {transaksi['jumlah_bayar']:,}",
                    transaksi['metode_pembayaran'],
                    transaksi['tanggal_bayar'].strftime("%H:%M:%S")
                ))
    
    # ========== METHOD UNTUK TAB MEMBER ==========
    
    def load_member_management_data(self):
        """Load data ke treeview manajemen member"""
        for item in self.member_management_tree.get_children():
            self.member_management_tree.delete(item)
        
        member_data = self.db.get_semua_member()
        if member_data:
            for member in member_data:
                # Potong alamat jika terlalu panjang
                alamat = member['alamat']
                if len(alamat) > 30:
                    alamat = alamat[:27] + "..."
                
                self.member_management_tree.insert('', 'end', values=(
                    member['id_member'],
                    member['nama'],
                    member['umur'],
                    member['jenis_kelamin'],
                    member['no_telepon'],
                    alamat
                ), tags=(member['id_member'],))
    
    def cari_member_gui(self, keyword):
        """Cari member dari GUI"""
        if not keyword:
            self.load_member_management_data()
            return
        
        for item in self.member_management_tree.get_children():
            self.member_management_tree.delete(item)
        
        hasil = self.db.cari_member(keyword)
        if hasil:
            for member in hasil:
                alamat = member['alamat']
                if len(alamat) > 30:
                    alamat = alamat[:27] + "..."
                
                self.member_management_tree.insert('', 'end', values=(
                    member['id_member'],
                    member['nama'],
                    member['umur'],
                    member['jenis_kelamin'],
                    member['no_telepon'],
                    alamat
                ))
            
            self.status_bar.config(text=f"Ditemukan {len(hasil)} member untuk '{keyword}'")
        else:
            self.status_bar.config(text=f"Tidak ditemukan member untuk '{keyword}'")
    
    def on_member_selected(self, event):
        """Ketika member dipilih dari treeview"""
        selection = self.member_management_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        member_id = self.member_management_tree.item(item, 'values')[0]
        
        # Ambil detail member dari database
        query = "SELECT * FROM member WHERE id_member = %s"
        result = self.db.execute_query(query, (member_id,), fetch=True)
        
        if result and len(result) > 0:
            member = result[0]
            
            # Ambil total penyewaan
            penyewaan_data = self.db.get_penyewaan_by_member(member_id)
            total_sewa = len(penyewaan_data) if penyewaan_data else 0
            
            # Tampilkan di detail panel
            self.member_detail_vars['id_detail'].set(member['id_member'])
            self.member_detail_vars['nama_detail'].set(member['nama'])
            self.member_detail_vars['umur_detail'].set(str(member['umur']))
            self.member_detail_vars['jk_detail'].set(member['jenis_kelamin'])
            
            # Clear dan insert untuk text widget
            self.member_detail_vars['alamat_detail'].config(state='normal')
            self.member_detail_vars['alamat_detail'].delete("1.0", tk.END)
            self.member_detail_vars['alamat_detail'].insert("1.0", member['alamat'])
            self.member_detail_vars['alamat_detail'].config(state='disabled')
            
            self.member_detail_vars['telp_detail'].set(member['no_telepon'])
            self.member_detail_vars['tgl_detail'].set(str(member.get('tanggal_daftar', '-')))
            self.member_detail_vars['total_sewa_detail'].set(str(total_sewa))
            
            self.status_bar.config(text=f"Memilih member: {member['nama']}")
            
            # Simpan ID member yang sedang dipilih
            self.selected_member_id = member_id
    
    def reset_pencarian_member(self):
        """Reset pencarian member"""
        self.search_member_var.set("")
        self.load_member_management_data()
        self.status_bar.config(text="Pencarian direset")
    
    def edit_member(self):
        """Edit data member"""
        if not hasattr(self, 'selected_member_id') or not self.selected_member_id:
            messagebox.showwarning("Peringatan", "Pilih member terlebih dahulu!")
            return
        
        # Buat popup edit
        self.create_edit_member_dialog()
    
    def hapus_member(self):
        """Hapus data member"""
        if not hasattr(self, 'selected_member_id') or not self.selected_member_id:
            messagebox.showwarning("Peringatan", "Pilih member terlebih dahulu!")
            return
        
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus member ini?\n"
            f"ID: {self.selected_member_id}"
        )
        
        if konfirmasi:
            try:
                query = "DELETE FROM member WHERE id_member = %s"
                result = self.db.execute_query(query, (self.selected_member_id,))
                
                if result:
                    messagebox.showinfo("Berhasil", "Member berhasil dihapus!")
                    self.load_member_management_data()
                    
                    # Clear detail panel
                    for key, widget in self.member_detail_vars.items():
                        if isinstance(widget, tk.StringVar):
                            widget.set("")
                        elif isinstance(widget, tk.Text):
                            widget.config(state='normal')
                            widget.delete("1.0", tk.END)
                            widget.config(state='disabled')
                    
                    self.selected_member_id = None
                    self.status_bar.config(text="Member berhasil dihapus")
                else:
                    messagebox.showerror("Error", "Gagal menghapus member!")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def create_edit_member_dialog(self):
        """Buat dialog edit member"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Data Member")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Ambil data member saat ini
        query = "SELECT * FROM member WHERE id_member = %s"
        result = self.db.execute_query(query, (self.selected_member_id,), fetch=True)
        
        if not result:
            dialog.destroy()
            return
        
        member = result[0]
        
        # Frame form
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill='both', expand=True)
        
        ttk.Label(form_frame, text=f"Edit Member: {self.selected_member_id}",
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Fields
        fields = [
            ("Nama:", "nama", member['nama']),
            ("Umur:", "umur", member['umur']),
            ("JK:", "jk", member['jenis_kelamin']),
            ("Alamat:", "alamat", member['alamat']),
            ("Telepon:", "telp", member['no_telepon'])
        ]
        
        entry_widgets = {}
        
        for i, (label, key, value) in enumerate(fields, start=1):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky='w', pady=5)
            
            if key == "alamat":
                text_widget = tk.Text(form_frame, height=4, width=30)
                text_widget.insert("1.0", value)
                text_widget.grid(row=i, column=1, pady=5, padx=5)
                entry_widgets[key] = text_widget
            elif key == "jk":
                var = tk.StringVar(value=value)
                frame = ttk.Frame(form_frame)
                frame.grid(row=i, column=1, sticky='w', pady=5, padx=5)
                ttk.Radiobutton(frame, text="Laki-laki", variable=var, value="Laki-laki").pack(side='left')
                ttk.Radiobutton(frame, text="Perempuan", variable=var, value="Perempuan").pack(side='left', padx=10)
                entry_widgets[key] = var
            else:
                var = tk.StringVar(value=str(value))
                entry = ttk.Entry(form_frame, textvariable=var, width=30)
                entry.grid(row=i, column=1, pady=5, padx=5)
                entry_widgets[key] = var
        
        def simpan_perubahan():
            """Simpan perubahan ke database"""
            try:
                # Ambil data dari form
                nama = entry_widgets['nama'].get() if isinstance(entry_widgets['nama'], tk.StringVar) else entry_widgets['nama']
                umur = int(entry_widgets['umur'].get()) if isinstance(entry_widgets['umur'], tk.StringVar) else entry_widgets['umur']
                jk = entry_widgets['jk'].get() if isinstance(entry_widgets['jk'], tk.StringVar) else entry_widgets['jk']
                alamat = entry_widgets['alamat'].get("1.0", tk.END).strip() if isinstance(entry_widgets['alamat'], tk.Text) else entry_widgets['alamat']
                telp = entry_widgets['telp'].get() if isinstance(entry_widgets['telp'], tk.StringVar) else entry_widgets['telp']
                
                # Validasi
                if not nama:
                    messagebox.showwarning("Peringatan", "Nama harus diisi!")
                    return
                
                # Update database
                query = """
                UPDATE member
                SET nama = %s, umur = %s, jenis_kelamin = %s,
                    alamat = %s, no_telepon = %s
                WHERE id_member = %s
                """
                params = (nama, umur, jk, alamat, telp, self.selected_member_id)
                
                if self.db.execute_query(query, params):
                    messagebox.showinfo("Berhasil", "Data member berhasil diperbarui!")
                    dialog.destroy()
                    self.load_member_management_data()
                    self.on_member_selected(None)  # Refresh detail
                    self.status_bar.config(text=f"Data {nama} diperbarui")
                else:
                    messagebox.showerror("Error", "Gagal memperbarui data!")
                    
            except ValueError:
                messagebox.showwarning("Peringatan", "Umur harus berupa angka!")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        
        # Tombol
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Simpan", command=simpan_perubahan,
                  width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Batal", command=dialog.destroy,
                  width=15).pack(side='left', padx=5)
    
    def lihat_riwayat_member(self):
        """Lihat riwayat penyewaan member"""
        if not hasattr(self, 'selected_member_id') or not self.selected_member_id:
            messagebox.showwarning("Peringatan", "Pilih member terlebih dahulu!")
            return
        
        # Ambil riwayat dari database
        riwayat = self.db.get_penyewaan_by_member(self.selected_member_id)
        if not riwayat:
            messagebox.showinfo("Info", "Member ini belum memiliki riwayat penyewaan.")
            return
        
        # Tampilkan dalam dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Riwayat Penyewaan - {self.selected_member_id}")
        dialog.geometry("800x400")
        
        # Treeview riwayat
        columns = ("ID", "Tanggal", "Lapangan", "Jam", "Durasi", "Biaya", "Status")
        tree = ttk.Treeview(dialog, columns=columns, show='headings', height=15)
        
        widths = [60, 100, 120, 100, 60, 100, 80]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Isi data
        total_biaya = 0
        for penyewaan in riwayat:
            tree.insert('', 'end', values=(
                penyewaan.get('id_penyewaan', '-'),
                penyewaan.get('tanggal_sewa', '-'),
                penyewaan.get('nama_lapangan', '-'),
                f"{penyewaan.get('jam_mulai', '-')} - {penyewaan.get('jam_selesai', '-')}",
                f"{penyewaan.get('durasi_jam', 0)} jam",
                f"Rp {penyewaan.get('total_biaya', 0):,}",
                penyewaan.get('status_pembayaran', '-')
            ))
            total_biaya += penyewaan.get('total_biaya', 0)
        
        # Total
        ttk.Label(dialog, text=f"Total Pengeluaran: Rp {total_biaya:,}",
                 font=('Arial', 10, 'bold')).pack(pady=10)
    
    # ========== METHOD UNTUK TAB LAPORAN ==========
    
    def load_statistik_harian(self):
        """Memuat data statistik harian"""
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        stats_data = self.db.get_statistik_harian()
        if stats_data:
            for stat in stats_data:
                self.stats_tree.insert('', 'end', values=(
                    stat['tanggal'],
                    stat['jumlah_penyewaan'],
                    stat['jumlah_member'],
                    f"Rp {stat['total_pendapatan']:,}"
                ))
    
    def load_statistik_popularitas(self):
        """Memuat statistik popularitas lapangan"""
        for item in self.popularitas_tree.get_children():
            self.popularitas_tree.delete(item)
        
        stats_data = self.db.get_statistik_lapangan()
        if stats_data:
            for stat in stats_data:
                self.popularitas_tree.insert('', 'end', values=(
                    stat['nama_lapangan'],
                    stat['jenis_olahraga'],
                    stat['jumlah_penyewaan'],
                    f"Rp {stat.get('total_pendapatan', 0):,}"
                ))
    
    def load_statistik_member(self):
        """Memuat statistik member"""
        for item in self.member_report_tree.get_children():
            self.member_report_tree.delete(item)
        
        # Query untuk mendapatkan member aktif
        query = """
        SELECT 
            m.id_member,
            m.nama,
            m.tanggal_daftar,
            COUNT(p.id_penyewaan) as jumlah_penyewaan,
            COALESCE(SUM(p.total_biaya), 0) as total_pengeluaran
        FROM member m
        LEFT JOIN penyewaan p ON m.id_member = p.id_member
        GROUP BY m.id_member, m.nama, m.tanggal_daftar
        ORDER BY total_pengeluaran DESC
        LIMIT 10
        """
        
        result = self.db.execute_query(query, fetch=True)
        if result:
            for member in result:
                self.member_report_tree.insert('', 'end', values=(
                    member['nama'],
                    member['jumlah_penyewaan'],
                    f"Rp {member['total_pengeluaran']:,}",
                    member['tanggal_daftar'].strftime("%Y-%m-%d")
                ))
    
    def refresh_laporan(self):
        """Refresh semua data laporan"""
        self.load_statistik_harian()
        self.load_statistik_popularitas()
        self.load_statistik_member()
        self.status_bar.config(text="Data laporan direfresh")
    
    def run(self):
        """Menjalankan aplikasi"""
        self.root.mainloop()

def main():
    """Fungsi utama untuk menjalankan GUI"""
    root = tk.Tk()
    app = SewaLapanganGUI(root)
    app.run()

if __name__ == "__main__":
    main()