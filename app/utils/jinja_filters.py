# utils/jinja_filters.py
def register_filters(app):
    @app.template_filter('datetime')
    def format_datetime(value, fmt="%d %b %Y"):
        if not value:
            return ""
        try:
            return value.strftime(fmt)
        except Exception:
            return str(value)
