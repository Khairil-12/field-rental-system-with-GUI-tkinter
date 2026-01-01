import mysql.connector
from mysql.connector import Error
from config import Config
import datetime

class Database:
    """Kelas untuk mengelola koneksi database"""
    
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Membuat koneksi ke database"""
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                port=Config.DB_PORT
            )
            if self.connection.is_connected():
                print(f"✓ Terhubung ke database: {Config.DB_NAME}")
                return True
        except Error as e:
            print(f"✗ Gagal terhubung ke database: {e}")
            return False
    
    def execute_query(self, query, params=None, fetch=False):
        """Menjalankan query SQL"""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                print(f"[QUERY DEBUG] SELECT returned {len(result)} rows")
            else:
                self.connection.commit()
                result = cursor.rowcount
                print(f"[QUERY DEBUG] Query executed, rows affected: {result}")
            
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"✗ MySQL Error: {e}")
            print(f" Error code: {e.errno}")
            print(f" SQL State: {e.sqlstate}")
            
            if self.connection:
                try:
                    self.connection.rollback()
                    print(" ↻ Rollback executed")
                except:
                    pass
            return False
        except Exception as e:
            print(f"✗ General Error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if cursor:
                cursor.close()
    
    # ========== METHOD UNTUK MEMBER ==========
    def tambah_member(self, id_member, nama, umur, jenis_kelamin, alamat, no_telepon):
        """Menambahkan member baru"""
        query = """
        INSERT INTO member (id_member, nama, umur, jenis_kelamin, alamat, no_telepon)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (id_member, nama, umur, jenis_kelamin, alamat, no_telepon)
        print(f"\n[DB] Menyimpan member: {nama} (ID: {id_member})")
        
        try:
            success = self.execute_query(query, params)
            if success:
                print(f"[DB] ✓ Member berhasil disimpan")
                return True
            else:
                print("[DB] ✗ Gagal menyimpan member")
                return False
        except Exception as e:
            print(f"[DB] ✗ Exception: {e}")
            return False
    
    def get_semua_member(self):
        """Mendapatkan semua member"""
        query = "SELECT * FROM member ORDER BY id_member"
        result = self.execute_query(query, fetch=True)
        
        if result is None:
            print("[DB] Warning: get_semua_member returned None")
            return []
        
        return result
    
    def cari_member(self, keyword):
        """Mencari member berdasarkan nama atau ID"""
        query = """
        SELECT * FROM member
        WHERE nama LIKE %s OR id_member LIKE %s
        ORDER BY nama
        """
        params = (f"%{keyword}%", f"%{keyword}%")
        return self.execute_query(query, params, fetch=True)
    
    def update_member(self, id_member, nama, umur, jenis_kelamin, alamat, no_telepon):
        """Update data member"""
        query = """
        UPDATE member
        SET nama = %s, umur = %s, jenis_kelamin = %s,
            alamat = %s, no_telepon = %s
        WHERE id_member = %s
        """
        params = (nama, umur, jenis_kelamin, alamat, no_telepon, id_member)
        return self.execute_query(query, params)
    
    def hapus_member(self, id_member):
        """Menghapus member"""
        query = "DELETE FROM member WHERE id_member = %s"
        params = (id_member,)
        return self.execute_query(query, params)
    
    # ========== METHOD UNTUK LAPANGAN ==========
    def get_semua_lapangan(self):
        """Mendapatkan semua lapangan"""
        query = "SELECT * FROM lapangan ORDER BY jenis_olahraga, nama_lapangan"
        return self.execute_query(query, fetch=True)
    
    def get_lapangan_by_jenis(self, jenis_olahraga):
        """Mendapatkan lapangan berdasarkan jenis olahraga"""
        query = """
        SELECT * FROM lapangan 
        WHERE jenis_olahraga = %s AND status = 'Tersedia'
        ORDER BY harga_per_jam
        """
        params = (jenis_olahraga,)
        return self.execute_query(query, params, fetch=True)
    
    def get_lapangan_by_id(self, id_lapangan):
        """Mendapatkan lapangan berdasarkan ID"""
        query = "SELECT * FROM lapangan WHERE id_lapangan = %s"
        params = (id_lapangan,)
        result = self.execute_query(query, params, fetch=True)
        return result[0] if result else None
    
    def update_status_lapangan(self, id_lapangan, status):
        """Update status lapangan"""
        query = "UPDATE lapangan SET status = %s WHERE id_lapangan = %s"
        params = (status, id_lapangan)
        return self.execute_query(query, params)
    
    # ========== METHOD UNTUK PENYEWAAN ==========
    def tambah_penyewaan(self, id_member, id_lapangan, tanggal_sewa, 
                         jam_mulai, jam_selesai, durasi_jam, total_biaya):
        """Menambahkan data penyewaan"""
        query = """
        INSERT INTO penyewaan 
        (id_member, id_lapangan, tanggal_sewa, jam_mulai, jam_selesai, durasi_jam, total_biaya)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (id_member, id_lapangan, tanggal_sewa, jam_mulai, jam_selesai, durasi_jam, total_biaya)
        return self.execute_query(query, params)
    
    def cek_ketersediaan_lapangan(self, id_lapangan, tanggal, jam_mulai, jam_selesai):
        """Memeriksa ketersediaan lapangan pada waktu tertentu"""
        query = """
        SELECT COUNT(*) as jumlah
        FROM penyewaan
        WHERE id_lapangan = %s 
          AND tanggal_sewa = %s
          AND (
            (jam_mulai < %s AND jam_selesai > %s) OR
            (jam_mulai >= %s AND jam_mulai < %s) OR
            (jam_selesai > %s AND jam_selesai <= %s)
          )
        """
        params = (id_lapangan, tanggal, jam_selesai, jam_mulai, 
                 jam_mulai, jam_selesai, jam_mulai, jam_selesai)
        
        result = self.execute_query(query, params, fetch=True)
        if result and result[0]['jumlah'] == 0:
            return True  # Tersedia
        return False  # Tidak tersedia
    
    def get_penyewaan_by_member(self, id_member):
        """Mendapatkan penyewaan berdasarkan member"""
        query = """
        SELECT p.*, l.nama_lapangan, l.jenis_olahraga, l.harga_per_jam,
               m.nama as nama_member
        FROM penyewaan p
        JOIN lapangan l ON p.id_lapangan = l.id_lapangan
        JOIN member m ON p.id_member = m.id_member
        WHERE p.id_member = %s
        ORDER BY p.tanggal_sewa DESC, p.jam_mulai DESC
        """
        params = (id_member,)
        return self.execute_query(query, params, fetch=True)
    
    def get_penyewaan_belum_lunas(self):
        """Mendapatkan semua penyewaan yang belum lunas"""
        query = """
        SELECT p.*, m.nama as nama_member, l.nama_lapangan
        FROM penyewaan p
        JOIN member m ON p.id_member = m.id_member
        JOIN lapangan l ON p.id_lapangan = l.id_lapangan
        WHERE p.status_pembayaran != 'Lunas'
        ORDER BY p.tanggal_pesan
        """
        return self.execute_query(query, fetch=True)
    
    def get_detail_penyewaan(self, id_penyewaan):
        """Mendapatkan detail penyewaan"""
        query = """
        SELECT p.*, m.nama as nama_member, m.alamat, m.no_telepon,
               l.nama_lapangan, l.jenis_olahraga, l.harga_per_jam
        FROM penyewaan p
        JOIN member m ON p.id_member = m.id_member
        JOIN lapangan l ON p.id_lapangan = l.id_lapangan
        WHERE p.id_penyewaan = %s
        """
        params = (id_penyewaan,)
        result = self.execute_query(query, params, fetch=True)
        return result[0] if result else None
    
    def update_status_penyewaan(self, id_penyewaan, status):
        """Update status pembayaran penyewaan"""
        query = "UPDATE penyewaan SET status_pembayaran = %s WHERE id_penyewaan = %s"
        params = (status, id_penyewaan)
        return self.execute_query(query, params)
    
    # ========== METHOD UNTUK PEMBAYARAN ==========
    def tambah_pembayaran(self, id_penyewaan, jumlah_bayar, metode_pembayaran):
        """Menambahkan pembayaran"""
        query = """
        INSERT INTO pembayaran (id_penyewaan, jumlah_bayar, metode_pembayaran)
        VALUES (%s, %s, %s)
        """
        params = (id_penyewaan, jumlah_bayar, metode_pembayaran)
        result = self.execute_query(query, params)
        
        if result:
            self._update_status_penyewaan(id_penyewaan, jumlah_bayar)
        
        return result
    
    def _update_status_penyewaan(self, id_penyewaan, jumlah_bayar):
        """Update status penyewaan setelah pembayaran"""
        # Hitung total yang sudah dibayar
        query_total = """
        SELECT SUM(jumlah_bayar) as total_bayar
        FROM pembayaran
        WHERE id_penyewaan = %s
        """
        params_total = (id_penyewaan,)
        result = self.execute_query(query_total, params_total, fetch=True)
        
        if result and result[0]['total_bayar']:
            total_bayar = result[0]['total_bayar']
            
            # Dapatkan total biaya penyewaan
            query_biaya = "SELECT total_biaya FROM penyewaan WHERE id_penyewaan = %s"
            biaya_result = self.execute_query(query_biaya, (id_penyewaan,), fetch=True)
            
            if biaya_result and biaya_result[0]['total_biaya']:
                biaya = biaya_result[0]['total_biaya']
                status = "Lunas" if total_bayar >= biaya else "DP"
                
                # Update status penyewaan
                query_update = """
                UPDATE penyewaan
                SET status_pembayaran = %s
                WHERE id_penyewaan = %s
                """
                self.execute_query(query_update, (status, id_penyewaan))
    
    def get_pembayaran_by_penyewaan(self, id_penyewaan):
        """Mendapatkan riwayat pembayaran untuk penyewaan"""
        query = """
        SELECT * FROM pembayaran
        WHERE id_penyewaan = %s
        ORDER BY tanggal_bayar
        """
        params = (id_penyewaan,)
        return self.execute_query(query, params, fetch=True)
    
    def get_total_sudah_dibayar(self, id_penyewaan):
        """Mendapatkan total yang sudah dibayar untuk penyewaan"""
        query = """
        SELECT COALESCE(SUM(jumlah_bayar), 0) as total_bayar
        FROM pembayaran
        WHERE id_penyewaan = %s
        """
        params = (id_penyewaan,)
        result = self.execute_query(query, params, fetch=True)
        return result[0]['total_bayar'] if result else 0
    
    def get_total_pembayaran_harian(self, tanggal=None):
        """Mendapatkan total pembayaran harian"""
        if not tanggal:
            tanggal = datetime.datetime.now().strftime("%Y-%m-%d")
        
        query = """
        SELECT
            DATE(tanggal_bayar) as tanggal,
            COUNT(*) as jumlah_transaksi,
            SUM(jumlah_bayar) as total_pembayaran
        FROM pembayaran
        WHERE DATE(tanggal_bayar) = %s
        GROUP BY DATE(tanggal_bayar)
        """
        params = (tanggal,)
        return self.execute_query(query, params, fetch=True)
    
    # ========== METHOD UNTUK LAPORAN ==========
    def get_statistik_harian(self):
        """Mendapatkan statistik harian"""
        query = """
        SELECT
            DATE(tanggal_sewa) as tanggal,
            COUNT(*) as jumlah_penyewaan,
            SUM(total_biaya) as total_pendapatan,
            COUNT(DISTINCT id_member) as jumlah_member
        FROM penyewaan
        GROUP BY DATE(tanggal_sewa)
        ORDER BY tanggal DESC
        LIMIT 7
        """
        return self.execute_query(query, fetch=True)
    
    def get_statistik_lapangan(self):
        """Mendapatkan statistik popularitas lapangan"""
        query = """
        SELECT
            l.id_lapangan,
            l.nama_lapangan,
            l.jenis_olahraga,
            COUNT(p.id_penyewaan) as jumlah_penyewaan,
            SUM(p.total_biaya) as total_pendapatan
        FROM lapangan l
        LEFT JOIN penyewaan p ON l.id_lapangan = p.id_lapangan
        GROUP BY l.id_lapangan, l.nama_lapangan, l.jenis_olahraga
        ORDER BY jumlah_penyewaan DESC
        """
        return self.execute_query(query, fetch=True)
    
    def get_jadwal_lapangan_hari_ini(self):
        """Mendapatkan jadwal lapangan hari ini"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        query = """
        SELECT
            p.id_penyewaan,
            p.jam_mulai,
            p.jam_selesai,
            m.nama as nama_member,
            l.nama_lapangan,
            l.jenis_olahraga
        FROM penyewaan p
        JOIN member m ON p.id_member = m.id_member
        JOIN lapangan l ON p.id_lapangan = l.id_lapangan
        WHERE p.tanggal_sewa = %s
        ORDER BY p.jam_mulai
        """
        params = (today,)
        return self.execute_query(query, params, fetch=True)
    
    def close(self):
        """Menutup koneksi database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Koneksi database ditutup")