# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""
import os
import sys

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'FireBird' + os.sep + 'lib' + os.sep
sys.path.append(cur_path)

import fdb

# Globals declared here
global mod_sqlserver_sessions
# Default declared here
SESSION_DEFAULT = "default"
global sesion
# Initialize settings for the module here
try:
    if not mod_sqlserver_sessions:
        mod_sqlserver_sessions = {SESSION_DEFAULT: {}}
except NameError:
    mod_sqlserver_sessions = {SESSION_DEFAULT: {}}



"""
    Obtengo el modulo que fue invocado
"""
module = GetParams("module")

try:
    if module == "connect":
        dns_ = GetParams('dns_')
        user_ = GetParams('user_')
        pass_ = GetParams('pass_')
        session_ = ""
        var_ = GetParams('var_')

        if not session_:
            session_ = SESSION_DEFAULT

        con = fdb.connect(
             dsn = dns_,
             user = user_, password = pass_,
             charset='UTF8' # specify a character set for the connection
            )
        cursor = con.cursor()
        mod_sqlserver_sessions[session_] = {
            "connection": con,
            "cursor": cursor,
            "engine": None,
        }
        sesion = session_
        SetVar(var_,True)

    if module == "query":
        query_ = GetParams('query_')
        var_ = GetParams('var_')
        session_ = ""


        if not session_:
            session = SESSION_DEFAULT

        cursor = mod_sqlserver_sessions[session]["cursor"]
        con = mod_sqlserver_sessions[session]["connection"]

       # Execute the SELECT statement:
        cursor.execute(query_)
        SetVar(var_,cursor.fetchall())
    
    if module == "update":
        query_ = GetParams('query_')
        var_ = GetParams('var_')
        session_ = ""


        if not session_:
            session = SESSION_DEFAULT

        cursor = mod_sqlserver_sessions[session]["cursor"]
        con = mod_sqlserver_sessions[session]["connection"]
        
        # Execute the UPDATE statement:
        try:
            cursor.execute(query_)
            con.commit()
            SetVar(var_,True)
        except:
            SetVar(var_,False)
        
    if module == "create":

        nombre_ = GetParams('nombre_')
        campo_ = GetParams('campo_')
        var_ = GetParams('var_')
        session_ = ""

        if not session_:
            session = SESSION_DEFAULT

        cursor = mod_sqlserver_sessions[session]["cursor"]
        con = mod_sqlserver_sessions[session]["connection"]

        # Execute the SELECT statement:
        cursor.execute("CREATE TABLE "+nombre_+"("+campo_+")")
        con.commit()

    if module == "insert":

        nombre_ = GetParams('nombre_')
        value_ = GetParams('value_')
        colum_ = GetParams('colum_')
        var_ = GetParams('var_')
        session_ = ""

        if not session_:
            session = SESSION_DEFAULT

        cursor = mod_sqlserver_sessions[session]["cursor"]
        con = mod_sqlserver_sessions[session]["connection"]

        # Execute the SELECT statement:
        cursor.execute("INSERT INTO "+nombre_+" ("+colum_+") values("+value_+")")
        con.commit()

    if module == "delete":

        nombre_ = GetParams('nombre_')
        var_ = GetParams('var_')
        session_ = ""

        if not session_:
            session = SESSION_DEFAULT

        cursor = mod_sqlserver_sessions[session]["cursor"]
        con = mod_sqlserver_sessions[session]["connection"]

        # Execute the SELECT statement:
        try:
            cursor.execute("DROP TABLE "+nombre_)
            con.commit()
            SetVar(var_,True)
        except:
            SetVar(var_,False)

    if module == "select":

        nombre_ = GetParams('nombre_')
        var_ = GetParams('var_')
        session_ = ""

        if not session_:
            session = SESSION_DEFAULT

        cursor = mod_sqlserver_sessions[session]["cursor"]
        con = mod_sqlserver_sessions[session]["connection"]

        # Execute the SELECT statement:
        try:
            cursor.execute("SELECT * FROM "+nombre_)
            SetVar(var_,cursor.fetchall())
        except:
            SetVar(var_,False)

    if module == "close":
        session_ = ""
        if not session_:
            session = SESSION_DEFAULT

        con = mod_sqlserver_sessions[session]["connection"]
        con.close()
        mod_sqlserver_sessions[session] = {}

except Exception as e:
    PrintException()
    raise e


