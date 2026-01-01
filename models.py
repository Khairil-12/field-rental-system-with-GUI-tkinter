from abc import ABC, abstractmethod
from datetime import datetime

# ========== KELAS ABSTRAK ==========
class Person(ABC):
    """Kelas abstrak untuk orang"""
    
    def __init__(self, id_person, nama):
        self._id_person = id_person
        self._nama = nama
    
    @abstractmethod
    def get_info(self):
        pass
    
    @property
    def id_person(self):
        return self._id_person
    
    @property
    def nama(self):
        return self._nama
    
    @nama.setter
    def nama(self, value):
        self._nama = value

# ========== KELAS MEMBER ==========
class Member(Person):
    """Kelas untuk member/pelanggan"""
    
    def __init__(self, id_member, nama, umur, jenis_kelamin, alamat="", no_telepon=""):
        super().__init__(id_member, nama)
        self._umur = umur
        self._jenis_kelamin = jenis_kelamin
        self._alamat = alamat
        self._no_telepon = no_telepon
        self._riwayat_sewa = []
        self._tanggal_daftar = datetime.now()
    
    def get_info(self):
        """Implementasi abstract method"""
        return f"{self._nama} ({self._umur} tahun, {self._jenis_kelamin})"
    
    def tambah_riwayat(self, penyewaan):
        """Menambah riwayat penyewaan"""
        self._riwayat_sewa.append(penyewaan)
    
    @property
    def umur(self):
        return self._umur
    
    @property
    def jenis_kelamin(self):
        return self._jenis_kelamin
    
    @property
    def alamat(self):
        return self._alamat
    
    @property
    def no_telepon(self):
        return self._no_telepon
    
    @property
    def tanggal_daftar(self):
        return self._tanggal_daftar
    
    @property
    def riwayat_sewa(self):
        return self._riwayat_sewa
    
    @property
    def total_pengeluaran(self):
        """Menghitung total pengeluaran member"""
        total = 0
        for sewa in self._riwayat_sewa:
            total += sewa._total_biaya
        return total

# ========== KELAS LAPANGAN ==========
class Lapangan:
    """Kelas untuk lapangan olahraga"""
    
    def __init__(self, id_lapangan, nama_lapangan, jenis_olahraga, 
                 harga_per_jam, status="Tersedia"):
        self._id_lapangan = id_lapangan
        self._nama_lapangan = nama_lapangan
        self._jenis_olahraga = jenis_olahraga
        self._harga_per_jam = harga_per_jam
        self._status = status
    
    def get_info(self):
        return f"{self._nama_lapangan} ({self._jenis_olahraga}) - Rp {self._harga_per_jam:,}/jam"
    
    @property
    def id_lapangan(self):
        return self._id_lapangan
    
    @property
    def nama_lapangan(self):
        return self._nama_lapangan
    
    @property
    def jenis_olahraga(self):
        return self._jenis_olahraga
    
    @property
    def harga_per_jam(self):
        return self._harga_per_jam
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        self._status = value

# ========== KELAS PENYEWAAN ==========
class Penyewaan:
    """Kelas untuk penyewaan lapangan"""
    
    def __init__(self, id_penyewaan, member, lapangan, tanggal_sewa, 
                 jam_mulai, jam_selesai, total_biaya, status_pembayaran="Belum Bayar"):
        self._id_penyewaan = id_penyewaan
        self._member = member
        self._lapangan = lapangan
        self._tanggal_sewa = tanggal_sewa
        self._jam_mulai = jam_mulai
        self._jam_selesai = jam_selesai
        self._total_biaya = total_biaya
        self._status_pembayaran = status_pembayaran
        self._durasi_jam = self._hitung_durasi()
    
    def _hitung_durasi(self):
        """Menghitung durasi dalam jam"""
        if isinstance(self._jam_mulai, str):
            jam_mulai = datetime.strptime(self._jam_mulai, "%H:%M").hour
            jam_selesai = datetime.strptime(self._jam_selesai, "%H:%M").hour
        else:
            jam_mulai = self._jam_mulai
            jam_selesai = self._jam_selesai
        
        return jam_selesai - jam_mulai
    
    def get_info(self):
        return f"Penyewaan {self._id_penyewaan}: {self._member.nama} - {self._lapangan.nama_lapangan}"
    
    @property
    def id_penyewaan(self):
        return self._id_penyewaan
    
    @property
    def member(self):
        return self._member
    
    @property
    def lapangan(self):
        return self._lapangan
    
    @property
    def tanggal_sewa(self):
        return self._tanggal_sewa
    
    @property
    def jam_mulai(self):
        return self._jam_mulai
    
    @property
    def jam_selesai(self):
        return self._jam_selesai
    
    @property
    def durasi_jam(self):
        return self._durasi_jam
    
    @property
    def total_biaya(self):
        return self._total_biaya
    
    @property
    def status_pembayaran(self):
        return self._status_pembayaran
    
    @status_pembayaran.setter
    def status_pembayaran(self, value):
        self._status_pembayaran = value

# ========== KELAS PEMBAYARAN ==========
class Pembayaran:
    """Kelas untuk pembayaran"""
    
    def __init__(self, id_pembayaran, penyewaan, jumlah_bayar, 
                 metode_pembayaran, tanggal_bayar):
        self._id_pembayaran = id_pembayaran
        self._penyewaan = penyewaan
        self._jumlah_bayar = jumlah_bayar
        self._metode_pembayaran = metode_pembayaran
        self._tanggal_bayar = tanggal_bayar
    
    @property
    def sisa_bayar(self):
        return self._penyewaan.total_biaya - self._jumlah_bayar
    
    @property
    def status(self):
        if self.sisa_bayar <= 0:
            return "Lunas"
        elif self._jumlah_bayar > 0:
            return "DP"
        else:
            return "Belum Bayar"
    
    def get_info(self):
        return f"Pembayaran {self._id_pembayaran}: {self._penyewaan.member.nama} - Rp {self._jumlah_bayar:,}"

# ========== KELAS SISTEM ==========
class SistemSewaLapangan:
    """Kelas utama sistem sewa lapangan"""
    
    def __init__(self, database):
        self.db = database
        self.member_aktif = None
        self.lapangan_aktif = None
    
    def daftar_member_baru(self, nama, umur, jenis_kelamin, alamat, no_telepon):
        """Mendaftarkan member baru"""
        print(f"\n[SYSTEM] === START: Daftar Member Baru ===")
        print(f" Nama: {nama}")
        print(f" Umur: {umur}")
        print(f" Jenis Kelamin: {jenis_kelamin}")
        
        try:
            # 1. Generate ID member
            semua_member = self.db.get_semua_member()
            if semua_member is None:
                semua_member = []
                print(" [INFO] Database kosong, mulai dari ID M001")
            
            print(f" [INFO] Total member saat ini: {len(semua_member)}")
            
            max_id = 0
            for m in semua_member:
                if 'id_member' in m:
                    id_str = m['id_member']
                    if id_str and id_str.startswith('M'):
                        try:
                            num = int(id_str[1:])
                            if num > max_id:
                                max_id = num
                        except:
                            continue
            
            next_id_num = max_id + 1
            id_member = f"M{next_id_num:03d}"
            print(f" [INFO] Generated ID: {id_member}")
            
            # 2. Buat objek Member
            print(" [INFO] Membuat objek Member...")
            member_obj = Member(
                id_member=id_member,
                nama=nama,
                umur=umur,
                jenis_kelamin=jenis_kelamin,
                alamat=alamat,
                no_telepon=no_telepon
            )
            print(f" [INFO] Objek Member dibuat: {member_obj.get_info()}")
            
            # 3. Simpan ke database
            print(" [INFO] Menyimpan ke database...")
            success = self.db.tambah_member(
                id_member, nama, umur, jenis_kelamin, alamat, no_telepon
            )
            
            if success:
                print(f" [SUCCESS] Member berhasil didaftarkan!")
                print(f" ID: {id_member}")
                print(f" Nama: {nama}")
                return member_obj
            else:
                print(" [ERROR] Gagal menyimpan ke database")
                return None
                
        except Exception as e:
            print(f" [EXCEPTION] Error di daftar_member_baru: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def cari_member(self, keyword):
        """Mencari member berdasarkan nama atau ID"""
        results = self.db.cari_member(keyword)
        member_list = []
        
        if results:
            for data in results:
                member = Member(
                    id_member=data['id_member'],
                    nama=data['nama'],
                    umur=data['umur'],
                    jenis_kelamin=data['jenis_kelamin'],
                    alamat=data.get('alamat', ''),
                    no_telepon=data.get('no_telepon', '')
                )
                member_list.append(member)
        
        return member_list
    
    def cek_ketersediaan_lapangan(self, id_lapangan, tanggal, jam_mulai, jam_selesai):
        """Memeriksa ketersediaan lapangan"""
        return self.db.cek_ketersediaan_lapangan(id_lapangan, tanggal, jam_mulai, jam_selesai)