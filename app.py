from flask import Flask, request
from graph import get_bode_plot_blob

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    """
    
    """
    numerador = request.args.get('numerador', type=str)
    denominador = request.args.get('denominador', type=str)
    blob = ""
    if not ((not numerador) or (not denominador)):
        blob = get_bode_plot_blob(numerador, denominador)#"3*s**2 + 2s", "2*s^3 - 3*s**2 + s - 4")
    
    return f"""
<form action="http://localhost:5000/" method="GET">
        <label for="numerador">Numerador:</label><br>
        <input type="text" id="numerador" name="numerador" value="{numerador}"required><br><br>
        
        <label for="denominador">Denominador:</label><br>
        <input type="text" id="denominador" name="denominador"  value="{denominador}"required><br><br>
        
        <input type="submit" value="Enviar">
    </form>

    <img src="data:image/png;base64, {blob}" alt="">
"""

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)
