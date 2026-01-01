class Config:
    """Kelas untuk konfigurasi aplikasi"""
    
    # Konfigurasi Database
    DB_HOST = "127.0.0.1"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "sewa_lapangan_db"
    DB_PORT = 3306
    
    # Konfigurasi Aplikasi
    APP_NAME = "Sistem Sewa Lapangan Olahraga"
    APP_VERSION = "1.0.0"
    
    # Jam operasional
    JAM_BUKA = 8  # 08:00
    JAM_TUTUP = 22  # 22:00
    
    # Konfigurasi Path
    BACKUP_DIR = "backups"
    LOG_DIR = "logs"
    
    @classmethod
    def get_db_config(cls):
        """Mengembalikan konfigurasi database sebagai dictionary"""
        return {
            'host': cls.DB_HOST,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD,
            'database': cls.DB_NAME,
            'port': cls.DB_PORT
        }
    
    @classmethod
    def get_jam_operasional(cls):
        """Mengembalikan list jam operasional"""
        return list(range(cls.JAM_BUKA, cls.JAM_TUTUP))