import sys
import os
from database import Database

# Tambahkan path ke direktori
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Memeriksa dependencies"""
    try:
        import mysql.connector
        import tkinter
        print("✓ Dependencies OK")
        return True
    except ImportError as e:
        print(f"✗ Error: {e}")
        print("\nInstall dependencies:")
        print("pip install mysql-connector-python")
        return False

def check_database():
    """Memeriksa koneksi database"""
    print("\n" + "="*50)
    print("SISTEM SEWA LAPANGAN OLAHRAGA")
    print("="*50)
    print("\nMemeriksa koneksi database...")
    
    db = Database()
    if db.connection and db.connection.is_connected():
        try:
            cursor = db.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            
            print(f"✓ Database terhubung")
            print(f"✓ Jumlah tabel: {len(tables)}")
            print(f"✓ Tabel yang ada: {', '.join(table_names)}")
            
            # Cek tabel penting
            required_tables = ['member', 'lapangan', 'penyewaan', 'pembayaran']
            missing_tables = [t for t in required_tables if t not in table_names]
            
            if missing_tables:
                print(f"\n⚠ Tabel berikut belum ada: {', '.join(missing_tables)}")
                print(" Import file migration.sql ke phpMyAdmin")
                db.close()
                return False
            else:
                print("✓ Database siap digunakan")
                db.close()
                return True
                
        except Exception as e:
            print(f"✗ Error: {e}")
            db.close()
            return False
    else:
        print("✗ Gagal terhubung ke database")
        print("\nSOLUSI:")
        print("1. Pastikan XAMPP MySQL berjalan (lampu hijau)")
        print("2. Pastikan database 'sewa_lapangan_db' sudah dibuat")
        print("3. Import file migration.sql ke phpMyAdmin")
        return False

def create_sample_data():
    """Buat data sample jika database kosong"""
    print("\nMemeriksa data sample...")
    
    db = Database()
    try:
        # Cek apakah ada member
        member = db.get_semua_member()
        if not member:
            print("⚠ Database kosong, membuat data sample...")
            
            # Tambah member sample
            db.tambah_member("M001", "Andi Wijaya", 25, "Laki-laki", "Jl. Merdeka No. 123", "08123456789")
            db.tambah_member("M002", "Siti Nurhaliza", 22, "Perempuan", "Jl. Sudirman No. 45", "08234567890")
            db.tambah_member("M003", "Budi Santoso", 30, "Laki-laki", "Jl. Gatot Subroto No. 67", "08345678901")
            db.tambah_member("M004", "Dewi Lestari", 28, "Perempuan", "Jl. Thamrin No. 89", "08456789012")
            
            print("✓ Data sample member berhasil dibuat")
        
        # Cek apakah ada lapangan
        lapangan = db.get_semua_lapangan()
        if not lapangan:
            print("⚠ Data lapangan kosong, pastikan sudah import migration.sql")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Error membuat data sample: {e}")
        db.close()
        return False

def main():
    """Fungsi utama"""
    # Cek dependencies
    if not check_dependencies():
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
    
    # Cek database
    if not check_database():
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
    
    create_sample_data()
    
    print("\n" + "="*50)
    print("MEMULAI APLIKASI...")
    print("="*50 + "\n")
    
    try:
        from gui import main as run_gui
        run_gui()
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        print("\nPastikan semua file berikut ada:")
        print("1. config.py")
        print("2. models.py")
        print("3. database.py")
        print("4. gui.py")
        input("\nTekan Enter untuk keluar...")
    except Exception as e:
        print(f"✗ Error menjalankan aplikasi: {e}")
        import traceback
        traceback.print_exc()
        input("\nTekan Enter untuk keluar...")

if __name__ == "__main__":
    main()