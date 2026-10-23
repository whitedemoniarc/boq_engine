from calculation.rebar import Rebar
from calculation.stirrup import Stirrup
from calculation.main_rebar import MainRebar


class Beam:

    def __init__(
        self,
        name,       # Nama balok, contoh: "B1"
        width,      # Lebar balok dalam mm
        height,     # Tinggi balok dalam mm
        length,     # Panjang balok dalam mm
        #cover       # Tebal selimut beton / concrete cover (mm)
        parameters  # Objek DesignParameters    
    ):

        self.name = name        # Nama balok, contoh: "B1"
        self.width = width      # Lebar balok dalam mm              
        self.height = height    # Tinggi balok dalam mm
        self.length = length    # Panjang balok dalam mm
        # self.cover = cover      # Tebal selimut beton / concrete cover (mm)

        self.main_rebars = []   # Tempat penampungan kosong untuk daftar besi utama (main rebar)
        self.rebars = []        # Tempat penampungan kosong untuk daftar besi
        self.stirrups = []      # Tempat penampungan kosong untuk daftar besi stirrup

        self.parameters = parameters       # Mengambil properti concrete dari objek DesignParameters

    # Memasukkan Besi Baru
    def add_rebar( 
        self,
        mark,
        diameter,
        quantity,
        length,
        position
    ):
        rebar = Rebar(
            mark=mark,                  # Kode tanda besi (misal: "T1", "B1")
            diameter=diameter,          # Diameter besi (misal: "D10", "D13", "D19")
            quantity=quantity,          # Jumlah batang besi
            length=length,              # Panjang batang besi (m)
            position=position           # Posisi besi (misal: "Atas", "Bawah", "Kiri", "Kanan")
        )

        self.rebars.append(rebar)       # Menambahkan objek Rebar yang baru dibuat ke dalam daftar self.rebars

    # Memasukkan Besi Utama Baru
    def add_main_rebar(
        self,
        mark,
        b_lebar_mm,
        h_tinggi_mm,
        diameter,
        quantity,
        # anchorage_left,
        # anchorage_right,
        # position
        anchorage_left=0,
        anchorage_right=0,
        position="BOTTOM",
    ):

        rebar = MainRebar(
        mark=mark,
        b_lebar_mm=b_lebar_mm,
        h_tinggi_mm=h_tinggi_mm,
        diameter=diameter,
        quantity=quantity,
        beam_length=self.length,
        anchorage_left=anchorage_left,
        anchorage_right=anchorage_right,
        position=position
    )

        self.main_rebars.append(rebar)
        return rebar

    # Memasukkan Besi Stirrup Baru
    def add_stirrup(
        self,
        mark,
        diameter,
        spacing
    ):
        stirrup = Stirrup(
            mark=mark,                  # Kode tanda besi (misal: "ST1", "ST2")
            diameter=diameter,          # Diameter besi stirrup (misal: "D10", "D13", "D19")
            spacing=spacing,            # Jarak antar stirrup (mm)
            beam_width=self.width,      # Lebar balok (mm)
            beam_height=self.height,    # Tinggi balok (mm)
            beam_length=self.length,    # Panjang balok (mm)
            cover=self.cover            # Jarak pelindung besi (mm)
        )

        self.stirrups.append(stirrup)   # Menambahkan objek Stirrup yang baru dibuat ke dalam daftar self.stirrups

    # Menghitung Berat Total Besi
    #    @property                           # Menandai bahwa metode ini adalah properti dari kelas Beam, sehingga dapat diakses seperti atribut biasa (tanpa tanda kurung)
    #    def total_rebar_weight(self):       # Menghitung berat total besi yang ada di dalam balok
    #        return sum(                     # Menggunakan fungsi sum() untuk menjumlahkan berat total besi dari setiap objek Rebar yang ada di dalam daftar self.rebars
    #            rebar.total_weight          # Mengambil properti total_weight dari setiap objek Rebar yang ada di dalam daftar self.rebars
    #            for rebar in self.rebars    # Melakukan iterasi untuk setiap objek Rebar yang ada di dalam daftar self.rebars
    #        )

    # Membuat Tabel Laporan Pembesian
    #    def rebar_schedule(self):

    #        schedule = []               # Membuat list kosong untuk menampung data schedule pembesian

    #        for rebar in self.rebars:   # Melakukan iterasi untuk setiap besi yang ada di dalam daftar rebars

    #                "mark": rebar.mark,             # Kode tanda besi (misal: "T1", "B1")
    #                "position": rebar.position,     # Posisi besi (misal: "Atas", "Bawah", "Kiri", "Kanan")
    #                "diameter": rebar.diameter,     # Diameter besi (misal: "D10", "D13", "D19")
    #                "quantity": rebar.quantity,     # Jumlah batang besi
    #                "length": rebar.length,         # Panjang batang besi (m)
    #                "total_length": rebar.total_length, # Total panjang besi (m)
    #                "weight": rebar.total_weight    # Berat total besi tersebut dalam kg (diambil otomatis dari properti kelas Rebar)
    #           })

    #        return schedule         # Mengembalikan daftar schedule pembesian dalam bentuk list of dictionaries

    @property
    def cover(self):
        return self.parameters.beam_cover

    @property
    def total_rebar_weight(self):

        main_weight = sum(
            rebar.total_weight
            for rebar in self.rebars
        )

        longitudinal_weight = sum(
            rebar.total_weight
            for rebar in self.main_rebars
        )

        stirrup_weight = sum(
            stirrup.total_weight
            for stirrup in self.stirrups
        )

        return (
            main_weight
            + longitudinal_weight
            + stirrup_weight
        )
