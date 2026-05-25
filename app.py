import streamlit as st

#======================================================================
# KELAS NODE KATEGORI
#======================================================================
class KategoriNode:
    def __init__(self, nama_kategori):
        self.nama = nama_kategori
        self.sub_kategori = []

    def tambah_sub(self, node_kategori):
        self.sub_kategori.append(node_kategori)

    def tampilkan_tree(self, level=0):
        indentasi = "    " * level
        simbol = "↳ " if level > 0 else "📦 "
        print(f"{indentasi}{simbol}{self.nama}")
        
        for sub in self.sub_kategori:
            sub.tampilkan_tree(level + 1)

    def cari_node(self, target_nama):
        # Mencari node spesifik untuk menambahkan anak di bawahnya
        if self.nama.lower() == target_nama.lower():
            return self
            
        for sub in self.sub_kategori:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil
                
        return None

    def cari_jalur(self, target, path=""):
        # Mencari jalur lengkap (breadcrumb) seperti studi kasus sebelumnya
        jalur_saat_ini = path + " > " + self.nama if path else self.nama
        
        if self.nama.lower() == target.lower():
            return jalur_saat_ini
            
        for sub in self.sub_kategori:
            hasil = sub.cari_jalur(target, jalur_saat_ini)
            if hasil:
                return hasil
                
        return None

# ==========================================
# PROGRAM UTAMA (INTER)
# ==========================================
st.set_page_config(page_title="Struktur Kategori", page_icon="+")

st.title("Pembuat Struktur Kategori")
st.write("Aplikasi interaktif untuk mensimulasikan struktur data Tree.")
 
# Inisialisasi session state untuk menyimpan struktur Tree agar tidak hilang sa
if 'root' not in st.session_state:
    st.session_state.root = None 
# Jika Root belum dibuat, tampilkan form pembuatan Root
if st.session_state.root is None:
    st.info("Sistem belum memiliki kategori utama. Silakan buat terlebih dahulu")
    nama_root = st.text_input("Masukkan nama kategori utama (Root):", value="Toko Saya")
  
if st.button("Buat Kategori Utama", type="primary"):
    st.session_state.root = KategoriNode(nama_root)
    st.rerun() # Refresh halaman
# Jika Root sudah ada, tampilkan Menu Utama menggunakan Tabs
else:
    root = st.session_state.root

    # Mengganti menu CLI dengan sistem Tab yang lebih modern
    tab1, tab2, tab3 = st.tabs([" Lihat Struktur", "+ Tambah Sub-Kategori", "Cari Jalur"])

    # TAB 1: Lihat Struktur
    with tab1:
        st.subheader("Struktur Kategori Saat Ini")
        tree_teks = root.dapatkan_tree_string()
        #menggunakan st.code agar format identasi (spasi) tetap rapi
        st.code(tree_teks, language="teks")

    # TAB 2 : TAMBAH SUB kategori 
    with tab2:
        st.subheader("tambah cabang baru")
        induk_nama= st.teks_input("Nama kategori induk tempat cabang ditambakan:")
        anak_nama= st.teks_input("nama sub kategori baru:")

        if st.button("tambah kategori"):
            if induk_nama and anak_nama:
                induk_node = root.cari_node(induk_nama)
                if induk_node:
                    induk_node.tambah_sub(KategoriNode(anak_nama))
                    st.success(f"Berhasil menambahkan '{anak_nama}' di bawah '{induk_node.nama}'!")
                else:
                    st.error(f"Kategori '{induk_nama}' tidak ditemukan! Pastikan ejaannya benar.")
            else:
                st.warning("Harap isi kedua kolom di atas.")

    # TAB 3: Cari Jalur
    with tab3:
        st.subheader("pencarian breadcrumb")
        target_cari = st.teks_input("nama kategori yang ingin dicari jalurnya:")

        if st.button("cari jalur"):
            if target_cari:
                hasil= root.cari_jalur(target_cari)
                if hasil:
                    st.success("ditemukan!")
                    st.info(f"jalur: {hasil}")
                else:
                    st.error(f"kategori '{target_cari}' tidak ditemukan dalam sistem")
            else:
                st.warning("harap isi nama ketegori yang dicari.")

    # TOMBOL RISET
    st.divider()
    if st.button("riset sistem / mulai dari awal"):
        st.session_state.root = None
        st.retrun()
