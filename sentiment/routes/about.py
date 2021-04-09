from flask import render_template

def main():
    return render_template(
        'about.html',
        page = 'about'
    )
