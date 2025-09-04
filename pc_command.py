import os
import json
from subprocess import Popen
import winreg
import urllib.parse

class PcCommand():
    def __init__(self):
        self.browser_cache_file = "browser_cache.json"
        self.cached_browser = self._load_cached_browser()
        
    def _load_cached_browser(self):
        """Cargar el navegador cacheado si existe"""
        try:
            if os.path.exists(self.browser_cache_file):
                with open(self.browser_cache_file, 'r') as f:
                    data = json.load(f)
                    if os.path.exists(data['path']):
                        print(f"Usando navegador cacheado: {data['name']} en {data['path']}")
                        return data
        except Exception as e:
            print(f"Error al cargar cache del navegador: {e}")
        return None

    def _save_browser_cache(self, browser_info):
        """Guardar la información del navegador encontrado"""
        try:
            with open(self.browser_cache_file, 'w') as f:
                json.dump(browser_info, f)
            print(f"Navegador guardado en cache: {browser_info['name']}")
        except Exception as e:
            print(f"Error al guardar cache del navegador: {e}")

    def _find_browser(self):
        """Buscar un navegador instalado en el sistema"""
        # Lista de posibles navegadores y sus ubicaciones comunes
        browsers = [
            {
                'name': 'Chrome',
                'paths': [
                    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                ]
            },
            {
                'name': 'Firefox',
                'paths': [
                    r'C:\Program Files\Mozilla Firefox\firefox.exe',
                    r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
                ]
            },
            {
                'name': 'Edge',
                'paths': [
                    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
                ]
            }
        ]

        # Primero buscar en las rutas comunes
        for browser in browsers:
            for path in browser['paths']:
                if os.path.exists(path):
                    return {'name': browser['name'], 'path': path}

        # Si no se encuentra, buscar en el registro de Windows
        try:
            for browser in ['Chrome', 'Firefox', 'Edge', 'Brave']:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                      rf'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{browser}.exe', 
                                      0, winreg.KEY_READ) as key:
                        path = winreg.QueryValue(key, None)
                        if os.path.exists(path):
                            return {'name': browser, 'path': path}
                except WindowsError:
                    continue
        except Exception as e:
            print(f"Error al buscar en el registro: {e}")

        return None

    def _process_url(self, website):
        """Procesar y formatear la URL correctamente"""
        if not website:
            return "about:blank"
            
        # Si no tiene protocolo, agregar https://
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
            
        # Si es solo un dominio sin extensión, agregar .com
        if '.' not in urllib.parse.urlparse(website).netloc:
            website = website.rstrip('/') + '.com'
            
        return website

    def open_chrome(self, website):
        """Abrir una URL en el navegador disponible"""
        try:
            # Intentar usar el navegador cacheado primero
            browser = self.cached_browser
            
            # Si no hay navegador cacheado, buscar uno
            if not browser:
                print("Buscando navegador instalado...")
                browser = self._find_browser()
                if browser:
                    self._save_browser_cache(browser)
                    
            if not browser:
                raise Exception("No se encontró ningún navegador instalado")
            
            # Procesar la URL
            processed_url = self._process_url(website)
            print(f"Abriendo {processed_url} en {browser['name']}...")
            
            # Abrir el navegador con la URL
            Popen([browser['path'], processed_url])
            return True
            
        except Exception as e:
            print(f"Error al abrir el navegador: {e}")
            return False