

from flask import Flask, render_template, request, redirect, url_for

from scraper import scrape_all
from ai_analyzer import enrich_records
from database import save_records, load_records, export_csv

app = Flask(__name__)


@app.route("/")
def index():
    df = load_records()
    sentiment_filter = request.args.get("sentiment", "All")
    search = request.args.get("q", "").strip().lower()

    if not df.empty:
        if sentiment_filter != "All":
            df = df[df["sentiment"] == sentiment_filter]
        if search:
            df = df[df["text"].str.lower().str.contains(search) |
                     df["author"].str.lower().str.contains(search)]

    return render_template(
        "index.html",
        records=df.to_dict(orient="records"),
        count=len(df),
        sentiment_filter=sentiment_filter,
        search=search,
    )


@app.route("/scrape", methods=["POST"])
def scrape():
    """Run the full pipeline: scrape -> analyze -> save."""
    pages = int(request.form.get("pages", 3))
    raw_records = scrape_all(max_pages=pages)
    enriched = enrich_records(raw_records)
    save_records(enriched)
    return redirect(url_for("index"))


@app.route("/export")
def export():
    export_csv()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
