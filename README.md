# Project Blog

Blog interativo e totalmente customizável, onde novas páginas e componentes como Tags e Categorias podem ser adicionadas diretamente pela área administrativa do Django, pelo usuário da aplicação, sem a necessidade de modificar seções no HTML. Em desenvolvimento o projeto foi otimizado para trabalhar com Docker e PostgreSQL, já em produção, todo o processo foi feito utilizando como meio de hospedagem, o Google Cloud.

Para utilizar o aplicativo Django, lembre-se de instalar as dependências presentes no arquivo "requirements.txt", ao fazer isso, siga os seguintes passos:

* Configure o seu ".env" e os locais em "settings.py" onde o enviroment é utilizado;

* O aplicativo em desenvolvimento está configurado para utilizar Docker, portanto instale-o também, caso contrário, configure o banco de sua escolha;

Primeiramente, crie o seu super-usuário, que será utilizado para acessar o ambiente administrativo do Django:

```
python(sua-versao) manage.py createsuperuser
```

Em casos de divergência com o uso do Docker, para iniciar a aplicação execute os seguintes comandos, para inicializar um servidor local de desenvolvimento em seu localhost:

```
python(sua-versao) manage.py makemigrations
python(sua-versao) manage.py migrate
python(sua-versao) manage.py runserver
``` 

Caso contrário, inicialize o Docker com o comando abaixo, isto irá executar os scripts contidos na pasta "scripts", servindo a aplicação em seu localhost, em estado de desenvolvimento:

```
docker compose up
```
