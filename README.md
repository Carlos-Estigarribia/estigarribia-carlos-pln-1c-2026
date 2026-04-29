# estigarribia-carlos-pln-1c-2026
# .venv\Scripts\Activate.ps1

git pull origin main
# editar o agregar archivos
git status
git add .
git commit -m "Mensaje descriptivo"
git push origin main

# Qué hace cada git:
git status          >muestra qué cambió;
git add .            >prepara los archivos para el commit;
git commit -m "..."   >guarda un punto de control local con mensaje;
git push origin main   >publica esos cambios en GitHub.