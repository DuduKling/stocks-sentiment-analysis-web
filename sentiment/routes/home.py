from flask import render_template

def main():
    return render_template(
        'form.html',
        page = 'home'
    )
