
### BUILDER

# Démarrer une image avec Node.js pour compiler l'application
FROM node:22-alpine as builder 

# Définir le répertoire de travail
WORKDIR /app

# Copier les manifeste pour profiter du cache Docker 
COPY package.json package-lock.json ./

# Installer les dépendances à partir du lockfile
RUN npm ci 

# Copier le reste des fichiers
COPY . . 

# Construire l'application en compilant le code en fichier statiques optimisés
RUN npm run build 


### SERVER

# Image Nginx minimale pour servir les fichiers statiques
FROM nginx:alpine

# Copier les artefacts construits (HTML/CSS/JS minifiés) depuis le builder vers le dossier web de Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# copier le fichier nginx.conf dans l'image docker a l'endroit ou nginx lit sa conf par defaut pour mieux servir l'application 
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Commande de demarrage de nginx
CMD ["nginx", "-g", "daemon off;"]

