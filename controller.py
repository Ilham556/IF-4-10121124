import streamlit as st
import re
# controller.py
from model import AppModel
from view import AppView
class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.jabatan_data = self.model.jabatan_data
        self.pegawai_data = self.model.pegawai_data
        self.pegawai_jabatan_data = self.model.pegawai_jabatan_data
        self.admin_data = self.model.admin_data
        self.natural_join = self.model.natural_join
    
    def pie(self, df):
        return self.view.pie(df)

    def line(self, df):
        return self.view.line(df)
    
    def table_admin(self,df,status):
        return self.view.table_admin(df,status)

    
    def login_validation(self,login_email, login_password):
        return self.model.login(login_email, login_password)
    
    def update_myuser(self, username, password, updated_at, ids):
        if any(value == "" for value in (username, password, updated_at, ids)):
            st.warning('All fields must be filled')
        else:
            self.model.update_myuser(username, password, updated_at, ids)
            st.experimental_rerun()
    
    #Crud Admin

    def createdata_admin(self, username, password,):
        if any(value == "" for value in (username, password)):
            st.warning('All fields must be filled')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", username):
            st.warning('Invalid email address')
        else:
            self.model.create_admin(username, password,)
            st.experimental_rerun()
    
    def updatedata_admin(self,ids, username, password):
        if any(value == "" for value in (username, password)):
            st.warning('All fields must be filled')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", username):
            st.warning('Invalid email address')
        else:
            self.model.update_admin(ids, username, password)
            st.experimental_rerun()
        
    def deletedata_admin(self,ids):
        self.model.delete_admin(ids)
        st.experimental_rerun()

    #crud Pegawai
    
    def createdata_pegawai(self, nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id):
        if any(value == "" for value in (nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id)):
            st.warning('All fields must be filled')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.warning('Invalid email address')
        else:
            self.model.create_pegawai(nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id)
            st.experimental_rerun() 
    
    def updatedata_pegawai(self,ids, nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id):
        if any(value == "" for value in (ids, nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id)):
            st.warning('All fields must be filled')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.warning('Invalid email address')
        else:
            self.model.update_pegawai(ids, nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id)
            st.experimental_rerun()
    
    def deletedata_pegawai(self,ids):
        
        self.model.delete_pegawai(ids)
        st.experimental_rerun()
    
    #crud Jabatan
    def createdata_jabatan(self, nama_jabatan, deskripsi, gaji):
        if any(value == "" for value in (nama_jabatan, deskripsi, gaji)):
            st.warning('All fields must be filled')
        else:
            self.model.create_jabatan(nama_jabatan, deskripsi, gaji)
            st.experimental_rerun() 
    
    def updatedata_jabatan(self,ids, nama_jabatan, deskripsi, gaji):
        if any(value == "" for value in (ids, nama_jabatan, deskripsi, gaji)):
            st.warning('All fields must be filled')
        else:
            self.model.update_jabatan(ids, nama_jabatan, deskripsi, gaji)
            st.experimental_rerun() 
    
    def deletedata_jabatan(self,ids):
        self.model.delete_jabatan(ids)
        st.experimental_rerun()
    
    #crud Pegawai per Jabatan
    
    def createdata_pegawaiperjabatan(self, id_pegawai, id_jabatan):
        if any(value == "" for value in (id_pegawai, id_jabatan)):
            st.warning('All fields must be filled')
        else:
            self.model.create_pegawaiperjabatan(id_pegawai, id_jabatan)
            st.experimental_rerun()
        
    def updatedata_pegawaiperjabatan(self, ids, id_pegawai, id_jabatan):
        
        if any(value == "" for value in (ids, id_pegawai, id_jabatan)):
            st.warning('All fields must be filled')
        else:
            self.model.update_pegawaiperjabatan(ids, numbers_only, id_jabatan)
            st.experimental_rerun()

    def deletedata_pegawaiperjabatan(self,ids):

        self.model.delete_pegawaiperjabatan(ids)
        st.experimental_rerun()
    
