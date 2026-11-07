"""Local, free AI recommendation feature."""
from flask import jsonify, request
from flask_appbuilder import BaseView, expose, has_access
from flask_login import login_required
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app import app, appbuilder, db
from app.models import Client, Discipline, Enrollment


def recommend_disciplines(client_id: int, limit: int = 3):
    """Recommend disciplines using a local TF-IDF content model.

    The model compares the client's stated goal with each discipline's name,
    category, schedule and description. Existing enrollments are excluded.
    """
    client = db.session.get(Client, client_id)
    if not client:
        return None, []
    disciplines = db.session.query(Discipline).order_by(Discipline.name).all()
    enrolled_ids = {
        enrollment.discipline_id
        for enrollment in client.enrollments
        if enrollment.status == "Activa"
    }
    available = [discipline for discipline in disciplines if discipline.id not in enrolled_ids]
    if not available:
        return client, []

    corpus = [client.goal] + [
        f"{item.name} {item.category} {item.schedule} {item.description}" for item in available
    ]
    vectorizer = TfidfVectorizer(lowercase=True, strip_accents="unicode")
    matrix = vectorizer.fit_transform(corpus)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    ranked = sorted(zip(available, scores), key=lambda pair: pair[1], reverse=True)
    return client, [(discipline, round(float(score), 4)) for discipline, score in ranked[:limit]]


class AIRecommendationView(BaseView):
    route_base = "/ai"
    default_view = "recommendations"

    @expose("/recommendations")
    @has_access
    def recommendations(self):
        clients = db.session.query(Client).order_by(Client.full_name).all()
        selected_id = request.args.get("client_id", type=int)
        client, recommendations = (None, [])
        if selected_id:
            client, recommendations = recommend_disciplines(selected_id)
        return self.render_template(
            "ai/recommendations.html",
            clients=clients,
            selected_id=selected_id,
            client=client,
            recommendations=recommendations,
        )


appbuilder.add_view(AIRecommendationView(), "Recomendador IA", icon="fa-magic", category="Inteligencia Artificial")


@app.route("/api/ai/recommendations/<int:client_id>")
@login_required
def recommendation_api(client_id):
    """Return the same AI result as JSON for integrations and demonstrations."""
    client, recommendations = recommend_disciplines(client_id)
    if client is None:
        return jsonify({"error": "Cliente no encontrado"}), 404
    return jsonify(
        {
            "client_id": client.id,
            "client": client.full_name,
            "goal": client.goal,
            "recommendations": [
                {
                    "discipline_id": discipline.id,
                    "discipline": discipline.name,
                    "category": discipline.category,
                    "score": score,
                }
                for discipline, score in recommendations
            ],
        }
    )
