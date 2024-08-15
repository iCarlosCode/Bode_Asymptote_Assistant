from flask import Flask, request, render_template
from graph2 import get_bode_plot_blob

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    """
    
    """
    numerador = request.args.get('numerador', type=str)
    denominador = request.args.get('denominador', type=str)
    if numerador is None:
        numerador = ""
    if denominador is None:
        denominador = ""
    blob = "iVBORw0KGgoAAAANSUhEUgAAA2wAAAAsCAYAAAAZ3DugAAAABHNCSVQICAgIfAhkiAAAABl0RVh0U29mdHdhcmUAZ25vbWUtc2NyZWVuc2hvdO8Dvz4AAAAmdEVYdENyZWF0aW9uIFRpbWUAcXVhIDE0IGFnbyAyMDI0IDIzOjQ5OjM360aDOgAAARVJREFUeJzt1zEBACAMwDDAv+dhgJ8eiYK+3TMzCwAAgJzzOwAAAIA3wwYAABBl2AAAAKIMGwAAQJRhAwAAiDJsAAAAUYYNAAAgyrABAABEGTYAAIAowwYAABBl2AAAAKIMGwAAQJRhAwAAiDJsAAAAUYYNAAAgyrABAABEGTYAAIAowwYAABBl2AAAAKIMGwAAQJRhAwAAiDJsAAAAUYYNAAAgyrABAABEGTYAAIAowwYAABBl2AAAAKIMGwAAQJRhAwAAiDJsAAAAUYYNAAAgyrABAABEGTYAAIAowwYAABBl2AAAAKIMGwAAQJRhAwAAiDJsAAAAUYYNAAAgyrABAABEGTYAAIAowwYAABBl2AAAAKIutCwEVBPWGVIAAAAASUVORK5CYII="
    if not ((not numerador) or (not denominador)):
        blob = get_bode_plot_blob(numerador, denominador)#"3*s**2 + 2s", "2*s^3 - 3*s**2 + s - 4")
    
    return render_template("index.html", numerador=numerador, denominador=denominador, blob=blob)

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)
