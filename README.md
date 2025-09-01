# mcp
Démonstration du protocole MCP pour l'IA générative

Installer les dépendances (requirements.txt)

Copier le fichier Python en local et noter son chemin absolu.

Un sous-répertoire tmp doit exister dans le dossier C:\users\<NOM>

Ajouter la définition du serveur MCP. Exemple pour Claude Desktop :
{
  "mcpServers": {
	"methodidacte_blog_scraper": {
	  "command": "python",
	  "args": ["C:\\Users\\<NOM>\\<CHEMIN_COMPLET>\\methodidacte_web_mcp_server.py"]
	}
}
