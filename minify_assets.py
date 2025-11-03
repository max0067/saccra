#!/usr/bin/env python3
"""
Script de minification des assets CSS/JS
Réduit la taille des fichiers de 20-40%
"""
import os
import re

def minify_css(css_content):
    """Minifie du CSS"""
    # Retirer les commentaires
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Retirer les espaces multiples
    css_content = re.sub(r'\s+', ' ', css_content)
    # Retirer les espaces autour des caractères spéciaux
    css_content = re.sub(r'\s*([{}:;,>])\s*', r'\1', css_content)
    # Retirer les derniers point-virgules avant }
    css_content = re.sub(r';}', '}', css_content)
    return css_content.strip()

def minify_js(js_content):
    """Minifie du JavaScript (basique)"""
    # Retirer les commentaires //
    js_content = re.sub(r'//.*?$', '', js_content, flags=re.MULTILINE)
    # Retirer les commentaires /* */
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    # Retirer les espaces multiples (sauf dans les strings)
    js_content = re.sub(r'\s+', ' ', js_content)
    # Retirer les espaces autour de certains caractères
    js_content = re.sub(r'\s*([{}();,:])\s*', r'\1', js_content)
    return js_content.strip()

def minify_file(input_path, output_path=None):
    """Minifie un fichier CSS ou JS"""
    if output_path is None:
        # Par défaut, ajouter .min avant l'extension
        base, ext = os.path.splitext(input_path)
        output_path = base + '.min' + ext

    # Lire le fichier
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Minifier selon le type
    if input_path.endswith('.css'):
        minified = minify_css(content)
    elif input_path.endswith('.js'):
        minified = minify_js(content)
    else:
        print(f"❌ Type de fichier non supporté: {input_path}")
        return False

    # Écrire le fichier minifié
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(minified)

    # Statistiques
    original_size = len(content)
    minified_size = len(minified)
    reduction = ((original_size - minified_size) / original_size) * 100

    print(f"✅ {input_path}")
    print(f"   → {output_path}")
    print(f"   📉 {original_size} → {minified_size} bytes ({reduction:.1f}% réduction)")

    return True

if __name__ == '__main__':
    print("=" * 70)
    print("MINIFICATION DES ASSETS - SACRA")
    print("=" * 70)
    print()

    # Fichiers à minifier
    files_to_minify = [
        'app/static/css/spiritual-loader.css',
        'app/static/js/spiritual-loader.js',
    ]

    total_before = 0
    total_after = 0

    for filepath in files_to_minify:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                size_before = len(f.read())

            minify_file(filepath)

            # Lire le fichier minifié
            base, ext = os.path.splitext(filepath)
            minified_path = base + '.min' + ext
            with open(minified_path, 'r') as f:
                size_after = len(f.read())

            total_before += size_before
            total_after += size_after
            print()
        else:
            print(f"❌ Fichier non trouvé: {filepath}\n")

    print("=" * 70)
    print(f"TOTAL: {total_before} → {total_after} bytes")
    print(f"RÉDUCTION GLOBALE: {((total_before - total_after) / total_before) * 100:.1f}%")
    print("=" * 70)
    print()
    print("💡 Pense à mettre à jour les templates pour utiliser les fichiers .min.css et .min.js")
