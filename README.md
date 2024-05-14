# ETS Integrasi Sistem

| Nama                            | NRP          |
| ------------------------------- | ------------ |
| Mohammad Arkananta Radithya     | `5027221003` |

# 1. Project memiliki ketentuan sebagai berikut:

    • Memiliki fitur Create, Read, Update, Delete data

    • Koneksi ke database (MongoDB atau yang lainnya)

    • Backend CRUD ke database

    • Mengimplementasikan UI

# 2. Cara menjalankan Project

Jalankan line dibawah pada terminal
```
python -m grpc_tools.protoc --proto_path=protobuf --python_out=backend --grpc_python_out=backend protobuf/tickets.proto  
```

Setelah itu jalankan file server.py sebagai backend yang akan berhubungan dengan database yang digunakan
```
python ./server.py
```

Langkah berikutnya Jalankan app.py yang berfungsi untuk menghubungkan antara backend dengan frontend yang digunakan
```
python ./app.py
```
