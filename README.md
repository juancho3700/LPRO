# Como programar una placa nRF

1. Instalar la extensión **nRF Connect for VS Code Extension Pack** en Visual Studio Code.
2. Instalar [nRF Command Line Tool](https://www.nordicsemi.com/Products/Development-tools/nRF-Command-Line-Tools/Download).
3. Entrar en el menú de la extensión de nRF (*Ctrl+Alt+N*).
4. Pulsar en el botón *Install Toolchain* y seleccionar la última versión.
5. Pulsar en el botón *Manage SDKs* y seleccionar la última versión.
6. Pulsar en el botón *Open an existing application* y abrir la carpeta **nRFchat**.
7. Conectar la placa que quieras programar al ordenador. Si la extensión la detecta en el submenú *CONNECTED DEVICES* debería aparecer una entrada con un número (el número que está apuntado en la pegatina blanca de la placa).
8. Seleccionar en el submenú *APPLICATIONS* la build respectiva a la placa que estés usando (para la grande *build* y para la pequeña *build_1*). Si está seleccionada correctamente se pondrá en azul.
9. En el submenú *ACTIONS* pulsar en el botón *build* y en cuanto termine en el botón *flash*.