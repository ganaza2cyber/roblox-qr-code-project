from flask import Flask, request, jsonify
import qrcode

app = Flask(__name__)

@app.route('/qrcode', methods=['GET'])
def get_qr():
    text = request.args.get('text', 'hello')
    print(f"Received request to generate QR for: '{text}'")
    
    try:
        # Use explicit configuration to guarantee a stable matrix layout
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=1,
            border=0, # We handle the quiet zone inside Roblox
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Extract raw boolean grid matrix
        raw_matrix = qr.get_matrix()
        
        # Ensure it's fully mapped as standard Python booleans for JSON serialization
        matrix = [[bool(cell) for cell in row] for row in raw_matrix]
        
        print(f"Successfully generated matrix of size {len(matrix)}x{len(matrix)}")
        return jsonify({"success": True, "matrix": matrix})
        
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
