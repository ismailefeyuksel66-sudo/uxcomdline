#!/usr/bin/env python3
import sys
import os
import base64
import zlib

# Uygulamaların şifrelenip saklanacağı ana dizin
APP_DIR = os.path.expanduser("~/.uxcomdline_apps")
if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)

def encrypt_code(code: str) -> bytes:
    """Kodu sıkıştırır ve Base64 ile şifreler."""
    compressed = zlib.compress(code.encode('utf-8'))
    return base64.b64encode(compressed)

def decrypt_code(encrypted_data: bytes) -> str:
    """Şifrelenmiş kodu çözer ve metin haline getirir."""
    compressed = base64.b64decode(encrypted_data)
    return zlib.decompress(compressed).decode('utf-8')

def print_help():
    print("uxcomdline - Application Container & Runner")
    print("Usage:")
    print("  uxcomdline --help                       : Show all available commands.")
    print("  uxcomdline --download <file> <appname>  : Download/Install and encrypt a python script.")
    print("  uxcomdline --list                       : List all installed applications.")
    print("  uxcomdline --remove <appname>           : Remove a specific installed application.")
    print("  uxcomdline <appname>                    : Run the specified application.")

def download_app(source_file, app_name):
    if not os.path.exists(source_file):
        print(f"File '{source_file}' not found.")
        return
        
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Kodu şifrele ve sisteme kaydet
        encrypted = encrypt_code(code)
        app_path = os.path.join(APP_DIR, f"{app_name}.ux")
        
        with open(app_path, 'wb') as f:
            f.write(encrypted)
            
        print(f'The application has been downloaded; to use it, run "uxcomdline {app_name}"')
    except Exception as e:
        print(f"Error during installation: {e}")

def run_app(app_name):
    app_path = os.path.join(APP_DIR, f"{app_name}.ux")
    
    if os.path.exists(app_path):
        try:
            with open(app_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Şifreyi çöz ve hafızada çalıştır (diskte açık kod kalmaz)
            code = decrypt_code(encrypted_data)
            exec(code, globals())
            
        except Exception as e:
            print(f"Application '{app_name}' crashed during execution: {e}")
    else:
        print('No such command exists; use "uxcomdline --help" to learn the commands')

def main():
    if len(sys.argv) < 2:
        print('No such command exists; use "uxcomdline --help" to learn the commands')
        return

    command = sys.argv[1]

    if command == "--help":
        print_help()
    elif command == "--download":
        if len(sys.argv) == 4:
            download_app(sys.argv[2], sys.argv[3])
        else:
            print('No such command exists; use "uxcomdline --help" to learn the commands')
    elif command == "--list":
        # Ekstra Özellik: Yüklü uygulamaları listele
        apps = [f[:-3] for f in os.listdir(APP_DIR) if f.endswith('.ux')]
        print("Installed applications:")
        for app in apps:
            print(f"  -> {app}")
        if not apps:
            print("  (No applications installed yet.)")
    elif command == "--remove":
        # Ekstra Özellik: Uygulama sil
        if len(sys.argv) == 3:
            app_name = sys.argv[2]
            app_path = os.path.join(APP_DIR, f"{app_name}.ux")
            if os.path.exists(app_path):
                os.remove(app_path)
                print(f"Application '{app_name}' has been removed successfully.")
            else:
                print(f"Application '{app_name}' not found.")
        else:
             print('No such command exists; use "uxcomdline --help" to learn the commands')
    elif command.startswith("-"):
        print('No such command exists; use "uxcomdline --help" to learn the commands')
    else:
        run_app(command)

if __name__ == "__main__":
    main()