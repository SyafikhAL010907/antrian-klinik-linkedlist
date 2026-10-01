# ============================================================
# TUGAS 3 - STRUKTUR DATA: SINGLE LINKED LIST (CUSTOMTKINTER GUI)
# STUDI KASUS  : SISTEM ANTRIAN KLINIK
# NAMA         : Maulana Syafikh Alkhudri
# NIM          : 1512625004
# KELAS        : B
# ============================================================

from tkinter import messagebox
import customtkinter as ctk  # type: ignore

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# ============================================================
# 1. STRUKTUR DATA: NODE & SINGLE LINKED LIST
# ============================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class KlinikQueue:
    def __init__(self):
        self.head = None

    # 1. INSERT DI AWAL (Prioritas / Emergency / Lansia)
    def insert_di_awal(self, data):
        baru = Node(data)
        baru.next = self.head
        self.head = baru

    # 2. INSERT DI AKHIR (Pasien Umum / Reguler)
    def insert_di_akhir(self, data):
        baru = Node(data)
        if self.head is None:
            self.head = baru
            return
        
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = baru

    # 3. HAPUS HEAD (Pasien Dipanggil Masuk Ruang Dokter)
    def hapus_head(self):
        if self.head is None:
            return None
        
        hapus = self.head
        self.head = self.head.next
        nama = hapus.data
        hapus.next = None
        return nama

    # 4. HAPUS TAIL (Menghapus Pasien Paling Belakang)
    def hapus_tail(self):
        if self.head is None:
            return None
        
        if self.head.next is None:
            nama = self.head.data
            self.head = None
            return nama
        
        current = self.head
        while current.next.next is not None:
            current = current.next
        
        nama = current.next.data
        current.next = None
        return nama

    # 5. HAPUS BY VALUE (Pasien Batal Periksa)
    def hapus_by_value(self, target_nama):
        if self.head is None:
            return False

        if target_nama.lower() in self.head.data.lower():
            self.hapus_head()
            return True

        current = self.head
        while current.next is not None and target_nama.lower() not in current.next.data.lower():
            current = current.next

        if current.next is None:
            return False

        hapus = current.next
        current.next = hapus.next
        hapus.next = None
        return True

    # 6. LIHAT DEPAN (Peek)
    def lihat_depan(self):
        if self.head is None:
            return None
        return self.head.data

    # 7. HITUNG PANJANG
    def hitung_panjang(self):
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count

    # HELPER: Representasi Format Visual Chain
    def get_chain_string(self):
        if self.head is None:
            return "Antrian Kosong (None)"
        
        chain = []
        current = self.head
        while current is not None:
            chain.append(f"[{current.data}]")
            current = current.next
        chain.append("None")
        return " ➜ ".join(chain)

    def to_list(self):
        items = []
        current = self.head
        while current is not None:
            items.append(current.data)
            current = current.next
        return items


# ============================================================
# 2. GUI DENGAN CUSTOMTKINTER
# ============================================================

class AplikasiKlinikModern(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Antrian Klinik — Single Linked List")
        self.geometry("1100x680")
        self.minsize(980, 620)

        self.COLOR_BG_WINDOW = "#F1F5F9"
        self.COLOR_CARD_BG   = "#FFFFFF"
        self.COLOR_HEADER    = "#0284C7"
        self.COLOR_TEAL      = "#0D9488"
        self.COLOR_TEAL_HOV  = "#0F766E"
        self.COLOR_ORANGE    = "#EA580C"
        self.COLOR_ORNG_HOV  = "#C2410C"
        self.COLOR_GREEN     = "#16A34A"
        self.COLOR_GRN_HOV   = "#15803D"
        self.COLOR_RED       = "#DC2626"
        self.COLOR_RED_HOV   = "#B91C1C"
        self.COLOR_BLUE_INFO = "#2563EB"
        self.COLOR_BLUE_HOV  = "#1D4ED8"
        self.COLOR_TEXT_MAIN = "#0F172A"
        self.COLOR_TEXT_MUT  = "#64748B"

        self.configure(fg_color=self.COLOR_BG_WINDOW)

        self.queue = KlinikQueue()

        self._setup_layout()
        self._update_monitor()

    # Layout Utama: Header + Grid Konten
    def _setup_layout(self):
        # Header Bar
        header_frame = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_HEADER,
            corner_radius=16,
            height=78
        )
        header_frame.pack(fill="x", padx=16, pady=(14, 10))
        header_frame.pack_propagate(False)

        lbl_title = ctk.CTkLabel(
            header_frame,
            text="🏥 SISTEM MANAJEMEN ANTRIAN KLINIK",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#FFFFFF"
        )
        lbl_title.pack(anchor="w", padx=22, pady=(12, 0))

        lbl_subtitle = ctk.CTkLabel(
            header_frame,
            text="Simulasi Single Linked List  ·  Maulana Syafikh Alkhudri  ·  NIM: 1512625004  ·  Kelas: B",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#E0F2FE"
        )
        lbl_subtitle.pack(anchor="w", padx=22, pady=(0, 10))

        # Kontainer Konten
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        content_frame.grid_columnconfigure(0, weight=0)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        self._build_panel_kontrol(content_frame)
        self._build_panel_monitor(content_frame)

    # Panel Kiri: Input Data & Tombol Operasi
    def _build_panel_kontrol(self, parent):
        panel_kiri = ctk.CTkFrame(
            parent,
            fg_color=self.COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color="#E2E8F0",
            width=360
        )
        panel_kiri.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        panel_kiri.pack_propagate(False)

        # Input Nama Pasien
        lbl_section_input = ctk.CTkLabel(
            panel_kiri,
            text="PENDAFTARAN PASIEN",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.COLOR_HEADER
        )
        lbl_section_input.pack(anchor="w", padx=18, pady=(16, 4))

        self.entry_nama = ctk.CTkEntry(
            panel_kiri,
            placeholder_text="Ketik nama pasien di sini...",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            corner_radius=10,
            height=40,
            border_width=1.5,
            border_color="#CBD5E1",
            fg_color="#F8FAFC",
            text_color=self.COLOR_TEXT_MAIN
        )
        self.entry_nama.pack(fill="x", padx=18, pady=(4, 6))
        self.entry_nama.bind("<Return>", lambda e: self._aksi_insert_akhir())

        lbl_hint = ctk.CTkLabel(
            panel_kiri,
            text="Tekan Enter untuk mendaftarkan pasien reguler.",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=self.COLOR_TEXT_MUT
        )
        lbl_hint.pack(anchor="w", padx=18, pady=(0, 12))

        # Tombol Tambah Antrian
        btn_umum = ctk.CTkButton(
            panel_kiri,
            text="➕  Insert Akhir (Pasien Umum)",
            command=self._aksi_insert_akhir,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=self.COLOR_TEAL,
            hover_color=self.COLOR_TEAL_HOV,
            corner_radius=10,
            height=38
        )
        btn_umum.pack(fill="x", padx=18, pady=4)

        btn_prioritas = ctk.CTkButton(
            panel_kiri,
            text="⚡  Insert Awal (Prioritas / Lansia)",
            command=self._aksi_insert_awal,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=self.COLOR_ORANGE,
            hover_color=self.COLOR_ORNG_HOV,
            corner_radius=10,
            height=38
        )
        btn_prioritas.pack(fill="x", padx=18, pady=4)

        sep1 = ctk.CTkFrame(panel_kiri, height=1, fg_color="#E2E8F0")
        sep1.pack(fill="x", padx=18, pady=12)

        # Tombol Pemanggilan & Hapus
        lbl_section_ops = ctk.CTkLabel(
            panel_kiri,
            text="PENGELOLAAN ANTRIAN",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.COLOR_HEADER
        )
        lbl_section_ops.pack(anchor="w", padx=18, pady=(0, 6))

        btn_panggil = ctk.CTkButton(
            panel_kiri,
            text="📢  Panggil Pasien (Hapus Head)",
            command=self._aksi_hapus_head,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=self.COLOR_GREEN,
            hover_color=self.COLOR_GRN_HOV,
            corner_radius=10,
            height=38
        )
        btn_panggil.pack(fill="x", padx=18, pady=4)

        btn_batal = ctk.CTkButton(
            panel_kiri,
            text="❌  Pasien Batal (Hapus by Value)",
            command=self._aksi_hapus_value,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=self.COLOR_RED,
            hover_color=self.COLOR_RED_HOV,
            corner_radius=10,
            height=38
        )
        btn_batal.pack(fill="x", padx=18, pady=4)

        btn_tail = ctk.CTkButton(
            panel_kiri,
            text="🗑️  Hapus Belakang (Hapus Tail)",
            command=self._aksi_hapus_tail,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#B91C1C",
            hover_color="#991B1B",
            corner_radius=10,
            height=36
        )
        btn_tail.pack(fill="x", padx=18, pady=4)

        sep2 = ctk.CTkFrame(panel_kiri, height=1, fg_color="#E2E8F0")
        sep2.pack(fill="x", padx=18, pady=10)

        # Tombol Informasi & Query
        lbl_section_info = ctk.CTkLabel(
            panel_kiri,
            text="INFORMASI LINKED LIST",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.COLOR_HEADER
        )
        lbl_section_info.pack(anchor="w", padx=18, pady=(0, 6))

        grid_info = ctk.CTkFrame(panel_kiri, fg_color="transparent")
        grid_info.pack(fill="x", padx=18, pady=2)
        grid_info.grid_columnconfigure((0, 1), weight=1)

        btn_peek = ctk.CTkButton(
            grid_info,
            text="👁️ Lihat Depan",
            command=self._aksi_lihat_depan,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=self.COLOR_BLUE_INFO,
            hover_color=self.COLOR_BLUE_HOV,
            corner_radius=8,
            height=34
        )
        btn_peek.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        btn_hitung = ctk.CTkButton(
            grid_info,
            text="📊 Hitung Total",
            command=self._aksi_hitung_panjang,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=self.COLOR_BLUE_INFO,
            hover_color=self.COLOR_BLUE_HOV,
            corner_radius=8,
            height=34
        )
        btn_hitung.grid(row=0, column=1, padx=(4, 0), sticky="ew")

    # Panel Kanan: Monitor Visualisasi Antrian & Riwayat Aktivitas
    def _build_panel_monitor(self, parent):
        panel_kanan = ctk.CTkFrame(
            parent,
            fg_color=self.COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color="#E2E8F0"
        )
        panel_kanan.grid(row=0, column=1, sticky="nsew")

        # Header Monitor
        monitor_top = ctk.CTkFrame(panel_kanan, fg_color="transparent", height=46)
        monitor_top.pack(fill="x", padx=20, pady=(16, 6))

        lbl_mon_title = ctk.CTkLabel(
            monitor_top,
            text="MONITOR ANTRIAN PASIEN REAL-TIME",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.COLOR_TEXT_MAIN
        )
        lbl_mon_title.pack(side="left")

        self.badge_status = ctk.CTkLabel(
            monitor_top,
            text="  0 PASIEN AKTIF  ",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#FFFFFF",
            fg_color="#64748B",
            corner_radius=12,
            padx=10,
            pady=3
        )
        self.badge_status.pack(side="right")

        # Visualisasi Kartu Pasien (Horizontal Scroll)
        lbl_sub_cards = ctk.CTkLabel(
            panel_kanan,
            text="Visual Urutan Node Antrian (Kiri: Head ➜ Kanan: Tail):",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.COLOR_TEXT_MUT
        )
        lbl_sub_cards.pack(anchor="w", padx=20, pady=(4, 6))

        self.cards_container = ctk.CTkScrollableFrame(
            panel_kanan,
            fg_color="#F8FAFC",
            corner_radius=14,
            border_width=1,
            border_color="#E2E8F0",
            orientation="horizontal",
            height=110
        )
        self.cards_container.pack(fill="x", padx=20, pady=(0, 10))

        # Layar Rantai Single Linked List
        lbl_chain = ctk.CTkLabel(
            panel_kanan,
            text="Representasi Struktur Data Single Linked List:",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.COLOR_TEXT_MUT
        )
        lbl_chain.pack(anchor="w", padx=20, pady=(6, 4))

        chain_box = ctk.CTkFrame(
            panel_kanan,
            fg_color="#0F172A",
            corner_radius=12,
            border_width=1,
            border_color="#1E293B"
        )
        chain_box.pack(fill="x", padx=20, pady=(0, 12))

        self.lbl_chain_display = ctk.CTkLabel(
            chain_box,
            text="Antrian Kosong (None)",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color="#38BDF8",
            wraplength=640,
            justify="left",
            padx=14,
            pady=12
        )
        self.lbl_chain_display.pack(fill="x")

        # Riwayat Aktivitas
        lbl_log = ctk.CTkLabel(
            panel_kanan,
            text="Riwayat Aktivitas Antrian:",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.COLOR_TEXT_MUT
        )
        lbl_log.pack(anchor="w", padx=20, pady=(0, 4))

        self.log_textbox = ctk.CTkTextbox(
            panel_kanan,
            fg_color="#F8FAFC",
            border_width=1,
            border_color="#E2E8F0",
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=self.COLOR_TEXT_MAIN
        )
        self.log_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        self.log_textbox.configure(state="disabled")

    # ============================================================
    # 3. HANDLER AKSI TOMBOL & LOGIKA LINKED LIST
    # ============================================================

    def _get_input(self):
        nama = self.entry_nama.get().strip()
        if not nama:
            messagebox.showwarning(
                "Input Kosong",
                "Silakan masukkan nama pasien terlebih dahulu di kolom pendaftaran!"
            )
            self.entry_nama.focus()
            return None
        return nama

    def _reset_input(self):
        self.entry_nama.delete(0, "end")
        self.entry_nama.focus()

    def _log(self, pesan):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"• {pesan}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    # Operasi 1: Insert di Akhir (Pasien Umum)
    def _aksi_insert_akhir(self):
        nama = self._get_input()
        if nama is None:
            return
        
        data_pasien = f"{nama} (Umum)"
        self.queue.insert_di_akhir(data_pasien)
        self._log(f"[+] Umum      : Pasien '{data_pasien}' masuk di antrian belakang (tail).")
        self._reset_input()
        self._update_monitor()

    # Operasi 2: Insert di Awal (Pasien Prioritas)
    def _aksi_insert_awal(self):
        nama = self._get_input()
        if nama is None:
            return
        
        data_pasien = f"{nama} (Prioritas)"
        self.queue.insert_di_awal(data_pasien)
        self._log(f"[+] Prioritas : Pasien '{data_pasien}' masuk di antrian paling DEPAN (head).")
        self._reset_input()
        self._update_monitor()

    # Operasi 3: Hapus Head (Panggil Pasien Masuk Ruang Dokter)
    def _aksi_hapus_head(self):
        data = self.queue.hapus_head()
        if data is None:
            messagebox.showinfo(
                "Antrian Kosong",
                "Tidak ada pasien yang mengantri. Antrian saat ini kosong."
            )
            return
        
        messagebox.showinfo(
            "Panggilan Pasien",
            f"📢 Panggilan untuk:\n\n{data}\n\nSilakan segera masuk ke Ruang Pemeriksaan Dokter."
        )
        self._log(f"[-] Dipanggil : '{data}' keluar antrian dan masuk ruang dokter.")
        self._update_monitor()

    # Operasi 4: Hapus Tail (Hapus Pasien Paling Belakang)
    def _aksi_hapus_tail(self):
        data = self.queue.hapus_tail()
        if data is None:
            messagebox.showwarning(
                "Antrian Kosong",
                "Gagal menghapus! Antrian sudah kosong."
            )
            return
        
        messagebox.showinfo(
            "Hapus Belakang",
            f"Pasien terakhir '{data}' telah dikeluarkan dari antrian."
        )
        self._log(f"[-] Tail Hapus: Pasien terakhir '{data}' dikeluarkan dari antrian.")
        self._update_monitor()

    # Operasi 5: Hapus by Value (Pasien Batal Periksa)
    def _aksi_hapus_value(self):
        nama = self._get_input()
        if nama is None:
            return
        
        berhasil = self.queue.hapus_by_value(nama)
        if berhasil:
            messagebox.showinfo(
                "Pasien Dibatalkan",
                f"Pasien dengan nama '{nama}' berhasil dibatalkan dan dihapus dari antrian."
            )
            self._log(f"[-] Batal     : Pasien '{nama}' membatalkan periksa dan dihapus dari antrian.")
            self._reset_input()
            self._update_monitor()
        else:
            messagebox.showerror(
                "Tidak Ditemukan",
                f"Pasien dengan nama '{nama}' tidak ditemukan dalam daftar antrian aktif!"
            )

    # Operasi 6: Lihat Depan (Peek)
    def _aksi_lihat_depan(self):
        data = self.queue.lihat_depan()
        if data is None:
            messagebox.showinfo(
                "Status Antrian",
                "Antrian saat ini sedang KOSONG."
            )
            return
        
        messagebox.showinfo(
            "Pasien Terdepan (Head)",
            f"Pasien urutan terdepan yang akan dipanggil berikutnya adalah:\n\n👤  {data}"
        )
        self._log(f"[i] Peek      : Pasien terdepan saat ini adalah '{data}'.")

    # Operasi 7: Hitung Panjang Antrian
    def _aksi_hitung_panjang(self):
        total = self.queue.hitung_panjang()
        messagebox.showinfo(
            "Total Pasien",
            f"Jumlah pasien yang sedang berada dalam antrian:\n\n📊  {total} Orang"
        )
        self._log(f"[i] Hitung    : Total antrian saat ini = {total} orang.")

    # ============================================================
    # 4. PEMBARUAN TAMPILAN MONITOR & KARTU NODE REAL-TIME
    # ============================================================

    def _update_monitor(self):
        pasien_list = self.queue.to_list()
        total = len(pasien_list)

        # Status Badge
        if total == 0:
            self.badge_status.configure(
                text="  ANTRIAN KOSONG  ",
                fg_color="#64748B"
            )
        else:
            self.badge_status.configure(
                text=f"  {total} PASIEN AKTIF  ",
                fg_color=self.COLOR_GREEN
            )

        # Teks Rantai Linked List
        self.lbl_chain_display.configure(text=self.queue.get_chain_string())

        # Render Kartu Node
        for widget in self.cards_container.winfo_children():
            widget.destroy()

        if total == 0:
            lbl_empty = ctk.CTkLabel(
                self.cards_container,
                text="Belum ada pasien dalam antrian. Silakan daftarkan pasien di panel kiri.",
                font=ctk.CTkFont(family="Segoe UI", size=12, slant="italic"),
                text_color=self.COLOR_TEXT_MUT
            )
            lbl_empty.pack(padx=20, pady=26)
            return

        for idx, nama_pasien in enumerate(pasien_list):
            is_head = (idx == 0)
            is_prioritas = "Prioritas" in nama_pasien

            card_color = "#FEF2F2" if is_prioritas else ("#F0FDF4" if is_head else "#FFFFFF")
            border_color = self.COLOR_ORANGE if is_prioritas else (self.COLOR_GREEN if is_head else "#CBD5E1")

            card = ctk.CTkFrame(
                self.cards_container,
                fg_color=card_color,
                corner_radius=12,
                border_width=1.5,
                border_color=border_color,
                height=72
            )
            card.pack(side="left", padx=4, pady=8)

            badge_text = "HEAD (Urutan 1)" if is_head else f"Urutan #{idx + 1}"
            badge_bg = self.COLOR_GREEN if is_head else "#E2E8F0"
            badge_fg = "#FFFFFF" if is_head else "#475569"

            lbl_badge = ctk.CTkLabel(
                card,
                text=f" {badge_text} ",
                font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
                fg_color=badge_bg,
                text_color=badge_fg,
                corner_radius=6
            )
            lbl_badge.pack(anchor="w", padx=10, pady=(6, 2))

            lbl_nama = ctk.CTkLabel(
                card,
                text=nama_pasien,
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                text_color=self.COLOR_TEXT_MAIN
            )
            lbl_nama.pack(anchor="w", padx=10, pady=(0, 8))

            if idx < total - 1:
                lbl_panah = ctk.CTkLabel(
                    self.cards_container,
                    text="➔",
                    font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                    text_color="#94A3B8"
                )
                lbl_panah.pack(side="left", padx=2)

        lbl_panah_none = ctk.CTkLabel(
            self.cards_container,
            text="➔",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#94A3B8"
        )
        lbl_panah_none.pack(side="left", padx=2)

        lbl_none = ctk.CTkLabel(
            self.cards_container,
            text=" None ",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold", slant="italic"),
            fg_color="#E2E8F0",
            text_color="#64748B",
            corner_radius=8,
            padx=8,
            pady=4
        )
        lbl_none.pack(side="left", padx=4)


# ============================================================
# 5. ENTRY POINT APLIKASI
# ============================================================
if __name__ == "__main__":
    app = AplikasiKlinikModern()
    app.mainloop()
