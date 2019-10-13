# Central de Erros
----

Em projetos modernos é cada vez mais comum o uso de arquiteturas baseadas em serviços ou microsserviços. Nestes ambientes complexos, erros podem surgir em diferentes camadas da aplicação (backend, frontend, mobile, desktop) e mesmo em serviços distintos. Desta forma, é muito importante que os desenvolvedores possam centralizar todos os registros de erros em um local, de onde podem monitorar e tomar decisões mais acertadas. Neste projeto vamos implementar um sistema para centralizar registros de erros de aplicações.


## Instruções de instalação:

1. Install the project requirements:

    ```bash
    python3.6 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

<!-- python3 manage.py makemigrations api -->
python3 manage.py migrate