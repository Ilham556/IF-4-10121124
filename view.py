import streamlit as st
import hydralit_components as hc
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, AgGridTheme
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype
import datetime
from datetime import date, timedelta
from streamlit_option_menu import option_menu
import re
import plotly.express as px

class AppView:
    def __init__(self):
        st.set_page_config(page_title="Dashboard",layout='wide',page_icon="⚠️")
        #auth
        self.user_info = None
        self.login_username = None
        self.login_password = None
        #admin
        self.username_user = None
        self.password_user = None
        #pegawai
        self.nama_pegawai = None
        self.alamat_pegawai = None
        self.tanggal_lahir_pegawai = None
        self.jenis_kelamin_pegawai = None
        self.telepon_pegawai = None
        self.email_pegawai = None
        self.admin_id_pegawai = None
        #jabatan
        self.nama_jabatan = None
        self.deskripsi_jabatan= None
        self.gaji_jabatan = None
        #pegawaiperjabatan
        self.id_pegawai = None
        self.id_jabatan = None
        
    def hidetopbar(self):
        hide_streamlit_style ="""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        div.embeddedAppMetaInfoBar_container__DxxL1 {visibility: hidden;}
        </style>

        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    def css(self):
        css = """
        <style>
            .stButton>button {
                width: 100%;
                height: 50px;
                font-size: 20px;
            }
            div[data-testid="stToolbar"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
            }
            div[data-testid="stDecoration"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
            }
            div[data-testid="stStatusWidget"] {
            visibility: hidden;
            height: 0%;
            position: fixed;
            }
            #MainMenu {
            visibility: hidden;
            height: 0%;
            }
            header {
            visibility: hidden;
            height: 0%;
            }
            footer {
            visibility: hidden;
            height: 0%;
            }

        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def table_admin(self,df,status):
        # Konfigurasi GridOptionsBuilder
        if status == 'aktif':
            status = True
        elif status == 'tidak':
            status = False
        else:
            status = False
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(
            editable=False, filter=False, resizable=True, sortable=True, value=True, 
            enablePivot=True, enableValue=True, floatingFilter=True, aggFunc='sum', 
            flex=1, minWidth=150, width=150, maxWidth=200
        )
        gb.configure_selection(selection_mode='multiple', use_checkbox=status)
        gb.configure_pagination(enabled=True, paginationAutoPageSize=True)
        gridOptions = gb.build()

        # Konfigurasi Grid
        grid = AgGrid(
            df,
            gridOptions=gridOptions,
            data_return_mode=DataReturnMode.AS_INPUT,
            update_on='MANUAL',
            enable_quicksearch=True,
            fit_columns_on_grid_load=True,
            theme=AgGridTheme.STREAMLIT,
            enable_enterprise_modules=True,
            height=600,
            width='100%',
            custom_css={
                "#gridToolBar": {
                    "padding-bottom": "0px !important",
                }
            }
        )

        return grid
    def set_controller(self,controller):
        self.controller = controller
    def title(self,title):
        st.title(title)
    def header(self,header):
        st.header(header)
    
    
    def run(self):
            # Use the provided controller instance
            self.hidetopbar()
            self.css()
            
            if not st.session_state.get('login', False):
                self.loginview()
            else:
                login_status, user_info = st.session_state.login
                if login_status == 'berhasil':
                    self.route()
                    
                else:
                    st.write('tidak')

    def loginview(self):
            self.title('Login')
            self.login_username = ""
            self.login_password = ""

            st.session_state.login = ""
            st.session_state.user = ""
            with st.form("login_user",clear_on_submit=True):
                self.login_username = st.text_input('Masukan Email')
                self.login_password = st.text_input('Masukan Password', type='password')  # Use password input for sensitive information
                login_btn = st.form_submit_button('Login')

            if login_btn:
                if self.login_username == "" and self.login_password =="":
                    st.warning('Email and Password Cannot Be Empty')
                    st.session_state.login = ""
                    pass
                elif self.login_username == "" or self.login_password =="":
                    st.warning('Email or Password Is Empty')
                    st.session_state.login = ""
                    pass
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.login_username):
                    st.warning('Invalid email address')
                else:
                    st.session_state.login = self.controller.login_validation(self.login_username, self.login_password)
                    login_status, self.user_info = st.session_state.login
                    

                    if str(login_status) == 'berhasil':
                        # Clear the input fields after successful login
                        st.info(str(login_status))
                        
                        st.experimental_rerun()
                        return True
                    else:
                        st.session_state.login = ''
                        st.warning('Email or Password Is Wrong')

    def route(self):
        login_status, self.user_info = st.session_state.login
        with st.sidebar:
            st.subheader(f'Hallo _Selamat Datang_ :blue[Kembali] {self.user_info["username"]} :sunglasses:')
            selected = option_menu("Dashboard", ["Dashboard","Pegawai","Jabatan", "Pegawai per Jabatan",'Admin','Pengaturan'], 
                icons=['house','bi bi-person-lines-fill','bi bi-briefcase', 'list-task','bi bi-person-workspace', 'gear'], menu_icon="bi bi-database", default_index=0)
            #st.write(selected)
        if selected == "Dashboard":
            self.dashboardadminview()
           
        elif selected == "Pegawai":
            self.pegawaiview(self.user_info)
          
        elif selected == "Jabatan":
            self.jabatanview()
          
        elif selected == "Pegawai per Jabatan":
            self.pegawaiperjabatanview()

        elif selected == "Admin":
            self.adminview()

        elif selected == "Pengaturan":
            self.pengaturanview()
    def pie(self, df):
        employee_count = df.groupby('nama_jabatan')['pegawai_id'].count().reset_index()
        fig = px.pie(employee_count, names='nama_jabatan', values='pegawai_id', 
                 title='Distribution of Employees Across Job Positions',
                 labels={'nama_jabatan': 'Job Position', 'pegawai_id': 'Number of Employees'})
        st.plotly_chart(fig, use_container_width=True)

    def line(self, df):
        df['created_at'] = pd.to_datetime(df['created_at'])
        # Calculate the cumulative sum of the number of employees
        df['cumulative_employees'] = df.groupby('created_at')['id'].cumsum()

        # Create a line chart to show the increase in the number of employees over time
        fig = px.line(df, x='created_at', y='cumulative_employees', 
                    title='Cumulative Increase in Number of Employees Over Time',
                    labels={'created': 'Date', 'cumulative_employees': 'Cumulative Number of Employees'})
        st.plotly_chart(fig, use_container_width=True)
    

    
    def dashboardadminview(self):
        col1,col2,col3 = st.columns(3)
        with col1:
            st.metric('Total pekerja',len(self.controller.pegawai_data))
        with col2:
            st.metric('Total posisi',len(self.controller.jabatan_data))
        with col3:
            st.metric('Total admin',len(self.controller.admin_data))
        col1,col2 = st.columns(2)
        with col1:
            self.controller.pie(self.controller.natural_join)
        with col2:
            self.controller.line(self.controller.pegawai_data)
        self.controller.table_admin(self.controller.natural_join,'tidak')
        

    def pegawaiview(self, idadmin):
        self.header('Pegawai')
        editmode = st.toggle(label = "Edit Mode")  
        status = 'tidak'
        if editmode == True:
            status = 'aktif'
        grid = self.controller.table_admin(self.controller.pegawai_data,status)
        selected_rows = grid['selected_rows']
        if editmode == True:
            if not grid.selected_rows:
                with st.form("create_pegawai",clear_on_submit=True):
                    self.nama_pegawai = st.text_input(label='Nama')
                    self.alamat_pegawai = st.text_input(label='Alamat')
                    min_date_of_birth = date.today() - timedelta(days=60*365.25)
                    self.tanggal_lahir_pegawai = st.date_input(label='Tanggal Lahir', min_value = min_date_of_birth)
                    self.jenis_kelamin_pegawai = st.radio(label='Jenis Kelamin', options=["Laki-laki","Perempuan"])
                    self.telepon_pegawai = st.text_input(label='Telepon',help="08xxxxxx")
                    self.email_pegawai = st.text_input(label='Email', help="@email.com")
                    self.admin_id_pegawai = st.text_input(label='Admin', value=idadmin['id'], disabled=True)
                    submitted = st.form_submit_button("Submit") 
                    if submitted:
                        self.controller.createdata_pegawai(self.nama_pegawai, self.alamat_pegawai, self.tanggal_lahir_pegawai, self.jenis_kelamin_pegawai, self.telepon_pegawai, self.email_pegawai, idadmin['id'])
            else:
                id_user = [row.get("id") for row in selected_rows] 
                if len(grid.selected_rows) == 1:
                    with st.form("update_admin",clear_on_submit=False):
                        st.text_input(label="id",placeholder=grid.selected_rows[0]['id'],disabled=True)
                        self.nama_pegawai = st.text_input(label='Nama', value=grid.selected_rows[0]['nama'])
                        self.alamat_pegawai = st.text_input(label='Alamat', value=grid.selected_rows[0]['alamat'])
                        self.tanggal_lahir_pegawai = st.date_input(label='Tanggal Lahir', value= datetime.datetime.strptime(grid.selected_rows[0]['tanggal_lahir'], "%Y-%m-%dT%H:%M:%S.%f").date())
                        self.jenis_kelamin_pegawai = st.radio(label='Jenis Kelamin', options=["Laki-laki","Perempuan"], index=0 if grid.selected_rows[0]['jenis_kelamin'] == "Laki-laki" else 1)
                        self.telepon_pegawai = st.text_input(label='Telepon',help="08xxxxxx", value=grid.selected_rows[0]['telepon'])
                        self.email_pegawai = st.text_input(label='Email', help="@email.com", value=grid.selected_rows[0]['email'])
                        self.admin_id_pegawai = st.text_input(label='Admin', value=idadmin['id'], disabled=True)
                        col1,col2 = st.columns(2)
                        with col1:
                            if len(grid.selected_rows) == 1:           
                                delete_button = st.form_submit_button("Delete")
                                if delete_button:            
                                    self.controller.deletedata_pegawai(id_user)
                        with col2: 
                            if len(grid.selected_rows) == 1:   
                                update_button = st.form_submit_button("Update")
                                if update_button:
                                    self.controller.updatedata_pegawai(str(id_user[0]),self.nama_pegawai, self.alamat_pegawai, self.tanggal_lahir_pegawai, self.jenis_kelamin_pegawai, self.telepon_pegawai, self.email_pegawai, idadmin['id'])
                if len(grid.selected_rows) != 1: 
                    with st.form("update_admin",clear_on_submit=False):  
                        st.write(id_user)
                        delete_button = st.form_submit_button("Delete")
                        if delete_button:            
                            self.controller.deletedata_pegawai(id_user)
        st.markdown("---")
    
    def jabatanview(self):
        self.header('Jabatan')
        editmode = st.toggle(label = "Edit Mode")  
        status = 'tidak'
        if editmode == True:
            status = 'aktif'
        grid = self.controller.table_admin(self.controller.jabatan_data,status)
        selected_rows = grid['selected_rows']
        if editmode == True:
            if not grid.selected_rows:
                with st.form("create_pegawai",clear_on_submit=True):
                    self.nama_jabatan = st.text_input(label='Jabatan')
                    self.deskripsi_jabatan= st.text_area(label='Deskripsi')
                    self.gaji_jabatan = st.number_input(label='Gaji')
                    submitted = st.form_submit_button("Submit") 
                    if submitted:
                        self.controller.createdata_jabatan(self.nama_jabatan,self.deskripsi_jabatan,self.gaji_jabatan)
            else:
                id_user = [row.get("id") for row in selected_rows] 
                if len(grid.selected_rows) == 1:
                    
                    with st.form("update_admin",clear_on_submit=False):
                        st.text_input(label="id",placeholder=grid.selected_rows[0]['id'],disabled=True)
                        self.nama_jabatan = st.text_input(label='Jabatan', value=grid.selected_rows[0]['nama_jabatan'])
                        self.deskripsi_jabatan= st.text_area(label='Deskripsi', value=grid.selected_rows[0]['deskripsi'])
                        self.gaji_jabatan = st.number_input(label='Gaji', value=grid.selected_rows[0]['gaji'])
                        col1,col2 = st.columns(2)
                        with col1:
                            if len(grid.selected_rows) == 1:           
                                delete_button = st.form_submit_button("Delete")
                                if delete_button:            
                                    self.controller.deletedata_jabatan(id_user)
                        with col2: 
                            if len(grid.selected_rows) == 1:   
                                update_button = st.form_submit_button("Update")
                                if update_button:
                                    self.controller.updatedata_jabatan(str(id_user[0]),self.nama_jabatan,self.deskripsi_jabatan,self.gaji_jabatan)
                if len(grid.selected_rows) != 1:  
                    with st.form("update_admin",clear_on_submit=False): 
                        st.write(id_user)
                        delete_button = st.form_submit_button("Delete")
                        if delete_button:            
                            self.controller.deletedata_jabatan(id_user)
        st.markdown("---")
    
    def pegawaiperjabatanview(self):
        self.header('Pegawai per Jabatan')
        angka_122=''
        editmode = st.toggle(label = "Edit Mode")  
        status = 'tidak'
        if editmode == True:
            status = 'aktif'
        grid = self.controller.table_admin(self.controller.pegawai_jabatan_data,status)
        selected_rows = grid['selected_rows']
        if editmode == True:
            if not grid.selected_rows:
                with st.form("create_pegawai",clear_on_submit=True):
                    options_id_pegawai = list(map(tuple, self.controller.pegawai_data[['id', 'nama']].values))
                    self.id_pegawai = st.selectbox(label='id_pegawai', options=options_id_pegawai, format_func=lambda x: f"{x[0]} - {x[1]}" if x is not None and len(x) == 2 else "")
                    options_id_jabatan = list(map(tuple, self.controller.jabatan_data[['id', 'nama_jabatan']].values))
                    self.id_jabatan = st.selectbox(label='id_jabatan', options=options_id_jabatan,format_func=lambda x: f"{x[0]} - {x[1]}" if x is not None and len(x) == 2 else "")
                    submitted = st.form_submit_button("Submit") 
                    if submitted:
                        
                        self.controller.createdata_pegawaiperjabatan(self.id_pegawai,self.id_jabatan)
            else:
                ids = [row.get("id") for row in selected_rows] 
                if len(grid.selected_rows) == 1:
                    with st.form("update_admin",clear_on_submit=False):
                        st.text_input(label="id",placeholder=grid.selected_rows[0]['id'],disabled=True)
                        self.id_pegawai = st.text_input(label='id_pegawai', value=grid.selected_rows[0]['id_pegawai'])
                        self.id_jabatan = st.text_input(label='id_jabatan', value=grid.selected_rows[0]['id_jabatan'])
                        col1,col2 = st.columns(2)
                        with col1:
                            if len(grid.selected_rows) == 1:           
                                delete_button = st.form_submit_button("Delete")
                                if delete_button:            
                                    self.controller.deletedata_pegawaiperjabatan(ids)
                        with col2: 
                            if len(grid.selected_rows) == 1:   
                                update_button = st.form_submit_button("Update")
                                if update_button:
                                    self.controller.updatedata_pegawaiperjabatan(str(ids[0]),self.id_pegawai,self.id_jabatan)
                    
                if len(grid.selected_rows) != 1:   
                    with st.form("update_admin",clear_on_submit=False):
                        st.write(ids)
                        delete_button = st.form_submit_button("Delete")
                        if delete_button:            
                            self.controller.deletedata_pegawaiperjabatan(ids)
        st.markdown("---")
    
    
    def adminview(self):
        self.header('Admin')
        editmode = st.toggle(label = "Edit Mode")  
        status = 'tidak'
        if editmode == True:
            status = 'aktif'
        grid = self.controller.table_admin(self.controller.admin_data,status)
        selected_rows = grid['selected_rows']
        if editmode == True:
            if not grid.selected_rows:
                with st.form("create_admin",clear_on_submit=True):
                    self.username_user = st.text_input(label='Username')
                    self.password_user = st.text_input(label='Password', type='password')
                    submitted = st.form_submit_button("Submit")  
                    if submitted:
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.username_user):
                            st.warning('Invalid email address')
                        else:
                            self.controller.createdata_admin(self.username_user,self.password_user
                            )
            else:
                id_user = [row.get("id") for row in selected_rows] 
                if len(grid.selected_rows) == 1:
                    with st.form("update_admin",clear_on_submit=False):
                        st.text_input(label="id",placeholder=grid.selected_rows[0]['id'],disabled=True)
                        self.username_user = st.text_input(label='Username',value=grid.selected_rows[0]['username'])
                        self.password_user = st.text_input(label='Password', type='password',value=grid.selected_rows[0]['password_hash'])
                        col1,col2 = st.columns(2)
                        with col1:
                                if len(grid.selected_rows) == 1:           
                                    delete_button = st.form_submit_button("Delete")
                                    if delete_button:            
                                        self.controller.deletedata_admin(id_user)
                        with col2: 
                            if len(grid.selected_rows) == 1:   
                                update_button = st.form_submit_button("Update")
                                if update_button:
                                    if not re.match(r"[^@]+@[^@]+\.[^@]+", self.username_user):
                                        st.warning('Invalid email address')
                                    else:
                                        self.controller.updatedata_admin(str(id_user[0]),self.username_user,self.password_user)
                    
                if len(grid.selected_rows) != 1:   
                    with st.form("update_admin",clear_on_submit=False):
                        st.write(id_user)
                        delete_button = st.form_submit_button("Delete")
                        if delete_button:            
                            self.controller.deletedata_admin(id_user)
        st.markdown("---")
    
    def pengaturanview(self):
        self.header('Pengaturan')
        now = datetime.datetime.now()
        login_status, user_info = st.session_state.login
        edit = st.toggle('Edit Profile')
        if edit:
            editmode = False
        else:
            editmode = True
        with st.form("edit_myuser"):            
            self.username_user = st.text_input(label='Username',value=user_info['username'],disabled=editmode)
            self.password_user = st.text_input(label='Password',value=user_info['password'] , type='password',disabled=editmode)
            self.update_at_input_user = now.strftime("%Y-%m-%d %H:%M:%S")
            submitted = st.form_submit_button('Submit',disabled=editmode)
            if submitted:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", self.username_user):
                    st.warning('Invalid email address')
                elif len(self.password_user) < 8:  # Adjust the minimum password length as needed
                    st.warning('Password must be at least 8 characters long')
                else:
                    st.session_state.update = self.controller.update_myuser(self.username_user,self.password_user,self.update_at_input_user,user_info['id'])

        if login_status == 'berhasil':
            if st.button('Logout'):
                  # Check if the Logout button is clicked
                st.session_state.login = ""  # Clear the login session state
                st.experimental_rerun()
                
        else:
            st.warning("Login gagal. Mohon cek kembali email dan password.")
        
        with st.expander("See Credits"):
            st.header('Nama : Muhammad Ilham Gymnastiar')
            st.header('Nim  : 10121124')
            st.header('Kelas : IF 4')
        st.markdown("---")

    