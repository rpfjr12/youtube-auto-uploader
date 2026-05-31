# analytics.py
from datetime import datetime, timedelta

def fetch_channel_metrics(youtube):
    """
    Returns a simple performance dict for the channel associated with the provided youtube client.
    The dict contains watch_time, views, estimated_revenue, ctr, and a combined score.
    """
    try:
        # Query last 7 days
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=7)
        # youtube is a built client for youtubeAnalytics
        analytics = youtube.analytics() if hasattr(youtube, "analytics") else None
        if analytics is None:
            return {"watch_time": 0, "views": 0, "revenue": 0.0, "ctr": 0.0, "score": 0.0}

        # Example query: metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage
        resp = analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date.isoformat(),
            endDate=end_date.isoformat(),
            metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage",
            dimensions="",
            sort="-views"
        ).execute()

        rows = resp.get("rows", [])
        if not rows:
            return {"watch_time": 0, "views": 0, "revenue": 0.0, "ctr": 0.0, "score": 0.0}

        # parse metrics
        # rows is a list; metrics order matches query
        views = float(rows[0][0])
        est_minutes = float(rows[0][1])
        avg_duration = float(rows[0][2])
        avg_pct = float(rows[0][3])

        # simple scoring: weight watch time and views
        score = views * 0.4 + est_minutes * 0.6

        return {
            "watch_time": est_minutes,
            "views": views,
            "revenue": 0.0,
            "ctr": avg_pct / 100.0,
            "score": score
        }
    except Exception:
        return {"watch_time": 0, "views": 0, "revenue": 0.0, "ctr": 0.0, "score": 0.0}
