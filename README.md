# AWS Pattern master/manager  

Diseño de programa para plantear el patrón master/manager sobre AWS IAM.
El ejercicio consiste en plantear una solución donde los usuarios maestro y manager puedan operar
sobre distintos recursos en gestión de usuarios, además de proporcionar funcionalidad para usuarios de distintos tipos
que tendrán características básicas para obtener la información necesaria para acceder al servicio de AWS STS.  

Pongamos el caso de un usuario que trabaja en una aplicación java que necesita acceder a AWS S3, en cuyo caso no dispondrá
de claves de acceso permanentes sino que hará uso de AWS STS para asumir un rol temporal con el que trabajará en la aplicación.  

Así unicamente exponemos credenciales básicas con permisos limitados sobre unas pocas opciones de boto3 con el fin de poder llegar
a obtener la credenciales temporales.  

También se plantea el diseño de seguridad ABAC como medida de control de acceso a recursos.  
