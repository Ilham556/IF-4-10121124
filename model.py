import streamlit as st
import pandas as pd
import mysql.connector

class AppModel:
    def __init__(self):
        self.mydb = mysql.connector.connect(
                port='3306',
                user='root',
                #password=db_secrets["password"],
                host='localhost',
                database='db_pegawai'
            )
        self.query_jabatan_data = "SELECT * FROM jabatan"
        self.jabatan_data = pd.read_sql(self.query_jabatan_data, self.mydb)
        self.query_pegawai_data = "SELECT * FROM pegawai"
        self.pegawai_data = pd.read_sql(self.query_pegawai_data, self.mydb)
        self.query_pegawai_jabatan_data = "SELECT * FROM pegawai_jabatan"
        self.pegawai_jabatan_data = pd.read_sql(self.query_pegawai_jabatan_data, self.mydb)
        self.query_admin_data = "SELECT * FROM admin"
        self.admin_data = pd.read_sql(self.query_admin_data, self.mydb)
        self.query_naturaljoin = """
            SELECT pegawai_jabatan.id as id,pegawai.id AS pegawai_id, pegawai.nama AS pegawai_nama, jabatan.id AS jabatan_id, jabatan.nama_jabatan, jabatan.deskripsi as deskripsi, pegawai_jabatan.created_at as created
            FROM pegawai
            JOIN pegawai_jabatan ON pegawai.id = pegawai_jabatan.id_pegawai
            JOIN jabatan ON jabatan.id = pegawai_jabatan.id_jabatan;
        """
        self.natural_join = pd.read_sql(self.query_naturaljoin, self.mydb)

    def natural_join(self):
        
        return pd.read_sql(query, self.mydb)

    def login(self, username, password):
        try:
            cursor = self.mydb.cursor(buffered=True)
            query = "SELECT * FROM admin WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, password))
            self.mydb.commit()
            result = cursor.fetchone()
            

            if result:
                
                # If login is successful, return the user information
                user_info = {
                    'id': result[0],
                    'username': result[1],
                    'password': result[2],
                }
                return 'berhasil', user_info
            else:

                return "gagal", {}
        except Exception as e:
            st.error(f'Error: {e}')
    
    def update_myuser(self, username, password, updated_at, id):
        try:
            cursor = self.mydb.cursor()
            query = "UPDATE admin SET username = %s, password_hash = %s, updated_at = %s WHERE id = %s"
            cursor.execute(query, (username, password, updated_at, id))
            self.mydb.commit()
            self.query = "SELECT * FROM admin"
            self.df_user = pd.read_sql(self.query, self.mydb)
            st.info('Data Successfully Added, log in again to see the changes.') 
            
        except Exception as e:
            st.error(f'Error: {e}')
        return self.df_user
    
    #crud admin

    def create_admin(self, username, password):
        try:
            cursor = self.mydb.cursor()
            # Contoh memanggil stored procedure tambah_admin
            cursor.callproc('tambah_admin', (username, password))

            # Commit perubahan ke database
            self.mydb.commit()

            st.info("Admin ditambahkan sukses!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
    
    def update_admin(self,ids, username, password):
        try:
            cursor = self.mydb.cursor()
            # Contoh memanggil stored procedure tambah_admin
            cursor.callproc('edit_admin', (ids, username, password))

            # Commit perubahan ke database
            self.mydb.commit()

            st.info("Admin diupdate sukses!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()

    def delete_admin(self,ids):
        try:
            with self.mydb.cursor() as cursor:
                if len(ids) > 1:
                    for data in ids:
                        cursor.callproc('hapus_admin', (data,))

                else:
                    cursor.callproc('hapus_admin', (ids))

                # Commit perubahan ke database
                self.mydb.commit()

            st.info("Admin dihapus sukses!")

        except mysql.connector.Error as err:
            st.error(f"Database Error: {err}")

        finally:
            cursor.close()
       
    #crud pegawai
    
    def create_pegawai(self, nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id):
        try:
            cursor = self.mydb.cursor()
            # Contoh memanggil stored procedure tambah_admin
            cursor.callproc('tambah_pegawai', (nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id))

            # Commit perubahan ke database
            self.mydb.commit()

            st.info("Pegawai ditambahkan sukses!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
    
    def update_pegawai(self, ids, nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id):
        try:
            cursor = self.mydb.cursor()
            # Contoh memanggil stored procedure tambah_admin
            cursor.callproc('edit_pegawai', (ids, nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id))

            # Commit perubahan ke database
            self.mydb.commit()

            st.info("Pegawai diupdate sukses!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
    
    def delete_pegawai(self,ids):       
        try:
            with self.mydb.cursor() as cursor:
                if len(ids) > 1:
                    for data in ids:
                        cursor.callproc('hapus_pegawai', (data,))

                else:
                    cursor.callproc('hapus_pegawai', (ids))

                # Commit perubahan ke database
                self.mydb.commit()

            st.info("Pegawai dihapus sukses!")

        except mysql.connector.Error as err:
            st.error(f"Database Error: {err}")

        finally:
            cursor.close()
    
    #crud jabatan
    
    def create_jabatan(self, nama_jabatan, deskripsi, gaji):
        try:
            cursor = self.mydb.cursor()
            # Contoh memanggil stored procedure tambah_admin
            cursor.callproc('tambah_jabatan', (nama_jabatan, deskripsi, gaji))

            # Commit perubahan ke database
            self.mydb.commit()

            st.info("Pegawai ditambahkan sukses!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
    
    def update_jabatan(self, ids, nama_jabatan, deskripsi, gaji):
        try:
            cursor = self.mydb.cursor()
            # Contoh memanggil stored procedure tambah_admin
            cursor.callproc('edit_jabatan', (ids, nama_jabatan, deskripsi, gaji))

            # Commit perubahan ke database
            self.mydb.commit()

            st.info("Jabatan diupdate sukses!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
    
    def delete_jabatan(self,ids):
        try:
            with self.mydb.cursor() as cursor:
                if len(ids) > 1:
                    for data in ids:
                        cursor.callproc('hapus_jabatan', (data,))

                else:
                    cursor.callproc('hapus_jabatan', (ids))

                # Commit perubahan ke database
                self.mydb.commit()

            st.info("Jabatan dihapus sukses!")

        except mysql.connector.Error as err:
            st.error(f"Database Error: {err}")

        finally:
            cursor.close()

    
    #crud Pegawai per Jabatan
    
    def create_pegawaiperjabatan(self, id_pegawai, id_jabatan):
        filter_id_pegawai = ''.join(filter(str.isdigit, str(id_pegawai)))
        filter_id_jabatan = ''.join(filter(str.isdigit, str(id_jabatan)))
        try:
            cursor = self.mydb.cursor()
            # Contoh memanggil stored procedure tambah_admin
            cursor.callproc('tambah_pegawai_jabatan', (filter_id_pegawai, filter_id_jabatan))

            # Commit perubahan ke database
            self.mydb.commit()

            st.info("Pegawai Jabatan ditambahkan sukses!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
    
    def update_pegawaiperjabatan(self, ids, id_pegawai, id_jabatan):
        try:
            cursor = self.mydb.cursor()
            # Contoh memanggil stored procedure tambah_admin
            cursor.callproc('edit_pegawai_jabatan', (ids, id_pegawai, id_jabatan))

            # Commit perubahan ke database
            self.mydb.commit()

            st.info("Pegawai Jabatan ditambahkan sukses!")
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
    
    def delete_pegawaiperjabatan(self, ids):
        try:
            with self.mydb.cursor() as cursor:
                if len(ids) > 1:
                    for data in ids:
                        cursor.callproc('hapus_pegawai_jabatan', (data,))

                else:
                    cursor.callproc('hapus_pegawai_jabatan', (ids))

                # Commit perubahan ke database
                self.mydb.commit()

            st.info("Pegawai Jabatan dihapus sukses!")

        except mysql.connector.Error as err:
            st.error(f"Database Error: {err}")

        finally:
            cursor.close()
