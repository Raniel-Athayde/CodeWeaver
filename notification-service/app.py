from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Log em memória (em produção seria um banco de dados ou fila)
events_log = []

@app.route('/log', methods=['POST'])
def log_event():
    try:
        data = request.get_json()
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": data.get("event_type"),
            "payload": data.get("payload")
        }
        events_log.append(event)
        
        # Print do evento
        print(f"[LOG] {event['event_type']} - {event['payload']}")
        
        return jsonify({
            "success": True,
            "event_id": len(events_log)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    """Retorna os últimos eventos registrados"""
    limit = request.args.get('limit', 50, type=int)
    return jsonify({
        "total": len(events_log),
        "events": events_log[-limit:]
    })

@app.route('/events/clear', methods=['DELETE'])
def clear_events():
    """Limpa os eventos (apenas para testes)"""
    global events_log
    events_log = []
    return jsonify({"success": True, "message": "Events cleared"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "notification-service",
        "events_count": len(events_log)
    }), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5006))
    app.run(debug=True, host='0.0.0.0', port=port)
