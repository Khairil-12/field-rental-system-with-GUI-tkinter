CREATE DATABASE IF NOT EXISTS sewa_lapangan_db;
USE sewa_lapangan_db;

-- ==================== TABEL MEMBER/PELANGGAN ====================
CREATE TABLE IF NOT EXISTS member (
    id_member VARCHAR(10) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    umur INT,
    jenis_kelamin ENUM('Laki-laki', 'Perempuan'),
    alamat TEXT,
    no_telepon VARCHAR(15),
    tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==================== TABEL LAPANGAN ====================
CREATE TABLE IF NOT EXISTS lapangan (
    id_lapangan VARCHAR(10) PRIMARY KEY,
    nama_lapangan VARCHAR(100) NOT NULL,
    jenis_olahraga ENUM('Futsal', 'Badminton', 'Tennis', 'Basket', 'Voli'),
    harga_per_jam DECIMAL(12,2) NOT NULL,
    status ENUM('Tersedia', 'Dalam Perawatan', 'Tidak Tersedia') DEFAULT 'Tersedia'
);

-- ==================== TABEL PENYEWAAN ====================
CREATE TABLE IF NOT EXISTS penyewaan (
    id_penyewaan INT PRIMARY KEY AUTO_INCREMENT,
    id_member VARCHAR(10) NOT NULL,
    id_lapangan VARCHAR(10) NOT NULL,
    tanggal_sewa DATE NOT NULL,
    jam_mulai TIME NOT NULL,
    jam_selesai TIME NOT NULL,
    durasi_jam INT NOT NULL,
    total_biaya DECIMAL(12,2) NOT NULL,
    status_pembayaran ENUM('Belum Bayar', 'DP', 'Lunas') DEFAULT 'Belum Bayar',
    tanggal_pesan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_member) REFERENCES member(id_member) ON DELETE CASCADE,
    FOREIGN KEY (id_lapangan) REFERENCES lapangan(id_lapangan) ON DELETE CASCADE
);

-- ==================== TABEL PEMBAYARAN ====================
CREATE TABLE IF NOT EXISTS pembayaran (
    id_pembayaran INT PRIMARY KEY AUTO_INCREMENT,
    id_penyewaan INT NOT NULL,
    jumlah_bayar DECIMAL(12,2) NOT NULL,
    metode_pembayaran ENUM('Tunai', 'Transfer', 'Debit', 'Kredit') DEFAULT 'Tunai',
    tanggal_bayar TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_penyewaan) REFERENCES penyewaan(id_penyewaan) ON DELETE CASCADE
);

-- ==================== TABEL ANTRIAN ====================
CREATE TABLE IF NOT EXISTS antrian (
    id_antrian INT PRIMARY KEY AUTO_INCREMENT,
    jenis ENUM('Pendaftaran', 'Pemesanan', 'Pembayaran'),
    id_member VARCHAR(10),
    status ENUM('Menunggu', 'Diproses', 'Selesai') DEFAULT 'Menunggu',
    waktu_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_member) REFERENCES member(id_member)
);

-- ========== DATA SAMPLE LAPANGAN ==========
INSERT IGNORE INTO lapangan (id_lapangan, nama_lapangan, jenis_olahraga, harga_per_jam, status) VALUES
('L001', 'Lapangan Futsal A', 'Futsal', 150000.00, 'Tersedia'),
('L002', 'Lapangan Futsal B', 'Futsal', 120000.00, 'Tersedia'),
('L003', 'Lapangan Badminton 1', 'Badminton', 80000.00, 'Tersedia'),
('L004', 'Lapangan Badminton 2', 'Badminton', 80000.00, 'Tersedia'),
('L005', 'Lapangan Tennis', 'Tennis', 200000.00, 'Tersedia'),
('L006', 'Lapangan Basket', 'Basket', 100000.00, 'Tersedia'),
('L007', 'Lapangan Voli', 'Voli', 90000.00, 'Tersedia');